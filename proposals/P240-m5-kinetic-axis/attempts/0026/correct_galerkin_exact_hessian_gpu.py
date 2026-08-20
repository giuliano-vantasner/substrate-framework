"""Exact-Hessian correction of the P240 smooth Galerkin stationary equations."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.fft import dctn
from scipy.optimize import least_squares
import torch


ATTEMPTS = Path(__file__).resolve().parents[1]
SOURCE = ATTEMPTS / "0025" / "solve_smooth_galerkin_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0025_galerkin", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
G = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = G
SPEC.loader.exec_module(G)
M = G.M


def torch_energy(
    values: torch.Tensor,
    parameters: M.Parameters,
    radial_order: int,
    axial_modes: int,
    seed: torch.Tensor,
    radial_basis: torch.Tensor,
    axial_bases: dict[int, torch.Tensor],
    envelope: torch.Tensor,
) -> torch.Tensor:
    coefficients = G.decode_coefficients(values, radial_order, axial_modes)
    interior = G.modal_interior(
        coefficients, seed, radial_basis, axial_bases, envelope
    )
    return M.observables(M.assemble(interior, seed), parameters)["total"]


class ExactOracle:
    def __init__(self, function_args: tuple):
        self.function_args = function_args
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
        energy = torch_energy(variable, *self.function_args)
        gradient = torch.autograd.grad(energy, variable, create_graph=True)[0]
        rows = []
        for index in range(values.size):
            rows.append(
                torch.autograd.grad(
                    gradient[index], variable, retain_graph=True
                )[0]
            )
        hessian = torch.stack(rows)
        torch.cuda.synchronize()
        self.cached_values = values.copy()
        self.cached_energy = float(energy.detach())
        self.cached_gradient = gradient.detach().cpu().numpy()
        self.cached_hessian = hessian.detach().cpu().numpy()
        self.evaluations += 1
        print(
            json.dumps(
                {
                    "stage": "exact_hessian",
                    "evaluation": self.evaluations,
                    "energy": self.cached_energy,
                    "gradient_inf_relative": float(
                        np.max(np.abs(self.cached_gradient))
                        / max(1.0, abs(self.cached_energy))
                    ),
                }
            ),
            flush=True,
        )
        return self.cached_energy, self.cached_gradient, self.cached_hessian


def high_power(field: torch.Tensor, parameters: M.Parameters) -> dict:
    physical = (*M.physical_components(field, parameters), field[..., 6])
    names = (
        "director",
        "tangent",
        "azimuthal",
        "angle_residual",
        "boost_rho",
        "boost_z",
        "scalar",
    )
    rows = {}
    for name, value in zip(names, physical):
        array = value.detach().cpu().numpy()
        centered = array - np.mean(array)
        coefficients = dctn(centered, type=2, norm="ortho")
        i, j = np.meshgrid(
            np.arange(array.shape[0]), np.arange(array.shape[1]), indexing="ij"
        )
        mask = (i >= array.shape[0] // 2) | (j >= array.shape[1] // 2)
        total = max(float(np.sum(coefficients**2)), np.finfo(np.float64).tiny)
        rows[name] = float(np.sum(coefficients[mask] ** 2) / total)
    return rows


def main() -> int:
    M.configure_device("cuda")
    parameters = M.Parameters(
        spacing=1 / 3,
        rho_cells=12,
        z_cells=24,
        projector_stiffness=2.0,
    )
    radial_order = 3
    axial_modes = 3
    seed = G.P.T.ORIGINAL_INITIAL_FIELD(parameters, 1.0)
    radial_basis, axial_bases, envelope = G.basis_data(
        parameters, radial_order, axial_modes
    )
    with np.load(
        ATTEMPTS / "0025" / "coefficients-order3-mesh12x24.npz"
    ) as state:
        initial_coefficients = np.asarray(state["coefficients"], dtype=np.float64)
    initial = initial_coefficients.ravel()
    function_args = (
        parameters,
        radial_order,
        axial_modes,
        seed,
        radial_basis,
        axial_bases,
        envelope,
    )
    oracle = ExactOracle(function_args)
    initial_energy, initial_gradient, initial_hessian = oracle.evaluate(initial)
    reference_scale = max(1.0, abs(initial_energy))

    def residual(values: np.ndarray) -> np.ndarray:
        return oracle.evaluate(values)[1] / reference_scale

    def jacobian(values: np.ndarray) -> np.ndarray:
        return oracle.evaluate(values)[2] / reference_scale

    initial_symmetry = float(
        np.max(np.abs(initial_hessian - initial_hessian.T))
        / max(1.0, np.max(np.abs(initial_hessian)))
    )
    direction = G.deterministic_directions(initial.size)[0]
    step_hessian = 1.0e-5
    plus_gradient = G.energy_and_coefficient_gradient(
        initial + step_hessian * direction, *function_args
    )[1]
    minus_gradient = G.energy_and_coefficient_gradient(
        initial - step_hessian * direction, *function_args
    )[1]
    finite_difference_hvp = (plus_gradient - minus_gradient) / (2 * step_hessian)
    ad_hvp = initial_hessian @ direction
    hvp_error = float(
        np.linalg.norm(finite_difference_hvp - ad_hvp)
        / max(1.0, np.linalg.norm(finite_difference_hvp), np.linalg.norm(ad_hvp))
    )
    solved = least_squares(
        residual,
        initial,
        jac=jacobian,
        method="lm",
        ftol=1.0e-13,
        xtol=1.0e-13,
        gtol=1.0e-13,
        max_nfev=160,
    )
    values = np.asarray(solved.x, dtype=np.float64)
    energy, gradient, hessian = oracle.evaluate(values)
    normalized_gradient = float(np.max(np.abs(gradient)) / max(1.0, abs(energy)))
    symmetry = float(
        np.max(np.abs(hessian - hessian.T))
        / max(1.0, np.max(np.abs(hessian)))
    )
    directions = G.deterministic_directions(values.size)
    step = 2.0e-5
    directional = []
    for test_direction in directions:
        plus = G.energy_value(values + step * test_direction, *function_args)
        minus = G.energy_value(values - step * test_direction, *function_args)
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
    power = high_power(field, parameters)
    output = ATTEMPTS / "0026" / "coefficients-corrected-order3-mesh12x24.npz"
    np.savez_compressed(
        output,
        coefficients=values.reshape(len(G.COMPONENTS), radial_order, axial_modes),
    )
    payload = {
        "campaign": "P240",
        "attempt": "0026",
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "initial": {
            "energy": initial_energy,
            "normalized_gradient_inf": float(
                np.max(np.abs(initial_gradient)) / max(1.0, abs(initial_energy))
            ),
            "hessian_symmetry_relative_max": initial_symmetry,
            "hessian_vector_fd_relative_error": hvp_error,
        },
        "solver": {
            "success": bool(solved.success),
            "message": str(solved.message),
            "function_evaluations": int(solved.nfev),
            "jacobian_evaluations": int(solved.njev),
            "exact_hessian_evaluations": oracle.evaluations,
            "cost": float(solved.cost),
            "optimality": float(solved.optimality),
        },
        "stationary": {
            "energy": energy,
            "normalized_coefficient_gradient_inf": normalized_gradient,
            "independent_directional_relative_max": float(max(directional)),
            "hessian_symmetry_relative_max": symmetry,
            "observables": {name: float(value.detach()) for name, value in observables.items()},
            "physical_high_half_DCT_power_fraction": power,
            "maximum_nontrivial_high_half_DCT_power_fraction": float(
                max(power[name] for name in ("director", "tangent", "azimuthal", "angle_residual", "scalar"))
            ),
        },
        "output_coefficients": str(output),
    }
    payload["stationary_gate_pass"] = bool(
        solved.success
        and normalized_gradient <= 1.0e-8
        and max(directional) <= 2.0e-8
        and symmetry <= 1.0e-10
        and hvp_error <= 1.0e-5
        and payload["stationary"]["maximum_nontrivial_high_half_DCT_power_fraction"] <= 0.10
    )
    print("P240_EXACT_HESSIAN_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["stationary_gate_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
