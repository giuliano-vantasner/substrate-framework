from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import sympy as sp
from scipy.integrate import quad

from substrate_framework.normalized_overlaps import matched_width_sech_overlap
from substrate_framework.translated_localization import (
    normalized_gaussian_overlap,
    poschl_teller_ground_ledger,
    poschl_teller_ground_state,
    poschl_teller_operator,
    poschl_sech_overlap_tail_ledger,
    reciprocal_rate_spacing_rescaling,
    sech_convolution,
    sech_overlap_tail_ledger,
    tail_spacing_ledger,
    translated_sech_overlap,
)


@pytest.mark.parametrize(
    ("alpha", "beta", "offset"),
    [(2.0, 1.0, 1.0), (1.0, 2.0, 2.0), (2.0, 2.0, 3.0)],
)
def test_exact_sech_convolution_matches_independent_quad(
    alpha: float, beta: float, offset: float
) -> None:
    exact = float(sp.N(sech_convolution(alpha, beta, offset), 16))
    numeric, error = quad(
        lambda z: 1.0 / np.cosh(z - offset) ** alpha / np.cosh(z) ** beta,
        -40.0,
        40.0,
        epsabs=1.0e-12,
        epsrel=1.0e-12,
        limit=300,
    )
    assert error < 1.0e-10
    assert numeric == pytest.approx(exact, rel=2.0e-11, abs=2.0e-12)


def test_sech_convolution_is_reflection_symmetric() -> None:
    positive = sech_convolution(3, sp.Rational(3, 2), sp.Rational(7, 5))
    negative = sech_convolution(3, sp.Rational(3, 2), -sp.Rational(7, 5))
    assert positive == negative


@pytest.mark.parametrize("mode_power", [1, 2, sp.Rational(3, 2)])
def test_zero_displacement_reproduces_same_center_api(mode_power: sp.Expr) -> None:
    translated = translated_sech_overlap(mode_power, 1, 3, 2, 0)
    same_center = matched_width_sech_overlap(mode_power, 1, 3, 2)
    assert sp.simplify(translated.normalized_overlap - same_center.normalized_overlap) == 0


def test_physical_displacement_enters_only_through_kappa_times_distance() -> None:
    first = translated_sech_overlap(1, 1, 2, 3, 4).normalized_overlap
    second = translated_sech_overlap(1, 1, 2, 6, 2).normalized_overlap
    assert sp.simplify(first - second) == 0


def test_positive_profile_overlap_respects_expectation_bound() -> None:
    overlap = float(sp.N(translated_sech_overlap(1, 1, 5, 1, 2).normalized_overlap))
    assert 0.0 < overlap < 5.0


def test_slower_profile_tail_sets_source_like_asymptotic_rate() -> None:
    ledger = sech_overlap_tail_ledger(1, 1, 1, 2)
    assert ledger.mode_density_power == 2
    assert ledger.dimensionless_decay_power == 1
    assert ledger.physical_decay_rate == 2
    assert ledger.polynomial_prefactor_power == 0
    for offset in (8, 10, 12):
        overlap = translated_sech_overlap(1, 1, 1, 2, offset).normalized_overlap
        scaled = float(sp.N(overlap * sp.exp(2 * offset), 16))
        expected = float(sp.N(ledger.normalized_leading_coefficient, 16))
        assert scaled == pytest.approx(expected, rel=2.0e-6)


def test_slower_mode_density_tail_changes_the_asymptotic_rate() -> None:
    ledger = sech_overlap_tail_ledger(sp.Rational(1, 2), 2, 1, 1)
    assert ledger.mode_density_power == 1
    assert ledger.dimensionless_decay_power == 1
    assert ledger.physical_decay_rate == 1
    assert ledger.polynomial_prefactor_power == 0


def test_equal_tail_rates_require_linear_displacement_prefactor() -> None:
    ledger = sech_overlap_tail_ledger(1, 2, 1, 1)
    assert ledger.dimensionless_decay_power == 2
    assert ledger.polynomial_prefactor_power == 1
    assert ledger.normalized_leading_coefficient == 8
    scaled_with_resonance = []
    for offset in (sp.Integer(12), sp.Integer(24)):
        overlap = translated_sech_overlap(1, 2, 1, 1, offset).normalized_overlap
        scaled_with_resonance.append(
            float(sp.N(overlap, 50) * sp.N(sp.exp(2 * offset), 50) / offset)
        )
    assert 0.0 < 8.0 - scaled_with_resonance[1] < 8.0 - scaled_with_resonance[0]
    assert scaled_with_resonance[1] == pytest.approx(8.0, rel=4.2e-2)
    pure_exponential_scaling = scaled_with_resonance[0] * 12
    assert pure_exponential_scaling > 80.0


def test_poschl_teller_ground_ledger_is_center_independent() -> None:
    origin = poschl_teller_ground_ledger(2, 1, 0)
    shifted = poschl_teller_ground_ledger(2, 1, 7)
    assert origin.index == shifted.index == 1
    assert origin.eigenvalue == shifted.eigenvalue == -1
    assert origin.normalization == shifted.normalization == sp.sqrt(2) / 2
    assert origin.density_tail_rate == shifted.density_tail_rate == 2
    assert shifted.center == 7


def test_poschl_teller_exact_ground_state_satisfies_shifted_operator() -> None:
    x = sp.symbols("x", real=True)
    mode = poschl_teller_ground_state(x, 2, 1, 3)
    applied = poschl_teller_operator(mode, x, 2, 1, 3)
    assert sp.simplify((applied + mode).rewrite(sp.exp)) == 0


def test_poschl_teller_ground_state_is_l2_normalized() -> None:
    ledger = poschl_teller_ground_ledger(2, 1, 0)
    unnormalized_norm = sp.sqrt(sp.pi) * sp.gamma(ledger.index) / sp.gamma(
        ledger.index + sp.Rational(1, 2)
    )
    assert sp.simplify(ledger.normalization**2 * unnormalized_norm - 1) == 0


def test_mh2_declared_well_has_faster_density_tail_than_core() -> None:
    well = poschl_teller_ground_ledger(12, sp.Rational(7, 10), 0)
    kappa = sp.sqrt(sp.Rational(1, 2) - sp.Rational(45, 100) ** 2)
    ladder = tail_spacing_ledger(well.density_tail_rate, kappa, 4)
    assert float(well.density_tail_rate) > float(kappa)
    assert ladder.overlap_tail_rate == kappa
    assert float(ladder.asymptotic_log_ratio) == pytest.approx(-2.181742423, rel=2e-10)
    assert ladder.resonant_equal_rates is False


def test_poschl_sech_tail_ledger_classifies_all_rate_regimes() -> None:
    profile_slow = poschl_sech_overlap_tail_ledger(2, 1, 3, 1)
    mode_slow = poschl_sech_overlap_tail_ledger(sp.Rational(1, 8), 4, 3, 1)
    equal = poschl_sech_overlap_tail_ledger(sp.Rational(1, 2), 2, 3, 1)
    assert profile_slow.ground.density_tail_rate == 2
    assert profile_slow.overlap_tail_rate == 1
    assert profile_slow.polynomial_prefactor_power == 0
    assert mode_slow.ground.density_tail_rate == sp.Rational(1, 2)
    assert mode_slow.overlap_tail_rate == sp.Rational(1, 2)
    assert mode_slow.polynomial_prefactor_power == 0
    assert equal.ground.density_tail_rate == 1
    assert equal.overlap_tail_rate == 1
    assert equal.polynomial_prefactor_power == 1
    assert all(
        float(item.leading_coefficient) > 0.0
        for item in (profile_slow, mode_slow, equal)
    )


def test_tail_spacing_product_has_a_reciprocal_free_direction() -> None:
    rate, spacing, invariant = reciprocal_rate_spacing_rescaling(2, 3, 5)
    assert rate == 10
    assert spacing == sp.Rational(3, 5)
    assert invariant == 6
    assert rate * spacing == invariant


def test_gaussian_localization_is_an_exact_nongeometric_countermodel() -> None:
    a = 2.0
    b = 3.0
    amplitude = 5.0
    offset = 1.7
    exact = float(normalized_gaussian_overlap(a, b, amplitude, offset))
    numeric, error = quad(
        lambda x: np.sqrt(a / np.pi)
        * np.exp(-a * (x - offset) ** 2)
        * amplitude
        * np.exp(-b * x**2),
        -12.0,
        12.0,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
    )
    assert error < 1.0e-11
    assert numeric == pytest.approx(exact, rel=1.0e-12)
    overlaps = [
        float(normalized_gaussian_overlap(a, b, amplitude, n)) for n in range(4)
    ]
    log_ratios = np.diff(np.log(overlaps))
    assert not np.allclose(log_ratios[1:], log_ratios[1])
    assert np.diff(log_ratios) == pytest.approx([-2.4, -2.4], rel=1.0e-12)


def test_translated_localization_module_has_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/translated_localization.py").read_text(
        encoding="utf-8"
    )
    assert "np.trapz" not in source
    assert "np.trapezoid" not in source


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: sech_convolution(0, 1, 0), "positive"),
        (lambda: translated_sech_overlap(1, 1, sp.I, 1, 0), "real"),
        (lambda: translated_sech_overlap(1, 1, 1, 0, 0), "positive"),
        (lambda: poschl_teller_ground_ledger(-1, 1), "positive"),
        (lambda: tail_spacing_ledger(1, 0, 1), "positive"),
        (lambda: reciprocal_rate_spacing_rescaling(1, 1, -1), "positive"),
        (lambda: normalized_gaussian_overlap(1, -1, 1, 0), "positive"),
    ],
)
def test_translated_localization_api_rejects_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
