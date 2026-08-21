"""Exact equivalence-class selection for the P240 timelike Skyrme current."""

from __future__ import annotations

from itertools import product

import sympy as sp

from substrate_framework.m5_covariant_action import m5_curvature_from_derivatives
from substrate_framework.m5_kinetic_axis import (
    axis_pontryagin_pseudoscalar,
    fixed_j_derrick_energy,
    timelike_skyrme_lagrangian_density,
)
from substrate_framework.verification import CheckLedger


P_T = sp.diag(1, 0, 0, 0)
P_N = sp.diag(0, 1, 0, 0)
ZERO = sp.zeros(4)


def _rotation_generator(left: int, right: int) -> sp.Matrix:
    result = sp.zeros(4)
    result[left, right] = -1
    result[right, left] = 1
    return result


def main() -> int:
    ledger = CheckLedger("P240/skyrme-equivalence")
    l1, l2, l3 = sp.symbols("lambda_1 lambda_2 lambda_3", real=True)
    z11, z22, z33, z12, z13, z23 = sp.symbols(
        "z11 z22 z33 z12 z13 z23", real=True
    )
    y3 = sp.diag(l1, l2, l3)
    z3 = sp.Matrix([[z11, z12, z13], [z12, z22, z23], [z13, z23, z33]])
    current = y3 * z3 - z3 * y3
    skyrme_norm = sp.factor(-sp.trace(current**2) / 2)
    trace_difference = sp.factor(sp.trace(y3**2 * z3**2) - sp.trace(y3 * z3 * y3 * z3))
    gap_sum = (
        (l1 - l2) ** 2 * z12**2
        + (l1 - l3) ** 2 * z13**2
        + (l2 - l3) ** 2 * z23**2
    )
    ledger.check(
        "standard Skyrme trace and commutator forms are identical",
        sp.simplify(skyrme_norm - trace_difference) == 0,
    )
    ledger.check(
        "Skyrme norm is the manifest eigenvalue-gap sum of squares",
        sp.simplify(skyrme_norm - gap_sum) == 0,
    )
    alpha, beta = sp.symbols("alpha beta", real=True)
    commuting_z = sp.diag(z11, z22, z33)
    commuting_combination = sp.expand(
        alpha * sp.trace(y3**2 * commuting_z**2)
        + beta * sp.trace(y3 * commuting_z * y3 * commuting_z)
    )
    commuting_coefficients = sp.Poly(
        commuting_combination, l1, l2, l3, z11, z22, z33
    ).coeffs()
    ledger.check(
        "commuting-null single-trace class is unique up to normalization",
        sp.solve(commuting_coefficients, (alpha, beta), dict=True)
        == [{alpha: -beta}],
    )

    n, left, right, omega = sp.symbols(
        "n lambda_theta lambda_phi omega", real=True
    )
    kappa = sp.symbols("kappa", positive=True)
    spatial = sp.diag(0, n, left, right)
    clock = omega * (
        _rotation_generator(2, 3) * spatial
        - spatial * _rotation_generator(2, 3)
    )
    derivatives = (clock, ZERO, ZERO, ZERO)
    quartic = timelike_skyrme_lagrangian_density(
        P_T, spatial, derivatives, kappa
    )
    sextic = timelike_skyrme_lagrangian_density(
        P_T, spatial, derivatives, kappa, axis_projector=P_N
    )
    ledger.check(
        "physical-axis sextic clock polynomial is exact",
        sp.simplify(sextic - kappa * n**2 * omega**2 * (left - right) ** 4) == 0,
    )
    ledger.check(
        "physical-axis sextic Hamiltonian is positive on the active branch",
        sextic.subs({n: 1, omega: 1, left: 1, right: 0}) == kappa,
    )
    wrong_spatial = sp.diag(0, 1, 0, 0)
    wrong_axis = sp.diag(0, 0, 1, 0)
    wrong_clock = _rotation_generator(1, 3) * wrong_spatial - wrong_spatial * _rotation_generator(1, 3)
    wrong_derivatives = (wrong_clock, ZERO, ZERO, ZERO)
    ledger.check(
        "quartic is wrong-axis active while sextic repair is null",
        timelike_skyrme_lagrangian_density(
            P_T, wrong_spatial, wrong_derivatives, kappa
        )
        == kappa
        and timelike_skyrme_lagrangian_density(
            P_T,
            wrong_spatial,
            wrong_derivatives,
            kappa,
            axis_projector=wrong_axis,
        )
        == 0,
    )
    linear_weight = sp.symbols("b", real=True)
    quadratic_weight, epsilon = sp.symbols("c epsilon", positive=True)
    weight = linear_weight * n + quadratic_weight * n**2
    opposite_product_limit = sp.limit(
        weight.subs(n, epsilon) * weight.subs(n, -epsilon) / epsilon**2,
        epsilon,
        0,
    )
    ledger.check(
        "a linear axis weight cannot be nonnegative on both eigenvalue signs",
        opposite_product_limit == -linear_weight**2,
    )
    ledger.check(
        "minimum nonnegative quadratic repair is n squared",
        sp.factor(weight.subs(linear_weight, 0)) == quadratic_weight * n**2,
    )
    ledger.check(
        "two natural rank-one eigenprojector weights are equivalent",
        sp.trace(P_N * spatial) ** 2 == sp.trace(P_N * spatial**2) == n**2,
    )
    l1_clock = kappa * n**2 * omega**2 * (left - right) ** 2
    ledger.check(
        "Skyrme sextic is not constant-proportional to L1",
        sp.simplify(sextic / l1_clock - (left - right) ** 2) == 0
        and sp.diff((left - right) ** 2, left) != 0,
    )

    homogeneous_curvature = m5_curvature_from_derivatives(derivatives)
    ledger.check(
        "homogeneous clock exactly separates Skyrme from Pontryagin",
        all(
            homogeneous_curvature[index] == 0
            for index in product(range(4), repeat=4)
        )
        and axis_pontryagin_pseudoscalar(
            homogeneous_curvature, P_N, sp.eye(4)
        )
        == 0
        and sextic != 0,
    )
    static_symbols = sp.symbols("s0:27", real=True)
    static_derivatives = [ZERO]
    for direction in range(3):
        raw = sp.Matrix(3, 3, static_symbols[9 * direction : 9 * direction + 9])
        symmetric = raw + raw.T
        embedded = sp.zeros(4)
        embedded[1:4, 1:4] = symmetric
        static_derivatives.append(embedded)
    ledger.check(
        "Skyrme sextic is identically null on arbitrary static 3x3 data",
        timelike_skyrme_lagrangian_density(
            P_T,
            spatial,
            tuple(static_derivatives),
            kappa,
            axis_projector=P_N,
        )
        == 0,
    )
    radius, curvature, current_coefficient, potential, inertia, momentum = sp.symbols(
        "R A C B I_0 J", positive=True
    )
    skyrme_scale_energy = fixed_j_derrick_energy(
        radius, curvature, current_coefficient, potential, inertia, momentum
    )
    pontryagin_rotational = momentum**2 * radius**3 / (4 * inertia)
    ledger.check(
        "Skyrme and Pontryagin inertia scalings are inequivalent",
        sp.limit(momentum**2 / (4 * inertia * radius**3), radius, 0, dir="+")
        == sp.oo
        and sp.limit(pontryagin_rotational, radius, 0, dir="+") == 0,
    )
    ledger.check(
        "Skyrme fixed-J energy has a finite strict scale minimum",
        sp.limit(skyrme_scale_energy, radius, 0, dir="+") == sp.oo
        and sp.limit(skyrme_scale_energy, radius, sp.oo) == sp.oo
        and sp.simplify(
            sp.diff(skyrme_scale_energy, radius, 2)
            - (
                2 * curvature / radius**3
                + 6 * potential * radius
                + 3 * momentum**2 / (inertia * radius**5)
            )
        )
        == 0
        and (
            2 * curvature / radius**3
            + 6 * potential * radius
            + 3 * momentum**2 / (inertia * radius**5)
        ).is_positive
        is True,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
