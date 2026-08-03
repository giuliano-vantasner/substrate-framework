import pytest
import sympy as sp

from substrate_framework.composite_factors import (
    actual_loss_cycle_product,
    common_loss_pair_magnitude,
    conditional_composite_factor,
    loss_cycle_composition,
    nominal_loss_cycle_product,
    zero_cutoff_nominal_loss_cycle_product,
)


def test_common_loss_pair_magnitude_is_exact_multi_pair_sum():
    gamma = sp.symbols("gamma", positive=True)
    result = common_loss_pair_magnitude((1, 2, 3), (sp.Rational(1, 100),) * 3, gamma)
    expected = gamma * sp.Rational(1, 100) * sum(
        1 / (sp.Integer(j) ** 2 + gamma**2 / 4) for j in (1, 2, 3)
    )
    assert sp.simplify(result - expected) == 0


def test_nominal_cycle_product_cancels_the_explicit_loss_factor():
    gamma, omega = sp.symbols("gamma omega", positive=True)
    result = nominal_loss_cycle_product((2,), (3,), gamma, omega)
    assert sp.simplify(result - omega * 3 / (2 * sp.pi * (4 + gamma**2 / 4))) == 0


def test_nominal_ledger_derivative_and_zero_limit_are_exact():
    gamma, omega = sp.symbols("gamma omega", positive=True)
    ledger = loss_cycle_composition((1, 2), (3, 5), gamma, omega)
    assert sp.simplify(sp.diff(ledger.nominal_product, gamma) - ledger.nominal_loss_derivative) == 0
    assert ledger.nominal_loss_derivative.is_negative is True
    assert sp.simplify(sp.limit(ledger.nominal_product, gamma, 0, dir="+") - ledger.zero_loss_limit) == 0
    assert ledger.zero_loss_limit.is_positive is True


def test_nominal_cutoff_extension_has_two_jump_boundaries():
    gamma = sp.symbols("gamma", nonnegative=True)
    piecewise = zero_cutoff_nominal_loss_cycle_product((1,), (2,), gamma, 3)
    assert piecewise.subs(gamma, 0) == 0
    assert piecewise.subs(gamma, 6) == 0
    assert piecewise.subs(gamma, 1).is_positive is True
    right_zero = sp.limit(3 * 2 / (2 * sp.pi * (1 + gamma**2 / 4)), gamma, 0, dir="+")
    left_critical = sp.limit(3 * 2 / (2 * sp.pi * (1 + gamma**2 / 4)), gamma, 6, dir="-")
    assert right_zero > 0
    assert left_critical > 0


def test_numeric_cutoff_branches_are_exact():
    assert zero_cutoff_nominal_loss_cycle_product((1,), (2,), 0, 3) == 0
    assert zero_cutoff_nominal_loss_cycle_product((1,), (2,), 6, 3) == 0
    assert zero_cutoff_nominal_loss_cycle_product((1,), (2,), 7, 3) == 0
    assert zero_cutoff_nominal_loss_cycle_product((1,), (2,), 1, 3) > 0


def test_actual_cycle_product_vanishes_at_criticality():
    gamma, omega = sp.symbols("gamma omega", positive=True)
    result = actual_loss_cycle_product((1,), (2,), gamma, omega)
    assert sp.limit(result, gamma, 2 * omega, dir="-") == 0
    expected_zero_limit = omega * 2 / (2 * sp.pi)
    assert sp.simplify(sp.limit(result, gamma, 0, dir="+") - expected_zero_limit) == 0


def test_actual_cycle_product_rejects_nonunderdamped_numeric_input():
    with pytest.raises(ValueError, match=r"gamma < 2\*omega_0"):
        actual_loss_cycle_product((1,), (2,), 6, 3)


def test_large_loss_coefficient_matches_inverse_square_asymptotic():
    gamma, omega = sp.symbols("gamma omega", positive=True)
    ledger = loss_cycle_composition((1, 2), (3, 5), gamma, omega)
    assert sp.simplify(
        sp.limit(gamma**2 * ledger.nominal_product, gamma, sp.oo)
        - ledger.large_loss_inverse_square_coefficient
    ) == 0


def test_conditional_factor_composes_canonical_activation_and_gate():
    gamma = sp.symbols("gamma", positive=True)
    result = conditional_composite_factor(
        5,
        7,
        11,
        13,
        (2,),
        (3,),
        gamma,
        17,
        sp.Rational(19, 23),
    )
    expected = (
        sp.exp(-sp.Rational(5, 7))
        * 11
        * 13
        * 17
        * 3
        / (2 * sp.pi * (4 + gamma**2 / 4))
        * sp.sech(sp.Rational(19, 46)) ** 2
        / 2
    )
    assert sp.simplify(result - expected) == 0


@pytest.mark.parametrize(
    ("detunings", "products", "message"),
    [
        ((), (), "nonempty"),
        ((1,), (1, 2), "equal length"),
        ((0,), (1,), "nonzero"),
        ((1,), (-1,), "nonnegative"),
        ((1,), (0,), "at least one"),
        ((1.0,), (1,), "exact"),
    ],
)
def test_pair_domain_guards(detunings, products, message):
    with pytest.raises(ValueError, match=message):
        common_loss_pair_magnitude(detunings, products, 1)


def test_loss_and_frequency_domain_guards():
    with pytest.raises(ValueError, match="loss must be explicitly positive"):
        nominal_loss_cycle_product((1,), (1,), 0, 1)
    with pytest.raises(ValueError, match="natural_frequency must be explicitly positive"):
        nominal_loss_cycle_product((1,), (1,), 1, 0)


def test_conditional_count_and_splitting_guards():
    with pytest.raises(ValueError, match="positive integer"):
        conditional_composite_factor(1, 1, sp.Rational(3, 2), 2, (1,), (1,), 1, 1, 1)
    with pytest.raises(ValueError, match="thermal_splitting must be explicitly positive"):
        conditional_composite_factor(1, 1, 1, 2, (1,), (1,), 1, 1, 0)
