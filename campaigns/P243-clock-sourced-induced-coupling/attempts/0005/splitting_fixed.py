"""Attempt 0005 -- corrected candidate-F refinement/quadrature rows.

splitting_scale.py's U-side order-18/20 ladders jumped families (third
documented occurrence of the re-solve family jump; its log is preserved
verbatim).  This addendum computes the refinement rows the FROZEN way:

- Delta_E(R) at order 20 uses ROOT energies: E_U from the validated
  candidate-e.json chain (no re-solve), E_S from fresh S ladders whose
  family identity is checked by lambda_1 > 0.
- Refinement row evaluates the FROZEN order-20 coefficient vectors of
  both families under an order-18 oracle and a 48x24 oracle; the
  splitting is stable iff Delta_E moves less than the 5% envelope.
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


def oracle(radius, order=20, nodes=32, angular=16):
    return Oracle(dict(radial_order=order, radial_nodes=nodes,
                       angular_nodes=angular, radius=radius))


def frozen_energy(values, radius, order=20, nodes=32, angular=16):
    total, _grad, _hess, _x = oracle(radius, order, nodes,
                                     angular).evaluate(np.asarray(values))
    return float(total)


def lam1(values, radius, order=20):
    _t, _g, hess, _x = oracle(radius, order).evaluate(np.asarray(values))
    mat = np.asarray(hess, dtype=float)
    lams = np.linalg.eigvalsh(0.5 * (mat + mat.T))
    return float(lams[0])


def main() -> int:
    t0 = time.time()
    big = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                      "attempts/0042/largeR-roots.json").read_text())
    cand = json.loads((HERE / "candidate-e.json").read_text())

    e_u_root = {float(r["radius"]): r["energy"]
                for r in cand["u_map"] if "error" not in r}
    u_vals = {13.0: np.asarray(cand["chain_tail_values"]["13.0"]),
              14.0: np.asarray(cand["chain_tail_values"]["14.0"])}

    # Rebuild U@12 order-20 values by monitored descent from 13.0
    cur = u_vals[13.0].copy()
    prev_vec = None
    for radius in (12.5, 12.0):
        row = solve_order(20, cur, dict(radial_nodes=32, angular_nodes=16,
                                        radius=radius))
        vals = np.asarray(row.pop("values"))
        _t, _g, hess, _x = oracle(radius).evaluate(vals)
        mat = np.asarray(hess, dtype=float)
        lams, vecs = np.linalg.eigh(0.5 * (mat + mat.T))
        if prev_vec is None:
            _t2, _g2, h2, _x2 = oracle(13.0).evaluate(u_vals[13.0])
            m2 = np.asarray(h2, dtype=float)
            _l2, v2 = np.linalg.eigh(0.5 * (m2 + m2.T))
            prev_vec = v2[:, 0]
        ovl = abs(float(np.dot(vecs[:, 0], prev_vec))) / (
            np.linalg.norm(vecs[:, 0]) * np.linalg.norm(prev_vec))
        prev_vec = vecs[:, 0]
        assert ovl > 0.95, f"family jump in U descent at {radius}"
        u_vals[radius] = vals
        cur = vals
        print(f"[U-desc] R={radius}: E={float(row['energy']):.9f} "
              f"ovl={ovl:.4f}", flush=True)

    out = {}
    for radius in (12.0, 14.0):
        s16 = np.asarray(big[f"R{int(radius)}"]["values"])
        s18 = np.asarray(solve_order(
            18, pad(s16, 18),
            dict(radial_nodes=32, angular_nodes=16,
                 radius=radius))["values"])
        srow = solve_order(20, pad(s18, 20),
                           dict(radial_nodes=32, angular_nodes=16,
                                radius=radius))
        s20 = np.asarray(srow.pop("values"))
        lam_s = lam1(s20, radius)
        assert lam_s > 0, f"S ladder lost stability at {radius}: {lam_s}"
        e_s20 = float(srow["energy"])
        e_u20 = e_u_root[radius]
        delta20 = e_u20 - e_s20
        # Frozen-field refinement: same order-20 coefficients,
        # order-18 oracle and denser quadrature.
        d18f = (frozen_energy(u_vals[radius], radius, order=18)
                - frozen_energy(s20, radius, order=18))
        dq48 = (frozen_energy(u_vals[radius], radius, nodes=48,
                              angular=24)
                - frozen_energy(s20, radius, nodes=48, angular=24))
        out[str(radius)] = {
            "E_U20_root": e_u20, "E_S20_root": e_s20,
            "delta_20_root": delta20,
            "lambda1_S20": lam_s,
            "delta_18_frozen": d18f,
            "delta_quad48_frozen": dq48,
            "refinement_shift_18_frac": abs(d18f - delta20) / abs(delta20),
            "quadrature_shift_frac": abs(dq48 - delta20) / abs(delta20),
            "relgrad_S20": float(srow["relative_gradient"]),
        }
        print(f"[F] R={radius}: d20={delta20:.6f} d18f={d18f:.6f} "
              f"dq48={dq48:.6f} lam1S={lam_s:+.3e}", flush=True)

    known = {
        "8.0": {"E_U20_root": 50.705900917,
                "E_S20_root": 50.44584629433424},
        "10.0": {"E_U20_root": 53.303024612,
                 "E_S20_root": 53.037789180460635},
    }
    for k, kv in known.items():
        kv["delta_20_root"] = kv["E_U20_root"] - kv["E_S20_root"]
    series = {k: v["delta_20_root"] for k, v in known.items()}
    series.update({k: v["delta_20_root"] for k, v in out.items()})
    dvals = np.array([series[k] for k in sorted(series, key=float)])
    mean = float(dvals.mean())
    spread = float(np.max(np.abs(dvals - mean)) / abs(mean))
    print(f"[F] delta_20 series={series}")
    print(f"[F] mean={mean:.9f} spread={spread * 100:.3f}%", flush=True)

    payload = {
        "meta": {"elapsed_s": time.time() - t0,
                 "note": "supersedes U-ladder rows of splitting_scale.py "
                         "(family jump); frozen-field protocol"},
        "new_radii": out,
        "known_comparators": known,
        "delta_20_series": series,
        "mean_delta_20": mean,
        "spread_fraction": spread,
    }
    (HERE / "splitting-scale-fixed.json").write_text(json.dumps(
        payload, indent=1))
    print("[DONE] splitting-scale-fixed.json written", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
