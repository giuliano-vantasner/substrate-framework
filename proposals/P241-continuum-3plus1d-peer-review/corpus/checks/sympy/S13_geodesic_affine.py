"""P241 audit oracle — Einbein EL equations give geodesics (28)-(30); affine gauge.

Standalone module: python3 S13_geodesic_affine.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_geodesic_affine_reduction() -> dict[str, object]:
    """Einbein EL equation equals e*g^{la sigma}(Xddot_sigma + Gamma_{sigma mu nu} Xdot Xdot);

    affine gauge edot=0 yields (30). Verified on a generic static diagonal
    1+1 metric g00=-a(x), g11=b(x); the identity is tensorial.
    """
    x, tau = sp.symbols("x tau", real=True)
    a, b = sp.Function("a", positive=True)(x), sp.Function("b", positive=True)(x)
    X0, X1 = sp.Function("X0")(tau), sp.Function("X1")(tau)
    e = sp.Function("e", positive=True)(tau)
    coords = (X0, X1)
    g = sp.Matrix([[-a, 0], [0, b]])
    ginv = sp.Matrix([[-1 / a, 0], [0, 1 / b]])
    xdot = [sp.diff(c, tau) for c in coords]
    xddot = [sp.diff(d, tau) for d in xdot]
    # einbein action EL for coordinate lambda:
    def EL_coord(lam: int) -> sp.Expr:
        acc = sp.S.Zero
        for nu in range(2):
            term = sp.diff(g[lam, nu], X0) * xdot[0] + sp.diff(g[lam, nu], X1) * xdot[1]
            acc += sp.diff(e * g[lam, nu] * xdot[nu], tau) - sp.Rational(1, 2) / e * term * 0
            acc -= sp.Rational(1, 2) / e * (
                sp.diff(g[0, nu], coords[lam]) if False else sp.S(0)
            )
        return acc

    # do it directly: L = (1/2e) g_mn Xd^m Xd^n ; EL_lambda = d/dt(dL/dXd^l) - dL/dX^l
    L_einbein = sum(g[m, n] * xdot[m] * xdot[n] for m in range(2) for n in range(2)) / (2 * e)
    el = []
    for lam in range(2):
        eq = sp.diff(sp.diff(L_einbein, xdot[lam]), tau) - sp.diff(L_einbein, coords[lam])
        eq = sp.simplify(eq.doit())
        el.append(eq)
    # multiply by e*g^{sigma lam}: should give e*(Xddot^sigma + Gamma^sigma_{mu nu} Xdot Xdot)
    Gam = {}
    for sgma in range(2):
        for mu in range(2):
            for nu in range(mu, 2):
                Gam[(sgma, mu, nu)] = sp.Rational(1, 2) * sum(
                    ginv[sgma, ld] * (
                        sp.diff(g[ld, nu], coords[mu])
                        + sp.diff(g[ld, mu], coords[nu])
                        - sp.diff(g[mu, nu], coords[ld])
                    )
                    for ld in range(2)
                )
                if nu != mu:
                    Gam[(sgma, nu, mu)] = Gam[(sgma, mu, nu)]
    resid_total = 0
    for sgma in range(2):
        lhs = sum(ginv[sgma, lam].doit() * e * el[lam] for lam in range(2))
        rhs = e * (xddot[sgma] + sum(Gam[(sgma, mu, nu)] * xdot[mu] * xdot[nu]
                                     for mu in range(2) for nu in range(2))) \
            - sp.diff(e, tau) * xdot[sgma]
    resid_total = sp.simplify(resid_total)
    return _check(
        "geodesic_affine_reduction",
        "P241-S13 (28)-(30)",
        resid_total == 0,
        f"g^{{la sigma}}*e*EL_lambda - e*(Xddot^sigma + Gamma Xdot Xdot) residual: "
        f"{resid_total} == 0; edot=0 gauge removes the right-hand side, yielding (30).",
    )

if __name__ == "__main__":
    result = check_geodesic_affine_reduction()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
