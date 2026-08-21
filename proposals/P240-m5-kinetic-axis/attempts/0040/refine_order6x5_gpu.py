"""Resolve the P240 spectral-Cartan branch in the 6x5 smooth basis."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import root


HERE = Path(__file__).resolve().parent
ATTEMPTS = HERE.parents[0]
SOURCE = ATTEMPTS / "0039" / "refine_order5x4_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0039_order6", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
R = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = R
SPEC.loader.exec_module(R)
S = R.S


def main() -> int:
    with np.load(ATTEMPTS / "0039" / "coefficients-order5x4.npz") as state:
        initial = S.pad_values(
            np.asarray(state["coefficients"], dtype=np.float64).ravel(),
            (5, 4),
            (6, 5),
        )
    settings = {
        "radial_order": 6,
        "angular_modes": 5,
        "radial_nodes": 32,
        "angular_nodes": 28,
        "radius": 6.0,
    }
    oracle = S.ExactOracle(settings)
    initial_energy = oracle.evaluate(initial)[0]
    scale = max(1.0, abs(initial_energy))
    residual = lambda values: oracle.evaluate(values)[1] / scale
    jacobian = lambda values: oracle.evaluate(values)[2] / scale
    primary = root(
        residual,
        initial,
        jac=jacobian,
        method="hybr",
        options={"xtol": 1.0e-11, "maxfev": 320},
    )
    values = np.asarray(primary.x, dtype=np.float64)
    total, gradient, hessian, components = oracle.evaluate(values)
    relative = float(np.max(np.abs(gradient)) / max(1.0, abs(total)))
    correction = None
    if relative > 1.0e-9:
        correction = root(
            residual,
            values,
            jac=jacobian,
            method="lm",
            options={"ftol": 1.0e-13, "xtol": 1.0e-13, "gtol": 1.0e-13, "maxiter": 900},
        )
        values = np.asarray(correction.x, dtype=np.float64)
        total, gradient, hessian, components = oracle.evaluate(values)
        relative = float(np.max(np.abs(gradient)) / max(1.0, abs(total)))

    symmetric = (hessian + hessian.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(symmetric)
    mode = eigenvectors[:, 0]
    symmetry = float(np.max(np.abs(hessian - hessian.T)) / max(1.0, np.max(np.abs(hessian))))
    directional = []
    for direction in S.deterministic_directions(values.size):
        step = 2.0e-5
        plus = S.energy_value(values + step * direction, settings)
        minus = S.energy_value(values - step * direction, settings)
        directional.append(abs((plus - minus) / (2 * step)) / max(1.0, abs(total)))
    curvatures = {}
    curvature_errors = {}
    for step in (0.004, 0.002, 0.001, 0.0005):
        curvature = (
            S.energy_value(values + step * mode, settings)
            - 2 * total
            + S.energy_value(values - step * mode, settings)
        ) / step**2
        curvatures[str(step)] = float(curvature)
        curvature_errors[str(step)] = float(
            abs(curvature - eigenvalues[0])
            / max(1.0, abs(curvature), abs(eigenvalues[0]))
        )

    withheld_settings = dict(
        settings, radial_order=7, angular_modes=6, radial_nodes=36, angular_nodes=32
    )
    withheld_values = S.pad_values(values, (6, 5), (7, 6))
    withheld_total, withheld_gradient, withheld_components = R.value_gradient(
        withheld_values, withheld_settings
    )
    withheld_relative = float(np.max(np.abs(withheld_gradient)) / max(1.0, abs(withheld_total)))
    quadrature_settings = dict(settings, radial_nodes=40, angular_nodes=36)
    quadrature_total, quadrature_gradient, quadrature_components = R.value_gradient(
        values, quadrature_settings
    )
    quadrature_change = abs(quadrature_total - total) / max(1.0, abs(total), abs(quadrature_total))
    quadrature_gradient_relative = float(np.max(np.abs(quadrature_gradient)) / max(1.0, abs(quadrature_total)))

    mode_tensor = mode.reshape(3, 6, 5)
    mode_structure = {
        "q_fraction": float(np.sum(mode_tensor[0] ** 2)),
        "tangent_fraction": float(np.sum(mode_tensor[1] ** 2)),
        "split_fraction": float(np.sum(mode_tensor[2] ** 2)),
        "highest_radial_fraction": float(np.sum(mode_tensor[:, -1, :] ** 2)),
        "highest_angular_fraction": float(np.sum(mode_tensor[:, :, -1] ** 2)),
    }
    output = HERE / "coefficients-order6x5.npz"
    np.savez_compressed(
        output,
        coefficients=values.reshape(3, 6, 5),
        minimum_mode=mode_tensor,
    )
    payload = {
        "campaign": "P240",
        "attempt": "0040",
        "candidate": "D_fixed_j_two_clock_spectral_cartan_one_body",
        "environment": {
            "torch": S.torch.__version__,
            "cuda_runtime": S.torch.version.cuda,
            "device": S.torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "primary": {
            "success": bool(primary.success),
            "status": int(primary.status),
            "message": str(primary.message),
            "function_evaluations": int(primary.nfev),
            "jacobian_evaluations": int(primary.njev),
        },
        "correction": None if correction is None else {
            "success": bool(correction.success),
            "status": int(correction.status),
            "message": str(correction.message),
            "function_evaluations": int(correction.nfev),
            "jacobian_evaluations": int(correction.njev),
        },
        "exact_oracle_evaluations": oracle.evaluations,
        "stationary": {
            "energy": total,
            "gradient_inf_relative": relative,
            "independent_directional_relative_max": float(max(directional)),
            "hessian_symmetry_relative_max": symmetry,
            "minimum_hessian_eigenvalue": float(eigenvalues[0]),
            "centered_energy_curvature": curvatures,
            "centered_curvature_relative_error": curvature_errors,
            "components": components,
            "mode_structure": mode_structure,
        },
        "withheld_order_7x6": {
            "energy": withheld_total,
            "gradient_inf_relative": withheld_relative,
            "components": withheld_components,
        },
        "higher_quadrature_40x36": {
            "energy": quadrature_total,
            "energy_relative_change": float(quadrature_change),
            "gradient_inf_relative": quadrature_gradient_relative,
            "components": quadrature_components,
        },
        "output_coefficients": str(output),
    }
    smallest_errors = [curvature_errors["0.001"], curvature_errors["0.0005"]]
    payload["one_body_gate_pass"] = bool(
        relative <= 1.0e-9
        and max(directional) <= 2.0e-8
        and symmetry <= 1.0e-10
        and eigenvalues[0] >= -1.0e-8
        and max(smallest_errors) <= 2.0e-4
        and quadrature_change <= 1.0e-6
        and quadrature_gradient_relative <= 2.0e-7
    )
    print("P240_ORDER6_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["one_body_gate_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
