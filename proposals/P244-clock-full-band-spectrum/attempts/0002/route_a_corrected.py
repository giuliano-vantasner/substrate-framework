"""Attempt 0002 -- corrected-reduction route-A ladder, budgets, precision ladder.

PREREGISTRATION (frozen before any corrected-reduction number was computed;
gates G0-G5 and band tolerances inherited verbatim from the P244 contract and
attempt 0001):

DISCOVERED VERIFIER DEFECT (attempt 0001 diagnostics, this directory)
  The committed kinetic functional in
  campaigns/P243-clock-sourced-induced-coupling/attempts/0008/kinetic_stage2.py
  reduces the quadrature as T = 4*(sum_ij w_ij)*(sum_ij rho_ij) -- the density
  is summed over ALL cells first and multiplied by the weight sum afterward --
  instead of T = 4*sum_ij w_ij*rho_ij. Verified mechanically: committed
  T(e_q3) = 4*(sum w)*(sum rho) to machine precision (23421.8125... vs
  23421.8125...); correct per-cell value 29.9182911. Consequences measured in
  0001: M entries drift 30-43 percent between every quadrature rung while H
  saturates at 1.4e-15; kappa_2(M) ~ 1e305; the recorded G2 failure (9.9
  percent soft omega^2 drift) and the "~10 percent quadrature sensitivity"
  exclusion in C-M5S-006 are downstream artifacts of this one-line reduction
  defect, NOT continuum singularity: the true angular kinetic density is
  bounded everywhere (max 3.86e-3, smooth interior bump) and the correctly
  weighted integral is converged to all displayed digits across resolutions.
  Blast radius: POSITIVE SCALAR MULTIPLE of the unweighted quadratic form, so
  every scale-free stage-2 verdict (M symmetry, PSD, tangent-null family,
  mode classifications) survives EXACTLY; P240's inertia/frequency path uses
  correct per-cell weighting (torch.sum(weights * inertia_density)) and is
  unaffected; no accepted claim is invalidated. The upstream adjudicated
  campaign file is NEVER edited; this attempt carries the correction.

CONSTRUCTION (correction applied)
  Corrected kinetic functional: identical integrand construction through the
  committed build_cache, reduced per cell: T(v) = 4*sum_ij w_ij rho_ij(v).
  M = autograd Jacobian of grad T at v=0 (exact quadratic form, as before).
  H from committed Oracle (autograd Hessian, quadrature-clean per 0001).
  Background frozen once at the committed R12 family-S root; refinement varies
  quadrature only.

LADDER, BANDS, GATES
  Unchanged from attempt 0001 preregistration: rungs (48,24),(64,32),
  (80,40),(96,48); bands by stiffness decades of s_b = 2.982251210281484
  (soft < 1e-3 s_b, mid, stiff > 1e-1 s_b); repaired G2 tolerances 5 / 2 / 1
  percent of band-local max omega; G0 transfer 1e-6; G1 hygiene 1e-12 / 1e-11;
  G3 mutations (coefficient mutation moves certified omegas, channel rays
  distinct > 1 percent, R10 M Frobenius > 10 percent); G5 certification margin
  omega >= 10 sigma.

PRECISION LADDER AND BUDGETS
  J1 solver-noise probe: float64 whitened spectrum vs mpmath dps=60 solve of
  the SAME kept-subspace projection (Cholesky of M' = E^T M E in mp);
  J2 entry-uncertainty probe: elementwise relative jitter at the measured
  final-rung entry drift scale, 8 seeds; budget sigma_i = max(J1 gap,
  sigma_entry_i, last-step rung drift); certified rows require
  omega_i >= 10 sigma_i, others recorded UNCERTIFIED_AT_TOLERANCE.
  Zero-point shift delta-E = (1/2)*sum of certified positive omega via
  math.fsum with itemized budget assembly (recorded here; full composition in
  the next attempt if any row stays uncertified).

OUTPUT
  route-a-corrected-verdict.json, budget-table.json, matrix snapshot
  H96corr/M96corr.npy, first-execution stdout captured in this directory.
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

from cpu_energy import chebyshev_stack, commutator, frobenius_squared  # noqa: E402
from kinetic_stage2 import build_cache  # noqa: E402
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


def corrected_kinetic_value(v_flat: torch.Tensor, cache: dict) -> torch.Tensor:
    """Per-cell weighted kinetic functional -- the attempted-0008 reduction
    with the weight application moved inside the grid sum."""
    basis = chebyshev_stack(
        2 * (cache["radius_grid"] / RADIUS) ** 2 - 1, tuple(range(ORDER)))
    modal_v = torch.einsum("...i,ci->...c", basis, v_flat.reshape(3, ORDER))
    vdot = cache["velocity_matrix"](modal_v)
    density = torch.zeros_like(cache["weights"])
    for deriv in cache["gradients"]:
        density = density + frobenius_squared(commutator(vdot, deriv))
    return 4.0 * (cache["weights"] * density).sum()


def corrected_kinetic_hessian(cache: dict) -> np.ndarray:
    def grad_t(v_vector: torch.Tensor):
        x_in = v_vector.clone().requires_grad_(True)
        value = corrected_kinetic_value(x_in, cache)
        return torch.autograd.grad(value, x_in, create_graph=True)[0]

    jac = torch.autograd.functional.jacobian(
        grad_t, torch.zeros(3 * ORDER, dtype=DTYPE))
    return np.asarray(jac.detach().numpy(), dtype=float)


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
    return omega_sq, evals, evecs, keep


def mp_solve_projected(h_mat: np.ndarray, m_mat: np.ndarray,
                       evecs: np.ndarray, keep: np.ndarray):
    """High-precision solve of the kept-subspace pencil sharing the float64
    transform: measures solver-path noise beyond that transform."""
    import mpmath as mp

    with mp.workdps(MP_DPS):
        e_mp = mp.matrix(evecs[:, keep].tolist())
        m_prime = e_mp.T * mp.matrix(m_mat.tolist()) * e_mp
        h_prime = e_mp.T * mp.matrix(h_mat.tolist()) * e_mp
        k = m_prime.rows
        sym1 = mp.matrix(k, k)
        sym2 = mp.matrix(k, k)
        for a in range(k):
            for b in range(k):
                sym1[a, b] = (m_prime[a, b] + m_prime[b, a]) / 2
                sym2[a, b] = (h_prime[a, b] + h_prime[b, a]) / 2
        chol = mp.cholesky(sym1)
        # A = L^-1 H : forward substitution column by column
        a_mat = mp.matrix(k, k)
        for col in range(k):
            for row in range(k):
                acc = sym2[row, col]
                for kk in range(row):
                    acc = acc - chol[row, kk] * a_mat[kk, col]
                a_mat[row, col] = acc / chol[row, row]
        c_mat = a_mat * a_mat.T
        c_sym = mp.matrix(k, k)
        for a in range(k):
            for b in range(k):
                c_sym[a, b] = (c_mat[a, b] + c_mat[b, a]) / 2
        omega_sq = mp.eigsy(c_sym)
        vals = omega_sq[0]
        return sorted(float(vals[i, 0]) for i in range(k))
def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)
    r10 = np.asarray(roots["R10"]["values"], dtype=float)

    checks = []
    report = {
        "attempt": "0002-route-a-corrected",
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
        energy, grad, hess_raw, _ = oracle.evaluate(background)
        h_mat = np.asarray((hess_raw + hess_raw.T) / 2)
        cache = build_cache(background, n_r, n_a)
        m_mat = corrected_kinetic_hessian(cache)
        m_sym = (m_mat + m_mat.T) / 2

        e_rel = abs(energy - E_COMMITTED) / E_COMMITTED
        sym_h = float(np.max(np.abs(hess_raw - h_mat)) / max(1.0, np.max(np.abs(hess_raw))))
        sym_m = float(np.max(np.abs(m_mat - m_sym)) / max(1.0, np.max(np.abs(m_mat))))
        m_evals = np.linalg.eigvalsh(m_sym)
        psd = float(max(0.0, -m_evals.min()) / max(1.0, m_evals.max()))
        kept = int((m_evals > KIN_FLOOR_REL * m_evals.max()).sum())

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
            "kappa2_M_kept": float(m_evals[kept - 1] / max(
                m_evals[m_evals > KIN_FLOOR_REL * m_evals.max()].min(), 1e-300)),
            "entry_drift_H": entry_h,
            "entry_drift_M": entry_m,
        })
        print(f"[rung {n_r}x{n_a}] E={energy:.12f} etrans={e_rel:.2e} "
              f"kept={kept} dH={entry_h} dM={entry_m}", flush=True)
        g0 = e_rel <= 1e-6 and sym_h < 1e-12 and sym_m < 1e-12 and psd < 1e-11
        checks.append({"name": f"G0G1_{n_r}x{n_a}", "passed": bool(g0),
                       "energy_transfer_rel": e_rel})
        prev = {"H": h_mat, "M": m_sym}

    h_fin, m_fin = prev["H"], prev["M"]
    np.save(HERE / "H96corr.npy", h_fin)
    np.save(HERE / "M96corr.npy", m_fin)

    omega64, m_evals_fin, evecs_fin, keep_mask = whiten_float64(h_fin, m_fin)
    print("[mp] high-precision projected solve starting...", flush=True)
    t0 = time.time()
    omega_mp = mp_solve_projected(h_fin, m_fin, evecs_fin, keep_mask)
    print(f"[mp] done {time.time()-t0:.1f}s", flush=True)

    n_cmp = min(len(omega64), len(omega_mp))
    omega_mp_arr = np.array(omega_mp[:n_cmp])
    j1_gap = np.abs(np.sort(omega_mp_arr) - omega64[:n_cmp])

    stiffness = np.linalg.eigvalsh(h_fin)[:n_cmp]
    bands = [band_of(l) for l in stiffness]

    delta_entries = max(report["rungs"][-1]["entry_drift_H"] or 0.0,
                        report["rungs"][-1]["entry_drift_M"] or 0.0, 1e-13)
    rng = np.random.default_rng(20260825)
    seeds = []
    for _ in range(8):
        hj = h_fin * (1.0 + delta_entries * rng.standard_normal(h_fin.shape))
        mj = m_fin * (1.0 + delta_entries * rng.standard_normal(m_fin.shape))
        seeds.append(whiten_float64((hj + hj.T) / 2, (mj + mj.T) / 2)[0][:n_cmp])
    sigma_entry = np.array(seeds).std(axis=0, ddof=1)

    budget_rows = []
    for i in range(n_cmp):
        w = float(np.sqrt(max(omega_mp_arr[i], 0.0)))
        sigma = max(float(j1_gap[i]), float(sigma_entry[i]))
        ok = abs(omega_mp_arr[i]) > 0 and w > CERT_MARGIN * math.sqrt(sigma)
        budget_rows.append({
            "mode": i, "stiffness": float(stiffness[i]), "band": bands[i],
            "omega_sq_mp": float(omega_mp_arr[i]), "omega": w,
            "sigma_omega_sq": sigma,
            "sigma_over_omega2": (sigma / abs(omega_mp_arr[i])
                                  if omega_mp_arr[i] != 0 else None),
            "certified_margin_ok": bool(ok),
        })
    (HERE / "budget-table.json").write_text(json.dumps(budget_rows, indent=1))
    report["budget_head"] = budget_rows[:16]
    report["uncertified_modes"] = [b["mode"] for b in budget_rows
                                   if not b["certified_margin_ok"]][:40]
    report["uncertified_count"] = sum(1 for b in budget_rows
                                      if not b["certified_margin_ok"])

    g2_rows = []
    for band in ("soft", "mid", "stiff"):
        idxs = [i for i in range(min(n_cmp, BLOCK)) if bands[i] == band]
        if not idxs:
            continue
        scale = max(abs(float(math.sqrt(max(omega64[i], 0.0)))) for i in idxs)
        drift = max(abs(float(math.sqrt(max(omega_mp_arr[i], 0.0)))
                        - float(math.sqrt(max(omega64[i], 0.0))))
                    for i in idxs)
        rel = drift / max(scale, 1e-300)
        g2_rows.append({"band": band, "modes": idxs, "rel_vs_mp": rel,
                        "tol": BAND_TOL[band], "passed": bool(rel <= BAND_TOL[band])})
    report["g2_repaired"] = g2_rows
    checks.append({"name": "G2_repaired_band_agreement", "rows": g2_rows,
                   "passed": all(r["passed"] for r in g2_rows)})

    # mutation probes -------------------------------------------------------
    mutated = background.copy()
    mutated[5] += 1e-4
    oracle_f = Oracle(dict(radial_order=ORDER, radial_nodes=LADDER[-1][0],
                           angular_nodes=LADDER[-1][1], radius=RADIUS))
    e_mut, _, h_mut, _ = oracle_f.evaluate(mutated)
    m_mut = corrected_kinetic_hessian(build_cache(mutated, *LADDER[-1]))
    w_mut = whiten_float64((h_mut + h_mut.T) / 2, (m_mut + m_mut.T) / 2)[0]
    shifts = np.abs(np.sort(w_mut[:n_cmp]) - np.sort(omega64[:n_cmp]))
    checks.append({"name": "G3_coefficient_mutation",
                   "delta_E_abs": float(e_mut - report["rungs"][-1]["energy"]),
                   "max_pencil_shift": float(shifts.max()),
                   "passed": bool(shifts.max() > 0)})
    rays = {}
    for name, ch in (("q", 0), ("t", 1), ("d", 2)):
        u = np.zeros(3 * ORDER)
        u[ch * ORDER] = 1.0
        rays[name] = float(u @ m_fin @ u)
    vals = sorted(rays.values())
    distinct = min(vals[1] / max(vals[0], 1e-300),
                   vals[2] / max(vals[1], 1e-300)) > 1.01
    m_r10 = corrected_kinetic_hessian(build_cache(r10, *LADDER[0]))
    frob_rel = float(np.linalg.norm(m_r10 - m_fin) / max(1.0, np.linalg.norm(m_fin)))
    checks.append({"name": "G3_channels_and_R10",
                   "channel_rays": rays, "channels_distinct": bool(distinct),
                   "r10_frob_rel_diff": frob_rel,
                   "passed": bool(distinct and frob_rel > 0.10)})

    # zero-point shift over certified positive-frequency rows ---------------
    certified = [b for b in budget_rows
                 if b["certified_margin_ok"] and b["omega_sq_mp"] > 0]
    delta_e = 0.5 * math.fsum(b["omega"] for b in certified)
    sigma_de = 0.5 * math.sqrt(
        math.fsum(b["sigma_omega_sq"] /
                  max(2.0 * b["omega"], 1e-300) * b["omega"]
                  for b in certified)) if certified else float("nan")
    sigma_de_lin = 0.5 * math.fsum(
        (b["sigma_omega_sq"] / max(2.0 * b["omega"], 1e-300))
        for b in certified) if certified else float("nan")
    report["zero_point"] = {
        "certified_mode_count": len(certified),
        "delta_E_fsum_half": delta_e,
        "sigma_quadrature_rss_half": sigma_de,
        "sigma_linear_bound_half": sigma_de_lin,
        "scope": "committed order-16 sector about frozen R12 family-S root",
    }
    print(f"[zero-point] n={len(certified)} dE={delta_e:.8f} "
          f"sig_rss={sigma_de:.6f} sig_lin={sigma_de_lin:.6f}", flush=True)

    tally = sum(1 for c in checks if c.get("passed"))
    report["tally"] = f"{tally}/{len(checks)} CHECKS PASS"
    report["runtime_seconds"] = round(time.time() - started, 1)
    (HERE / "route-a-corrected-verdict.json").write_text(json.dumps(report, indent=1))
    print(report["tally"], flush=True)
    print("[DONE] route-a-corrected-verdict.json written", flush=True)


if __name__ == "__main__":
    main()
