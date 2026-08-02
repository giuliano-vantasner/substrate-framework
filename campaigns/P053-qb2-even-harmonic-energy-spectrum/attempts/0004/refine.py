from __future__ import annotations

import json

import numpy as np

from substrate_framework.radial_harmonic_balance import (
    nonlinear_projection_remainder,
    solve_radial_harmonic_balance,
)
from substrate_framework.radial_harmonic_observables import (
    integrate_spherical_radial_density,
    periodic_fourier_coefficients,
    radial_harmonic_energy_density,
)


def ladder(points: int):
    current = None
    output = []
    for maximum in (1, 3, 5, 7, 9):
        current = solve_radial_harmonic_balance(
            tuple(range(1, maximum + 1, 2)),
            central_fundamental=2.5,
            outer_radius=40.0,
            frequency_guess=0.9769 if current is None else current.frequency,
            radial_points=points,
            temporal_samples=256,
            tolerance=1.0e-8,
            initial_solution=current,
        )
        output.append(current)
    return output


def sampled_density(solution, radius):
    amplitudes = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.amplitudes]
    )
    derivatives = np.vstack(
        [np.interp(radius, solution.radius, row) for row in solution.radial_derivatives]
    )
    phase = 2.0 * np.pi * np.arange(512) / 512
    density = radial_harmonic_energy_density(
        amplitudes, derivatives, solution.harmonics, solution.frequency, phase
    )
    return amplitudes, density


def diagnostics(solution):
    full_radius = np.linspace(
        solution.origin_epsilon, solution.outer_radius, 2401
    )
    _, full_density = sampled_density(solution, full_radius)
    energy = np.asarray(
        integrate_spherical_radial_density(full_radius, full_density)
    )
    core_radius = np.linspace(solution.origin_epsilon, 12.0, 2401)
    core_amplitudes, core_density = sampled_density(solution, core_radius)
    second = np.asarray(
        integrate_spherical_radial_density(
            core_radius, core_density, radial_power=2
        )
    )
    spectrum = periodic_fourier_coefficients(second, max_harmonic=20)
    remainder = nonlinear_projection_remainder(
        core_amplitudes, solution.harmonics, temporal_samples=1024
    )
    return {
        "omega": solution.frequency,
        "core_second_cos2": float(spectrum.cosine[2]),
        "full_box_energy_relative_range": float(np.ptp(energy) / np.mean(energy)),
        "core_full_remainder_rms": float(np.sqrt(np.mean(np.square(remainder)))),
        "max_collocation_rms": solution.max_collocation_rms_residual,
    }


baseline = ladder(300)
mesh_200 = ladder(200)[-1]
mesh_400 = ladder(400)[-1]
tight = solve_radial_harmonic_balance(
    baseline[-1].harmonics,
    central_fundamental=2.5,
    outer_radius=40.0,
    frequency_guess=baseline[-1].frequency,
    temporal_samples=512,
    tolerance=1.0e-9,
    initial_solution=baseline[-1],
)
result = {
    "ladder": {
        str(solution.harmonics[-1]): diagnostics(solution) for solution in baseline
    },
    "N9_initial_mesh": {
        "200": diagnostics(mesh_200),
        "300": diagnostics(baseline[-1]),
        "400": diagnostics(mesh_400),
    },
    "N9_tolerance": {
        "1e-8": diagnostics(baseline[-1]),
        "1e-9_with_512_projection_samples": diagnostics(tight),
    },
}
print(json.dumps(result, indent=2, sort_keys=True))
