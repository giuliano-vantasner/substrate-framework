"""Exact ensemble stress-energy checks for toronic flux tubes (issue #28)."""

from __future__ import annotations

import sympy as sp

from substrate_framework.flux_tube_ensemble import (
    isotropic_average_equation_of_state,
    modulus_stationary_point_exists,
    orientation_average_nn,
    oriented_grassmannian_2_4_volume,
    self_dual_split_norms_constant,
    timelike_axis_induced_metric,
    timelike_axis_orbit_volume,
    tube_longitudinal_pressure,
    tube_transverse_pressure,
)


def test_tube_pressures_for_inverse_quartic_density() -> None:
    c = sp.Symbol("c", positive=True)
    L = sp.Symbol("L", positive=True)
    rho = -c * L**-4
    assert sp.simplify(tube_transverse_pressure(c) - rho) == 0
    assert sp.simplify(tube_longitudinal_pressure(c) + rho) == 0


def test_isotropic_average_w_is_one_third() -> None:
    assert isotropic_average_equation_of_state(1) == sp.Rational(1, 3)
    assert isotropic_average_equation_of_state(-1) == sp.Rational(1, 3)


def test_orientation_average_is_delta_over_three() -> None:
    for i in range(3):
        for j in range(3):
            expected = sp.Rational(1, 3) if i == j else sp.Integer(0)
            assert orientation_average_nn(i, j) == expected


def test_timelike_axis_induced_metric_is_hyperboloid() -> None:
    # the derived invariant measure on the H^3 orbit, not a declared stand-in
    metric = timelike_axis_induced_metric()
    eta, theta = sp.symbols("eta theta", positive=True)
    expected = sp.diag(1, sp.sinh(eta) ** 2, sp.sinh(eta) ** 2 * sp.sin(theta) ** 2)
    assert sp.simplify(metric - expected) == sp.zeros(3)


def test_timelike_axis_orbit_volume_diverges() -> None:
    assert timelike_axis_orbit_volume() is sp.oo


def test_self_dual_split_norms_constant() -> None:
    assert self_dual_split_norms_constant() is True


def test_oriented_grassmannian_volume_is_finite() -> None:
    volume = oriented_grassmannian_2_4_volume()
    assert sp.simplify(volume - 16 * sp.pi**2) == 0
    assert volume.is_finite


def test_modulus_has_no_stationary_point_either_sign() -> None:
    assert modulus_stationary_point_exists(1) is False
    assert modulus_stationary_point_exists(-1) is False
