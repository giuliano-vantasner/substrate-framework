"""Radius-dependence of one-body stability (attempt 0041, stage 3).

The coefficients describe profiles as functions of x = r/R, so the same
coefficient vector carries the branch to any domain radius.  Scanning R
therefore maps the stability of the spherically symmetric stationary branch
as a function of the domain size.

Findings (all roots converged unless flagged):
  R=6   lambda_min = -0.0640  Morse index 1  (certified saddle; stages 1-2)
  R=7.5 lambda_min = +4.5e-5  index 0
  R=8   lambda_min = +9.7e-6 (N=20) / frozen M=24: +2.8e-6, index 0;
        basis-free Q[eta_lowest] = +2.5e-6 (matches eigenvalue)
  R=10  lambda_min = +5.7e-5 (N=16) / frozen M=20: +1.1e-5, index 0

Critical radius R* in (6, 7.5): the tangential-split instability exists only
below R*.  R=7 was attempted but did not converge (|g|/|E| ~ 4e-2) and is
excluded.  The R >= 7.5 branch is marginally stable (lambda_min positive but
small) with a boundary-clustered soft mode.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

import sys

sys.path.insert(0, str(HERE))
from solve_radial_1d import Oracle, solve_order  # noqa: E402


def fit(values, new_order):
    return values.reshape(3, -1)[:, :new_order].ravel()


def pad(values, new_order):
    old = values.reshape(3, -1)
    out = np.zeros((3, new_order))
    out[:, : old.shape[1]] = old
    return out.ravel()


def main():
    rows = json.loads((HERE / "radial-results.json").read_text())
    root20 = np.asarray([r for r in rows if r["radial_order"] == 20][0]["values"])

    results = {}
    for radius in (7.5, 8.0):
        base = dict(radial_nodes=32, angular_nodes=16, radius=radius)
        row = solve_order(16, fit(root20, 16), base)
        v16 = np.asarray(row.pop("values"))
        results[f"R={radius}"] = {"N16": {k: row[k] for k in
                                          ("energy", "relative_gradient", "lambda_min",
                                           "morse_index", "components")}}
        print(f"R={radius}: N=16 lambda_min={row['lambda_min']:+.8f} "
              f"index={row['morse_index']} |g|/|E|={row['relative_gradient']:.1e}", flush=True)

    # R=8 refinement chain and frozen certification
    base8 = dict(radial_nodes=32, angular_nodes=16, radius=8.0)
    r = solve_order(18, pad(fit(root20, 16), 18), base8)
    v18 = np.asarray(r.pop("values"))
    results["R=8"]["N18"] = {"lambda_min": r["lambda_min"], "morse_index": r["morse_index"]}
    r = solve_order(20, pad(v18, 20), base8)
    v20 = np.asarray(r.pop("values"))
    results["R=8"]["N20"] = {"lambda_min": r["lambda_min"], "morse_index": r["morse_index"],
                             "energy": r["energy"], "components": r["components"]}
    print(f"R=8: N=20 lambda_min={r['lambda_min']:+.8f}", flush=True)
    spectrum = {}
    for m in (22, 24):
        o = Oracle(dict(radial_order=m, radial_nodes=48, angular_nodes=16, radius=8.0))
        t, g, h, c = o.evaluate(pad(v20, m))
        e = np.linalg.eigvalsh((h + h.T) / 2)
        spectrum[m] = e[:4].tolist()
        print(f"R=8 frozen M={m}: lambda_min={e[0]:+.8f} lambda_2={e[1]:.3e}", flush=True)
    results["R=8"]["frozen_spectrum"] = spectrum

    # R=10 from the R=8 N=16 coefficients
    row = solve_order(16, v16.copy(), dict(radial_nodes=32, angular_nodes=16, radius=10.0))
    v = np.asarray(row.pop("values"))
    results["R=10"] = {"N16": {"lambda_min": row["lambda_min"],
                               "morse_index": row["morse_index"]}}
    o = Oracle(dict(radial_order=20, radial_nodes=48, angular_nodes=16, radius=10.0))
    t, g, h, c = o.evaluate(pad(v, 20))
    e = np.linalg.eigvalsh((h + h.T) / 2)
    results["R=10"]["frozen_M20_lambda_min"] = float(e[0])
    print(f"R=10: N=16 lambda_min={row['lambda_min']:+.8f}; frozen M=20 {e[0]:+.8f}", flush=True)

    (HERE / "radius-scan-results.json").write_text(json.dumps(results, indent=2))
    print("wrote radius-scan-results.json")


if __name__ == "__main__":
    main()
