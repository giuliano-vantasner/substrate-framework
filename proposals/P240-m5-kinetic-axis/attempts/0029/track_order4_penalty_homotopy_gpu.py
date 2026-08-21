"""Track the P240 smooth branch into order 4 with a removable mode penalty."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import least_squares
import torch


ATTEMPTS = Path(__file__).resolve().parents[1]
SOURCE = ATTEMPTS / "0026" / "correct_galerkin_exact_hessian_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0026_for_homotopy", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
C = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = C
SPEC.loader.exec_module(C)
G = C.G
M = C.M


class PenalizedOracle:
    def __init__(self, function_args: tuple, mask: np.ndarray, penalty: float):
        self.function_args = function_args
        self.mask = torch.tensor(mask, dtype=torch.float64, device=M.DEVICE)
        self.penalty = penalty
        self.cached_values: np.ndarray | None = None
        self.cached_energy: float | None = None
        self.cached_gradient: np.ndarray | None = None
        self.cached_hessian: np.ndarray | None = None
        self.evaluations = 0

    def evaluate(self, values: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
        values = np.asarray(values, dtype=np.float64)
        if self.cached_values is not None and np.array_equal(values, self.cached_values):
            return self.cached_energy, self.cached_gradient, self.cached_hessian
        variable = torch.tensor(
            values, dtype=torch.float64, device=M.DEVICE, requires_grad=True
        )
        physical_energy = C.torch_energy(variable, *self.function_args)
        penalty_energy = self.penalty * torch.sum(self.mask * variable**2) / 2
        total = physical_energy + penalty_energy
        gradient = torch.autograd.grad(total, variable, create_graph=True)[0]
        rows = [
            torch.autograd.grad(gradient[index], variable, retain_graph=True)[0]
            for index in range(values.size)
        ]
        hessian = torch.stack(rows)
        torch.cuda.synchronize()
        self.cached_values = values.copy()
        self.cached_energy = float(total.detach())
        self.cached_gradient = gradient.detach().cpu().numpy()
        self.cached_hessian = hessian.detach().cpu().numpy()
        self.evaluations += 1
        print(
            json.dumps(
                {
                    "stage": "penalty_homotopy",
                    "mu": self.penalty,
                    "evaluation": self.evaluations,
                    "modified_energy": self.cached_energy,
                    "gradient_inf_relative": float(
                        np.max(np.abs(self.cached_gradient))
                        / max(1.0, abs(self.cached_energy))
                    ),
                }
            ),
            flush=True,
        )
        return self.cached_energy, self.cached_gradient, self.cached_hessian


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
        ATTEMPTS / "0027" / "coefficients-converged-order3-mesh12x24.npz"
    ) as state:
        old = np.asarray(state["coefficients"], dtype=np.float64)
    coefficients = np.zeros(
        (len(G.COMPONENTS), radial_order, axial_modes), dtype=np.float64
    )
    coefficients[:, : old.shape[1], : old.shape[2]] = old
    values = coefficients.ravel()
    mask_tensor = np.zeros_like(coefficients)
    mask_tensor[:, -1, :] = 1.0
    mask_tensor[:, :, -1] = 1.0
    mask = mask_tensor.ravel()
    function_args = (
        parameters,
        radial_order,
        axial_modes,
        seed,
        radial_basis,
        axial_bases,
        envelope,
    )
    stage_rows = []
    final_hessian = None
    completed = True
    for penalty in (10000.0, 1000.0, 100.0, 10.0, 1.0, 0.0):
        oracle = PenalizedOracle(function_args, mask, penalty)
        initial_energy, _, _ = oracle.evaluate(values)
        reference_scale = max(1.0, abs(initial_energy))

        def residual(current: np.ndarray) -> np.ndarray:
            return oracle.evaluate(current)[1] / reference_scale

        def jacobian(current: np.ndarray) -> np.ndarray:
            return oracle.evaluate(current)[2] / reference_scale

        solved = least_squares(
            residual,
            values,
            jac=jacobian,
            method="lm",
            ftol=1.0e-14,
            xtol=1.0e-14,
            gtol=1.0e-14,
            max_nfev=100,
        )
        values = np.asarray(solved.x, dtype=np.float64)
        modified_energy, gradient, hessian = oracle.evaluate(values)
        normalized_gradient = float(
            np.max(np.abs(gradient)) / max(1.0, abs(modified_energy))
        )
        stage_pass = bool(solved.success and normalized_gradient <= 1.0e-8)
        stage_path = ATTEMPTS / "0029" / f"coefficients-mu-{penalty:g}.npz"
        np.savez_compressed(
            stage_path,
            coefficients=values.reshape(
                len(G.COMPONENTS), radial_order, axial_modes
            ),
            penalty=np.array(penalty),
        )
        stage_rows.append(
            {
                "penalty": penalty,
                "success": bool(solved.success),
                "message": str(solved.message),
                "function_evaluations": int(solved.nfev),
                "jacobian_evaluations": int(solved.njev),
                "exact_hessian_evaluations": oracle.evaluations,
                "modified_energy": modified_energy,
                "normalized_modified_gradient_inf": normalized_gradient,
                "new_mode_coefficient_norm": float(np.linalg.norm(mask * values)),
                "stage_gate_pass": stage_pass,
                "artifact": str(stage_path),
            }
        )
        if not stage_pass:
            completed = False
            break
        if penalty == 0.0:
            final_hessian = hessian

    payload = {
        "campaign": "P240",
        "attempt": "0029",
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "stages": stage_rows,
        "zero_penalty_reached": bool(completed and stage_rows[-1]["penalty"] == 0.0),
        "endpoint": None,
    }
    if payload["zero_penalty_reached"]:
        physical_energy, physical_gradient = G.energy_and_coefficient_gradient(
            values, *function_args
        )
        directions = G.deterministic_directions(values.size)
        step = 2.0e-5
        directional = []
        for direction in directions:
            plus = G.energy_value(values + step * direction, *function_args)
            minus = G.energy_value(values - step * direction, *function_args)
            directional.append(
                abs((plus - minus) / (2 * step)) / max(1.0, abs(physical_energy))
            )
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
            np.max(np.abs(full_gradient)) / max(1.0, abs(physical_energy))
        )
        symmetry = float(
            np.max(np.abs(final_hessian - final_hessian.T))
            / max(1.0, np.max(np.abs(final_hessian)))
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
        payload["endpoint"] = {
            "physical_energy": physical_energy,
            "normalized_physical_gradient_inf": float(
                np.max(np.abs(physical_gradient))
                / max(1.0, abs(physical_energy))
            ),
            "independent_directional_relative_max": float(max(directional)),
            "hessian_symmetry_relative_max": symmetry,
            "minimum_restricted_hessian_eigenvalue": float(
                np.linalg.eigvalsh((final_hessian + final_hessian.T) / 2)[0]
            ),
            "full_pointwise_grid_residual_inf_relative": full_residual,
            "maximum_nontrivial_high_half_DCT_power_fraction": maximum_power,
            "observables": {
                name: float(value.detach()) for name, value in observables.items()
            },
        }
        endpoint = payload["endpoint"]
        payload["endpoint_gate_pass"] = bool(
            endpoint["normalized_physical_gradient_inf"] <= 1.0e-8
            and endpoint["independent_directional_relative_max"] <= 2.0e-8
            and endpoint["hessian_symmetry_relative_max"] <= 1.0e-10
            and endpoint["maximum_nontrivial_high_half_DCT_power_fraction"] <= 0.10
            and endpoint["full_pointwise_grid_residual_inf_relative"]
            < 0.03082054476231251
        )
    else:
        payload["endpoint_gate_pass"] = False
    print("P240_ORDER4_HOMOTOPY_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["endpoint_gate_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
