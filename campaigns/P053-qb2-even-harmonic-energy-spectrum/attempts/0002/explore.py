from __future__ import annotations

import json

import numpy as np

from substrate_framework.radial_harmonic_balance import solve_radial_harmonic_balance
from substrate_framework.radial_harmonic_observables import (
    integrate_spherical_radial_density,
    periodic_fourier_coefficients,
    radial_harmonic_energy_density,
    spherical_radial_second_moment_tensor,
    time_averaged_per_axis_energy_variance,
)


def solve_ladder(
    outer_radius: float,
    *,
    radial_points: int = 300,
    temporal_samples: int = 256,
    tolerance: float = 1.0e-8,
):
    current = None
    solutions = []
    frequency = 0.9769
    for maximum in (1, 3, 5, 7, 9):
        current = solve_radial_harmonic_balance(
            tuple(range(1, maximum + 1, 2)),
            central_fundamental=2.5,
            outer_radius=outer_radius,
            frequency_guess=frequency,
            radial_points=radial_points,
            temporal_samples=temporal_samples,
            tolerance=tolerance,
            initial_solution=current,
        )
        solutions.append(current)
        frequency = current.frequency
    return solutions


def analyze(solution, *, phase_samples: int, radial_samples: int, cutoff: float | None):
    stop = solution.outer_radius if cutoff is None else min(cutoff, solution.outer_radius)
    radius = np.linspace(solution.origin_epsilon, stop, radial_samples)
    amplitudes = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.amplitudes]
    )
    derivatives = np.vstack(
        [
            np.interp(radius, solution.radius, row)
            for row in solution.radial_derivatives
        ]
    )
    phase = 2.0 * np.pi * np.arange(phase_samples) / phase_samples
    density = radial_harmonic_energy_density(
        amplitudes,
        derivatives,
        solution.harmonics,
        solution.frequency,
        phase,
    )
    energy = np.asarray(integrate_spherical_radial_density(radius, density))
    second = np.asarray(
        integrate_spherical_radial_density(radius, density, radial_power=2)
    )
    energy_spectrum = periodic_fourier_coefficients(energy, max_harmonic=20)
    second_spectrum = periodic_fourier_coefficients(second, max_harmonic=20)
    amplitude = second_spectrum.amplitude
    even_power = float(np.sum(np.square(amplitude[2::2])))
    odd_power = float(np.sum(np.square(amplitude[1::2])))
    tensor = spherical_radial_second_moment_tensor(radius, density)
    trace = np.trace(tensor, axis1=-2, axis2=-1)
    trace_free = tensor - trace[:, None, None] * np.eye(3) / 3.0
    return {
        "omega": solution.frequency,
        "energy_relative_range": float(np.ptp(energy) / np.mean(energy)),
        "second_dc": float(second_spectrum.cosine[0]),
        "second_cos2": float(second_spectrum.cosine[2]),
        "second_cos4": float(second_spectrum.cosine[4]),
        "second_two_even_power_fraction": float(amplitude[2] ** 2 / even_power),
        "second_odd_even_power_ratio": odd_power / even_power,
        "per_axis_variance": time_averaged_per_axis_energy_variance(radius, density),
        "max_stf": float(np.max(np.abs(trace_free))),
    }


baseline = solve_ladder(40.0)
result = {
    "harmonic_ladder_core_r12": {
        str(solution.harmonics[-1]): analyze(
            solution, phase_samples=512, radial_samples=2401, cutoff=12.0
        )
        for solution in baseline
    },
    "N9_full_box": analyze(
        baseline[-1], phase_samples=512, radial_samples=2401, cutoff=None
    ),
    "N9_time_refinement": {
        str(samples): analyze(
            baseline[-1], phase_samples=samples, radial_samples=2401, cutoff=12.0
        )
        for samples in (256, 512, 1024)
    },
    "N9_radial_refinement": {
        str(samples): analyze(
            baseline[-1], phase_samples=512, radial_samples=samples, cutoff=12.0
        )
        for samples in (1201, 2401, 4801)
    },
    "N9_domain_scan_full_box": {},
    "N9_domain_scan_core_r12": {},
}
for outer in (30.0, 40.0, 50.0, 60.0):
    solution = baseline[-1] if outer == 40.0 else solve_ladder(outer)[-1]
    result["N9_domain_scan_full_box"][str(int(outer))] = analyze(
        solution, phase_samples=512, radial_samples=2401, cutoff=None
    )
    result["N9_domain_scan_core_r12"][str(int(outer))] = analyze(
        solution, phase_samples=512, radial_samples=2401, cutoff=12.0
    )
print(json.dumps(result, indent=2, sort_keys=True))
