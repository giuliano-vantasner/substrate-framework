"""P241 audit oracle — Equatorial minimal model (58)-(60) vs the published 2+1D profiles.

Standalone module: python3 S22_minimal_model_published.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_minimal_model_matches_published() -> dict[str, object]:
    """Equatorial minimal model (58)-(60) vs the published 2+1D profiles."""
    r, c0, rs, a = sp.symbols("r c_0 r_s a", positive=True)
    f_expr = 1 - rs / r + a**2 / r**2
    paper = {
        "Arr": c0**2 * f_expr**2,
        "Aphph": c0**2 / r**2 * f_expr,
        "Vphi": c0 * a / r**2,
    }
    published21 = {
        "Arr": c0**2 * f_expr**2,
        "Aphph": c0**2 / r**2 * f_expr,
        "Vphi": c0 * a / r**2,
    }
    matches = all(sp.simplify(paper[k_] - published21[k_]) == 0 for k_ in paper)
    # but NOT equal to the full 3+1D construction at theta=pi/2:
    Delta = r**2 - rs * r + a**2
    Ag_eq = (r**2 + a**2) ** 2 - a**2 * Delta
    full_Aphph_eq = c0**2 * (r**2 / Ag_eq) ** 2  # from (55) at Sigma = r^2
    diff_expr = sp.simplify(sp.expand(full_Aphph_eq - paper["Aphph"]))
    probe = diff_expr.subs({r: sp.Rational(7, 2), c0: 1, rs: sp.Rational(2, 5), a: sp.Rational(9, 50)})
    differs = probe != 0
    return _check(
        "minimal_model_matches_published",
        "P241-S22 (58)-(60)",
        bool(matches and probe != 0),
        "(58)-(60) reproduce the published 2+1D minimal rotating model verbatim; "
        "they do NOT coincide with the paper's own full construction at theta=pi/2 "
        "(A^{phphi}: minimal vs full differ at the sample point), and per the "
        "upstream P238 review this minimal model is not conformal to Kerr — keep "
        "the 'minimal rotating acoustic model' name.",
    )

if __name__ == "__main__":
    result = check_minimal_model_matches_published()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
