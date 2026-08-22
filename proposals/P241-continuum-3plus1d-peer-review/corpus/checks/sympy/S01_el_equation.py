"""P241 audit oracle — Euler-Lagrange equation (5) from Lagrangian density (2).

Standalone module: python3 S01_el_equation.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_el_equation() -> dict[str, object]:
    """Euler-Lagrange equation (5) from Lagrangian density (2)."""
    x, t = sp.symbols("x t", real=True)
    u = sp.Function("u")
    rho = sp.Function("rho", positive=True)(x, t)
    V = sp.Function("V", positive=True)(x, t)
    Th = sp.Function("Theta", positive=True)(x, t)
    Uf = sp.Function("U")
    Dt_u = sp.Derivative(u(x, t), t) + V * sp.Derivative(u(x, t), x)
    L_full = rho / 2 * Dt_u**2 - Th / 2 * sp.Derivative(u(x, t), x) ** 2 - Uf(u(x, t))
    EL = (
        sp.diff(L_full, sp.Derivative(u(x, t), t)).diff(t)
        + sp.diff(L_full, sp.Derivative(u(x, t), x)).diff(x)
        - L_full.diff(u(x, t))
    ).doit()
    EL_sub = sp.expand(EL)
    Dt_paper = sp.diff(u(x, t), t) + V * sp.diff(u(x, t), x)
    paper5 = sp.expand(
        sp.diff(rho * Dt_paper, t)
        + sp.diff(rho * V * Dt_paper - Th * sp.diff(u(x, t), x), x)
        + Uf(u(x, t)).diff(u(x, t))
    )
    residual = sp.simplify(EL_sub - paper5)
    return _check(
        "el_equation_exact",
        "P241-S01 (1)-(5)",
        residual == 0,
        f"EL residual vs displayed equation (5): {residual} == 0.",
    )

if __name__ == "__main__":
    result = check_el_equation()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
