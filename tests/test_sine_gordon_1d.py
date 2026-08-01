import numpy as np
import pytest

from substrate_framework import (
    SolverTolerances,
    endpoint_charge_coordinate,
    evolve_driven_sine_gordon_leapfrog,
    evolve_driven_sine_gordon_mol,
    evolve_periodic_sine_gordon_leapfrog,
    evolve_periodic_sine_gordon_mol,
    gaussian_sine_neumann_drive,
    moving_breather_samples,
    sampled_boundary_sign_correlation,
)


def test_moving_breather_samples_match_independent_finite_differences() -> None:
    coordinate = np.linspace(-2.0, 2.0, 17)
    time = 0.7
    step = 1.0e-6
    field, velocity, derivative = moving_breather_samples(
        coordinate,
        time,
        0.6,
        velocity=-0.2,
        center=0.4,
    )
    field_later, _, _ = moving_breather_samples(
        coordinate,
        time + step,
        0.6,
        velocity=-0.2,
        center=0.4,
    )
    field_earlier, _, _ = moving_breather_samples(
        coordinate,
        time - step,
        0.6,
        velocity=-0.2,
        center=0.4,
    )
    field_right, _, _ = moving_breather_samples(
        coordinate + step,
        time,
        0.6,
        velocity=-0.2,
        center=0.4,
    )
    field_left, _, _ = moving_breather_samples(
        coordinate - step,
        time,
        0.6,
        velocity=-0.2,
        center=0.4,
    )
    assert field.shape == coordinate.shape
    assert velocity == pytest.approx((field_later - field_earlier) / (2.0 * step), abs=2e-8)
    assert derivative == pytest.approx((field_right - field_left) / (2.0 * step), abs=2e-8)


def test_endpoint_charge_coordinate_does_not_force_integer_winding() -> None:
    assert endpoint_charge_coordinate(0.3, 1.7) == pytest.approx(
        (1.7 - 0.3) / (2.0 * np.pi)
    )
    assert endpoint_charge_coordinate(0.0, 2.0 * np.pi) == pytest.approx(1.0)


def test_sampled_boundary_correlation_matches_harmonic_limit() -> None:
    omega = 0.7
    amplitude = 1.3
    derivative_amplitude = -0.8
    phase = 0.4
    exact = 4.0 * derivative_amplitude * np.cos(phase) / omega
    errors = []
    for sample_count in (1001, 2001, 4001):
        time = np.linspace(0.0, 2.0 * np.pi / omega, sample_count)
        velocity = amplitude * np.sin(omega * time)
        derivative = derivative_amplitude * np.sin(omega * time + phase)
        correlation = sampled_boundary_sign_correlation(time, velocity, derivative)
        errors.append(abs(correlation - exact))
    assert errors[1] < errors[0] / 1.9
    assert errors[2] < errors[1] / 1.9
    assert errors[-1] / abs(exact) < 3.0e-4


def test_periodic_breather_evolution_has_second_order_self_convergence() -> None:
    errors = []
    drifts = []
    for point_count in (128, 256, 512):
        coordinate = np.linspace(-20.0, 20.0, point_count, endpoint=False)
        field0, velocity0, _ = moving_breather_samples(coordinate, 0.0, 0.6)
        spacing = coordinate[1] - coordinate[0]
        result = evolve_periodic_sine_gordon_leapfrog(
            coordinate,
            field0,
            velocity0,
            2.0,
            0.2 * spacing,
            sample_stride=8,
        )
        exact, _, _ = moving_breather_samples(coordinate, 2.0, 0.6)
        errors.append(float(np.sqrt(np.mean(np.square(result.field[-1] - exact)))))
        drifts.append(float(np.ptp(result.energy) / result.energy[0]))

    assert errors[1] < errors[0] / 3.8
    assert errors[2] < errors[1] / 3.8
    assert drifts[1] < drifts[0] / 3.8
    assert drifts[2] < drifts[1] / 3.8
    assert errors[-1] < 2.0e-4


def test_periodic_dop853_is_independent_time_method_cross_check() -> None:
    coordinate = np.linspace(-20.0, 20.0, 256, endpoint=False)
    field0, velocity0, _ = moving_breather_samples(coordinate, 0.0, 0.6)
    leapfrog = evolve_periodic_sine_gordon_leapfrog(
        coordinate,
        field0,
        velocity0,
        2.0,
        0.03,
        sample_stride=7,
    )
    adaptive = evolve_periodic_sine_gordon_mol(
        coordinate,
        field0,
        velocity0,
        np.linspace(0.0, 2.0, 11),
        tolerances=SolverTolerances(rtol=1.0e-10, atol=1.0e-12, max_step=0.05),
    )
    difference = np.sqrt(np.mean(np.square(leapfrog.field[-1] - adaptive.field[-1])))
    assert adaptive.method.endswith("DOP853")
    assert adaptive.function_evaluations is not None
    assert difference < 2.0e-4
    assert np.ptp(adaptive.energy) / adaptive.energy[0] < 1.0e-9


def test_zero_driven_problem_is_an_exact_rejection_guard_for_both_methods() -> None:
    coordinate = np.linspace(0.0, 10.0, 101)
    zero = np.zeros_like(coordinate)
    leapfrog = evolve_driven_sine_gordon_leapfrog(
        coordinate,
        zero,
        zero,
        lambda _time: 0.0,
        1.0,
        0.04,
        bulk_start=2.0,
    )
    adaptive = evolve_driven_sine_gordon_mol(
        coordinate,
        zero,
        zero,
        lambda _time: 0.0,
        np.linspace(0.0, 1.0, 21),
        bulk_start=2.0,
    )
    for result in (leapfrog, adaptive):
        assert result.final_field == pytest.approx(zero)
        assert result.final_velocity == pytest.approx(zero)
        assert result.endpoint_charge_coordinate == 0.0
        assert result.bulk_endpoint_charge_coordinate == 0.0
        assert result.boundary_sign_correlation == 0.0
        assert result.energy_balance_residual == 0.0


def test_gaussian_neumann_drive_keeps_sign_and_phase_explicit() -> None:
    positive = gaussian_sine_neumann_drive(2.0, 0.5, 3.0, 1.2, 0.4)
    negative = gaussian_sine_neumann_drive(-2.0, 0.5, 3.0, 1.2, 0.4)
    shifted = gaussian_sine_neumann_drive(2.0, 0.5, 3.0, 1.2, 0.4 + np.pi)
    for time in (0.0, 2.5, 3.0, 5.0):
        assert negative(time) == pytest.approx(-positive(time))
        assert shifted(time) == pytest.approx(-positive(time), abs=1.0e-14)


def test_evolvers_reject_inconsistent_grid_or_courant_step() -> None:
    nonuniform = np.array([0.0, 0.1, 0.2, 0.4, 0.5])
    zero = np.zeros_like(nonuniform)
    with pytest.raises(ValueError, match="uniformly"):
        evolve_periodic_sine_gordon_leapfrog(
            nonuniform,
            zero,
            zero,
            1.0,
            0.01,
        )

    coordinate = np.linspace(0.0, 1.0, 11)
    zero = np.zeros_like(coordinate)
    with pytest.raises(ValueError, match="time_step/spatial_step"):
        evolve_driven_sine_gordon_leapfrog(
            coordinate,
            zero,
            zero,
            lambda _time: 0.0,
            1.0,
            0.2,
            bulk_start=0.5,
        )
