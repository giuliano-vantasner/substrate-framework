"""Attempt 0004 diagnostic: quadrature response of lambda_1 at frozen values.

The fine-quadrature re-solve in morse_bisection.py reported lambda_min =
+8.13e-06 at R=6.0 where the certified coarse-quadrature spectrum has
lambda_1 = -6.26e-02.  Two explanations:
  (a) the unstable eigenvalue is born by the coarse quadrature and melts
      under refinement (candidate D's threshold would be an artifact);
  (b) the re-solve converged to a DIFFERENT stationary point, and the
      comparison never tested the same field.
This script decides without any root-finding: hold the committed R=6
order-20 coefficient vector frozen and re-evaluate its Hessian spectrum
across quadrature densities and solver orders.  Energy and gradient are
monitored so a quadrature that cannot even integrate this field honestly
is visible.
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

from solve_radial_1d import Oracle  # noqa: E402
from window_continuation import fit  # noqa: E402


def main() -> int:
    rows = json.loads(
        (P240 / "0041" / "radial-results.json").read_text()
    )
    root20 = np.asarray(
        [r for r in rows if r["radial_order"] == 20][0]["values"]
    )
    out = []
    print(f"{'nodes':>6} {'ang':>4} {'ord':>4} {'energy':>16} "
          f"{'lam1':>14} {'lam2':>12} {'lam3':>12}", flush=True)
    for nodes, angular in ((32, 16), (40, 20), (48, 24), (64, 32),
                           (80, 40), (96, 48)):
        for order in (16, 18, 20):
            values = root20 if order == 20 else fit(root20, order)
            oracle = Oracle(dict(radial_order=order, radial_nodes=nodes,
                                 angular_nodes=angular, radius=6.0))
            total, grad, hess, _ = oracle.evaluate(values)
            sym = (hess + hess.T) / 2.0
            ev = np.linalg.eigvalsh(sym)
            rel_grad = float(np.max(np.abs(grad)) / max(1.0, abs(total)))
            row = {
                "nodes": nodes, "angular": angular, "order": order,
                "energy": float(total), "relative_gradient": rel_grad,
                "lambda_1": float(ev[0]), "lambda_2": float(ev[1]),
                "lambda_3": float(ev[2]),
            }
            out.append(row)
            print(f"{nodes:>6} {angular:>4} {order:>4} {total:>16.9f} "
                  f"{ev[0]:>14.6e} {ev[1]:>12.4e} {ev[2]:>12.4e}",
                  flush=True)
    json.dump(out, open(HERE / "quadrature-probe.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
