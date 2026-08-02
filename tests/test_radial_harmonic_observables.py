from __future__ import annotations

import numpy as np
import pytest
from scipy.special import jv

from substrate_framework.radial_harmonic_observables import (
    integrate_spherical_radial_density,
    periodic_fourier_coefficients,
    radial_harmonic_energy_density,
    radial_harmonic_kinematics,
    spherical_radial_second_moment_tensor,
    time_averaged_per_axis_energy_variance,
)


def test_kinematics_includes_harmonic_index_and_frequency() -> None:
    phase = np.array([0.0, np.pi / 2.0])
    kinematics = radial_harmonic_kinematics(
        [[2.0], [0.5]],
        [[-0.3], [0.2]],
        (1, 3),
        0.8,
        phase,
    )

    np.testing.assert_allclose(kinematics.field[:, 0], [2.5, 0.0], atol=2.0e-15)
    np.testing.assert_allclose(
        kinematics.time_derivative[:, 0],
        [0.0, -0.8 * (2.0 - 3.0 * 0.5)],
        atol=2.0e-15,
    )
    np.testing.assert_allclose(
        kinematics.radial_derivative[:, 0], [-0.1, 0.0], atol=2.0e-15
    )


def test_odd_field_harmonics_give_only_even_energy_harmonics() -> None:
    phase = 2.0 * np.pi * np.arange(512) / 512
    amplitudes = np.array([[1.2, 0.8], [-0.2, 0.1], [0.03, -0.02]])
    derivatives = np.array([[-0.1, 0.2], [0.04, -0.03], [-0.01, 0.005]])
    density = radial_harmonic_energy_density(
        amplitudes, derivatives, (1, 3, 5), 0.91, phase
    )
    shifted = radial_harmonic_energy_density(
        amplitudes, derivatives, (1, 3, 5), 0.91, phase + np.pi
    )
    spectrum = periodic_fourier_coefficients(density, max_harmonic=15)

    np.testing.assert_allclose(shifted, density, atol=3.0e-15)
    assert np.max(spectrum.amplitude[1::2]) < 2.0e-15


def test_single_mode_two_frequency_coefficient_includes_every_energy_term() -> None:
    phase = 2.0 * np.pi * np.arange(2048) / 2048
    amplitude, derivative, frequency = 0.8, 0.3, 0.9
    density = radial_harmonic_energy_density(
        [[amplitude]], [[derivative]], (1,), frequency, phase
    )
    spectrum = periodic_fourier_coefficients(density[:, 0], max_harmonic=6)
    expected = (
        derivative**2 / 4.0
        - frequency**2 * amplitude**2 / 4.0
        + 2.0 * jv(2, amplitude)
    )

    assert spectrum.cosine[1] == pytest.approx(0.0, abs=2.0e-15)
    assert spectrum.cosine[2] == pytest.approx(expected, abs=2.0e-15)


def test_even_selection_does_not_force_a_nonzero_two_frequency_line() -> None:
    phase = 2.0 * np.pi * np.arange(2048) / 2048
    amplitude, frequency = 1.0, 0.97
    derivative_squared = frequency**2 * amplitude**2 - 8.0 * jv(2, amplitude)
    assert derivative_squared > 0.0
    density = radial_harmonic_energy_density(
        [[amplitude]],
        [[np.sqrt(derivative_squared)]],
        (1,),
        frequency,
        phase,
    )
    spectrum = periodic_fourier_coefficients(density[:, 0], max_harmonic=8)

    assert spectrum.amplitude[1] < 2.0e-15
    assert spectrum.amplitude[2] < 2.0e-15
    assert spectrum.amplitude[4] > 1.0e-3


def test_direct_real_fourier_normalization_recovers_phase() -> None:
    phase = 2.0 * np.pi * np.arange(256) / 256
    values = 1.4 + 0.7 * np.cos(4.0 * phase) - 0.2 * np.sin(6.0 * phase)
    spectrum = periodic_fourier_coefficients(values, max_harmonic=8)

    assert spectrum.cosine[0] == pytest.approx(1.4, abs=1.0e-14)
    assert spectrum.cosine[4] == pytest.approx(0.7, abs=1.0e-14)
    assert spectrum.sine[6] == pytest.approx(-0.2, abs=1.0e-14)
    assert np.max(np.delete(spectrum.amplitude, [0, 4, 6])) < 2.0e-15


def test_spherical_moment_is_isotropic_and_uses_spherical_measure() -> None:
    radius = np.linspace(0.0, 2.0, 1001)
    density = np.ones((3, radius.size))
    energy = integrate_spherical_radial_density(radius, density)
    second = integrate_spherical_radial_density(radius, density, radial_power=2)
    tensor = spherical_radial_second_moment_tensor(radius, density)
    trace_free = tensor - np.trace(tensor, axis1=-2, axis2=-1)[..., None, None] * np.eye(3) / 3.0

    np.testing.assert_allclose(energy, 4.0 * np.pi * 2.0**3 / 3.0, rtol=2.0e-6)
    np.testing.assert_allclose(second, 4.0 * np.pi * 2.0**5 / 5.0, rtol=7.0e-6)
    np.testing.assert_allclose(trace_free, 0.0, atol=2.0e-15)
    assert time_averaged_per_axis_energy_variance(radius, density) == pytest.approx(
        2.0**2 / 5.0, rel=8.0e-6
    )


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: periodic_fourier_coefficients([1.0, 2.0, 3.0], max_harmonic=1),
            "at least four",
        ),
        (
            lambda: periodic_fourier_coefficients(np.ones(8), max_harmonic=4),
            "Nyquist",
        ),
        (
            lambda: radial_harmonic_kinematics([[1.0]], [[1.0], [2.0]], (1,), 0.9, [0.0]),
            "one row",
        ),
        (
            lambda: integrate_spherical_radial_density([0.0, 1.0], [1.0], radial_power=0),
            "one final-axis",
        ),
        (
            lambda: time_averaged_per_axis_energy_variance(
                [0.0, 1.0], np.zeros((4, 2))
            ),
            "positive",
        ),
    ],
)
def test_invalid_observable_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
