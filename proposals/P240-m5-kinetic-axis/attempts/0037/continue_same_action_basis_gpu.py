"""Nested-basis roots of the unchanged P240 spectral-Cartan functional."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import root


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[0] / "0036" / "solve_spectral_cartan_hedgehog_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0036", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
S = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = S
SPEC.loader.exec_module(S)


def solve_stage(values, radial_order, angular_modes, maxfev=200):
    settings = {
        "radial_order": radial_order,
        "angular_modes": angular_modes,
        "radial_nodes": 24,
        "angular_nodes": 20,
        "radius": 6.0,
    }
    oracle = S.ExactOracle(settings)
    initial_energy = oracle.evaluate(values)[0]
    scale = max(1.0, abs(initial_energy))
    solved = root(
        lambda current: oracle.evaluate(current)[1] / scale,
        values,
        jac=lambda current: oracle.evaluate(current)[2] / scale,
        method="hybr",
        options={"xtol": 1.0e-11, "maxfev": maxfev},
    )
    final = np.asarray(solved.x, dtype=np.float64)
    energy, gradient, hessian, components = oracle.evaluate(final)
    row = {
        "radial_order": radial_order,
        "angular_modes": angular_modes,
        "coefficient_count": final.size,
        "success": bool(solved.success),
        "status": int(solved.status),
        "message": str(solved.message),
        "function_evaluations": int(solved.nfev),
        "jacobian_evaluations": int(solved.njev),
        "exact_oracle_evaluations": oracle.evaluations,
        "energy": energy,
        "gradient_inf_relative": float(np.max(np.abs(gradient)) / max(1.0, abs(energy))),
        "minimum_hessian_eigenvalue": float(np.linalg.eigvalsh((hessian + hessian.T) / 2)[0]),
        "components": components,
    }
    return final, hessian, row


def main() -> int:
    stages = ((1, 1), (2, 1), (2, 2), (3, 2), (4, 3))
    rows = []
    values = None
    current_shape = None
    first_stage = None
    for split_seed in (0.125, 0.5, 2.0):
        start = S.initial_values(1, 1)
        start.reshape(3, 1, 1)[2, 0, 0] = split_seed
        candidate, hessian, row = solve_stage(start, 1, 1)
        row["initial_split_amplitude"] = split_seed
        rows.append(row)
        if row["success"] and row["gradient_inf_relative"] <= 1.0e-9:
            values = candidate
            current_shape = (1, 1)
            first_stage = row
            break
    if values is None:
        payload = {
            "campaign": "P240",
            "attempt": "0037",
            "status": "failed_first_unmodified_subspace",
            "stages": rows,
            "final_gate_pass": False,
        }
        print("P240_BASIS_CONTINUATION_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
        return 2

    continuation_rows = [first_stage]
    for radial_order, angular_modes in stages[1:]:
        values = S.pad_values(values, current_shape, (radial_order, angular_modes))
        values, hessian, row = solve_stage(values, radial_order, angular_modes)
        continuation_rows.append(row)
        current_shape = (radial_order, angular_modes)
        if not row["success"] or row["gradient_inf_relative"] > 1.0e-9:
            payload = {
                "campaign": "P240",
                "attempt": "0037",
                "status": "failed_before_full_root",
                "seed_trials": rows,
                "stages": continuation_rows,
                "final_gate_pass": False,
            }
            print("P240_BASIS_CONTINUATION_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
            return 2

    settings = {
        "radial_order": 4,
        "angular_modes": 3,
        "radial_nodes": 24,
        "angular_nodes": 20,
        "radius": 6.0,
    }
    final_oracle = S.ExactOracle(settings)
    total, gradient, hessian, components = final_oracle.evaluate(values)
    gradient_relative = float(np.max(np.abs(gradient)) / max(1.0, abs(total)))
    hessian_symmetry = float(np.max(np.abs(hessian - hessian.T)) / max(1.0, np.max(np.abs(hessian))))
    minimum_eigenvalue = float(np.linalg.eigvalsh((hessian + hessian.T) / 2)[0])
    step = 2.0e-5
    directional = []
    for direction in S.deterministic_directions(values.size):
        plus = S.energy_value(values + step * direction, settings)
        minus = S.energy_value(values - step * direction, settings)
        directional.append(abs((plus - minus) / (2 * step)) / max(1.0, abs(total)))

    withheld_settings = dict(settings, radial_order=5, angular_modes=4)
    withheld_values = S.pad_values(values, (4, 3), (5, 4))
    withheld_oracle = S.ExactOracle(withheld_settings)
    withheld_total, withheld_gradient, _, withheld_components = withheld_oracle.evaluate(withheld_values)
    withheld_relative = float(np.max(np.abs(withheld_gradient)) / max(1.0, abs(withheld_total)))

    quadrature_settings = dict(settings, radial_nodes=32, angular_nodes=28)
    quadrature_oracle = S.ExactOracle(quadrature_settings)
    quadrature_total, quadrature_gradient, _, quadrature_components = quadrature_oracle.evaluate(values)
    quadrature_energy_change = abs(quadrature_total - total) / max(1.0, abs(total), abs(quadrature_total))
    quadrature_gradient_relative = float(np.max(np.abs(quadrature_gradient)) / max(1.0, abs(quadrature_total)))

    output = HERE / "coefficients-order4x3.npz"
    np.savez_compressed(output, coefficients=values.reshape(3, 4, 3), radius=np.array(6.0))
    payload = {
        "campaign": "P240",
        "attempt": "0037",
        "environment": {
            "torch": S.torch.__version__,
            "cuda_runtime": S.torch.version.cuda,
            "device": S.torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "seed_trials": rows,
        "stages": continuation_rows,
        "final": {
            "energy": total,
            "gradient_inf_relative": gradient_relative,
            "independent_directional_relative_max": float(max(directional)),
            "hessian_symmetry_relative_max": hessian_symmetry,
            "minimum_hessian_eigenvalue": minimum_eigenvalue,
            "components": components,
            "withheld_order_5x4_gradient_inf_relative": withheld_relative,
            "withheld_components": withheld_components,
            "higher_quadrature_energy_relative_change": float(quadrature_energy_change),
            "higher_quadrature_gradient_inf_relative": quadrature_gradient_relative,
            "higher_quadrature_components": quadrature_components,
        },
        "output_coefficients": str(output),
    }
    payload["final_gate_pass"] = bool(
        continuation_rows[-1]["success"]
        and gradient_relative <= 1.0e-9
        and max(directional) <= 2.0e-8
        and hessian_symmetry <= 1.0e-10
        and minimum_eigenvalue >= -1.0e-8
        and components["inertia"] > 0
        and np.isfinite(components["frequency"])
        and components["frequency"] > 0
        and withheld_relative <= 1.0e-6
        and quadrature_energy_change <= 1.0e-6
        and quadrature_gradient_relative <= 2.0e-7
    )
    print("P240_BASIS_CONTINUATION_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["final_gate_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
