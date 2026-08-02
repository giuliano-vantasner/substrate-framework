"""Explore the averaged l=2 operator on the accepted C-PDE-006 background."""

from __future__ import annotations

import json

import numpy as np
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh
from scipy.special import spherical_jn

from substrate_framework.radial_harmonic_balance import solve_radial_harmonic_balance


def solve_background():
    previous = None
    for maximum in (1, 3, 5, 7, 9):
        previous = solve_radial_harmonic_balance(
            tuple(range(1, maximum + 1, 2)),
            central_fundamental=2.5,
            outer_radius=40.0,
            frequency_guess=0.9769 if previous is None else previous.frequency,
            radial_points=300,
            temporal_samples=256,
            tolerance=1.0e-8,
            initial_solution=previous,
        )
    return previous


def averaged_potential(solution, radius: np.ndarray, phases: int = 1024) -> tuple[np.ndarray, np.ndarray]:
    amplitudes = np.vstack(
        [np.interp(radius, solution.radius, row, left=row[0]) for row in solution.amplitudes]
    )
    tau = 2.0 * np.pi * np.arange(phases, dtype=float) / phases
    field = amplitudes.T @ np.cos(np.outer(solution.harmonics, tau))
    return np.mean(np.cos(field), axis=1), field


def eigenpair(solution, outer_radius: float, intervals: int, *, vacuum: bool = False) -> dict[str, float]:
    radius = np.linspace(0.0, outer_radius, intervals + 1)
    spacing = radius[1]
    if vacuum:
        potential = np.ones_like(radius)
        field = np.zeros((radius.size, 1))
    else:
        potential, field = averaged_potential(solution, radius)
    interior = radius[1:-1]
    diagonal = 2.0 / spacing**2 + 6.0 / interior**2 + potential[1:-1]
    off_diagonal = np.full(interior.size - 1, -1.0 / spacing**2)
    operator = diags((off_diagonal, diagonal, off_diagonal), offsets=(-1, 0, 1), format="csr")
    values, vectors = eigsh(operator, k=1, which="SA", tol=1.0e-11, maxiter=100_000)
    eigenvalue = float(values[0])
    vector = vectors[:, 0]
    vector /= np.sqrt(np.sum(vector**2) * spacing)
    residual = operator @ vector - eigenvalue * vector
    relative_residual = float(np.linalg.norm(residual) / max(1.0, abs(eigenvalue)) / np.linalg.norm(vector))
    tail = interior >= 0.75 * outer_radius
    tail_fraction = float(np.sum(vector[tail] ** 2) / np.sum(vector**2))
    if vacuum:
        defect = 0.0
    else:
        temporal_defect = (np.cos(field[1:-1]) - potential[1:-1, None]) * vector[:, None]
        defect = float(
            np.sqrt(np.mean(np.sum(temporal_defect**2, axis=0)) * spacing)
            / np.sqrt(np.sum(vector**2) * spacing)
        )
    return {
        "outer_radius": outer_radius,
        "intervals": intervals,
        "spacing": spacing,
        "eigenvalue": eigenvalue,
        "continuum_gap": 1.0 - eigenvalue,
        "relative_residual": relative_residual,
        "outer_quarter_v_norm_fraction": tail_fraction,
        "weighted_relative_full_equation_defect": defect,
    }


def first_spherical_j2_zero() -> float:
    return float(brentq(lambda value: spherical_jn(2, value), 5.0, 6.5))


def main() -> None:
    solution = solve_background()
    meshes = [eigenpair(solution, 40.0, intervals) for intervals in (800, 1600, 3200)]
    walls = [eigenpair(solution, outer, int(40 * outer)) for outer in (20.0, 30.0, 40.0)]
    zero = first_spherical_j2_zero()
    vacuum_meshes = [eigenpair(solution, 40.0, intervals, vacuum=True) for intervals in (800, 1600, 3200)]
    exact_vacuum = 1.0 + (zero / 40.0) ** 2
    output = {
        "background": {
            "harmonics": solution.harmonics,
            "frequency": solution.frequency,
            "max_collocation_rms_residual": solution.max_collocation_rms_residual,
            "outer_conditions": solution.outer_conditions,
        },
        "mesh_refinement": meshes,
        "wall_refinement": walls,
        "vacuum_reference": {
            "first_spherical_j2_zero": zero,
            "exact_first_eigenvalue": exact_vacuum,
            "meshes": vacuum_meshes,
        },
    }
    fine_errors = [abs(item["eigenvalue"] - meshes[-1]["eigenvalue"]) for item in meshes[:-1]]
    output["diagnostics"] = {
        "coarse_to_medium_error_ratio_against_fine": fine_errors[0] / fine_errors[1],
        "wall_30_to_40_eigenvalue_difference": abs(walls[1]["eigenvalue"] - walls[2]["eigenvalue"]),
        "fine_vacuum_absolute_error": abs(vacuum_meshes[-1]["eigenvalue"] - exact_vacuum),
        "spectral_residual_gate": meshes[-1]["relative_residual"] < 1.0e-8,
        "mesh_ratio_gate": fine_errors[0] / fine_errors[1] > 2.0,
        "vacuum_gate": abs(vacuum_meshes[-1]["eigenvalue"] - exact_vacuum) < 5.0e-4,
        "bound_candidate_gate": meshes[-1]["continuum_gap"] > 5.0e-3
        and abs(walls[1]["eigenvalue"] - walls[2]["eigenvalue"]) < 2.0e-3
        and meshes[-1]["outer_quarter_v_norm_fraction"] < 1.0e-4,
        "full_equation_equivalence_gate": meshes[-1]["weighted_relative_full_equation_defect"] < 1.0e-3,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
