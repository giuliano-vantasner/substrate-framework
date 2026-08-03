from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from substrate_framework.first_passage import (
    free_reflected_absorbing_mfpt,
    linear_potential_reflected_absorbing_mfpt,
    quadratic_barrier_gradient,
    quadratic_barrier_potential,
    reflected_absorbing_backward_residual,
    reflected_absorbing_mfpt,
    simulate_reflected_euler_maruyama,
    summarize_censored_first_passage,
    thresholded_completed_only_rate,
)


@pytest.mark.parametrize("force", [-1.2, 0.0, 0.7, 2.0])
def test_adaptive_integral_matches_exact_linear_force_control(force: float) -> None:
    length = 1.4
    theta = 0.8
    gamma = 1.3
    evidence = reflected_absorbing_mfpt(
        lambda coordinate: force * coordinate,
        0.0,
        0.0,
        length,
        theta,
        gamma,
        epsabs=1.0e-12,
        epsrel=1.0e-12,
    )
    expected = linear_potential_reflected_absorbing_mfpt(
        force,
        length,
        theta,
        gamma,
    )
    assert evidence.mean_first_passage_time == pytest.approx(expected, rel=2.0e-11)
    assert evidence.outer_absolute_error < 1.0e-10
    assert evidence.maximum_inner_absolute_error < 1.0e-10
    assert evidence.inner_evaluations > 0


def test_zero_force_formula_and_absorbing_start_limit() -> None:
    expected = free_reflected_absorbing_mfpt(2.0, 0.5, 3.0)
    assert expected == 12.0
    evidence = reflected_absorbing_mfpt(
        lambda _coordinate: 4.0,
        2.0,
        0.0,
        2.0,
        0.5,
        3.0,
    )
    assert evidence.mean_first_passage_time == 0.0
    assert np.isinf(evidence.inverse_mean_first_passage_time)


def test_additive_potential_constant_cancels() -> None:
    base = reflected_absorbing_mfpt(
        lambda coordinate: 2.0 * coordinate - coordinate**2,
        0.0,
        0.0,
        1.6,
        0.7,
        1.0,
    )
    shifted = reflected_absorbing_mfpt(
        lambda coordinate: 123.0 + 2.0 * coordinate - coordinate**2,
        0.0,
        0.0,
        1.6,
        0.7,
        1.0,
    )
    assert shifted.mean_first_passage_time == pytest.approx(
        base.mean_first_passage_time,
        rel=2.0e-13,
    )


def test_backward_residual_and_quadratic_barrier_derivative() -> None:
    coordinate = 0.3
    energy = 2.5
    gradient = quadratic_barrier_gradient(coordinate, energy)
    step = 1.0e-5
    finite_difference = (
        quadratic_barrier_potential(coordinate + step, energy)
        - quadratic_barrier_potential(coordinate - step, energy)
    ) / (2.0 * step)
    assert finite_difference == pytest.approx(gradient, rel=2.0e-11)
    assert reflected_absorbing_backward_residual(0.8, 1.2, gradient, 0.4, 0.25) == pytest.approx(
        0.8 * 0.25 - gradient * 0.4 + 1.2
    )


def test_censoring_summary_does_not_call_missing_paths_zero_time() -> None:
    summary = summarize_censored_first_passage(
        [1.0, 2.0, np.nan, np.nan],
        [True, True, False, False],
        10.0,
    )
    assert summary.completed_count == 2
    assert summary.completion_fraction == 0.5
    assert summary.completed_only_mean == 1.5
    assert summary.inverse_completed_only_mean == pytest.approx(2.0 / 3.0)
    assert summary.restricted_mean == 5.75
    assert summary.inverse_restricted_mean == pytest.approx(1.0 / 5.75)
    assert thresholded_completed_only_rate(summary, 0.6) == 0.0
    assert thresholded_completed_only_rate(summary, 0.5) == pytest.approx(2.0 / 3.0)


def test_reflected_euler_maruyama_is_seeded_and_reports_censoring() -> None:
    options = dict(
        potential_gradient=lambda coordinate: 2.0 * (1.0 - coordinate),
        initial_coordinate=0.0,
        reflecting_boundary=0.0,
        absorbing_boundary=1.6,
        thermal_scale=1.0,
        friction=1.0,
        trajectory_count=128,
        time_step=0.01,
        horizon=1.0,
        seed=42,
    )
    first = simulate_reflected_euler_maruyama(**options)
    second = simulate_reflected_euler_maruyama(**options)
    np.testing.assert_array_equal(first.completed, second.completed)
    np.testing.assert_allclose(first.event_times, second.event_times, equal_nan=True)
    assert first.reflection_rule == "absolute_overshoot"
    assert np.all(first.final_coordinates >= 0.0)
    assert first.summary.trajectory_count == 128
    assert 0.0 <= first.summary.completion_fraction <= 1.0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: reflected_absorbing_mfpt(lambda coordinate: coordinate, -0.1, 0.0, 1.0, 1.0, 1.0),
            "closed interval",
        ),
        (
            lambda: reflected_absorbing_mfpt(lambda coordinate: coordinate, 0.0, 1.0, 0.0, 1.0, 1.0),
            "must exceed",
        ),
        (
            lambda: summarize_censored_first_passage([1.0, 2.0], [True, False], 1.5),
            "censored event times must be NaN",
        ),
        (
            lambda: simulate_reflected_euler_maruyama(
                lambda coordinate: coordinate,
                0.0,
                0.0,
                1.0,
                1.0,
                1.0,
                trajectory_count=10,
                time_step=0.3,
                horizon=1.0,
                seed=1,
            ),
            "integer multiple",
        ),
    ],
)
def test_invalid_first_passage_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()


def test_canonical_module_uses_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/first_passage.py").read_text(encoding="utf-8")
    assert "np.tr" + "apz" not in source
