"""Certify the Morse index of the frozen 1D radial profile in enlarged bases.

Second stage of the Kelvin-method validation (issue #146 comment 5360116141).
Takes the N=20 stationary root from solve_radial_1d.py, embeds it zero-padded
into larger radial bases (same physical profile, same functional, fixed
quadrature), and computes the exact Hessian of the second-variation bilinear
form in each basis.  Nested subspaces + min-max => lambda_min(M) is
non-increasing in M and bounded above by the continuum infimum.  Convergence to
a negative limit certifies a genuine continuum saddle; collapse toward 0 from
above would expose the negativity as representation sensitivity.

Also: quadrature-refinement check on the frozen profile, nodal census and field
fractions of the certified lowest mode, and a multi-seed branch hunt for any
stable stationary branch in the spherically symmetric sector.
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


def load_root(order=20):
    rows = json.loads((HERE / "radial-results.json").read_text())
    row = [r for r in rows if r["radial_order"] == order][0]
    return np.asarray(row["values"], dtype=np.float64)


def pad(values: np.ndarray, new_order: int):
    old = values.reshape(3, -1)
    out = np.zeros((3, new_order), dtype=np.float64)
    out[:, : old.shape[1]] = old
    return out.ravel()


def main():
    root20 = load_root(20)

    print("== frozen-profile second variation in enlarged bases ==")
    quad = dict(radial_nodes=48, angular_nodes=16, radius=6.0)
    spectrum = {}
    lowest_mode = None
    for m in (20, 24, 28, 32):
        settings = dict(quad, radial_order=m)
        oracle = Oracle(settings)
        values = pad(root20, m)
        total, grad, hess, comp = oracle.evaluate(values)
        sym = (hess + hess.T) / 2
        eigenvalues, eigenvectors = np.linalg.eigh(sym)
        spectrum[m] = eigenvalues.tolist()
        print(
            f"M={m:2d}  E={total:.8f}  |g|/|E|={np.max(np.abs(grad))/abs(total):.2e}  "
            f"lambda_min={eigenvalues[0]:.6f}  lambda_2={eigenvalues[1]:.6f}  "
            f"lambda_3={eigenvalues[2]:.6f}  lambda_max={eigenvalues[-1]:.3e}",
            flush=True,
        )
        if m == 20:
            fractions, nodes = analyze_mode(eigenvectors[:, 0])
            lowest_mode = {
                "field_fractions": [float(f) for f in fractions],
                "radial_nodes_split": nodes,
            }
            print(f"   lowest mode: fractions={np.round(fractions, 5).tolist()}  nodes={nodes}")
            for rq, aq in ((56, 20), (64, 24)):
                o2 = Oracle(dict(radial_order=m, radial_nodes=rq, angular_nodes=aq, radius=6.0))
                t2, _, h2, _ = o2.evaluate(values)
                e2 = np.linalg.eigvalsh((h2 + h2.T) / 2)
                print(
                    f"   quadrature {rq}x{aq}: E={t2:.8f} "
                    f"(dE={abs(t2-total)/abs(total):.2e})  lambda_min={e2[0]:.6f}",
                    flush=True,
                )

    print()
    print("== multi-seed branch hunt (N=12, spherically symmetric sector) ==")
    seeds = {}
    base = np.zeros((3, 12))
    base[2, 0] = 0.5
    seeds["split_const"] = base.ravel()
    base2 = np.zeros((3, 12))
    base2[1, 0] = 0.5
    seeds["tangent_const"] = base2.ravel()
    base3 = np.zeros((3, 12))
    base3[0, 0] = 0.5
    seeds["q_const"] = base3.ravel()
    rng = np.random.default_rng(7)
    seeds["random_a"] = (0.1 * rng.standard_normal((3, 12))).ravel()
    seeds["random_b"] = (
        0.05 * rng.standard_normal((3, 12)) + np.array([0, 0, 0.3])[:, None]
    ).ravel()

    settings = dict(radial_order=12, radial_nodes=32, angular_nodes=16, radius=6.0)
    findings = []
    for name, seed in seeds.items():
        oracle = Oracle(settings)

        def residual(v):
            total, grad, _, _ = oracle.evaluate(v)
            return grad / max(1.0, abs(total))

        def jacobian(v):
            _, _, hess, _ = oracle.evaluate(v)
            return hess / max(1.0, abs(oracle.cached_result[0]))

        sol = root(residual, np.asarray(seed, dtype=np.float64), jac=jacobian,
                   method="hybr", options=dict(xtol=1e-14, maxfev=300))
        v = np.asarray(sol.x)
        total, grad, hess, comp = oracle.evaluate(v)
        rel = float(np.max(np.abs(grad)) / max(1.0, abs(total)))
        eig = np.linalg.eigvalsh((hess + hess.T) / 2)
        idx = int(np.sum(eig < -1e-8 * max(1.0, float(np.max(np.abs(eig))))))
        findings.append(dict(seed=name, success=bool(sol.success), energy=total,
                             relative_gradient=rel, lambda_min=float(eig[0]),
                             morse_index=idx, inertia=comp["inertia"],
                             frequency=comp["frequency"]))
        print(
            f"{name:>14s}  conv={sol.success}  |g|/|E|={rel:.1e}  E={total:.8f}  "
            f"inertia={comp['inertia']:.6f}  omega={comp['frequency']:.6f}  "
            f"lambda_min={eig[0]:.6f}  index={idx}",
            flush=True,
        )

    (HERE / "certify-results.json").write_text(json.dumps(
        {"spectrum": {str(k): v for k, v in spectrum.items()},
         "lowest_mode": lowest_mode,
         "branch_hunt": findings}, indent=2))
    print("wrote certify-results.json")


if __name__ == "__main__":
    main()
