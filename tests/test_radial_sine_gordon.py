from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.radial_sine_gordon import (
    estimate_angular_frequency,
    estimate_peak_angular_frequency,
    evolve_radial_sine_gordon_leapfrog,
    gaussian_radial_seed,
    radial_gradient,
    radial_laplacian,
    radial_sine_gordon_energy,
    radial_sine_gordon_energy_radius_moment,
)


def test_radial_operator_has_regular_origin_and_quadratic_limit() -> None:
    spacing = 0.05
    radius = spacing * np.arange(101)
    field = radius**2
    laplacian = radial_laplacian(field, spacing)
    assert np.allclose(laplacian[:-1], 6.0, atol=2.0e-12)
    assert radial_gradient(field, spacing)[0] == 0.0


def test_geometry_mutation_breaks_three_dimensional_quadratic_limit() -> None:
    spacing = 0.1
    radius = spacing * np.arange(51)
    field = radius**2
    assert np.allclose(radial_laplacian(field, spacing)[:-1], 6.0)
    assert np.allclose(
        radial_laplacian(field, spacing, geometric_coefficient=0.0)[:-1], 2.0
    )


def test_energy_uses_spherical_measure_and_current_trapezoid_api() -> None:
    radius = np.linspace(0.0, 2.0, 101)
    field = np.zeros_like(radius)
    velocity = np.ones_like(radius)
    expected = 2.0 * np.pi * 2.0**3 / 3.0
    assert radial_sine_gordon_energy(field, velocity, radius) == pytest.approx(
        expected, rel=2.0e-4
    )
    expected_radius_moment = 2.0 * np.pi * 2.0**5 / 5.0
    assert radial_sine_gordon_energy_radius_moment(
        field, velocity, radius
    ) == pytest.approx(expected_radius_moment, rel=7.0e-4)


def test_frequency_estimates_agree_for_a_known_signal() -> None:
    time = np.linspace(0.0, 100.0, 5001)
    trace = 1.2 * np.cos(0.83 * time + 0.2) + 0.08 * np.cos(1.66 * time)
    evidence = estimate_angular_frequency(time, trace, window_start=20.0)
    assert evidence.spectral_omega == pytest.approx(0.83, abs=2.0e-3)
    assert evidence.crossing_omega == pytest.approx(0.83, abs=2.0e-3)
    assert evidence.crossing_cycles >= 9


def test_peak_frequency_handles_linear_drift_and_harmonics() -> None:
    time = np.linspace(0.0, 100.0, 5001)
    trace = (
        0.03 * time
        + 1.2 * np.cos(1.66 * time + 0.2)
        + 0.08 * np.cos(3.32 * time)
    )
    evidence = estimate_peak_angular_frequency(
        time,
        trace,
        window_start=20.0,
        minimum_period=2.5,
    )
    assert evidence.angular_frequency == pytest.approx(1.66, abs=2.0e-3)
    assert evidence.relative_period_standard_deviation < 0.01
    assert evidence.cycles >= 19


def test_short_leapfrog_run_completes_with_finite_diagnostics() -> None:
    result = evolve_radial_sine_gordon_leapfrog(
        amplitude=0.2,
        width=3.0,
        spacing=0.2,
        outer_radius=20.0,
        final_time=2.0,
        core_radius=5.0,
        sample_interval=0.2,
    )
    assert result.completed
    assert result.method == "centered-leapfrog"
    assert result.time.size >= 9
    assert np.all(np.isfinite(result.total_energy))
    assert np.all(np.isfinite(result.core_energy_radius_moment))
    assert np.all(np.isfinite(result.total_energy_radius_moment))
    assert result.total_energy.min() > 0.0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: gaussian_radial_seed([0.0, 1.0, 2.0], 1.0, 0.0), "width"),
        (lambda: radial_laplacian([0.0, 1.0], 0.1), "three"),
        (
            lambda: radial_sine_gordon_energy(
                [0.0, 0.0, 0.0], [0.0, 0.0], [0.0, 1.0, 2.0]
            ),
            "same size",
        ),
        (
            lambda: evolve_radial_sine_gordon_leapfrog(
                amplitude=1.0,
                width=1.0,
                spacing=0.1,
                outer_radius=10.05,
                final_time=1.0,
                core_radius=5.0,
            ),
            "integer multiple",
        ),
    ],
)
def test_invalid_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
