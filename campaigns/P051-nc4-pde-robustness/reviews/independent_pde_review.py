#!/usr/bin/env python3
"""Independent spectral and direct-solve_ivp review for P051."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp, trapezoid

from substrate_framework import CheckLedger


def breather_samples(
    coordinate: np.ndarray,
    time: float,
    omega: float,
    speed: float,
    center: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Independently evaluate the Lorentz-boosted breather and time derivative."""

    eta = np.sqrt(1.0 - omega**2)
    gamma = 1.0 / np.sqrt(1.0 - speed**2)
    xi = gamma * (coordinate - center - speed * time)
    tau = gamma * (time - speed * (coordinate - center))
    numerator = eta * np.sin(omega * tau)
    denominator = omega * np.cosh(eta * xi)
    normalization = numerator**2 + denominator**2
    field = 4.0 * np.arctan2(numerator, denominator)
    numerator_t = eta * omega * np.cos(omega * tau) * gamma
    denominator_t = omega * eta * np.sinh(eta * xi) * (-gamma * speed)
    velocity = 4.0 * (
        denominator * numerator_t - numerator * denominator_t
    ) / normalization
    return field, velocity


def spectral_reference() -> tuple[float, float]:
    """Evolve a rest breather with a Fourier spatial operator."""

    point_count = 384
    coordinate = np.linspace(-30.0, 30.0, point_count, endpoint=False)
    spacing = coordinate[1] - coordinate[0]
    wave_numbers = 2.0 * np.pi * np.fft.fftfreq(point_count, d=spacing)
    field0, velocity0 = breather_samples(coordinate, 0.0, 0.6, 0.0, 0.0)

    def rhs(_time: float, state: np.ndarray) -> np.ndarray:
        field = state[:point_count]
        velocity = state[point_count:]
        laplacian = np.fft.ifft(-wave_numbers**2 * np.fft.fft(field)).real
        return np.concatenate((velocity, laplacian - np.sin(field)))

    result = solve_ivp(
        rhs,
        (0.0, 2.0),
        np.concatenate((field0, velocity0)),
        method="DOP853",
        rtol=1.0e-11,
        atol=1.0e-13,
        max_step=0.02,
    )
    if not result.success:
        raise RuntimeError(result.message)
    exact_field, exact_velocity = breather_samples(
        coordinate,
        2.0,
        0.6,
        0.0,
        0.0,
    )
    field_error = float(
        np.sqrt(np.mean((result.y[:point_count, -1] - exact_field) ** 2))
    )
    velocity_error = float(
        np.sqrt(np.mean((result.y[point_count:, -1] - exact_velocity) ** 2))
    )
    return field_error, velocity_error


def source_parameters(omega: float) -> dict[str, float]:
    eta = np.sqrt(1.0 - omega**2)
    speed = 0.3
    center = 35.0
    impact = center / speed
    width = 1.0 / (speed * eta)
    final = impact + 3.0 * width + 20.0
    gap = 16.0 * (1.0 - eta)
    _, impact_velocity = breather_samples(
        np.asarray([0.0]), impact, omega, -speed, center
    )
    amplitude = gap * np.pi / (2.0 * abs(impact_velocity[0]) * width)
    return {
        "speed": speed,
        "center": center,
        "impact": impact,
        "width": width,
        "final": final,
        "amplitude": float(amplitude),
    }


def direct_driven_case(
    omega: float,
    orientation: int,
    scale: float,
    phase: float,
    *,
    intervals: int = 300,
) -> tuple[float, float]:
    """Direct solve_ivp implementation independent of package evolution APIs."""

    parameters = source_parameters(omega)
    coordinate = np.linspace(0.0, 60.0, intervals + 1)
    spacing = coordinate[1] - coordinate[0]
    point_count = coordinate.size
    field0, velocity0 = breather_samples(
        coordinate,
        0.0,
        omega,
        -parameters["speed"],
        parameters["center"],
    )

    def drive(time: float) -> float:
        envelope = np.exp(
            -0.5 * ((time - parameters["impact"]) / parameters["width"]) ** 2
        )
        return float(
            orientation
            * scale
            * parameters["amplitude"]
            * envelope
            * np.sin(omega * (time - parameters["impact"]) + phase)
        )

    def rhs(time: float, state: np.ndarray) -> np.ndarray:
        field = state[:point_count]
        velocity = state[point_count:]
        acceleration = np.empty_like(field)
        acceleration[1:-1] = (
            (field[2:] - 2.0 * field[1:-1] + field[:-2]) / spacing**2
            - np.sin(field[1:-1])
        )
        acceleration[0] = (
            2.0 * (field[1] - field[0]) / spacing**2
            - 2.0 * drive(time) / spacing
            - np.sin(field[0])
        )
        acceleration[-1] = -(velocity[-1] - velocity[-2]) / spacing
        return np.concatenate((velocity, acceleration))

    samples = np.linspace(
        0.0,
        parameters["final"],
        int(np.ceil(parameters["final"] / 0.1)) + 1,
    )
    result = solve_ivp(
        rhs,
        (0.0, parameters["final"]),
        np.concatenate((field0, velocity0)),
        method="DOP853",
        t_eval=samples,
        rtol=1.0e-8,
        atol=1.0e-10,
        max_step=0.1,
    )
    if not result.success or not np.all(np.isfinite(result.y)):
        raise RuntimeError(result.message)
    final_field = result.y[:point_count, -1]
    bulk_index = int(np.searchsorted(coordinate, 10.0, side="left"))
    endpoint_coordinate = float(
        (final_field[-1] - final_field[bulk_index]) / (2.0 * np.pi)
    )
    boundary_velocity = result.y[point_count]
    derivative = np.asarray([drive(time) for time in samples])
    window = (
        (samples > parameters["impact"] - 2.0 * parameters["width"])
        & (samples < parameters["impact"] + 2.0 * parameters["width"])
    )
    selected = np.where(window)[0][1:-1]
    correlation = float(
        trapezoid(
            np.sign(boundary_velocity[selected]) * derivative[selected],
            samples[selected],
        )
    )
    return endpoint_coordinate, correlation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    arguments = parser.parse_args()
    source = arguments.source_file.read_text(encoding="utf-8")
    ledger = CheckLedger("P051-INDEPENDENT")

    field_error, velocity_error = spectral_reference()
    ledger.check(
        "a Fourier spatial method independently evolves the exact nonlinear breather",
        field_error < 2.0e-9 and velocity_error < 2.0e-9,
    )

    q_plus, _ = direct_driven_case(0.6, 1, 1.0, 5.50)
    q_minus, _ = direct_driven_case(0.6, -1, 1.0, 5.50)
    ledger.check(
        "direct solve_ivp independently recovers the tuned w=0.6 endpoint response",
        q_plus - q_minus < -1.0,
    )
    _, wq_plus = direct_driven_case(0.6, 1, 0.15, 5.50)
    _, wq_minus = direct_driven_case(0.6, -1, 0.15, 5.50)
    ledger.check(
        "the independent diagnostic route recovers opposite tuned correlations",
        wq_plus > 0.0 and wq_minus < 0.0,
    )

    q08_plus, _ = direct_driven_case(0.8, 1, 1.0, 5.50)
    q08_minus, _ = direct_driven_case(0.8, -1, 1.0, 5.50)
    ledger.check(
        "the common-phase w=0.8 response independently reverses the sweep sign",
        q08_plus - q08_minus > 1.0,
    )

    parameters = source_parameters(0.6)
    times = np.linspace(parameters["impact"] - 1.0, parameters["impact"] + 1.0, 51)

    def drive(orientation: int, phase: float) -> np.ndarray:
        envelope = np.exp(
            -0.5 * ((times - parameters["impact"]) / parameters["width"]) ** 2
        )
        return (
            orientation
            * parameters["amplitude"]
            * envelope
            * np.sin(0.6 * (times - parameters["impact"]) + phase)
        )

    ledger.check(
        "a phase shift by pi independently swaps the declared orientation labels",
        np.allclose(drive(1, 5.50 + np.pi), drive(-1, 5.50), atol=2.0e-15),
    )
    ledger.check(
        "the source amplitude sweep changes more than field amplitude",
        "PHASES = {0.2: 5.50, 0.4: 0.79, 0.6: 5.50, 0.8: 4.71}" in source
        and "DeltaE" in source
        and "T_int" in source,
    )
    ledger.check(
        "the zero-drive guard is an identical-input identity",
        "scale=0.0" in source and "F0 = scale" in source,
    )
    ledger.check(
        "the source's fractional endpoint result is not integer winding",
        abs(-0.572 - round(-0.572)) > 0.1,
    )
    ledger.check(
        "source dQ and W_Q do not come from one declared drive experiment",
        "DIAG_SCALE = 0.15" in source and "FULL_SCALE = 1.0" in source,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
