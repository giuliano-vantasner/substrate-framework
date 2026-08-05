#!/usr/bin/env python3
"""Independent raw-series rederivation for the P198 coherent-state claim."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P198-MD3-INDEPENDENT")
    x, y = sp.symbols("x y", real=True)
    alpha = x + sp.I * y
    S = x**2 + y**2

    def coefficient(order: int) -> sp.Expr:
        return sp.exp(-S / 2) * alpha**order / sp.sqrt(sp.factorial(order))

    for order in range(8):
        current = coefficient(order)
        probability = sp.simplify(sp.conjugate(current) * current)
        expected = sp.exp(-S) * S**order / sp.factorial(order)
        checks.check(
            f"raw coefficient modulus order {order}",
            sp.simplify(probability - expected) == 0,
        )

    order_symbol = sp.symbols("n", integer=True, nonnegative=True)
    total = sp.summation(
        sp.exp(-S) * S**order_symbol / sp.factorial(order_symbol),
        (order_symbol, 0, sp.oo),
    )
    checks.check("raw series norm is one", sp.simplify(total - 1) == 0)

    for order in range(7):
        checks.check(
            f"raw annihilation recurrence order {order}",
            sp.simplify(
                sp.sqrt(order + 1) * coefficient(order + 1)
                - alpha * coefficient(order)
            )
            == 0,
        )

    t = sp.symbols("t", real=True)
    pgf = sp.summation(
        sp.exp(-S) * S**order_symbol * t**order_symbol / sp.factorial(order_symbol),
        (order_symbol, 0, sp.oo),
    )
    checks.check("raw PGF is exponential", sp.simplify(pgf - sp.exp(S * (t - 1))) == 0)
    mean = sp.diff(pgf, t).subs(t, 1)
    variance = sp.diff(pgf, t, 2).subs(t, 1) + mean - mean**2
    checks.check("raw number mean is S", sp.simplify(mean - S) == 0)
    checks.check("raw number variance is S", sp.simplify(variance - S) == 0)

    beta_x, beta_y = sp.symbols("u v", real=True)
    beta = beta_x + sp.I * beta_y
    T = beta_x**2 + beta_y**2
    overlap = sp.summation(
        sp.exp(-(S + T) / 2)
        * sp.conjugate(alpha) ** order_symbol
        * beta**order_symbol
        / sp.factorial(order_symbol),
        (order_symbol, 0, sp.oo),
    )
    checks.check(
        "raw overlap sums independently",
        sp.simplify(
            overlap
            - sp.exp(-(S + T) / 2 + sp.conjugate(alpha) * beta)
        )
        == 0,
    )
    checks.check(
        "raw overlap diagonal is one",
        sp.simplify(overlap.subs({beta_x: x, beta_y: y}) - 1) == 0,
    )

    integer_intensity = sp.Integer(25)
    ratio_before = integer_intensity / integer_intensity
    ratio_after = integer_intensity / (integer_intensity + 1)
    checks.check(
        "positive integer intensity has an adjacent mode tie",
        ratio_before == 1 and ratio_after < 1,
    )

    phase = sp.symbols("phase", real=True)
    charge = sp.symbols("charge", integer=True)
    multiplier = sp.exp(sp.I * charge * phase)
    checks.check(
        "independent compact vertex preserves density",
        sp.simplify(sp.conjugate(multiplier) * multiplier - 1) == 0,
    )
    checks.check(
        "independent compact vertex is periodic for integer charge",
        sp.simplify(
            multiplier.subs(phase, phase + 2 * sp.pi) - multiplier
        )
        == 0,
    )

    wrong_total = sp.summation(
        S**order_symbol / sp.factorial(order_symbol),
        (order_symbol, 0, sp.oo),
    )
    checks.check(
        "missing Gaussian factor is independently rejected",
        wrong_total == sp.exp(S) and sp.simplify(wrong_total - 1) != 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
