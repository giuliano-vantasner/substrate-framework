"""Exact ensemble stress-energy checks for toronic flux tubes (issue #26)."""

from __future__ import annotations

import sympy as sp

from substrate_framework.flux_tube_ensemble import (
    boost_orbit_measure_volume,
    euclidean_plane_measure_is_finite,
    isotropic_average_equation_of_state,
    modulus_stationary_point_exists,
    orientation_average_nn,
    tube_longitudinal_pressure,
    tube_transverse_pressure,
)


def test_single_tube_pressures_for_casimir_scaling() -> None:
    c = sp.Symbol("c", positive=True)
    L = sp.Symbol("L", positive=True)
    rho = -c * L**-4
    assert sp.simplify(tube_longitudinal_pressure(c) + rho) == 0  # p_∥ = -rho
    assert sp.simplify(tube_transverse_pressure(c) - rho) == 0  # p_⊥ = +rho


def test_orientation_average_is_delta_over_three() -> None:
    for i in range(3):
        for j in range(3):
            expected = sp.Rational(1, 3) if i == j else sp.Rational(0)
            assert orientation_average_nn(i, j) == expected


def test_isotropic_ensemble_has_w_equals_one_third() -> None:
    c = sp.Symbol("c", positive=True)
    assert isotropic_average_equation_of_state(c) == sp.Rational(1, 3)


def test_no_normalizable_boost_invariant_ensemble() -> None:
    assert boost_orbit_measure_volume() is sp.oo
    # compact Euclidean contrast: the O(4) membrane measure is finite
    assert euclidean_plane_measure_is_finite() is True


def test_modulus_has_no_stationary_point_either_sign() -> None:
    assert modulus_stationary_point_exists(1) is False
    assert modulus_stationary_point_exists(-1) is False
