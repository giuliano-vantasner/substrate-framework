"""P240 attempt 0042, issue #151 Phase 1: is the R >= 7.5 minimum intrinsic?

Stage 1: R-ladder at R = 8, 10, 12, 16 with order refinement N = 16 -> 18 -> 20.
Stage 2: R* bisection in (6, 7.5) by warm-start continuation from R = 7.5.
Stage 3: declared-error-model enclosure of lambda_min at R = 8.

Interpretation criteria are preregistered in manifest.yaml and were frozen
before any ladder value was inspected. Writes results incrementally to
phase1-results.json so partial progress survives interruption.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

sys.path.insert(0, str(HERE / ".." / "0041"))
from solve_radial_1d import Oracle, solve_order  # noqa: E402

RESULTS = HERE / "phase1-results.json"
BASE_QUAD = dict(radial_nodes=32, angular_nodes=16)


def fit(values, n):
    return values.reshape(3, -1)[:, :n].ravel()


def pad(values, n):
    old = values.reshape(3, -1)
    out = np.zeros((3, n))
    out[:, : old.shape[1]] = old
    return out.ravel()


def load_results():
    if RESULTS.exists():
        return json.loads(RESULTS.read_text())
    return {"ladder": {}, "bisection": [], "enclosure": {}}


def save(res):
    RESULTS.write_text(json.dumps(res, indent=2))


def full_spectrum(values, order, radius, nodes=48, angular=16):
    o = Oracle(dict(radial_order=order, radial_nodes=nodes,
                    angular_nodes=angular, radius=radius))
    t, g, h, c = o.evaluate(pad(values, order))
    e = np.linalg.eigvalsh((h + h.T) / 2)
    return float(t), e[:4].tolist(), float(np.max(np.abs(g)) / abs(t))


def run_ladder(res):
    rows = json.loads((HERE / ".." / "0041" / "radial-results.json").read_text())
    root20 = np.asarray([r for r in rows if r["radial_order"] == 20][0]["values"])
    for radius in (8.0, 10.0, 12.0, 16.0):
        key = f"R={radius}"
        if key in res["ladder"] and res["ladder"][key].get("complete"):
            continue
        entry = {"orders": {}}
        v = None
        for n in (16, 18, 20):
            seed = fit(root20, n) if v is None else pad(v, n)
            t0 = time.time()
            try:
                row = solve_order(n, seed, dict(BASE_QUAD, radius=radius))
            except Exception as exc:  # noqa: BLE001 - record and continue ladder
                entry["orders"][str(n)] = {"converged": False, "error": repr(exc)}
                break
            vals = np.asarray(row.pop("values"))
            energy, spectrum, relgrad = full_spectrum(vals, min(n + 4, 24), radius)
            rec = {
                "converged": bool(row["relative_gradient"] < 1e-10),
                "relative_gradient": row["relative_gradient"],
                "energy": row["energy"],
                "inertia": row["components"]["inertia"],
                "omega": row["components"]["frequency"],
                "hess_lambda_min_N": row["lambda_min"],
                "frozen_spectrum_Mplus4": spectrum,
                "soft_mode_ratio": row["lambda_min"] / spectrum[1] if spectrum[1] > 0 else None,
                "minutes": round((time.time() - t0) / 60, 1),
            }
            entry["orders"][str(n)] = rec
            print(f"ladder {key} N={n}: lam={row['lambda_min']:+.3e} "
                  f"conv={rec['converged']} ({rec['minutes']}min)", flush=True)
            if not rec["converged"]:
                break
            v = vals
        entry["complete"] = True
        res["ladder"][key] = entry
        save(res)


def run_bisection(res):
    rows = json.loads((HERE / ".." / "0041" / "radial-results.json").read_text())
    root20 = np.asarray([r for r in rows if r["radial_order"] == 20][0]["values"])
    v16 = fit(root20, 16)
    done = {b["radius"] for b in res["bisection"]}
    # downward continuation from the converged R=7.5 branch
    current = v16
    for radius in (7.5, 7.4, 7.25, 7.1, 7.0, 6.9, 6.8, 6.6, 6.4, 6.2):
        if radius in done:
            continue
        try:
            row = solve_order(16, current, dict(BASE_QUAD, radius=radius))
        except Exception as exc:  # noqa: BLE001
            res["bisection"].append({"radius": radius, "converged": False,
                                     "error": repr(exc)})
            save(res)
            continue
        vals = np.asarray(row.pop("values"))
        conv = bool(row["relative_gradient"] < 1e-10)
        rec = {"radius": radius, "converged": conv,
               "relative_gradient": row["relative_gradient"],
               "lambda_min": row["lambda_min"], "morse_index": row["morse_index"]}
        res["bisection"].append(rec)
        print(f"bisect R={radius}: lam={row['lambda_min']:+.3e} conv={conv}", flush=True)
        save(res)
        if conv:
            current = vals


def run_enclosure(res):
    """lambda_min enclosure at R=8: eigenpair residual + quadrature variation."""
    rows = json.loads((HERE / ".." / "0041" / "radial-results.json").read_text())
    root20 = np.asarray([r for r in rows if r["radial_order"] == 20][0]["values"])
    base = dict(BASE_QUAD, radius=8.0)
    r = solve_order(16, fit(root20, 16), base)
    v16 = np.asarray(r.pop("values"))
    M = 24
    estimates = []
    for nodes, angular in ((48, 16), (80, 28), (112, 36)):
        o = Oracle(dict(radial_order=M, radial_nodes=nodes,
                        angular_nodes=angular, radius=8.0))
        t, g, h, c = o.evaluate(pad(v16, M))
        hs = (h + h.T) / 2
        e, vec = np.linalg.eigh(hs)
        lam, d = float(e[0]), vec[:, 0]
        residual = float(np.linalg.norm(hs @ d - lam * d))
        estimates.append({"quadrature": f"{nodes}x{angular}", "lambda_min": lam,
                          "eigenpair_residual": residual})
        print(f"enclosure {nodes}x{angular}: lam={lam:+.10f} resid={residual:.2e}",
              flush=True)
    lams = [x["lambda_min"] for x in estimates]
    q_var = max(lams) - min(lams)
    max_res = max(x["eigenpair_residual"] for x in estimates)
    half_width = q_var + max_res
    center = sum(lams) / len(lams)
    res["enclosure"] = {
        "estimates": estimates,
        "center": center,
        "half_width": half_width,
        "interval": [center - half_width, center + half_width],
        "excludes_zero": bool(abs(center) > 3 * half_width),
    }
    print(f"enclosure: lambda_min in [{center - half_width:+.3e}, "
          f"{center + half_width:+.3e}], excludes_zero="
          f"{res['enclosure']['excludes_zero']}", flush=True)
    save(res)


if __name__ == "__main__":
    res = load_results()
    stage = sys.argv[1] if len(sys.argv) > 1 else "all"
    if stage in ("all", "ladder"):
        run_ladder(res)
    if stage in ("all", "bisection"):
        run_bisection(res)
    if stage in ("all", "enclosure"):
        run_enclosure(res)
    print("done")
