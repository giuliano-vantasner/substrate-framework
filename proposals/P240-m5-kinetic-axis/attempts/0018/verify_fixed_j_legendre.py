"""Exact fixed-J reduction of the full P240 alternating-sextic term."""

from __future__ import annotations

import sympy as sp

from substrate_framework.m5_kinetic_axis import (
    spatial_covariant_metric_from_timelike_projector,
)
from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P240/alternating-fixed-J")
    rapidity, omega, b0 = sp.symbols("rapidity omega B_0", real=True)
    spatial_current, kappa, momentum = sp.symbols("b kappa J", positive=True)
    eta = sp.diag(-1, 1, 1, 1)
    projector_rest = sp.diag(1, 0, 0, 0)
    boost = sp.eye(4)
    boost[0, 0] = boost[3, 3] = sp.cosh(rapidity)
    boost[0, 3] = boost[3, 0] = sp.sinh(rapidity)
    projector_t = boost.inv() * projector_rest * boost
    spatial_metric = spatial_covariant_metric_from_timelike_projector(
        projector_t, eta
    )
    alternating = sp.Matrix((b0, 0, 0, omega * spatial_current))
    lagrangian = sp.factor(
        kappa * (alternating.T * spatial_metric * alternating)[0]
    )
    static_piece = sp.factor(lagrangian.subs(omega, 0))
    linear_piece = sp.factor(sp.diff(lagrangian, omega).subs(omega, 0) / 2)
    inertia = sp.factor(sp.diff(lagrangian, omega, 2) / 2)
    ledger.check(
        "dynamic q gives the exact constant linear and quadratic clock pieces",
        static_piece == kappa * b0**2 * sp.sinh(rapidity) ** 2
        and sp.trigsimp(
            linear_piece
            - kappa
            * b0
            * spatial_current
            * sp.sinh(rapidity)
            * sp.cosh(rapidity)
        )
        == 0
        and sp.trigsimp(
            inertia
            - kappa * spatial_current**2 * sp.cosh(rapidity) ** 2
        )
        == 0,
    )
    ledger.check(
        "the declared clock polynomial reconstructs the full density",
        sp.simplify(
            lagrangian
            - (static_piece + 2 * linear_piece * omega + inertia * omega**2)
        )
        == 0,
    )
    canonical_momentum = sp.diff(lagrangian, omega)
    omega_solution = sp.factor(
        (momentum - 2 * linear_piece) / (2 * inertia)
    )
    ledger.check(
        "omega is eliminated from the canonical momentum exactly",
        sp.simplify(canonical_momentum.subs(omega, omega_solution) - momentum)
        == 0,
    )
    fixed_j_hamiltonian = sp.factor(
        (momentum * omega - lagrangian).subs(omega, omega_solution)
    )
    expected_hamiltonian = sp.factor(
        (momentum - 2 * linear_piece) ** 2 / (4 * inertia) - static_piece
    )
    ledger.check(
        "fixed-J Hamiltonian includes the momentum shift and static subtraction",
        sp.simplify(fixed_j_hamiltonian - expected_hamiltonian) == 0,
    )
    simplified_hamiltonian = sp.factor(
        momentum**2
        / (4 * kappa * spatial_current**2 * sp.cosh(rapidity) ** 2)
        - momentum * b0 * sp.tanh(rapidity) / spatial_current
    )
    ledger.check(
        "the boost witness Hamiltonian has the exact closed form",
        sp.simplify(fixed_j_hamiltonian - simplified_hamiltonian) == 0,
    )
    rest_hamiltonian = sp.factor(fixed_j_hamiltonian.subs(rapidity, 0))
    ledger.check(
        "the familiar J squared over four I form is only the rest-slice limit",
        rest_hamiltonian
        == momentum**2 / (4 * kappa * spatial_current**2)
        and static_piece.subs(rapidity, 0) == 0
        and linear_piece.subs(rapidity, 0) == 0,
    )
    b0_zero_fixed_j = sp.factor(fixed_j_hamiltonian.subs(b0, 0))
    fixed_j_second = sp.factor(
        sp.diff(b0_zero_fixed_j, rapidity, 2).subs(rapidity, 0)
    )
    ledger.check(
        "B0 zero fixed-J boost curvature is strictly negative",
        fixed_j_second
        == -momentum**2 / (2 * kappa * spatial_current**2)
        and fixed_j_second.is_negative is True,
    )
    held_omega_hamiltonian = sp.factor(
        (omega * canonical_momentum - lagrangian).subs(b0, 0)
    )
    held_omega_second = sp.factor(
        sp.diff(held_omega_hamiltonian, rapidity, 2).subs(rapidity, 0)
    )
    ledger.check(
        "holding omega instead gives the opposite positive boost curvature",
        held_omega_second
        == 2 * kappa * omega**2 * spatial_current**2
        and held_omega_second.is_nonnegative is True,
    )
    old_rest_only_fixed_j = momentum**2 / (
        4 * kappa * spatial_current**2
    )
    ledger.check(
        "the old rest-only inertia misses the load-bearing fixed-J response",
        sp.diff(old_rest_only_fixed_j, rapidity, 2) == 0
        and sp.simplify(b0_zero_fixed_j - old_rest_only_fixed_j) != 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
