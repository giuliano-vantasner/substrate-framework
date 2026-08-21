"""Resolve the P240 spectral-Cartan branch in the 5x4 smooth basis."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import root
import torch


HERE = Path(__file__).resolve().parent
ATTEMPTS = HERE.parents[0]
SOURCE = ATTEMPTS / "0036" / "solve_spectral_cartan_hedgehog_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0036_order5", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
S = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = S
SPEC.loader.exec_module(S)


def value_gradient(values, settings):
    variable = torch.tensor(values, dtype=S.DTYPE, device=S.DEVICE, requires_grad=True)
    total, components = S.energy(variable, **settings)
    gradient = torch.autograd.grad(total, variable)[0]
    torch.cuda.synchronize()
    return (
        float(total.detach()),
        gradient.detach().cpu().numpy(),
        {name: float(value.detach()) for name, value in components.items()},
    )


def main() -> int:
    with np.load(ATTEMPTS / "0038" / "coefficients-branch-0-order4x3.npz") as state:
        initial = S.pad_values(
            np.asarray(state["coefficients"], dtype=np.float64).ravel(),
            (4, 3),
            (5, 4),
        )
    settings = {
        "radial_order": 5,
        "angular_modes": 4,
        "radial_nodes": 28,
        "angular_nodes": 24,
        "radius": 6.0,
    }
    oracle = S.ExactOracle(settings)
    initial_energy = oracle.evaluate(initial)[0]
    scale = max(1.0, abs(initial_energy))

    def residual(values):
        return oracle.evaluate(values)[1] / scale

    def jacobian(values):
        return oracle.evaluate(values)[2] / scale

    primary = root(
        residual,
        initial,
        jac=jacobian,
        method="hybr",
        options={"xtol": 1.0e-11, "maxfev": 260},
    )
    values = np.asarray(primary.x, dtype=np.float64)
    total, gradient, hessian, components = oracle.evaluate(values)
    gradient_relative = float(np.max(np.abs(gradient)) / max(1.0, abs(total)))
    correction = None
    if gradient_relative > 1.0e-9:
        correction = root(
            residual,
            values,
            jac=jacobian,
            method="lm",
            options={"ftol": 1.0e-13, "xtol": 1.0e-13, "gtol": 1.0e-13, "maxiter": 700},
        )
        values = np.asarray(correction.x, dtype=np.float64)
        total, gradient, hessian, components = oracle.evaluate(values)
        gradient_relative = float(np.max(np.abs(gradient)) / max(1.0, abs(total)))

    symmetric_hessian = (hessian + hessian.T) / 2
    eigenvalues, eigenvectors = np.linalg.eigh(symmetric_hessian)
    mode = eigenvectors[:, 0]
    hessian_symmetry = float(np.max(np.abs(hessian - hessian.T)) / max(1.0, np.max(np.abs(hessian))))
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
        settings, radial_order=6, angular_modes=5, radial_nodes=32, angular_nodes=28
    )
    withheld_values = S.pad_values(values, (5, 4), (6, 5))
    withheld_total, withheld_gradient, withheld_components = value_gradient(
        withheld_values, withheld_settings
    )
    withheld_relative = float(
        np.max(np.abs(withheld_gradient)) / max(1.0, abs(withheld_total))
    )
    quadrature_settings = dict(settings, radial_nodes=36, angular_nodes=32)
    quadrature_total, quadrature_gradient, quadrature_components = value_gradient(
        values, quadrature_settings
    )
    quadrature_change = abs(quadrature_total - total) / max(
        1.0, abs(total), abs(quadrature_total)
    )
    quadrature_gradient_relative = float(
        np.max(np.abs(quadrature_gradient)) / max(1.0, abs(quadrature_total))
    )

    mode_tensor = mode.reshape(3, 5, 4)
    mode_structure = {
        "q_fraction": float(np.sum(mode_tensor[0] ** 2)),
        "tangent_fraction": float(np.sum(mode_tensor[1] ** 2)),
        "split_fraction": float(np.sum(mode_tensor[2] ** 2)),
        "highest_radial_fraction": float(np.sum(mode_tensor[:, -1, :] ** 2)),
        "highest_angular_fraction": float(np.sum(mode_tensor[:, :, -1] ** 2)),
    }
    output = HERE / "coefficients-order5x4.npz"
    np.savez_compressed(
        output,
        coefficients=values.reshape(3, 5, 4),
        minimum_mode=mode_tensor,
    )
    payload = {
        "campaign": "P240",
        "attempt": "0039",
        "candidate": "D_fixed_j_two_clock_spectral_cartan_one_body",
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "primary": {
            "success": bool(primary.success),
            "status": int(primary.status),
            "message": str(primary.message),
            "function_evaluations": int(primary.nfev),
            "jacobian_evaluations": int(primary.njev),
        },
        "correction": None
        if correction is None
        else {
            "success": bool(correction.success),
            "status": int(correction.status),
            "message": str(correction.message),
            "function_evaluations": int(correction.nfev),
            "jacobian_evaluations": int(correction.njev),
        },
        "exact_oracle_evaluations": oracle.evaluations,
        "stationary": {
            "energy": total,
            "gradient_inf_relative": gradient_relative,
            "independent_directional_relative_max": float(max(directional)),
            "hessian_symmetry_relative_max": hessian_symmetry,
            "minimum_hessian_eigenvalue": float(eigenvalues[0]),
            "centered_energy_curvature": curvatures,
            "centered_curvature_relative_error": curvature_errors,
            "components": components,
            "mode_structure": mode_structure,
        },
        "withheld_order_6x5": {
            "energy": withheld_total,
            "gradient_inf_relative": withheld_relative,
            "components": withheld_components,
        },
        "higher_quadrature_36x32": {
            "energy": quadrature_total,
            "energy_relative_change": float(quadrature_change),
            "gradient_inf_relative": quadrature_gradient_relative,
            "components": quadrature_components,
        },
        "output_coefficients": str(output),
    }
    smallest_errors = [curvature_errors["0.001"], curvature_errors["0.0005"]]
    payload["one_body_gate_pass"] = bool(
        gradient_relative <= 1.0e-9
        and max(directional) <= 2.0e-8
        and hessian_symmetry <= 1.0e-10
        and eigenvalues[0] >= -1.0e-8
        and max(smallest_errors) <= 2.0e-4
        and withheld_relative <= 1.0e-6
        and quadrature_change <= 1.0e-6
        and quadrature_gradient_relative <= 2.0e-7
    )
    print("P240_ORDER5_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["one_body_gate_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
