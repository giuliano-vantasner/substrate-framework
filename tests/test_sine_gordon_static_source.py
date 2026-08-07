import pytest
import sympy as sp

from substrate_framework.dimensional_sine_gordon import dimensional_sine_gordon_coefficients
from substrate_framework.sine_gordon_static_source import (
    sine_gordon_static_source_enclosure,
)


def test_static_breather_source_has_a_quadratic_profile_error_enclosure() -> None:
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    supplied_newton = sp.Rational(7, 13)
    near = sine_gordon_static_source_enclosure(
        sp.Rational(4, 5), coefficients, supplied_newton, 10
    )
    far = sine_gordon_static_source_enclosure(
        sp.Rational(4, 5), coefficients, supplied_newton, 20
    )
    assert near.source_energy == far.source_energy == sp.Rational(576, 5)
    assert near.source_mass == far.source_mass == sp.Rational(144, 5)
    assert far.maximum_relative_profile_error == near.maximum_relative_profile_error / 4
    assert near.maximum_relative_profile_error < 1
    assert near.exact_potential_lower_bound < near.exact_potential_upper_bound < 0
    assert near.newton_constant == supplied_newton
    assert near.monopole_compactness == -near.monopole.potential_over_speed_squared


def test_static_source_enclosure_rejects_an_uncontrolled_near_profile() -> None:
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    with pytest.raises(ValueError, match="profile error"):
        sine_gordon_static_source_enclosure(
            sp.Rational(4, 5),
            coefficients,
            1,
            sp.Rational(1, 2),
        )


def test_supplied_newton_constant_scales_the_bounds_but_not_the_error() -> None:
    coefficients = dimensional_sine_gordon_coefficients(2, 8, 18)
    baseline = sine_gordon_static_source_enclosure(
        sp.Rational(4, 5), coefficients, 3, 10
    )
    scaled = sine_gordon_static_source_enclosure(
        sp.Rational(4, 5), coefficients, 15, 10
    )
    assert scaled.maximum_relative_profile_error == baseline.maximum_relative_profile_error
    assert scaled.exact_potential_lower_bound == 5 * baseline.exact_potential_lower_bound
    assert scaled.exact_potential_upper_bound == 5 * baseline.exact_potential_upper_bound
