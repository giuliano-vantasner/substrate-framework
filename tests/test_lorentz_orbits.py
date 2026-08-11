"""Exact tests for dimension-aware, narrowly named Lorentz-orbit geometry."""

from __future__ import annotations

import sympy as sp
import pytest

from substrate_framework.lorentz_orbits import (
    unit_timelike_vector_orbit_metric,
    unit_timelike_vector_orbit_volume,
)


def test_unit_timelike_vector_orbit_metric_is_hyperbolic() -> None:
    metric = unit_timelike_vector_orbit_metric()
    eta, theta = sp.symbols("eta theta", positive=True)
    expected = sp.diag(
        1,
        sp.sinh(eta) ** 2,
        sp.sinh(eta) ** 2 * sp.sin(theta) ** 2,
    )
    assert sp.simplify(metric - expected) == sp.zeros(3)


def test_unit_timelike_vector_orbit_metric_in_2plus1_is_h2() -> None:
    metric = unit_timelike_vector_orbit_metric(3)
    eta = sp.Symbol("eta", positive=True)
    expected = sp.diag(1, sp.sinh(eta) ** 2)
    assert sp.simplify(metric - expected) == sp.zeros(2)


def test_unit_timelike_vector_orbit_volume_diverges() -> None:
    assert unit_timelike_vector_orbit_volume() is sp.oo
    assert unit_timelike_vector_orbit_volume(3) is sp.oo


def test_unit_timelike_vector_orbit_rejects_unsupported_dimension() -> None:
    with pytest.raises(ValueError, match="3 or 4"):
        unit_timelike_vector_orbit_metric(2)
    with pytest.raises(ValueError, match="3 or 4"):
        unit_timelike_vector_orbit_volume(5)
