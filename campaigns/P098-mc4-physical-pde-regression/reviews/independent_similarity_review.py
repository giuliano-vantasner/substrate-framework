"""Independent physical-coordinate similarity audit for P098.

This review deliberately imports neither the canonical sine-Gordon physics
modules nor the canonical periodic solver. It rederives the physical update,
scale-covariant energy/width diagnostics, and gapless traveling-wave control.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.numerics import trapezoid_integral
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class PhysicalEvolution:
    coordinate: np.ndarray
    field: np.ndarray
    velocity: np.ndarray
    initial_energy: float
    final_energy: float
    ell: float
    signal_speed: float
    physical_time_step: float
    normalized_time_step: float


def _periodic_acceleration(
    field: np.ndarray,
    spatial_step: float,
    signal_speed: float,
    ell: float,
    onsite_factor: float,
) -> np.ndarray:
    laplacian = (
        np.roll(field, -1) - 2.0 * field + np.roll(field, 1)
    ) / spatial_step**2
    return signal_speed**2 * laplacian - onsite_factor * (
        signal_speed / ell
    ) ** 2 * np.sin(field)


def _periodic_energy(
    field: np.ndarray,
    velocity: np.ndarray,
    spatial_step: float,
    signal_speed: float,
    ell: float,
) -> float:
    edge_derivative = (np.roll(field, -1) - field) / spatial_step
    density = (
        np.square(velocity) / (2.0 * signal_speed**2)
        + 0.5 * np.square(edge_derivative)
        + (1.0 - np.cos(field)) / ell**2
    )
    return float(spatial_step * np.sum(density))


def _physical_evolution(
    *,
    ell: float,
    signal_speed: float = 1.0,
    frequency_ratio: float = 0.7,
    normalized_half_width: float = 20.0,
    normalized_spatial_step: float = 0.1,
    normalized_final_time: float = 3.7,
    requested_normalized_time_step: float = 0.04,
    onsite_factor: float = 1.0,
    initial_velocity_factor: float = 1.0,
) -> PhysicalEvolution:
    normalized_coordinate = np.arange(
        -normalized_half_width,
        normalized_half_width,
        normalized_spatial_step,
        dtype=np.float64,
    )
    coordinate = ell * normalized_coordinate
    spatial_step = ell * normalized_spatial_step
    steps = int(np.ceil(normalized_final_time / requested_normalized_time_step))
    normalized_time_step = normalized_final_time / steps
    physical_time_step = ell * normalized_time_step / signal_speed
    inverse_width = np.sqrt(1.0 - frequency_ratio**2)
    field = np.zeros_like(coordinate)
    velocity = initial_velocity_factor * (
        signal_speed
        / ell
        * 4.0
        * inverse_width
        / np.cosh(inverse_width * normalized_coordinate)
    )
    initial_energy = _periodic_energy(
        field,
        velocity,
        spatial_step,
        signal_speed,
        ell,
    )
    acceleration = _periodic_acceleration(
        field,
        spatial_step,
        signal_speed,
        ell,
        onsite_factor,
    )
    half_velocity = velocity + 0.5 * physical_time_step * acceleration
    for _ in range(steps):
        field = field + physical_time_step * half_velocity
        acceleration = _periodic_acceleration(
            field,
            spatial_step,
            signal_speed,
            ell,
            onsite_factor,
        )
        velocity = half_velocity + 0.5 * physical_time_step * acceleration
        half_velocity = half_velocity + physical_time_step * acceleration
    final_energy = _periodic_energy(
        field,
        velocity,
        spatial_step,
        signal_speed,
        ell,
    )
    return PhysicalEvolution(
        coordinate=coordinate,
        field=field,
        velocity=velocity,
        initial_energy=initial_energy,
        final_energy=final_energy,
        ell=ell,
        signal_speed=signal_speed,
        physical_time_step=physical_time_step,
        normalized_time_step=normalized_time_step,
    )


def _centered_derivative(field: np.ndarray, coordinate: np.ndarray) -> np.ndarray:
    spatial_step = float(coordinate[1] - coordinate[0])
    return (
        np.roll(field, -1) - np.roll(field, 1)
    ) / (2.0 * spatial_step)


def _rms_width(evolution: PhysicalEvolution, *, source_proxy: bool) -> float:
    coordinate = evolution.coordinate
    derivative = _centered_derivative(evolution.field, coordinate)
    if source_proxy:
        weight = np.square(derivative) + 1.0 - np.cos(evolution.field)
    else:
        weight = (
            np.square(evolution.velocity) / (2.0 * evolution.signal_speed**2)
            + 0.5 * np.square(derivative)
            + (1.0 - np.cos(evolution.field)) / evolution.ell**2
        )
    total = trapezoid_integral(weight, coordinate)
    center = trapezoid_integral(coordinate * weight, coordinate) / total
    variance = trapezoid_integral(
        np.square(coordinate - center) * weight,
        coordinate,
    ) / total
    return float(np.sqrt(variance))


def main() -> int:
    checks = CheckLedger("P098-INDEPENDENT")
    ell_one = _physical_evolution(ell=1.0)
    ell_two = _physical_evolution(ell=2.0)

    checks.check(
        "scaled physical grids represent the same normalized coordinate",
        np.max(np.abs(ell_one.coordinate - ell_two.coordinate / 2.0)) < 1.0e-13,
    )
    checks.check(
        "physical timesteps scale with ell at fixed normalized step",
        abs(ell_two.physical_time_step / ell_one.physical_time_step - 2.0)
        < 1.0e-14
        and ell_one.normalized_time_step == ell_two.normalized_time_step,
    )
    checks.check(
        "independent physical leapfrog trajectories are exactly similar",
        np.max(np.abs(ell_one.field - ell_two.field)) < 2.0e-13,
    )
    checks.check(
        "normalized velocities are exactly similar",
        np.max(
            np.abs(
                ell_one.ell / ell_one.signal_speed * ell_one.velocity
                - ell_two.ell / ell_two.signal_speed * ell_two.velocity
            )
        )
        < 2.0e-13,
    )
    checks.check(
        "source-normalized physical energy scales as inverse ell",
        abs(ell_one.initial_energy / ell_two.initial_energy - 2.0) < 2.0e-13
        and abs(ell_one.final_energy / ell_two.final_energy - 2.0) < 2.0e-13,
    )

    covariant_width_one = _rms_width(ell_one, source_proxy=False)
    covariant_width_two = _rms_width(ell_two, source_proxy=False)
    source_width_one = _rms_width(ell_one, source_proxy=True)
    source_width_two = _rms_width(ell_two, source_proxy=True)
    covariant_ratio = covariant_width_two / covariant_width_one
    source_ratio = source_width_two / source_width_one
    print("P098 independent covariant width ratio:", covariant_ratio)
    print("P098 independent source-proxy width ratio:", source_ratio)
    checks.check(
        "scale-covariant Hamiltonian width scales exactly with ell",
        abs(covariant_ratio - 2.0) < 2.0e-13,
    )
    checks.check(
        "source mixed-unit width proxy breaks the exact ratio",
        abs(source_ratio - 2.0) > 1.0e-3,
    )

    wrong_curvature = _physical_evolution(ell=2.0, onsite_factor=4.0)
    checks.check(
        "wrong onsite scaling breaks physical similarity",
        np.max(np.abs(wrong_curvature.field - ell_one.field)) > 1.0e-2,
    )
    wrong_velocity = _physical_evolution(ell=2.0, initial_velocity_factor=2.0)
    checks.check(
        "omitting the inverse-ell initial-velocity factor breaks similarity",
        np.max(np.abs(wrong_velocity.field - ell_one.field)) > 1.0e-2,
    )

    sample_count = 625
    sample_spacing_one = 0.16
    sample_spacing_two = 0.32
    fft_step_one = 2.0 * np.pi / (sample_count * sample_spacing_one)
    fft_step_two = 2.0 * np.pi / (sample_count * sample_spacing_two)
    source_bin_one = 11.0 * fft_step_one
    source_bin_two = 11.0 * fft_step_two
    checks.check(
        "source frequencies are the nearest eleventh FFT bins",
        abs(source_bin_one - 0.6911503837897545) < 1.0e-14
        and abs(source_bin_two - 0.34557519189487723) < 1.0e-14,
    )
    checks.check(
        "source frequency accuracy is resolution bounded",
        abs(0.7 - source_bin_one) < 0.5 * fft_step_one
        and abs(0.35 - source_bin_two) < 0.5 * fft_step_two,
    )
    checks.check(
        "ell-two FFT output is a rescaled copy of ell-one output",
        abs(source_bin_one / source_bin_two - 2.0) < 1.0e-14,
    )

    x, t, c = sp.symbols("x t c", real=True, positive=True)
    traveling_packet = sp.sech(x - c * t)
    wave_residual = sp.diff(traveling_packet, t, 2) - c**2 * sp.diff(
        traveling_packet,
        x,
        2,
    )
    packet_energy_at_zero = sp.simplify(
        (
            sp.diff(traveling_packet, t) ** 2 / (2 * c**2)
            + sp.diff(traveling_packet, x) ** 2 / 2
        ).subs(t, 0)
    )
    packet_energy_primitive = sp.tanh(x) ** 3 / 3
    checks.check(
        "independent d'Alembert packet solves the gapless equation",
        sp.simplify(wave_residual) == 0,
    )
    checks.check(
        "gapless traveling packet has finite positive energy",
        sp.simplify(
            sp.diff(packet_energy_primitive, x) - packet_energy_at_zero
        )
        == 0
        and sp.limit(packet_energy_primitive, x, sp.oo)
        - sp.limit(packet_energy_primitive, x, -sp.oo)
        == sp.Rational(2, 3),
    )
    checks.check(
        "fixed-core drainage cannot imply universal gapless delocalization",
        traveling_packet.subs(x, c * t) == 1,
    )

    verifier_text = Path(__file__).read_text(encoding="utf-8")
    verifier_tree = ast.parse(verifier_text)
    direct_numpy_integrals = [
        node
        for node in ast.walk(verifier_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
        and node.func.attr in {"trapz", "trapezoid"}
    ]
    checks.check(
        "independent sampled integrals use the shared compatibility API",
        not direct_numpy_integrals,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
