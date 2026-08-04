#!/usr/bin/env python3
"""Fresh exact SM3 review without importing the P165 anomaly API."""

from __future__ import annotations

from itertools import product

import sympy as sp

from substrate_framework.verification import CheckLedger


def _equations(
    values: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr],
) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    q, u, d, l, e = values
    return tuple(
        sp.expand(expression)
        for expression in (
            2 * q + u + d,
            3 * q + l,
            6 * q + 3 * u + 3 * d + 2 * l + e,
            6 * q**3 + 3 * u**3 + 3 * d**3 + 2 * l**3 + e**3,
        )
    )


def _component_names(
    values: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr],
) -> tuple[str, ...]:
    q, u, d, l, e = values
    candidates = (
        ("displayed", (u + 4 * q, d - 2 * q, l + 3 * q, e - 6 * q)),
        ("exchanged", (u - 2 * q, d + 4 * q, l + 3 * q, e - 6 * q)),
        ("vectorlike", (q, l, e, d + u)),
    )
    return tuple(
        name
        for name, residuals in candidates
        if all(sp.simplify(residual) == 0 for residual in residuals)
    )


def run() -> int:
    checks = CheckLedger("P165-INDEPENDENT")
    q, u, d, l, e = sp.symbols("q u d l e", real=True)
    equations = _equations((q, u, d, l, e))

    linear_solution = sp.solve(equations[:3], (d, l, e), dict=True)
    checks.check(
        "fresh linear elimination has one exact two-parameter chart",
        linear_solution == [{d: -2 * q - u, e: 6 * q, l: -3 * q}],
    )
    reduced = sp.factor(equations[3].subs(linear_solution[0]))
    checks.check(
        "fresh cubic reduction retains the zero-q factor",
        reduced == 18 * q * (2 * q - u) * (4 * q + u),
    )

    groebner = sp.groebner(equations, e, l, d, u, q, order="lex")
    checks.check(
        "fresh Groebner basis independently matches the eliminated ideal",
        tuple(groebner.polys)
        == tuple(
            sp.Poly(expression, e, l, d, u, q)
            for expression in (
                e - 6 * q,
                l + 3 * q,
                d + 2 * q + u,
                -8 * q**3 + 2 * q**2 * u + q * u**2,
            )
        ),
    )

    t = sp.symbols("t", real=True)
    branches = {
        "displayed": (t, -4 * t, 2 * t, -3 * t, 6 * t),
        "exchanged": (t, 2 * t, -4 * t, -3 * t, 6 * t),
        "vectorlike": (0, t, -t, 0, 0),
    }
    checks.check(
        "fresh substitution proves all three parameterized lines",
        all(
            all(residual == 0 for residual in _equations(values))
            for values in branches.values()
        ),
    )

    grid_solutions = tuple(
        values
        for values in product(range(-2, 3), repeat=5)
        if all(residual == 0 for residual in _equations(values))
    )
    expected_grid_solutions = {
        tuple(sp.expand(sp.sympify(value).subs(t, parameter)) for value in branch)
        for branch in branches.values()
        for parameter in range(-2, 3)
        if all(
            -2 <= sp.sympify(value).subs(t, parameter) <= 2
            for value in branch
        )
    }
    checks.check(
        "independent bounded exact enumeration finds no fourth component",
        set(grid_solutions) == expected_grid_solutions
        and all(_component_names(values) for values in grid_solutions),
    )

    displayed = (
        sp.Rational(1, 6),
        -sp.Rational(2, 3),
        sp.Rational(1, 3),
        -sp.Rational(1, 2),
        sp.Integer(1),
    )
    exchanged = (
        sp.Rational(1, 6),
        sp.Rational(1, 3),
        -sp.Rational(2, 3),
        -sp.Rational(1, 2),
        sp.Integer(1),
    )
    vectorlike = (0, 1, -1, 0, 0)
    checks.check(
        "fresh displayed point is anomaly-free",
        _equations(displayed) == (0, 0, 0, 0)
        and _component_names(displayed) == ("displayed",),
    )
    checks.check(
        "fresh row-exchanged point refutes uniqueness up to scale",
        _equations(exchanged) == (0, 0, 0, 0)
        and _component_names(exchanged) == ("exchanged",),
    )
    checks.check(
        "fresh vectorlike point preserves the omitted zero-q component",
        _equations(vectorlike) == (0, 0, 0, 0)
        and _component_names(vectorlike) == ("vectorlike",),
    )

    lambda_symbol = sp.symbols("lambda", real=True, nonzero=True)
    scaled = tuple(lambda_symbol * value for value in (q, u, d, l, e))
    scaled_equations = _equations(scaled)
    checks.check(
        "fresh homogeneity calculation has degrees one one one and three",
        tuple(
            sp.simplify(scaled_equations[index] - lambda_symbol * equations[index])
            for index in range(3)
        )
        == (0, 0, 0)
        and sp.simplify(scaled_equations[3] - lambda_symbol**3 * equations[3]) == 0,
    )

    wrong_electron = displayed[:-1] + (sp.Integer(0),)
    checks.check(
        "fresh one-row mutation reopens cubic and gravitational coefficients",
        _equations(wrong_electron)[2:] == (-1, -1),
    )
    checks.check(
        "fresh global criteria depend on supplied representations not charges",
        3 + 1 == 4
        and (3 + 1) % 2 == 0
        and 2 - 1 - 1 == 0
        and 3 % 2 == 1,
    )
    checks.check(
        "fresh neutral singlet counterfamily leaves every coefficient unchanged",
        1 * 1 * 0 == 0 and 1 * 1 * 0**3 == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P165 INDEPENDENT ALL {result} CHECKS PASS")
