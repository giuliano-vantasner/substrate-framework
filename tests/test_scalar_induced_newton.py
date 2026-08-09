import inspect

import pytest
import sympy as sp

import substrate_framework as framework
from substrate_framework.induced_gravity import induced_inverse_newton_ledger
from substrate_framework.scalar_induced_newton import (
    FOUR_DIMENSIONAL_CONFORMAL_COUPLING,
    SHARP_PROPER_TIME_REGULATOR,
    leading_scalar_newton_shift_coefficient,
    scalar_heat_kernel_a2,
)


def test_scalar_induced_newton_api_is_exported_from_package() -> None:
    assert (
        framework.leading_scalar_newton_shift_coefficient
        is leading_scalar_newton_shift_coefficient
    )
    assert framework.scalar_heat_kernel_a2 is scalar_heat_kernel_a2
    assert (
        framework.FOUR_DIMENSIONAL_CONFORMAL_COUPLING
        == FOUR_DIMENSIONAL_CONFORMAL_COUPLING
    )
    assert framework.SHARP_PROPER_TIME_REGULATOR == SHARP_PROPER_TIME_REGULATOR


def test_scalar_a2_follows_the_declared_laplace_operator_convention() -> None:
    mass_squared = sp.Symbol("m2", nonnegative=True)
    generic = scalar_heat_kernel_a2(sp.Rational(1, 12), mass_squared)
    assert generic.curvature_weight == sp.Rational(1, 12)
    assert generic.mass_weight == -mass_squared
    assert generic.conformal_zero is False

    conformal = scalar_heat_kernel_a2(FOUR_DIMENSIONAL_CONFORMAL_COUPLING)
    assert conformal.curvature_weight == 0
    assert conformal.conformal_zero is True

    unknown = scalar_heat_kernel_a2(sp.Symbol("xi", real=True))
    assert unknown.conformal_zero is None


def test_sharp_proper_time_normalization_is_independently_reconstructed() -> None:
    result = leading_scalar_newton_shift_coefficient(
        1,
        0,
        regulator=SHARP_PROPER_TIME_REGULATOR,
    )
    fresh_scheme_factor = sp.simplify(
        16 * sp.pi * sp.Rational(1, 2) * (4 * sp.pi) ** -2
    )
    proper_time, cutoff = sp.symbols("tau Lambda", positive=True)
    leading_integral = sp.integrate(
        proper_time**-2,
        (proper_time, cutoff**-2, sp.oo),
    )
    assert leading_integral == cutoff**2
    assert fresh_scheme_factor == sp.Rational(1, 2) / sp.pi
    assert result.scheme_factor == fresh_scheme_factor
    assert result.coefficient == 1 / (12 * sp.pi)
    assert result.coefficient_per_field == 1 / (12 * sp.pi)

    wrong_complex_scalar_weight = sp.simplify(
        16 * sp.pi * 1 * (4 * sp.pi) ** -2
    )
    wrong_heat_kernel_power = sp.simplify(
        16 * sp.pi * sp.Rational(1, 2) * (4 * sp.pi) ** -1
    )
    assert wrong_complex_scalar_weight != result.scheme_factor
    assert wrong_heat_kernel_power != result.scheme_factor


def test_leading_shift_is_exact_and_linear_in_real_scalar_count() -> None:
    one = leading_scalar_newton_shift_coefficient(
        1,
        sp.Rational(1, 12),
        regulator=SHARP_PROPER_TIME_REGULATOR,
    )
    seven = leading_scalar_newton_shift_coefficient(
        7,
        sp.Rational(1, 12),
        regulator=SHARP_PROPER_TIME_REGULATOR,
    )
    expected = (1 - 6 * sp.Rational(1, 12)) / (12 * sp.pi)
    assert sp.simplify(one.coefficient - expected) == 0
    assert sp.simplify(seven.coefficient - 7 * one.coefficient) == 0


def test_regulator_must_be_named_and_unknown_schemes_do_not_default() -> None:
    signature = inspect.signature(leading_scalar_newton_shift_coefficient)
    assert signature.parameters["regulator"].default is inspect.Parameter.empty
    with pytest.raises(TypeError, match="regulator"):
        leading_scalar_newton_shift_coefficient(1, 0)
    with pytest.raises(ValueError, match="unknown regulator"):
        leading_scalar_newton_shift_coefficient(
            1,
            0,
            regulator="momentum_cutoff",
        )


def test_sign_gate_describes_only_the_leading_additive_shift() -> None:
    positive = leading_scalar_newton_shift_coefficient(
        1,
        0,
        regulator=SHARP_PROPER_TIME_REGULATOR,
    )
    zero = leading_scalar_newton_shift_coefficient(
        1,
        FOUR_DIMENSIONAL_CONFORMAL_COUPLING,
        regulator=SHARP_PROPER_TIME_REGULATOR,
    )
    negative = leading_scalar_newton_shift_coefficient(
        1,
        sp.Rational(1, 2),
        regulator=SHARP_PROPER_TIME_REGULATOR,
    )
    assert (positive.sign, zero.sign, negative.sign) == (1, 0, -1)
    assert positive.positive_leading_shift is True
    assert zero.positive_leading_shift is False
    assert negative.positive_leading_shift is False
    assert not hasattr(positive, "attractive")
    assert not hasattr(positive, "induced_planck_length")
    assert not hasattr(positive, "sine_gordon_length")


def test_leading_coefficient_composes_with_conditional_ledger() -> None:
    cutoff, speed, action = sp.symbols("a c hbar", positive=True)
    baseline = sp.Symbol("B", real=True)
    coefficient = leading_scalar_newton_shift_coefficient(
        3,
        0,
        regulator=SHARP_PROPER_TIME_REGULATOR,
    ).coefficient
    ledger = induced_inverse_newton_ledger(
        cutoff,
        coefficient,
        speed,
        action,
        baseline_inverse_newton=baseline,
    )
    assert ledger.induced_inverse_newton == coefficient * action / (
        cutoff**2 * speed**3
    )
    assert ledger.total_inverse_newton == baseline + ledger.induced_inverse_newton
    assert sp.simplify(
        ledger.pure_induced_newton * ledger.induced_inverse_newton - 1
    ) == 0


def test_coefficient_is_target_blind_and_has_no_sine_gordon_inputs() -> None:
    xi = sp.Symbol("xi", real=True, negative=True)
    count = sp.Symbol("N", integer=True, positive=True)
    result = leading_scalar_newton_shift_coefficient(
        count,
        xi,
        regulator=SHARP_PROPER_TIME_REGULATOR,
    )
    assert result.coefficient.free_symbols == {count, xi}
    forbidden = {"G", "ell", "lambda", "mu", "T"}
    assert all(
        str(symbol) not in forbidden
        for symbol in result.coefficient.free_symbols
    )


@pytest.mark.parametrize("bad_count", [0, -1, sp.Rational(3, 2), sp.Float(2.0)])
def test_field_count_must_be_an_exact_positive_integer(bad_count) -> None:
    with pytest.raises(ValueError):
        leading_scalar_newton_shift_coefficient(
            bad_count,
            0,
            regulator=SHARP_PROPER_TIME_REGULATOR,
        )


@pytest.mark.parametrize("bad_mass_squared", [-1, sp.Symbol("m2", real=True)])
def test_mass_squared_must_be_exact_and_provably_nonnegative(
    bad_mass_squared,
) -> None:
    with pytest.raises(ValueError):
        scalar_heat_kernel_a2(0, bad_mass_squared)


def test_undecidable_shift_sign_is_rejected_without_weakening_a2_data() -> None:
    xi = sp.Symbol("xi", real=True)
    assert scalar_heat_kernel_a2(xi).curvature_weight == sp.Rational(1, 6) - xi
    with pytest.raises(ValueError, match="decidable relation"):
        leading_scalar_newton_shift_coefficient(
            1,
            xi,
            regulator=SHARP_PROPER_TIME_REGULATOR,
        )
