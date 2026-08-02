from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.normalized_overlaps import (
    conditional_overlap_mass_ledger,
    matched_width_sech_overlap,
    normalized_expectation_bounds,
    overlap_mass_ratio,
    quartic_bound_mode_overlap_ledger,
    reciprocal_overlap_scale_rescaling,
    sech_power_integral,
)


def test_sech_power_integral_reproduces_exact_standard_values() -> None:
    kappa = sp.symbols("kappa", positive=True)
    assert sp.simplify(sech_power_integral(1, kappa) - sp.pi / kappa) == 0
    assert sp.simplify(sech_power_integral(2, kappa) - 2 / kappa) == 0
    assert sp.simplify(sech_power_integral(4, kappa) - 4 / (3 * kappa)) == 0
    assert sp.simplify(sech_power_integral(5, kappa) - 3 * sp.pi / (8 * kappa)) == 0


@pytest.mark.parametrize(
    ("power", "expected"),
    [
        (1, sp.pi / 4),
        (2, 9 * sp.pi / 32),
        (3, 75 * sp.pi / 256),
    ],
)
def test_source_sampled_sech_overlaps_are_normalized_exactly(power, expected) -> None:
    amplitude, kappa = sp.symbols("A kappa", positive=True)
    result = matched_width_sech_overlap(power, 1, amplitude, kappa)
    assert sp.simplify(result.normalized_overlap - amplitude * expected) == 0


def test_general_matched_width_overlap_is_a_gamma_ratio() -> None:
    p, r, amplitude, kappa = sp.symbols("p r A kappa", positive=True)
    result = matched_width_sech_overlap(p, r, amplitude, kappa)
    expected = amplitude * sp.gamma(p + r / 2) * sp.gamma(p + sp.Rational(1, 2)) / (
        sp.gamma(p) * sp.gamma(p + r / 2 + sp.Rational(1, 2))
    )
    assert sp.simplify(result.normalized_overlap - expected) == 0
    assert sp.simplify(sp.diff(result.normalized_overlap, kappa)) == 0


def test_general_overlap_retains_amplitude_sign() -> None:
    positive = matched_width_sech_overlap(2, 1, 3, 2).normalized_overlap
    negative = matched_width_sech_overlap(2, 1, -3, 2).normalized_overlap
    assert positive > 0
    assert negative < 0
    assert positive == -negative


def test_normalized_expectation_bounds_preserve_supplied_profile_range() -> None:
    lower, upper = normalized_expectation_bounds(0, 3)
    overlap = matched_width_sech_overlap(2, 1, 3, 1).normalized_overlap
    assert lower == 0 and upper == 3
    assert bool(lower < overlap < upper)
    assert normalized_expectation_bounds(-3, 0) == (-3, 0)


def test_quartic_even_and_actual_odd_mode_overlaps_are_distinct() -> None:
    amplitude, kappa = sp.symbols("A kappa", positive=True)
    result = quartic_bound_mode_overlap_ledger(amplitude, kappa)
    assert sp.simplify(result.even_mode_norm - 4 / (3 * kappa)) == 0
    assert sp.simplify(result.odd_mode_norm - 2 / (3 * kappa)) == 0
    assert result.even_overlap == 9 * sp.pi * amplitude / 32
    assert result.odd_overlap == 3 * sp.pi * amplitude / 16
    assert result.weighted_cross_overlap == 0


def test_actual_odd_mode_overlap_matches_direct_whole_line_integration() -> None:
    x = sp.symbols("x", real=True)
    norm = sp.integrate(1 / sp.cosh(x) ** 2, (x, -sp.oo, sp.oo)) - sp.integrate(
        1 / sp.cosh(x) ** 4, (x, -sp.oo, sp.oo)
    )
    raw = sp.integrate(1 / sp.cosh(x) ** 3, (x, -sp.oo, sp.oo)) - sp.integrate(
        1 / sp.cosh(x) ** 5, (x, -sp.oo, sp.oo)
    )
    result = quartic_bound_mode_overlap_ledger(1, 1)
    assert norm == sp.Rational(2, 3)
    assert raw == sp.pi / 8
    assert sp.simplify(raw / norm - result.odd_overlap) == 0


def test_even_multiplier_makes_even_odd_weighted_cross_term_zero() -> None:
    x = sp.symbols("x", real=True)
    integrand = sp.sech(x) ** 4 * sp.tanh(x)
    assert sp.integrate(integrand, (x, -sp.oo, sp.oo)) == 0


def test_conditional_mass_ledger_keeps_dimensions_and_free_scale_explicit() -> None:
    overlap, scale = sp.symbols("y v", real=True)
    ledger = conditional_overlap_mass_ledger(
        overlap,
        scale,
        profile_mass_dimension=sp.Rational(1, 2),
        scale_mass_dimension=sp.Rational(1, 2),
    )
    assert ledger.mapped_mass == overlap * scale
    assert ledger.profile_mass_dimension == sp.Rational(1, 2)
    assert ledger.scale_mass_dimension == sp.Rational(1, 2)
    assert ledger.mapped_mass_dimension == 1


def test_common_mass_scale_cancels_but_profile_amplitudes_need_not() -> None:
    a0, a1, scale = sp.symbols("A0 A1 v", positive=True)
    y0 = matched_width_sech_overlap(2, 1, a0, 1).normalized_overlap
    y1 = quartic_bound_mode_overlap_ledger(a1, 1).odd_overlap
    mass_ratio = sp.simplify((y1 * scale) / (y0 * scale))
    assert mass_ratio == overlap_mass_ratio(y1, y0)
    assert mass_ratio == 2 * a1 / (3 * a0)
    assert mass_ratio.has(a0, a1) and not mass_ratio.has(scale)


def test_reciprocal_overlap_scale_rescaling_leaves_product_unidentified() -> None:
    overlap, scale, rho = sp.symbols("y v rho", nonzero=True, real=True)
    changed_overlap, changed_scale, invariant = reciprocal_overlap_scale_rescaling(
        overlap, scale, rho
    )
    assert changed_overlap == overlap * rho
    assert changed_scale == scale / rho
    assert sp.simplify(changed_overlap * changed_scale - invariant) == 0
    assert invariant == overlap * scale


def test_canonical_overlap_module_uses_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/normalized_overlaps.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: sech_power_integral(0, 1), "positive"),
        (lambda: sech_power_integral(1, 0), "positive"),
        (lambda: matched_width_sech_overlap(1, 0, 1, 1), "positive"),
        (lambda: matched_width_sech_overlap(1, 1, sp.I, 1), "real"),
        (lambda: normalized_expectation_bounds(2, 1), "must not exceed"),
        (lambda: overlap_mass_ratio(1, 0), "nonzero"),
        (lambda: reciprocal_overlap_scale_rescaling(1, 1, 0), "nonzero"),
    ],
)
def test_normalized_overlap_api_rejects_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
