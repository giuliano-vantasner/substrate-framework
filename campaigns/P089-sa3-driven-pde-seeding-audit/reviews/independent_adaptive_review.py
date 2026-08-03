#!/usr/bin/env python3
"""Independent adaptive-time review of P089's narrow fast-drive branch."""

from __future__ import annotations

import numpy as np

from substrate_framework import (
    SolverTolerances,
    evolve_bulk_driven_sine_gordon_leapfrog,
    evolve_bulk_driven_sine_gordon_mol,
    fit_rest_breather_center_trace,
    fit_rest_breather_snapshot,
    gaussian_sine_full_line_l2,
    gaussian_sine_trace,
    localized_sech_bulk_source,
)
from substrate_framework.verification import CheckLedger


def _rising_crossing_frequency(time: np.ndarray, trace: np.ndarray) -> float:
    indices = np.flatnonzero((trace[:-1] < 0.0) & (trace[1:] >= 0.0))
    if indices.size < 3:
        raise AssertionError("fewer than three late rising crossings")
    crossings = []
    for index in indices:
        fraction = -trace[index] / (trace[index + 1] - trace[index])
        crossings.append(time[index] + fraction * (time[index + 1] - time[index]))
    return float(2.0 * np.pi / np.mean(np.diff(crossings)))


def main() -> int:
    checks = CheckLedger("P089-INDEPENDENT")
    omega_drive = 1.0 / np.sqrt(2.0)
    inverse_width = np.sqrt(1.0 - omega_drive**2)
    temporal_width = 4.0 / omega_drive
    amplitude = np.sqrt(
        400.0 / gaussian_sine_full_line_l2(1.0, omega_drive, temporal_width)
    )
    spacing = 0.05
    coordinate = np.linspace(-80.0, 80.0, 3201)
    zero = np.zeros_like(coordinate)
    damping = np.zeros_like(coordinate)
    selected = np.abs(coordinate) > 40.0
    damping[selected] = np.square((np.abs(coordinate[selected]) - 40.0) / 40.0)
    source = localized_sech_bulk_source(
        coordinate,
        inverse_width,
        gaussian_sine_trace(
            amplitude,
            omega_drive,
            30.0,
            temporal_width,
        ),
    )
    sample_times = np.linspace(0.0, 410.0, 2564)
    adaptive = evolve_bulk_driven_sine_gordon_mol(
        coordinate,
        zero,
        zero,
        source,
        damping,
        sample_times,
        core_radius=12.0,
        tolerances=SolverTolerances(
            rtol=2.0e-8,
            atol=2.0e-10,
            max_step=0.05,
        ),
    )
    checks.check(
        "adaptive DOP853 solve exits with finite state and evaluations",
        adaptive.method.endswith("DOP853")
        and adaptive.function_evaluations is not None
        and adaptive.function_evaluations > 0
        and np.all(np.isfinite(adaptive.final_field))
        and np.all(np.isfinite(adaptive.final_velocity)),
    )
    late = adaptive.time > 320.0
    adaptive_trace_fit = fit_rest_breather_center_trace(
        adaptive.time[late],
        adaptive.center_field[late],
    )
    adaptive_snapshot_fit = fit_rest_breather_snapshot(
        adaptive.coordinate,
        adaptive.final_field,
        adaptive.final_velocity,
        fit_radius=12.0,
    )
    crossing_frequency = _rising_crossing_frequency(
        adaptive.time[late],
        adaptive.center_field[late],
    )
    checks.check(
        "independent crossing estimator agrees with the nonlinear trace fit",
        abs(crossing_frequency - adaptive_trace_fit.angular_frequency) < 0.004,
        (
            f"crossing={crossing_frequency:.9f}, "
            f"fit={adaptive_trace_fit.angular_frequency:.9f}"
        ),
    )
    checks.check(
        "adaptive late trace and full snapshot satisfy the composite classifier",
        adaptive_trace_fit.relative_rms_error < 0.03
        and adaptive_snapshot_fit.joint_relative_l2_error < 0.08
        and 0.2 < adaptive_trace_fit.angular_frequency < 0.4,
    )
    checks.check(
        "adaptive source-work energy ledger closes at sampled-quadrature scale",
        abs(adaptive.energy_balance_residual)
        / adaptive.cumulative_source_work
        < 1.0e-6,
        f"residual={adaptive.energy_balance_residual:.9e}",
    )

    leapfrog_runs = []
    for courant in (0.4, 0.2):
        result = evolve_bulk_driven_sine_gordon_leapfrog(
            coordinate,
            zero,
            zero,
            source,
            damping,
            410.0,
            courant * spacing,
            core_radius=12.0,
            sample_interval=0.16,
        )
        selected_time = result.time > 320.0
        leapfrog_runs.append(
            fit_rest_breather_center_trace(
                result.time[selected_time],
                result.center_field[selected_time],
            )
        )
    adaptive_frequency = adaptive_trace_fit.angular_frequency
    errors = [
        abs(fit.angular_frequency - adaptive_frequency)
        for fit in leapfrog_runs
    ]
    checks.check(
        "timestep halving converges leapfrog frequency toward adaptive DOP853",
        errors[1] < errors[0] / 3.0 and errors[1] < 0.005,
        f"leapfrog errors={errors}",
    )
    checks.check(
        "both leapfrog timesteps retain the exact-family waveform classifier",
        all(fit.relative_rms_error < 0.03 for fit in leapfrog_runs),
    )

    print(
        "P089 independent metrics: "
        f"nfev={adaptive.function_evaluations}, "
        f"DOP_omega={adaptive_trace_fit.angular_frequency:.9f}, "
        f"crossing_omega={crossing_frequency:.9f}, "
        f"trace_rel={adaptive_trace_fit.relative_rms_error:.9e}, "
        f"snapshot_joint={adaptive_snapshot_fit.joint_relative_l2_error:.9e}, "
        f"balance={adaptive.energy_balance_residual:.9e}, "
        f"LF_omega={[fit.angular_frequency for fit in leapfrog_runs]}"
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
