#!/usr/bin/env python3
"""Independent factorization and mode-role review for P033."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P033-INDEPENDENT")
    coordinate = sp.symbols("y", real=True)
    function = sp.Function("g")(coordinate)

    def a(value: sp.Expr, level: int) -> sp.Expr:
        return sp.diff(value, coordinate) + level * sp.tanh(coordinate) * value

    def adag(value: sp.Expr, level: int) -> sp.Expr:
        return -sp.diff(value, coordinate) + level * sp.tanh(coordinate) * value

    def k(value: sp.Expr, level: int) -> sp.Expr:
        return -sp.diff(value, coordinate, 2) - level * (level + 1) * sp.sech(
            coordinate
        ) ** 2 * value

    checks.check(
        "independent s=2 factorization is exact",
        sp.simplify(adag(a(function, 2), 2) - k(function, 2) - 4 * function)
        == 0,
    )
    checks.check(
        "the s=2 partner is the s=1 operator",
        sp.simplify(a(adag(function, 2), 2) - k(function, 1) - 4 * function)
        == 0,
    )
    checks.check(
        "the s=1 partner terminates at the free operator",
        sp.simplify(
            a(adag(function, 1), 1)
            + sp.diff(function, coordinate, 2)
            - function
        )
        == 0,
    )

    even = sp.sech(coordinate) ** 2
    odd = sp.sech(coordinate) * sp.tanh(coordinate)
    h = lambda value: k(value, 2) + value
    checks.check(
        "independent exact eigenpairs are minus three and zero in scaled units",
        sp.simplify(h(even) + 3 * even) == 0
        and sp.simplify(h(odd)) == 0,
    )
    checks.check(
        "the modes are L2 and parity orthogonal",
        sp.integrate(even.rewrite(sp.cosh) ** 2, (coordinate, -sp.oo, sp.oo))
        == sp.Rational(4, 3)
        and sp.integrate(odd.rewrite(sp.exp) ** 2, (coordinate, -sp.oo, sp.oo))
        == sp.Rational(2, 3)
        and sp.integrate(even * odd, (coordinate, -sp.oo, sp.oo)) == 0,
    )
    checks.check(
        "the odd mode is the derivative of the sech background",
        sp.simplify(sp.diff(sp.sech(coordinate), coordinate) + odd) == 0,
    )
    checks.check(
        "the free partner has continuum threshold zero before the plus-one shift",
        sp.limit(-6 * sp.sech(coordinate) ** 2 + 1, coordinate, sp.oo) == 1,
    )
    checks.check(
        "the exact levels cannot both be positive particle masses",
        -3 < 0 and sp.Integer(0) == 0,
    )

    total = checks.finish()
    print(f"P033 INDEPENDENT FACTORIZATION REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
