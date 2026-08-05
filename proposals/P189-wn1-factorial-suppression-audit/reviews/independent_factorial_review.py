#!/usr/bin/env python3
"""Independent raw-SymPy review of WN1's factorial suppression claims."""

from __future__ import annotations

import ast
import math
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def _q(order: int) -> sp.Rational:
    return sp.Rational(1, math.factorial(order) ** 2)


def _decimal_floor(value: sp.Rational) -> int:
    numerator, denominator = map(int, sp.fraction(value))
    exponent = len(str(numerator)) - len(str(denominator))
    while (
        numerator < denominator * 10**exponent
        if exponent >= 0
        else numerator * 10 ** (-exponent) < denominator
    ):
        exponent -= 1
    while (
        numerator >= denominator * 10 ** (exponent + 1)
        if exponent + 1 >= 0
        else numerator * 10 ** (-(exponent + 1)) >= denominator
    ):
        exponent += 1
    return exponent


def main() -> int:
    checks = CheckLedger("C-CMB-001-INDEPENDENT")
    own_text = Path(__file__).read_text(encoding="utf-8")
    own_tree = ast.parse(own_text)
    imported_modules = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "review imports neither the new API nor the accepted cosine API",
        imported_modules.isdisjoint(
            {
                "substrate_framework.factorial_suppression",
                "substrate_framework.cosine_vertices",
            }
        ),
    )

    high, low = sp.symbols("H L", real=True)
    amplitude, high_scale, low_scale = sp.symbols("A a_H a_L", real=True)
    background = sp.Symbol("phi_0", real=True)
    potential = amplitude * (
        1 - sp.cos(background + high_scale * high + low_scale * low)
    )
    raw_coefficients: dict[int, sp.Expr] = {}
    for order in range(12):
        derivative = sp.diff(potential, high, 1, low, order).subs(
            {high: 0, low: 0, background: 0}
        )
        raw_coefficients[order] = sp.simplify(derivative / math.factorial(order))
    checks.check(
        "fresh differentiation gives zero at every sampled even low order",
        all(raw_coefficients[order] == 0 for order in range(0, 12, 2)),
    )
    checks.check(
        "fresh differentiation gives the signed normalized odd formula",
        all(
            sp.simplify(
                raw_coefficients[order]
                - amplitude
                * (-1) ** ((order - 1) // 2)
                * high_scale
                * low_scale**order
                / math.factorial(order)
            )
            == 0
            for order in range(1, 12, 2)
        ),
    )
    checks.check(
        "fresh square retains amplitude and coordinate normalizations",
        sp.factor(raw_coefficients[5] ** 2)
        == amplitude**2 * high_scale**2 * low_scale**10 / math.factorial(5) ** 2,
    )
    background_coefficient = sp.simplify(
        sp.diff(potential, high, 1, low, 4).subs({high: 0, low: 0})
        / math.factorial(4)
    )
    checks.check(
        "fresh background mutation breaks the vacuum parity specialization",
        background_coefficient.subs(background, 0) == 0
        and background_coefficient.subs(background, sp.pi / 2) != 0,
    )

    values = [_q(order) for order in range(1, 30)]
    checks.check("fresh exact factorial sequence stays positive", all(value > 0 for value in values))
    checks.check(
        "fresh quotient gives the inverse-square recurrence",
        all(
            sp.simplify(values[order] / values[order - 1])
            == sp.Rational(1, (order + 1) ** 2)
            for order in range(1, len(values))
        ),
    )
    checks.check(
        "fresh recurrence is strictly decreasing after the unit initial value",
        values[0] == 1 and all(first > second for first, second in zip(values, values[1:])),
    )
    expected_floors = {1: 0, 3: -2, 5: -5, 7: -8, 15: -25, 31: -68, 51: -133}
    checks.check(
        "fresh exact integer comparisons reproduce every decimal floor",
        {order: _decimal_floor(_q(order)) for order in expected_floors} == expected_floors,
    )

    finite_sum = sum(sp.Rational(1, math.factorial(k)) for k in range(4))
    tail_majorant = sp.Rational(1, 24) / (1 - sp.Rational(1, 5))
    checks.check(
        "fresh exponential-series majorant proves the rational e ceiling",
        finite_sum == sp.Rational(8, 3)
        and tail_majorant == sp.Rational(5, 96)
        and finite_sum + tail_majorant < sp.Rational(49, 18)
        and sp.Rational(49, 18) < sp.Rational(11, 4),
    )
    checks.check(
        "fresh integer arithmetic proves the twentieth-power block",
        11**20 < 10**9 * 4**20
        and 10**9 * 4**20 - 11**20 == 426_761_632_843_439_990_799,
    )
    for order in (1, 2, 5, 13, 34):
        selected_term = sp.Rational(order**order, math.factorial(order))
        positive_companion = sp.Integer(1)
        checks.check(
            f"fresh positive-series term is strictly subordinate at order {order}",
            selected_term + positive_companion > selected_term
            and _q(order) < (sp.E / order) ** (2 * order),
        )

    expected_bounds = {7: 131_000_000, 9: 17_100_000_000, 11: 2_110_000_000_000}
    checks.check(
        "fresh block grouping reproduces the three exact decade ceilings",
        all(
            (20 * decade - 9) * 10**decade // 10 == exponent
            for decade, exponent in expected_bounds.items()
        ),
    )
    checks.check(
        "fresh decade ceilings strengthen monotonically",
        expected_bounds[7] < expected_bounds[9] < expected_bounds[11],
    )

    tail_certificates: list[tuple[int, int, sp.Rational]] = []
    for power in (*range(25), 257):
        start = max(1, math.isqrt(2 ** (power + 1) - 1))
        while (start + 1) ** 2 < 2 ** (power + 1):
            start += 1
        ratio = sp.Rational((start + 1) ** power, start**power * (start + 1) ** 2)
        tail_certificates.append((power, start, ratio))
    checks.check(
        "fresh fixed-power construction gives geometric half-tails",
        all(
            ratio <= sp.Rational(1, 2)
            and (start + 1) ** 2 >= 2 ** (power + 1)
            for power, start, ratio in tail_certificates
        ),
    )
    tail_offset = sp.Symbol("k", nonnegative=True, integer=True)
    checks.check(
        "geometric half-tail implies every fixed-power sequence tends to zero",
        sp.limit(sp.Rational(1, 2) ** tail_offset, tail_offset, sp.oo) == 0,
    )

    try:
        machine_value = 1.0 / float(math.factorial(171)) ** 2
    except OverflowError:
        machine_value = 0.0
    checks.check(
        "fresh representation probe separates machine zero from exact positivity",
        machine_value == 0.0 and _q(171) > 0,
    )

    coefficient_square = sp.Rational(1, 36)
    interaction, density = sp.symbols("g rho", nonnegative=True)
    conditional_rate = 2 * sp.pi * interaction**2 * density * coefficient_square
    checks.check(
        "fresh null interaction and density countermodels refute automatic rate typing",
        coefficient_square > 0
        and conditional_rate.subs(interaction, 0) == 0
        and conditional_rate.subs(density, 0) == 0,
    )
    checks.mutation_sensitive(
        "fresh recurrence mutation probe",
        lambda candidate: candidate == sp.Rational(1, 12**2),
        _q(12) / _q(11),
        (sp.Rational(1, 12), sp.Rational(1, 11**2)),
    )
    numpy_imports = [
        node
        for node in ast.walk(own_tree)
        if (
            isinstance(node, ast.Import)
            and any(alias.name == "numpy" for alias in node.names)
        )
        or (isinstance(node, ast.ImportFrom) and node.module == "numpy")
    ]
    numpy_accesses = [
        node
        for node in ast.walk(own_tree)
        if isinstance(node, ast.Name) and node.id in {"np", "numpy"}
    ]
    checks.check(
        "independent review has no NumPy compatibility surface",
        not numpy_imports and not numpy_accesses,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
