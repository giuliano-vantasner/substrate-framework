from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.cosine_vertices import (
    cosine_mixed_coefficient,
    cosine_mixed_derivative,
    cosine_mixed_taylor_polynomial,
    vacuum_cosine_mixed_coefficient,
    vacuum_one_high_coefficient,
)


def test_vacuum_all_order_closed_form_on_grid() -> None:
    amplitude, high_scale, low_scale = sp.symbols("A a_H a_L", nonzero=True)
    for high_order in range(7):
        for low_order in range(7):
            total = high_order + low_order
            actual = vacuum_cosine_mixed_coefficient(
                high_order,
                low_order,
                amplitude=amplitude,
                high_scale=high_scale,
                low_scale=low_scale,
            )
            if total == 0 or total % 2:
                expected = 0
            else:
                expected = (
                    amplitude
                    * (-1) ** (total // 2 + 1)
                    * high_scale**high_order
                    * low_scale**low_order
                    / (sp.factorial(high_order) * sp.factorial(low_order))
                )
            assert sp.simplify(actual - expected) == 0


def test_one_high_specialization_has_odd_low_order_only() -> None:
    for low_order in range(9):
        actual = vacuum_one_high_coefficient(low_order)
        expected = (
            (-1) ** ((low_order - 1) // 2) / sp.factorial(low_order)
            if low_order % 2
            else 0
        )
        assert sp.simplify(actual - expected) == 0


def test_raw_derivative_and_polynomial_coefficient_differ_by_factorials() -> None:
    assert cosine_mixed_coefficient(2, 4) == sp.Rational(1, 48)
    assert cosine_mixed_derivative(2, 4) == 1
    assert sp.factorial(2) * sp.factorial(4) * cosine_mixed_coefficient(2, 4) == 1


def test_coordinate_normalizations_are_load_bearing() -> None:
    high_scale, low_scale = sp.symbols("a_H a_L", nonzero=True)
    coefficient = vacuum_one_high_coefficient(
        3,
        high_scale=high_scale,
        low_scale=low_scale,
    )
    assert coefficient == -high_scale * low_scale**3 / 6
    assert sp.simplify(coefficient.subs(high_scale, 2 * high_scale) / coefficient) == 2
    assert sp.simplify(coefficient.subs(low_scale, 2 * low_scale) / coefficient) == 8


def test_nonvacuum_background_breaks_total_parity_rule() -> None:
    background = sp.pi / 2
    assert cosine_mixed_coefficient(1, 0, background=background) == 1
    assert cosine_mixed_coefficient(0, 1, background=background) == 1
    assert cosine_mixed_coefficient(1, 1, background=background) == 0
    assert cosine_mixed_coefficient(1, 2, background=background) == -sp.Rational(1, 2)


def test_background_constant_coefficient_is_retained() -> None:
    background = sp.symbols("phi_0", real=True)
    assert cosine_mixed_coefficient(0, 0, background=background) == 1 - sp.cos(background)


def test_total_degree_polynomial_matches_direct_series() -> None:
    high, low, scale = sp.symbols("H L lambda", real=True)
    polynomial = cosine_mixed_taylor_polynomial(high, low, 8)
    direct = 1 - sp.cos(high + low)
    residual_series = sp.series(
        (direct - polynomial).subs({high: scale * high, low: scale * low}),
        scale,
        0,
        10,
    ).removeO()
    assert sp.simplify(residual_series) == 0
    next_series = sp.series(
        (direct - polynomial).subs({high: scale * high, low: scale * low}),
        scale,
        0,
        11,
    ).removeO()
    assert sp.simplify(next_series) != 0


def test_univariate_reconstruction_agrees_with_cosine_series() -> None:
    field = sp.symbols("phi", real=True)
    polynomial = cosine_mixed_taylor_polynomial(field, 0, 6)
    expected = sp.series(1 - sp.cos(field), field, 0, 8).removeO()
    assert sp.expand(polynomial - expected) == 0


@pytest.mark.parametrize("bad_order", [-1, sp.Rational(1, 2), sp.Symbol("n")])
def test_order_validation_rejects_unresolved_or_invalid_orders(bad_order: sp.Expr) -> None:
    with pytest.raises(ValueError):
        cosine_mixed_coefficient(bad_order, 1)


def test_factorial_suppression_is_explicit_for_nonzero_one_high_terms() -> None:
    magnitudes = [abs(vacuum_one_high_coefficient(n)) for n in (1, 3, 5, 7)]
    assert magnitudes == [1, sp.Rational(1, 6), sp.Rational(1, 120), sp.Rational(1, 5040)]
    assert all(left > right for left, right in zip(magnitudes, magnitudes[1:]))
