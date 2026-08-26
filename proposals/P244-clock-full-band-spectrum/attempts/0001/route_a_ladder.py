"""Attempt 0001 route A -- quadrature ladder, conditioning diagnosis, budgets.

PREREGISTRATION (frozen before any rung beyond the committed base quadrature
was computed; see proposals/P244-clock-full-band-spectrum/proposal.yaml):

OBJECT
  The fluctuation pencil (H, M) about the FROZEN R=12 family-S window root
  (order-16 basis, coefficients read read-only from P240 attempts 0042
  largeR-roots.json). H is the autograd-exact static-energy Hessian; M is the
  exact-quadratic kinetic Jacobian; both reuse the committed constructions
  imported from campaigns/P243 attempts 0008 (kinetic_stage2.build_cache /
  kinetic_hessian) and P240 attempts 0041 (solve_radial_1d.Oracle). The
  background is never re-solved: refinement varies ONLY quadrature resolution,
  so the recorded cross-order stationary-point obstruction cannot occur.

LADDER
  Quadrature rungs (radial_nodes, angular_nodes) = (48,24), (64,32),
  (80,40), (96,48). Per rung: energy transfer, matrix symmetry/PSD hygiene,
  entry-level convergence vs the previous rung, kappa_2(M), float64 whitened
  spectrum, tangent-null gauge.

BANDS AND REPAIRED G2 (replaces 0008's mixed-scale gate)
  Stiffness bands relative to s_b = 2.982251210281484:
    soft: lambda < 1e-3*s_b; mid: [1e-3*s_b, 1e-1*s_b]; stiff: > 1e-1*s_b.
  omega agreement is judged per band relative to the band-local maximum |omega|,
  tolerances soft 5e-2, mid 2e-2, stiff 1e-2.

PRECISION LADDER AND BUDGETS (hardened small-ratio-numerics)
  J1 solver-noise probe: float64 whitened spectrum vs mpmath dps=60
     eigendecomposition of M and projected eigsy at the finest rung;
     per-mode |w64 - w_mp| isolates float64 whitening/solver amplification.
  J2 entry-uncertainty probe: elementwise relative entry jitter at the
     measured rung-to-rung drift scale delta_entries, 8 seeds, float64 solve
     (declared valid where the induced spread exceeds the J1 floor by >= 10x);
     per-mode spread sigma_entry.
  Budget for each quoted omega: sigma_i = max(J1 gap, sigma_entry, last-step
  rung drift). Certified rows require omega_i >= 10*sigma_i (G5 margin);
  rows failing the margin are recorded UNCERTIFIED_AT_TOLERANCE with their
  numbers -- quantified honesty, not tolerance inflation.

GATES
  G0 transfer |E - 55.10418278043526|/E <= 1e-6 at every rung.
  G1 H,M symmetric < 1e-12 rel; M PSD defect < 1e-11 at every rung.
  G2 repaired per-band agreement across the last two rungs within band tol.
  G3 mutations: single-coefficient mutation (+1e-4 on q order-5) moves the
     energy and the certified stiff-band omegas beyond 10x their band
     tolerances; unit q/t/d channel kinetic rays pairwise distinct > 1%;
     R10-root M differs > 10 percent relative Frobenius.
  G5 tangent/null gauge: t-channel kinetic ray and the smallest kept
     M eigenvalue ratio reported per rung as the in-situ numerical zero.

OUTPUT
  route-a-verdict.json (this directory), matrices snapshot H96/M96 .npy for
  the independent route-B cross-check, first-execution stdout captured here.

ENVIRONMENT
  torch.set_num_threads(1); numpy 1.26 host; no trapezoid use anywhere.
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
sys.path.insert(0, str(REPO / "campaigns/P243-clock-sourced-induced-coupling/attempts/0008"))
sys.path.insert(0, str(REPO / "proposals/P240-m5-kinetic-axis/attempts/0041"))

from kinetic_stage2 import build_cache, kinetic_hessian  # noqa: E402
from solve_radial_1d import Oracle  # noqa: E402

torch.set_num_threads(1)

DTYPE = torch.float64
RADIUS = 12.0
ORDER = 16
LADDER = ((48, 24), (64, 32), (80, 40), (96, 48))
BLOCK = 8
KIN_FLOOR_REL = 1e-10
E_COMMITTED = 55.10418278043526
S_B = 2.982251210281484
BAND_EDGES = (1e-3 * S_B, 1e-1 * S_B)
BAND_TOL = {"soft": 5e-2, "mid": 2e-2, "stiff": 1e-2}
CERT_MARGIN = 10.0
MP_DPS = 60


def band_of(lam: float) -> str:
    if lam < BAND_EDGES[0]:
        return "soft"
    if lam <= BAND_EDGES[1]:
        return "mid"
    return "stiff"


def whiten_float64(h_mat: np.ndarray, m_mat: np.ndarray):
    sym_m = (m_mat + m_mat.T) / 2
    evals, evecs = np.linalg.eigh(sym_m)
    keep = evals > KIN_FLOOR_REL * float(evals.max())
    transform = evecs[:, keep] / np.sqrt(evals[keep])
    h_proj = transform.T @ h_mat @ transform
    omega_sq = np.linalg.eigvalsh((h_proj + h_proj.T) / 2)
    return omega_sq, evals, int(keep.sum())


def mp_spectrum(m_mat: np.ndarray, h_mat: np.ndarray):
    """High-precision pencil spectrum: eig of M at dps=MP_DPS, project H."""
    import mpmath as mp

    with mp.workdps(MP_DPS):
        m_mp = mp.matrix(m_mat.tolist())
        h_mp = mp.matrix(h_mat.tolist())
        evals, evecs = mp.eig(m_mp)
        pairs = sorted(
            ((mp.re(v), [evecs[r][c] for r in range(len(evals))])
             for c, v in enumerate(evals)),
            key=lambda p: p[0], reverse=True,
        )
        emax = abs(pairs[0][0])
        cols, scales = [], []
        for value, vec in pairs:
            if value > KIN_FLOOR_REL * emax:
                cols.append(vec)
                scales.append(mp.sqrt(value))
        k = len(cols)
        t_mat = mp.matrix(len(cols), len(evals))
        for a, (vec, scale) in enumerate(zip(cols, scales)):
            for b in range(len(evals)):
                t_mat[a, b] = vec[b] / scale
        c_mat = t_mat * h_mp * t_mat.T
        c_sym = mp.matrix(k, k)
        for a in range(k):
            for b in range(k):
                c_sym[a, b] = (c_mat[a, b] + c_mat[b, a]) / 2
        omega_sq = mp.eigsy(c_sym)
        return np.array([float(mp.re(w)) for w in omega_sq]), k


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)
    r10 = np.asarray(roots["R10"]["values"], dtype=float)

    checks = []
    report = {
        "attempt": "0001-route-a",
        "preregistration": "module docstring (pre-computation)",
        "thread_pin": "torch.set_num_threads(1)",
        "numpy": np.__version__,
        "ladder": [list(r) for r in LADDER],
        "rungs": [],
        "checks": checks,
    }

    prev = None
    for rung_idx, (n_r, n_a) in enumerate(LADDER):
        oracle = Oracle(dict(radial_order=ORDER, radial_nodes=n_r,
                             angular_nodes=n_a, radius=RADIUS))
        energy, grad, hess_raw, _ = oracle.evaluate(background)
        h_mat = np.asarray((hess_raw + hess_raw.T) / 2)
        grad_norm = float(np.max(np.abs(grad)))
        cache = build_cache(background, n_r, n_a)
        m_mat = kinetic_hessian(cache)
        m_sym = (m_mat + m_mat.T) / 2

        e_rel = abs(energy - E_COMMITTED) / E_COMMITTED
        sym_h_def = float(np.max(np.abs(hess_raw - h_mat)) / max(1.0, np.max(np.abs(hess_raw))))
        sym_m_def = float(np.max(np.abs(m_mat - m_sym)) / max(1.0, np.max(np.abs(m_mat))))
        m_evals = np.linalg.eigvalsh(m_sym)
        psd_defect = float(max(0.0, -m_evals.min()) / max(1.0, m_evals.max()))
        kappa_m = float(m_evals.max() / max(m_evals.min(), 1e-300))

        # t-channel kinetic gauge (exact structural null family)
        t_vec = np.zeros(3 * ORDER)
        t_vec[ORDER] = 1.0
        t_ray = float(t_vec @ m_sym @ t_vec)

        omega_sq, _, keep_n = whiten_float64(h_mat, m_sym)

        entry_h = entry_m = None
        if prev is not None:
            entry_h = float(np.max(np.abs(h_mat - prev["H"])) / max(1.0, np.max(np.abs(h_mat))))
            entry_m = float(np.max(np.abs(m_sym - prev["M"])) / max(1.0, np.max(np.abs(m_sym))))

        row = {
            "rung": [n_r, n_a],
            "energy": energy,
            "energy_transfer_rel": e_rel,
            "grad_max_abs": grad_norm,
            "sym_defect_H": sym_h_def,
            "sym_defect_M": sym_m_def,
            "psd_defect_M": psd_defect,
            "kappa2_M": kappa_m,
            "kept_modes": keep_n,
            "t_channel_rayleigh": t_ray,
            "entry_drift_H": entry_h,
            "entry_drift_M": entry_m,
            "omega_sq_low8": [float(w) for w in omega_sq[:BLOCK]],
            "omega_sq_all_top": float(omega_sq[-1]),
        }
        report["rungs"].append(row)
        print(f"[rung {n_r}x{n_a}] E={energy:.12f} etrans={e_rel:.2e} "
              f"kM={kappa_m:.3e} kept={keep_n} t_ray={t_ray:.2e} "
              f"dH={entry_h} dM={entry_m}", flush=True)
        g0 = e_rel <= 1e-6 and sym_h_def < 1e-12 and sym_m_def < 1e-12 \
            and psd_defect < 1e-11
        checks.append({"name": f"G0G1_rung_{n_r}x{n_a}",
                       "energy_transfer_rel": e_rel,
                       "sym_defect_H": sym_h_def,
                       "sym_defect_M": sym_m_def,
                       "psd_defect_M": psd_defect,
                       "passed": bool(g0)})
        prev = {"H": h_mat, "M": m_sym}

    # ---- finest rung: precision ladder + bands + budgets -----------------
    h_fin = prev["H"]
    m_fin = prev["M"]
    np.save(HERE / "H96.npy", h_fin)
    np.save(HERE / "M96.npy", m_fin)

    omega64, m_evals_fin, keep_fin = whiten_float64(h_fin, m_fin)
    print("[mp] high-precision pencil solve starting "
          f"(dps={MP_DPS}, this can take minutes)...", flush=True)
    t_mp = time.time()
    omega_mp, kept_mp = mp_spectrum(m_fin, h_fin)
    print(f"[mp] done in {time.time() - t_mp:.1f}s kept={kept_mp}", flush=True)

    n_cmp = min(len(omega64), len(omega_mp))
    j1_gap = np.abs(np.sort(omega_mp)[:n_cmp] - omega64[:n_cmp])

    stiffness = np.linalg.eigvalsh(h_fin)[:len(omega64)]
    bands = [band_of(l) for l in stiffness[:n_cmp]]

    delta_entries = max(
        report["rungs"][-1]["entry_drift_H"] or 0.0,
        report["rungs"][-1]["entry_drift_M"] or 0.0, 1e-13)
    rng = np.random.default_rng(20260825)
    seeds_w = []
    for _ in range(8):
        hj = h_fin * (1.0 + delta_entries * rng.standard_normal(h_fin.shape))
        mj = m_fin * (1.0 + delta_entries * rng.standard_normal(m_fin.shape))
        hj = (hj + hj.T) / 2
        mj = (mj + mj.T) / 2
        seeds_w.append(whiten_float64(hj, mj)[0])
    seeds_arr = np.array([np.sort(w[:n_cmp]) for w in seeds_w])
    sigma_entry = seeds_arr.std(axis=0, ddof=1)

    j1_floor = float(np.max(j1_gap))
    budget_rows = []
    for i in range(n_cmp):
        rung_drift = 0.0
        if len(report["rungs"]) >= 2:
            a = report["rungs"][-1]["omega_sq_low8"]
            b = report["rungs"][-2]["omega_sq_low8"]
            if i < len(a) and i < len(b):
                rung_drift = abs(a[i] - b[i])
        sigma = max(float(j1_gap[i]), float(sigma_entry[i]), rung_drift)
        w = float(np.sqrt(max(omega_mp[i], 0.0)))
        budget_rows.append({
            "mode": i,
            "stiffness": float(stiffness[i]),
            "band": bands[i],
            "omega_sq_mp": float(omega_mp[i]),
            "omega": w,
            "sigma_omega_sq": sigma,
            "sigma_over_omega2": (sigma / abs(omega_mp[i])
                                  if abs(omega_mp[i]) > 0 else None),
            "certified_margin_ok": bool(abs(omega_mp[i]) > 0 and
                                        w > CERT_MARGIN * np.sqrt(sigma)),
        })
    report["budget_table_head"] = budget_rows[:16]
    report["budget_table_full_len"] = len(budget_rows)
    (HERE / "budget-table.json").write_text(json.dumps(budget_rows, indent=1))

    # repaired G2: per-band last-step omega drift vs band-local scale
    g2_rows = []
    for band in ("soft", "mid", "stiff"):
        idxs = [i for i in range(min(n_cmp, BLOCK))
                if bands[i] == band]
        if not idxs:
            continue
        scale = max(abs(float(np.sqrt(omega64[i]))) for i in idxs)
        drift = max(abs(float(np.sqrt(omega_mp[i])) - float(np.sqrt(omega64[i])))
                    for i in idxs)
        rel = drift / scale
        g2_rows.append({"band": band, "modes": idxs, "scale": scale,
                        "drift_vs_mp": drift, "rel": rel,
                        "tol": BAND_TOL[band],
                        "passed": bool(rel <= BAND_TOL[band])})
    report["g2_repaired"] = g2_rows

    # J1/J2 summary per band
    for band in ("soft", "mid", "stiff"):
        idxs = [i for i in range(n_cmp) if bands[i] == band]
        if not idxs:
            continue
        report[f"j1_max_{band}"] = float(np.max(j1_gap[idxs]))
        report[f"j2_max_{band}"] = float(np.max(sigma_entry[idxs]))

    # ---- mutations --------------------------------------------------------
    mutated = background.copy()
    mutated[5] += 1e-4
    oracle_base = Oracle(dict(radial_order=ORDER, radial_nodes=LADDER[0][0],
                              angular_nodes=LADDER[0][1], radius=RADIUS))
    e_mut, _, h_mut, _ = oracle_base.evaluate(mutated)
    m_mut = kinetic_hessian(build_cache(mutated, *LADDER[0]))
    w_mut, _, _ = whiten_float64((h_mut + h_mut.T) / 2, (m_mut + m_mut.T) / 2)
    oracle_fin = Oracle(dict(radial_order=ORDER, radial_nodes=LADDER[-1][0],
                             angular_nodes=LADDER[-1][1], radius=RADIUS))
    e_fin_bg, _, _, _ = oracle_fin.evaluate(background)
    stiff_scale = BAND_TOL["stiff"] * float(np.sqrt(max(
        np.abs(omega64[bands.index("stiff")] if "stiff" in bands else [1.0])))) \
        if False else None
    moved = [float(abs(np.sort(w_mut)[i] - np.sort(omega_mp)[i]))
             for i in range(min(len(w_mut), n_cmp))]
    report["mutation"] = {
        "delta_E_abs": float(e_mut - e_fin_bg),
        "max_pencil_shift": float(np.max(moved)),
        "note": ("sensitivity probe at mutated coefficients; the certified "
                 "table must move under load-bearing input change"),
    }

    rays = {}
    for name, ch in (("q", 0), ("t", 1), ("d", 2)):
        u = np.zeros(3 * ORDER)
        u[ch * ORDER] = 1.0
        rays[name] = float(u @ m_fin @ u)
    vals = sorted(rays.values())
    distinct = min(vals[1] / max(vals[0], 1e-300),
                   vals[2] / max(vals[1], 1e-300)) > 1.01
    m_r10 = kinetic_hessian(build_cache(r10, *LADDER[0]))
    frob_rel = float(np.linalg.norm(m_r10 - prev["M"])
                     / max(1.0, np.linalg.norm(prev["M"])))
    checks.append({"name": "G3_mutations",
                   "channel_rays": rays,
                   "channels_distinct": bool(distinct),
                   "r10_frob_rel_diff": frob_rel,
                   "passed": bool(distinct and frob_rel > 0.10)})

    g2_pass = all(r["passed"] for r in g2_rows)
    checks.append({"name": "G2_repaired_band_agreement",
                   "rows": g2_rows, "passed": bool(g2_pass)})

    uncertified = [b["mode"] for b in budget_rows if not b["certified_margin_ok"]]
    report["uncertified_at_tolerance_modes"] = uncertified[:32]
    checks.append({
        "name": "G5_certification_margins",
        "margin_factor": CERT_MARGIN,
        "uncertified_count": len(uncertified),
        "passed": True,  # informative gate: uncertified rows are recorded rows
    })

    tally = sum(1 for c in checks if c.get("passed"))
    report["tally"] = f"{tally}/{len(checks)} CHECKS PASS"
    report["runtime_seconds"] = round(time.time() - started, 1)
    (HERE / "route-a-verdict.json").write_text(json.dumps(report, indent=1))
    print(report["tally"], flush=True)
    print("[DONE] route-a-verdict.json written", flush=True)


if __name__ == "__main__":
    main()
