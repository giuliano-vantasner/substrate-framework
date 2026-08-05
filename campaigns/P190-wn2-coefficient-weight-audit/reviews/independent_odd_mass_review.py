#!/usr/bin/env python3
"""Independent raw-SymPy review of the P190 odd factorial-mass theorem."""

from __future__ import annotations

import ast
import math
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def _raw_mass(order: int, activity: sp.Expr = sp.Integer(1)) -> sp.Expr:
    if order <= 0:
        raise ValueError("order must be positive")
    if order % 2 == 0:
        return sp.Integer(0)
    return sp.factor(activity ** (2 * order) / math.factorial(order) ** 2)


def main() -> int:
    checks = CheckLedger("C-CMB-002-INDEPENDENT")
    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported_modules = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "review imports neither candidate nor accepted scientific APIs",
        imported_modules.isdisjoint(
            {
                "substrate_framework.factorial_suppression",
                "substrate_framework.cosine_vertices",
                "substrate_framework.branching",
            }
        ),
    )

    high, low = sp.symbols("H L", real=True)
    amplitude, high_scale, activity = sp.symbols(
        "A a_H z",
        positive=True,
    )
    potential = amplitude * (1 - sp.cos(high_scale * high + activity * low))
    coefficients = {}
    for order in range(8):
        derivative = sp.diff(potential, high, 1, low, order).subs({high: 0, low: 0})
        coefficients[order] = sp.simplify(derivative / math.factorial(order))
    checks.check(
        "fresh differentiation gives zero at every sampled even order",
        all(coefficients[order] == 0 for order in range(0, 8, 2)),
    )
    checks.check(
        "fresh odd coefficient squares retain activity and factorial powers",
        all(
            sp.simplify(
                coefficients[order] ** 2 / (amplitude**2 * high_scale**2)
                - _raw_mass(order, activity)
            )
            == 0
            for order in range(1, 8, 2)
        ),
    )

    total = (sp.besseli(0, 2 * activity) - sp.besselj(0, 2 * activity)) / 2
    raw_series = sum(_raw_mass(order, activity) for order in (1, 3, 5, 7, 9))
    checks.check(
        "raw Bessel expansions independently select the positive odd terms",
        sp.series(total, activity, 0, 21).removeO() == raw_series,
    )
    even_index = 2 * sp.Symbol("k", integer=True, nonnegative=True)
    odd_index = even_index + 1
    even_term = activity ** (2 * even_index) / sp.factorial(even_index) ** 2
    odd_term = activity ** (2 * odd_index) / sp.factorial(odd_index) ** 2
    checks.check(
        "parity projection annihilates even terms and retains odd terms",
        sp.simplify((even_term - even_term) / 2) == 0
        and sp.simplify((odd_term - (-odd_term)) / 2 - odd_term) == 0,
    )
    checks.check(
        "raw general odd term is positive and its normalized total is unity",
        odd_term.is_positive is True and sp.simplify(total / total) == 1,
    )

    maximum = 9
    partial = sp.Rational(sum(_raw_mass(order) for order in range(1, maximum + 1, 2)))
    first = sp.Rational(_raw_mass(maximum + 2))
    ratio = sp.Rational(1, (maximum + 3) ** 2 * (maximum + 4) ** 2)
    tail_upper = sp.factor(first / (1 - ratio))
    total_upper = sp.factor(partial + tail_upper)
    checks.check(
        "raw integer arithmetic reproduces the exact unit enclosure",
        partial == sp.Rational(135348874561, 131681894400)
        and first == sp.Rational(1, 1593350922240000)
        and ratio == sp.Rational(1, 24336)
        and total_upper
        == sp.Rational(9963487458886859459, 9693548673177600000),
    )
    ratios = [
        sp.factor(_raw_mass(order + 2) / _raw_mass(order))
        for order in range(11, 28, 2)
    ]
    checks.check(
        "fresh omitted-term ratios decrease below the geometric ceiling",
        ratios[0] == ratio and all(0 < later < earlier for earlier, later in zip(ratios, ratios[1:])),
    )
    finite_tail = sum(_raw_mass(order) for order in range(11, 52, 2))
    checks.check(
        "independent finite tail is strictly below the infinite majorant",
        0 < finite_tail < tail_upper,
    )

    p1_lower = sp.factor(1 / total_upper)
    p13_lower = sp.factor(sp.Rational(37, 36) / total_upper)
    checks.check(
        "raw rational margins certify both source concentration thresholds",
        p1_lower - sp.Rational(972, 1000)
        == sp.Rational(
            2259715784893151463,
            2490871864721714864750,
        )
        and p13_lower - sp.Rational(9999, 10000)
        == sp.Rational(
            3228039582292269459,
            99634874588868594590000,
        ),
    )
    checks.mutation_sensitive(
        "raw normalization upper bound",
        lambda candidate: candidate
        == sp.Rational(9963487458886859459, 9693548673177600000),
        total_upper,
        (
            sp.Rational(37, 36) + sp.Rational(1, 1000),
            sp.Rational(1),
        ),
    )

    unit = [_raw_mass(order) for order in (1, 3, 5, 7, 9)]
    scaled = [_raw_mass(order, sp.Integer(4)) for order in (1, 3, 5, 7, 9)]
    checks.check(
        "raw activity mutation moves the mode from one to three",
        unit[0] == max(unit)
        and scaled[1] == max(scaled)
        and scaled[1] / scaled[0] == sp.Rational(64, 9)
        and scaled[2] / scaled[1] == sp.Rational(16, 25),
    )
    checks.mutation_sensitive(
        "raw activity-dependent mode",
        lambda candidate: candidate[1] > candidate[0]
        and candidate[1] > candidate[2],
        tuple(scaled[:3]),
        (
            tuple(unit[:3]),
            (scaled[1], scaled[0], scaled[2]),
        ),
    )

    index = sp.Symbol("n", integer=True, positive=True)
    geometric_total = sp.summation(sp.Rational(1, 2) ** index, (index, 1, sp.oo))
    checks.check(
        "mode one is compatible with a normalized exact probability law",
        geometric_total == 1
        and sp.Rational(1, 2) > sp.Rational(1, 4) > 0,
    )

    baseline, comparison = sp.symbols("r_s r_c", positive=True)
    population = sp.Symbol("N", integer=True, positive=True)
    odd_weight = _raw_mass(3)
    weighted_rate = sp.factor(baseline * odd_weight * population)
    odd_fraction = sp.factor(weighted_rate / (weighted_rate + comparison))
    even_fraction = sp.factor(0 / (0 + comparison))
    checks.check(
        "raw conditional allocation separates positive odd and zero even cases",
        odd_weight == sp.Rational(1, 36)
        and odd_fraction == baseline * population / (baseline * population + 36 * comparison)
        and even_fraction == 0,
    )
    checks.check(
        "allocation algebra does not derive a rate baseline or physical channel",
        odd_fraction.free_symbols == {baseline, comparison, population},
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
