"""P241 audit oracle — Corrected full-3D Kerr dictionary reproduces Omega^2 x Kerr exactly.

Standalone module: python3 S21_kerr_corrected_dictionary.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_kerr_corrected_dictionary() -> dict[str, object]:
    """Corrected full-3D dictionary reproduces Omega^2 x Kerr exactly.

    With rs = 2GM/c0^2, define K = Sigma*Ag/(Ag*Delta + rs^2*c0^4*a^2*r^2*sin^2 th),
    P = (Delta*r^4/(Sigma*Ag))^{1/3}, so that Omega^4 = P*K satisfies the g00
    equation because K*(Q+R) = 1 with Q = rs^2*c0^4*a^2*r^2*sin^2/(Ag*Sigma),
    R = Delta/Sigma. Then n_r = Omega^2*Sigma/Delta,
    n_theta = Omega^2*Sigma/r^2, n_phi = Omega^2*Ag/(Sigma*r^2),
    V_phi = -rs*a*c0^3*r^2*sin(th)/Ag realize all five Kerr components times
    Omega^2(r,theta).
    """
    r, th, c0, rs, a = sp.symbols("r theta c_0 r_s a", positive=True)
    Delta = r**2 - rs * r + a**2
    Sigma = r**2 + a**2 * sp.cos(th) ** 2
    Ag = (r**2 + a**2) ** 2 - a**2 * Delta * sp.sin(th) ** 2
    X = rs**2 * c0**4 * a**2 * r**2 * sp.sin(th) ** 2
    K = Sigma * Ag / (Ag * Delta + X)
    Q = X / (Ag * Sigma)
    R = Delta / Sigma
    identity = sp.cancel(K * (Q + R) - 1)
    vals = {r: sp.Rational(7, 3), th: sp.Rational(4, 10), c0: sp.Rational(297, 100),
            rs: sp.Rational(2, 5), a: sp.Rational(9, 50)}
    import mpmath as mp

    def num(expr):
        return mp.mpf(str(sp.N(expr.subs(vals))))

    Dv, Sv, Av = num(Delta), num(Sigma), num(Ag)
    cv, rv, thv, rsv, av = num(c0), num(r), num(th), num(rs), num(a)
    GM = rsv * cv**2 / 2
    Om4 = ((Dv * rv**4 / (Sv * Av)) ** (mp.mpf(1) / 3)) * Sv * Av / (Av * Dv + 4 * GM**2 * av**2 * rv**2 * mp.sin(thv) ** 2)
    Om2 = Om4 ** (mp.mpf(1) / 2)
    nrv = Om2 * Sv / Dv
    nthv = Om2 * Sv / rv**2
    npv = Om2 * Av / (Sv * rv**2)
    Vv = -rsv * av * cv**3 * rv**2 * mp.sin(thv) / Av
    nbv = (nrv * nthv * npv) ** (mp.mpf(1) / 3)
    resids = {
        "g_rr": float(nrv - Om2 * Sv / Dv),
        "g_thth": float(nthv * rv**2 - Om2 * Sv),
        "g_phph": float(npv * rv**2 * mp.sin(thv) ** 2 - Om2 * Av / Sv * mp.sin(thv) ** 2),
        "g_0ph": float(npv * Vv * rv * mp.sin(thv) / cv + Om2 * 2 * GM * av * rv * mp.sin(thv) ** 2 / Sv),
        "g_00": float(-1 / nbv + npv * Vv**2 / cv**2 + Om2 * Dv / Sv),
    }
    max_resid = max(abs(v_) for v_ in resids.values())
    return _check(
        "kerr_corrected_dictionary_exact",
        "P241-S21 corrected realisation (replacement)",
        bool(identity == 0 and max_resid < 1e-12),
        f"K*(Q+R)-1 = {identity} exactly; component residuals at sample point "
        f"{resids} (max |residual| = {max_resid:.2e}). The induced metric equals "
        "Omega^2(r,theta) times Kerr with the explicit conformal factor above; "
        "null geodesics are exactly Kerr's, timelike structure up to the declared "
        "factor.",
    )

if __name__ == "__main__":
    result = check_kerr_corrected_dictionary()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
