"""Attempt 0007 -- multi-family quadrature exactness (G6) + final composition.

PREREGISTRATION (frozen before execution):

ROLE OF THIS ATTEMPT
  Attempts 0005/0006 established that a finite-difference radial
  discretization of the pencil agrees with route A only at its own truncation
  floor. The load-bearing independence argument upgrades to quadrature
  EXACTNESS across independent node/weight families:

G6 QUADRATURE-EXACTNESS GATE
  Implementation isolates ONE variable: the quadrature rule. The committed
  constructions (kinetic_stage2.build_cache/kinetic_functional,
  solve_radial_1d.energy_radial/Oracle) are used VERBATIM; their module-level
  gauss_grid symbol is rebound, per rung, to an alternative rule object with
  the identical return contract. Alternative family: interior Chebyshev
  second-kind nodes x_j = cos(j*pi/(n+1)) in BOTH coordinates with weights
  solved for exactness on all polynomials of degree < n (basis U_k,
  int U_k dx = (1-(-1)^(k+1))/(k+1)); radial mapping r = R*sqrt(x) with
  radial weight (R/2)*w_x/sqrt(x) so that w_r*r^2 equals (R^3/2)*sqrt(x)*w_x
  and the continuum measure 2*pi*r^2 dr dmu is reproduced exactly.
  Endpoint-free by construction (constructions divide by sqrt(x), sin(theta)).
  Gates (preregistered before any B' number exists):
    max_ij |K_ij^B' - K_ij^A| / max(1, max|K^A|) <= 1e-13 for K in {H, M};
    pencil |omega_B' - omega_A| / omega_A <= 1e-9 over kept modes;
    delta-E(B') within 1e-6 relative of attempt 0004's 72.58859646;
    energy transfer |E_B' - E_committed|/E <= 1e-9 (rule exactness makes the
    energy agree far tighter than the old FD-style 5 percent gate).
  Failure would demonstrate non-polynomial density content and revert the
  campaign to convergence-floor certification with the mechanism named.

FINAL COMPOSITION (same artifact)
  final-certified-result.json combines gates, the zero-point shift from both
  families, and the budget reference from attempt 0004.
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
for p in (
    "campaigns/P243-clock-sourced-induced-coupling/attempts/0008",
    "proposals/P240-m5-kinetic-axis/attempts/0041",
    "proposals/P244-clock-full-band-spectrum/attempts/0002",
    "proposals/P244-clock-full-band-spectrum/attempts/0003",
):
    sys.path.insert(0, str(REPO / p))

import cpu_energy  # noqa: E402
import kinetic_stage2  # noqa: E402
import solve_radial_1d  # noqa: E402
from route_a_corrected import corrected_kinetic_hessian  # noqa: E402
from route_final import pencil_float64  # noqa: E402
from kinetic_stage2 import build_cache  # noqa: E402
from solve_radial_1d import Oracle  # noqa: E402

torch.set_num_threads(1)

DTYPE = torch.float64
RADIUS = 12.0
ORDER = 16
E_COMMITTED = 55.10418278043526


def interior_cheb_rule(n: int):
    """Interior second-kind Chebyshev nodes on [-1,1]; weights solved for
    polynomial exactness of degree < n."""
    j = np.arange(1, n + 1)
    x = np.cos(j * math.pi / (n + 1))
    V = np.zeros((n, n))
    V[:, 0] = 1.0
    if n > 1:
        V[:, 1] = 2.0 * x
    for k in range(2, n):
        V[:, k] = 2.0 * x * V[:, k - 1] - V[:, k - 2]
    rhs = np.array([(1.0 - (-1.0)**(k + 1)) / (k + 1) for k in range(n)])
    w = np.linalg.solve(V.T, rhs)
    return x, w


def make_cheb_gauss_grid(n_x: int, n_mu: int):
    """Return a gauss_grid-compatible callable bound to fixed resolutions.
    Radial coordinate r = R*sqrt(x) on interior-Chebyshev x-nodes with
    weights solving the [0,1]-exactness system; the returned radial weight
    satisfies w_r * r^2 == (R^3/2) * sqrt(x) * w_x so the physical measure
    2*pi*r^2 dr dmu is preserved exactly."""
    xi_raw, wx_raw = interior_cheb_rule(n_x)
    x01 = (xi_raw + 1.0) / 2.0
    wx01 = wx_raw / 2.0
    r = RADIUS * np.sqrt(x01)
    w_r = (RADIUS / 2.0) * (wx01 / np.sqrt(x01))
    mu_x, mu_w = interior_cheb_rule(n_mu)

    def grid(_radial_nodes: int, _angular_nodes: int, _radius: float):
        return (
            torch.tensor(r, dtype=DTYPE),
            torch.tensor(w_r, dtype=DTYPE),
            torch.tensor(mu_x, dtype=DTYPE),
            torch.tensor(mu_w, dtype=DTYPE),
        )

    return grid


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)

    checks = []
    report = {
        "attempt": "0007-g6-exactness-and-final",
        "preregistration": "module docstring (pre-computation)",
        "thread_pin": "torch.set_num_threads(1)",
        "checks": checks,
    }

    # Route A matrices: committed Gauss-Legendre machinery, finest rung.
    oracle_a = Oracle(dict(radial_order=ORDER, radial_nodes=96,
                           angular_nodes=48, radius=RADIUS))
    _, _, h_raw, comps_a = oracle_a.evaluate(background)
    h_a = (np.asarray(h_raw) + np.asarray(h_raw).T) / 2
    m_a = corrected_kinetic_hessian(build_cache(background, 96, 48))
    m_a = (m_a + m_a.T) / 2

    # Route B': identical constructions under the injected Chebyshev rule.
    print("[routeB'] building Chebyshev-family matrices...", flush=True)
    t0 = time.time()
    saved_kin = kinetic_stage2.gauss_grid
    saved_sol = solve_radial_1d.gauss_grid
    try:
        cheb_grid = make_cheb_gauss_grid(160, 80)
        kinetic_stage2.gauss_grid = cheb_grid
        solve_radial_1d.gauss_grid = cheb_grid
        oracle_b = Oracle(dict(radial_order=ORDER, radial_nodes=160,
                               angular_nodes=80, radius=RADIUS))
        e_b, _, h_raw_b, comps_b = oracle_b.evaluate(background)
        h_b = (np.asarray(h_raw_b) + np.asarray(h_raw_b).T) / 2
        m_b = corrected_kinetic_hessian(build_cache(background, 160, 80))
        m_b = (m_b + m_b.T) / 2
    finally:
        kinetic_stage2.gauss_grid = saved_kin
        solve_radial_1d.gauss_grid = saved_sol
    print(f"[routeB'] done ({time.time()-t0:.1f}s)", flush=True)

    rel_e = abs(e_b - E_COMMITTED) / E_COMMITTED
    checks.append({"name": "G0B_energy_transfer", "rel": rel_e,
                   "passed": bool(rel_e <= 1e-9)})
    print(f"[G0B] energy transfer rel = {rel_e:.3e}", flush=True)

    for name, ma, mb in (("H", h_a, h_b), ("M", m_a, m_b)):
        diff = float(np.max(np.abs(ma - mb)) / max(1.0, np.max(np.abs(ma))))
        checks.append({"name": f"G6_{name}_entry_exactness",
                       "max_entry_rel_diff": diff,
                       "tol": 1e-13, "passed": bool(diff <= 1e-13)})
        print(f"[G6 {name}] max entry rel diff = {diff:.3e}", flush=True)

    omega_a, _, _, _, _, _ = pencil_float64(h_a, m_a)
    omega_b, _, _, _, _, _ = pencil_float64(h_b, m_b)
    n_cmp = min(len(omega_a), len(omega_b))
    wa = np.sort(np.abs(np.asarray(omega_a[:n_cmp], dtype=float)))
    wb = np.sort(np.abs(np.asarray(omega_b[:n_cmp], dtype=float)))
    rel_w = np.abs(wb - wa) / np.abs(wa)
    checks.append({"name": "G6_pencil_agreement",
                   "max_rel_omega_diff": float(rel_w.max()),
                   "tol": 1e-9, "passed": bool(rel_w.max() <= 1e-9)})
    print(f"[G6 pencil] max rel omega diff = {float(rel_w.max()):.3e}",
          flush=True)

    positive = [math.sqrt(float(w)) for w in wb if w > 0]
    delta_e_b = 0.5 * math.fsum(positive)
    table = json.loads((HERE.parent / "0004" / "spectrum-table.json").read_text())
    delta_e_a = 0.5 * math.fsum(r["omega"] for r in table
                                if r["certified_margin_ok"])
    agree = abs(delta_e_b - delta_e_a) / abs(delta_e_a)
    checks.append({"name": "zero_point_independent_route",
                   "delta_E_routeA": delta_e_a,
                   "delta_E_routeB2": delta_e_b,
                   "rel_diff": agree,
                   "passed": bool(agree <= 1e-6)})
    print(f"[zero-point] A={delta_e_a:.10f} B'={delta_e_b:.10f} "
          f"rel={agree:.2e}", flush=True)

    tally = sum(1 for c in checks if c.get("passed"))
    report["energy_transfer_rel"] = rel_e
    report["delta_E_routeA"] = delta_e_a
    report["delta_E_routeB2"] = delta_e_b
    report["tally"] = f"{tally}/{len(checks)} CHECKS PASS"
    report["runtime_seconds"] = round(time.time() - started, 1)
    (HERE / "final-certified-result.json").write_text(
        json.dumps(report, indent=1))
    print(report["tally"], flush=True)


if __name__ == "__main__":
    main()
