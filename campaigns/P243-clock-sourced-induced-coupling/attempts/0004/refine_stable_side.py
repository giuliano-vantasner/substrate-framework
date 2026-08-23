"""Attempt 0004 diagnostic: stable-side ladder extension + frozen-field
quadrature sign check at the upper bracket end R = 6.01171875.

Open systematics left by morse_bisection.py:
  1. lambda_min on the stable side halves per solver order (3.69e-05 ->
     1.67e-05 -> 8.08e-06 at N16/18/20); does it converge to a strictly
     positive continuum value or slide to a zero?  Orders 22 and 24
     decide between geometric-to-zero and saturation.
  2. The sign classification at the bracket ends must survive quadrature
     refinement AT FIXED FIELD VALUES (the re-solve-based check in
     morse_bisection.py jumped roots and is superseded by this probe
     protocol; see quadrature-probe.json for the R=6.0 end).
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

R_HI = 6.01171875


def local_spectrum(settings, order, values):
    oracle = Oracle(dict(settings, radial_order=order))
    _, _, hess, _ = oracle.evaluate(values)
    sym = (hess + hess.T) / 2.0
    return np.linalg.eigvalsh(sym)


def main() -> int:
    settings = dict(radial_nodes=32, angular_nodes=16, radius=R_HI)
    # Seed: continue from the committed R=6 order-20 root exactly as the
    # bisection did (fit to 16), then climb orders including 22, 24.
    rows = json.loads(
        (P240 / "0041" / "radial-results.json").read_text()
    )
    root20 = np.asarray(
        [r for r in rows if r["radial_order"] == 20][0]["values"]
    )
    values = fit(root20, 16)
    ladder = {}
    saved_values = {}
    for order in (16, 18, 20, 22, 24):
        row = solve_order(order, values if order == 16 else pad(values,
                                                                order),
                          settings)
        values = np.asarray(row.pop("values"))
        spec = local_spectrum(settings, order, values)
        rel_grad = float(row["relative_gradient"])
        ladder[str(order)] = {
            "lambda_min": float(spec[0]),
            "lambda_2": float(spec[1]),
            "energy": float(row["energy"]),
            "relative_gradient": rel_grad,
            "mode_fractions": row.pop("mode_fractions"),
            "mode_radial_nodes_split": row.pop("mode_radial_nodes_split"),
        }
        saved_values[str(order)] = values.tolist()
        print(f"N={order}: lam={spec[0]:+.6e} lam2={spec[1]:.4e} "
              f"E={row['energy']:.9f} |g|/E={rel_grad:.2e}", flush=True)

    # Ratios decide geometric-vs-saturated.
    lams = [ladder[o]["lambda_min"] for o in ("16", "18", "20", "22",
                                              "24")]
    ratios = [lams[i + 1] / lams[i] for i in range(len(lams) - 1)]
    print("ratios:", [f"{r:.3f}" for r in ratios], flush=True)

    # Frozen-field quadrature sweep at the highest resolved order.
    sweep = []
    for nodes, angular in ((32, 16), (48, 24), (64, 32), (96, 48)):
        vals = np.asarray(saved_values["24"])
        oracle = Oracle(dict(radial_order=24, radial_nodes=nodes,
                             angular_nodes=angular, radius=R_HI))
        total, grad, hess, _ = oracle.evaluate(vals)
        sym = (hess + hess.T) / 2.0
        ev = np.linalg.eigvalsh(sym)
        sweep.append({
            "nodes": nodes, "angular": angular,
            "energy": float(total),
            "relative_gradient":
                float(np.max(np.abs(grad)) / max(1.0, abs(total))),
            "lambda_1": float(ev[0]), "lambda_2": float(ev[1]),
        })
        print(f"sweep {nodes:>3}/{angular:>3}: lam1={ev[0]:+.6e} "
              f"E={total:.9f}", flush=True)

    json.dump({
        "radius": R_HI,
        "ladder": ladder,
        "order_ratios": ratios,
        "frozen_field_quadrature_sweep": sweep,
        "values_by_order": saved_values,
    }, open(HERE / "stable-side-refinement.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
