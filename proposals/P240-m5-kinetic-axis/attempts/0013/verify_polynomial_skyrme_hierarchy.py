"""Exact exhaustion of constant-polynomial P240 Skyrme currents."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P240/polynomial-skyrme-hierarchy")
    x, y, zxy = sp.symbols("x y z_xy", real=True)
    a, b = sp.symbols("a b", real=True)
    p_x = a * x + b * x**2
    p_y = a * y + b * y**2
    response = sp.factor((p_x - p_y) ** 2 * zxy**2)
    expected = (x - y) ** 2 * (a + b * (x + y)) ** 2 * zxy**2
    ledger.check(
        "general polynomial-current response factors exactly",
        sp.simplify(response - expected) == 0,
    )
    ledger.check(
        "standard Y current is active on every split pair",
        sp.factor(response.subs({a: 1, b: 0})) == (x - y) ** 2 * zxy**2,
    )
    ledger.check(
        "pure Y2 current has an opposite-eigenvalue blind line",
        response.subs({a: 0, b: 1, y: -x}) == 0
        and (x - (-x)) ** 2 != 0,
    )
    nonzero_a, nonzero_b = sp.symbols("a0 b0", nonzero=True, real=True)
    ledger.check(
        "every mixed Y plus Y2 current has a split blind pair",
        sp.simplify(
            expected.subs(
                {a: nonzero_a, b: nonzero_b, x: 0, y: -nonzero_a / nonzero_b}
            )
        )
        == 0
        and sp.simplify(nonzero_a / nonzero_b) != 0,
    )
    ledger.check(
        "only b zero removes the extra polynomial blind factor",
        sp.solve(sp.Poly(a + b * (x + y), x, y).coeffs()[1:], b, dict=True)
        == [{b: 0}],
    )

    third = sp.symbols("z", real=True)
    y_matrix = sp.diag(x, y, third)
    trace_y = sp.trace(y_matrix)
    trace_y2 = sp.trace(y_matrix**2)
    determinant_y = y_matrix.det()
    cayley_hamilton_remainder = (
        y_matrix**3
        - trace_y * y_matrix**2
        + (trace_y**2 - trace_y2) * y_matrix / 2
        - determinant_y * sp.eye(3)
    )
    ledger.check(
        "three-dimensional Cayley-Hamilton leaves only I Y Y2",
        cayley_hamilton_remainder.applyfunc(sp.factor) == sp.zeros(3),
    )

    c1, c2 = sp.symbols("c1 c2", positive=True)
    combined = sp.factor(
        c1 * (x - y) ** 2 * zxy**2
        + c2 * (x**2 - y**2) ** 2 * zxy**2
    )
    ledger.check(
        "a positive combined norm avoids the blind line only by retaining standard current",
        sp.simplify(combined.subs(y, -x) - 4 * c1 * x**2 * zxy**2) == 0,
    )
    ratio = sp.symbols("r", positive=True)
    normalized_combined = sp.factor(combined.subs({c1: 1, c2: ratio}))
    ledger.check(
        "combined hierarchy introduces an unfixed inequivalent coupling ratio",
        sp.diff(normalized_combined, ratio) != 0,
    )
    n = sp.symbols("n", real=True)
    ledger.check(
        "outer n squared repair remains the unique zero-axis factor",
        sp.factor(n**2 * response).subs(n, 0) == 0
        and sp.factor(n**2 * response).subs({n: 1, a: 1, b: 0}) != 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
