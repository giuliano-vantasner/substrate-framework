"""Canonical P052 harmonic-balance refinement study."""

from __future__ import annotations

import numpy as np

from substrate_framework.radial_harmonic_balance import (
    nonlinear_projection_remainder,
    odd_harmonics,
    project_sine_harmonics,
    sampled_harmonic_balance_residual,
    solve_radial_harmonic_balance,
)


def solve_ladder(
    outer_radius: float,
    *,
    radial_points: int = 300,
    temporal_samples: int = 256,
    tolerance: float = 1.0e-8,
):
    solutions = []
    previous = None
    frequency = 0.9769
    for maximum in (1, 3, 5, 7, 9):
        solution = solve_radial_harmonic_balance(
            odd_harmonics(maximum),
            central_fundamental=2.5,
            outer_radius=outer_radius,
            frequency_guess=frequency,
            radial_points=radial_points,
            temporal_samples=temporal_samples,
            tolerance=tolerance,
            initial_solution=previous,
        )
        solutions.append(solution)
        previous = solution
        frequency = solution.frequency
    return solutions


def metrics(solution) -> dict:
    radius = np.linspace(solution.origin_epsilon, solution.outer_radius, 2401)
    amplitudes = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.amplitudes]
    )
    core = radius <= 12.0
    remainder = nonlinear_projection_remainder(
        amplitudes, solution.harmonics, temporal_samples=1024
    )
    next_mode = solution.harmonics[-1] + 2
    omitted = project_sine_harmonics(
        amplitudes,
        solution.harmonics,
        target_harmonics=(next_mode,),
        temporal_samples=1024,
    )[0]
    independent = sampled_harmonic_balance_residual(
        radius,
        amplitudes,
        solution.harmonics,
        solution.frequency,
        temporal_samples=1024,
    )
    tail = radius >= 0.75 * solution.outer_radius
    return {
        "harmonics": solution.harmonics,
        "omega": solution.frequency,
        "nodes": solution.radius.size,
        "max_collocation_rms": solution.max_collocation_rms_residual,
        "core_remainder_rms": float(np.sqrt(np.mean(remainder[:, core] ** 2))),
        "core_remainder_max": float(np.max(np.abs(remainder[:, core]))),
        "next_mode": next_mode,
        "next_mode_core_rms": float(np.sqrt(np.mean(omitted[core] ** 2))),
        "independent_projected_rms": [
            float(np.sqrt(np.mean(row[4:-4] ** 2))) for row in independent
        ],
        "tail_r_amplitude_rms": [
            float(np.sqrt(np.mean((radius[tail] * row[tail]) ** 2)))
            for row in amplitudes
        ],
        "channels": [channel.behavior for channel in solution.tail_channels],
        "outer_conditions": solution.outer_conditions,
    }


def main() -> None:
    baseline = solve_ladder(40.0)
    print("BASELINE")
    for solution in baseline:
        print(metrics(solution))

    for outer_radius in (30.0, 50.0, 60.0):
        solution = solve_ladder(outer_radius)[-1]
        print("DOMAIN", outer_radius, metrics(solution))

    coarse_mesh = solve_ladder(40.0, radial_points=200)[-1]
    fine_mesh = solve_ladder(40.0, radial_points=400)[-1]
    print("MESH_200", metrics(coarse_mesh))
    print("MESH_400", metrics(fine_mesh))

    time_512 = solve_radial_harmonic_balance(
        baseline[-1].harmonics,
        central_fundamental=2.5,
        outer_radius=40.0,
        frequency_guess=baseline[-1].frequency,
        temporal_samples=512,
        tolerance=1.0e-8,
        initial_solution=baseline[-1],
    )
    tight = solve_radial_harmonic_balance(
        time_512.harmonics,
        central_fundamental=2.5,
        outer_radius=40.0,
        frequency_guess=time_512.frequency,
        temporal_samples=512,
        tolerance=1.0e-9,
        initial_solution=time_512,
    )
    print("TIME_512", metrics(time_512))
    print("TOL_1E-9", metrics(tight))


if __name__ == "__main__":
    main()
