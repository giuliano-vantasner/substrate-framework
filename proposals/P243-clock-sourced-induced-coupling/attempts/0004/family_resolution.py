"""Attempt 0004 diagnostic: resolve the two clock-branch families near R*.

morse_bisection.py + refine_stable_side.py revealed two distinct
stationary-point families near R ~ 6.01:
  family U (unstable): contains the certified P240 R=6 root
    (E=46.5836, lambda_1=-6.26e-2); continues smoothly to R=6.0117
    (E=46.614, lambda_1=-6.19e-2 at N20, refine_stable_side run).
  family S (stable): lambda_1 ~ +8e-6 plateau; contains every window
    root R >= 7.5 certified by P240; sampled down to R=6.0117
    (E=46.357) by the bisection chain.

The index flip bracketed as [6.0, 6.0117] conflates the families.  Two
questions decide candidate D's fate:
  Q1 (S-descent): does family S terminate at a fold just below 6.0117,
      or persist to smaller radii?  If it persists well below 6.0,
      there is no UV threshold at ~6.01 and candidate D is refuted.
  Q2 (U-ascent): does family U's lambda_1 (rising slowly with R) cross
      zero at some R_U in (6.0117, 6.375)?  If yes, the certified
      branch itself stabilizes there and R_U is the natural critical
      radius; if it persists unstable, the certified R=6 root is a
      saddle on a branch that never stabilizes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
P240 = HERE.parents[3] / "proposals" / "P240-m5-kinetic-axis" / "attempts"
sys.path.insert(0, str(P240 / "0041"))
sys.path.insert(0, str(HERE.parent / "0002"))

from solve_radial_1d import Oracle, solve_order  # noqa: E402
from window_continuation import fit, pad  # noqa: E402


def local_lambda(settings, order, values):
    oracle = Oracle(dict(settings, radial_order=order))
    _, _, hess, _ = oracle.evaluate(values)
    sym = (hess + hess.T) / 2.0
    return float(np.linalg.eigvalsh(sym)[0])


def walk(radius_list, seed_values, tag):
    """Order-20 continuation walk; classify family at each radius."""

    rows = []
    values = np.asarray(seed_values, dtype=np.float64)
    for radius in radius_list:
        settings = dict(radial_nodes=32, angular_nodes=16,
                        radius=radius)
        try:
            row = solve_order(20, values, settings)
        except Exception as exc:  # noqa: BLE001 - record solver blowups
            rows.append({"radius": radius, "family": tag,
                         "failed": repr(exc)[:200]})
            print(f"[{tag}] R={radius}: SOLVER FAIL {exc!r}", flush=True)
            break
        values = np.asarray(row.pop("values"))
        total = float(row["energy"])
        rel = float(row["relative_gradient"])
        if not np.isfinite(total) or not (40.0 < total < 60.0):
            rows.append({"radius": radius, "family": tag,
                         "failed": "energy_window", "energy": total})
            print(f"[{tag}] R={radius}: ENERGY WINDOW E={total}",
                  flush=True)
            break
        if rel > 1e-10:
            rows.append({"radius": radius, "family": tag,
                         "failed": "unconverged", "relative_gradient": rel})
            print(f"[{tag}] R={radius}: UNCONVERGED {rel:.2e}",
                  flush=True)
            break
        lam1 = local_lambda(settings, 20, values)
        family = "S" if lam1 > -1e-3 else "U"
        rows.append({"radius": radius, "family": family, "energy": total,
                     "lambda_1": lam1,
                     "relative_gradient": rel})
        print(f"[{tag}-> {family}] R={radius}: E={total:.9f} "
              f"lam1={lam1:+.6e}", flush=True)
    return rows


def main() -> int:
    rows_json = json.loads(
        (P240 / "0041" / "radial-results.json").read_text()
    )
    root20 = np.asarray(
        [r for r in rows_json if r["radial_order"] == 20][0]["values"]
    )

    # Q2: U-ascent from the saved refine-run N20 values at
    # R=6.01171875 (family U by construction, lambda_1 = -6.19e-2).
    refine = json.loads(
        (HERE / "stable-side-refinement.json").read_text()
    )
    u_values = np.asarray(refine["values_by_order"]["20"])
    u_rows = walk([6.05, 6.1, 6.15, 6.2, 6.3, 6.375, 6.5, 6.75, 7.0,
                   7.25, 7.5, 7.75, 8.0], u_values, "U")

    # Q1: regenerate family S at 6.375 through the full order ladder
    # (the bisection chain landed on S there from this seed route).
    settings = dict(radial_nodes=32, angular_nodes=16, radius=6.375)
    values = fit(root20, 16)
    row = {}
    for order in (16, 18, 20):
        row = solve_order(order, values if order == 16
                          else pad(values, order), settings)
        values = np.asarray(row.pop("values"))
    s_values = values
    s0_lambda = local_lambda(settings, 20, s_values)
    print(f"[S-seed] R=6.375: E={row['energy']:.9f} "
          f"lam1={s0_lambda:+.6e}", flush=True)
    s_rows = walk([6.2, 6.1, 6.05, 6.0234375, 6.01171875,
                   6.005859375, 6.0029296875, 6.0, 5.995, 5.99, 5.95,
                   5.9], s_values, "S")


    json.dump({"U_ascent": u_rows, "S_seed": {
        "radius": 6.375, "energy": float(row["energy"]),
        "lambda_1": s0_lambda,
        "values": s_values.tolist()}, "S_descent": s_rows},
        open(HERE / "family-resolution.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
