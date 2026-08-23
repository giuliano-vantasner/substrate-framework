"""Attempt 0005 -- missing frozen-quadrature row at R=14 for candidate F.

The splitting_scale.py wave's R=14 quadrature entry used family-jumped
"U" coefficients (its U-ladder collapsed into S; log preserved).  This
run recomputes the R=14 S ladder cleanly (lambda_1 > 0 asserted) and
evaluates Delta_E under the 48x24 oracle at frozen order-20 fields of
both families (U values from the validated candidate-e.json chain).
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
from window_continuation import pad  # noqa: E402

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


def main() -> int:
    t0 = time.time()
    big = json.loads((REPO / "proposals/P240-m5-kinetic-axis/"
                      "attempts/0042/largeR-roots.json").read_text())
    cand = json.loads((HERE / "candidate-e.json").read_text())
    radius = 14.0

    s16 = np.asarray(big["R14"]["values"])
    s18 = np.asarray(solve_order(18, pad(s16, 18),
                                 dict(SETTINGS, radius=radius))["values"])
    srow = solve_order(20, pad(s18, 20), dict(SETTINGS, radius=radius))
    s20 = np.asarray(srow.pop("values"))
    lam_s = lam1(s20, radius)
    e_s20 = float(srow["energy"])
    assert lam_s > 0 and srow["relative_gradient"] < 1e-6, (
        f"S ladder fingerprint failure: lam={lam_s}")

    u14 = np.asarray(cand["chain_tail_values"]["14.0"])
    e_u20 = float([r for r in cand["u_map"]
                   if r.get("radius") == radius][0]["energy"])
    dq48 = (frozen_energy(u14, radius, nodes=48, angular=24)
            - frozen_energy(s20, radius, nodes=48, angular=24))
    delta20 = e_u20 - e_s20
    payload = {
        "meta": {"elapsed_s": time.time() - t0},
        "radius": radius,
        "E_U20_root": e_u20, "E_S20_root": e_s20,
        "delta_20_root": delta20,
        "delta_quad48_frozen": dq48,
        "quadrature_shift_frac": abs(dq48 - delta20) / abs(delta20),
        "lambda1_S20": lam_s,
        "relgrad_S20": float(srow["relative_gradient"]),
    }
    (HERE / "splitting-dq14.json").write_text(json.dumps(payload, indent=1))
    print(f"[F] R=14: d20={delta20:.9f} dq48={dq48:.9f} "
          f"shift={payload['quadrature_shift_frac']:.3e}", flush=True)
    print("[DONE] splitting-dq14.json written", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
