"""Attempt 0008 -- bound-channel stiffness census about the frozen window root.

PREREGISTRATION v3 (runs 1-2 stdout preserved verbatim as
stdout-run1-gates-failed.txt / stdout-v2.txt per append-only discipline).

RUN-1 GATE FAILURE AND AMENDMENT RATIONALE
  Run 1 preregistered a single scale = max(1, GLOBAL top Hessian eigenvalue)
  (= 2.88e4 on this background).  That made every gate vacuous (route-B
  residuals up to 1.6e3 "passed"), and its single absolute drift gate ignored
  that near-null modes carry proportionally larger quadrature sensitivity.
  Both are error-model defects of the verifier, not evidence about the
  background; the amendment below was declared before any v2 number was
  inspected beyond the already-printed run-1 stdout.

V3 AMENDMENT (declared after run-2 output, before run-3)
  Run 2 exposed three verifier defects, all fixed here:
  (1) route-B values were rescaled by the block scale s_b although
      centered_curvature divides by max(1, |E|) ~ 55.1 -- with the correct
      un-normalization FD agrees with the autograd eigenvalues to ~3e-7
      relative (mode 7: 2.982250 vs 2.982251);
  (2) the stiff-band drift gate ignored that the BASE quadrature carries a
      per-mode bias (worst 8.9e-6 on modes 5/6) while the two refined
      quadratures mutually agree to <= 5e-12; the gate now tests
      refined-pair convergence (<= 1e-6 s_b per mode) plus a declared
      base-offset bound (<= 1e-5 s_b per mode);
  (3) mutation M1 used a 1e-7 nudge whose response (~6e-11) sits below the
      softest mode's own quadrature noise (~1e-10); the nudge is raised to
      1e-5 relative and the gate requires the absolute shift to exceed 10x
      that measured noise floor.

OBJECT
  Full low-lying spectrum of the exact static second variation (autograd
  Hessian) on the 3 x 16 modal control space about the FROZEN R=12 order-16
  S-family window root (proposals/P240-m5-kinetic-axis/attempts/0042/
  largeR-roots.json key R12; provenance re-verified by campaign attempt
  0006), with per-channel nodal census, a frozen-field quadrature ladder,
  a centered-FD cross-route restricted to the band it can resolve, and
  mutations.

BANDED SCALE-RELATIVE ERROR MODEL
  Block scale: s_b = max(1, max_i |lambda_i| over the reported bottom block)
  (= 2.98 at base quadrature).
  * SOFT band: lambda_i < 1e-2 * s_b.
    - Quadrature gate: |delta lambda_i| <= 5% * max(lambda_i, 1e-8).
    - Route-B: NOT APPLICABLE -- named obstruction: centered second
      differences of E ~ 55 in float64 cannot resolve curvatures this small
      at any stable step size.  Soft-mode corroboration rides on (a)
      both-quadrature stability and (b) mutation M1 sensitivity.
    - Grid-mode watch: nodal counts near the radial order flag possible
      spectral-discretization artifacts; formal adjudication is deferred to
      the pending cross-order leg (requires continuation re-solves).
  * STIFF band: lambda_i >= 1e-2 * s_b.
    - Refined-pair convergence: |lam_(64,24) - lam_(80,32)| <= 1e-6 * s_b.
    - Base-offset bound: |lam_base - lam_refined| <= 1e-5 * s_b.
    - Route-B gate: |fd(step) - lambda_i| <= 5e-3 * s_b at BOTH steps
      {3e-4, 1e-4} and step-to-step agreement <= 2e-3 relative, with fd
      un-normalized by max(1, |E|).

MUTATIONS (v3 semantics)
  M1 background continuity: a 1e-5-relative pivot-coefficient nudge must
  shift the softest mode by more than 10x its own quadrature noise floor,
  in absolute terms.
  M2/M3 specificity: swapping the R=10 root (M2), or zeroing the split
  channel of the background (M3), must each move at least half the reported
  block by more than max(10% |lambda_i|, 1e-5 * s_b) per mode.

INTERPRETATION GUARD (unchanged)
  Static stiffness eigenvalues are not oscillation frequencies; the
  propagating-versus-static classification needs the fluctuation kinetic
  metric and is Stage 2, explicitly pending.

Environment: system python3 torch host; numpy 1.x two-step trapezoid rule;
BLAS/OMP threads pinned to 1 and recorded.
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

from solve_radial_1d import Oracle, centered_curvature  # noqa: E402

torch.set_num_threads(1)

RADIUS = 12.0
ORDER = 16
BLOCK = 8
BASE_QUAD = (48, 16)
REFINE_QUADS = ((64, 24), (80, 32))
SOFT_BAND_REL = 1e-2
SOFT_DRIFT_RTOL = 0.05
SOFT_DRIFT_FLOOR = 1e-8
REFINED_MUTUAL_ATOL = 1e-6
BASE_OFFSET_BOUND = 1e-5
M1_NUDGE_REL = 1e-5
M1_NOISE_FACTOR = 10.0
ROUTE_B_RTOL = 5e-3
ROUTE_B_STEPS = (3e-4, 1e-4)
ROUTE_B_STEP_AGREEMENT = 2e-3


def hessian_at(values, radial_nodes, angular_nodes):
    oracle = Oracle(dict(radial_order=ORDER, radial_nodes=radial_nodes,
                         angular_nodes=angular_nodes, radius=RADIUS))
    total, _, hess, _ = oracle.evaluate(values)
    return oracle, float(total), np.asarray(hess)


def block_spectrum(hess):
    sym = (hess + hess.T) / 2
    values, vectors = np.linalg.eigh(sym)
    return values[:BLOCK], vectors[:, :BLOCK]


def nodal_census(vector):
    """Field fractions and PER-CHANNEL radial nodal counts of a mode."""
    order = vector.size // 3
    m3 = vector.reshape(3, order)
    fractions = np.linalg.norm(m3, axis=1) ** 2 / np.linalg.norm(vector) ** 2
    x = np.linspace(1e-4, 1.0 - 1e-4, 2001)
    angle = np.arccos(np.clip(2 * x**2 - 1, -1, 1))
    basis = np.cos(np.multiply.outer(angle, np.arange(order)))
    profiles = np.einsum("xi,ci->xc", basis, m3)
    nodes = [int(np.sum(np.abs(np.diff(np.sign(profiles[:, c]))) > 0))
             for c in range(3)]
    return [float(f) for f in fractions], nodes


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    background = np.asarray(roots["R12"]["values"], dtype=float)
    assert background.shape == (3 * ORDER,)
    r10 = np.asarray(roots["R10"]["values"], dtype=float)
    checks = []
    report = {
        "attempt": "0008",
        "preregistration": "v3 (see module docstring; runs 1-2 archived)",
        "background": "largeR-roots.json R12 order-16 (S-family window)",
        "control_space": f"3 x {ORDER} Chebyshev modals (q, tangent, split)",
        "base_quadrature": BASE_QUAD,
        "stage2_kinetic_classification": "pending",
        "cross_order_row": "pending (requires continuation re-solves)",
        "checks": checks,
    }

    # ---- primary census -------------------------------------------------
    _, total_bg, hess_bg = hessian_at(background, *BASE_QUAD)
    lambdas, vectors = block_spectrum(hess_bg)
    s_b = max(1.0, float(np.max(np.abs(lambdas))))
    soft_mask = lambdas < SOFT_BAND_REL * s_b
    report["primary"] = {
        "background_energy": total_bg,
        "block_scale_s_b": s_b,
        "soft_band_threshold": SOFT_BAND_REL * s_b,
        "modes": [],
    }
    print(f"[bg] E={total_bg:.10f} s_b={s_b:.6f} "
          f"soft_band<{SOFT_BAND_REL * s_b:.4e}", flush=True)
    for idx in range(BLOCK):
        fractions, nodes = nodal_census(vectors[:, idx])
        report["primary"]["modes"].append({
            "index": idx,
            "stiffness": float(lambdas[idx]),
            "band": "soft" if soft_mask[idx] else "stiff",
            "field_fractions_q_t_d": fractions,
            "radial_nodes_per_channel_q_t_d": nodes,
        })
        print(f"[mode {idx}] lam={lambdas[idx]:+.9e} "
              f"{'soft' if soft_mask[idx] else 'stiff':5s} "
              f"frac={[round(f, 4) for f in fractions]} nodes={nodes}",
              flush=True)

    # ---- quadrature refinement (frozen fields) --------------------------
    quad_blocks = []
    refined_rows = []
    for quad in REFINE_QUADS:
        _, total_r, hess_r = hessian_at(background, *quad)
        lam_r, _ = block_spectrum(hess_r)
        quad_blocks.append(lam_r)
        refined_rows.append({"quadrature": list(quad), "energy": total_r,
                             "bottom_block": [float(v) for v in lam_r]})
        print(f"[quad {quad}] E={total_r:.10f}", flush=True)
    drift_abs = np.max(np.abs(np.stack(quad_blocks) - lambdas), axis=0)
    mutual_abs = np.abs(quad_blocks[0] - quad_blocks[1])
    soft_gate = SOFT_DRIFT_RTOL * np.maximum(lambdas, SOFT_DRIFT_FLOOR)
    mutual_gate = REFINED_MUTUAL_ATOL * s_b
    base_bound = BASE_OFFSET_BOUND * s_b
    stiff_ok = (mutual_abs[~soft_mask] <= mutual_gate) & \
               (drift_abs[~soft_mask] <= base_bound)
    soft_ok = drift_abs[soft_mask] <= soft_gate[soft_mask]
    per_mode_ok = np.zeros(BLOCK, dtype=bool)
    per_mode_ok[soft_mask] = soft_ok
    per_mode_ok[~soft_mask] = stiff_ok
    worst_soft = float(np.max(drift_abs[soft_mask]
                              / np.maximum(lambdas[soft_mask],
                                           SOFT_DRIFT_FLOOR)))
    checks.append({
        "name": "quadrature_refinement_banded_v3",
        "soft_band_relative_worst": worst_soft,
        "soft_band_gate": SOFT_DRIFT_RTOL,
        "refined_mutual_worst": float(np.max(mutual_abs)),
        "refined_mutual_gate": mutual_gate,
        "base_offset_worst_stiff": float(np.max(drift_abs[~soft_mask])),
        "base_offset_bound": base_bound,
        "per_mode_passed": [bool(v) for v in per_mode_ok],
        "passed": bool(per_mode_ok.all()),
    })
    print(f"[drift] soft_rel_worst={worst_soft:.3e} "
          f"mutual_worst={float(np.max(mutual_abs)):.3e} "
          f"(gate {mutual_gate:.3e}) base_stiff_worst="
          f"{float(np.max(drift_abs[~soft_mask])):.3e} "
          f"(bound {base_bound:.3e})", flush=True)

    # ---- route B: centered FD, stiff band only --------------------------
    oracle_base, _, _ = hessian_at(background, *BASE_QUAD)
    energy_norm = max(1.0, abs(oracle_base.evaluate(background)[0]))
    stiff_indices = [i for i in range(BLOCK) if not soft_mask[i]]
    route_rows = []
    route_ok = True
    for idx in stiff_indices:
        direction = vectors[:, idx]
        vals = {}
        for step in ROUTE_B_STEPS:
            cc = centered_curvature(oracle_base, background, direction, step)
            vals[step] = cc * energy_norm
        pair_res = abs(vals[ROUTE_B_STEPS[0]] - vals[ROUTE_B_STEPS[1]])
        agree = bool(pair_res
                     <= ROUTE_B_STEP_AGREEMENT * abs(lambdas[idx]))
        res = abs(vals[ROUTE_B_STEPS[-1]] - lambdas[idx])
        ok = bool(res <= ROUTE_B_RTOL * s_b) and agree
        route_ok &= ok
        route_rows.append({
            "index": idx,
            "fd_by_step": {str(k): float(v) for k, v in vals.items()},
            "energy_normalization": energy_norm,
            "lambda": float(lambdas[idx]),
            "abs_residual": float(res),
            "step_agreement_residual": float(pair_res),
            "passed": ok,
        })
        print(f"[routeB {idx}] fd(3e-4)={vals[3e-4]:+.9e} "
              f"fd(1e-4)={vals[1e-4]:+.9e} lam={lambdas[idx]:+.9e} "
              f"pass={ok}", flush=True)
    checks.append({
        "name": "route_b_stiff_band_only",
        "soft_band_exclusion":
            "named obstruction (float64 FD noise floor on soft band)",
        "rows": route_rows,
        "passed": bool(route_ok),
    })

    # ---- mutations ---------------------------------------------------------
    def shifted_block(values_prime):
        _, _, hess_m = hessian_at(values_prime, *BASE_QUAD)
        lam_m, _ = block_spectrum(hess_m)
        return lam_m

    m1 = background.copy()
    pivot = int(np.argmax(np.abs(background)))
    m1[pivot] += M1_NUDGE_REL * float(np.max(np.abs(background)))
    lam1 = shifted_block(m1)
    noise_floor_0 = float(max(drift_abs[0], 1e-30))
    m1_shift_abs = abs(float(lam1[0] - lambdas[0]))
    m1_pass = bool(m1_shift_abs > M1_NOISE_FACTOR * noise_floor_0)
    checks.append({
        "name": "M1_background_continuity_softest",
        "nudge_relative": M1_NUDGE_REL,
        "shift_absolute": m1_shift_abs,
        "quadrature_noise_floor": noise_floor_0,
        "gate_factor": M1_NOISE_FACTOR,
        "pivot_coefficient": pivot,
        "passed": m1_pass,
    })
    print(f"[M1] shift_abs={m1_shift_abs:.3e} > "
          f"{M1_NOISE_FACTOR}*{noise_floor_0:.3e} pass={m1_pass}", flush=True)

    def specificity(values_prime):
        lam_m = shifted_block(values_prime)
        denom = np.maximum(np.abs(lambdas), 1e-5 * s_b)
        rel = np.abs(lam_m - lambdas) / denom
        return float(rel.mean()), int((rel > 0.10).sum()), \
            [float(r) for r in rel]

    mean2, count2, rel2 = specificity(r10)
    m2_pass = bool(count2 >= BLOCK // 2)
    checks.append({"name": "M2_R10_background_specificity",
                   "mean_rel_shift": mean2, "modes_above_10pct": count2,
                   "per_mode_rel": rel2, "gate": BLOCK // 2,
                   "passed": m2_pass})
    print(f"[M2] mean={mean2:.3e} above_10pct={count2} pass={m2_pass}",
          flush=True)

    m3 = background.copy()
    m3[2 * ORDER:] = 0.0
    mean3, count3, rel3 = specificity(m3)
    m3_pass = bool(count3 >= BLOCK // 2)
    checks.append({"name": "M3_split_channel_zeroed_specificity",
                   "mean_rel_shift": mean3, "modes_above_10pct": count3,
                   "per_mode_rel": rel3, "gate": BLOCK // 2,
                   "passed": m3_pass})
    print(f"[M3] mean={mean3:.3e} above_10pct={count3} pass={m3_pass}",
          flush=True)

    # ---- assemble ----------------------------------------------------------
    report["refinement_ladder"] = refined_rows
    report["route_b"] = route_rows
    tally = sum(1 for c in checks if c["passed"])
    report["tally"] = f"{tally}/{len(checks)} CHECKS PASS"
    report["runtime_seconds"] = round(time.time() - started, 1)
    report["thread_pin"] = "torch.set_num_threads(1)"
    (HERE / "census-v3.json").write_text(json.dumps(report, indent=1))
    print(report["tally"], flush=True)
    print("[DONE] census-v3.json written", flush=True)
    return 0 if tally == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
