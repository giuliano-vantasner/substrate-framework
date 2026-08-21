"""Exact-Jacobian Newton solve of the unmodified P240 order-4 action."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import root
import torch


ATTEMPTS = Path(__file__).resolve().parents[1]
SOURCE = ATTEMPTS / "0026" / "correct_galerkin_exact_hessian_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0026_for_newton", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
C = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = C
SPEC.loader.exec_module(C)
G = C.G
M = C.M


def main() -> int:
    M.configure_device("cuda")
    parameters = M.Parameters(
        spacing=1 / 3,
        rho_cells=12,
        z_cells=24,
        projector_stiffness=2.0,
    )
    radial_order = 4
    axial_modes = 4
    seed = G.P.T.ORIGINAL_INITIAL_FIELD(parameters, 1.0)
    radial_basis, axial_bases, envelope = G.basis_data(
        parameters, radial_order, axial_modes
    )
    with np.load(
        ATTEMPTS / "0028" / "coefficients-converged-order4-mesh12x24.npz"
    ) as state:
        initial = np.asarray(state["coefficients"], dtype=np.float64).ravel()
    function_args = (
        parameters,
        radial_order,
        axial_modes,
        seed,
        radial_basis,
        axial_bases,
        envelope,
    )
    oracle = C.ExactOracle(function_args)
    initial_energy, initial_gradient, _ = oracle.evaluate(initial)
    reference_scale = max(1.0, abs(initial_energy))

    def residual(values: np.ndarray) -> np.ndarray:
        return oracle.evaluate(values)[1] / reference_scale

    def jacobian(values: np.ndarray) -> np.ndarray:
        return oracle.evaluate(values)[2] / reference_scale

    solved = root(
        residual,
        initial,
        jac=jacobian,
        method="hybr",
        options={"xtol": 1.0e-11, "maxfev": 200},
    )
    values = np.asarray(solved.x, dtype=np.float64)
    energy, gradient, hessian = oracle.evaluate(values)
    normalized_gradient = float(np.max(np.abs(gradient)) / max(1.0, abs(energy)))
    directions = G.deterministic_directions(values.size)
    step = 2.0e-5
    directional = []
    for direction in directions:
        plus = G.energy_value(values + step * direction, *function_args)
        minus = G.energy_value(values - step * direction, *function_args)
        directional.append(abs((plus - minus) / (2 * step)) / max(1.0, abs(energy)))
    coefficient_tensor = G.decode_coefficients(
        torch.tensor(values, dtype=torch.float64, device=M.DEVICE),
        radial_order,
        axial_modes,
    )
    interior = G.modal_interior(
        coefficient_tensor, seed, radial_basis, axial_bases, envelope
    )
    field = M.assemble(interior, seed)
    observables = M.observables(field, parameters)
    _, full_gradient = M._energy_and_gradient(
        interior.detach().cpu().numpy().ravel(),
        tuple(interior.shape),
        seed,
        parameters,
    )
    full_residual = float(
        np.max(np.abs(full_gradient)) / max(1.0, abs(energy))
    )
    symmetry = float(
        np.max(np.abs(hessian - hessian.T))
        / max(1.0, np.max(np.abs(hessian)))
    )
    power = C.high_power(field, parameters)
    maximum_power = float(
        max(
            power[name]
            for name in (
                "director",
                "tangent",
                "azimuthal",
                "angle_residual",
                "scalar",
            )
        )
    )
    output = ATTEMPTS / "0031" / "coefficients-order4-exact-newton.npz"
    np.savez_compressed(
        output,
        coefficients=values.reshape(len(G.COMPONENTS), radial_order, axial_modes),
    )
    payload = {
        "campaign": "P240",
        "attempt": "0031",
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "initial": {
            "energy": initial_energy,
            "normalized_coefficient_gradient_inf": float(
                np.max(np.abs(initial_gradient)) / max(1.0, abs(initial_energy))
            ),
        },
        "solver": {
            "success": bool(solved.success),
            "status": int(solved.status),
            "message": str(solved.message),
            "function_evaluations": int(solved.nfev),
            "jacobian_evaluations": int(solved.njev),
            "exact_hessian_evaluations": oracle.evaluations,
        },
        "stationary": {
            "energy": energy,
            "normalized_coefficient_gradient_inf": normalized_gradient,
            "independent_directional_relative_max": float(max(directional)),
            "hessian_symmetry_relative_max": symmetry,
            "full_pointwise_grid_residual_inf_relative": full_residual,
            "minimum_restricted_hessian_eigenvalue": float(
                np.linalg.eigvalsh((hessian + hessian.T) / 2)[0]
            ),
            "maximum_nontrivial_high_half_DCT_power_fraction": maximum_power,
            "observables": {name: float(value.detach()) for name, value in observables.items()},
        },
        "output_coefficients": str(output),
    }
    payload["stationary_gate_pass"] = bool(
        solved.success
        and normalized_gradient <= 1.0e-8
        and max(directional) <= 2.0e-8
        and symmetry <= 1.0e-10
        and maximum_power <= 0.10
        and full_residual < 0.03082054476231251
    )
    print("P240_ORDER4_NEWTON_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["stationary_gate_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
