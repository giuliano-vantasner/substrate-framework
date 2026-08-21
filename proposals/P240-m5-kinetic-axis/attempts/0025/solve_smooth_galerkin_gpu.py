"""Direct smooth Galerkin Euler-Lagrange solve for the P240 one-body branch."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.fft import dctn
from scipy.optimize import root
import torch


ATTEMPTS = Path(__file__).resolve().parents[1]
SOURCE = ATTEMPTS / "0023" / "audit_projection_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0023_for_galerkin", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
P = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = P
SPEC.loader.exec_module(P)
M = P.M


COMPONENTS = (0, 1, 2, 3, 6)
COMPONENT_NAMES = ("anisotropy", "common", "split", "angle_control", "scalar")
EVEN_COMPONENTS = {0, 1, 2, 6}


def chebyshev_values(coordinate: torch.Tensor, degrees: tuple[int, ...]) -> torch.Tensor:
    angle = torch.acos(torch.clamp(coordinate, -1.0, 1.0))
    return torch.stack(tuple(torch.cos(degree * angle) for degree in degrees), dim=-1)


def basis_data(
    parameters: M.Parameters, radial_order: int, axial_modes: int
) -> tuple[torch.Tensor, dict[int, torch.Tensor], torch.Tensor]:
    rho, z = M.coordinates(parameters)
    rho = rho[:-1, 1:-1]
    z = z[:-1, 1:-1]
    radial_extent = parameters.rho_cells * parameters.spacing
    axial_half_extent = parameters.z_cells * parameters.spacing / 2
    radial_coordinate = 2 * (rho / radial_extent) ** 2 - 1
    axial_coordinate = z / axial_half_extent
    radial_basis = chebyshev_values(
        radial_coordinate[:, 0], tuple(range(radial_order))
    )
    axial_bases = {
        component: chebyshev_values(
            axial_coordinate[0],
            tuple(
                2 * index + (0 if component in EVEN_COMPONENTS else 1)
                for index in range(axial_modes)
            ),
        )
        for component in COMPONENTS
    }
    envelope = (1 - (rho / radial_extent) ** 2) * (
        1 - (z / axial_half_extent) ** 2
    )
    return radial_basis, axial_bases, envelope


def decode_coefficients(
    flat: torch.Tensor, radial_order: int, axial_modes: int
) -> torch.Tensor:
    return flat.reshape(len(COMPONENTS), radial_order, axial_modes)


def modal_interior(
    coefficients: torch.Tensor,
    seed: torch.Tensor,
    radial_basis: torch.Tensor,
    axial_bases: dict[int, torch.Tensor],
    envelope: torch.Tensor,
) -> torch.Tensor:
    interior = seed[:-1, 1:-1].clone()
    for slot, component in enumerate(COMPONENTS):
        delta = torch.einsum(
            "ra,ab,zb->rz",
            radial_basis,
            coefficients[slot],
            axial_bases[component],
        )
        interior[..., component] = interior[..., component] + envelope * delta
    interior[..., 4] = 0.0
    interior[..., 5] = 0.0
    return interior


def energy_and_coefficient_gradient(
    values: np.ndarray,
    parameters: M.Parameters,
    radial_order: int,
    axial_modes: int,
    seed: torch.Tensor,
    radial_basis: torch.Tensor,
    axial_bases: dict[int, torch.Tensor],
    envelope: torch.Tensor,
) -> tuple[float, np.ndarray]:
    variable = torch.tensor(
        values, dtype=torch.float64, device=M.DEVICE, requires_grad=True
    )
    coefficients = decode_coefficients(variable, radial_order, axial_modes)
    interior = modal_interior(
        coefficients, seed, radial_basis, axial_bases, envelope
    )
    total = M.observables(M.assemble(interior, seed), parameters)["total"]
    gradient = torch.autograd.grad(total, variable)[0]
    torch.cuda.synchronize()
    return float(total.detach()), gradient.detach().cpu().numpy()


def energy_value(*args) -> float:
    return energy_and_coefficient_gradient(*args)[0]


def deterministic_directions(size: int) -> list[np.ndarray]:
    index = np.arange(size, dtype=np.float64) + 1
    rows = []
    for frequency in (0.41, 0.73, 1.07):
        value = np.sin(frequency * index) + 0.5 * np.cos((frequency + 0.19) * index)
        rows.append(value / np.linalg.norm(value))
    return rows


def pad_coefficients(
    path: Path | None, radial_order: int, axial_modes: int
) -> np.ndarray:
    target = np.zeros((len(COMPONENTS), radial_order, axial_modes), dtype=np.float64)
    if path is None:
        return target.ravel()
    with np.load(path) as state:
        old = np.asarray(state["coefficients"], dtype=np.float64)
    radial_copy = min(radial_order, old.shape[1])
    axial_copy = min(axial_modes, old.shape[2])
    target[:, :radial_copy, :axial_copy] = old[:, :radial_copy, :axial_copy]
    return target.ravel()


def physical_high_power(field: torch.Tensor, parameters: M.Parameters) -> dict:
    physical = M.physical_components(field, parameters)
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
    for name, values in zip(names, physical):
        array = values.detach().cpu().numpy()
        centered = array - np.mean(array)
        coefficients = dctn(centered, type=2, norm="ortho")
        radial_indices, axial_indices = np.meshgrid(
            np.arange(array.shape[0]), np.arange(array.shape[1]), indexing="ij"
        )
        high = (radial_indices >= array.shape[0] // 2) | (
            axial_indices >= array.shape[1] // 2
        )
        total = max(float(np.sum(coefficients**2)), np.finfo(np.float64).tiny)
        rows[name] = float(np.sum(coefficients[high] ** 2) / total)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid-id", required=True)
    parser.add_argument("--spacing", type=float, required=True)
    parser.add_argument("--rho-cells", type=int, required=True)
    parser.add_argument("--z-cells", type=int, required=True)
    parser.add_argument("--radial-order", type=int, required=True)
    parser.add_argument("--axial-modes", type=int, required=True)
    parser.add_argument("--initial-coefficients", type=Path)
    parser.add_argument("--output-coefficients", type=Path, required=True)
    parser.add_argument("--root-iterations", type=int, default=600)
    args = parser.parse_args()
    M.configure_device("cuda")
    parameters = M.Parameters(
        spacing=args.spacing,
        rho_cells=args.rho_cells,
        z_cells=args.z_cells,
        projector_stiffness=2.0,
    )
    seed = P.T.ORIGINAL_INITIAL_FIELD(parameters, 1.0)
    radial_basis, axial_bases, envelope = basis_data(
        parameters, args.radial_order, args.axial_modes
    )
    initial = pad_coefficients(
        args.initial_coefficients, args.radial_order, args.axial_modes
    )
    function_args = (
        parameters,
        args.radial_order,
        args.axial_modes,
        seed,
        radial_basis,
        axial_bases,
        envelope,
    )
    initial_energy, initial_gradient = energy_and_coefficient_gradient(
        initial, *function_args
    )
    reference_scale = max(1.0, abs(initial_energy))
    evaluations = 0

    def residual(values: np.ndarray) -> np.ndarray:
        nonlocal evaluations
        evaluations += 1
        if evaluations % 100 == 0:
            energy, gradient = energy_and_coefficient_gradient(values, *function_args)
            print(
                json.dumps(
                    {
                        "stage": "galerkin_root",
                        "evaluation": evaluations,
                        "energy": energy,
                        "gradient_inf_relative": float(
                            np.max(np.abs(gradient)) / max(1.0, abs(energy))
                        ),
                    }
                ),
                flush=True,
            )
            return gradient / reference_scale
        return energy_and_coefficient_gradient(values, *function_args)[1] / reference_scale

    solved = root(
        residual,
        initial,
        method="krylov",
        options={"fatol": 1.0e-9, "maxiter": args.root_iterations, "line_search": "armijo"},
    )
    values = np.asarray(solved.x, dtype=np.float64)
    energy, gradient = energy_and_coefficient_gradient(values, *function_args)
    normalized_gradient = float(np.max(np.abs(gradient)) / max(1.0, abs(energy)))
    directions = deterministic_directions(values.size)
    step = 2.0e-5
    directional = []
    for direction in directions:
        plus = energy_value(values + step * direction, *function_args)
        minus = energy_value(values - step * direction, *function_args)
        directional.append(abs((plus - minus) / (2 * step)) / max(1.0, abs(energy)))
    coefficients = decode_coefficients(
        torch.tensor(values, dtype=torch.float64, device=M.DEVICE),
        args.radial_order,
        args.axial_modes,
    )
    interior = modal_interior(
        coefficients, seed, radial_basis, axial_bases, envelope
    )
    field = M.assemble(interior, seed)
    observables = M.observables(field, parameters)
    full_values = interior.detach().cpu().numpy().ravel()
    full_shape = tuple(interior.shape)
    _, full_gradient = M._energy_and_gradient(
        full_values, full_shape, seed, parameters
    )
    full_residual = float(
        np.max(np.abs(full_gradient)) / max(1.0, abs(energy))
    )
    boundary_values = field.detach().cpu().numpy()
    seed_values = seed.detach().cpu().numpy()
    boundary_residual = float(
        max(
            np.max(np.abs(boundary_values[-1] - seed_values[-1])),
            np.max(np.abs(boundary_values[:, 0] - seed_values[:, 0])),
            np.max(np.abs(boundary_values[:, -1] - seed_values[:, -1])),
        )
    )
    args.output_coefficients.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output_coefficients,
        coefficients=values.reshape(
            len(COMPONENTS), args.radial_order, args.axial_modes
        ),
        spacing=np.array(args.spacing),
        rho_cells=np.array(args.rho_cells),
        z_cells=np.array(args.z_cells),
    )
    high_power = physical_high_power(field, parameters)
    payload = {
        "campaign": "P240",
        "attempt": "0025",
        "grid_id": args.grid_id,
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "representation": {
            "radial_order": args.radial_order,
            "axial_modes": args.axial_modes,
            "coefficient_count": values.size,
        },
        "initial": {
            "energy": initial_energy,
            "normalized_coefficient_gradient_inf": float(
                np.max(np.abs(initial_gradient)) / max(1.0, abs(initial_energy))
            ),
        },
        "root": {
            "success": bool(solved.success),
            "message": str(solved.message),
            "evaluations": evaluations,
            "normalized_coefficient_gradient_inf": normalized_gradient,
            "independent_directional_relative_max": float(max(directional)),
        },
        "full_grid_normalized_residual_inf": full_residual,
        "boundary_residual": boundary_residual,
        "observables": {name: float(value.detach()) for name, value in observables.items()},
        "physical_high_half_DCT_power_fraction": high_power,
        "upper_half_DCT_power_fraction_max_nonzero_background": float(
            max(high_power[name] for name in ("director", "tangent", "azimuthal", "angle_residual", "scalar"))
        ),
        "output_coefficients": str(args.output_coefficients),
        "stationary_gate_pass": bool(
            solved.success
            and normalized_gradient <= 1.0e-8
            and max(directional) <= 2.0e-8
            and boundary_residual == 0.0
            and float(observables["inertia"].detach()) > 0.0
            and np.isfinite(float(observables["frequency"].detach()))
            and float(observables["frequency"].detach()) > 0.0
        ),
    }
    print("P240_GALERKIN_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if payload["stationary_gate_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
