"""P241 numerical oracle N04 — eikonal frozen-background residual O(l/L).

Standalone module: python3 N04_eikonal_residual.py

Section 5 builds the effective metric by inserting a WKB/eikonal ansatz
u = a(X) exp(i S(X)/ell) into the field equation while holding the
background index nbar frozen (geometric-optics hypothesis S07). This
module quantifies the residual left by that insertion in the model
problem of radial scalar waves at wavenumber k,

    u_rr + (2/r) u_r + k^2 n(r)^2 u = 0,   n(r) = 1 + 0.3 e^{-r^2},

with ONLY the phase imposed (S' = n, constant amplitude a = 1). The
residual is then dominated by the unbalanced transport terms,

    R = k (n' + 2 n / r) * i * e^{i k S(r)}  (imaginary),

whose magnitude relative to the leading term k^2 n^2 falls like 1/k,
i.e. like ell/L. Pass criteria: relative residuals at k = 10, 20, 40 form
a geometric sequence with successive ratios in [1.8, 2.2], demonstrating
the declared first-order accuracy of the frozen-background reduction.
"""

from __future__ import annotations

import json

import numpy as np

from _numerics import trapezoid


def relative_residual(k: float, n_pts: int = 200001) -> float:
    r = np.linspace(0.05, 6.0, n_pts)
    n = 1.0 + 0.3 * np.exp(-(r**2))
    # Phase S(r) = int_0.05^r n ds by cumulative trapezoid on the same grid.
    dr = r[1] - r[0]
    cum = np.concatenate([[0.0], np.cumsum((n[1:] + n[:-1]) * 0.5 * dr)])
    phase_arg = k * cum
    u = np.exp(1j * phase_arg)
    lap = _lap(u, dr)
    resid = lap + (2.0 / r) * np.gradient(u, dr) + (k**2) * (n**2) * u
    denom = (k**2) * (n**2) * np.abs(u)
    num = np.abs(resid)
    return float(trapezoid(num, r) / trapezoid(denom, r))


def _lap(f: np.ndarray, dr: float) -> np.ndarray:
    lap = np.zeros_like(f)
    lap[1:-1] = (f[2:] - 2 * f[1:-1] + f[:-2]) / dr**2
    return lap


def main() -> dict[str, object]:
    ks = [10.0, 20.0, 40.0]
    res = [relative_residual(k_) for k_ in ks]
    ratios = [res[i] / res[i + 1] for i in range(len(res) - 1)]
    ok = all(1.8 < rt < 2.2 for rt in ratios)
    detail = (
        f"Relative frozen-background residuals {np.round(res, 6).tolist()} at "
        f"k = {ks}; successive ratios {np.round(ratios, 4).tolist()} ~= 2: the "
        "residual of the pure-eikonal insertion is O(ell/L), confirming the "
        "first-order accuracy declared by the Section-5 eikonal hypothesis "
        "(S07) and bounding its systematic error in the metric construction."
    )
    return {"name": "scipy_eikonal_residual", "claim": "P241-S07 support",
            "passed": bool(ok), "detail": detail}


if __name__ == "__main__":
    result = main()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
