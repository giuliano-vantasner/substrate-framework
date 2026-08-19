"""Constructive SciPy replacement for the P238 real-scalar lump claim.

The paper's cited charged-complex-field theorem does not prove existence for
its real 2+1D scalar.  This file supplies a narrower result with the same
intended purpose: reproducible finite-time numerical evidence for a localized
real 2+1D sine-Gordon energy lump, using two independent time integrators.
It does not claim an eternal breather or all-potential existence theorem.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class Evolution:
    method: str
    time: FloatArray
    center: FloatArray
    core_energy: FloatArray
    total_energy: FloatArray


@dataclass(frozen=True)
class ReplacementResult:
    claim: str
    revised_claim: str
    passed: bool
    leapfrog_late_core_fraction: float
    mol_late_core_fraction: float
    refined_late_core_fraction: float
    refinement_difference: float
    leapfrog_energy_drift: float
    mol_energy_drift: float
    center_relative_rms: float
    core_relative_max: float
    parameters: dict[str, float]


def radial_laplacian_2d(field: FloatArray, spacing: float) -> FloatArray:
    """Second-order ``u_rr+u_r/r`` with even origin regularity."""

    radius = spacing * np.arange(field.size, dtype=np.float64)
    result = np.zeros_like(field)
    result[1:-1] = (
        (field[2:] - 2.0 * field[1:-1] + field[:-2]) / spacing**2
        + (field[2:] - field[:-2])
        / (2.0 * spacing * radius[1:-1])
    )
    result[0] = 4.0 * (field[1] - field[0]) / spacing**2
    return result


def energy_2d(
    field: FloatArray,
    velocity: FloatArray,
    radius: FloatArray,
    *,
    maximum_radius: float | None = None,
) -> float:
    """Return ``2*pi*integral r*T00 dr`` for ``U=1-cos(u)``."""

    spacing = float(radius[1] - radius[0])
    gradient = np.empty_like(field)
    gradient[0] = 0.0
    gradient[1:-1] = (field[2:] - field[:-2]) / (2.0 * spacing)
    gradient[-1] = (field[-1] - field[-2]) / spacing
    density = (
        0.5 * velocity**2
        + 0.5 * gradient**2
        + 1.0
        - np.cos(field)
    )
    selected = np.ones(radius.size, dtype=bool)
    if maximum_radius is not None:
        selected = radius <= maximum_radius
    return float(
        2.0
        * np.pi
        * np.trapezoid(radius[selected] * density[selected], radius[selected])
    )


def _diagnostics(
    method: str,
    time: FloatArray,
    fields: FloatArray,
    velocities: FloatArray,
    radius: FloatArray,
    core_radius: float,
) -> Evolution:
    core = np.asarray(
        [
            energy_2d(field, velocity, radius, maximum_radius=core_radius)
            for field, velocity in zip(fields, velocities, strict=True)
        ]
    )
    total = np.asarray(
        [
            energy_2d(field, velocity, radius)
            for field, velocity in zip(fields, velocities, strict=True)
        ]
    )
    return Evolution(
        method=method,
        time=time,
        center=fields[:, 0],
        core_energy=core,
        total_energy=total,
    )


def evolve_leapfrog(
    *,
    amplitude: float,
    width: float,
    spacing: float,
    outer_radius: float,
    final_time: float,
    core_radius: float,
    sample_interval: float,
    courant: float = 0.35,
) -> Evolution:
    radius = np.arange(0.0, outer_radius + 0.5 * spacing, spacing)
    previous = amplitude * np.exp(-np.square(radius / width))
    previous[-1] = 0.0
    steps = int(np.ceil(final_time / (courant * spacing)))
    timestep = final_time / steps
    current = previous + 0.5 * timestep**2 * (
        radial_laplacian_2d(previous, spacing) - np.sin(previous)
    )
    current[-1] = 0.0
    stride = max(1, int(round(sample_interval / timestep)))
    times = [0.0]
    fields = [previous.copy()]
    velocities = [np.zeros_like(previous)]
    for step in range(1, steps):
        following = (
            2.0 * current
            - previous
            + timestep**2
            * (radial_laplacian_2d(current, spacing) - np.sin(current))
        )
        following[-1] = 0.0
        centered_velocity = (following - previous) / (2.0 * timestep)
        if step % stride == 0:
            times.append(step * timestep)
            fields.append(current.copy())
            velocities.append(centered_velocity.copy())
        previous, current = current, following
    return _diagnostics(
        "centered-leapfrog",
        np.asarray(times),
        np.asarray(fields),
        np.asarray(velocities),
        radius,
        core_radius,
    )


def evolve_mol(
    *,
    amplitude: float,
    width: float,
    spacing: float,
    outer_radius: float,
    final_time: float,
    core_radius: float,
    sample_interval: float,
) -> Evolution:
    radius = np.arange(0.0, outer_radius + 0.5 * spacing, spacing)
    field0 = amplitude * np.exp(-np.square(radius / width))
    field0[-1] = 0.0
    interior = radius.size - 1
    state0 = np.concatenate((field0[:-1], np.zeros(interior)))
    sample_count = int(round(final_time / sample_interval)) + 1
    sample_time = np.linspace(0.0, final_time, sample_count)

    def rhs(_time: float, state: FloatArray) -> FloatArray:
        field = np.zeros(radius.size)
        field[:-1] = state[:interior]
        velocity = state[interior:]
        acceleration = radial_laplacian_2d(field, spacing)[:-1] - np.sin(
            field[:-1]
        )
        return np.concatenate((velocity, acceleration))

    solution = solve_ivp(
        rhs,
        (0.0, final_time),
        state0,
        method="DOP853",
        t_eval=sample_time,
        rtol=2.0e-8,
        atol=2.0e-10,
        max_step=0.1,
    )
    if not solution.success:
        raise RuntimeError(f"SciPy evolution failed: {solution.message}")
    fields = np.zeros((solution.t.size, radius.size))
    velocities = np.zeros_like(fields)
    fields[:, :-1] = solution.y[:interior].T
    velocities[:, :-1] = solution.y[interior:].T
    return _diagnostics(
        "DOP853-method-of-lines",
        solution.t,
        fields,
        velocities,
        radius,
        core_radius,
    )


def run() -> ReplacementResult:
    parameters = {
        "amplitude": 3.0,
        "width": 4.0,
        "spacing": 0.25,
        "outer_radius": 60.0,
        "final_time": 30.0,
        "core_radius": 15.0,
        "sample_interval": 0.25,
    }
    leapfrog = evolve_leapfrog(**parameters)
    mol = evolve_mol(**parameters)
    refined_parameters = dict(parameters)
    refined_parameters["spacing"] = 0.2
    refined = evolve_leapfrog(**refined_parameters)

    late_start = 0.75 * parameters["final_time"]
    leapfrog_late = leapfrog.time >= late_start
    mol_late = mol.time >= late_start
    leapfrog_fraction = float(
        np.min(leapfrog.core_energy[leapfrog_late]) / leapfrog.total_energy[0]
    )
    mol_fraction = float(
        np.min(mol.core_energy[mol_late]) / mol.total_energy[0]
    )
    refined_late = refined.time >= late_start
    refined_fraction = float(
        np.min(refined.core_energy[refined_late]) / refined.total_energy[0]
    )
    refinement_difference = abs(refined_fraction - leapfrog_fraction)
    leapfrog_drift = float(
        np.max(np.abs(leapfrog.total_energy / leapfrog.total_energy[0] - 1.0))
    )
    mol_drift = float(
        np.max(np.abs(mol.total_energy / mol.total_energy[0] - 1.0))
    )

    leapfrog_center = np.interp(mol.time, leapfrog.time, leapfrog.center)
    leapfrog_core = np.interp(mol.time, leapfrog.time, leapfrog.core_energy)
    center_scale = max(float(np.std(mol.center)), 1.0e-12)
    center_rms = float(
        np.sqrt(np.mean(np.square(leapfrog_center - mol.center)))
        / center_scale
    )
    core_relative_max = float(
        np.max(np.abs(leapfrog_core - mol.core_energy))
        / np.mean(mol.core_energy)
    )
    passed = bool(
        leapfrog_fraction > 0.75
        and mol_fraction > 0.75
        and refined_fraction > 0.75
        and refinement_difference < 0.005
        and leapfrog_drift < 0.01
        and mol_drift < 0.01
        and center_rms < 0.03
        and core_relative_max < 0.01
    )
    return ReplacementResult(
        claim="P238-S06",
        revised_claim=(
            "For U(u)=1-cos(u) and the declared Gaussian initial data, the "
            "real radial 2+1D NLKG has a finite-time localized trajectory "
            "through t=30, reproduced by leapfrog and SciPy DOP853."
        ),
        passed=passed,
        leapfrog_late_core_fraction=leapfrog_fraction,
        mol_late_core_fraction=mol_fraction,
        refined_late_core_fraction=refined_fraction,
        refinement_difference=refinement_difference,
        leapfrog_energy_drift=leapfrog_drift,
        mol_energy_drift=mol_drift,
        center_relative_rms=center_rms,
        core_relative_max=core_relative_max,
        parameters=parameters,
    )


def main() -> int:
    result = run()
    print(json.dumps(asdict(result), indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
