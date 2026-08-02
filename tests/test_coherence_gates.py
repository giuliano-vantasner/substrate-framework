from __future__ import annotations

import pytest
import sympy as sp
import substrate_framework as framework

from substrate_framework.coherence_gates import (
    activated_relative_response,
    continuous_population_threshold,
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
    ],
)
def test_exact_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
