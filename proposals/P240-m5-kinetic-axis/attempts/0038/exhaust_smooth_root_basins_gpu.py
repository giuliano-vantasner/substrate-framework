"""Enumerate and continue all smooth roots of the unchanged P240 action."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import root


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[0] / "0036" / "solve_spectral_cartan_hedgehog_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0036_exhaust", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
S = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = S
SPEC.loader.exec_module(S)


def settings(radial_order, angular_modes, radial_nodes=24, angular_nodes=20):
    return {
        "radial_order": radial_order,
        "angular_modes": angular_modes,
        "radial_nodes": radial_nodes,
        "angular_nodes": angular_nodes,
        "radius": 6.0,
    }


def solve(values, radial_order, angular_modes):
    stage_settings = settings(radial_order, angular_modes)
    oracle = S.ExactOracle(stage_settings)
    initial_energy = oracle.evaluate(values)[0]
    scale = max(1.0, abs(initial_energy))

    def residual(current):
        return oracle.evaluate(current)[1] / scale

    def jacobian(current):
        return oracle.evaluate(current)[2] / scale

    primary = root(
        residual,
        values,
        jac=jacobian,
        method="hybr",
        options={"xtol": 1.0e-11, "maxfev": 220},
    )
    current = np.asarray(primary.x, dtype=np.float64)
    energy_value, gradient, hessian, components = oracle.evaluate(current)
    relative = float(np.max(np.abs(gradient)) / max(1.0, abs(energy_value)))
    correction = None
    if relative > 1.0e-9:
        correction = root(
            residual,
            current,
            jac=jacobian,
            method="lm",
            options={"ftol": 1.0e-13, "xtol": 1.0e-13, "gtol": 1.0e-13, "maxiter": 500},
        )
        current = np.asarray(correction.x, dtype=np.float64)
        energy_value, gradient, hessian, components = oracle.evaluate(current)
        relative = float(np.max(np.abs(gradient)) / max(1.0, abs(energy_value)))
    eigenvalues, eigenvectors = np.linalg.eigh((hessian + hessian.T) / 2)
    row = {
        "radial_order": radial_order,
        "angular_modes": angular_modes,
        "coefficient_count": current.size,
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
        "root_pass": relative <= 1.0e-9,
        "energy": energy_value,
        "gradient_inf_relative": relative,
        "minimum_hessian_eigenvalue": float(eigenvalues[0]),
        "components": components,
    }
    return current, hessian, eigenvectors[:, 0], row


def equivalent(left, right):
    return np.linalg.norm(left - right) <= 1.0e-8 * max(
        1.0, np.linalg.norm(left), np.linalg.norm(right)
    )


def main() -> int:
    seed_rows = []
    branches = []
    for split_seed in (0.125, 0.5, 2.0):
        initial = S.initial_values(1, 1)
        initial.reshape(3, 1, 1)[2, 0, 0] = split_seed
        values, hessian, mode, row = solve(initial, 1, 1)
        row["initial_split_amplitude"] = split_seed
        row["duplicate_of"] = None
        if row["root_pass"]:
            for index, branch in enumerate(branches):
                if equivalent(values, branch["values"]):
                    row["duplicate_of"] = index
                    break
            else:
                branches.append(
                    {"values": values, "shape": (1, 1), "stages": [row]}
                )
        seed_rows.append(row)

    for branch_index, branch in enumerate(branches):
        for target_shape in ((2, 1), (2, 2), (3, 2), (4, 3)):
            padded = S.pad_values(branch["values"], branch["shape"], target_shape)
            values, hessian, mode, row = solve(padded, *target_shape)
            branch["values"] = values
            branch["shape"] = target_shape
            branch["hessian"] = hessian
            branch["mode"] = mode
            branch["stages"].append(row)
            if not row["root_pass"]:
                break

    final_rows = []
    any_pass = False
    for branch_index, branch in enumerate(branches):
        row = {
            "branch": branch_index,
            "stages": branch["stages"],
            "reached_full_order": branch["shape"] == (4, 3),
        }
        if branch["shape"] != (4, 3) or not branch["stages"][-1]["root_pass"]:
            row["final_gate_pass"] = False
            final_rows.append(row)
            continue
        values = branch["values"]
        stage_settings = settings(4, 3)
        oracle = S.ExactOracle(stage_settings)
        total, gradient, hessian, components = oracle.evaluate(values)
        symmetry = float(np.max(np.abs(hessian - hessian.T)) / max(1.0, np.max(np.abs(hessian))))
        eigenvalues, eigenvectors = np.linalg.eigh((hessian + hessian.T) / 2)
        mode = eigenvectors[:, 0]
        directional = []
        for direction in S.deterministic_directions(values.size):
            step = 2.0e-5
            plus = S.energy_value(values + step * direction, stage_settings)
            minus = S.energy_value(values - step * direction, stage_settings)
            directional.append(abs((plus - minus) / (2 * step)) / max(1.0, abs(total)))
        curvatures = {}
        curvature_errors = {}
        for step in (0.01, 0.005, 0.0025, 0.00125):
            curvature = (
                S.energy_value(values + step * mode, stage_settings)
                - 2 * total
                + S.energy_value(values - step * mode, stage_settings)
            ) / step**2
            curvatures[str(step)] = float(curvature)
            curvature_errors[str(step)] = float(
                abs(curvature - eigenvalues[0])
                / max(1.0, abs(curvature), abs(eigenvalues[0]))
            )
        withheld_settings = settings(5, 4)
        withheld_values = S.pad_values(values, (4, 3), (5, 4))
        withheld = S.ExactOracle(withheld_settings).evaluate(withheld_values)
        withheld_relative = float(np.max(np.abs(withheld[1])) / max(1.0, abs(withheld[0])))
        quadrature_settings = settings(4, 3, 32, 28)
        quadrature = S.ExactOracle(quadrature_settings).evaluate(values)
        quadrature_change = abs(quadrature[0] - total) / max(1.0, abs(total), abs(quadrature[0]))
        quadrature_gradient = float(np.max(np.abs(quadrature[1])) / max(1.0, abs(quadrature[0])))
        final = {
            "energy": total,
            "gradient_inf_relative": float(np.max(np.abs(gradient)) / max(1.0, abs(total))),
            "independent_directional_relative_max": float(max(directional)),
            "hessian_symmetry_relative_max": symmetry,
            "minimum_hessian_eigenvalue": float(eigenvalues[0]),
            "centered_energy_curvature": curvatures,
            "centered_curvature_relative_error": curvature_errors,
            "withheld_order_5x4_gradient_inf_relative": withheld_relative,
            "higher_quadrature_energy_relative_change": float(quadrature_change),
            "higher_quadrature_gradient_inf_relative": quadrature_gradient,
            "components": components,
        }
        row["final"] = final
        row["final_gate_pass"] = bool(
            final["gradient_inf_relative"] <= 1.0e-9
            and final["independent_directional_relative_max"] <= 2.0e-8
            and symmetry <= 1.0e-10
            and eigenvalues[0] >= -1.0e-8
            and max(curvature_errors.values()) <= 1.0e-4
            and withheld_relative <= 1.0e-6
            and quadrature_change <= 1.0e-6
            and quadrature_gradient <= 2.0e-7
        )
        any_pass = any_pass or row["final_gate_pass"]
        np.savez_compressed(
            HERE / f"coefficients-branch-{branch_index}-order4x3.npz",
            coefficients=values.reshape(3, 4, 3),
            minimum_mode=mode.reshape(3, 4, 3),
        )
        final_rows.append(row)

    payload = {
        "campaign": "P240",
        "attempt": "0038",
        "candidate": "D_fixed_j_two_clock_spectral_cartan_one_body",
        "environment": {
            "torch": S.torch.__version__,
            "cuda_runtime": S.torch.version.cuda,
            "device": S.torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "seed_roots": seed_rows,
        "distinct_root_count": len(branches),
        "branches": final_rows,
        "any_final_gate_pass": any_pass,
    }
    print("P240_EXHAUST_ROOTS_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if any_pass else 2


if __name__ == "__main__":
    raise SystemExit(main())
