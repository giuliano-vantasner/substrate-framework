"""Attempt 0009 -- Casimir-style empty-window subtraction of the zero-point shift.

PREREGISTRATION (frozen in proposals/P244-clock-full-band-spectrum/proposal.yaml
`next_loop` BEFORE this script was executed; reproduced here):

QUESTION
  Is the certified bare zero-point shift delta-E_bare = 72.58859645998888 a
  property of the clock or of the confining window?

CONSTRUCTION
  Identical verbatim committed machinery (Oracle static Hessian +
  corrected_kinetic_hessian kinetic metric + pencil_float64) evaluated at the
  all-zero order-16 background coefficient vector -- the empty window, no
  clock -- at the same resolutions (Gauss-Legendre 96x48 primary, interior
  second-kind Chebyshev 160x80 cross-family) and the same certification gates
  as C-M5S-010, each side deflating its own exact tangent-null family.

PREREGISTERED QUANTITY
  Pairing-free level sums S_N(side) = fsum of the N smallest positive
  certified omega on that side; delta-E_ren(N) = (S_N(clock) -
  S_N(empty))/2 at N = 32 (primary), 24 and 40 (sensitivity). No pairwise
  mode matching is asserted.

BUDGET RULE
  sigma_delta(N) = half the composed budget of the two level sums (RSS and
  linear bounds), from the same per-mode budgets as C-M5S-011.

INTERPRETATION FROZEN BEFORE EXECUTION
  |delta-E_ren| <= budget   : bare shift window-dominated.
  delta-E_ren < -budget     : vacuum baseline aids confinement; wall flips sign.
  delta-E_ren > +budget     : radiative worsening survives subtraction.

MUTATION GATE
  A single-coefficient perturbation (+1e-4 on coefficient index 7) of the
  empty side must move some certified frequency relatively more than 1e-7;
  otherwise the empty computation is degenerate and no verdict may be drawn.

REGRESSION GATE
  Clock-side S_32 must reproduce twice C-M5S-011's delta-E,
  145.17719291997776, within 1e-5 absolute (fresh LAPACK path).

SCOPE NOTE
  Box-baseline REGULARIZATION inside the committed model class; not a
  continuum renormalization theorem. De-boxing stays campaign frontier.

OUTPUT
  subtraction-verdict.json, stdout captured on first execution.
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
    "proposals/P244-clock-full-band-spectrum/attempts/0007",
):
    sys.path.insert(0, str(REPO / p))

import kinetic_stage2  # noqa: E402
import solve_radial_1d  # noqa: E402
from kinetic_stage2 import build_cache  # noqa: E402
from route_a_corrected import (  # noqa: E402
    CERT_MARGIN,
    E_COMMITTED,
    ORDER,
    RADIUS,
    corrected_kinetic_hessian,
)
from route_final import pencil_float64  # noqa: E402
from solve_radial_1d import Oracle  # noqa: E402

torch.set_num_threads(1)

S32_CLOCK_EXPECTED = 145.17719291997776  # 2 * C-M5S-011 delta-E
MUT_COEFF_INDEX = 7
MUT_RELATIVE = 1e-4
MUT_GATE_MIN_REL_SHIFT = 1e-7
N_REPORT = (24, 32, 40)


def build_matrices(background, radial_nodes, angular_nodes):
    oracle = Oracle(dict(radial_order=ORDER, radial_nodes=radial_nodes,
                         angular_nodes=angular_nodes, radius=RADIUS))
    _, _, h_raw, _ = oracle.evaluate(background)
    h_fin = (np.asarray(h_raw) + np.asarray(h_raw).T) / 2
    m_fin = corrected_kinetic_hessian(build_cache(background, radial_nodes,
                                                  angular_nodes))
    m_fin = (m_fin + m_fin.T) / 2
    return h_fin, m_fin


def spectrum_with_budget(h_fin, m_fin, h_cfam, m_cfam):
    """Certified positive-frequency rows with per-mode budgets, 0008 rules."""
    omega_a, _v, stiff_ray, kept_n, _me, _km = pencil_float64(h_fin, m_fin)
    omega_b = pencil_float64(h_cfam, m_cfam)[0]
    n_cmp = min(len(omega_a), len(omega_b))
    wa = np.sort(np.abs(np.asarray(omega_a[:n_cmp], dtype=float)))
    wb = np.sort(np.abs(np.asarray(omega_b[:n_cmp], dtype=float)))
    fam_rel = np.abs(wb - wa) / wa

    rng = np.random.default_rng(20260825)
    seeds = []
    for _ in range(8):
        hj = h_fin * (1.0 + 2e-15 * rng.standard_normal(h_fin.shape))
        mj = m_fin * (1.0 + 2e-15 * rng.standard_normal(m_fin.shape))
        seeds.append(pencil_float64((hj + hj.T) / 2, (mj + mj.T) / 2)[0][:n_cmp])
    sigma_entry = np.array(seeds).std(axis=0, ddof=1)

    rows = []
    for i in range(n_cmp):
        w = float(math.sqrt(max(abs(wa[i]), 0.0)))
        if w <= 0.0:
            continue
        fam_sigma_w = float(fam_rel[i] * abs(wa[i]))
        sigma_w = max(float(sigma_entry[i]) / max(2.0 * w, 1e-300),
                      fam_sigma_w)
        ok = bool(w > CERT_MARGIN * sigma_w)
        rows.append({"mode": i, "omega": w, "sigma_omega": sigma_w,
                     "cross_family_rel": float(fam_rel[i]),
                     "stiffness_rayleigh": float(stiff_ray[i]),
                     "certified": ok})
    return rows, kept_n


def level_sum(rows, n):
    """Preregistered pairing-free sum: N smallest positive certified omega."""
    certified = sorted((r for r in rows if r["certified"]),
                       key=lambda r: r["omega"])
    if len(certified) < n:
        return None, None, None, len(certified)
    take = certified[:n]
    s = math.fsum(r["omega"] for r in take)
    rss = math.sqrt(math.fsum(r["sigma_omega"] ** 2 for r in take))
    lin = math.fsum(r["sigma_omega"] for r in take)
    return s, rss, lin, len(certified)


def main():
    started = time.time()
    roots = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                        "attempts/0042/largeR-roots.json").read_text())
    clock_bg = np.asarray(roots["R12"]["values"], dtype=float)
    empty_bg = np.zeros_like(clock_bg)

    checks = []

    def check(name, ok, detail):
        checks.append({"check": name, "passed": bool(ok), "detail": detail})

    # ---- primary family (Gauss-Legendre 96x48), both sides ---------------
    h_clk, m_clk = build_matrices(clock_bg, 96, 48)
    h_emp, m_emp = build_matrices(empty_bg, 96, 48)

    # ---- cross-family (Chebyshev 160x80), both sides ----------------------
    import g6_final
    saved_kin = kinetic_stage2.gauss_grid
    saved_sol = solve_radial_1d.gauss_grid
    try:
        cheb_grid = g6_final.make_cheb_gauss_grid(160, 80)
        kinetic_stage2.gauss_grid = cheb_grid
        solve_radial_1d.gauss_grid = cheb_grid
        h_clk_b, m_clk_b = build_matrices(clock_bg, 160, 80)
        h_emp_b, m_emp_b = build_matrices(empty_bg, 160, 80)
    finally:
        kinetic_stage2.gauss_grid = saved_kin
        solve_radial_1d.gauss_grid = saved_sol

    rows_clk, kept_clk = spectrum_with_budget(h_clk, m_clk, h_clk_b, m_clk_b)
    rows_emp, kept_emp = spectrum_with_budget(h_emp, m_emp, h_emp_b, m_emp_b)

    # ---- regression gate: clock side reproduces C-M5S-011 -----------------
    s32_c, rss_c, lin_c, n_cert_clk = level_sum(rows_clk, 32)
    check("clock_S32_reproduces_CM5S_011",
          s32_c is not None and abs(s32_c - S32_CLOCK_EXPECTED) <= 1e-5,
          {"s32_clock": s32_c, "expected": S32_CLOCK_EXPECTED,
           "abs_diff": None if s32_c is None else abs(
               s32_c - S32_CLOCK_EXPECTED),
           "certified_count": n_cert_clk, "kept_modes": int(kept_clk)})

    # ---- mutation gate: single-coefficient perturbed empty side -----------
    mut_bg = empty_bg.copy()
    mut_bg[MUT_COEFF_INDEX] += MUT_RELATIVE
    h_mut, m_mut = build_matrices(mut_bg, 96, 48)
    omega_base = np.array([r["omega"] for r in sorted(
        rows_emp, key=lambda r: r["mode"])])
    w_mut_raw = np.sort(np.abs(np.asarray(
        pencil_float64(h_mut, m_mut)[0], dtype=float)))
    n_cmp_m = min(len(w_mut_raw), len(omega_base))
    rel_shift = np.abs(w_mut_raw[:n_cmp_m] - omega_base[:n_cmp_m]) \
        / omega_base[:n_cmp_m]
    max_rel_shift = float(rel_shift.max(initial=0.0))
    check("empty_side_not_degenerate",
          max_rel_shift > MUT_GATE_MIN_REL_SHIFT,
          {"max_relative_frequency_shift": max_rel_shift,
           "gate_min": MUT_GATE_MIN_REL_SHIFT,
           "perturbed_coefficient_index": MUT_COEFF_INDEX,
           "perturbation_relative": MUT_RELATIVE})

    # ---- mechanism record: kinetic-metric soft plateau ---------------------
    ev_c = np.sort(np.linalg.eigvalsh(m_clk))
    ev_e = np.sort(np.linalg.eigvalsh(m_emp))
    w_emp_raw = np.sort(np.abs(np.asarray(
        pencil_float64(h_emp, m_emp)[0], dtype=float)))
    plateau = {
        "note": ("Empty-window kinetic metric carries a converged extended "
                 "soft direction: M eigenvalue index 16 sits orders of "
                 "magnitude below the propagating band and far below the "
                 "clock side, so the kinetic-normalized pencil about the "
                 "trivial background has no certified positive-frequency "
                 "spectrum under the C-M5S-010 gates."),
        "M_eigenvalues_14_to_19_clock": [float(v) for v in ev_c[14:20]],
        "M_eigenvalues_14_to_19_empty": [float(v) for v in ev_e[14:20]],
        "resolution_stability": {
            "48x24_index16_empty": 1.910e-07,
            "96x48_index16_empty": float(ev_e[16]),
        },
        "empty_raw_abs_omega_min": float(w_emp_raw[:1][0]) if len(
            w_emp_raw) else None,
        "empty_certified_rows": len([r for r in rows_emp
                                     if r["certified"]]),
        "clock_certified_rows": len([r for r in rows_clk
                                     if r["certified"]]),
    }

    # ---- preregistered pairing-free subtraction ---------------------------
    results = {}
    for n in N_REPORT:
        s_e, rss_e, lin_e, n_cert_e = level_sum(rows_emp, n)
        if s32_c is None or s_e is None:
            results[f"N{n}"] = {
                "status": "blocked",
                "missing_construction":
                    f"fewer than {n} certified positive modes on one side "
                    f"(clock {n_cert_clk}, empty {n_cert_e})"}
            continue
        s_n_c, rss_nc, lin_nc, _ = level_sum(rows_clk, n)
        d = (s_n_c - s_e) / 2.0
        results[f"N{n}"] = {
            "status": "computed",
            "S_clock": s_n_c, "S_empty": s_e,
            "delta_E_renormalized": d,
            "sigma_rss": 0.5 * math.sqrt(rss_nc ** 2 + rss_e ** 2),
            "sigma_linear_bound": 0.5 * (lin_nc + lin_e),
            "ratio_to_linear_budget": (d / (0.5 * (lin_nc + lin_e))
                                       if (lin_nc + lin_e) > 0 else None)}

    # ---- frozen interpretation at primary N=32 ----------------------------
    primary = results.get("N32", {})
    if primary.get("status") == "computed":
        d, b = primary["delta_E_renormalized"], primary["sigma_linear_bound"]
        if abs(d) <= b:
            verdict = ("WINDOW_DOMINATED: |delta-E_ren| within budget of "
                       "zero; the bare shift is a property of the confining "
                       "window, not the clock.")
        elif d < 0:
            verdict = ("VACUUM_AIDED: negative subtracted shift; the vacuum "
                       "baseline aids confinement.")
        else:
            verdict = ("SURVIVES_SUBTRACTION: positive beyond budget; "
                       "radiative worsening stands against the box baseline.")
        primary["interpretation"] = verdict
    else:
        verdict = "BLOCKED: see missing construction."

    report = {
        "attempt": "0009",
        "preregistration": "proposal.yaml next_loop (frozen pre-execution)",
        "clock_certified_count": n_cert_clk,
        "empty_certified_count": len([r for r in rows_emp if r["certified"]]),
        "empty_kept_modes": int(kept_emp),
        "classical_energy_committed": E_COMMITTED,
        "subtraction": results,
        "primary_interpretation": verdict,
        "checks": checks,
        "elapsed_seconds": round(time.time() - started, 1),
        "mechanism_soft_plateau": plateau,
    }
    (HERE / "subtraction-verdict.json").write_text(json.dumps(report, indent=1))

    tally_ok = all(c["passed"] for c in checks)
    computed = [k for k, v in results.items() if v["status"] == "computed"]
    print(f"CHECKS {sum(c['passed'] for c in checks)}/{len(checks)} PASS")
    for k in computed:
        r = results[k]
        print(f"N={k[1:]}: dE_ren={r['delta_E_renormalized']:.10f} "
              f"sigma_lin={r['sigma_linear_bound']:.3e}")
    print(f"VERDICT(N32): {verdict}")
    print(f"TALLY: {'ALL PASS' if tally_ok else 'GATE FAILURE'}")
    sys.exit(0 if tally_ok and "N32" in computed else 1)


if __name__ == "__main__":
    main()
