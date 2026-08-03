from __future__ import annotations

import pytest
import sympy as sp
import substrate_framework as framework

from substrate_framework.coherence_gates import (
    activated_relative_response,
    brownian_mean_phasor_window_average,
    brownian_pair_coherence_window_average,
    brownian_phase_characteristic,
    brownian_phase_pair_coherence,
    continuous_population_threshold,
    damped_brownian_coherent_mean_factor,
    damped_brownian_coherent_quadratic_factor,
    gaussian_phase_pair_coherence,
    iid_equal_amplitude_expected_intensity,
    population_activation_scale,
)


def test_public_package_exports_the_coherence_gate_api() -> None:
    assert framework.iid_equal_amplitude_expected_intensity is (
        iid_equal_amplitude_expected_intensity
    )
    assert framework.gaussian_phase_pair_coherence is gaussian_phase_pair_coherence
    assert framework.population_activation_scale is population_activation_scale
    assert framework.continuous_population_threshold is continuous_population_threshold
    assert framework.activated_relative_response is activated_relative_response
    assert framework.brownian_phase_characteristic is brownian_phase_characteristic
    assert framework.brownian_phase_pair_coherence is brownian_phase_pair_coherence
    assert (
        framework.brownian_mean_phasor_window_average
        is brownian_mean_phasor_window_average
    )
    assert (
        framework.brownian_pair_coherence_window_average
        is brownian_pair_coherence_window_average
    )
    assert (
        framework.damped_brownian_coherent_mean_factor
        is damped_brownian_coherent_mean_factor
    )
    assert (
        framework.damped_brownian_coherent_quadratic_factor
        is damped_brownian_coherent_quadratic_factor
    )


def test_iid_equal_amplitude_sum_separates_diagonal_and_pairs() -> None:
    count = sp.Symbol("N", integer=True, positive=True)
    intensity = sp.Symbol("I_1", positive=True)
    coherence = sp.Symbol("V", real=True)
    expected = iid_equal_amplitude_expected_intensity(
        count, intensity, coherence
    )
    assert sp.expand(expected) == sp.expand(
        intensity * (count + count * (count - 1) * coherence)
    )
    assert expected.subs(coherence, 0) == count * intensity
    assert expected.subs(coherence, 1) == count**2 * intensity
    assert expected.subs(count, 1) == intensity


def test_gaussian_phase_coherence_uses_the_squared_mean_phasor() -> None:
    variance = sp.Symbol("sigma_squared", nonnegative=True)
    mean_phasor = sp.exp(-variance / 2)
    assert gaussian_phase_pair_coherence(variance) == mean_phasor**2
    assert gaussian_phase_pair_coherence(0) == 1
    assert sp.limit(gaussian_phase_pair_coherence(variance), variance, sp.oo) == 0


def test_brownian_phase_characteristic_fixes_time_and_harmonic_dependence() -> None:
    diffusion = sp.Symbol("D", nonnegative=True)
    time = sp.Symbol("t", nonnegative=True)
    harmonic = sp.Symbol("n", integer=True)
    characteristic = brownian_phase_characteristic(diffusion, time, harmonic)
    assert characteristic == sp.exp(-(harmonic**2) * diffusion * time)
    assert sp.simplify(
        sp.diff(characteristic, time)
        + diffusion * harmonic**2 * characteristic
    ) == 0
    assert brownian_phase_characteristic(0, time, harmonic) == 1
    assert brownian_phase_characteristic(diffusion, 0, harmonic) == 1


def test_brownian_pair_coherence_uses_full_phase_variance() -> None:
    diffusion = sp.Symbol("D", nonnegative=True)
    time = sp.Symbol("t", nonnegative=True)
    mean_phasor = brownian_phase_characteristic(diffusion, time)
    pair_coherence = brownian_phase_pair_coherence(diffusion, time)
    assert mean_phasor == sp.exp(-diffusion * time)
    assert pair_coherence == sp.exp(-2 * diffusion * time)
    assert pair_coherence == mean_phasor**2
    assert pair_coherence == gaussian_phase_pair_coherence(2 * diffusion * time)


def test_brownian_window_averages_are_not_endpoint_values() -> None:
    diffusion = sp.Symbol("D", positive=True)
    window = sp.Symbol("T", positive=True)
    mean_average = brownian_mean_phasor_window_average(diffusion, window)
    pair_average = brownian_pair_coherence_window_average(diffusion, window)
    assert mean_average == (1 - sp.exp(-diffusion * window)) / (
        diffusion * window
    )
    assert pair_average == (1 - sp.exp(-2 * diffusion * window)) / (
        2 * diffusion * window
    )
    assert sp.simplify(mean_average - sp.exp(-diffusion * window)) != 0
    assert sp.simplify(pair_average - sp.exp(-2 * diffusion * window)) != 0
    assert brownian_mean_phasor_window_average(0, window) == 1
    assert brownian_pair_coherence_window_average(0, window) == 1


def test_damped_brownian_mean_and_quadratic_factors_remain_distinct() -> None:
    damping = sp.Symbol("Gamma", nonnegative=True)
    diffusion = sp.Symbol("D", nonnegative=True)
    time = sp.Symbol("t", nonnegative=True)
    mean_factor = damped_brownian_coherent_mean_factor(
        damping,
        diffusion,
        time,
    )
    quadratic_factor = damped_brownian_coherent_quadratic_factor(
        damping,
        diffusion,
        time,
    )
    assert mean_factor == sp.exp(-(damping / 2 + diffusion) * time)
    assert sp.simplify(
        quadratic_factor - sp.exp(-(damping + 2 * diffusion) * time)
    ) == 0
    assert sp.simplify(quadratic_factor - mean_factor**2) == 0


def test_population_threshold_solves_the_declared_scale() -> None:
    barrier, unit = sp.symbols("E theta", positive=True)
    coherence = sp.Symbol("V", positive=True)
    threshold = continuous_population_threshold(barrier, unit, coherence)
    assert sp.simplify(
        unit * threshold * (1 + (threshold - 1) * coherence) - barrier
    ) == 0
    assert continuous_population_threshold(barrier, unit, 0) == barrier / unit
    assert continuous_population_threshold(barrier, unit, 1) == sp.sqrt(
        barrier / unit
    )


def test_coherent_threshold_order_requires_barrier_over_unit_above_one() -> None:
    assert continuous_population_threshold(4, 1, 1) == 2
    assert continuous_population_threshold(4, 1, 0) == 4
    assert continuous_population_threshold(1, 4, 1) == sp.Rational(1, 2)
    assert continuous_population_threshold(1, 4, 0) == sp.Rational(1, 4)


def test_activated_response_is_a_factor_and_increases_with_scale() -> None:
    barrier, scale = sp.symbols("E Theta", positive=True)
    response = activated_relative_response(barrier, scale)
    assert response == sp.exp(-barrier / scale)
    assert sp.diff(response, scale).is_positive
    assert sp.diff(response, barrier).is_negative
    assert sp.limit(response, scale, 0, dir="+") == 0
    assert sp.limit(response, scale, sp.oo) == 1


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: iid_equal_amplitude_expected_intensity(2.0, 1, 0), "count"),
        (lambda: iid_equal_amplitude_expected_intensity(0, 1, 0), "count"),
        (lambda: iid_equal_amplitude_expected_intensity(2, 0, 0), "intensity"),
        (lambda: iid_equal_amplitude_expected_intensity(2, 1, 2), "interval"),
        (lambda: gaussian_phase_pair_coherence(-1), "nonnegative"),
        (lambda: population_activation_scale(0, 1, 0), "population"),
        (lambda: continuous_population_threshold(1, -1, 0), "scale"),
        (lambda: activated_relative_response(0, 1), "barrier"),
        (lambda: brownian_phase_characteristic(-1, 1), "nonnegative"),
        (lambda: brownian_phase_characteristic(1, -1), "nonnegative"),
        (lambda: brownian_phase_characteristic(1, 1, sp.Rational(1, 2)), "integer"),
        (lambda: brownian_mean_phasor_window_average(1, 0), "positive"),
        (lambda: damped_brownian_coherent_mean_factor(-1, 1, 1), "nonnegative"),
    ],
)
def test_exact_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
