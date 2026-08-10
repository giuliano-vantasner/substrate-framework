"""Exact tests for narrowly named Lorentz-orbit geometry."""

from __future__ import annotations

import sympy as sp

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


def test_unit_timelike_vector_orbit_volume_diverges() -> None:
    assert unit_timelike_vector_orbit_volume() is sp.oo
