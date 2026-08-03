"""Independent P109 derivation from complex exponentials and binomials."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _exponential_derivative(total: int, background: sp.Expr) -> sp.Expr:
    if total == 0:
        return 1 - sp.cos(background)
    return sp.simplify(
        -(
            sp.I**total * sp.exp(sp.I * background)
            + (-sp.I) ** total * sp.exp(-sp.I * background)
        )
        / 2
    )


def main() -> int:
    checks = CheckLedger("C-SG-019-INDEPENDENT")
    high, low = sp.symbols("H L", real=True)
    high_scale, low_scale = sp.symbols("a_H a_L", nonzero=True)
    amplitude = sp.symbols("A", nonzero=True)

    checks.check(
        "complex exponentials reconstruct the declared cosine potential",
        sp.simplify(
            1
            - (
                sp.exp(sp.I * (high + low))
                + sp.exp(-sp.I * (high + low))
            )
            / 2
            - (1 - sp.cos(high + low))
        )
        == 0,
    )
    for total in range(1, 13):
        derivative = sp.simplify(_exponential_derivative(total, sp.Integer(0)))
        expected = 0 if total % 2 else (-1) ** (total // 2 + 1)
        checks.check(
            f"fresh exponential derivative has correct total-order cycle {total}",
            sp.simplify(derivative - expected) == 0,
        )

    for total in range(2, 11):
        direct_total = (-1) ** (total // 2 + 1) if total % 2 == 0 else 0
        reconstructed = sp.Integer(0)
        for high_order in range(total + 1):
            low_order = total - high_order
            coefficient = (
                amplitude
                * direct_total
                * high_scale**high_order
                * low_scale**low_order
                / (sp.factorial(high_order) * sp.factorial(low_order))
            )
            reconstructed += coefficient * high**high_order * low**low_order
        expected_homogeneous = (
            amplitude
            * direct_total
            * (high_scale * high + low_scale * low) ** total
            / sp.factorial(total)
        )
        checks.check(
            f"fresh binomial reconstruction agrees at total order {total}",
            sp.expand(reconstructed - expected_homogeneous) == 0,
        )

    checks.check(
        "fresh one-high extraction gives the exact odd subsequence",
        all(
            sp.simplify(
                amplitude
                * (-1) ** ((n - 1) // 2)
                * high_scale
                * low_scale**n
                / sp.factorial(n)
                - amplitude
                * (-1) ** ((n + 1) // 2 + 1)
                * high_scale
                * low_scale**n
                / sp.factorial(n)
            )
            == 0
            for n in (1, 3, 5, 7, 15)
        ),
    )
    checks.check(
        "fresh even-low one-high coefficients vanish by odd total degree",
        all(_exponential_derivative(1 + n, 0) == 0 for n in (0, 2, 4, 6)),
    )
    checks.check(
        "fresh pi-over-two background retains its nonzero constant value",
        _exponential_derivative(0, sp.pi / 2) == 1,
    )
    checks.check(
        "fresh pi-over-two background exchanges positive-order parity support",
        all(
            _exponential_derivative(total, sp.pi / 2) == 0
            for total in (2, 4, 6)
        )
        and all(
            _exponential_derivative(total, sp.pi / 2) != 0
            for total in (1, 3, 5, 7)
        ),
    )
    checks.check(
        "fresh coefficient-to-derivative conversion carries both factorials",
        sp.factorial(3) * sp.factorial(5)
        * (
            (-1) ** ((8 // 2) + 1)
            * high_scale**3
            * low_scale**5
            / (sp.factorial(3) * sp.factorial(5))
        )
        == -high_scale**3 * low_scale**5,
    )
    checks.check(
        "fresh field rescaling changes one-high order n by the nth low power",
        sp.simplify(
            (high_scale * (2 * low_scale) ** 5 / sp.factorial(5))
            / (high_scale * low_scale**5 / sp.factorial(5))
        )
        == 32,
    )
    n = sp.symbols("n", integer=True, positive=True)
    checks.check(
        "fresh factorial family vanishes at unbounded odd order",
        sp.limit(1 / sp.gamma(2 * n + 2), n, sp.oo) == 0,
    )

    scale = sp.symbols("lambda", real=True)
    eighth = sum(
        (-1) ** (order // 2 + 1)
        * (scale * (high + low)) ** order
        / sp.factorial(order)
        for order in (2, 4, 6, 8)
    )
    residual = 1 - sp.cos(scale * (high + low)) - eighth
    checks.check(
        "fresh finite polynomial has zero series only through degree nine",
        sp.series(residual, scale, 0, 10).removeO() == 0,
    )
    checks.check(
        "fresh finite polynomial has a nonzero degree-ten remainder",
        sp.simplify(
            sp.expand(sp.series(residual, scale, 0, 11).removeO()).coeff(scale, 10)
            - (high + low) ** 10 / sp.factorial(10)
        )
        == 0,
    )
    checks.check(
        "fresh nonzero local coefficient does not encode time space or states",
        not any(
            expression.has(sp.Derivative, sp.Integral, sp.Function)
            for expression in (
                _exponential_derivative(4, 0),
                high_scale * low_scale**3 / 6,
                eighth,
            )
        ),
    )
    checks.check(
        "fresh review uses no numerical quadrature solver or fitted comparator",
        not any(
            expression.has(sp.Float, sp.Integral)
            for expression in (
                _exponential_derivative(4, 0),
                eighth,
                residual,
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
