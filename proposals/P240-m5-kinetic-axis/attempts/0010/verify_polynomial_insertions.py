"""Exact screening of the remaining P240 quartic insertion basis."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

from substrate_framework.m5_covariant_action import m5_curvature_from_derivatives
from substrate_framework.m5_kinetic_axis import (
    axis_eigenvalue,
    axis_pontryagin_pseudoscalar,
    fixed_j_derrick_energy,
)
from substrate_framework.verification import CheckLedger


PAIRS = tuple(combinations(range(4), 2))
P_N = sp.diag(0, 1, 0, 0)
Y = sp.diag(0, 1, sp.Rational(2, 5), -sp.Rational(1, 5))


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


def _source_derivatives(omega: sp.Symbol, variant: int) -> tuple[sp.Matrix, ...]:
    order_parameter = sp.diag(-8, 1, sp.Rational(2, 5), -sp.Rational(1, 5))
    generator = sp.zeros(4)
    generator[2, 3], generator[3, 2] = -1, 1
    clock = omega * (generator * order_parameter + order_parameter * generator.T)
    spatial = [
        sp.Matrix([[0, 0, 0, 0], [0, 2, 0, -1], [0, 0, -1, -2], [0, -1, -2, -2]]),
        sp.Matrix([[0, 0, 0, 0], [0, 2, sp.Rational(1, 2), sp.Rational(3, 2)], [0, sp.Rational(1, 2), 1, sp.Rational(3, 2)], [0, sp.Rational(3, 2), sp.Rational(3, 2), 0]]),
        sp.Matrix([[0, 0, 0, 0], [0, 0, 2, -1], [0, 2, 1, 0], [0, -1, 0, 0]]),
    ]
    if variant == 2:
        spatial[0] = spatial[0] + sp.diag(0, 1, -2, 3)
        spatial[2] = spatial[2] + sp.Matrix(
            [[0, 0, 0, 0], [0, 0, -1, 2], [0, -1, 0, 1], [0, 2, 1, 0]]
        )
    return (clock, *spatial)


def main() -> int:
    ledger = CheckLedger("P240/quartic-polynomial-insertions")
    spatial_pairs = sp.zeros(6)
    for row, column in product((3, 4, 5), repeat=2):
        spatial_pairs[row, column] = row - 2 * column + 4
    static_curvature = _tensor_from_pair_matrix(spatial_pairs)
    ledger.check(
        "external epsilon is null on arbitrary static 3x3 curvature for Y",
        axis_pontryagin_pseudoscalar(static_curvature, Y, sp.eye(4)) == 0,
    )
    ledger.check(
        "external epsilon is null on arbitrary static 3x3 curvature for Y2",
        axis_pontryagin_pseudoscalar(static_curvature, Y**2, sp.eye(4)) == 0,
    )

    omega = sp.symbols("omega", real=True)
    curvatures = tuple(
        m5_curvature_from_derivatives(_source_derivatives(omega, variant))
        for variant in (1, 2)
    )
    identity_values = tuple(
        axis_pontryagin_pseudoscalar(value, sp.eye(4), sp.eye(4))
        for value in curvatures
    )
    ledger.check("identity insertion cancels on both source witnesses", identity_values == (0, 0))
    y_values = tuple(
        axis_pontryagin_pseudoscalar(value, Y, sp.eye(4)) for value in curvatures
    )
    y2_values = tuple(
        axis_pontryagin_pseudoscalar(value, Y**2, sp.eye(4)) for value in curvatures
    )
    ledger.check(
        "Y insertion has nonzero velocity-linear source response",
        all(value != 0 and sp.diff(value, omega, 2) == 0 for value in y_values),
    )
    ledger.check(
        "Y2 insertion has nonzero velocity-linear source response",
        all(value != 0 and sp.diff(value, omega, 2) == 0 for value in y2_values),
    )
    ledger.check(
        "Y and Y2 responses are not a fixed proportional functional",
        sp.simplify(y_values[0] * y2_values[1] - y_values[1] * y2_values[0]) != 0,
    )

    transformation = sp.eye(4)
    transformation[0, 0] = transformation[1, 1] = sp.Rational(5, 3)
    transformation[0, 1] = transformation[1, 0] = sp.Rational(4, 3)
    transformed_curvature = _transform_curvature(curvatures[0], transformation)
    transformed_y = transformation * Y * transformation.inv()
    transformed_h = transformation * sp.eye(4) * transformation.T
    transformed_value = axis_pontryagin_pseudoscalar(
        transformed_curvature, transformed_y, transformed_h
    )
    ledger.check(
        "Y-inserted factor is proper-Lorentz invariant",
        sp.simplify(transformed_value - y_values[0]) == 0,
    )
    parity = sp.diag(1, -1, 1, 1)
    parity_value = axis_pontryagin_pseudoscalar(
        _transform_curvature(curvatures[0], parity), parity * Y * parity, parity * parity
    )
    ledger.check(
        "Y-inserted factor is parity odd and its square parity even",
        sp.simplify(parity_value + y_values[0]) == 0
        and sp.simplify(parity_value**2 - y_values[0] ** 2) == 0,
    )
    strength = sp.symbols("gamma", positive=True)
    density = strength * axis_eigenvalue(P_N, Y) ** 2 * y_values[0] ** 2 / 2
    ledger.check(
        "Y density has positive Legendre Hamiltonian",
        density.subs(omega, 1) > 0
        and sp.simplify(omega * sp.diff(density, omega) - density - density) == 0,
    )
    wrong_axis = sp.diag(0, 0, 0, 1)
    wrong_y = sp.diag(0, 1, sp.Rational(2, 5), 0)
    wrong_density = (
        strength
        * axis_eigenvalue(wrong_axis, wrong_y) ** 2
        * y_values[0] ** 2
        / 2
    )
    ledger.check("outer axis weight kills zero-eigenline mutation", wrong_density == 0)
    radius, a, c, b, inertia, momentum = sp.symbols(
        "R A C B I J", positive=True
    )
    energy = fixed_j_derrick_energy(radius, a, c, b, inertia, momentum)
    ledger.check(
        "fixed-J scale energy has finite strict minimum",
        sp.limit(energy, radius, 0, dir="+") == sp.oo
        and sp.limit(energy, radius, sp.oo) == sp.oo
        and sp.diff(energy, radius, 2).is_positive is True,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
