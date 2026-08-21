"""Test the delta=0 (polar/azimuthal-symmetric) subsector.

The hedgehog energy should be even under delta -> -delta (exchange of the polar
and azimuthal eigenvalue channels), so delta == 0 is a stationary subsector.
Solve the (q, tangent) system with split pinned to zero, then evaluate the FULL
three-field Hessian at that point.  Outcomes:
  - full-space lambda_min > 0: stable electron candidate found, no action change;
  - negative curvature concentrated in the split direction: the split channel is
    intrinsically unstable in this action and a stabilizing term is required.

Seeding note: constant-coefficient seeds diverge (see certify-results.json
branch hunt), so the (q, t) seed is taken from the converged full root's own
q/t blocks, which are already near-stationary in the q/t sector.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import root

HERE = Path(__file__).resolve().parent

import sys

sys.path.insert(0, str(HERE))
from solve_radial_1d import Oracle, analyze_mode  # noqa: E402


def main():
    settings_base = dict(radial_nodes=32, angular_nodes=16, radius=6.0)
    full_root = np.asarray(
        [
            r
            for r in json.loads((HERE / "radial-results.json").read_text())
            if r["radial_order"] == 20
        ][0]["values"]
    ).reshape(3, 20)

    rows = []
    for order in (8, 10, 12, 14, 16):
        settings = dict(settings_base, radial_order=order)
        oracle = Oracle(settings)
        n_qt = 2 * order

        def expand(x):
            full = np.zeros(3 * order)
            full[:n_qt] = x
            return full

        def residual(x):
            total, grad, _, _ = oracle.evaluate(expand(x))
            return grad[:n_qt] / max(1.0, abs(total))

        def jacobian(x):
            _, _, hess, _ = oracle.evaluate(expand(x))
            return hess[:n_qt, :n_qt] / max(1.0, abs(oracle.cached_result[0]))

        seed = np.zeros(n_qt)
        take = min(20, order)
        seed[:take] = full_root[0, :take]
        seed[order : order + take] = full_root[1, :take]

        sol = root(residual, seed, jac=jacobian, method="hybr",
                   options=dict(xtol=1e-14, maxfev=400))
        x = np.asarray(sol.x)
        full = expand(x)
        total, grad, hess, comp = oracle.evaluate(full)
        rel_qt = float(np.max(np.abs(grad[:n_qt])) / max(1.0, abs(total)))
        rel_split = float(np.max(np.abs(grad[n_qt:])) / max(1.0, abs(total)))
        sym = (hess + hess.T) / 2
        eigenvalues, eigenvectors = np.linalg.eigh(sym)
        lam_min = float(eigenvalues[0])
        index = int(np.sum(eigenvalues < -1e-8 * max(1.0, float(np.max(np.abs(eigenvalues))))))
        fractions, nodes = analyze_mode(eigenvectors[:, 0])
        row = dict(
            radial_order=order,
            success=bool(sol.success),
            energy=total,
            relative_gradient_qt=rel_qt,
            relative_gradient_split=rel_split,
            lambda_min=lam_min,
            morse_index=index,
            inertia=comp["inertia"],
            frequency=comp["frequency"],
            mode_fractions=[float(f) for f in fractions],
            mode_nodes=nodes,
            values=full.tolist(),
            lowest_eigenvalues=[float(e) for e in eigenvalues[:6]],
        )
        rows.append(row)
        print(
            f"N={order:2d}  conv={sol.success}  |g_qt|/|E|={rel_qt:.1e}  "
            f"|g_split|/|E|={rel_split:.1e}  E={total:.8f}  inertia={comp['inertia']:.6f}  "
            f"omega={comp['frequency']:.6f}  lambda_min={lam_min:.6f}  index={index}  "
            f"fractions={np.round(fractions, 4).tolist()}",
            flush=True,
        )

    (HERE / "delta0-results.json").write_text(json.dumps(rows, indent=2))
    print("wrote delta0-results.json")


if __name__ == "__main__":
    main()
