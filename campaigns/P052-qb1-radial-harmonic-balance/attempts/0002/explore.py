"""Independent P052 exploration of finite-box harmonic balance."""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_bvp


def sine_projections(
    amplitudes: np.ndarray,
    harmonics: tuple[int, ...],
    samples: int,
) -> np.ndarray:
    tau = 2.0 * np.pi * np.arange(samples, dtype=float) / samples
    basis = np.cos(np.outer(np.asarray(harmonics, dtype=float), tau))
    field = basis.T @ amplitudes
    return (2.0 / samples) * basis @ np.sin(field)


def target_projections(
    amplitudes: np.ndarray,
    input_harmonics: tuple[int, ...],
    target_harmonics: tuple[int, ...],
    samples: int,
) -> np.ndarray:
    tau = 2.0 * np.pi * np.arange(samples, dtype=float) / samples
    input_basis = np.cos(np.outer(np.asarray(input_harmonics, dtype=float), tau))
    target_basis = np.cos(np.outer(np.asarray(target_harmonics, dtype=float), tau))
    field = input_basis.T @ amplitudes
    return (2.0 / samples) * target_basis @ np.sin(field)


def solve_balance(
    harmonics: tuple[int, ...],
    *,
    amplitude: float,
    outer_radius: float,
    frequency_guess: float,
    temporal_samples: int = 192,
    mesh_points: int = 400,
    tolerance: float = 1.0e-7,
    source_wall: bool = False,
):
    count = len(harmonics)
    epsilon = 1.0e-3
    radius = np.linspace(epsilon, outer_radius, mesh_points)
    inverse_width = np.sqrt(max(1.0 - frequency_guess**2, 1.0e-3))
    state = np.zeros((2 * count, radius.size))
    seed = amplitude * (1.0 + inverse_width * radius) * np.exp(
        -inverse_width * radius
    )
    state[0] = seed
    state[1] = -amplitude * inverse_width**2 * radius * np.exp(
        -inverse_width * radius
    )

    def equations(r: np.ndarray, values: np.ndarray, parameter: np.ndarray):
        frequency = float(parameter[0])
        amplitudes = values[0::2]
        projections = sine_projections(
            amplitudes, harmonics, temporal_samples
        )
        derivative = np.empty_like(values)
        derivative[0::2] = values[1::2]
        for index, harmonic in enumerate(harmonics):
            derivative[2 * index + 1] = (
                -2.0 * values[2 * index + 1] / r
                - (harmonic * frequency) ** 2 * values[2 * index]
                + projections[index]
            )
        return derivative

    def boundary(left: np.ndarray, right: np.ndarray, parameter: np.ndarray):
        frequency = float(parameter[0])
        projected_left = sine_projections(
            left[0::2, None], harmonics, temporal_samples
        )[:, 0]
        residuals = []
        for index, harmonic in enumerate(harmonics):
            curvature = (
                projected_left[index]
                - (harmonic * frequency) ** 2 * left[2 * index]
            ) / 3.0
            residuals.append(left[2 * index + 1] - epsilon * curvature)
        for index, harmonic in enumerate(harmonics):
            if index == 0 and not source_wall:
                inverse_width = np.sqrt(max(1.0 - frequency**2, 1.0e-14))
                residuals.append(
                    right[1]
                    + (inverse_width + 1.0 / outer_radius) * right[0]
                )
            else:
                residuals.append(right[2 * index])
        residuals.append(left[0] - 0.5 * epsilon * left[1] - amplitude)
        return np.asarray(residuals)

    return solve_bvp(
        equations,
        boundary,
        radius,
        state,
        p=[frequency_guess],
        tol=tolerance,
        max_nodes=50_000,
    )


def summarize(solution, harmonics: tuple[int, ...], outer_radius: float) -> dict:
    dense_radius = np.linspace(1.0e-3, outer_radius, 2401)
    state = solution.sol(dense_radius)
    amplitudes = state[0::2]
    frequency = float(solution.p[0])
    projections = sine_projections(amplitudes, harmonics, 768)
    omitted = target_projections(amplitudes, harmonics, (7,), 768)[0]
    tail = dense_radius >= 0.75 * outer_radius
    result = {
        "success": bool(solution.success),
        "omega": frequency,
        "nodes": int(solution.x.size),
        "max_collocation_rms": float(np.max(solution.rms_residuals)),
        "max_amplitudes": [float(np.max(np.abs(row))) for row in amplitudes],
        "omitted_7_core_rms": float(
            np.sqrt(np.mean(omitted[dense_radius <= 12.0] ** 2))
        ),
        "tail_r_times_amplitude_rms": [
            float(np.sqrt(np.mean((dense_radius[tail] * row[tail]) ** 2)))
            for row in amplitudes
        ],
        "channels": [
            "evanescent" if harmonic * frequency < 1.0 else "radiative"
            for harmonic in harmonics
        ],
    }
    # Reconstruct second derivatives independently from dense output values,
    # rather than recycling the collocation right-hand side.
    projected_equation_rms = []
    spacing = float(dense_radius[1] - dense_radius[0])
    for index, harmonic in enumerate(harmonics):
        independent_second = np.gradient(
            np.gradient(amplitudes[index], spacing, edge_order=2),
            spacing,
            edge_order=2,
        )
        residual = (
            independent_second
            + 2.0 * state[2 * index + 1] / dense_radius
            + (harmonic * frequency) ** 2 * amplitudes[index]
            - projections[index]
        )
        projected_equation_rms.append(
            float(np.sqrt(np.mean(residual[3:-3] ** 2)))
        )
    result["projected_equation_rms"] = projected_equation_rms
    return result


def main() -> None:
    amplitude = 2.5
    single = {}
    for radius in (20.0, 30.0, 40.0, 60.0):
        solution = solve_balance(
            (1,),
            amplitude=amplitude,
            outer_radius=radius,
            frequency_guess=0.9769,
        )
        single[str(int(radius))] = summarize(solution, (1,), radius)
    print("SINGLE_ROBIN", single)

    boxes = {}
    for radius in (30.0, 40.0, 50.0, 60.0):
        solution = solve_balance(
            (1, 3, 5),
            amplitude=amplitude,
            outer_radius=radius,
            frequency_guess=single["40"]["omega"],
            source_wall=True,
        )
        boxes[str(int(radius))] = summarize(solution, (1, 3, 5), radius)
    print("MULTI_SOURCE_WALL", boxes)

    corrected = solve_balance(
        (1, 3, 5),
        amplitude=amplitude,
        outer_radius=40.0,
        frequency_guess=single["40"]["omega"],
        source_wall=False,
    )
    print("MULTI_FUNDAMENTAL_ROBIN", summarize(corrected, (1, 3, 5), 40.0))


if __name__ == "__main__":
    main()
