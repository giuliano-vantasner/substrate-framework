"""Refine the full temporal harmonic residual rather than frequency alone."""

from __future__ import annotations

import runpy
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
PREVIOUS = ROOT / "attempts" / "0003" / "explore.py"
API = runpy.run_path(str(PREVIOUS))
projection = API["projection"]
solve_ladder = API["solve_ladder"]
solve_stage = API["solve_stage"]


def residual_metrics(stage, radius: float) -> dict:
    solution = stage.solution
    dense_radius = np.linspace(1.0e-3, radius, 2001)
    amplitudes = solution.sol(dense_radius)[0::2]
    tau = 2.0 * np.pi * np.arange(1024, dtype=float) / 1024.0
    basis = np.cos(np.outer(stage.harmonics, tau))
    field = basis.T @ amplitudes
    retained = projection(
        amplitudes, stage.harmonics, stage.harmonics, 1024
    )
    projected_nonlinearity = basis.T @ retained
    remainder = np.sin(field) - projected_nonlinearity
    core = dense_radius <= 12.0
    next_harmonic = stage.harmonics[-1] + 2
    next_projection = projection(
        amplitudes, stage.harmonics, (next_harmonic,), 1024
    )[0]
    return {
        "harmonics": stage.harmonics,
        "success": bool(solution.success),
        "omega": float(solution.p[0]),
        "max_collocation_rms": float(np.max(solution.rms_residuals)),
        "max_amplitudes": [float(np.max(np.abs(row))) for row in amplitudes],
        "core_full_remainder_rms": float(np.sqrt(np.mean(remainder[:, core] ** 2))),
        "core_full_remainder_max": float(np.max(np.abs(remainder[:, core]))),
        "next_harmonic": next_harmonic,
        "next_projection_core_rms": float(
            np.sqrt(np.mean(next_projection[core] ** 2))
        ),
    }


def main() -> None:
    one, three, five = solve_ladder(40.0, temporal_samples=192, tolerance=1.0e-8)
    stages = [one, three, five]
    previous = five
    for harmonics in ((1, 3, 5, 7), (1, 3, 5, 7, 9)):
        current = solve_stage(
            harmonics,
            amplitude=2.5,
            radius=40.0,
            frequency_guess=float(previous.solution.p[0]),
            temporal_samples=256,
            tolerance=1.0e-8,
            previous=previous,
        )
        stages.append(current)
        previous = current
    for stage in stages:
        print(residual_metrics(stage, 40.0))


if __name__ == "__main__":
    main()
