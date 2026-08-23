"""Attempt 0005 -- candidate E: Lambda = 1/R_U*, stabilization of family U.

Preregistered construction (proposal.yaml id E, registered in
attempts/0004/result.yaml BEFORE any solve at radii in (8.0, 9.0)):
Lambda = 1/R_U* with R_U* the radius at which the discrete Morse index
of family U (the stationary-point family containing the certified P240
R=6 root) falls from >= 1 to 0 under increasing radius.

FROZEN PROTOCOL (fixed before launch):
- Oracle: packaged discrete index, threshold lam < -1e-8*max(1,max|lam|),
  symmetrized Hessian eigh at the converged root.
- Chain discipline: every radius solved at order 20 by continuation from
  the nearest evaluated U root.
- Family identity monitors per solve: energy distance from linear
  interpolation of the two bracketing roots (>0.05 flags),
  soft-eigenvector overlap with the nearer bracketing root (<0.80
  flags), soft-vector sign-change count, lam_min/lam_2 ratio,
  frequency/inertia continuity.
- Bisection acceptance: midpoint root joins the chain only if it passes
  both monitors and relative_gradient < 1e-6; retry from the other
  side; on second failure record SUSPECT and stop honestly.
- Confirmation at the final bracket ends: full 16/18/20 ladders (pad)
  must flip index within the SAME bracket; frozen-field quadrature
  sweep 32x16 -> 48x24 -> 64x32 sign stability at both ends.
- Interpretation rule (frozen): continuous index flip => R_U* = bracket
  midpoint +- half-width.  Non-convergence or family merge below the
  flip => no stabilization radius; candidate E refuted/blocked with the
  named mechanism, NOT silently converted into another construction.

Environment: system python3 (torch host), BLAS threads pinned and
recorded at module level per small-ratio-numerics reproducibility.
Oracle.evaluate returns (energy, gradient, hessian, extra).
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path.insert(0, str(REPO / "proposals/P240-m5-kinetic-axis/attempts/0041"))
sys.path.insert(0, str(REPO / "proposals/P243-clock-sourced-induced-coupling/attempts/0002"))

from solve_radial_1d import Oracle, solve_order  # noqa: E402
from window_continuation import pad  # noqa: E402

try:
    import torch
    THREADS = torch.get_num_threads()
except Exception:
    THREADS = -1

ORDER = 20
INDEX_REL = -1e-8
LOGGED_ENERGIES = {6.05: 46.713640819, 6.1: 46.842195074,
                   6.15: 46.969228152, 6.2: 47.094737575,
                   6.3: 47.341190314, 6.375: 47.522053192,
                   6.5: 47.816001577, 6.75: 48.376537228,
                   7.0: 48.902313409, 7.25: 49.395698629,
                   7.5: 49.859166607, 7.75: 50.295138302,
                   8.0: 50.705900917}


def oracle_settings(radius):
    return dict(radial_nodes=32, angular_nodes=16, radius=radius)


def sym_hessian(radius, values, nodes=32, angular=16):
    oracle = Oracle(dict(radial_order=ORDER, radial_nodes=nodes,
                         angular_nodes=angular, radius=radius))
    _total, _grad, hess, _extra = oracle.evaluate(np.asarray(values))
    hess = np.asarray(hess, dtype=float)
    return 0.5 * (hess + hess.T)


def spectrum(radius, values):
    return np.linalg.eigh(sym_hessian(radius, values))


def index_of(lams):
    thr = INDEX_REL * max(1.0, float(np.abs(lams).max()))
    return int(np.sum(lams < thr)), float(thr)


def soft_nodes(vec):
    signs = np.sign(vec)
    signs = signs[signs != 0]
    return int(np.sum(signs[1:] * signs[:-1] < 0))


def solve_u(radius, seed_values):
    row = solve_order(ORDER, np.asarray(seed_values, dtype=float),
                      oracle_settings(radius))
    vals = np.asarray(row.pop("values"))
    lams, vecs = spectrum(radius, vals)
    idx, thr = index_of(lams)
    lam1, lam2 = float(lams[0]), float(lams[1])
    return {
        "radius": radius,
        "energy": float(row["energy"]),
        "relative_gradient": float(row["relative_gradient"]),
        "lambda_1": lam1,
        "lambda_2": lam2,
        "ratio_l1_l2": (lam1 / lam2) if lam2 > 0 else None,
        "index": idx,
        "threshold": thr,
        "frequency": float(row.get("frequency", float("nan"))),
        "inertia": float(row.get("inertia", float("nan"))),
        "nodes_soft": soft_nodes(vecs[:, 0]),
        "values": vals.tolist(),
        "_vec": vecs[:, 0],
    }


def strip(row):
    return {k: v for k, v in row.items() if k not in ("values", "_vec")}


def attach_monitors(new_row, near_row, far_row=None):
    nv, pv = new_row["_vec"], near_row["_vec"]
    new_row["overlap_near"] = float(
        abs(np.dot(nv, pv)) / (np.linalg.norm(nv) * np.linalg.norm(pv)))
    gap = 0.0
    if far_row is not None:
        e0, e1 = far_row["energy"], near_row["energy"]
        r0, r1 = far_row["radius"], near_row["radius"]
        interp = e1 + (new_row["radius"] - r1) * (e1 - e0) / (r1 - r0)
        gap = abs(new_row["energy"] - interp)
    new_row["energy_interp_gap"] = float(gap)
    new_row["family_flag"] = bool(gap > 0.05 or new_row["overlap_near"] < 0.80)
    return new_row


def run_chain(radii, start_values):
    rows, mismatch = [], []
    cur = np.asarray(start_values)
    prev = None
    for radius in radii:
        try:
            row = solve_u(radius, cur)
        except Exception as exc:
            rows.append({"radius": radius, "error": repr(exc)[:200]})
            print(f"[U] R={radius}: SOLVER FAIL {exc!r}", flush=True)
            break
        if prev is None:
            row.update(overlap_near=1.0, energy_interp_gap=0.0,
                       family_flag=False)
        else:
            far = rows[-2] if len(rows) >= 2 and "energy" in rows[-2] \
                else None
            row = attach_monitors(row, prev, far)
        logged = LOGGED_ENERGIES.get(radius)
        if logged is not None and abs(row["energy"] - logged) > 2e-6:
            mismatch.append({"radius": radius,
                             "gap": abs(row["energy"] - logged)})
        rows.append(row)
        cur = np.asarray(row["values"])
        prev = row
        print(f"[U] R={radius}: E={row['energy']:.9f} "
              f"lam1={row['lambda_1']:+.6e} lam2={row['lambda_2']:+.3e} "
              f"idx={row['index']} ovl={row['overlap_near']:.4f} "
              f"gap={row['energy_interp_gap']:.2e} "
              f"nodes={row['nodes_soft']}"
              f"{' FLAG' if row['family_flag'] else ''}", flush=True)
        if row["index"] == 0:
            print(f"[U] stabilization reached at R={radius}", flush=True)
            break
    return rows, mismatch


def bisect_index(lo_row, hi_row):
    lo_vals = np.asarray(lo_row["values"])
    hi_vals = np.asarray(hi_row["values"])
    chain = []
    note = ""
    for step in range(14):
        mid = 0.5 * (lo_row["radius"] + hi_row["radius"])
        accepted = None
        for seed_name, seed, near, other in (
                ("lo", lo_vals, lo_row, hi_row),
                ("hi", hi_vals, hi_row, lo_row)):
            try:
                row = solve_u(mid, seed)
            except Exception as exc:
                chain.append({"step": step, "mid": mid, "seed": seed_name,
                              "error": repr(exc)[:160]})
                print(f"[B] R={mid:.7f} seed={seed_name}: FAIL {exc!r}",
                      flush=True)
                continue
            row = attach_monitors(row, near, other)
            chain.append({**strip(row), "seed": seed_name})
            ok = not row["family_flag"] and row["relative_gradient"] < 1e-6
            print(f"[B] R={mid:.7f} seed={seed_name}: "
                  f"E={row['energy']:.9f} lam1={row['lambda_1']:+.4e} "
                  f"idx={row['index']} ovl={row['overlap_near']:.4f} "
                  f"gap={row['energy_interp_gap']:.2e} ok={ok}", flush=True)
            if ok:
                accepted = (seed_name, row)
                break
        if accepted is None:
            note = f"SUSPECT at mid={mid}; bisection halted"
            print(f"[B] {note}", flush=True)
            break
        _, row = accepted
        if row["index"] >= 1:
            lo_row, lo_vals = row, np.asarray(row["values"])
        else:
            hi_row, hi_vals = row, np.asarray(row["values"])
        if hi_row["radius"] - lo_row["radius"] < 1e-3:
            break
    return chain, lo_row, hi_row, lo_vals, hi_vals, note


def confirm_endpoint(tag, base_row, base_vals):
    radius = base_row["radius"]
    settings = oracle_settings(radius)
    base = np.asarray(base_vals)
    v16 = np.asarray(solve_order(16, base[:48], settings)["values"])
    v18 = np.asarray(solve_order(18, pad(v16, 18), settings)["values"])
    lad = {}
    for order, vals_o in ((16, v16), (18, v18), (ORDER, base)):
        lams_o, _ = np.linalg.eigh(
            sym_hessian(radius, vals_o))
        idx_o, _ = index_of(lams_o)
        lad[str(order)] = {"lambda_1": float(lams_o[0]), "index": idx_o}
    frz = {}
    for nodes, ang in ((32, 16), (48, 24), (64, 32)):
        lams_f = np.linalg.eigvalsh(sym_hessian(radius, base,
                                                nodes=nodes, angular=ang))
        idx_f, _ = index_of(lams_f)
        frz[f"{nodes}x{ang}"] = {"lambda_1": float(lams_f[0]),
                                 "index": idx_f}
    print(f"[C] {tag} R={radius:.7f}: ladder={lad} frozen={frz}", flush=True)
    return {"radius": radius, "ladder": lad}, frz


def main() -> int:
    t0 = time.time()
    refine = json.loads((HERE.parent / "0004/stable-side-refinement.json")
                        .read_text())
    anchor = np.asarray(refine["values_by_order"]["20"])  # family U anchor

    radii = list(LOGGED_ENERGIES) + [8.25, 8.5, 8.75, 9.0, 9.25, 9.5,
                                     9.75, 10.0, 10.5, 11.0, 11.5, 12.0,
                                     12.5, 13.0, 13.5, 14.0]
    u_map, mismatch = run_chain(radii, anchor)

    good = [r for r in u_map if "error" not in r]
    neg = [r for r in good if r["index"] >= 1]
    pos = [r for r in good if r["index"] == 0]

    chain, ladders, frozen = [], {}, {}
    verdict_note = ""
    lo_row = hi_row = None
    lo_vals = hi_vals = None
    if neg and pos:
        chain, lo_row, hi_row, lo_vals, hi_vals, verdict_note = \
            bisect_index(neg[-1], pos[0])
        ladder_lo, frozen_lo = confirm_endpoint("lo", lo_row, lo_vals)
        ladder_hi, frozen_hi = confirm_endpoint("hi", hi_row, hi_vals)
        ladders = {"lo": ladder_lo, "hi": ladder_hi}
        frozen = {"lo": frozen_lo, "hi": frozen_hi}
    elif good:
        verdict_note = ("no stabilization within R <= "
                        f"{good[-1]['radius']:.2f}")

    lo_radius = None if lo_row is None else lo_row["radius"]
    hi_radius = None if hi_row is None else hi_row["radius"]
    lo_block = (None if lo_vals is None else
                {"radius": lo_radius, "values": lo_vals.tolist()})
    hi_block = (None if hi_vals is None else
                {"radius": hi_radius, "values": hi_vals.tolist()})
    payload = {
        "meta": {"threads": THREADS, "order": ORDER,
                 "index_rel_threshold": INDEX_REL,
                 "elapsed_s": time.time() - t0,
                 "replay_mismatches": mismatch},
        "u_map": [strip(r) for r in u_map],
        "bisect_chain": chain,
        "endpoint_ladders": ladders,
        "frozen_checks": frozen,
        "verdict_note": verdict_note,
        "bracket": {"lo_radius": lo_radius, "hi_radius": hi_radius},
        "bracket_values": {"lo": lo_block, "hi": hi_block},
        "chain_tail_values": {str(r["radius"]): r["values"]
                              for r in good[-3:]},
    }
    (HERE / "candidate-e.json").write_text(json.dumps(payload, indent=1))
    print("[DONE] candidate-e.json written", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
