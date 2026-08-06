from __future__ import annotations

import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.translated_overlap_matrices import (
    phase_weighted_self_overlap_limit,
    singular_value_cluster_bound,
)


def test_translated_overlap_limit_public_api_is_exported() -> None:
    assert sf.SingularValueClusterBound is not None
    assert sf.phase_weighted_self_overlap_limit is phase_weighted_self_overlap_limit
    assert sf.singular_value_cluster_bound is singular_value_cluster_bound


def test_phase_weighted_limit_has_one_common_singular_value() -> None:
    alpha = sp.Rational(7, 5)
    phases = (0, 2 * sp.pi / 3, 4 * sp.pi / 3)
    limit = phase_weighted_self_overlap_limit(alpha, phases)
    gram = limit.conjugate().T * limit
    assert all(
        sp.simplify(sp.expand_complex(value)) == 0
        for value in gram - alpha**2 * sp.eye(3)
    )
    expected = (
        alpha,
        alpha * sp.exp(2 * sp.pi * sp.I / 3),
        alpha * sp.exp(4 * sp.pi * sp.I / 3),
    )
    assert all(
        sp.simplify(sp.expand_complex(actual - target)) == 0
        for actual, target in zip(limit.diagonal(), expected)
    )


def test_singular_value_cluster_bound_is_exact_and_sensitive() -> None:
    result = singular_value_cluster_bound(5, sp.Rational(1, 2), count=3)
    assert result.singular_value_lower_bound == sp.Rational(9, 2)
    assert result.singular_value_upper_bound == sp.Rational(11, 2)
    assert result.condition_number_upper_bound == sp.Rational(11, 9)
    looser = singular_value_cluster_bound(5, 1, count=3)
    assert looser.condition_number_upper_bound > result.condition_number_upper_bound


def test_diagonal_perturbation_attains_both_cluster_endpoints() -> None:
    alpha = sp.Integer(5)
    epsilon = sp.Rational(1, 2)
    limit = phase_weighted_self_overlap_limit(alpha, (0, 0, 0))
    perturbed = limit + sp.diag(epsilon, 0, -epsilon)
    singular_values = sorted(perturbed.singular_values(), key=float)
    result = singular_value_cluster_bound(alpha, epsilon, count=3)
    assert singular_values[0] == result.singular_value_lower_bound
    assert singular_values[-1] == result.singular_value_upper_bound


def test_unequal_self_overlaps_break_the_degeneracy_premise() -> None:
    unequal = sp.diag(1, 2, 3)
    assert unequal.singular_values() == [3, 2, 1]
    common = phase_weighted_self_overlap_limit(2, (0, 0, 0))
    assert common.singular_values() == [2, 2, 2]


@pytest.mark.parametrize(
    "call",
    [
        lambda: phase_weighted_self_overlap_limit(0, [0]),
        lambda: phase_weighted_self_overlap_limit(1, []),
        lambda: phase_weighted_self_overlap_limit(1, [sp.I]),
        lambda: singular_value_cluster_bound(1, -1, count=2),
        lambda: singular_value_cluster_bound(1, 1, count=2),
        lambda: singular_value_cluster_bound(1, 0, count=True),
        lambda: singular_value_cluster_bound(1, 0, count=0),
    ],
)
def test_translated_overlap_limit_inputs_are_typed(call) -> None:
    with pytest.raises((TypeError, ValueError)):
        call()
