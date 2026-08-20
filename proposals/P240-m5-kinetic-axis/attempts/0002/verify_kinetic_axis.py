"""Exact P240 comparison of issue-147 candidates L1 and L2."""

from __future__ import annotations

import sympy as sp

from substrate_framework.m5_kinetic_axis import (
    fixed_j_derrick_energy,
    kinetic_axis_comoving_hamiltonian_density,
    kinetic_axis_lagrangian_density,
    timelike_skyrme_lagrangian_density,
)
from substrate_framework.verification import CheckLedger


ETA = sp.diag(-1, 1, 1, 1)
P_T = sp.diag(1, 0, 0, 0)
P_N = sp.diag(0, 1, 0, 0)
ZERO = sp.zeros(4)


def _rotation_generator(left: int, right: int) -> sp.Matrix:
    generator = sp.zeros(4)
    generator[left, right] = -1
    generator[right, left] = 1
    return generator


def _derivative_covector_transform(
    derivatives: tuple[sp.Matrix, ...], transformation: sp.Matrix
) -> tuple[sp.Matrix, ...]:
    inverse = transformation.inv()
    return tuple(
        sp.simplify(
            sum(
                (
                    inverse[rho, mu]
                    * transformation
                    * derivatives[rho]
                    * inverse
                    for rho in range(4)
                ),
                sp.zeros(4),
            )
        )
        for mu in range(4)
    )


def main() -> int:
    ledger = CheckLedger("P240/kinetic-axis-structural-selection")
    n, left, right = sp.symbols("n lambda_theta lambda_phi", real=True)
    kappa = sp.symbols("kappa", positive=True)
    spatial = sp.diag(0, n, left, right)
    clock_generator = _rotation_generator(2, 3)
    clock_derivative = clock_generator * spatial - spatial * clock_generator
    derivatives = (clock_derivative, ZERO, ZERO, ZERO)

    l1 = kinetic_axis_lagrangian_density(
        P_T, P_N, spatial, derivatives, kappa
    )
    expected_l1 = kappa * n**2 * (left - right) ** 2
    ledger.check(
        "L1 gives the physical-axis clock inertia",
        sp.simplify(l1 - expected_l1) == 0,
    )
    hamiltonian = kinetic_axis_comoving_hamiltonian_density(
        P_T, P_N, spatial, clock_derivative, kappa
    )
    ledger.check(
        "L1 comoving Hamiltonian is the same positive square",
        sp.simplify(hamiltonian - expected_l1) == 0,
    )

    arbitrary = sp.symbols("d1_11:14 d2_11:14 d3_11:14")
    static_derivatives = [ZERO]
    for offset in range(3):
        matrix = sp.zeros(4)
        values = arbitrary[3 * offset : 3 * offset + 3]
        matrix[1, 1], matrix[2, 2], matrix[3, 3] = values
        matrix[1, 2] = matrix[2, 1] = values[0] - values[1]
        matrix[1, 3] = matrix[3, 1] = values[1] - values[2]
        matrix[2, 3] = matrix[3, 2] = values[2] - values[0]
        static_derivatives.append(matrix)
    ledger.check(
        "L1 vanishes on an arbitrary static uniform-time-row 3x3 field",
        kinetic_axis_lagrangian_density(
            P_T, P_N, spatial, tuple(static_derivatives), kappa
        )
        == 0,
    )

    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = sp.Rational(4, 3)
    inverse = boost.inv()
    transformed_derivatives = _derivative_covector_transform(derivatives, boost)
    transformed_l1 = kinetic_axis_lagrangian_density(
        boost * P_T * inverse,
        boost * P_N * inverse,
        boost * spatial * inverse,
        transformed_derivatives,
        kappa,
    )
    ledger.check(
        "L1 is an exact Lorentz scalar",
        sp.simplify(transformed_l1 - l1) == 0,
    )

    wrong_spatial = sp.diag(0, 1, 0, 0)
    wrong_axis = sp.diag(0, 0, 1, 0)
    wrong_generator = _rotation_generator(1, 3)
    wrong_derivative = wrong_generator * wrong_spatial - wrong_spatial * wrong_generator
    wrong_derivatives = (wrong_derivative, ZERO, ZERO, ZERO)
    ledger.check(
        "L1 assigns zero inertia to the zero-eigenline escape",
        kinetic_axis_lagrangian_density(
            P_T, wrong_axis, wrong_spatial, wrong_derivatives, kappa
        )
        == 0,
    )
    ledger.check(
        "L1 remains active on a split physical-director clock",
        l1.subs({n: 1, left: sp.Rational(1, 3), right: 0})
        == kappa / 9,
    )

    quartic = timelike_skyrme_lagrangian_density(
        P_T, spatial, derivatives, kappa
    )
    ledger.check(
        "L2 quartic current is the axis-blind fourth-power inertia",
        sp.simplify(quartic - kappa * (left - right) ** 4) == 0,
    )
    wrong_quartic = timelike_skyrme_lagrangian_density(
        P_T, wrong_spatial, wrong_derivatives, kappa
    )
    ledger.check(
        "L2 quartic fails the wrong-axis gate",
        wrong_quartic == kappa,
    )
    sextic = timelike_skyrme_lagrangian_density(
        P_T, spatial, derivatives, kappa, axis_projector=P_N
    )
    ledger.check(
        "L2 sextic repairs the axis gate by the same eigenvalue weight",
        sp.simplify(sextic - kappa * n**2 * (left - right) ** 4) == 0
        and timelike_skyrme_lagrangian_density(
            P_T,
            wrong_spatial,
            wrong_derivatives,
            kappa,
            axis_projector=wrong_axis,
        )
        == 0,
    )

    scale = sp.symbols("R", positive=True)
    curvature, current, potential, inertia, momentum = sp.symbols(
        "A C B I_0 J", positive=True
    )
    energy = fixed_j_derrick_energy(
        scale, curvature, current, potential, inertia, momentum
    )
    ledger.check(
        "fixed-J scale energy diverges at both endpoints",
        sp.limit(energy, scale, 0, dir="+") == sp.oo
        and sp.limit(energy, scale, sp.oo) == sp.oo,
    )
    second_derivative = sp.factor(sp.diff(energy, scale, 2))
    expected_second = (
        2 * curvature / scale**3
        + 6 * potential * scale
        + 3 * momentum**2 / (inertia * scale**5)
    )
    ledger.check(
        "fixed-J scale energy is strictly convex",
        sp.simplify(second_derivative - expected_second) == 0
        and expected_second.is_positive is True,
    )
    frequency = momentum / (2 * inertia * scale**3)
    ledger.check(
        "the finite-scale fixed-J frequency is positive and finite",
        frequency.is_positive is True and frequency.is_finite is True,
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
