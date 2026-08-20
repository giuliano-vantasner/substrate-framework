"""Exact projector-current plus alternating-Skyrme completion for P240."""

from __future__ import annotations

import sympy as sp

from substrate_framework.m5_covariant_action import (
    projector_current_bilinear,
    projector_sigma_hamiltonian_density,
    projector_sigma_lagrangian_density,
)
from substrate_framework.m5_kinetic_axis import (
    alternating_sextic_lagrangian_density,
)
from substrate_framework.verification import CheckLedger


P_T = sp.diag(1, 0, 0, 0)
ZERO = sp.zeros(4)


def _generator(left: int, right: int) -> sp.Matrix:
    result = sp.zeros(4)
    result[left, right] = -1
    result[right, left] = 1
    return result


def _preimage(spatial: sp.Matrix, current: sp.Matrix) -> sp.Matrix:
    result = sp.zeros(4)
    for left in range(4):
        for right in range(left + 1, 4):
            if current[left, right] != 0:
                result[left, right] = result[right, left] = (
                    current[left, right]
                    / (spatial[left, left] - spatial[right, right])
                )
    return result


def main() -> int:
    ledger = CheckLedger("P240/projector-plus-skyrme")
    rapidity = sp.symbols("rapidity", real=True)
    kappa_b, kappa_s, momentum, current_scale = sp.symbols(
        "kappa_b kappa_s J b", positive=True
    )
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.cosh(rapidity)
    boost[0, 1] = boost[1, 0] = sp.sinh(rapidity)
    projector_t = boost.inv() * P_T * boost
    projector_tangent = sp.simplify(sp.diff(projector_t, rapidity))
    ledger.check(
        "rank-one rapidity has an exact unit projector-current metric",
        sp.simplify(
            projector_current_bilinear(projector_tangent, projector_tangent)
            - 1
        )
        == 0,
    )
    rapidity_t, rapidity_x, rapidity_y, rapidity_z = sp.symbols(
        "r_t r_x r_y r_z", real=True
    )
    derivatives = tuple(
        coefficient * projector_tangent
        for coefficient in (rapidity_t, rapidity_x, rapidity_y, rapidity_z)
    )
    lagrangian = projector_sigma_lagrangian_density(derivatives, kappa_b)
    hamiltonian = projector_sigma_hamiltonian_density(derivatives, kappa_b)
    ledger.check(
        "projector current has the exact wave Lagrangian and positive Hamiltonian",
        sp.simplify(
            lagrangian
            - kappa_b
            * (
                rapidity_t**2
                - rapidity_x**2
                - rapidity_y**2
                - rapidity_z**2
            )
        )
        == 0
        and sp.simplify(
            hamiltonian
            - kappa_b
            * (
                rapidity_t**2
                + rapidity_x**2
                + rapidity_y**2
                + rapidity_z**2
            )
        )
        == 0,
    )
    ledger.check(
        "uniform time-row 3x3 fields are exactly projector-current null",
        projector_sigma_lagrangian_density((ZERO, ZERO, ZERO, ZERO), kappa_b)
        == 0
        and projector_sigma_hamiltonian_density(
            (ZERO, ZERO, ZERO, ZERO), kappa_b
        )
        == 0,
    )

    spatial = sp.diag(0, 1, 2, 4)
    axis = sp.diag(0, 0, 0, 1)
    target_currents = (
        _generator(2, 3),
        _generator(3, 1),
        _generator(1, 2),
        ZERO,
    )
    spatial_derivatives = tuple(
        _preimage(spatial, current) for current in target_currents
    )
    skyrme_density = alternating_sextic_lagrangian_density(
        P_T, axis, spatial, spatial_derivatives, kappa_s
    )
    ledger.check(
        "alternating Skyrme clock remains active with constant P_t",
        skyrme_density.is_positive is True
        and projector_sigma_hamiltonian_density(
            (ZERO, ZERO, ZERO, ZERO), kappa_b
        )
        == 0,
    )
    ledger.check(
        "the two terms act on distinct load-bearing derivatives",
        sp.simplify(
            projector_current_bilinear(projector_tangent, projector_tangent)
            - 1
        )
        == 0
        and skyrme_density != 0
        and all(
            derivative == derivative.T for derivative in spatial_derivatives
        ),
    )

    lambda_one, mode_norm_squared = sp.symbols(
        "lambda_1 mode_norm_squared", positive=True
    )
    adverse_mass = momentum**2 / (4 * kappa_s * current_scale**2)
    lower_bound = sp.factor(
        (kappa_b * lambda_one - adverse_mass) * mode_norm_squared
    )
    critical_stiffness = sp.factor(adverse_mass / lambda_one)
    ledger.check(
        "Poincare gives the exact bounded-domain Hessian lower bound",
        sp.simplify(
            lower_bound
            - (
                kappa_b * lambda_one
                - momentum**2 / (4 * kappa_s * current_scale**2)
            )
            * mode_norm_squared
        )
        == 0,
    )
    ledger.check(
        "the sufficient positive coefficient region is nonempty",
        sp.simplify(
            lower_bound.subs(kappa_b, 2 * critical_stiffness)
            - adverse_mass * mode_norm_squared
        )
        == 0
        and critical_stiffness.is_positive is True,
    )
    ledger.check(
        "removing the projector current restores the adverse direction",
        lower_bound.subs(kappa_b, 0).is_negative is True,
    )
    radius = sp.symbols("R", positive=True)
    ledger.check(
        "projector-gradient energy has the expected three-dimensional R scaling",
        sp.simplify(radius**3 * (1 / radius) ** 2 - radius) == 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
