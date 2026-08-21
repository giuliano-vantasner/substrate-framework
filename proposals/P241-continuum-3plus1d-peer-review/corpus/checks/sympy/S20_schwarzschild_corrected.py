"""P241 audit oracle — Corrected Schwarzschild realization up to declared conformal factor.

Standalone module: python3 S20_schwarzschild_corrected.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_schwarzschild_corrected_profiles() -> dict[str, object]:
    """Corrected Schwarzschild realization: Omega^2=f^{-1/3},
    n_r=f^{-4/3}, n_theta=n_phi=f^{-1/3} reproduce every component of
    Omega^2 x (Schwarzschild, length coordinates) exactly."""
    f = sp.Symbol("f", positive=True)
    Om2 = f ** sp.Rational(-1, 3)
    n_r = f ** sp.Rational(-4, 3)
    n_t = f ** sp.Rational(-1, 3)
    nbar = (n_r * n_t * n_t) ** sp.Rational(1, 3)
    eqs = {
        "g_rr": sp.simplify(n_r - Om2 / f),
        "g_thth": sp.simplify(n_t - Om2),           # after dividing by r^2
        "g_00": sp.simplify(-1 / nbar + Om2 * f),
    }
    resid_total = sum(abs(e) for e in eqs.values())
    return _check(
        "schwarzschild_corrected_profiles_exact",
        "P241-S20 (44)-(47) replacement",
        resid_total == 0,
        "With Omega^2 = f^(-1/3), n_r = f^(-4/3), n_t = n_phi = f^(-1/3) the "
        "induced metric equals Omega^2 times Schwarzschild (length coords) "
        "component-by-component: residual {0}. Physical eigenvalues "
        "lambda_r = c0^2*f^(8/3), lambda_t = lambda_phi = c0^2*f^(2/3); the "
        "realization is exact up to the declared conformal factor.".format(resid_total),
    )

if __name__ == "__main__":
    result = check_schwarzschild_corrected_profiles()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
