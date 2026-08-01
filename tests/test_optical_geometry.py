from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.optical_geometry import (
    index_from_potential,
    optical_box_static_1d,
    optical_dilaton,
    optical_dilaton_source_operator_1d,
    optical_metric_1d,
    optical_ricci_scalar_1d,
    slow_geodesic_acceleration_from_potential,
)


def test_optical_dilaton_matches_curvature_for_nontrivial_profile() -> None:
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    index = 1 + x**2
    metric = optical_metric_1d(index, c0)
    assert metric.det() == -1 / c0**2
    assert sp.simplify(
        optical_box_static_1d(optical_dilaton(index), index, x, c0)
        - optical_ricci_scalar_1d(index, x, c0)
    ) == 0


def test_conditional_potential_map_and_drift_are_exact() -> None:
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    potential = sp.Function("Phi")(x)
    index = index_from_potential(potential, c0)
    assert index == 1 / (1 + 2 * potential / c0**2)
    assert sp.simplify(
        slow_geodesic_acceleration_from_potential(potential, x, c0)
        + (1 + 2 * potential / c0**2) * sp.diff(potential, x)
    ) == 0


def test_conditional_source_operator_is_exact_not_just_weak_field() -> None:
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    potential = sp.Function("Phi")(x)
    source_side = optical_dilaton_source_operator_1d(potential, x, c0)
    assert sp.simplify(source_side - 2 * sp.diff(potential, x, 2)) == 0
    assert c0 not in source_side.free_symbols


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: optical_metric_1d(0, 1), "index"),
        (lambda: optical_metric_1d(1, 0), "signal_speed"),
        (lambda: index_from_potential(-sp.Rational(1, 2), 1), "positive optical index"),
    ],
)
def test_numeric_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
