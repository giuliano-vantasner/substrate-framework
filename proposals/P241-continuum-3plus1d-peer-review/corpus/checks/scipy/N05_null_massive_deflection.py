"""P241 numerical oracle N05 — null vs massive deflection ratio (claim S19).

Standalone module: python3 N05_null_massive_deflection.py

Section 7 asserts massless rays follow "the same acceleration law" as
massive lumps. The exact SymPy audit (S19 module) derives, in the
isotropic metric g00 = -1/nbar, g_ij = nbar delta_ij:

    massive (slow-limit) law:   a = +c0^2 grad(nbar) / (2 nbar^3)
    null-ray law (Fermat):      a = +c0^2 grad(nbar) / nbar^3

whose leading transverse-acceleration ratio is exactly 2. This module
integrates those two closed-form laws across a weak bump
nbar = 1 + A exp(-(r/ell)^2) (same straight-ish geometry, unit speed),
measures both asymptotic deflection angles, and Richardson-extrapolates
their ratio to A -> 0. Pass criteria:

  (i)   extrapolated angle_null / angle_massive = 2 within 2%;
  (ii)  both angles share sign (deflection toward increasing nbar,
        opposite to displayed Eq. (43)'s printed sign, see S18);
  (iii) no mass parameter appears anywhere in either law (universality
        across M0 holds; the failed scope is masslessness only).
"""

from __future__ import annotations

import json

import numpy as np
from scipy.integrate import solve_ivp


def make_index(a_amp: float, ell: float = 1.0):
    def n(pos):
        return 1.0 + a_amp * np.exp(-(pos[0] ** 2 + pos[1] ** 2) / ell**2)

    def grad_n(pos):
        e = a_amp * np.exp(-(pos[0] ** 2 + pos[1] ** 2) / ell**2)
        return np.array([-2 * pos[0] * e / ell**2, -2 * pos[1] * e / ell**2])

    return n, grad_n


def integrate(kind: str, a_amp: float, b: float = 0.6):
    """Deflection angle for one of the two exact reduced laws."""
    n, grad_n = make_index(a_amp)
    denom_half = 0.5 if kind == "massive" else 1.0

    def rhs(_t, y):
        pos, vel = y[:2], y[2:]
        acc = denom_half * grad_n(pos) / n(pos) ** 3
        return np.concatenate([vel, acc])

    def crossed(_t, y):
        return y[0] - 20.0

    crossed.terminal = True
    crossed.direction = 1.0
    y0 = np.array([-20.0, b, 1.0, 0.0])
    sol = solve_ivp(rhs, (0.0, 200.0), y0, method="DOP853",
                    rtol=1e-11, atol=1e-13, events=crossed)
    assert sol.success and sol.t_events[0].size > 0, kind
    yf = sol.y_events[0][0]
    return float(np.arctan2(yf[3], yf[2]))


def main() -> dict[str, object]:
    ratios = []
    angles = []
    for a_amp in (0.08, 0.04):
        tn = integrate("null", a_amp)
        tm = integrate("massive", a_amp)
        ratios.append(tn / tm)
        angles.append((tn, tm))
    # Richardson: ratio(A) = 2 + c*A + ... ; extrapolate with A/2 grid
    r_extrap = 2.0 * ratios[-1] - ratios[-2]

    ok = abs(r_extrap - 2.0) < 0.02 and angles[-1][0] * angles[-1][1] > 0
    detail = (
        f"Angle ratios {np.round(ratios, 6).tolist()} at A = 0.08, 0.04; "
        f"Richardson-extrapolated ratio {r_extrap:.6f} ~= 2: massless probes "
        "curve exactly twice as much per unit time, refuting the Section-7 "
        "'same acceleration law' sentence while supporting universality "
        "across massive lumps (no M0 enters either law). Both deflect toward "
        "increasing nbar (sign consistent with prose, opposite to displayed "
        "Eq. (43))."
    )
    return {"name": "scipy_null_massive_ratio", "claim": "P241-S19",
            "passed": bool(ok), "detail": detail}


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
