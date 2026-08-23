"""Attempt 0005 -- candidate F final comparator rows (corrected).

Lessons folded in:
- splitting_scale.py: U-side order-18/20 ladders jumped families
  (log preserved); its S rows are valid.
- splitting_fixed.py: an order-18 oracle requires 54-length input --
  "frozen field across orders" is undefined at coefficient level; only
  quadrature density can be varied at fixed fields.

This wave computes, per radius R in {12, 14}:
  - S roots at orders 16 -> 18 -> 20 (ladder; lambda_1 > 0 asserted),
  - a TRUE order-18 U root via multi-seed solves accepted only on the
    U fingerprint (lambda_1 < 0, relative_gradient < 1e-6),
  - Delta_E at order 20 (root energies: E_U from the validated chain,
    E_S from this wave), Delta_E at order 18 (root energies),
    and Delta_E under 48x24 quadrature at frozen order-20 fields,
then the four-radius Delta_E(R) box-independence series.
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

SETTINGS = dict(radial_nodes=32, angular_nodes=16)


def oracle(radius, order=20, nodes=32, angular=16):
    return Oracle(dict(radial_order=order, radial_nodes=nodes,
                       angular_nodes=angular, radius=radius))


def frozen_energy(values, radius, nodes=32, angular=16):
    total, _g, _h, _x = oracle(radius, 20, nodes,
                               angular).evaluate(np.asarray(values))
    return float(total)


def lam1(values, radius, order=20):
    _t, _g, hess, _x = oracle(radius, order).evaluate(np.asarray(values))
    mat = np.asarray(hess, dtype=float)
    return float(np.linalg.eigvalsh(0.5 * (mat + mat.T))[0])


def solve_checked(order, seed, radius, want_negative_lambda):
    row = solve_order(order, np.asarray(seed, dtype=float),
                      dict(SETTINGS, radius=radius))
    vals = np.asarray(row.pop("values"))
    lam = lam1(vals, radius, order=order)
    ok = (row["relative_gradient"] < 1e-6 and
          ((lam < 0) if want_negative_lambda else (lam > 0)))
    return vals, float(row["energy"]), lam, ok


def main() -> int:
    t0 = time.time()
    big = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                      "attempts/0042/largeR-roots.json").read_text())
    cand = json.loads((HERE / "candidate-e.json").read_text())

    e_u_root = {float(r["radius"]): r["energy"]
                for r in cand["u_map"] if "error" not in r}
    u_vals = {13.0: np.asarray(cand["chain_tail_values"]["13.0"]),
              14.0: np.asarray(cand["chain_tail_values"]["14.0"])}
    cur = u_vals[13.0].copy()
    prev_vec = None
    for radius in (12.5, 12.0):
        row = solve_order(20, cur, dict(SETTINGS, radius=radius))
        vals = np.asarray(row.pop("values"))
        _t, _g, hess, _x = oracle(radius).evaluate(vals)
        mat = np.asarray(hess, dtype=float)
        _lams, vecs = np.linalg.eigh(0.5 * (mat + mat.T))
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
        # --- S side: ladder with positive-lambda fingerprint
        s16 = np.asarray(big[f"R{int(radius)}"]["values"])
        s18, e_s18, lam_s18, ok18 = solve_checked(18, pad(s16, 18),
                                                  radius, False)
        assert ok18, f"S18 failed fingerprint at {radius}"
        s20, e_s20, lam_s20, ok20 = solve_checked(20, pad(s18, 20),
                                                  radius, False)
        assert ok20, f"S20 failed fingerprint at {radius}"

        # --- U side: order-18 root by multi-seed search
        u18 = e_u18 = lam_u18 = None
        seed_sources = [u_vals[12.5], u_vals[13.0], u_vals[radius]]
        for src in seed_sources:
            seed = pad(fit(np.asarray(src), 16), 18)
            try:
                vals, energy, lam, ok = solve_checked(18, seed, radius,
                                                      True)
            except Exception as exc:
                print(f"[U18] R={radius} seed@{src[0]:.3f}: FAIL {exc!r}",
                      flush=True)
                continue
            print(f"[U18] R={radius} seed@{src[0]:.3f}: "
                  f"E={energy:.9f} lam1={lam:+.4e} ok={ok}", flush=True)
            if ok:
                u18, e_u18, lam_u18 = vals, energy, lam
                break
        assert u18 is not None, f"no order-18 U root found at {radius}"

        e_u20 = e_u_root[radius]
        delta20 = e_u20 - e_s20
        delta18 = e_u18 - e_s18
        dq48 = (frozen_energy(u_vals[radius], radius, nodes=48,
                              angular=24)
                - frozen_energy(s20, radius, nodes=48, angular=24))
        out[str(radius)] = {
            "E_U20_root": e_u20, "E_S20_root": e_s20,
            "delta_20_root": delta20,
            "E_U18_root": e_u18, "E_S18_root": e_s18,
            "delta_18_root": delta18,
            "lambda1_S20": lam_s20, "lambda1_S18": lam_s18,
            "lambda1_U18": lam_u18,
            "delta_quad48_frozen": dq48,
            "refinement_shift_18_frac":
                abs(delta18 - delta20) / abs(delta20),
            "quadrature_shift_frac":
                abs(dq48 - delta20) / abs(delta20),
        }
        print(f"[F] R={radius}: d20={delta20:.6f} d18={delta18:.6f} "
              f"dq48={dq48:.6f}", flush=True)

    known = {
        "8.0": {"delta_20_root": 50.705900917 - 50.44584629433424},
        "10.0": {"delta_20_root": 53.303024612 - 53.037789180460635},
    }
    series = {k: v["delta_20_root"] for k, v in known.items()}
    series.update({k: v["delta_20_root"] for k, v in out.items()})
    dvals = np.array([series[k] for k in sorted(series, key=float)])
    mean = float(dvals.mean())
    spread = float(np.max(np.abs(dvals - mean)) / abs(mean))
    print(f"[F] delta_20 series={series}")
    print(f"[F] mean={mean:.9f} spread={spread * 100:.3f}%", flush=True)

    payload = {
        "meta": {"elapsed_s": time.time() - t0},
        "new_radii": out,
        "delta_20_series": series,
        "mean_delta_20": mean,
        "spread_fraction": spread,
    }
    (HERE / "splitting-final.json").write_text(json.dumps(payload,
                                                          indent=1))
    print("[DONE] splitting-final.json written", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
