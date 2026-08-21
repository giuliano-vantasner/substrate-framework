"""Verify the corrected P240 L1 replacement of time-curvature inertia."""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

from substrate_framework.m5_covariant_action import double_two_form_contraction
from substrate_framework.m5_kinetic_axis import (
    kinetic_axis_lagrangian_density,
    spatial_curvature_hamiltonian_density,
    spatial_curvature_lagrangian_density,
    spatial_inverse_metric_from_timelike_projector,
)
from substrate_framework.verification import CheckLedger


ETA = sp.diag(-1, 1, 1, 1)
P_T = sp.diag(1, 0, 0, 0)
P_N = sp.diag(0, 1, 0, 0)
PAIRS = tuple(combinations(range(4), 2))
ZERO = sp.zeros(4)


def _tensor_from_pair_matrix(matrix: sp.Matrix) -> sp.ImmutableDenseNDimArray:
    tensor = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for row, (mu, nu) in enumerate(PAIRS):
        for column, (internal_a, internal_b) in enumerate(PAIRS):
            value = matrix[row, column]
            tensor[mu, nu, internal_a, internal_b] = value
            tensor[nu, mu, internal_a, internal_b] = -value
            tensor[mu, nu, internal_b, internal_a] = -value
            tensor[nu, mu, internal_b, internal_a] = value
    return sp.ImmutableDenseNDimArray(tensor)


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


def _transform_curvature(
    curvature: sp.NDimArray, transformation: sp.Matrix
) -> sp.ImmutableDenseNDimArray:
    pair_transform = _pair_transform(transformation.inv().T)
    pair_matrix = sp.Matrix(
        6,
        6,
        lambda row, column: curvature[
            PAIRS[row][0], PAIRS[row][1], PAIRS[column][0], PAIRS[column][1]
        ],
    )
    return _tensor_from_pair_matrix(pair_transform * pair_matrix * pair_transform.T)


def _rotation_generator(left: int, right: int) -> sp.Matrix:
    generator = sp.zeros(4)
    generator[left, right] = -1
    generator[right, left] = 1
    return generator


def main() -> int:
    ledger = CheckLedger("P240/kinetic-axis-replacement")
    spatial_inverse = spatial_inverse_metric_from_timelike_projector(P_T)
    ledger.check(
        "M-derived external metric is purely spatial in the comoving frame",
        spatial_inverse == sp.diag(0, 1, 1, 1),
    )

    spatial_pairs = sp.zeros(6)
    for row, column in product((3, 4, 5), repeat=2):
        spatial_pairs[row, column] = 2 * row - column + 1
    spatial_curvature = _tensor_from_pair_matrix(spatial_pairs)
    old_static = -sp.Rational(1, 2) * double_two_form_contraction(
        spatial_curvature, ETA, sp.eye(4)
    )
    new_static = spatial_curvature_lagrangian_density(
        spatial_curvature, P_T, sp.eye(4)
    )
    ledger.check(
        "complete static 3x3 curvature coefficient is unchanged",
        new_static == old_static,
    )
    ledger.check(
        "spatial curvature Hamiltonian is the positive static square",
        spatial_curvature_hamiltonian_density(
            spatial_curvature, P_T, sp.eye(4)
        )
        == -old_static
        and -old_static > 0,
    )

    time_pairs = sp.zeros(6)
    time_pairs[0, 0] = 2
    time_pairs[1, 2] = -3
    time_pairs[2, 1] = 1
    time_curvature = _tensor_from_pair_matrix(time_pairs)
    old_time_hamiltonian = sp.Rational(1, 2) * double_two_form_contraction(
        time_curvature, sp.eye(4), sp.eye(4)
    )
    new_time_hamiltonian = spatial_curvature_hamiltonian_density(
        time_curvature, P_T, sp.eye(4)
    )
    ledger.check(
        "old time-curvature inertia is removed rather than supplemented",
        old_time_hamiltonian > 0 and new_time_hamiltonian == 0,
    )

    transformation = sp.eye(4)
    transformation[0, 0] = transformation[1, 1] = sp.Rational(5, 3)
    transformation[0, 1] = transformation[1, 0] = sp.Rational(4, 3)
    inverse = transformation.inv()
    transformed_curvature = _transform_curvature(spatial_curvature, transformation)
    transformed_projector = transformation * P_T * inverse
    transformed_spatial_inverse = spatial_inverse_metric_from_timelike_projector(
        transformed_projector
    )
    ledger.check(
        "M-derived spatial inverse metric transforms contravariantly",
        sp.simplify(
            transformed_spatial_inverse
            - transformation * spatial_inverse * transformation.T
        )
        == sp.zeros(4),
    )
    ledger.check(
        "spatial curvature replacement is an exact Lorentz scalar",
        sp.simplify(
            spatial_curvature_lagrangian_density(
                transformed_curvature,
                transformed_projector,
                transformation * sp.eye(4) * transformation.T,
            )
            - new_static
        )
        == 0,
    )

    kappa = sp.symbols("kappa", positive=True)
    active = sp.diag(0, 1, sp.Rational(1, 3), 0)
    active_clock = _rotation_generator(2, 3) * active - active * _rotation_generator(2, 3)
    physical_l1 = kinetic_axis_lagrangian_density(
        P_T, P_N, active, (active_clock, ZERO, ZERO, ZERO), kappa
    )
    wrong_axis = sp.diag(0, 0, 1, 0)
    wrong = sp.diag(0, 1, 0, 0)
    wrong_clock = _rotation_generator(1, 3) * wrong - wrong * _rotation_generator(1, 3)
    wrong_l1 = kinetic_axis_lagrangian_density(
        P_T, wrong_axis, wrong, (wrong_clock, ZERO, ZERO, ZERO), kappa
    )
    ledger.check(
        "corrected total clock channel selects the physical axis",
        physical_l1 == kappa / 9 and wrong_l1 == 0,
    )
    ledger.check(
        "retaining the old channel is a sensitivity mutation that restores the escape",
        wrong_l1 + old_time_hamiltonian > 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
