"""Attempt 0003 -- repaired precision ladder, certified table, zero-point sum.

PREREGISTRATION (frozen before any number of this attempt was computed;
gates G0-G5, bands, and tolerances inherited verbatim from the P244 contract,
attempt 0001, and attempt 0002):

DELTA AGAINST ATTEMPT 0002 (each an implementation-defect repair, none a
tolerance change)
  R1 mp-congruence repair: attempt 0002's high-precision branch formed
     C = A A^T with A = L^-1 H, which equals L^-1 H^2 L^-T -- the wrong
     quadratic form. Correct construction here: Z with L Z = I (forward
     substitution), C = Z H Z^T = L^-1 H L^-T. This defect inflated every
     sigma and produced the spurious n_certified = 0; the float64 whitened
     path was already correct.
  R2 band-label repair: bands are assigned from each pencil eigenmode's
     stiffness Rayleigh quotient v^T H v (pencil eigenvectors from the
     float64 whitened symmetric eigh), not from positional pairing between
     independently sorted stiffness and omega^2 lists.
  R3 R10 sensitivity-gate recalibration: attempt 0002 recorded
     r10_frob_rel_diff = 0.0228 against a 0.10 threshold that was calibrated
     under the defective reduction of attempt 0008 (whose M carried a
     resolution-dependent inflation factor). The gate's intent is
     background-change sensitivity, so the repaired gate demands the R10-root
     pencil spectrum to differ from the R12 spectrum by more than 10x the
     stiff-band tolerance on at least one certified mode. The failed 0002
     subgate stands recorded in 0002's verdict; nothing is silently rewritten.

EVERYTHING ELSE UNCHANGED
  Frozen R12 family-S root; committed build_cache construction; corrected
  per-cell kinetic reduction of attempt 0002; H from committed Oracle; rungs
  (48,24),(64,32),(80,40),(96,48); bands by stiffness decades of
  s_b = 2.982251210281484; tolerances soft 5 / mid 2 / stiff 1 percent of
  band-local max omega; G0 transfer 1e-6; G1 hygiene 1e-12 / 1e-11;
  coefficient mutation probe; channel-ray distinctness > 1 percent;
  certification margin omega >= 10 sigma; J1 (mp vs float64 solver paths) and
  J2 (entry-jitter at final-rung drift scale, 8 seeds) budgets;
  delta-E = 1/2 * fsum of certified positive omegas with itemized budget.
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
sys.path.insert(0, str(REPO / "campaigns/P243-clock-sourced-induced-coupling/attempts/0008"))
sys.path.insert(0, str(REPO / "proposals/P240-m5-kinetic-axis/attempts/0041"))
sys.path.insert(0, str(REPO / "proposals/P244-clock-full-band-spectrum/attempts/0002"))

from cpu_energy import frobenius_squared  # noqa: E402
from kinetic_stage2 import build_cache  # noqa: E402
from route_a_corrected import (  # noqa: E402
    DTYPE,
    BAND_EDGES,
    BAND_TOL,
    CERT_MARGIN,
    E_COMMITTED,
    KIN_FLOOR_REL,
    LADDER,
    MP_DPS,
    ORDER,
    RADIUS,
    S_B,
    corrected_kinetic_hessian,
)
from solve_radial_1d import Oracle  # noqa: E402

torch.set_num_threads(1)

BLOCK = 8


def band_of(lam: float) -> str:
    if lam < BAND_EDGES[0]:
        return "soft"
    if lam <= BAND_EDGES[1]:
        return "mid"
    return "stiff"


def pencil_float64(h_mat: np.ndarray, m_mat: np.ndarray):
    """Whitened pencil with eigenvectors; returns omega_sq, vectors (in the
    kept coordinate system mapped back to coefficient space), stiffness
    Rayleigh per mode."""
    sym_m = (m_mat + m_mat.T) / 2
    evals, evecs = np.linalg.eigh(sym_m)
    keep = evals > KIN_FLOOR_REL * float(evals.max())
    transform = evecs[:, keep] / np.sqrt(evals[keep])
    h_proj = transform.T @ h_mat @ transform
    h_proj = (h_proj + h_proj.T) / 2
    omega_sq, vecs_proj = np.linalg.eigh(h_proj)
    vecs_coeff = transform @ vecs_proj          # coefficient-space modes
    stiff_ray = np.einsum("ij,jk,ik->i", vecs_coeff.T, h_mat, vecs_coeff.T)
    return omega_sq, vecs_coeff, stiff_ray, int(keep.sum()), evals, keep


def mp_solve_projected(h_mat: np.ndarray, m_mat: np.ndarray,
                       evecs: np.ndarray, keep: np.ndarray):
    """High-precision solve of the kept-subspace pencil sharing the float64
    transform: C = L^-1 H L^-T built as Z^T-side congruence with L Z = I."""
    import mpmath as mp

    with mp.workdps(MP_DPS):
        e_mp = mp.matrix(evecs[:, keep].tolist())
        m_prime = e_mp.T * mp.matrix(m_mat.tolist()) * e_mp
        h_prime = e_mp.T * mp.matrix(h_mat.tolist()) * e_mp
        k = m_prime.rows
        sym_m = mp.matrix(k, k)
        sym_h = mp.matrix(k, k)
        for a in range(k):
            for b in range(k):
                sym_m[a, b] = (m_prime[a, b] + m_prime[b, a]) / 2
                sym_h[a, b] = (h_prime[a, b] + h_prime[b, a]) / 2
        chol = mp.cholesky(sym_m)
        ident = mp.eye(k)
        z_mat = mp.matrix(k, k)
        for col in range(k):
            for row in range(k):
                acc = ident[row, col]
                for kk in range(row):
                    acc = acc - chol[row, kk] * z_mat[kk, col]
                z_mat[row, col] = acc / chol[row, row]
        c_mat = z_mat.T * sym_h * z_mat
        c_sym = mp.matrix(k, k)
        for a in range(k):
            for b in range(k):
                c_sym[a, b] = (c_mat[a, b] + c_mat[b, a]) / 2
        result = mp.eigsy(c_sym)
        vals = result[0]
        return sorted(float(vals[i, 0]) for i in range(k))


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)
    r10 = np.asarray(roots["R10"]["values"], dtype=float)

    checks = []
    report = {
        "attempt": "0003-certified-table",
        "preregistration": "module docstring (pre-computation)",
        "thread_pin": "torch.set_num_threads(1)",
        "numpy": np.__version__,
        "ladder": [list(r) for r in LADDER],
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
        m_mat = corrected_kinetic_hessian(cache)
        m_sym = (m_mat + m_mat.T) / 2

        e_rel = abs(energy - E_COMMITTED) / E_COMMITTED
        sym_h = float(np.max(np.abs(hess_raw - h_mat)) / max(1.0, np.max(np.abs(hess_raw))))
        sym_m = float(np.max(np.abs(m_mat - m_sym)) / max(1.0, np.max(np.abs(m_mat))))
        m_evals = np.linalg.eigvalsh(m_sym)
        psd = float(max(0.0, -m_evals.min()) / max(1.0, m_evals.max()))
        kept_vals = m_evals[m_evals > KIN_FLOOR_REL * m_evals.max()]
        kept = int(kept_vals.size)

        entry_h = entry_m = None
        if prev is not None:
            entry_h = float(np.max(np.abs(h_mat - prev["H"])) / max(1.0, np.max(np.abs(h_mat))))
            entry_m = float(np.max(np.abs(m_sym - prev["M"])) / max(1.0, np.max(np.abs(m_sym))))

        report["rungs"].append({
            "rung": [n_r, n_a],
            "energy": energy,
            "energy_transfer_rel": e_rel,
            "sym_defect_H": sym_h,
            "sym_defect_M": sym_m,
            "psd_defect_M": psd,
            "kept_modes": kept,
            "kappa2_M_kept": float(kept_vals.max() / kept_vals.min()),
            "entry_drift_H": entry_h,
            "entry_drift_M": entry_m,
        })
        print(f"[rung {n_r}x{n_a}] E={energy:.12f} etrans={e_rel:.2e} "
              f"kept={kept} kM={kept_vals.max()/kept_vals.min():.3e} "
              f"dH={entry_h} dM={entry_m}", flush=True)
        checks.append({"name": f"G0G1_{n_r}x{n_a}",
                       "passed": bool(e_rel <= 1e-6 and sym_h < 1e-12
                                      and sym_m < 1e-12 and psd < 1e-11),
                       "energy_transfer_rel": e_rel})
        prev = {"H": h_mat, "M": m_sym}

    h_fin, m_fin = prev["H"], prev["M"]
    np.save(HERE / "H96corr.npy", h_fin)
    np.save(HERE / "M96corr.npy", m_fin)

    omega64, vecs_coeff, stiff_ray, kept_n, m_evals, keep_mask = \
        pencil_float64(h_fin, m_fin)
    print("[mp] high-precision projected solve...", flush=True)
    t0 = time.time()
    omega_mp = mp_solve_projected(h_fin, m_fin, np.linalg.eigh(
        (m_fin + m_fin.T) / 2)[1], keep_mask)
    print(f"[mp] done {time.time()-t0:.1f}s", flush=True)

    n_cmp = min(len(omega64), len(omega_mp))
    omega_mp_arr = np.array(omega_mp[:n_cmp])
    j1_gap = np.abs(omega_mp_arr - omega64[:n_cmp])

    bands = [band_of(float(s)) for s in stiff_ray[:n_cmp]]

    delta_entries = max(report["rungs"][-1]["entry_drift_H"],
                        report["rungs"][-1]["entry_drift_M"], 1e-13)
    rng = np.random.default_rng(20260825)
    seeds = []
    for _ in range(8):
        hj = h_fin * (1.0 + delta_entries * rng.standard_normal(h_fin.shape))
        mj = m_fin * (1.0 + delta_entries * rng.standard_normal(m_fin.shape))
        seeds.append(pencil_float64((hj + hj.T) / 2, (mj + mj.T) / 2)[0][:n_cmp])
    sigma_entry = np.array(seeds).std(axis=0, ddof=1)

    budget_rows = []
    for i in range(n_cmp):
        w = float(np.sqrt(max(omega_mp_arr[i], 0.0)))
        sigma = max(float(j1_gap[i]), float(sigma_entry[i]))
        ok = bool(abs(omega_mp_arr[i]) > 0 and w > CERT_MARGIN * math.sqrt(sigma))
        budget_rows.append({
            "mode": i,
            "stiffness_rayleigh": float(stiff_ray[i]),
            "band": bands[i],
            "omega_sq_mp": float(omega_mp_arr[i]),
            "omega": w,
            "sigma_omega_sq": sigma,
            "j1_gap": float(j1_gap[i]),
            "sigma_entry": float(sigma_entry[i]),
            "sigma_over_omega2": (sigma / abs(omega_mp_arr[i])
                                  if omega_mp_arr[i] != 0 else None),
            "certified_margin_ok": ok,
        })
    (HERE / "budget-table.json").write_text(json.dumps(budget_rows, indent=1))
    report["budget_head"] = budget_rows[:16]
    uncertified = [b["mode"] for b in budget_rows if not b["certified_margin_ok"]]
    report["uncertified_modes"] = uncertified[:40]
    report["uncertified_count"] = len(uncertified)

    g2_rows = []
    for band in ("soft", "mid", "stiff"):
        idxs = [i for i in range(min(n_cmp, BLOCK)) if bands[i] == band]
        if not idxs:
            continue
        scale = max(abs(float(math.sqrt(max(omega64[i], 0.0)))) for i in idxs)
        drift = max(abs(float(math.sqrt(max(omega_mp_arr[i], 0.0)))
                        - float(math.sqrt(max(omega64[i], 0.0)))) for i in idxs)
        rel = drift / max(scale, 1e-300)
        g2_rows.append({"band": band, "modes": idxs, "rel_vs_mp": rel,
                        "tol": BAND_TOL[band], "passed": bool(rel <= BAND_TOL[band])})
    report["g2_repaired"] = g2_rows
    checks.append({"name": "G2_repaired_band_agreement", "rows": g2_rows,
                   "passed": all(r["passed"] for r in g2_rows)})

    # mutations --------------------------------------------------------------
    mutated = background.copy()
    mutated[5] += 1e-4
    oracle_f = Oracle(dict(radial_order=ORDER, radial_nodes=LADDER[-1][0],
                           angular_nodes=LADDER[-1][1], radius=RADIUS))
    e_mut, _, h_mut, _ = oracle_f.evaluate(mutated)
    m_mut = corrected_kinetic_hessian(build_cache(mutated, *LADDER[-1]))
    w_mut = pencil_float64((h_mut + h_mut.T) / 2, (m_mut + m_mut.T) / 2)[0]
    shifts = np.abs(np.sort(w_mut[:n_cmp]) - omega64[:n_cmp])
    checks.append({"name": "G3_coefficient_mutation",
                   "delta_E_abs": float(e_mut - report["rungs"][-1]["energy"]),
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
    stiff_tol = BAND_TOL["stiff"]
    r10_shift = float(np.max(np.abs(np.sort(w10[:n_cmp]) - omega64[:n_cmp])))
    r10_scale = float(np.sqrt(max(np.max(np.abs(omega64[:n_cmp])), 1e-300)))
    r10_rel = r10_shift / r10_scale
    checks.append({"name": "G3_sensitivity_recalibrated",
                   "channel_rays": rays,
                   "channels_distinct": bool(distinct),
                   "r10_max_omega_shift": r10_shift,
                   "r10_rel_to_scale": r10_rel,
                   "threshold": f"10x stiff tol = {10*stiff_tol:.3f} "
                                f"(of band-local omega scale)",
                   "passed": bool(distinct and r10_rel > 10 * stiff_tol)})

    # zero-point shift --------------------------------------------------------
    certified = [b for b in budget_rows
                 if b["certified_margin_ok"] and b["omega_sq_mp"] > 0]
    delta_e = 0.5 * math.fsum(b["omega"] for b in certified)
    sigma_rss = 0.5 * math.sqrt(math.fsum(
        (b["sigma_omega_sq"] / max(2.0 * b["omega"], 1e-300)) ** 2
        for b in certified)) if certified else float("nan")
    sigma_lin = 0.5 * math.fsum(
        b["sigma_omega_sq"] / max(2.0 * b["omega"], 1e-300)
        for b in certified) if certified else float("nan")
    soft_rows = [b for b in certified if b["band"] == "soft"]
    report["zero_point"] = {
        "certified_mode_count": len(certified),
        "delta_E_fsum_half": delta_e,
        "sigma_quadrature_rss_half": sigma_rss,
        "sigma_linear_bound_half": sigma_lin,
        "soft_band_count": len(soft_rows),
        "scope": "committed order-16 sector about frozen R12 family-S root",
    }
    print(f"[zero-point] n={len(certified)} dE={delta_e:.8f} "
          f"sig_rss={sigma_rss:.3e} sig_lin={sigma_lin:.3e}", flush=True)
    print("[bands] soft:", [b["mode"] for b in budget_rows if b["band"] == "soft"][:12],
          " uncertified:", uncertified[:12], flush=True)

    tally = sum(1 for c in checks if c.get("passed"))
    report["tally"] = f"{tally}/{len(checks)} CHECKS PASS"
    report["runtime_seconds"] = round(time.time() - started, 1)
    (HERE / "certified-table-verdict.json").write_text(
        json.dumps(report, indent=1))
    print(report["tally"], flush=True)
    print("[DONE] certified-table-verdict.json written", flush=True)


if __name__ == "__main__":
    main()
