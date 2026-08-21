"""Track one stationary branch across meshes, then map its exact-linear Hessian.

This is a numerical-method repair of P240 attempt 0021.  It reuses that
attempt's frozen action translation but never treats optimizer loss as a
scientific oracle and never computes a stability verdict at a failed root.
"""

from __future__ import annotations

import argparse
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.linalg import eigh
import torch


SOURCE = Path(__file__).resolve().parents[1] / "0021" / "solve_refined_fixed_j.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0021_frozen", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load frozen numerical translation {SOURCE}")
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)


def _cell_centres(cells: int, spacing: float, *, radial: bool) -> np.ndarray:
    if radial:
        return (np.arange(cells) + 0.5) * spacing
    return (np.arange(cells) - cells / 2 + 0.5) * spacing


def tracked_seed(
    parameters: M.Parameters,
    split_sign: float,
    state_path: Path | None,
) -> torch.Tensor:
    seed = ORIGINAL_INITIAL_FIELD(parameters, split_sign)
    if state_path is None:
        return seed
    with np.load(state_path) as state:
        old_field = np.asarray(state["field"], dtype=np.float64)
        old_spacing = float(state["spacing"])
        old_rho_cells = int(state["rho_cells"])
        old_z_cells = int(state["z_cells"])
    if old_field.shape != (old_rho_cells, old_z_cells, 7):
        raise ValueError("saved control field has inconsistent shape metadata")
    old_extents = (old_rho_cells * old_spacing, old_z_cells * old_spacing)
    new_extents = (
        parameters.rho_cells * parameters.spacing,
        parameters.z_cells * parameters.spacing,
    )
    if not np.allclose(old_extents, new_extents, rtol=0.0, atol=1.0e-12):
        raise ValueError(
            f"branch tracking requires fixed extents: {old_extents} != {new_extents}"
        )
    old_rho = _cell_centres(old_rho_cells, old_spacing, radial=True)
    old_z = _cell_centres(old_z_cells, old_spacing, radial=False)
    new_rho = _cell_centres(parameters.rho_cells, parameters.spacing, radial=True)
    new_z = _cell_centres(parameters.z_cells, parameters.spacing, radial=False)
    rho_grid, z_grid = np.meshgrid(new_rho[:-1], new_z[1:-1], indexing="ij")
    points = np.stack((rho_grid.ravel(), z_grid.ravel()), axis=-1)
    interpolator = RegularGridInterpolator(
        (old_rho, old_z),
        old_field,
        method="linear",
        bounds_error=False,
        fill_value=None,
    )
    interpolated = interpolator(points).reshape(
        parameters.rho_cells - 1, parameters.z_cells - 2, 7
    )
    seed[:-1, 1:-1] = torch.tensor(
        interpolated, dtype=torch.float64, device=M.DEVICE
    )
    if not torch.all(torch.isfinite(seed)):
        raise FloatingPointError("branch interpolation produced non-finite controls")
    return seed


def deterministic_directions(size: int) -> list[np.ndarray]:
    return M._deterministic_directions(size, count=3)


def dense_stiffness_map(
    values: np.ndarray,
    shape: tuple[int, ...],
    seed: torch.Tensor,
    parameters: M.Parameters,
    ladder: tuple[float, ...],
) -> dict:
    zero = replace(parameters, projector_stiffness=0.0)
    unit = replace(parameters, projector_stiffness=1.0)
    dimension = values.size
    hessian_zero = np.empty((dimension, dimension), dtype=np.float64)
    hessian_unit = np.empty_like(hessian_zero)
    basis = np.zeros(dimension, dtype=np.float64)
    for column in range(dimension):
        basis[column] = 1.0
        hessian_zero[:, column] = M._hessian_vector(
            values, basis, shape, seed, zero
        )
        hessian_unit[:, column] = M._hessian_vector(
            values, basis, shape, seed, unit
        )
        basis[column] = 0.0
        if column % 100 == 0:
            print(
                json.dumps(
                    {"stage": "dense_linear_map", "column": column, "columns": dimension}
                ),
                flush=True,
            )
    projector = hessian_unit - hessian_zero
    scale_zero = max(1.0, float(np.max(np.abs(hessian_zero))))
    scale_projector = max(1.0, float(np.max(np.abs(projector))))
    symmetry_zero = float(
        np.max(np.abs(hessian_zero - hessian_zero.T)) / scale_zero
    )
    symmetry_projector = float(
        np.max(np.abs(projector - projector.T)) / scale_projector
    )
    component_names = (
        "anisotropy",
        "common",
        "split",
        "angle_control",
        "boost_rho",
        "boost_z",
        "scalar",
    )
    rows = []
    for stiffness in ladder:
        current_parameters = replace(parameters, projector_stiffness=stiffness)
        current_hessian = hessian_zero + stiffness * projector
        eigenvalues, eigenvectors = eigh(
            current_hessian, subset_by_index=(0, 5), driver="evr"
        )
        energy, gradient = M._energy_and_gradient(
            values, shape, seed, current_parameters
        )
        mode = eigenvectors[:, 0]
        mode /= np.linalg.norm(mode)
        mode_shape = mode.reshape(shape)
        component_power = np.sum(mode_shape**2, axis=(0, 1))
        step = 0.00125
        centered_curvature = (
            M._energy_value(values + step * mode, shape, seed, current_parameters)
            - 2 * energy
            + M._energy_value(values - step * mode, shape, seed, current_parameters)
        ) / step**2
        eigen_residual = np.linalg.norm(
            current_hessian @ mode - eigenvalues[0] * mode
        ) / max(1.0, abs(float(eigenvalues[0])))
        rows.append(
            {
                "projector_stiffness": stiffness,
                "root_residual_inf_relative": float(
                    np.max(np.abs(gradient)) / max(1.0, abs(energy))
                ),
                "six_smallest_eigenvalues": [float(value) for value in eigenvalues],
                "minimum_eigen_residual_relative": float(eigen_residual),
                "minimum_mode_projector_rayleigh": float(mode @ projector @ mode),
                "minimum_mode_components": {
                    name: float(value)
                    for name, value in zip(component_names, component_power)
                },
                "centered_energy_curvature": float(centered_curvature),
                "centered_curvature_relative_error": float(
                    abs(centered_curvature - eigenvalues[0])
                    / max(1.0, abs(centered_curvature), abs(float(eigenvalues[0])))
                ),
                "passes_spectrum_gate": bool(eigenvalues[0] >= -1.0e-6),
            }
        )
    return {
        "dimension": dimension,
        "hessian_zero_symmetry_relative_max": symmetry_zero,
        "projector_hessian_symmetry_relative_max": symmetry_projector,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid-id", required=True)
    parser.add_argument("--spacing", type=float, required=True)
    parser.add_argument("--rho-cells", type=int, required=True)
    parser.add_argument("--z-cells", type=int, required=True)
    parser.add_argument("--initial-state", type=Path)
    parser.add_argument("--output-state", type=Path, required=True)
    parser.add_argument("--adam-steps", type=int)
    parser.add_argument("--lbfgsb-iterations", type=int, default=12000)
    parser.add_argument("--root-iterations", type=int, default=480)
    parser.add_argument("--map-stiffness", action="store_true")
    args = parser.parse_args()
    M.configure_device("cpu")
    adam_steps = args.adam_steps
    if adam_steps is None:
        adam_steps = 1800 if args.initial_state is None else 0
    parameters = M.Parameters(
        spacing=args.spacing,
        rho_cells=args.rho_cells,
        z_cells=args.z_cells,
        adam_steps=adam_steps,
        lbfgsb_iterations=args.lbfgsb_iterations,
        projector_stiffness=2.0,
    )
    captured: dict[str, object] = {}

    def initial_field(current: M.Parameters, split_sign: float) -> torch.Tensor:
        seed = tracked_seed(current, split_sign, args.initial_state)
        captured["seed"] = seed.clone()
        return seed

    def capturing_root(*root_args, **root_kwargs):
        solved = ORIGINAL_ROOT(*root_args, **root_kwargs)
        captured["values"] = np.asarray(solved.x, dtype=np.float64).copy()
        return solved

    def no_spectrum(operator, **_kwargs):
        return np.empty(0, dtype=np.float64), np.empty(
            (operator.shape[0], 0), dtype=np.float64
        )

    M.initial_field = initial_field
    M.root = capturing_root
    M.eigsh = no_spectrum
    branch = M.solve_branch(parameters, 1.0, args.root_iterations)
    stationary_pass = bool(
        branch["root_success"]
        and branch["euler_lagrange_residual_inf_relative"] <= 1.0e-8
        and branch["root_directional_derivative_relative_max"] <= 2.0e-8
        and branch["boundary_residual"] == 0.0
    )
    payload = {
        "campaign": "P240",
        "attempt": "0022",
        "grid_id": args.grid_id,
        "initial_state": str(args.initial_state) if args.initial_state else None,
        "parameters": {
            "spacing": args.spacing,
            "rho_cells": args.rho_cells,
            "z_cells": args.z_cells,
            "projector_stiffness": 2.0,
        },
        "stationary": {
            key: branch[key]
            for key in (
                "warm_optimizer_success",
                "warm_optimizer_message",
                "warm_iterations",
                "root_success",
                "root_message",
                "root_outer_iterations",
                "euler_lagrange_residual_inf_relative",
                "root_directional_derivative_relative_max",
                "boundary_residual",
                "timelike_gap",
                "max_abs_boost",
                "observables",
            )
        },
        "stationary_gate_pass": stationary_pass,
        "stiffness_map": None,
    }
    if not stationary_pass:
        payload["stability_adjudication"] = "aborted_failed_stationary_gate"
        print("P240_TRACKED_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
        return 2
    values = np.asarray(captured["values"], dtype=np.float64)
    seed = captured["seed"]
    shape = tuple(seed[:-1, 1:-1].shape)
    full_field = M.assemble(
        torch.tensor(values.reshape(shape), dtype=torch.float64, device=M.DEVICE),
        seed,
    ).detach().cpu().numpy()
    args.output_state.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output_state,
        field=full_field,
        spacing=np.array(args.spacing),
        rho_cells=np.array(args.rho_cells),
        z_cells=np.array(args.z_cells),
    )
    payload["output_state"] = str(args.output_state)
    if args.map_stiffness:
        payload["stiffness_map"] = dense_stiffness_map(
            values,
            shape,
            seed,
            parameters,
            (2.0, 4.0, 8.0, 16.0, 32.0),
        )
    print("P240_TRACKED_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0


ORIGINAL_INITIAL_FIELD = M.initial_field
ORIGINAL_ROOT = M.root


if __name__ == "__main__":
    raise SystemExit(main())
