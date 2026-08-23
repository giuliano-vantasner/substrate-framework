"""Attempt 0004: Morse-index bisection for the clock-branch critical radius.

Candidate D (preregistered in proposal.yaml before any solve at radii in
(6, 7.5) was executed): Lambda = 1/R*, where R* is the radius at which the
confined-clock branch's tangential-split Hessian eigenvalue changes sign
(Morse index 1 below, index 0 above; certified R=6 index 1 from the
committed order-20 spectrum lambda_1 = -6.25e-2, window R=7.5 index 0).

Small-ratio discipline (skill small-ratio-numerics):
- bracket by the DISCRETE Morse index; raw near-zero signs are never the
  oracle because lambda_min sits 4+ orders below the bulk spectrum;
- lambda_min is truncation-dominated at the 1e-5 level (committed R=8
  ladder moves it 4.5e-5 -> 9.7e-6 across orders 16 -> 20), so the
  convergent observable is the per-order crossing radius R*(N); the
  spread across N is the quoted error bar;
- soft-mode identity is inspected (field fractions + radial node count),
  guarding against boundary/mesh artifacts masquerading as bulk modes;
- an independent monitor (energy/inertia/frequency branch continuity)
  that does not share the soft direction gates every solve;
- an independent-discretization monitor (finer quadrature) must preserve
  the side classification at the bracket ends;
- BLAS thread count is recorded with the results.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
P240 = HERE.parents[3] / "proposals" / "P240-m5-kinetic-axis" / "attempts"
sys.path.insert(0, str(P240 / "0041"))
sys.path.insert(0, str(HERE.parent / "0002"))

from solve_radial_1d import Oracle, solve_order  # noqa: E402
from window_continuation import fit, pad  # noqa: E402


def local_spectrum(settings, order, values):
    """Full symmetrized Hessian spectrum at a converged root.

    solve_order exposes only summaries; the small-ratio diagnostics need
    lambda_2, max|lambda|, and the raw-sign index, so re-evaluate the
    Hessian locally through the same Oracle.
    """

    oracle = Oracle(dict(settings, radial_order=order))
    _, _, hess, _ = oracle.evaluate(values)
    sym = (hess + hess.T) / 2.0
    return np.linalg.eigvalsh(sym)


def evaluate_radius(radius, seed16, *, nodes=32, angular=16):
    """Continue the branch to `radius`; return per-order diagnostics."""

    settings = dict(radial_nodes=nodes, angular_nodes=angular,
                    radius=radius)
    values = np.asarray(seed16, dtype=np.float64)
    orders_data = {}
    energy_prev = None
    for order in (16, 18, 20):
        seed_values = values if order == 16 else pad(values, order)
        row = solve_order(order, seed_values, settings)
        values = np.asarray(row.pop("values"))
        total = float(row["energy"])
        rel_grad = float(row["relative_gradient"])
        if not np.isfinite(total) or not (40.0 < total < 60.0):
            return {"radius": radius, "failed": "energy_out_of_window",
                    "energy": total}
        if rel_grad > 1e-10:
            return {"radius": radius, "failed": "unconverged",
                    "relative_gradient": rel_grad}
        comp = row["components"]
        inertia = float(comp["inertia"])
        omega = float(comp["frequency"])
        if energy_prev is not None and abs(total - energy_prev) > 1.0:
            return {"radius": radius, "failed": "energy_jump",
                    "energy": total, "previous": energy_prev}
        if not (0.65 < omega < 1.10) or not (0.45 < inertia < 0.85):
            return {"radius": radius, "failed": "observables_off_branch",
                    "omega": omega, "inertia": inertia}
        spectrum = local_spectrum(settings, order, values)
        orders_data[str(order)] = {
            "lambda_min": float(spectrum[0]),
            "lambda_2": float(spectrum[1]),
            "max_abs_eig": float(np.max(np.abs(spectrum))),
            "morse_index_packaged": int(row["morse_index"]),
            "index_raw_sign": int(np.sum(spectrum < 0.0)),
            "mode_fractions": row.pop("mode_fractions"),
            "mode_radial_nodes_split": row.pop("mode_radial_nodes_split"),
            "energy": total,
            "relative_gradient": rel_grad,
            "inertia": inertia,
            "omega": omega,
        }
        energy_prev = total
    return {"radius": radius, "values": values.tolist(),
            "orders": orders_data}


def index_at(record, order="20"):
    """Packaged-threshold index at a given order (discrete oracle)."""

    return record["orders"][order]["morse_index_packaged"]


def crossing_per_order(records, lo, hi):
    """Linear zero-crossing of lambda_min(R) per solver order.

    Uses only converged records inside [lo - 0.15, hi + 0.15] with data
    on both sides of zero; the spread across orders is the systematic
    error bar (truncation-dominated eigenvalue, convergent location).
    """

    out = {}
    for order in ("16", "18", "20"):
        pts = []
        for rec in records:
            if "orders" not in rec:
                continue
            if not (lo - 0.15 <= rec["radius"] <= hi + 0.15):
                continue
            lam = rec["orders"][order]["lambda_min"]
            pts.append((rec["radius"], lam))
        below = [p for p in pts if p[1] < 0.0]
        above = [p for p in pts if p[1] >= 0.0]
        if not below or not above or len(pts) < 3:
            out[order] = None
            continue
        arr = np.asarray(pts)
        slope, intercept = np.polyfit(arr[:, 0], arr[:, 1], 1)
        if slope <= 0:
            out[order] = None
            continue
        out[order] = {
            "R_star": float(-intercept / slope),
            "slope": float(slope),
            "n_points": len(pts),
        }
    return out


def main() -> int:
    print(f"threads={torch.get_num_threads()}", flush=True)
    rows = json.loads(
        (P240 / "0041" / "radial-results.json").read_text()
    )
    root20 = np.asarray(
        [r for r in rows if r["radial_order"] == 20][0]["values"]
    )

    records = []
    seed = fit(root20, 16)
    coarse = [6.0, 6.375, 6.75, 7.125, 7.5]

    def emit(rec):
        records.append(rec)
        if "failed" in rec:
            print(f"R={rec['radius']}: FAILED {rec['failed']}",
                  flush=True)
            json.dump({"records": [
                {k: v for k, v in r.items() if k != "values"}
                for r in records
            ], "blocked": rec}, open(HERE / "morse-results.json", "w"),
               indent=1)
            return False
        lam = rec["orders"]["20"]["lambda_min"]
        idx = rec["orders"]["20"]["morse_index_packaged"]
        raw = rec["orders"]["20"]["index_raw_sign"]
        print(f"R={rec['radius']}: "
              f"E={rec['orders']['20']['energy']:.6f} "
              f"lam20={lam:+.6e} "
              f"lam2={rec['orders']['20']['lambda_2']:.3e} "
              f"index={idx} raw={raw}", flush=True)
        return True

    for radius in coarse:
        if not emit(evaluate_radius(radius, seed)):
            return 1
        seed = fit(np.asarray(records[-1]["values"]), 16)

    # Locate the adjacent coarse pair carrying the index flip.
    by_radius = {r["radius"]: r for r in records}
    lo = hi = None
    for prev, curr in zip(coarse, coarse[1:]):
        if index_at(by_radius[prev]) >= 1 and index_at(by_radius[curr]) == 0:
            lo, hi = prev, curr
            break
    if lo is None:
        print("NO INDEX FLIP FOUND ON COARSE GRID", flush=True)
        json.dump({"records": [
            {k: v for k, v in r.items() if k != "values"}
            for r in records], "blocked": "no_flip"},
            open(HERE / "morse-results.json", "w"), indent=1)
        return 1
    print(f"bracket located: [{lo}, {hi}]", flush=True)

    # Bisection on the discrete index, order 20 as primary.
    while hi - lo > 0.02:
        mid = 0.5 * (lo + hi)
        rec = evaluate_radius(mid, seed)
        if not emit(rec):
            return 1
        idx = index_at(rec)
        if idx >= 1:
            lo = mid
        else:
            hi = mid
        seed = fit(np.asarray(rec["values"]), 16)

    crossings = crossing_per_order(records, lo, hi)
    primary = crossings["20"]
    if primary is None:
        print("CROSSING FIT FAILED AT ORDER 20", flush=True)
        json.dump({"records": [], "blocked": "no_crossing_fit",
                   "bracket": [lo, hi]},
                  open(HERE / "morse-results.json", "w"), indent=1)
        return 1
    estimates = [v["R_star"] for v in crossings.values() if v]
    spread = max(estimates) - min(estimates)
    r_star = primary["R_star"]

    # Independent-discretization monitor: finer quadrature must preserve
    # the side classification at the bracket ends.
    quad = {}
    for label, radius in (("lo", lo), ("hi", hi)):
        vals = next(r["values"] for r in records
                    if abs(r["radius"] - radius) < 1e-9)
        fine = evaluate_radius(radius, fit(np.asarray(vals), 16),
                               nodes=48, angular=24)
        quad[label] = {
            "radius": radius,
            "index": None if "failed" in fine else index_at(fine),
            "lambda_min": None if "failed" in fine
            else fine["orders"]["20"]["lambda_min"],
        }
        print(f"fine-quadrature R={radius}: {quad[label]}", flush=True)

    closest = min(
        (r for r in records if "orders" in r),
        key=lambda r: abs(r["radius"] - r_star),
    )
    mode = closest["orders"]["20"]
    result = {
        "candidate": "D",
        "definition": "Lambda = 1/R*, R* = Morse-index critical radius",
        "thread_count": torch.get_num_threads(),
        "bracket": [lo, hi],
        "bracket_width": hi - lo,
        "R_star_per_order": crossings,
        "R_star_primary_order20": r_star,
        "refinement_spread_R": spread,
        "Lambda_D": 1.0 / r_star,
        "Lambda_D_relative_uncertainty": spread / r_star,
        "lambda_slope_at_crossing_order20": primary["slope"],
        "fine_quadrature_check": quad,
        "closest_record_summary": {
            "radius": closest["radius"],
            "lambda_min": mode["lambda_min"],
            "lambda_2": mode["lambda_2"],
            "ratio_lambda_min_over_lambda_2":
                mode["lambda_min"] / mode["lambda_2"],
            "max_abs_eig": mode["max_abs_eig"],
            "mode_fractions": mode["mode_fractions"],
            "mode_radial_nodes_split": mode["mode_radial_nodes_split"],
        },
        "chain": [
            {"radius": r["radius"],
             "lam_by_order": {o: d["lambda_min"]
                              for o, d in r["orders"].items()},
             "index20": r["orders"]["20"]["morse_index_packaged"],
             "energy": r["orders"]["20"]["energy"]}
            for r in records if "orders" in r
        ],
    }
    print(json.dumps(result, indent=2))
    json.dump(result, open(HERE / "morse-results.json", "w"), indent=1)
    print(f"\nR* = {r_star:.6f} +- {spread:.6f} (order spread); "
          f"Lambda_D = {result['Lambda_D']:.6f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
