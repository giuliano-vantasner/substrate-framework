#!/usr/bin/env python3
"""Run P047 attempt 0001's frozen corrected-trace derivative study."""

from __future__ import annotations

import json

import numpy as np

from substrate_framework.numerics import (
    interpolating_spline_time_derivative,
    local_polynomial_time_derivative,
)
from substrate_framework.radial_sine_gordon import gaussian_radial_seed
from substrate_framework.sine_gordon_l_modes import (
    LinearizedAngularModeEvolution,
    evolve_radial_background_with_linearized_mode,
    regular_l_mode_gaussian_seed,
)


def run_branch(
    spacing: float,
    *,
    outer_radius: float = 80.0,
    final_time: float = 40.0,
    courant: float = 0.4,
    mode_amplitude: float = 0.2,
) -> LinearizedAngularModeEvolution:
    radius = spacing * np.arange(int(round(outer_radius / spacing)) + 1)
    return evolve_radial_background_with_linearized_mode(
        gaussian_radial_seed(radius, 3.0, 4.0),
        regular_l_mode_gaussian_seed(
            radius,
            ell=2,
            amplitude=mode_amplitude,
            width=4.0,
        ),
        spacing=spacing,
        final_time=final_time,
        ell=2,
        courant=courant,
        sample_interval=0.16,
    )


def sampled(result: LinearizedAngularModeEvolution, stride: int) -> tuple[np.ndarray, np.ndarray]:
    return (
        result.time[::stride],
        result.p2_triple_stf_zz_coefficient[::stride],
    )


def derivatives(
    time: np.ndarray,
    trace: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    interval = float(time[1] - time[0])
    local_second = local_polynomial_time_derivative(
        time,
        trace,
        2,
        window_duration=8.0 * interval,
        polynomial_order=5,
    )
    local_third = local_polynomial_time_derivative(
        time,
        trace,
        3,
        window_duration=8.0 * interval,
        polynomial_order=5,
    )
    spline_second = interpolating_spline_time_derivative(
        time,
        trace,
        2,
        spline_degree=5,
    )
    spline_third = interpolating_spline_time_derivative(
        time,
        trace,
        3,
        spline_degree=5,
    )
    return local_second, local_third, spline_second, spline_third


def mask(time: np.ndarray) -> np.ndarray:
    return (time >= 5.0) & (time <= 35.0)


def rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values))))


def symmetric_relative_rms(first: np.ndarray, second: np.ndarray) -> float:
    denominator = 0.5 * (rms(first) + rms(second))
    if denominator <= 1.0e-14:
        if np.array_equal(first, second):
            return 0.0
        raise RuntimeError("near-zero derivative comparison has unequal traces")
    return rms(first - second) / denominator


def aligned_local(result: LinearizedAngularModeEvolution) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    time, trace = sampled(result, 2)
    second, third, _spline_second, _spline_third = derivatives(time, trace)
    interior = mask(time)
    return time[interior], second[interior], third[interior]


def main() -> None:
    coarse, baseline, fine = [run_branch(spacing) for spacing in (0.2, 0.1, 0.05)]
    timestep = run_branch(0.1, courant=0.2)
    domain = run_branch(0.1, outer_radius=100.0)
    half_amplitude = run_branch(0.1, mode_amplitude=0.1)
    zero_amplitude = run_branch(0.2, final_time=8.0, mode_amplitude=0.0)

    aligned = [aligned_local(result) for result in (coarse, baseline, fine)]
    for time, _second, _third in aligned[1:]:
        if not np.array_equal(time, aligned[0][0]):
            raise RuntimeError("mesh derivative time grids do not align")
    mesh_second = [
        symmetric_relative_rms(aligned[0][1], aligned[1][1]),
        symmetric_relative_rms(aligned[1][1], aligned[2][1]),
    ]
    mesh_third = [
        symmetric_relative_rms(aligned[0][2], aligned[1][2]),
        symmetric_relative_rms(aligned[1][2], aligned[2][2]),
    ]

    base_time, base_second, base_third = aligned[1]
    timestep_time, timestep_second, timestep_third = aligned_local(timestep)
    domain_time, domain_second, domain_third = aligned_local(domain)
    half_time, half_second, half_third = aligned_local(half_amplitude)
    if not all(
        np.array_equal(base_time, comparison)
        for comparison in (timestep_time, domain_time, half_time)
    ):
        raise RuntimeError("mutation derivative time grids do not align")

    dense_time, dense_trace = sampled(baseline, 1)
    dense_second, dense_third, _dense_spline_second, _dense_spline_third = derivatives(
        dense_time,
        dense_trace,
    )
    dense_interior = mask(dense_time)
    dense_time_interior = dense_time[dense_interior]
    dense_second_interior = dense_second[dense_interior]
    dense_third_interior = dense_third[dense_interior]
    dense_on_reported = np.searchsorted(dense_time_interior, base_time)
    if not np.array_equal(dense_time_interior[dense_on_reported], base_time):
        raise RuntimeError("dense and reported sample grids do not align")

    reported_time, reported_trace = sampled(baseline, 2)
    local_second, local_third, spline_second, spline_third = derivatives(
        reported_time,
        reported_trace,
    )
    reported_interior = mask(reported_time)
    local_second = local_second[reported_interior]
    local_third = local_third[reported_interior]
    spline_second = spline_second[reported_interior]
    spline_third = spline_third[reported_interior]

    zero_trace_exact = bool(
        np.array_equal(
            zero_amplitude.p2_triple_stf_zz_coefficient,
            np.zeros_like(zero_amplitude.p2_triple_stf_zz_coefficient),
        )
    )
    half_second_error = symmetric_relative_rms(half_second, 0.5 * base_second)
    half_third_error = symmetric_relative_rms(half_third, 0.5 * base_third)
    correct_power = np.square(base_third) / 30.0
    half_power = np.square(half_third) / 30.0
    source_convention_power = 1.5 * np.square(base_third) / 5.0

    result = {
        "completed": bool(
            all(
                branch.completed
                and np.all(np.isfinite(branch.p2_triple_stf_zz_coefficient))
                for branch in (coarse, baseline, fine, timestep, domain, half_amplitude)
            )
        ),
        "mesh_second_relative_rms": mesh_second,
        "mesh_third_relative_rms": mesh_third,
        "timestep_second_relative_rms": symmetric_relative_rms(base_second, timestep_second),
        "timestep_third_relative_rms": symmetric_relative_rms(base_third, timestep_third),
        "domain_second_relative_rms": symmetric_relative_rms(base_second, domain_second),
        "domain_third_relative_rms": symmetric_relative_rms(base_third, domain_third),
        "sampling_second_relative_rms": symmetric_relative_rms(
            base_second,
            dense_second_interior[dense_on_reported],
        ),
        "sampling_third_relative_rms": symmetric_relative_rms(
            base_third,
            dense_third_interior[dense_on_reported],
        ),
        "estimator_second_relative_rms": symmetric_relative_rms(local_second, spline_second),
        "estimator_third_relative_rms": symmetric_relative_rms(local_third, spline_third),
        "half_second_scaling_error": half_second_error,
        "half_third_scaling_error": half_third_error,
        "half_power_quarter_scaling_error": symmetric_relative_rms(half_power, 0.25 * correct_power),
        "zero_trace_exact": zero_trace_exact,
        "triple_qzz_second_rms": rms(base_second),
        "triple_qzz_third_rms": rms(base_third),
        "conditional_edge_on_waveform_R_over_G_rms": rms(base_second / 2.0),
        "conditional_power_over_G_mean": float(np.mean(correct_power)),
        "conditional_power_over_G_min": float(np.min(correct_power)),
        "source_wrong_convention_mean_power_ratio": float(
            np.mean(source_convention_power) / np.mean(correct_power)
        ),
        "background_boundary_max": max(
            branch.max_boundary_background for branch in (coarse, baseline, fine)
        ),
        "mode_boundary_max": max(
            branch.max_boundary_mode for branch in (coarse, baseline, fine)
        ),
        "sample_count_reported_interior": int(base_time.size),
        "sample_count_dense_interior": int(dense_time_interior.size),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
