"""Audit P240 coarse-to-fine projection on PyTorch 2.4 CUDA."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.interpolate import RegularGridInterpolator
import torch


ATTEMPTS = Path(__file__).resolve().parents[1]
SOURCE = ATTEMPTS / "0022" / "track_branch_and_map.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0022_projection", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
T = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = T
SPEC.loader.exec_module(T)
M = T.M


def coordinates(cells_rho: int, cells_z: int, spacing: float) -> tuple[np.ndarray, np.ndarray]:
    rho = (np.arange(cells_rho) + 0.5) * spacing
    z = (np.arange(cells_z) - cells_z / 2 + 0.5) * spacing
    return np.meshgrid(rho, z, indexing="ij")


def interpolate_array(
    values: np.ndarray,
    old_spacing: float,
    new_shape: tuple[int, int],
    new_spacing: float,
    method: str,
) -> np.ndarray:
    old_rho, old_z = coordinates(values.shape[0], values.shape[1], old_spacing)
    new_rho, new_z = coordinates(new_shape[0], new_shape[1], new_spacing)
    interpolator = RegularGridInterpolator(
        (old_rho[:, 0], old_z[0, :]),
        values,
        method=method,
        bounds_error=False,
        fill_value=None,
    )
    points = np.stack((new_rho.ravel(), new_z.ravel()), axis=-1)
    return interpolator(points).reshape(new_shape + values.shape[2:])


def physical_components_numpy(field: np.ndarray, spacing: float) -> np.ndarray:
    rho, z = coordinates(field.shape[0], field.shape[1], spacing)
    radius_squared = rho**2 + z**2
    q_radius = radius_squared / (radius_squared + 1.0)
    q_axis = rho**2 / (rho**2 + 1.0)
    q_vector = rho / np.sqrt(rho**2 + 1.0)
    anisotropy, common, split, angle_control = (
        field[..., index] for index in range(4)
    )
    return np.stack(
        (
            common + q_radius * anisotropy,
            common + q_axis * split,
            common - q_axis * split,
            q_vector * angle_control,
            q_vector * field[..., 4],
            field[..., 5],
            field[..., 6],
        ),
        axis=-1,
    )


def controls_from_physical(physical: np.ndarray, spacing: float) -> np.ndarray:
    rho, z = coordinates(physical.shape[0], physical.shape[1], spacing)
    radius_squared = rho**2 + z**2
    q_radius = radius_squared / (radius_squared + 1.0)
    q_axis = rho**2 / (rho**2 + 1.0)
    q_vector = rho / np.sqrt(rho**2 + 1.0)
    director, tangent, azimuthal, angle_residual, boost_rho, boost_z, scalar = (
        physical[..., index] for index in range(7)
    )
    common = 0.5 * (tangent + azimuthal)
    return np.stack(
        (
            (director - common) / q_radius,
            common,
            (tangent - azimuthal) / (2 * q_axis),
            angle_residual / q_vector,
            boost_rho / q_vector,
            boost_z,
            scalar,
        ),
        axis=-1,
    )


def exact_boundary(shape: tuple[int, int], spacing: float) -> np.ndarray:
    parameters = M.Parameters(
        rho_cells=shape[0], z_cells=shape[1], spacing=spacing
    )
    return T.ORIGINAL_INITIAL_FIELD(parameters, 1.0).detach().cpu().numpy()


def project_controls(
    field: np.ndarray,
    old_spacing: float,
    new_shape: tuple[int, int],
    new_spacing: float,
    *,
    method: str = "linear",
    impose_boundary: bool = False,
) -> np.ndarray:
    projected = interpolate_array(field, old_spacing, new_shape, new_spacing, method)
    if impose_boundary:
        boundary = exact_boundary(new_shape, new_spacing)
        projected[-1] = boundary[-1]
        projected[:, 0] = boundary[:, 0]
        projected[:, -1] = boundary[:, -1]
    return projected


def project_physical(
    field: np.ndarray,
    old_spacing: float,
    new_shape: tuple[int, int],
    new_spacing: float,
    *,
    impose_boundary: bool = False,
) -> np.ndarray:
    old_physical = physical_components_numpy(field, old_spacing)
    new_physical = interpolate_array(
        old_physical, old_spacing, new_shape, new_spacing, "linear"
    )
    projected = controls_from_physical(new_physical, new_spacing)
    if impose_boundary:
        boundary = exact_boundary(new_shape, new_spacing)
        projected[-1] = boundary[-1]
        projected[:, 0] = boundary[:, 0]
        projected[:, -1] = boundary[:, -1]
    return projected


def cylindrical_relative_l2(
    computed: np.ndarray, reference: np.ndarray, spacing: float
) -> float:
    rho, _ = coordinates(computed.shape[0], computed.shape[1], spacing)
    weights = rho[..., None] * spacing**2
    numerator = float(np.sum(weights * (computed - reference) ** 2))
    denominator = max(
        float(np.sum(weights * reference**2)),
        float(np.sum(weights)),
    )
    return float(np.sqrt(numerator / denominator))


def manufactured_controls(shape: tuple[int, int], spacing: float) -> np.ndarray:
    rho, z = coordinates(shape[0], shape[1], spacing)
    radius_squared = rho**2 + z**2
    envelope = np.exp(-0.12 * radius_squared)
    return np.stack(
        (
            0.8 + 0.04 * radius_squared,
            0.18 * envelope,
            0.12 * envelope * (1 + 0.05 * z),
            0.09 * envelope,
            0.06 * envelope,
            0.04 * envelope * z,
            -0.08 * envelope,
        ),
        axis=-1,
    )


def affine_controls(shape: tuple[int, int], spacing: float) -> np.ndarray:
    rho, z = coordinates(shape[0], shape[1], spacing)
    constants = np.linspace(-0.2, 0.2, 7)
    radial = np.linspace(0.01, 0.025, 7)
    axial = np.linspace(-0.02, 0.015, 7)
    return constants + rho[..., None] * radial + z[..., None] * axial


def boundary_residual(field: np.ndarray, spacing: float) -> float:
    boundary = exact_boundary(field.shape[:2], spacing)
    return float(
        max(
            np.max(np.abs(field[-1] - boundary[-1])),
            np.max(np.abs(field[:, 0] - boundary[:, 0])),
            np.max(np.abs(field[:, -1] - boundary[:, -1])),
        )
    )


def actual_state_metrics(field: np.ndarray, spacing: float) -> dict:
    parameters = M.Parameters(
        rho_cells=field.shape[0],
        z_cells=field.shape[1],
        spacing=spacing,
        projector_stiffness=2.0,
    )
    seed = T.ORIGINAL_INITIAL_FIELD(parameters, 1.0)
    shape = tuple(seed[:-1, 1:-1].shape)
    values = field[:-1, 1:-1].ravel()
    energy, gradient = M._energy_and_gradient(values, shape, seed, parameters)
    variable = torch.tensor(
        values.reshape(shape), dtype=torch.float64, device=M.DEVICE
    )
    assembled = M.assemble(variable, seed)
    observables = M.observables(assembled, parameters)
    physical = M.physical_components(assembled, parameters)
    eigenvalues = torch.stack(physical[:3], dim=-1)
    gap = torch.min(torch.abs(parameters.g + assembled[..., 6, None] - eigenvalues))
    torch.cuda.synchronize()
    return {
        "energy": float(energy),
        "normalized_euler_lagrange_residual_inf": float(
            np.max(np.abs(gradient)) / max(1.0, abs(energy))
        ),
        "gradient_finite": bool(np.all(np.isfinite(gradient))),
        "inertia": float(observables["inertia"].detach()),
        "frequency": float(observables["frequency"].detach()),
        "timelike_gap": float(gap.detach()),
        "max_abs_boost": float(
            torch.max(torch.abs(torch.stack(physical[4:6], dim=-1))).detach()
        ),
    }


def main() -> int:
    M.configure_device("cuda")
    baseline_path = ATTEMPTS / "0022" / "state-baseline.npz"
    with np.load(baseline_path) as state:
        baseline = np.asarray(state["field"], dtype=np.float64)

    affine_old = affine_controls((8, 16), 0.5)
    affine_exact = affine_controls((10, 20), 0.4)
    affine_linear = project_controls(affine_old, 0.5, (10, 20), 0.4)
    affine_nearest = project_controls(
        affine_old, 0.5, (10, 20), 0.4, method="nearest"
    )
    affine_linear_error = float(np.max(np.abs(affine_linear - affine_exact)))
    affine_nearest_error = float(np.max(np.abs(affine_nearest - affine_exact)))

    manufactured_8 = manufactured_controls((8, 16), 0.5)
    manufactured_10 = manufactured_controls((10, 20), 0.4)
    manufactured_12 = manufactured_controls((12, 24), 1 / 3)
    manufactured_rows = {}
    for name, projector in (
        ("regularized_control_bilinear", project_controls),
        ("physical_component_bilinear", project_physical),
    ):
        projected_10 = projector(manufactured_8, 0.5, (10, 20), 0.4)
        projected_12 = projector(manufactured_10, 0.4, (12, 24), 1 / 3)
        error_8_to_10 = cylindrical_relative_l2(
            physical_components_numpy(projected_10, 0.4),
            physical_components_numpy(manufactured_10, 0.4),
            0.4,
        )
        error_10_to_12 = cylindrical_relative_l2(
            physical_components_numpy(projected_12, 1 / 3),
            physical_components_numpy(manufactured_12, 1 / 3),
            1 / 3,
        )
        medium = projector(
            baseline, 0.5, (10, 20), 0.4, impose_boundary=True
        )
        roundtrip = projector(
            medium, 0.4, (8, 16), 0.5, impose_boundary=True
        )
        roundtrip_error = cylindrical_relative_l2(
            physical_components_numpy(roundtrip[:-1, 1:-1], 0.5),
            physical_components_numpy(baseline[:-1, 1:-1], 0.5),
            0.5,
        )
        metrics = actual_state_metrics(medium, 0.4)
        manufactured_rows[name] = {
            "manufactured_physical_relative_l2_8_to_10": error_8_to_10,
            "manufactured_physical_relative_l2_10_to_12": error_10_to_12,
            "manufactured_error_decreases": bool(error_10_to_12 < error_8_to_10),
            "actual_roundtrip_physical_relative_l2": roundtrip_error,
            "boundary_residual": boundary_residual(medium, 0.4),
            "actual_projected_state": metrics,
            "passes_projection_gates": bool(
                error_10_to_12 < error_8_to_10
                and roundtrip_error <= 0.05
                and boundary_residual(medium, 0.4) == 0.0
                and metrics["timelike_gap"] >= 2.0
                and metrics["inertia"] > 0.0
                and metrics["gradient_finite"]
            ),
        }

    payload = {
        "campaign": "P240",
        "attempt": "0023",
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
            "dtype": "float64",
        },
        "affine_control_reproduction_max_abs": affine_linear_error,
        "wrong_nearest_affine_error_max_abs": affine_nearest_error,
        "affine_gate_pass": bool(affine_linear_error <= 1.0e-12),
        "wrong_method_mutation_breaks_oracle": bool(
            affine_nearest_error > max(1.0e-12, 100 * affine_linear_error)
        ),
        "projection_rows": manufactured_rows,
        "scope": "projection_starting_representation_only_no_stationary_or_stability_verdict",
    }
    print("P240_PROJECTION_RESULT " + json.dumps(payload, sort_keys=True), flush=True)
    return 0 if (
        payload["affine_gate_pass"]
        and payload["wrong_method_mutation_breaks_oracle"]
        and any(row["passes_projection_gates"] for row in manufactured_rows.values())
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main())
