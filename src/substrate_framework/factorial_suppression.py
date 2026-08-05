"""Exact suppression ledgers for inverse-square factorial sequences.

The helpers compose the classical coefficient theorem in
:mod:`substrate_framework.cosine_vertices` with elementary exact factorial
bounds.  A coefficient square is not by itself a matrix element, probability,
transition rate, branching weight, or physical subdivision law.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Any

import sympy as sp

from .cosine_vertices import vacuum_one_high_coefficient


def _integer_at_least(value: Any, *, name: str, minimum: int) -> int:
    expression = sp.sympify(value)
    if (
        expression.is_number is not True
        or expression.is_integer is not True
        or expression.has(sp.Float)
    ):
        raise ValueError(f"{name} must be an exact integer")
    integer = int(expression)
    if integer < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return integer


def _exact_real(value: Any, *, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float) or expression.is_real is not True:
        raise ValueError(f"{name} must be exact and provably real")
    return expression


def exact_rational_log10_floor(value: Any) -> int:
    """Return ``floor(log10(value))`` using exact integer comparisons.

    ``value`` must be a positive exact rational.  No logarithm or floating-
    point conversion is evaluated.
    """

    expression = sp.sympify(value)
    if expression.has(sp.Float) or expression.is_Rational is not True:
        raise ValueError("value must be an exact rational")
    rational = sp.Rational(expression)
    if rational <= 0:
        raise ValueError("value must be positive")
    numerator = int(sp.numer(rational))
    denominator = int(sp.denom(rational))

    def at_least_power_of_ten(exponent: int) -> bool:
        if exponent >= 0:
            return numerator >= denominator * 10**exponent
        return numerator * 10 ** (-exponent) >= denominator

    exponent = len(str(numerator)) - len(str(denominator))
    while not at_least_power_of_ten(exponent):
        exponent -= 1
    while at_least_power_of_ten(exponent + 1):
        exponent += 1
    return exponent


def cosine_one_high_coefficient_square(
    low_order: Any,
    *,
    amplitude: Any = 1,
    high_scale: Any = 1,
    low_scale: Any = 1,
) -> sp.Expr:
    """Return the exact square of the declared real one-high coefficient.

    At zero background this is zero for even ``low_order``.  For odd ``n`` it
    is ``A**2*a_H**2*a_L**(2*n)/(n!)**2``.  The explicit normalization factors
    prevent the unit specialization from being mistaken for a universal
    transition weight.
    """

    order = _integer_at_least(low_order, name="low_order", minimum=0)
    amplitude_expression = _exact_real(amplitude, name="amplitude")
    high_expression = _exact_real(high_scale, name="high_scale")
    low_expression = _exact_real(low_scale, name="low_scale")
    coefficient = vacuum_one_high_coefficient(
        order,
        amplitude=amplitude_expression,
        high_scale=high_expression,
        low_scale=low_expression,
    )
    return sp.factor(coefficient**2)


@dataclass(frozen=True)
class FactorialSuppressionEvidence:
    """Exact data for ``q_n=1/(n!)**2`` at one positive integer order."""

    order: int
    inverse_square_factorial: sp.Rational
    next_inverse_square_factorial: sp.Rational
    recurrence_ratio: sp.Rational
    exact_log10_floor: int
    exponential_upper_bound: sp.Expr
    physical_rate_interpretation_is_separate_premise: bool


def factorial_suppression_evidence(order: Any) -> FactorialSuppressionEvidence:
    """Return exact sequence, recurrence, decimal, and exponential-bound data."""

    n = _integer_at_least(order, name="order", minimum=1)
    value = sp.Rational(1, int(sp.factorial(n)) ** 2)
    next_value = sp.Rational(1, int(sp.factorial(n + 1)) ** 2)
    return FactorialSuppressionEvidence(
        order=n,
        inverse_square_factorial=value,
        next_inverse_square_factorial=next_value,
        recurrence_ratio=sp.simplify(next_value / value),
        exact_log10_floor=exact_rational_log10_floor(value),
        exponential_upper_bound=sp.Pow(sp.E / n, 2 * n),
        physical_rate_interpretation_is_separate_premise=True,
    )


@dataclass(frozen=True)
class SuperpolynomialTailEvidence:
    """A geometric tail certificate for ``n**p/(n!)**2``."""

    power: int
    start_order: int
    ratio_ceiling: sp.Rational
    exact_ratio_at_start: sp.Rational


def factorial_superpolynomial_tail(power: Any) -> SuperpolynomialTailEvidence:
    """Return an exact tail where consecutive terms have ratio at most one-half.

    For fixed nonnegative integer ``p``, put ``a_n=n**p/(n!)**2``.  Since
    ``a_(n+1)/a_n <= 2**p/(n+1)**2`` for ``n>=1``, choosing
    ``n+1>=ceil(sqrt(2**(p+1)))`` gives a geometric tail with ratio at most
    one-half and hence ``a_n -> 0``.
    """

    p = _integer_at_least(power, name="power", minimum=0)
    target = 2 ** (p + 1)
    root = isqrt(target)
    ceiling_root = root if root * root == target else root + 1
    start = max(1, ceiling_root - 1)
    ratio = sp.Rational((start + 1) ** p, start**p * (start + 1) ** 2)
    return SuperpolynomialTailEvidence(
        power=p,
        start_order=start,
        ratio_ceiling=sp.Rational(1, 2),
        exact_ratio_at_start=ratio,
    )


@dataclass(frozen=True)
class FactorialDecadeBound:
    """An exact base-ten exponent ceiling at ``n=10**decade``."""

    decade: int
    order: int
    e_series_upper_bound: sp.Rational
    convenient_e_upper_bound: sp.Rational
    twentieth_power_left: int
    twentieth_power_right: int
    twentieth_power_margin: int
    positive_exponent: int
    log10_upper_bound: int
    exposed_order_is_separate_physical_premise: bool


def factorial_decade_bound(decade: Any) -> FactorialDecadeBound:
    r"""Return the exact conservative bound at ``n=10**decade``.

    The exponential series gives ``e<49/18<11/4`` and exact integer arithmetic
    gives ``(11/4)**20<10**9``.  Grouping ``2*n=20*(n/10)`` therefore proves

    ``1/(n!)**2 < 10**(-((20*decade-9)*n/10))``

    for every positive integer decade.  The returned exponent is an integer;
    the enormous decimal itself is never materialized.
    """

    d = _integer_at_least(decade, name="decade", minimum=1)
    n = 10**d
    left = 11**20
    right = 10**9 * 4**20
    positive_exponent = (20 * d - 9) * n // 10
    return FactorialDecadeBound(
        decade=d,
        order=n,
        e_series_upper_bound=sp.Rational(49, 18),
        convenient_e_upper_bound=sp.Rational(11, 4),
        twentieth_power_left=left,
        twentieth_power_right=right,
        twentieth_power_margin=right - left,
        positive_exponent=positive_exponent,
        log10_upper_bound=-positive_exponent,
        exposed_order_is_separate_physical_premise=True,
    )
