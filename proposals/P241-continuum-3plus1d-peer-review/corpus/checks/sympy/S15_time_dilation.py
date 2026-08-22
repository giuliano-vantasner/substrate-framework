"""P241 audit oracle — Time dilation (35)-(36): omega = omega0*sqrt(-g00).

Standalone module: python3 S15_time_dilation.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_time_dilation_static() -> dict[str, object]:
    """Time dilation (36): omega_lab = omega_proper*sqrt(-g00) = 1/sqrt(nbar)."""
    nbar = sp.Symbol("nbar", positive=True)
    g00 = -1 / nbar
    rate = sp.sqrt(-g00)
    ok = sp.simplify(rate - 1 / sp.sqrt(nbar)) == 0
    slower = rate.subs(nbar, sp.Rational(9, 4)) < 1
    return _check(
        "time_dilation_static",
        "P241-S15 (35)-(36)",
        bool(ok and slower),
        "d(tau)/dt = sqrt(-g00) = 1/sqrt(nbar) < 1 for nbar > 1: clocks in "
        "elevated-index regions run slow relative to infinity, as displayed.",
    )

if __name__ == "__main__":
    result = check_time_dilation_static()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
