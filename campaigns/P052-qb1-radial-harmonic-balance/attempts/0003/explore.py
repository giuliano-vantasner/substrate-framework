"""Continuation-safe finite-box audit of QB1 harmonic balance."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_bvp


@dataclass(frozen=True)
class Stage:
    harmonics: tuple[int, ...]
    solution: object


def projection(
    amplitudes: np.ndarray,
    input_harmonics: tuple[int, ...],
    targets: tuple[int, ...],
    samples: int,
) -> np.ndarray:
    tau = 2.0 * np.pi * np.arange(samples, dtype=float) / samples
    input_basis = np.cos(np.outer(input_harmonics, tau))
    target_basis = np.cos(np.outer(targets, tau))
    field = input_basis.T @ amplitudes
    return (2.0 / samples) * target_basis @ np.sin(field)


def solve_stage(
    harmonics: tuple[int, ...],
    *,
    amplitude: float,
    radius: float,
    frequency_guess: float,
    temporal_samples: int,
    tolerance: float,
    previous: Stage | None = None,
    fundamental_robin: bool = False,
    corrected_origin: bool = False,
) -> Stage:
    epsilon = 1.0e-3
    if previous is None:
        mesh = np.linspace(epsilon, radius, 400)
        state = np.zeros((2 * len(harmonics), mesh.size))
        inverse_width = np.sqrt(max(1.0 - frequency_guess**2, 1.0e-3))
        state[0] = amplitude * np.exp(-inverse_width * mesh)
        state[1] = -amplitude * inverse_width * np.exp(-inverse_width * mesh)
        parameter = [frequency_guess]
    else:
        mesh = previous.solution.x
        state = np.zeros((2 * len(harmonics), mesh.size))
        for old_index, old_harmonic in enumerate(previous.harmonics):
            new_index = harmonics.index(old_harmonic)
            state[2 * new_index : 2 * new_index + 2] = previous.solution.y[
                2 * old_index : 2 * old_index + 2
            ]
        parameter = previous.solution.p

    def equations(coordinate, values, fitted):
        frequency = float(fitted[0])
        amplitudes = values[0::2]
        nonlinear = projection(
            amplitudes,
            harmonics,
            harmonics,
            temporal_samples,
        )
        derivatives = np.empty_like(values)
        derivatives[0::2] = values[1::2]
        for index, harmonic in enumerate(harmonics):
            derivatives[2 * index + 1] = (
                -2.0 * values[2 * index + 1] / coordinate
                - (harmonic * frequency) ** 2 * values[2 * index]
                + nonlinear[index]
            )
        return derivatives

    def boundary(left, right, fitted):
        frequency = float(fitted[0])
        residuals: list[float] = []
        if corrected_origin:
            nonlinear_left = projection(
                left[0::2, None], harmonics, harmonics, temporal_samples
            )[:, 0]
            for index, harmonic in enumerate(harmonics):
                curvature = (
                    nonlinear_left[index]
                    - (harmonic * frequency) ** 2 * left[2 * index]
                ) / 3.0
                residuals.append(left[2 * index + 1] - epsilon * curvature)
        else:
            residuals.extend(float(value) for value in left[1::2])
        for index, _harmonic in enumerate(harmonics):
            if index == 0 and fundamental_robin:
                if not 0.0 < frequency < 1.0:
                    return np.full(2 * len(harmonics) + 1, 1.0e6)
                inverse_width = np.sqrt(1.0 - frequency**2)
                residuals.append(
                    right[1] + (inverse_width + 1.0 / radius) * right[0]
                )
            else:
                residuals.append(right[2 * index])
        if corrected_origin:
            residuals.append(left[0] - 0.5 * epsilon * left[1] - amplitude)
        else:
            residuals.append(left[0] - amplitude)
        return np.asarray(residuals)

    solution = solve_bvp(
        equations,
        boundary,
        mesh,
        state,
        p=parameter,
        tol=tolerance,
        max_nodes=50_000,
    )
    return Stage(harmonics=harmonics, solution=solution)


def solve_ladder(
    radius: float,
    *,
    temporal_samples: int = 96,
    tolerance: float = 1.0e-7,
) -> tuple[Stage, Stage, Stage]:
    common = dict(
        amplitude=2.5,
        radius=radius,
        temporal_samples=temporal_samples,
        tolerance=tolerance,
    )
    one = solve_stage((1,), frequency_guess=0.9769, **common)
    if not one.solution.success or not 0.0 < one.solution.p[0] < 1.0:
        return one, one, one
    three = solve_stage(
        (1, 3), frequency_guess=float(one.solution.p[0]), previous=one, **common
    )
    if not three.solution.success or not 0.0 < three.solution.p[0] < 1.0:
        return one, three, three
    five = solve_stage(
        (1, 3, 5),
        frequency_guess=float(three.solution.p[0]),
        previous=three,
        **common,
    )
    return one, three, five


def metrics(stage: Stage, radius: float, samples: int = 768) -> dict:
    solution = stage.solution
    result = {
        "success": bool(solution.success),
        "omega": float(solution.p[0]),
        "nodes": int(solution.x.size),
        "max_collocation_rms": float(np.max(solution.rms_residuals)),
    }
    if not solution.success:
        return result
    dense_radius = np.linspace(1.0e-3, radius, 2401)
    state = solution.sol(dense_radius)
    amplitudes = state[0::2]
    omitted = projection(amplitudes, stage.harmonics, (7,), samples)[0]
    tail = dense_radius >= 0.75 * radius
    result.update(
        max_amplitudes=[float(np.max(np.abs(row))) for row in amplitudes],
        tail_r_amplitude_rms=[
            float(np.sqrt(np.mean((dense_radius[tail] * row[tail]) ** 2)))
            for row in amplitudes
        ],
        omitted_7_core_rms=float(
            np.sqrt(np.mean(omitted[dense_radius <= 12.0] ** 2))
        ),
        channels=[
            "evanescent" if harmonic * solution.p[0] < 1.0 else "radiative"
            for harmonic in stage.harmonics
        ],
    )
    return result


def main() -> None:
    ladders: dict[float, tuple[Stage, Stage, Stage]] = {}
    for radius in (30.0, 40.0, 50.0, 60.0):
        ladder = solve_ladder(radius)
        ladders[radius] = ladder
        print(
            "BOX",
            radius,
            [metrics(stage, radius) for stage in ladder],
        )

    baseline = ladders[40.0][2]
    dense_time = solve_stage(
        (1, 3, 5),
        amplitude=2.5,
        radius=40.0,
        frequency_guess=float(baseline.solution.p[0]),
        temporal_samples=192,
        tolerance=1.0e-7,
        previous=baseline,
    )
    tight = solve_stage(
        (1, 3, 5),
        amplitude=2.5,
        radius=40.0,
        frequency_guess=float(dense_time.solution.p[0]),
        temporal_samples=192,
        tolerance=1.0e-8,
        previous=dense_time,
    )
    robin = solve_stage(
        (1, 3, 5),
        amplitude=2.5,
        radius=40.0,
        frequency_guess=float(tight.solution.p[0]),
        temporal_samples=192,
        tolerance=1.0e-8,
        previous=tight,
        fundamental_robin=True,
        corrected_origin=True,
    )
    print("TIME_192", metrics(dense_time, 40.0))
    print("TIGHT", metrics(tight, 40.0))
    print("ROBIN_CORRECTED", metrics(robin, 40.0))


if __name__ == "__main__":
    main()
