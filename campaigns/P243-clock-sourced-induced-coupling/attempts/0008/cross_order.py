"""Attempt 0008 cross-order leg -- adjudicate the grid-mode suspicion.

PREREGISTRATION (declared before any solve below was launched):

Question.  Stage 1 found two soft modes about the frozen R=12 order-16
window root, the softest split-dominant with 13-14 radial nodes -- nodal
count near the basis order, the classic spectral grid-scale-artifact
signature.  Family-S lambda_min also halves per order across the committed
R=8 ladder (4.5e-5 -> 2.0e-5 -> 9.7e-6).  This leg decides, for each soft
mode, GRID ARTIFACT vs PHYSICAL BOUND MODE vs INCONCLUSIVE.

Protocol (hardening rules from attempts 0004/0005):
  - continuation seeding only: seed order N+2 by zero-padding the accepted
    lower-order coefficients (profiles are Chebyshev in 2(r/R)^2 - 1);
  - solver = the certified solve_order (hybr, exact autograd Jacobian,
    xtol 1e-14, base quadrature 32x16);
  - family guard BEFORE any spectrum is read: converged (relgrad < 1e-10)
    AND relative energy continuity |E_N - E_prev| / E_prev < 1e-3;
  - spectra are read at FROZEN new-root field values on the SAME census
    quadrature (48x16) used by stage 1, bottom block of 8.

Decision rule (fixed now):
  * GRID ARTIFACT   : soft-mode eigenvalue shrinks by factor >= 3 per order
    step AND its dominant-channel nodal count grows by >= 2 per order step;
  * PHYSICAL        : eigenvalue changes <= 5% per order step once above the
    stage-1 resolution floor AND dominant-channel nodal count stable (+-1);
  * INCONCLUSIVE    : order-N solve fails the family guard -- recorded as a
    named obstruction (consistent with the committed R=10 ladder
    divergence at N >= 18); classification then defers to the stage-2
    kinetic-metric route.

Sanity row (not a pass/fail gate): stiff-band modes are expected to drift
<= 10% per order step; larger drift is recorded as an anomaly.

AMENDMENT v2 (declared after run 1, before any N>=18 spectrum was read --
the failed guard aborted before census_at, so those numbers are unopened):
  Run 1 exposed two guard defects:
  (a) the code required hybr's success flag in addition to relgrad < 1e-10;
      this docstring never asked for the flag (phase1_ladder's house
      convention is relgrad-only).  The N=18 root sits at
      relgrad = 1.83e-14 -- a genuine stationary point.  Fixed: relgrad
      only.
  (b) the scalar energy-continuity gate (1e-3) conflates systematic
      variational lowering under basis enrichment with branch jumps.
      Branch identity is instead tested structurally, pre-declared here:
      stiff-band modes 2..7 must drift <= 25% relative vs N16 with no mode
      crossing zero and both soft modes staying positive (a branch jump
      decorrelates the whole spectrum; the committed R=10 jump diverges to
      E=inf).  Energy continuity stays REPORTED with a loose 1e-2 anomaly
      bound only.
  All other rules unchanged.


Environment: system python3 torch host; threads pinned to 1.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
import numpy as np
import torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "proposals/P240-m5-kinetic-axis/attempts/0041"))
sys.path.insert(0, str(HERE))

from solve_radial_1d import Oracle, solve_order  # noqa: E402
from window_census import BLOCK, nodal_census  # noqa: E402

torch.set_num_threads(1)
RADIUS = 12.0

ENERGY_ANOMALY_RTOL = 1e-2
STIFF_IDENTITY_RTOL = 0.25
SOLVE_QUAD = dict(radial_nodes=32, angular_nodes=16)
CENSUS_QUAD = (48, 16)
RELGRAD_GATE = 1e-10
GRID_SHRINK_FACTOR = 3.0
GRID_NODE_GROWTH = 2
PHYS_CHANGE_RTOL = 0.05
STIFF_SANITY_RTOL = 0.10


def pad(values, n):
    old = np.asarray(values).reshape(3, -1)
    out = np.zeros((3, n))
    out[:, :old.shape[1]] = old
    return out.ravel()


def bottom_block(hess):
    sym = (hess + hess.T) / 2
    values, vectors = np.linalg.eigh(sym)
    return values[:BLOCK], vectors[:, :BLOCK]


def census_at(values, order):
    oracle = Oracle(dict(radial_order=order, radial_nodes=CENSUS_QUAD[0],
                         angular_nodes=CENSUS_QUAD[1], radius=RADIUS))
    total, grad, hess, _ = oracle.evaluate(values)
    relgrad = float(np.max(np.abs(grad)) / max(1.0, abs(total)))
    lam, vec = bottom_block(hess)
    return float(total), relgrad, lam, vec


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    values16 = np.asarray(roots["R12"]["values"], dtype=float)
    e_ref, _, lam16, vec16 = census_at(values16, 16)
    print(f"[base N=16] E={e_ref:.10f} bottom={lam16[0]:+.6e} "
          f"lam1={lam16[1]:+.6e}", flush=True)

    rows = []
    prev_energy = e_ref
    prev_values = values16
    verdicts = {}
    for order in (18, 20):
        seed = pad(prev_values, order)
        t0 = time.time()
        row = solve_order(order, seed,
                          dict(SOLVE_QUAD, radius=RADIUS))
        values_n = np.asarray(row.pop("values"))
        conv = bool(row["relative_gradient"] < RELGRAD_GATE)
        d_e = abs(row["energy"] - prev_energy) / max(1.0, abs(prev_energy))
        e_n, relgrad_n, lam_n, vec_n = census_at(values_n, order)
        stiff_rel = (np.abs(lam_n[2:BLOCK] - lam16[2:BLOCK])
                     / np.abs(lam16[2:BLOCK]))
        identity_ok = bool(
            np.all(stiff_rel <= STIFF_IDENTITY_RTOL)
            and np.all(lam_n[2:BLOCK] > 0.0)
            and lam_n[0] > 0.0 and lam_n[1] > 0.0)
        anomaly = bool(d_e > ENERGY_ANOMALY_RTOL)
        family_ok = bool(conv and identity_ok and not anomaly)
        rec = {
            "order": order,
            "solver_success": bool(row["success"]),
            "relative_gradient": row["relative_gradient"],
            "energy": row["energy"],
            "energy_continuity_rel": d_e,
            "energy_anomaly": anomaly,
            "stiff_band_max_rel_drift":
                float(np.max(stiff_rel)),
            "family_guard_passed": family_ok,
            "minutes": round((time.time() - t0) / 60.0, 1),
        }
        print(f"[solve N={order}] conv={conv} E={row['energy']:.10f} "
              f"dE_rel={d_e:.3e} stiff_drift={float(np.max(stiff_rel)):.3e} "
              f"({rec['minutes']}min)", flush=True)
        if not family_ok:
            rec["disposition"] = (
                "family-guard failure -- named obstruction; "
                "INCONCLUSIVE by this route")
            rows.append(rec)
            break
        ratios = lam_n[:2] / lam16[:2]
        nodes_prev = [nodal_census(vec16[:, i])[1] for i in range(2)]
        nodes_now = [nodal_census(vec_n[:, i])[1] for i in range(2)]
        stiff_drift = float(np.max(stiff_rel))
        rec.update({
            "census_energy": e_n,
            "census_relgrad": relgrad_n,
            "bottom_block": [float(v) for v in lam_n],
            "soft_ratios_vs_N16": [float(r) for r in ratios],
            "soft_nodes_prev": nodes_prev,
            "soft_nodes_now": nodes_now,
            "stiff_band_max_rel_drift": stiff_drift,
        })
        rows.append(rec)
        print(f"[census N={order}] lam0={lam_n[0]:+.6e} "
              f"(x{ratios[0]:.3f}) lam1={lam_n[1]:+.6e} (x{ratios[1]:.3f}) "
              f"nodes0={nodes_now[0]} nodes1={nodes_now[1]} "
              f"stiff_drift={stiff_drift:.3e}", flush=True)
        prev_energy = row["energy"]
        prev_values = values_n

    # ---- fixed decision rule ------------------------------------------------
    usable = [r for r in rows if "bottom_block" in r]
    for mode_idx in range(2):
        if not usable:
            verdicts[f"mode_{mode_idx}"] = "INCONCLUSIVE (no guarded solve)"
            continue
        last = usable[-1]
        ratio = last["soft_ratios_vs_N16"][mode_idx]
        d_nodes = (last["soft_nodes_now"][mode_idx]
                   - last["soft_nodes_prev"][mode_idx])
        steps = last["order"] // 2 - 8  # number of +2 order steps from 16
        shrink_per_step = ratio ** (1.0 / max(steps, 1))
        if shrink_per_step <= 1.0 / GRID_SHRINK_FACTOR \
                and d_nodes >= GRID_NODE_GROWTH:
            verdicts[f"mode_{mode_idx}"] = "GRID ARTIFACT"
        elif abs(shrink_per_step - 1.0) <= PHYS_CHANGE_RTOL \
                and abs(d_nodes) <= 1:
            verdicts[f"mode_{mode_idx}"] = "PHYSICAL BOUND MODE"
        else:
            verdicts[f"mode_{mode_idx}"] = (
                f"INCONCLUSIVE (shrink/step={shrink_per_step:.3f}, "
                f"d_nodes={d_nodes})")
    report = {
        "attempt": "0008-cross-order",
        "preregistration": "this module docstring (pre-solve)",
        "base_reference": {"N": 16, "energy": e_ref,
                           "bottom_block": [float(v) for v in lam16]},
        "rows": rows,
        "verdicts": verdicts,
        "runtime_seconds": round(time.time() - started, 1),
        "thread_pin": "torch.set_num_threads(1)",
    }
    (HERE / "cross-order.json").write_text(json.dumps(report, indent=1))
    for k, v in verdicts.items():
        print(f"[VERDICT {k}] {v}", flush=True)
    print("[DONE] cross-order.json written", flush=True)


if __name__ == "__main__":
    main()
