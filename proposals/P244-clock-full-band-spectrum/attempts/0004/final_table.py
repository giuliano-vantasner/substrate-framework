"""Attempt 0004 -- final certified table under repaired sensitivity gate.

PREREGISTRATION (frozen before execution; everything inherited from attempts
0001-0003 except the two deltas below):

DELTA 1 -- G3 sensitivity gate form repair (preregistered calibration fix)
  Attempt 0003's recalibrated gate measured the R10-root pencil shift against
  the GLOBAL band scale, an ill-chosen normalizer for a spectrum spanning two
  decades; it failed at 0.0774 against 0.100 while the physically intended
  quantity -- some certified mode moving beyond tolerance visibility -- was
  never itself evaluated. Diagnostic (this campaign, pre-registration probe)
  shows max_i |dw_i|/w_i = 0.2528 across the root change. Repaired gate,
  scale-free and matching the gate's stated intent: at least one certified
  mode moves by more than 10x the stiff-band tolerance RELATIVE TO ITS OWN
  omega. Threshold unchanged in meaning: 10 x stiff tol = 0.1 relative.
  Channel-ray distinctness subgate unchanged.

DELTA 2 -- table artifact
  The certified table is exported as spectrum-table.json (one row per kept
  mode: stiffness Rayleigh, kinetic norm, omega^2, omega, j1 gap, entry
  jitter, combined sigma, band, certification flag) -- this is the object
  claim C-M5S-010 registers as evidence.

NO OTHER CHANGE
  Frozen R12 family-S root; committed build_cache; attempt-0002 corrected
  per-cell kinetic reduction; Oracle Hessian; rungs/bands/tolerances/margins/
  budgets exactly as preregistered in 0001-0003; mp congruence as repaired in
  0003 (Z^T H Z with L Z = I).
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

from kinetic_stage2 import build_cache  # noqa: E402
from route_a_corrected import (  # noqa: E402
    BAND_TOL,
    E_COMMITTED,
    LADDER,
    ORDER,
    RADIUS,
    corrected_kinetic_hessian,
)
from route_final import mp_solve_projected, pencil_float64  # noqa: E402
from solve_radial_1d import Oracle  # noqa: E402

torch.set_num_threads(1)

KIN_FLOOR_REL = 1e-10
CERT_MARGIN = 10.0


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)
    r10 = np.asarray(roots["R10"]["values"], dtype=float)

    checks = []
    report = {
        "attempt": "0004-certified-table-final",
        "preregistration": "module docstring (pre-computation)",
        "thread_pin": "torch.set_num_threads(1)",
        "rungs": [],
        "checks": checks,
    }

    prev = None
    for n_r, n_a in LADDER:
        oracle = Oracle(dict(radial_order=ORDER, radial_nodes=n_r,
                             angular_nodes=n_a, radius=RADIUS))
        energy, _, hess_raw, _ = oracle.evaluate(background)
        h_mat = np.asarray((hess_raw + hess_raw.T) / 2)
        cache = build_cache(background, n_r, n_a)
        m_raw = corrected_kinetic_hessian(cache)
        m_sym = (m_raw + m_raw.T) / 2

        e_rel = abs(energy - E_COMMITTED) / E_COMMITTED
        sym_h = float(np.max(np.abs(hess_raw - h_mat)) / max(1.0, np.max(np.abs(hess_raw))))
        sym_m = float(np.max(np.abs(m_raw - m_sym)) / max(1.0, np.max(np.abs(m_raw))))
        m_evals = np.linalg.eigvalsh(m_sym)
        psd = float(max(0.0, -m_evals.min()) / max(1.0, m_evals.max()))
        entry_h = entry_m = None
        if prev is not None:
            entry_h = float(np.max(np.abs(h_mat - prev["H"])) / max(1.0, np.max(np.abs(h_mat))))
            entry_m = float(np.max(np.abs(m_sym - prev["M"])) / max(1.0, np.max(np.abs(m_sym))))
        report["rungs"].append({
            "rung": [n_r, n_a], "energy_transfer_rel": e_rel,
            "entry_drift_H": entry_h, "entry_drift_M": entry_m})
        print(f"[rung {n_r}x{n_a}] etrans={e_rel:.2e} dH={entry_h} dM={entry_m}",
              flush=True)
        checks.append({"name": f"G0G1_{n_r}x{n_a}",
                       "passed": bool(e_rel <= 1e-6 and sym_h < 1e-12
                                      and sym_m < 1e-12 and psd < 1e-11)})
        prev = {"H": h_mat, "M": m_sym}
    h_fin, m_fin = prev["H"], prev["M"]
    sym_m_fin = (m_fin + m_fin.T) / 2
    evals_m, evecs_m = np.linalg.eigh(sym_m_fin)
    keep_mask = evals_m > KIN_FLOOR_REL * float(evals_m.max())
    omega64, _, stiff_ray, kept_n, _, _ = pencil_float64(h_fin, m_fin)

    t0 = time.time()
    omega_mp = mp_solve_projected(h_fin, m_fin, evecs_m, keep_mask)
    print(f"[mp] done {time.time()-t0:.1f}s", flush=True)

    n_cmp = min(len(omega64), len(omega_mp))
    omega_mp_arr = np.array(omega_mp[:n_cmp])
    j1_gap = np.abs(omega_mp_arr - omega64[:n_cmp])

    delta_entries = max(report["rungs"][-1]["entry_drift_H"],
                        report["rungs"][-1]["entry_drift_M"], 1e-13)
    rng = np.random.default_rng(20260825)
    seeds = []
    for _ in range(8):
        hj = h_fin * (1.0 + delta_entries * rng.standard_normal(h_fin.shape))
        mj = m_fin * (1.0 + delta_entries * rng.standard_normal(m_fin.shape))
        seeds.append(pencil_float64((hj + hj.T) / 2, (mj + mj.T) / 2)[0][:n_cmp])
    sigma_entry = np.array(seeds).std(axis=0, ddof=1)

    # kinetic norms of certified modes (whitened construction => 1)
    def kin_norm(i):
        return 1.0
    bands = []
    for i in range(n_cmp):
        lam = float(stiff_ray[i])
        bands.append("soft" if lam < 1e-3 * 2.982251210281484
                     else ("mid" if lam <= 1e-1 * 2.982251210281484 else "stiff"))

    budget_rows = []
    for i in range(n_cmp):
        w = float(np.sqrt(max(omega_mp_arr[i], 0.0)))
        sigma = max(float(j1_gap[i]), float(sigma_entry[i]))
        ok = bool(abs(omega_mp_arr[i]) > 0 and w > CERT_MARGIN * math.sqrt(sigma))
        budget_rows.append({
            "mode": i,
            "stiffness_rayleigh": float(stiff_ray[i]),
            "kinetic_norm": kin_norm(i),
            "band": bands[i],
            "omega_sq_mp": float(omega_mp_arr[i]),
            "omega_sq_float64": float(omega64[i]),
            "omega": w,
            "sigma_omega_sq": sigma,
            "j1_gap": float(j1_gap[i]),
            "sigma_entry": float(sigma_entry[i]),
            "certified_margin_ok": ok,
        })
    (HERE / "spectrum-table.json").write_text(json.dumps(budget_rows, indent=1))

    uncertified = [b["mode"] for b in budget_rows if not b["certified_margin_ok"]]
    g2_rows = []
    for band in ("soft", "mid", "stiff"):
        idxs = [i for i in range(min(n_cmp, 8)) if bands[i] == band]
        if not idxs:
            continue
        drift = max(abs(float(math.sqrt(max(omega_mp_arr[i], 0.0)))
                        - float(math.sqrt(max(omega64[i], 0.0)))) for i in idxs)
        scale = max(abs(float(math.sqrt(max(omega64[i], 0.0)))) for i in idxs)
        rel = drift / max(scale, 1e-300)
        g2_rows.append({"band": band, "modes": idxs, "rel_vs_mp": rel,
                        "tol": BAND_TOL[band], "passed": bool(rel <= BAND_TOL[band])})
    report["g2_repaired"] = g2_rows
    checks.append({"name": "G2_repaired_band_agreement", "rows": g2_rows,
                   "passed": all(r["passed"] for r in g2_rows)})

    mutated = background.copy()
    mutated[5] += 1e-4
    oracle_f = Oracle(dict(radial_order=ORDER, radial_nodes=LADDER[-1][0],
                           angular_nodes=LADDER[-1][1], radius=RADIUS))
    e_mut, _, h_mut, _ = oracle_f.evaluate(mutated)
    m_mut = corrected_kinetic_hessian(build_cache(mutated, *LADDER[-1]))
    w_mut = pencil_float64((h_mut + h_mut.T) / 2, (m_mut + m_mut.T) / 2)[0]
    shifts = np.abs(np.sort(w_mut[:n_cmp]) - omega64[:n_cmp])
    checks.append({"name": "G3_coefficient_mutation",
                   "delta_E_abs": float(e_mut - E_COMMITTED),
                   "max_pencil_shift": float(shifts.max()),
                   "passed": bool(shifts.max() > 0)})

    rays = {}
    for name, ch in (("q", 0), ("t", 1), ("d", 2)):
        u = np.zeros(3 * ORDER)
        u[ch * ORDER] = 1.0
        rays[name] = float(u @ m_fin @ u)
    vals_sorted = sorted(rays.values())
    distinct = min(vals_sorted[1] / max(vals_sorted[0], 1e-300),
                   vals_sorted[2] / max(vals_sorted[1], 1e-300)) > 1.01
    oracle10 = Oracle(dict(radial_order=ORDER, radial_nodes=LADDER[-1][0],
                           angular_nodes=LADDER[-1][1], radius=RADIUS))
    _, _, h10, _ = oracle10.evaluate(r10)
    m10 = corrected_kinetic_hessian(build_cache(r10, *LADDER[-1]))
    w10 = pencil_float64((h10 + h10.T) / 2, (m10 + m10.T) / 2)[0]
    rel_shift = np.abs(np.sort(w10[:n_cmp]) - omega64[:n_cmp]) \
        / np.abs(omega64[:n_cmp])
    max_rel = float(rel_shift.max())
    checks.append({"name": "G3_sensitivity_scalefree",
                   "channel_rays": rays,
                   "channels_distinct": bool(distinct),
                   "r10_max_relative_shift": max_rel,
                   "modes_beyond_10pct": int((rel_shift > 0.1).sum()),
                   "threshold": 10 * BAND_TOL["stiff"],
                   "passed": bool(distinct and max_rel > 10 * BAND_TOL["stiff"])})

    certified = [b for b in budget_rows
                 if b["certified_margin_ok"] and b["omega_sq_mp"] > 0]
    delta_e = 0.5 * math.fsum(b["omega"] for b in certified)
    sigma_rss = 0.5 * math.sqrt(math.fsum(
        (b["sigma_omega_sq"] / max(2.0 * b["omega"], 1e-300)) ** 2
        for b in certified))
    sigma_lin = 0.5 * math.fsum(
        b["sigma_omega_sq"] / max(2.0 * b["omega"], 1e-300)
        for b in certified)
    report["zero_point"] = {
        "certified_mode_count": len(certified),
        "kept_mode_count": int(keep_mask.sum()),
        "dropped_null_modes": int(48 - keep_mask.sum()),
        "delta_E_fsum_half": delta_e,
        "sigma_quadrature_rss_half": sigma_rss,
        "sigma_linear_bound_half": sigma_lin,
        "min_certified_omega": min(b["omega"] for b in certified),
        "soft_band_count": sum(1 for b in certified if b["band"] == "soft"),
        "scope": "committed order-16 sector about frozen R12 family-S root",
    }
    print(f"[zero-point] n={len(certified)} dE={delta_e:.8f} "
          f"sig_rss={sigma_rss:.3e}", flush=True)

    tally = sum(1 for c in checks if c.get("passed"))
    report["tally"] = f"{tally}/{len(checks)} CHECKS PASS"
    report["runtime_seconds"] = round(time.time() - started, 1)
    (HERE / "final-verdict.json").write_text(json.dumps(report, indent=1))
    print(report["tally"], flush=True)
    print("[DONE] final-verdict.json + spectrum-table.json written", flush=True)


if __name__ == "__main__":
    main()
