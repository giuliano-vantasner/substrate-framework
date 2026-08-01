from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.circular_pair import (
    conditional_equal_mass_circular_power,
    conditional_equal_mass_circular_waveform,
    equal_mass_circular_pair_moments,
)
from substrate_framework.tt_angular import (
    conditional_tt_power,
    frobenius_norm_squared,
)


def test_equal_mass_pair_has_fixed_monopole_zero_dipole_and_declared_separation() -> None:
    time, mass, radius, frequency = sp.symbols(
        "t m a Omega", positive=True, real=True
    )
    moments = equal_mass_circular_pair_moments(mass, radius, frequency, time)
    assert moments.monopole == 2 * mass
    assert moments.dipole == sp.zeros(3, 1)
    assert moments.triple_normalized_quadrupole == 3 * moments.trace_free_second_moment


def test_normalized_stf_derivative_norms_have_correct_orbital_radius_factors() -> None:
    time, mass, radius, frequency = sp.symbols(
        "t m a Omega", positive=True, real=True
    )
    moments = equal_mass_circular_pair_moments(mass, radius, frequency, time)
    second = sp.simplify(moments.trace_free_second_moment.diff(time, 2))
    third = sp.simplify(moments.trace_free_second_moment.diff(time, 3))
    assert sp.trigsimp(frobenius_norm_squared(second)) == (
        32 * mass**2 * radius**4 * frequency**4
    )
    assert sp.trigsimp(frobenius_norm_squared(third)) == (
        128 * mass**2 * radius**4 * frequency**6
    )
    assert sp.trigsimp(
        frobenius_norm_squared(3 * third)
    ) == 1152 * mass**2 * radius**4 * frequency**6


def test_arbitrary_inclination_conventional_waveform_is_exact() -> None:
    time, mass, radius, frequency, inclination, wave, distance = sp.symbols(
        "t m a Omega i A R", positive=True, real=True
    )
    result = conditional_equal_mass_circular_waveform(
        mass,
        radius,
        frequency,
        time,
        inclination,
        wave,
        distance,
    )
    phase = 2 * frequency * time
    expected_plus = (
        -2
        * wave
        * mass
        * radius**2
        * frequency**2
        * (1 + sp.cos(inclination) ** 2)
        * sp.cos(phase)
        / distance
    )
    expected_cross = (
        -4
        * wave
        * mass
        * radius**2
        * frequency**2
        * sp.cos(inclination)
        * sp.sin(phase)
        / distance
    )
    assert sp.trigsimp(result.conventional_plus - expected_plus) == 0
    assert sp.trigsimp(result.conventional_cross - expected_cross) == 0
    assert sp.simplify(
        result.normalized_plus_coordinate - sp.sqrt(2) * result.conventional_plus
    ) == 0
    assert sp.simplify(
        result.normalized_cross_coordinate - sp.sqrt(2) * result.conventional_cross
    ) == 0


def test_face_on_and_edge_on_limits_are_distinct() -> None:
    time, mass, radius, frequency, wave, distance = sp.symbols(
        "t m a Omega A R", positive=True, real=True
    )
    face = conditional_equal_mass_circular_waveform(
        mass, radius, frequency, time, 0, wave, distance
    )
    edge = conditional_equal_mass_circular_waveform(
        mass, radius, frequency, time, sp.pi / 2, wave, distance
    )
    phase = 2 * frequency * time
    assert sp.trigsimp(
        face.conventional_plus
        + 4 * wave * mass * radius**2 * frequency**2 * sp.cos(phase) / distance
    ) == 0
    assert sp.trigsimp(
        face.conventional_cross
        + 4 * wave * mass * radius**2 * frequency**2 * sp.sin(phase) / distance
    ) == 0
    assert edge.conventional_cross == 0
    assert sp.trigsimp(
        edge.conventional_plus
        + 2 * wave * mass * radius**2 * frequency**2 * sp.cos(phase) / distance
    ) == 0


def test_normalized_and_triple_quadrupole_waveforms_are_identical_after_rescaling() -> None:
    time, mass, radius, frequency, coupling = sp.symbols(
        "t m a Omega G", positive=True, real=True
    )
    result = conditional_equal_mass_circular_waveform(
        mass, radius, frequency, time, 0, 2 * coupling, 1
    )
    normalized = result.normalized_stf_second_derivative
    triple = 3 * normalized
    normalized_field = 2 * coupling * normalized
    triple_field = 2 * coupling / 3 * triple
    assert sp.simplify(normalized_field - triple_field) == sp.zeros(3)


def test_corrected_conditional_power_is_128_over_five_in_orbital_radius() -> None:
    mass, radius, frequency, coupling = sp.symbols(
        "m a Omega G", positive=True, real=True
    )
    flux = 1 / (32 * sp.pi * coupling)
    power = conditional_equal_mass_circular_power(
        mass, radius, frequency, 2 * coupling, flux
    )
    assert sp.trigsimp(
        power
        - sp.Rational(128, 5)
        * coupling
        * mass**2
        * radius**4
        * frequency**6
    ) == 0


def test_gw4_triple_convention_power_is_nine_times_corrected_power() -> None:
    time, mass, radius, frequency, coupling = sp.symbols(
        "t m a Omega G", positive=True, real=True
    )
    moments = equal_mass_circular_pair_moments(mass, radius, frequency, time)
    normalized_third = sp.simplify(
        moments.trace_free_second_moment.diff(time, 3)
    )
    flux = 1 / (32 * sp.pi * coupling)
    correct = conditional_tt_power(normalized_third, 2 * coupling, flux)
    source = conditional_tt_power(3 * normalized_third, 2 * coupling, flux)
    assert sp.trigsimp(source - 9 * correct) == 0


def test_invalid_time_and_distance_are_rejected() -> None:
    with pytest.raises(ValueError, match="time"):
        equal_mass_circular_pair_moments(1, 1, 1, 0)
    time = sp.symbols("t")
    with pytest.raises(ValueError, match="distance"):
        conditional_equal_mass_circular_waveform(1, 1, 1, time, 0, 1, 0)
