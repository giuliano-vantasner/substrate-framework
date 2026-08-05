from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.factorial_suppression import (
    cosine_one_high_coefficient_square,
    exact_rational_log10_floor,
    factorial_decade_bound,
    factorial_superpolynomial_tail,
    factorial_suppression_evidence,
)


def test_inverse_square_factorial_sequence_and_recurrence_are_exact() -> None:
    for order in range(1, 20):
        evidence = factorial_suppression_evidence(order)
        expected = sp.Rational(1, int(sp.factorial(order)) ** 2)
        assert evidence.inverse_square_factorial == expected
        assert evidence.recurrence_ratio == sp.Rational(1, (order + 1) ** 2)
        assert evidence.next_inverse_square_factorial < expected
        assert evidence.inverse_square_factorial > 0


def test_exact_rational_decimal_floor_matches_known_table() -> None:
    expected = {1: 0, 3: -2, 5: -5, 7: -8, 15: -25, 31: -68, 51: -133}
    assert {
        order: factorial_suppression_evidence(order).exact_log10_floor
        for order in expected
    } == expected
    assert exact_rational_log10_floor(sp.Rational(999, 100)) == 0
    assert exact_rational_log10_floor(sp.Rational(1, 10)) == -1
    assert exact_rational_log10_floor(sp.Integer(10)) == 1


def test_general_cosine_square_retains_parity_and_normalizations() -> None:
    amplitude, high_scale, low_scale = sp.symbols(
        "A a_H a_L", real=True
    )
    assert cosine_one_high_coefficient_square(
        4,
        amplitude=amplitude,
        high_scale=high_scale,
        low_scale=low_scale,
    ) == 0
    actual = cosine_one_high_coefficient_square(
        5,
        amplitude=amplitude,
        high_scale=high_scale,
        low_scale=low_scale,
    )
    expected = (
        amplitude**2
        * high_scale**2
        * low_scale**10
        / sp.factorial(5) ** 2
    )
    assert sp.simplify(actual - expected) == 0
    assert sp.simplify(actual.subs(amplitude, 2 * amplitude) / actual) == 4
    assert sp.simplify(actual.subs(low_scale, 2 * low_scale) / actual) == 2**10


def test_exact_decade_bounds_reproduce_the_conservative_exponents() -> None:
    expected = {
        7: -131_000_000,
        9: -17_100_000_000,
        11: -2_110_000_000_000,
    }
    for decade, exponent in expected.items():
        bound = factorial_decade_bound(decade)
        assert bound.log10_upper_bound == exponent
        assert bound.twentieth_power_margin > 0
        assert bound.e_series_upper_bound < bound.convenient_e_upper_bound


def test_superpolynomial_tail_certificate_has_geometric_ratio() -> None:
    for power in range(17):
        tail = factorial_superpolynomial_tail(power)
        assert tail.start_order >= 1
        assert tail.exact_ratio_at_start <= tail.ratio_ceiling
        for order in range(tail.start_order, tail.start_order + 8):
            ratio = sp.Rational(
                (order + 1) ** power,
                order**power * (order + 1) ** 2,
            )
            assert ratio <= sp.Rational(1, 2)


def test_exact_value_remains_positive_at_source_float_zero_order() -> None:
    evidence = factorial_suppression_evidence(171)
    assert evidence.inverse_square_factorial > 0


@pytest.mark.parametrize("bad", [0, -1, sp.Rational(3, 2), sp.Symbol("n"), 2.0])
def test_positive_integer_domains_reject_invalid_orders(bad: object) -> None:
    with pytest.raises(ValueError):
        factorial_suppression_evidence(bad)


@pytest.mark.parametrize("bad", [-1, sp.Rational(1, 2), sp.Symbol("p"), 2.0])
def test_nonnegative_integer_power_domain_is_exact(bad: object) -> None:
    with pytest.raises(ValueError):
        factorial_superpolynomial_tail(bad)


@pytest.mark.parametrize("bad", [0, -1, sp.Rational(1, 2), sp.Symbol("d"), 2.0])
def test_positive_integer_decade_domain_is_exact(bad: object) -> None:
    with pytest.raises(ValueError):
        factorial_decade_bound(bad)


@pytest.mark.parametrize("bad", [0, -1, sp.sqrt(2), sp.Symbol("q"), 0.1])
def test_exact_log_floor_rejects_nonpositive_or_nonrational_values(bad: object) -> None:
    with pytest.raises(ValueError):
        exact_rational_log10_floor(bad)


def test_coefficient_square_rejects_inexact_or_nonreal_coordinates() -> None:
    with pytest.raises(ValueError):
        cosine_one_high_coefficient_square(3, amplitude=1.0)
    with pytest.raises(ValueError):
        cosine_one_high_coefficient_square(3, low_scale=sp.Symbol("z"))
