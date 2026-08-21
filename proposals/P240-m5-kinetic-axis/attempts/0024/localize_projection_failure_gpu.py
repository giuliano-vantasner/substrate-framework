"""Localize why the actual P240 coarse state cannot be safely prolonged."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
from scipy.fft import dctn
from scipy.interpolate import RegularGridInterpolator
import torch


ATTEMPTS = Path(__file__).resolve().parents[1]
SOURCE = ATTEMPTS / "0023" / "audit_projection_gpu.py"
SPEC = importlib.util.spec_from_file_location("p240_attempt0023_projection", SOURCE)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"could not load {SOURCE}")
P = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = P
SPEC.loader.exec_module(P)
M = P.M


def even_axis_control_projection(
    field: np.ndarray,
    old_spacing: float,
    new_shape: tuple[int, int],
    new_spacing: float,
    *,
    impose_boundary: bool,
) -> np.ndarray:
    old_rho, old_z = P.coordinates(field.shape[0], field.shape[1], old_spacing)
    new_rho, new_z = P.coordinates(new_shape[0], new_shape[1], new_spacing)
    rho_axis = old_rho[:, 0]
    augmented_rho = np.concatenate((-rho_axis[::-1], rho_axis))
    augmented_field = np.concatenate((field[::-1], field), axis=0)
    interpolator = RegularGridInterpolator(
        (augmented_rho, old_z[0, :]),
        augmented_field,
        method="linear",
        bounds_error=False,
        fill_value=None,
    )
    points = np.stack((new_rho.ravel(), new_z.ravel()), axis=-1)
    projected = interpolator(points).reshape(new_shape + (7,))
    if impose_boundary:
        boundary = P.exact_boundary(new_shape, new_spacing)
        projected[-1] = boundary[-1]
        projected[:, 0] = boundary[:, 0]
        projected[:, -1] = boundary[:, -1]
    return projected


def relative_components(
    computed: np.ndarray, reference: np.ndarray, spacing: float
) -> list[float]:
    return [
        P.cylindrical_relative_l2(
            computed[..., index : index + 1],
            reference[..., index : index + 1],
            spacing,
        )
        for index in range(computed.shape[-1])
    ]


def error_shell_fractions(
    computed: np.ndarray, reference: np.ndarray, spacing: float
) -> dict:
    rho, _ = P.coordinates(computed.shape[0], computed.shape[1], spacing)
    error = rho * np.sum((computed - reference) ** 2, axis=-1)
    total = max(float(np.sum(error)), np.finfo(np.float64).tiny)
    mask = np.zeros(error.shape, dtype=bool)
    mask[0] = True
    axis = float(np.sum(error[mask]) / total)
    mask[:] = False
    mask[-1] = True
    outer_rho = float(np.sum(error[mask]) / total)
    mask[:] = False
    mask[:, 0] = True
    mask[:, -1] = True
    z_edges = float(np.sum(error[mask]) / total)
    return {
        "axis_row_fraction": axis,
        "outer_rho_row_fraction": outer_rho,
        "z_edge_rows_fraction": z_edges,
    }


def spectral_diagnostics(field: np.ndarray) -> dict:
    physical = P.physical_components_numpy(field, 0.5)
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
    radial_count, axial_count = physical.shape[:2]
    radial_indices, axial_indices = np.meshgrid(
        np.arange(radial_count), np.arange(axial_count), indexing="ij"
    )
    high_mask = (radial_indices >= radial_count // 2) | (
        axial_indices >= axial_count // 2
    )
    checker = (-1.0) ** (radial_indices + axial_indices)
    for index, name in enumerate(names):
        values = physical[..., index]
        centered = values - np.mean(values)
        coefficients = dctn(centered, type=2, norm="ortho")
        total_power = max(float(np.sum(coefficients**2)), np.finfo(np.float64).tiny)
        centered_norm = max(float(np.linalg.norm(centered)), np.finfo(np.float64).tiny)
        rows[name] = {
            "high_half_DCT_power_fraction": float(
                np.sum(coefficients[high_mask] ** 2) / total_power
            ),
            "checkerboard_correlation_abs": float(
                abs(np.sum(centered * checker))
                / (centered_norm * np.linalg.norm(checker))
            ),
            "range": [float(np.min(values)), float(np.max(values))],
        }
    return rows


def full_metrics(field: np.ndarray, spacing: float) -> dict:
    parameters = M.Parameters(
        rho_cells=field.shape[0],
        z_cells=field.shape[1],
        spacing=spacing,
        projector_stiffness=2.0,
    )
    seed = P.T.ORIGINAL_INITIAL_FIELD(parameters, 1.0)
    shape = tuple(seed[:-1, 1:-1].shape)
    values = field[:-1, 1:-1].ravel()
    energy, gradient = M._energy_and_gradient(values, shape, seed, parameters)
    variable = torch.tensor(
        values.reshape(shape), dtype=torch.float64, device=M.DEVICE
    )
    assembled = M.assemble(variable, seed)
    observables = M.observables(assembled, parameters)
    torch.cuda.synchronize()
    return {
        "total": float(energy),
        "normalized_residual_inf": float(
            np.max(np.abs(gradient)) / max(1.0, abs(energy))
        ),
        "terms": {name: float(value.detach()) for name, value in observables.items()},
    }


def main() -> int:
    M.configure_device("cuda")
    with np.load(ATTEMPTS / "0022" / "state-baseline.npz") as state:
        baseline = np.asarray(state["field"], dtype=np.float64)
    baseline_metrics = full_metrics(baseline, 0.5)
    same_grid = P.project_controls(baseline, 0.5, (8, 16), 0.5)
    same_grid_error = float(np.max(np.abs(same_grid - baseline)))
    baseline_physical = P.physical_components_numpy(baseline, 0.5)

    projectors = {
        "control_linear": lambda field, old_h, shape, new_h, boundary: P.project_controls(
            field, old_h, shape, new_h, impose_boundary=boundary
        ),
        "physical_linear": lambda field, old_h, shape, new_h, boundary: P.project_physical(
            field, old_h, shape, new_h, impose_boundary=boundary
        ),
        "even_axis_control_linear": lambda field, old_h, shape, new_h, boundary: even_axis_control_projection(
            field, old_h, shape, new_h, impose_boundary=boundary
        ),
    }
    rows = {}
    for name, projector in projectors.items():
        medium = projector(baseline, 0.5, (10, 20), 0.4, True)
        restricted_with_boundary = projector(medium, 0.4, (8, 16), 0.5, True)
        medium_no_boundary = projector(baseline, 0.5, (10, 20), 0.4, False)
        restricted_no_boundary = projector(
            medium_no_boundary, 0.4, (8, 16), 0.5, False
        )
        physical_with_boundary = P.physical_components_numpy(
            restricted_with_boundary, 0.5
        )
        physical_no_boundary = P.physical_components_numpy(
            restricted_no_boundary, 0.5
        )
        rows[name] = {
            "medium_metrics": full_metrics(medium, 0.4),
            "roundtrip_with_boundary_relative_l2": P.cylindrical_relative_l2(
                physical_with_boundary[:-1, 1:-1],
                baseline_physical[:-1, 1:-1],
                0.5,
            ),
            "roundtrip_without_boundary_relative_l2": P.cylindrical_relative_l2(
                physical_no_boundary[:-1, 1:-1],
                baseline_physical[:-1, 1:-1],
                0.5,
            ),
            "roundtrip_component_errors_with_boundary": relative_components(
                physical_with_boundary[:-1, 1:-1],
                baseline_physical[:-1, 1:-1],
                0.5,
            ),
            "roundtrip_error_shell_fractions_with_boundary": error_shell_fractions(
                physical_with_boundary[:-1, 1:-1],
                baseline_physical[:-1, 1:-1],
                0.5,
            ),
        }

    manufactured = P.manufactured_controls((8, 16), 0.5)
    payload = {
        "campaign": "P240",
        "attempt": "0024",
        "environment": {
            "torch": torch.__version__,
            "cuda_runtime": torch.version.cuda,
            "device": torch.cuda.get_device_name(0),
        },
        "saved_baseline_reconstruction": baseline_metrics,
        "same_grid_control_identity_max_abs": same_grid_error,
        "actual_baseline_spectrum": spectral_diagnostics(baseline),
        "smooth_manufactured_spectrum": spectral_diagnostics(manufactured),
        "projection_rows": rows,
        "scope": "failure_localization_only",
    }
    print("P240_PROJECTION_LOCALIZATION " + json.dumps(payload, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
