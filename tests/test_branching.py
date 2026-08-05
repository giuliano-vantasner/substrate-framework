import pytest
import sympy as sp

import substrate_framework as framework
from substrate_framework.branching import (
    PopulationDependentWeightLedger,
    channel_odds,
    population_dependent_weight_ledger,
    relative_weighted_odds_enhancement,
    two_channel_allocation,
    weighted_channel_allocation,
)


def test_two_positive_channels_partition_exactly() -> None:
    first, second = sp.symbols("A B", positive=True)
    result = two_channel_allocation(first, second)
    assert result.total_rate == first + second
    assert result.first_fraction == first / (first + second)
    assert result.second_fraction == second / (first + second)
    assert sp.simplify(result.first_fraction + result.second_fraction) == 1


def test_zero_endpoints_are_retained_but_double_zero_is_rejected() -> None:
    assert two_channel_allocation(0, 3).first_fraction == 0
    assert two_channel_allocation(0, 3).second_fraction == 1
    assert two_channel_allocation(5, 0).first_fraction == 1
    assert two_channel_allocation(5, 0).second_fraction == 0
    with pytest.raises(ValueError, match="explicitly positive"):
        two_channel_allocation(0, 0)


def test_exact_derivatives_and_limits_fix_the_monotone_allocation() -> None:
    first, second = sp.symbols("A B", positive=True)
    fraction = two_channel_allocation(first, second).first_fraction
    assert sp.simplify(sp.diff(fraction, first) - second / (first + second) ** 2) == 0
    assert sp.simplify(sp.diff(fraction, second) + first / (first + second) ** 2) == 0
    assert sp.limit(fraction, first, 0, dir="+") == 0
    assert sp.limit(fraction, first, sp.oo) == 1


def test_common_scaling_cancels_and_relative_scaling_does_not() -> None:
    first, second, scale = sp.symbols("A B s", positive=True)
    original = two_channel_allocation(first, second).first_fraction
    common = two_channel_allocation(scale * first, scale * second).first_fraction
    relative = two_channel_allocation(scale * first, second).first_fraction
    assert sp.simplify(common - original) == 0
    assert sp.simplify(relative - original) != 0


def test_channel_odds_requires_a_positive_denominator() -> None:
    first, second = sp.symbols("A B", positive=True)
    assert channel_odds(first, second) == first / second
    assert channel_odds(0, second) == 0
    with pytest.raises(ValueError, match="denominator_rate"):
        channel_odds(first, 0)


def test_weighted_specialization_reproduces_the_conditional_source_algebra() -> None:
    soft, gamma, weight = sp.symbols("r_s r_gamma w", positive=True)
    population = sp.symbols("N", positive=True, integer=True)
    result = weighted_channel_allocation(soft, gamma, weight, population)
    rho = gamma / soft
    assert result.weighted_rate == soft * weight * population
    assert result.baseline_ratio == rho
    assert sp.simplify(result.weighted_fraction - weight * population / (weight * population + rho)) == 0
    assert sp.simplify(result.comparison_fraction - rho / (weight * population + rho)) == 0
    assert sp.simplify(result.weighted_fraction + result.comparison_fraction) == 1


def test_weighted_comparison_fraction_decreases_with_population() -> None:
    rho, weight, population = sp.symbols("rho w N", positive=True)
    hard_fraction = rho / (weight * population + rho)
    assert sp.diff(hard_fraction, population) == -rho * weight / (weight * population + rho) ** 2


def test_relative_enhancement_keeps_weight_and_population_free() -> None:
    weight, baseline = sp.symbols("w w1", positive=True)
    population = sp.symbols("N", positive=True, integer=True)
    enhancement = relative_weighted_odds_enhancement(weight, population, baseline)
    assert enhancement == weight * population / baseline
    assert relative_weighted_odds_enhancement(baseline, 1, baseline) == 1
    assert enhancement.free_symbols == {weight, population, baseline}


@pytest.mark.parametrize(
    "call",
    [
        lambda: two_channel_allocation(-1, 2),
        lambda: two_channel_allocation(1.0, 2),
        lambda: weighted_channel_allocation(1, 1, 0, 1),
        lambda: weighted_channel_allocation(1, 1, 1, 0),
        lambda: weighted_channel_allocation(1, 1, 1, sp.Rational(3, 2)),
        lambda: relative_weighted_odds_enhancement(1, 1, 0),
    ],
)
def test_invalid_domains_are_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()


def test_branching_api_is_exported_without_a_physical_rate_claim() -> None:
    assert framework.two_channel_allocation is two_channel_allocation
    assert framework.weighted_channel_allocation is weighted_channel_allocation
    assert framework.relative_weighted_odds_enhancement is relative_weighted_odds_enhancement
    assert "does not derive physical states" in framework.branching.__doc__


def test_population_dependent_derivative_is_exact() -> None:
    population, rho, weight, slope = sp.symbols("N rho w s", positive=True)
    result = population_dependent_weight_ledger(population, rho, weight, slope)
    expected = -rho * (weight + population * slope) / (
        population * weight + rho
    ) ** 2
    assert sp.simplify(result.comparison_fraction_derivative - expected) == 0
    assert result.monotonicity == "decreasing"


def test_constant_positive_weight_recovers_C_BRN_001() -> None:
    population, rho, weight = sp.symbols("N rho w", positive=True)
    result = population_dependent_weight_ledger(population, rho, weight, 0)
    assert result.derivative_control == weight
    assert result.comparison_fraction_derivative == -rho * weight / (
        population * weight + rho
    ) ** 2


def test_positive_decreasing_weights_cover_all_three_signs() -> None:
    population = sp.symbols("N", positive=True)
    decreasing = population_dependent_weight_ledger(
        population, 2, 1 / sp.sqrt(population), -1 / (2 * population ** sp.Rational(3, 2))
    )
    stationary = population_dependent_weight_ledger(
        population, 2, 1 / population, -1 / population**2
    )
    increasing = population_dependent_weight_ledger(
        population, 2, 1 / population**2, -2 / population**3
    )
    assert decreasing.monotonicity == "decreasing"
    assert stationary.monotonicity == "stationary"
    assert increasing.monotonicity == "increasing"


def test_positive_weight_alone_is_not_a_monotonicity_oracle() -> None:
    population = sp.symbols("N", positive=True)
    result = population_dependent_weight_ledger(
        population, 1, 1 / population**2, -2 / population**3
    )
    assert result.weight.is_positive
    assert result.comparison_fraction_derivative.is_positive


def test_undecidable_control_sign_is_rejected() -> None:
    slope = sp.symbols("s", real=True)
    with pytest.raises(ValueError, match="decidable sign"):
        population_dependent_weight_ledger(2, 3, 5, slope)


def test_population_dependent_ledger_preserves_physical_ceilings() -> None:
    result = population_dependent_weight_ledger(2, 3, 5, -1)
    assert isinstance(result, PopulationDependentWeightLedger)
    assert result.physical_weight_law_is_separate_premise
    assert result.exhaustive_channel_interpretation_is_separate_premise
    text = " ".join(population_dependent_weight_ledger.__doc__.split())
    assert "positive weight alone does not determine monotonicity" in text
