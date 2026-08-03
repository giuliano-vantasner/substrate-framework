import pytest
import sympy as sp

from substrate_framework.crossovers import (
    exponential_crossover_energy,
    exponential_crossover_ledger,
    exponential_saturation,
    monotone_range_location,
    shifted_barrier_crossover_energy,
    shifted_barrier_crossover_ledger,
    shifted_barrier_crossover_residual,
    shifted_barrier_zero_energy_floor,
)


def test_monotone_range_classifies_every_level_region():
    assert monotone_range_location(0, 1, -1) == "below_range"
    assert monotone_range_location(0, 1, 0) == "lower_endpoint"
    assert monotone_range_location(0, 1, sp.Rational(1, 2)) == "unique_interior"
    assert monotone_range_location(0, 1, 1) == "upper_limit_only"
    assert monotone_range_location(0, 1, 2) == "above_range"


def test_exponential_inverse_residual_is_exact():
    scale = sp.symbols("E0", positive=True)
    level = sp.Rational(3, 7)
    crossing = exponential_crossover_energy(scale, level)
    assert sp.simplify(exponential_saturation(crossing, scale) - level) == 0


def test_exponential_endpoint_and_log_two_example():
    assert exponential_crossover_energy(3, 0) == 0
    assert exponential_crossover_energy(1, sp.Rational(1, 2)) == sp.log(2)


def test_exponential_sensitivities_and_convexity_are_exact():
    scale = sp.symbols("E0", positive=True)
    level = sp.Rational(2, 5)
    ledger = exponential_crossover_ledger(scale, level)
    assert ledger.level_derivative == sp.Rational(5, 3) * scale
    assert sp.simplify(
        ledger.scale_derivative + sp.log(sp.Rational(3, 5))
    ) == 0
    assert ledger.level_second_derivative == sp.Rational(25, 9) * scale


def test_exponential_common_energy_scaling_is_covariant():
    scale, rho = sp.symbols("E0 rho", positive=True)
    level = sp.Rational(1, 3)
    assert sp.simplify(
        exponential_crossover_energy(rho * scale, level)
        - rho * exponential_crossover_energy(scale, level)
    ) == 0


def test_shifted_floor_distinguishes_positive_and_zero_shift():
    assert shifted_barrier_zero_energy_floor(8, 2) == sp.exp(-2)
    assert shifted_barrier_zero_energy_floor(8, 0) == 0


def test_shifted_crossover_residual_is_exact_for_interior_level():
    barrier = sp.symbols("G", positive=True)
    shift = barrier
    level = sp.exp(-sp.Rational(1, 2))
    crossing = shifted_barrier_crossover_energy(barrier, shift, level)
    assert crossing == 3 * barrier
    assert shifted_barrier_crossover_residual(barrier, shift, level) == 0


def test_shifted_crossover_sensitivities_are_exact():
    ledger = shifted_barrier_crossover_ledger(8, 1, sp.exp(-2))
    assert ledger.crossover_energy == 1
    assert ledger.barrier_derivative == sp.Rational(1, 4)
    assert ledger.shift_derivative == -1
    assert sp.simplify(ledger.level_derivative - 2 * sp.exp(2)) == 0


def test_shifted_common_energy_scaling_is_covariant():
    barrier, shift, rho = sp.symbols("G U rho", positive=True)
    level = sp.exp(-sp.Rational(2, 3))
    assert sp.simplify(
        shifted_barrier_crossover_energy(rho * barrier, rho * shift, level)
        - rho * shifted_barrier_crossover_energy(barrier, shift, level)
    ) == 0


@pytest.mark.parametrize("level", [-1, 1, 2, 0.5])
def test_exponential_level_guards(level):
    with pytest.raises(ValueError):
        exponential_crossover_energy(1, level)


def test_shifted_level_must_exceed_the_floor():
    with pytest.raises(ValueError, match="exceed"):
        shifted_barrier_crossover_energy(8, 2, sp.exp(-3))


def test_exact_input_guards_reject_floats_and_bad_ranges():
    with pytest.raises(ValueError, match="exact"):
        exponential_saturation(1.0, 2)
    with pytest.raises(ValueError, match="below"):
        monotone_range_location(1, 0, sp.Rational(1, 2))
    with pytest.raises(ValueError, match="numeric"):
        monotone_range_location(0, 1, sp.symbols("c", real=True))
