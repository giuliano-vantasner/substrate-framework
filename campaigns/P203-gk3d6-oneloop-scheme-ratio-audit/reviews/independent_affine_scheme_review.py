#!/usr/bin/env python3
"""Independent raw-SymPy review of GK3D6's affine scheme claims."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P203-INDEPENDENT-AFFINE-SCHEME")
    own_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported = {
        node.module
        for node in ast.walk(own_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "review imports no kinetic scale trace or radial claim API",
        imported.isdisjoint(
            {
                "substrate_framework.kinetic_scale_matching",
                "substrate_framework.vacuum_polarization",
                "substrate_framework.charge_traces",
                "substrate_framework.radial_qball",
            }
        ),
    )

    K = 8 * sp.pi**2
    bi, bj = sp.symbols("b_i b_j", positive=True)
    zi, zj = sp.symbols("z_i z_j", real=True)
    L, s = sp.symbols("L s", real=True)
    Zi = zi + bi * (L - s) / K
    Zj = zj + bj * (L - s) / K
    R = sp.cancel(Zj / Zi)
    dR = sp.factor(sp.diff(R, s))
    checks.check(
        "fresh quotient differentiation retains affine boundaries",
        sp.simplify(dR - (bi * zj - bj * zi) / (K * Zi**2)) == 0,
    )
    checks.check(
        "fresh cancellation condition is proportional boundary data",
        sp.factor(sp.together(dR).as_numer_denom()[0])
        == K * (bi * zj - bj * zi),
    )
    alpha = sp.Symbol("alpha", real=True)
    checks.check(
        "fresh proportional boundary branch gives inverse weight ratio",
        sp.simplify(R.subs({zi: alpha * bi, zj: alpha * bj}) - bj / bi) == 0,
    )
    checks.check(
        "fresh zero boundary branch is a specialization",
        sp.simplify(R.subs({zi: 0, zj: 0}) - bj / bi) == 0,
    )
    checks.check(
        "fresh one-boundary mutation breaks cancellation",
        sp.diff(R.subs({zi: 1, zj: 0}), s) != 0,
    )

    Li, Lj, si, sj = sp.symbols("L_i L_j s_i s_j", real=True)
    Zi2 = zi + bi * (Li - si) / K
    Zj2 = zj + bj * (Lj - sj) / K
    residual = sp.factor(bi * Zj2 - bj * Zi2)
    checks.check(
        "fresh factorwise residual contains boundary and log differences",
        sp.simplify(
            residual
            - (
                bi * zj
                - bj * zi
                + bi * bj * ((Lj - sj) - (Li - si)) / K
            )
        )
        == 0,
    )
    checks.check(
        "fresh factor-log mutation breaks the source ratio",
        sp.simplify(
            residual.subs({zi: 0, zj: 0, Li: L, Lj: L + 1, si: s, sj: s})
            - bi * bj / K
        )
        == 0,
    )
    checks.check(
        "fresh factor-scale mutation breaks the source ratio",
        sp.simplify(
            residual.subs({zi: 0, zj: 0, Li: L, Lj: L, si: s, sj: s + 1})
            + bi * bj / K
        )
        == 0,
    )

    ell0, ell1, k0, k1, rho = sp.symbols(
        "ell_0 ell_1 K_0 K_1 rho", positive=True
    )
    scale_log = sp.log((ell1 / ell0) / (k1 / k0))
    checks.check(
        "fresh common length rescaling preserves the logarithm",
        sp.simplify(
            scale_log.subs({ell0: rho * ell0, ell1: rho * ell1}) - scale_log
        )
        == 0,
    )
    checks.check(
        "fresh one-conversion mutation changes the logarithm",
        sp.simplify(scale_log.subs(k1, rho * k1) - scale_log) == -sp.log(rho),
    )

    Zc = bi * (L - s) / K
    Z1 = bi * L / K
    gc = 1 / Zc
    g1 = 1 / Z1
    checks.check(
        "fresh normalization and inverse-coordinate shifts differ",
        sp.simplify((Zc - Z1) / Z1) == -s / L
        and sp.simplify((gc - g1) / g1) == s / (L - s),
    )
    checks.check(
        "fresh zero and sign domain counterexamples remain",
        Zc.subs(s, L) == 0 and Zc.subs(s, L + 1).is_negative is True,
    )

    t2 = sp.Integer(2)
    ty = sp.Rational(10, 3)
    trace_angle = sp.simplify(t2 / (t2 + ty))
    g2, gy = sp.symbols("g_2 g_Y", positive=True)
    coupling_angle = sp.simplify(gy**2 / (g2**2 + gy**2))
    checks.check("fresh trace arithmetic is three eighths", trace_angle == sp.Rational(3, 8))
    checks.check(
        "fresh independent couplings refute an automatic physical angle",
        coupling_angle.subs({g2: 1, gy: 1}) == sp.Rational(1, 2)
        and trace_angle != sp.Rational(1, 2),
    )
    rho_y = sp.Symbol("rho_Y", positive=True)
    covariant = sp.simplify(
        (sp.sqrt(3) / rho_y) ** 2
        / (sp.sqrt(5) ** 2 + (sp.sqrt(3) / rho_y) ** 2)
    )
    checks.check(
        "fresh Abelian normalization mutation moves the coordinate",
        covariant.subs(rho_y, 1) == sp.Rational(3, 8)
        and covariant.subs(rho_y, 2) == sp.Rational(3, 23),
    )

    numpy_imports = [
        node
        for node in ast.walk(own_tree)
        if (
            isinstance(node, ast.Import)
            and any(alias.name == "numpy" for alias in node.names)
        )
        or (isinstance(node, ast.ImportFrom) and node.module == "numpy")
    ]
    checks.check("independent review has no NumPy compatibility surface", not numpy_imports)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
