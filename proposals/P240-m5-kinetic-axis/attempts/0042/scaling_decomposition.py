"""P240 attempt 0042: derivation-first stability classification, v3.

Exact scaling identity, now enforced at the DISCRETE level by fixed-quadrature
x-space evaluation (xspace_energy.XOracle):

    E(R)[c] = R^3 V[c] + (C[c] + Phi[c]) / R,   Phi[c] = 1/(4 I[c])
=>  H(R)  = R^3 A + R^{-1} D
    A = nabla^2 V,  D = nabla^2 (C + Phi)

A and D are extracted from whole Hessians at two radii (exact 2x2 system);
a third radius must reproduce to machine precision.  Consequences:

    lambda_min(R) = R^3 * lambda_min(A + R^{-4} D)
    R -> infinity verdict follows from the spectrum of A alone;
    critical radius R* = s_*^{-1/4} where lambda_min(A + s_* D) = 0.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from xspace_energy import XOracle  # noqa: E402

RESULTS = HERE / "scaling-results.json"
ORDER = 20


def sym(m):
    return (m + m.T) / 2


def main():
    rows = json.loads((HERE / ".." / "0041" / "radial-results.json").read_text())
    root = np.asarray([r for r in rows if r["radial_order"] == ORDER][0]["values"])
    oracle = XOracle(root, ORDER, 48, 16)
    res = {"method": "fixed-quadrature two-radius extraction"}
    _, H6 = oracle.hessian_at(6.0)
    _, H8 = oracle.hessian_at(8.0)
    r1, r2 = 6.0, 8.0
    # H(r1) = r1^3 A + r1^-1 D ; H(r2) = r2^3 A + r2^-1 D
    # combine with weights r2^-1 and r1^-1 so the D terms cancel:
    A = (r2**-1 * H6 - r1**-1 * H8) / (r1**3 / r2 - r2**3 / r1)
    D = (H6 - r1**3 * A) * r1
    _, H10 = oracle.hessian_at(10.0)
    recon_err = float(np.abs(sym(1000.0 * A + D / 10.0) - sym(H10)).max())
    print(f"cross-check R=10 reconstruction max|diff| = {recon_err:.3e}", flush=True)
    res["cross_check_R10_maxdiff"] = recon_err

    a_eigs = np.linalg.eigvalsh(sym(A))
    d_eigs = np.linalg.eigvalsh(sym(D))
    print(f"A: lambda_min={a_eigs[0]:+.8e} lambda_max={a_eigs[-1]:+.4e}", flush=True)
    print(f"D: lambda_min={d_eigs[0]:+.8e} lambda_max={d_eigs[-1]:+.4e}", flush=True)
    res["matrices"] = {"A_bottom6": a_eigs[:6].tolist(),
                       "A_top2": a_eigs[-2:].tolist(),
                       "D_bottom4": d_eigs[:4].tolist()}

    # Stage 2: pencil vs direct frozen-background Hessians
    pencil = {}
    for radius in (6.0, 7.5, 8.0, 10.0):
        s = radius**-4
        lam = radius**3 * float(np.linalg.eigvalsh(sym(A + s * D))[0])
        _, H = oracle.hessian_at(radius)
        lam_direct = float(np.linalg.eigvalsh(sym(H))[0])
        pencil[f"R={radius}"] = {"pencil": lam, "direct": lam_direct,
                                 "abs_diff": abs(lam - lam_direct)}
        print(f"R={radius}: pencil={lam:+.8e} direct={lam_direct:+.8e} "
              f"diff={abs(lam - lam_direct):.2e}", flush=True)
    res["pencil_vs_direct_frozen_background"] = pencil

    # Stage 3: asymptotic verdict and critical radius
    s_grid = np.geomspace(20.0**-4, 1.0, 4000)[::-1]
    zeros = []
    prev = None
    for s in s_grid:
        val = float(np.linalg.eigvalsh(sym(A + s * D))[0])
        if prev is not None and prev[1] < 0 <= val:
            zeros.append((prev[0] + s) / 2)
        prev = (s, val)
    res["asymptotic"] = {
        "lambda_min_A": float(a_eigs[0]),
        "verdict": ("intrinsic_instability_at_large_R"
                    if a_eigs[0] < 0 else
                    "stability_strengthening_R3_growth"),
        "predicted_critical_R": [float(z) ** -0.25 for z in zeros],
        "A_negative_directions": int(np.sum(a_eigs < 0)),
    }
    print(f"verdict: {res['asymptotic']['verdict']}; "
          f"negative directions in A: {res['asymptotic']['A_negative_directions']}",
          flush=True)
    print("predicted R* =", [round(float(z) ** -0.25, 4) for z in zeros], flush=True)

    RESULTS.write_text(json.dumps(res, indent=2))
    print("wrote scaling-results.json")


if __name__ == "__main__":
    main()
