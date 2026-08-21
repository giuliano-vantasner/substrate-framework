"""P240 attempt 0044: clean continuation — honest quadrature + acceptance gate.

Lessons baked in:
  - solving grid must integrate the basis: radial_nodes >= 4 * order;
  - a root is accepted ONLY if its energy reproduces at doubled quadrature
    (shift < 1e-6) — rejects aliasing-exploiting spurious stationary points;
  - order escalates with R (Chebyshev cutoff ~ 2*pi*R/order held near 2.5);
  - checkpoints after every accepted step.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE / ".." / "0041")); sys.path.insert(0, str(HERE / ".." / "0042"))

from debox_ladder import extract_A, project_root, solve_radius
from solve_radial_1d import energy_radial
from xspace_energy import XOracle

STATE = HERE / "clean-ladder-state.json"


def energy_at(values, order, radius, rn, an=16):
    t, _ = energy_radial(torch.tensor(np.asarray(values, dtype=np.float64)),
                         radial_order=order, radial_nodes=rn, angular_nodes=an, radius=radius)
    return float(t)


def main():
    state = {"ladder": []}
    if STATE.exists():
        state = json.loads(STATE.read_text())
    if not state["ladder"]:
        rows = json.loads((HERE / ".." / "0042" / "largeR-roots.json").read_text())
        v13 = None
        prev = json.loads((HERE / "ladder-state.json").read_text())["ladder"]
        for r in prev:  # reuse the validated R=13 root if present
            if r["radius"] == 13.0:
                v13 = r["values"]
        seed_order = 16
        seed = v13 if v13 is not None else np.asarray(rows["R12"]["values"])
        radius = 13.0 if v13 is not None else 12.0
        row = solve_radius(seed_order, seed, radius, radial_nodes=4 * seed_order)
        row["values"] = np.asarray(row["values"]).tolist()
        state["ladder"].append(row)
        print(f"anchor R={radius} order={seed_order} E={row['energy']:.8f}", flush=True)

    for target in (14.0, 15.0, 16.0, 17.0, 18.0):
        last = state["ladder"][-1]
        if target <= last["radius"]:
            continue
        order = last["order"] + 4
        nodes = 4 * order
        seed = project_root(last["values"], last["order"], order)
        row = solve_radius(order, seed, target, radial_nodes=nodes)
        e_verify = energy_at(row["values"], order, target, 2 * nodes)
        shift = abs(e_verify - row["energy"]) / max(1e-30, abs(row["energy"]))
        ok = shift < 1e-6 and row["rel_grad"] < 1e-9
        print(f"R={target} order={order} nodes={nodes} E={row['energy']:.8f} "
              f"verify={e_verify:.8f} shift={shift:.1e} relgrad={row['rel_grad']:.1e} "
              f"{'ACCEPT' if ok else 'REJECT'}", flush=True)
        if not ok:
            print("stopping at first rejected step", flush=True)
            break
        row["values"] = np.asarray(row["values"]).tolist()
        state["ladder"].append(row)
        STATE.write_text(json.dumps(state, indent=2))

        # A-spectrum on the fresh root
        ox = XOracle(row["values"], order, max(48, nodes // 2), 16)
        A, recon = extract_A(ox, target, 2 * target, 1.5 * target)
        lam = float(np.linalg.eigvalsh(A)[0])
        state.setdefault("A_spectrum", []).append(
            {"radius": target, "order": order, "lambda_min_A": lam,
             "reconstruction_maxdiff": recon})
        STATE.write_text(json.dumps(state, indent=2))
        print(f"  lambda_min(A) = {lam:+.6e} (recon {recon:.1e})", flush=True)
    print("clean ladder done", flush=True)


if __name__ == "__main__":
    main()
