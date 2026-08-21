"""P241 audit oracle — Counterexample: massless rays do NOT follow the massive acceleration law.

Standalone module: python3 S19_massless_factor_two.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_massless_factor_two() -> dict[str, object]:
    """Counterexample to 'the same acceleration law ... massless'.

    Weak-field isotropic index n = 1 + eps*y^2/k^2: massive-lump transverse
    acceleration per unit time has leading coefficient c0^2*phi'(y0)/2, while
    the null-ray law (Fermat curvature kappa = grad_perp(log n), speed
    c0/n) gives c0^2*phi'(y0). Ratio exactly 2 at leading order.
    """
    y, eps, k, c0 = sp.symbols("y epsilon k c_0", positive=True)
    phi = eps * y**2 / k**2
    n = 1 + phi
    y0 = sp.Symbol("y_0", positive=True)
    # massive: c0^2 * d(n)/dy / (2 n^3) evaluated at y0:
    a_massive = sp.simplify(c0**2 * sp.diff(n, y) / (2 * n**3)).subs(y, y0)
    coeff_massive = sp.limit(a_massive / eps, eps, 0)
    # null: curvature per length = d(log n)/dy; per time multiply by (dx/dt)^2 = c0^2/n^2:
    kappa = sp.diff(sp.log(n), y).subs(y, y0)
    a_null = sp.simplify(kappa * c0**2 / n.subs(y, y0) ** 2)
    coeff_null = sp.limit(a_null / eps, eps, 0)
    ratio = sp.simplify(coeff_null / coeff_massive)
    return _check(
        "massless_factor_two_counterexample",
        "P241-S19 (Section 7 equivalence claim)",
        ratio == 2,
        f"Leading transverse-acceleration coefficients: massive {coeff_massive}, "
        f"null {coeff_null}, ratio {ratio}. Null rays curve exactly twice as much "
        "per unit time in the weak-field limit; 'every energy concentration falls "
        "in exactly the same way' is false. Supported scope: universality across "
        "massive lumps (M0-independent law); massless probes follow the doubled "
        "null-cone deflection (analogue of the GR light-bending factor).",
    )

if __name__ == "__main__":
    result = check_massless_factor_two()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
