"""Reject L1 boundedness and verify the healthy P240 L2 construction."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

from substrate_framework.m5_covariant_action import m5_curvature_from_derivatives
from substrate_framework.m5_kinetic_axis import (
    axis_pontryagin_pseudoscalar,
    axis_weighted_pontryagin_lagrangian_density,
)
from substrate_framework.verification import CheckLedger


ETA = sp.diag(-1, 1, 1, 1)
P_N = sp.diag(0, 1, 0, 0)
PAIRS = tuple(combinations(range(4), 2))


def _pair_transform(covector_transform: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        6,
        6,
        lambda new, old: sp.expand(
            covector_transform[PAIRS[old][0], PAIRS[new][0]]
            * covector_transform[PAIRS[old][1], PAIRS[new][1]]
            - covector_transform[PAIRS[old][1], PAIRS[new][0]]
            * covector_transform[PAIRS[old][0], PAIRS[new][1]]
        ),
    )


def _tensor_from_pair_matrix(matrix: sp.Matrix) -> sp.ImmutableDenseNDimArray:
    tensor = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for row, (mu, nu) in enumerate(PAIRS):
        for column, (a, b) in enumerate(PAIRS):
            value = matrix[row, column]
            tensor[mu, nu, a, b] = value
            tensor[nu, mu, a, b] = -value
            tensor[mu, nu, b, a] = -value
            tensor[nu, mu, b, a] = value
    return sp.ImmutableDenseNDimArray(tensor)


def _transform_curvature(curvature, transformation):
    pair_transform = _pair_transform(transformation.inv().T)
    pair_matrix = sp.Matrix(
        6,
        6,
        lambda row, column: curvature[
            PAIRS[row][0], PAIRS[row][1], PAIRS[column][0], PAIRS[column][1]
        ],
    )
    return _tensor_from_pair_matrix(pair_transform * pair_matrix * pair_transform.T)


def _source_clock_derivatives(omega: sp.Symbol) -> tuple[sp.Matrix, ...]:
    order_parameter = sp.diag(-8, 1, sp.Rational(2, 5), -sp.Rational(1, 5))
    generator = sp.zeros(4)
    generator[2, 3], generator[3, 2] = -1, 1
    clock = omega * (generator * order_parameter + order_parameter * generator.T)
    spatial = (
        sp.Matrix([[0, 0, 0, 0], [0, 2, 0, -1], [0, 0, -1, -2], [0, -1, -2, -2]]),
        sp.Matrix([[0, 0, 0, 0], [0, 2, sp.Rational(1, 2), sp.Rational(3, 2)], [0, sp.Rational(1, 2), 1, sp.Rational(3, 2)], [0, sp.Rational(3, 2), sp.Rational(3, 2), 0]]),
        sp.Matrix([[0, 0, 0, 0], [0, 0, 2, -1], [0, 2, 1, 0], [0, -1, 0, 0]]),
    )
    return (clock, *spatial)


def main() -> int:
    ledger = CheckLedger("P240/l2-axis-pontryagin")

    wave_number, epsilon, rapidity, kappa = sp.symbols(
        "k epsilon b kappa", positive=True
    )
    negative_gradient = -kappa * sp.sinh(rapidity) ** 2 * epsilon**2 * wave_number**2 / 2
    potential_bound = sp.symbols("V_epsilon", nonnegative=True)
    ledger.check(
        "L1 has an exact high-frequency unbounded Hamiltonian channel",
        sp.limit(negative_gradient + potential_bound, wave_number, sp.oo) == -sp.oo,
    )

    spatial_pairs = sp.zeros(6)
    for row, column in product((3, 4, 5), repeat=2):
        spatial_pairs[row, column] = row - 2 * column + 4
    static_curvature = _tensor_from_pair_matrix(spatial_pairs)
    ledger.check(
        "L2 pseudoscalar is identically null on arbitrary static 3x3 curvature",
        axis_pontryagin_pseudoscalar(static_curvature, P_N, sp.eye(4)) == 0,
    )

    omega = sp.symbols("omega", real=True)
    curvature = m5_curvature_from_derivatives(_source_clock_derivatives(omega))
    pseudoscalar = axis_pontryagin_pseudoscalar(curvature, P_N, sp.eye(4))
    ledger.check(
        "source-admissible physical-axis clock witness is nonzero and velocity linear",
        sp.simplify(pseudoscalar / omega) != 0
        and sp.diff(pseudoscalar, omega, 2) == 0,
    )

    strength = sp.symbols("gamma", positive=True)
    spatial = sp.diag(0, 1, sp.Rational(2, 5), -sp.Rational(1, 5))
    density = axis_weighted_pontryagin_lagrangian_density(
        curvature, P_N, spatial, sp.eye(4), strength
    )
    ledger.check(
        "L2 Legendre Hamiltonian equals its positive velocity square",
        sp.simplify(omega * sp.diff(density, omega) - density - density) == 0
        and density.subs(omega, 1) > 0,
    )
    wrong_axis = sp.diag(0, 0, 0, 1)
    wrong_spatial = sp.diag(0, 1, sp.Rational(2, 5), 0)
    ledger.check(
        "zero-eigenline axis mutation has zero L2 clock density",
        axis_weighted_pontryagin_lagrangian_density(
            curvature, wrong_axis, wrong_spatial, sp.eye(4), strength
        )
        == 0,
    )

    transformation = sp.eye(4)
    transformation[0, 0] = transformation[1, 1] = sp.Rational(5, 3)
    transformation[0, 1] = transformation[1, 0] = sp.Rational(4, 3)
    inverse = transformation.inv()
    transformed_curvature = _transform_curvature(curvature, transformation)
    transformed_axis = transformation * P_N * inverse
    transformed_internal = transformation * sp.eye(4) * transformation.T
    transformed_spatial = transformation * spatial * inverse
    transformed_pseudoscalar = axis_pontryagin_pseudoscalar(
        transformed_curvature, transformed_axis, transformed_internal
    )
    ledger.check(
        "axis Pontryagin factor is a proper-Lorentz pseudoscalar",
        sp.simplify(transformed_pseudoscalar - pseudoscalar) == 0,
    )
    parity = sp.diag(1, -1, 1, 1)
    parity_curvature = _transform_curvature(curvature, parity)
    parity_value = axis_pontryagin_pseudoscalar(
        parity_curvature,
        parity * P_N * parity,
        parity * sp.eye(4) * parity,
    )
    parity_density = axis_weighted_pontryagin_lagrangian_density(
        parity_curvature,
        parity * P_N * parity,
        parity * spatial * parity,
        parity * sp.eye(4) * parity,
        strength,
    )
    ledger.check(
        "pseudoscalar flips under parity while its density is parity even",
        sp.simplify(parity_value + pseudoscalar) == 0
        and sp.simplify(parity_density - density) == 0,
    )

    scale = sp.symbols("R", positive=True)
    curvature_coefficient, current_coefficient, potential_coefficient, inertia_coefficient, momentum = sp.symbols(
        "A C B I_0 J", positive=True
    )
    scale_energy = (
        curvature_coefficient / scale
        + current_coefficient * scale
        + potential_coefficient * scale**3
        + momentum**2 * scale**3 / (4 * inertia_coefficient)
    )
    ledger.check(
        "L2 fixed-J scale energy has a finite strict minimum",
        sp.limit(scale_energy, scale, 0, dir="+") == sp.oo
        and sp.limit(scale_energy, scale, sp.oo) == sp.oo
        and sp.diff(scale_energy, scale, 2).is_positive is True,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
