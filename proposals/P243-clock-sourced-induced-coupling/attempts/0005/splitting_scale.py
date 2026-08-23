"""Attempt 0005 -- candidate F comparator wave: same-order U-S splitting.

Computes Delta_E(R) = E_U(R) - E_S(R) at MATCHED solver order for
R in {12, 14} (order-20 S roots do not exist yet; 0042 largeR roots
are order 16).  Registered frozen criteria live in proposal.yaml id F;
this run evaluates the previously-unevaluated comparators.

Chain sources:
- S: 0042 order-16 values -> ladder 16 -> 18 -> 20 (pad).
- U: saved order-20 values at R=13.0 (candidate-e.json chain tail)
  -> descend 12.5 -> 12.0 with family monitors -> fit to order 16 ->
  ladder 18 -> 20 for the refinement row.
Refinement row: Delta_E at order 18 vs order 20 at R=12 and R=14.
Quadrature row: frozen-field energies at 48x24 for both families at
R=14 (Delta_E stability under density change).
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
from window_continuation import fit, pad  # noqa: E402


def oracle(radius, order=20, nodes=32, angular=16):
    return Oracle(dict(radial_order=order, radial_nodes=nodes,
                       angular_nodes=angular, radius=radius))


def eval_energy(values, radius, order=20, nodes=32, angular=16):
    total, grad, hess, _x = oracle(radius, order, nodes,
                                   angular).evaluate(np.asarray(values))
    return float(total)


def lam1(values, radius, order=20):
    _t, _g, hess, _x = oracle(radius, order).evaluate(np.asarray(values))
    hess = np.asarray(hess, dtype=float)
    lams = np.linalg.eigvalsh(0.5 * (hess + hess.T))
    return float(lams[0])


def ladder(seed16, radius):
    v18 = np.asarray(solve_order(18, pad(np.asarray(seed16), 18),
                                 dict(radial_nodes=32, angular_nodes=16,
                                      radius=radius))["values"])
    r20 = solve_order(20, pad(v18, 20),
                      dict(radial_nodes=32, angular_nodes=16,
                           radius=radius))
    return v18, np.asarray(r20.pop("values")), r20


def main() -> int:
    t0 = time.time()
    big = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                      "attempts/0042/largeR-roots.json").read_text())
    cand = json.loads((HERE / "candidate-e.json").read_text())
    out = {}

    # --- U descent 13.0 -> 12.5 -> 12.0 (order 20, family-monitored)
    u_vals = {13.0: np.asarray(cand["chain_tail_values"]["13.0"]),
              14.0: np.asarray(cand["chain_tail_values"]["14.0"])}
    vec_prev = None
    cur = u_vals[13.0].copy()
    for radius in (12.5, 12.0):
        row = solve_order(20, cur, dict(radial_nodes=32, angular_nodes=16,
                                        radius=radius))
        vals = np.asarray(row.pop("values"))
        _t, _g, hess, _x = oracle(radius).evaluate(vals)
        hess = np.asarray(hess, dtype=float)
        lams, vecs = np.linalg.eigh(0.5 * (hess + hess.T))
        if vec_prev is None:
            _t2, _g2, h2, _x2 = oracle(13.0).evaluate(u_vals[13.0])
            h2 = np.asarray(h2, dtype=float)
            _l2, v2 = np.linalg.eigh(0.5 * (h2 + h2.T))
            vec_prev = v2[:, 0]
        ovl = abs(float(np.dot(vecs[:, 0], vec_prev))) / (
            np.linalg.norm(vecs[:, 0]) * np.linalg.norm(vec_prev))
        vec_prev = vecs[:, 0]
        print(f"[U-desc] R={radius}: E={float(row['energy']):.9f} "
              f"lam1={lams[0]:+.4e} ovl={ovl:.4f}", flush=True)
        u_vals[radius] = vals
        cur = vals

    # --- S ladders at 12 and 14; U ladders for the refinement row
    rows = {}
    for radius in (12.0, 14.0):
        s16 = np.asarray(big[f"R{int(radius)}"]["values"])
        s18, s20, summary = ladder(s16, radius)
        u16 = fit(u_vals[radius], 16)
        u18, u20_check, _sum_u = ladder(u16, radius)
        e_s18 = eval_energy(s18, radius, order=18)
        e_s20 = float(summary["energy"])
        e_u18 = eval_energy(u18, radius, order=18)
        e_u20 = eval_energy(u20_check, radius, order=20)
        d18 = e_u18 - e_s18
        d20 = e_u20 - e_s20
        q_s = eval_energy(s20, radius, nodes=48, angular=24)
        q_u = eval_energy(u20_check, radius, nodes=48, angular=24)
        rows[radius] = {
            "E_U18": e_u18, "E_S18": e_s18, "delta_18": d18,
            "E_U20": e_u20, "E_S20": e_s20, "delta_20": d20,
            "lambda1_S20": lam1(s20, radius),
            "lambda1_U20": lam1(u20_check, radius),
            "quad48_E_U20": q_u, "quad48_E_S20": q_s,
            "delta_quad48": q_u - q_s,
            "relgrad_S20": float(summary["relative_gradient"]),
        }
        print(f"[F] R={radius}: d18={d18:.6f} d20={d20:.6f} "
              f"dq48={rows[radius]['delta_quad48']:.6f} "
              f"lam1S={rows[radius]['lambda1_S20']:+.3e} "
              f"lam1U={rows[radius]['lambda1_U20']:+.3e}", flush=True)

    # Known same-order comparators (committed/reproduced, order 20)
    known = {
        8.0: {"E_U20": 50.705900917, "E_S20": 50.44584629433424},
        10.0: {"E_U20": 53.303024612, "E_S20": 53.037789180460635},
    }
    for r, kv in known.items():
        kv["delta_20"] = kv["E_U20"] - kv["E_S20"]

    series = {str(r): rows[r]["delta_20"] for r in rows}
    series.update({str(r): kv["delta_20"] for r, kv in known.items()})
    dvals = np.array([series[k] for k in sorted(series, key=float)])
    mean = float(dvals.mean())
    spread = float(np.max(np.abs(dvals - mean)) / abs(mean))
    print(f"[F] delta_20 series={series} mean={mean:.6f} "
          f"spread={spread*100:.2f}%", flush=True)

    payload = {
        "meta": {"elapsed_s": time.time() - t0},
        "known_comparators": {str(k): v for k, v in known.items()},
        "new_radii": {str(k): v for k, v in rows.items()},
        "delta_20_series": series,
        "mean_delta_20": mean,
        "spread_fraction": spread,
    }
    (HERE / "splitting-scale.json").write_text(json.dumps(payload,
                                                          indent=1))
    print("[DONE] splitting-scale.json written", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
