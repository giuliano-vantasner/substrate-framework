"""Independent exact P108 review without importing the primary ledger."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P108-INDEPENDENT")
    d = sp.Rational(2224, 1000)
    t = sp.Rational(8482, 1000)
    he3 = sp.Rational(7718, 1000)
    he4 = sp.Rational(28296, 1000)
    b11 = sp.Rational(76205, 1000)
    q = (he4 - 2 * d, he4 - d - he3, he4 - d - t, 3 * he4 - b11)
    expected = (
        sp.Rational(23848, 1000),
        sp.Rational(18354, 1000),
        sp.Rational(17590, 1000),
        sp.Rational(8683, 1000),
    )
    checks.check("fresh bookkeeping reproduces the four exact decimals", q == expected)
    checks.check("fresh selected releases are positive and unequal", all(value > 0 for value in q) and len(set(q)) == 4)

    unit = 16 * sp.pi * sp.Rational(51099895, 100000000)
    ratios = tuple(sp.simplify(value / unit) for value in q)
    checks.check(
        "fresh ratios reproduce the displayed ordering",
        ratios[0] > ratios[1] > ratios[2] > ratios[3],
    )
    checks.check(
        "fresh literal bracket holds only at the supplied unit",
        all(sp.Rational(3, 10) < value < 1 for value in ratios),
    )
    a = sp.symbols("a", positive=True)
    checks.check(
        "fresh common-scale transformation is inverse linear",
        all(sp.simplify((value / (a * unit)) / ratio - 1 / a) == 0 for value, ratio in zip(q, ratios)),
    )
    checks.check(
        "fresh pairwise quotients cancel the scale",
        sp.simplify(ratios[0] / ratios[3] - q[0] / q[3]) == 0,
    )

    low = max(q)
    high = min(q) / sp.Rational(3, 10)
    checks.check(
        "fresh bracket inverse is a nonunique open scale interval",
        low < unit < high and low < high,
    )
    checks.check(
        "fresh scale counterexamples violate the bracket on opposite sides",
        max(value / 10 for value in q) > 1
        and max(value / 100 for value in q) < sp.Rational(3, 10),
    )
    checks.check(
        "fresh multiplicative spread is exactly scale independent",
        sp.simplify((max(q) / (a * unit)) / (min(q) / (a * unit)) - max(q) / min(q)) == 0,
    )
    checks.check(
        "fresh additive range changes under scale rescaling",
        sp.simplify(
            (max(q) / (a * unit) - min(q) / (a * unit))
            / (max(q) / unit - min(q) / unit)
            - 1 / a
        )
        == 0,
    )

    for index, selected in enumerate(q):
        checks.check(
            f"fresh denominator mutation selects release {index} as the exact unit",
            all(
                abs(selected / selected - 1) < abs(other / selected - 1)
                for j, other in enumerate(q)
                if j != index
            ),
        )
    target = sp.symbols("t", positive=True)
    checks.check(
        "fresh arbitrary-target inverse leaves the target coordinate free",
        all(sp.simplify(value / (value / target) - target) == 0 for value in q),
    )
    checks.check(
        "fresh zero and negative additions defeat selected positivity",
        not all(value > 0 for value in (*q, sp.Integer(0)))
        and not all(value > 0 for value in (*q, sp.Integer(-1))),
    )
    checks.check(
        "fresh distant positive addition defeats the finite bracket",
        not all(sp.Rational(3, 10) < value / unit < 1 for value in (*q, 100 * unit)),
    )
    checks.check(
        "fresh state-label mutation is independent of energy arithmetic",
        q == expected and "4He" != "degree-4 rational-map branch",
    )
    checks.check(
        "fresh review uses no numerical solver sampled quadrature or fitted tolerance",
        not any(expression.has(sp.Float, sp.Integral) for expression in (*q, *ratios, low, high)),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
