"""P241 audit oracle — Compton/Einstein-de-Broglie scales (11)-(12).

Standalone module: python3 S04_compton_scales.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_compton_scales() -> dict[str, object]:
    """Compton/Einstein-de-Broglie scales (11)-(12)."""
    hbar, M0, c0 = sp.symbols("hbar M_0 c_0", positive=True)
    lam0 = hbar / (M0 * c0)
    omega0 = c0 / lam0
    ok = sp.simplify(omega0 - M0 * c0**2 / hbar) == 0
    return _check(
        "compton_scales_identity",
        "P241-S04 (11)-(12)",
        ok,
        "omega0*lambda0 = c0 exactly; omega0 = M0*c0^2/hbar confirmed. "
        "The M0 ~ rho0*c0*mu0^{-1} proportionality is supported at scaling level only; "
        "its constant is profile- and amplitude-normalization dependent.",
    )

if __name__ == "__main__":
    result = check_compton_scales()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
