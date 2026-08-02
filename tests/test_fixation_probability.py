from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.fixation_probability import (
    continuous_exponential_fixation_probability,
    exponential_fixation_ledger,
    two_intensity_selection_ledger,
)


def test_continuous_probability_defines_the_neutral_point_exactly() -> None:
    x = sp.symbols("x", real=True)
    assert continuous_exponential_fixation_probability(x, 0) == x
    selection = sp.symbols("S", real=True)
    probability = continuous_exponential_fixation_probability(x, selection)
    assert probability.subs(selection, 0) == x


def test_nonzero_branch_has_absorbing_boundaries_and_exact_bvp_residual() -> None:
    x = sp.symbols("x", real=True)
    selection = sp.symbols("S", real=True, nonzero=True)
    ledger = exponential_fixation_ledger(x, selection)
    assert ledger.boundary_at_zero == 0
    assert ledger.boundary_at_one == 1
    assert ledger.bvp_residual == 0
    assert ledger.bvp_boundary_determinant == sp.exp(-selection) - 1
    assert ledger.bvp_boundary_determinant != 0
    assert ledger.neutral_limit == x


def test_boundary_value_constants_reconstruct_the_probability() -> None:
    x = sp.symbols("x", real=True)
    selection = sp.symbols("S", real=True, nonzero=True)
    ledger = exponential_fixation_ledger(x, selection)
    reconstructed = sp.simplify(
        ledger.bvp_constant_offset
        + ledger.bvp_exponential_coefficient * sp.exp(-selection * x)
    )
    assert sp.simplify(reconstructed - ledger.probability) == 0
    assert ledger.bvp_boundary_matrix.det() == ledger.bvp_boundary_determinant


def test_generator_coefficient_mutation_breaks_the_bvp_residual() -> None:
    x = sp.symbols("x", real=True)
    selection = sp.symbols("S", real=True, nonzero=True)
    ledger = exponential_fixation_ledger(x, selection)
    wrong_residual = sp.simplify(
        sp.diff(ledger.probability, x, 2)
        + 2 * selection * sp.diff(ledger.probability, x)
    )
    assert ledger.bvp_residual == 0
    assert wrong_residual != 0


def test_complement_symmetry_and_frequency_monotonicity_are_exact() -> None:
    x = sp.symbols("x", real=True)
    selection = sp.symbols("S", real=True, nonzero=True)
    ledger = exponential_fixation_ledger(x, selection)
    assert ledger.complement_symmetry_residual == 0
    assert sp.simplify(
        ledger.frequency_derivative
        - selection * sp.exp(-selection * x) / (1 - sp.exp(-selection))
    ) == 0


def test_selection_derivative_is_factored_by_the_strict_convexity_gap() -> None:
    x = sp.symbols("x", real=True)
    selection = sp.symbols("S", real=True, nonzero=True)
    ledger = exponential_fixation_ledger(x, selection)
    assert ledger.selection_derivative_factorization_residual == 0
    assert ledger.selection_derivative_convexity_gap == sp.simplify(
        (1 - x) + x * sp.exp(selection) - sp.exp(selection * x)
    )


def test_small_selection_series_exposes_bias_and_first_correction() -> None:
    x = sp.symbols("x", real=True)
    selection = sp.symbols("S", real=True, nonzero=True)
    ledger = exponential_fixation_ledger(x, selection)
    expected = sp.simplify(
        x
        + selection * x * (1 - x) / 2
        + selection**2 * x * (1 - x) * (1 - 2 * x) / 12
        - selection**3 * x**2 * (1 - x) ** 2 / 24
    )
    assert sp.simplify(
        ledger.small_selection_series_through_cubic - expected
    ) == 0


def test_positive_and_negative_selection_bias_opposite_directions() -> None:
    x = sp.Rational(2, 5)
    positive = continuous_exponential_fixation_probability(x, 3)
    negative = continuous_exponential_fixation_probability(x, -3)
    assert 0 < negative < x < positive < 1
    assert sp.simplify(
        positive
        + continuous_exponential_fixation_probability(1 - x, -3)
        - 1
    ) == 0


def test_interior_frequency_spans_open_probability_interval_with_selection() -> None:
    x = sp.Rational(2, 5)
    selection = sp.symbols("S", real=True)
    branch = (1 - sp.exp(-selection * x)) / (1 - sp.exp(-selection))
    assert sp.limit(branch, selection, -sp.oo) == 0
    assert sp.limit(branch, selection, sp.oo) == 1


def test_intensity_parameterization_separates_total_and_frequency() -> None:
    first, second, coefficient, scale = sp.symbols(
        "I1 I2 kappa lambda", positive=True
    )
    ledger = two_intensity_selection_ledger(
        first, second, coefficient, scale
    )
    assert ledger.initial_frequency == first / (first + second)
    assert ledger.normalized_contrast == (first - second) / (first + second)
    assert sp.simplify(
        ledger.normalized_contrast - (2 * ledger.initial_frequency - 1)
    ) == 0
    assert ledger.raw_contrast == first - second
    assert sp.simplify(
        ledger.raw_contrast
        - ledger.total_intensity * ledger.normalized_contrast
    ) == 0


def test_common_amplitude_rescaling_changes_fixed_coefficient_coordinate() -> None:
    first, second, coefficient, scale = sp.symbols(
        "I1 I2 kappa lambda", positive=True
    )
    ledger = two_intensity_selection_ledger(
        first, second, coefficient, scale
    )
    assert ledger.scaled_initial_frequency == ledger.initial_frequency
    assert ledger.scaled_raw_contrast == scale**2 * ledger.raw_contrast
    assert (
        ledger.fixed_coefficient_scaled_selection
        == scale**2 * ledger.selection_ratio
    )


def test_compensating_coefficient_and_unit_normalization_preserve_selection() -> None:
    first, second, coefficient, scale = sp.symbols(
        "I1 I2 kappa lambda", positive=True
    )
    ledger = two_intensity_selection_ledger(
        first, second, coefficient, scale
    )
    assert ledger.covariant_scaled_coefficient == coefficient / scale**2
    assert ledger.covariant_scaled_selection == ledger.selection_ratio
    assert sp.simplify(
        ledger.unit_normalized_first_intensity
        + ledger.unit_normalized_second_intensity
        - 1
    ) == 0
    assert ledger.unit_normalized_selection == ledger.selection_ratio


def test_as8_example_uses_different_unnormalized_totals() -> None:
    first = two_intensity_selection_ledger(4, 1, 1, 5)
    second = two_intensity_selection_ledger(100, 25, 1, 1)
    assert first.initial_frequency == second.initial_frequency == sp.Rational(4, 5)
    assert first.total_intensity == 5
    assert second.total_intensity == 125
    assert second.selection_ratio == 25 * first.selection_ratio
    assert first.unit_normalized_contrast == second.unit_normalized_contrast


@pytest.mark.parametrize(
    "call",
    [
        lambda: continuous_exponential_fixation_probability(-1, 1),
        lambda: continuous_exponential_fixation_probability(2, 1),
        lambda: continuous_exponential_fixation_probability(sp.Rational(1, 2), 1.0),
        lambda: exponential_fixation_ledger(sp.Rational(1, 2), 0),
        lambda: two_intensity_selection_ledger(0, 1, 1, 1),
        lambda: two_intensity_selection_ledger(1, 1, sp.I, 1),
        lambda: two_intensity_selection_ledger(1, 1, 1, 0),
    ],
)
def test_fixation_ledgers_reject_invalid_or_inexact_inputs(call) -> None:
    with pytest.raises(ValueError):
        call()


def test_fixation_module_uses_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/fixation_probability.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source
