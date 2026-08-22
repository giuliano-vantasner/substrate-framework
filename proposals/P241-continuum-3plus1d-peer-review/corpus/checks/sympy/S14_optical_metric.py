"""P241 audit oracle — Optical components (31)-(34) coincide with (23)-(25).

Standalone module: python3 S14_optical_metric.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_optical_metric_equivalence() -> dict[str, object]:
    """Optical components (31)-(34) coincide with (23)-(25)."""
    c0 = sp.Symbol("c_0", positive=True)
    v1, v2, v3 = sp.symbols("V^1 V^2 V^3", real=True)
    a1, a2, a3 = sp.symbols("a1 a2 a3", positive=True)
    nbar_a = c0 / (a1 * a2 * a3) ** sp.Rational(1, 6)
    g00_opt = -1 / nbar_a + sum(vj**2 * (c0 * aj ** -sp.Rational(1, 2)) / c0**2
                                for vj, aj in zip((v1, v2, v3), (a1, a2, a3)))
    g00_can = (-(a1 * a2 * a3) ** sp.Rational(1, 6) / c0
               + sum(vj**2 / (sp.sqrt(aj) * c0)
                     for vj, aj in zip((v1, v2, v3), (a1, a2, a3))))
    vals = {a1: sp.Rational(4), a2: sp.Rational(9, 4), a3: sp.Rational(2, 3),
            v1: sp.Rational(1, 3), v2: -sp.Rational(2, 5), v3: sp.Rational(7, 2),
            c0: sp.Rational(297, 100)}
    resid = sp.simplify(g00_opt.subs(vals) - g00_can.subs(vals))
    # nbar = (det n)^{1/3}:
    nbar_detn = ((c0 * a1 ** -sp.Rational(1, 2)) * (c0 * a2 ** -sp.Rational(1, 2))
                 * (c0 * a3 ** -sp.Rational(1, 2))) ** sp.Rational(1, 3)
    resid2 = sp.simplify(nbar_detn.subs(vals) - nbar_a.subs(vals))
    return _check(
        "optical_metric_equivalence",
        "P241-S14 (31)-(34)",
        resid == 0 and resid2 == 0,
        f"g00 optical vs canonical residual {resid}; "
        f"nbar==(det n)^{{1/3}} residual {resid2}.",
    )

if __name__ == "__main__":
    result = check_optical_metric_equivalence()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
