"""P241 audit oracle — Counterexample to displayed Newtonian limit (43): sign error.

Standalone module: python3 S18_newtonian_limit_sign.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_newtonian_limit_sign() -> dict[str, object]:
    """Newtonian-limit counterexample to displayed equation (43).

    Geodesics of g00=-1/n(x), g_ij=n(x)*delta_ij give
    d^2X/dt^2 = +c0^2/(2n^3) grad(n) = +(c0^2/2)*grad(log n)/n^2,
    directed toward INCREASING index (as the manuscript's own prose states),
    while displayed (43) carries the opposite sign. Concrete probe:
    n(x) = 1 + k*x.
    """
    x, c0, k = sp.symbols("x c_0 k", positive=True)
    n_expr = 1 + k * x
    g = sp.Matrix([[-1 / n_expr, 0], [0, n_expr]])
    ginv = sp.Matrix([[-n_expr, 0], [0, 1 / n_expr]])
    Gamma100 = sp.simplify(sp.Rational(1, 2) * ginv[1, 1] * (-sp.diff(g[0, 0], x)))
    acc_true = sp.simplify(-c0**2 * Gamma100)
    paper43 = sp.simplify(-c0**2 / 2 * sp.diff(sp.log(n_expr), x))
    resid = sp.simplify(acc_true - paper43)
    vals = {x: sp.Rational(3, 10), c0: sp.Rational(297, 100), k: sp.Rational(1, 4)}
    true_val = float(acc_true.subs(vals))
    paper_val = float(paper43.subs(vals))
    exact_law = sp.simplify(acc_true - c0**2 * k / (2 * n_expr**3)) == 0
    mismatch = resid != 0 and true_val > 0 and paper_val < 0 and exact_law
    return _check(
        "newtonian_limit_sign_counterexample",
        "P241-S18 (43)",
        bool(mismatch),
        f"Geodesic limit d2X/dt2 = c0^2*k/(2*n^3) (exact law confirmed: {exact_law}); "
        f"at n=11/10, dn/dx=1/4 the geodesic gives {true_val:.6g} > 0 while displayed "
        f"(43) gives {paper_val:.6g} < 0. The displayed sign contradicts both the "
        "manuscript's prose and its own metric; the exact law also carries a 1/n^2 "
        "factor beyond grad(log n). Mass-independence of the law IS supported.",
    )

if __name__ == "__main__":
    result = check_newtonian_limit_sign()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
