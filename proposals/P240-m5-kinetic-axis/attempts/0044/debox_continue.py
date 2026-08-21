"""P240 attempt 0044: gentle continuation ladder (radius step 1, order step 4).

The one-shot order jump diverged to spurious stationary points; this runner
tracks the branch with small steps, projects the basis between steps, guards
against energy blowup, and checkpoints after every accepted step.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import root

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / ".." / "0041"))
sys.path.insert(0, str(HERE / ".." / "0042"))

from debox_ladder import extract_A, profile_arrays, project_root, solve_radius  # noqa: E402
from xspace_energy import XOracle  # noqa: E402

ATTEMPTS = HERE.parent
STATE = HERE / "ladder-state.json"


def load_start():
    rows = json.loads((ATTEMPTS / "0042" / "largeR-roots.json").read_text())
    v12 = np.asarray(rows["R12"]["values"])
    return 12.0, v12, v12.size // 3


def main():
    state = {"ladder": []}
    if STATE.exists():
        state = json.loads(STATE.read_text())
    if state["ladder"]:
        last = state["ladder"][-1]
        radius, values, order = last["radius"], np.asarray(last["values"]), last["order"]
    else:
        radius, values, order = load_start()
        row = solve_radius(order, values, radius)
        row["values"] = np.asarray(row["values"]).tolist()
        print(f"anchor R={radius} order={order} E={row['energy']:.8f} "
              f"relgrad={row['rel_grad']:.1e}", flush=True)
        state["ladder"].append(row)

    schedule = [14.0, 16.0, 18.0, 20.0, 22.0, 24.0]
    schedule = [r for r in schedule if r > state["ladder"][-1]["radius"]]
    for target in schedule:
        while radius < target - 1e-9:
            step = min(1.0, target - radius)
            new_radius = radius + step
            new_order = order + (4 if new_radius >= 14.0 and order < 40 else 0)
            seed = project_root(values, order, new_order)
            row = solve_radius(new_order, seed, new_radius)
            accepted = (
                row["rel_grad"] < 1e-9
                and row["energy"] < 3.0 * state["ladder"][-1]["energy"]
                and np.isfinite(row["energy"])
            )
            if not accepted:
                print(f"  rejected R={new_radius} order={new_order} "
                      f"E={row['energy']:.3e} relgrad={row['rel_grad']:.1e}; "
                      f"retrying with half step / same order", flush=True)
                if step > 0.25:
                    schedule.insert(0, new_radius)  # will be retried in smaller steps
                    break
                # last resort: keep order, tiny step
                new_order = order
                seed = project_root(values, order, new_order)
                row = solve_radius(new_order, seed, new_radius)
                if not (row["rel_grad"] < 1e-9 and np.isfinite(row["energy"])
                        and row["energy"] < 3.0 * state["ladder"][-1]["energy"]):
                    print("  stuck; stopping", flush=True)
                    STATE.write_text(json.dumps(state, indent=2))
                    return
            radius, values, order = new_radius, np.asarray(row["values"]), row["order"]
            row["values"] = np.asarray(row["values"]).tolist()
            state["ladder"].append(row)
            STATE.write_text(json.dumps(state, indent=2))
            print(f"R={radius:5.2f} order={order} E={row['energy']:.8f} "
                  f"I={row['inertia']:.6f} lam_branch={row['lambda_min_branch']:+.3e} "
                  f"relgrad={row['rel_grad']:.1e}", flush=True)

    # A-spectrum on the final ladder
    a_rows = []
    for row in state["ladder"]:
        if row["radius"] < 13.0:
            continue
        ox = XOracle(row["values"], row["order"], 48, 16)
        R = row["radius"]
        A, recon = extract_A(ox, R, 2.0 * R, 1.5 * R)
        eigs = np.linalg.eigvalsh(A)
        a_rows.append({"radius": R, "order": row["order"],
                       "lambda_min_A": float(eigs[0]),
                       "reconstruction_maxdiff": recon})
        print(f"A[c(R={R})] order={row['order']}: lambda_min={eigs[0]:+.6e} "
              f"recon={recon:.1e}", flush=True)
    state["A_spectrum"] = a_rows
    STATE.write_text(json.dumps(state, indent=2))
    print("state saved")


if __name__ == "__main__":
    main()
