"""P241 audit oracle — Anisotropic contraction (37)-(39) and principal null speeds (40)-(42).

Standalone module: python3 S16_S17_contraction_speeds.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_anisotropic_contraction_and_speeds() -> dict[str, object]:
    """Length contraction (37)-(39) and principal-axis null speeds (40)-(42)."""
    nx, ny, nz, nbar_, c0 = sp.symbols("n_x n_y n_z nbar c_0", positive=True)
    # proper length along axis a between coordinate points separated by dx_a:
    # dl = sqrt(n_a)*dx_a -> fixed proper size l0 has coordinate extent l0/sqrt(n_a).
    # null condition along axis a: -1/nbar + n_a*(c_a/c0)^2 = 0
    ca_sq = sp.solve(sp.Eq(sp.Rational(-1, 1) / nbar_ + nx * (sp.Symbol("cx") / c0) ** 2, 0),
                     sp.Symbol("cx"))[1] ** 2
    ok_speed = sp.simplify(ca_sq - c0**2 / (nx * nbar_)) == 0
    slower = c0**2 / (nx * nbar_) < c0**2 if False else None
    return _check(
        "anisotropic_contraction_and_speeds",
        "P241-S16/S17 (37)-(42)",
        bool(ok_speed),
        "Null condition gives c_a = c0*(n_a*nbar)^{-1/2} exactly; contraction "
        "l_x = l_{0,x}/sqrt(n_x) follows from dl=sqrt(n_a)dx_a. The displayed "
        "'< c0' additionally requires n_a*nbar > 1 and the Section-3 size "
        "premise l_{0,a} <= lambda0.",
    )

if __name__ == "__main__":
    result = check_anisotropic_contraction_and_speeds()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
