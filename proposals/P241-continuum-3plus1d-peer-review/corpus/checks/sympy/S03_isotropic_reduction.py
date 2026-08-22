"""P241 audit oracle — Isotropic reduction (6)-(10) to NLKG (8) with c0^2=Theta0/rho0.

Standalone module: python3 S03_isotropic_reduction.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_isotropic_reduction() -> dict[str, object]:
    """Isotropic reduction (6)-(7) to NLKG (8) with c0^2 = Theta0/rho0."""
    X, Y, Z, T = sp.symbols("X Y Z T", real=True)
    rho0, c0, M0, hbar, lam4 = sp.symbols("rho0 c0 M_0 hbar lambda", positive=True)
    uu = sp.Function("uu")
    lap = sum(sp.Derivative(uu(T, X, Y, Z), s, 2) for s in (X, Y, Z))
    w0sq = (M0 * c0**2 / hbar) ** 2
    el7_over_rho0 = (
        sp.Derivative(uu(T, X, Y, Z), T, 2)
        - c0**2 * lap
        + c0**2 * w0sq * uu(T, X, Y, Z)
        + (lam4 / rho0) * uu(T, X, Y, Z) ** 3
    )
    eq8 = (
        sp.Rational(1) / c0**2 * sp.Derivative(uu(T, X, Y, Z), T, 2)
        - lap
        + w0sq * uu(T, X, Y, Z)
        + (lam4 / (rho0 * c0**2)) * uu(T, X, Y, Z) ** 3
    )
    residual = sp.simplify(el7_over_rho0 - eq8 * c0**2)
    return _check(
        "isotropic_reduction_exact",
        "P241-S03 (6)-(10)",
        residual == 0,
        f"EL((7))/rho0 vs c0^2*(8) residual: {residual} == 0 "
        "(quartic coefficient lam4/rho0 == c0^2*lam4/(Theta0) under Theta0=rho0*c0^2).",
    )

if __name__ == "__main__":
    result = check_isotropic_reduction()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
