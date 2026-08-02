"""Independent Gauss-projection and shooting review for P052."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import yaml
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_bvp, solve_ivp
from scipy.optimize import least_squares
from scipy.sparse import lil_matrix
from scipy.special import jv

from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "1f387c140ca80be0e457efd17146267bdecab1cbdbcdd10dd34287bc5de2dc7a"


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _shooting_frequency(amplitude: float, iterations: int = 38) -> float:
    def classify(frequency: float) -> int:
        inverse_width = np.sqrt(1.0 - frequency**2)
        outer = max(160.0, 22.0 / inverse_width)
        epsilon = 1.0e-4
        curvature = (-frequency**2 * amplitude + 2.0 * jv(1, amplitude)) / 3.0

        def equations(radius, state):
            return np.array(
                [
                    state[1],
                    -2.0 * state[1] / radius
                    - frequency**2 * state[0]
                    + 2.0 * jv(1, state[0]),
                ]
            )

        def zero(_radius, state):
            return state[0]

        def large(_radius, state):
            return state[0] - 2.0 * amplitude

        zero.terminal = True
        zero.direction = -1
        large.terminal = True
        large.direction = 1
        result = solve_ivp(
            equations,
            (epsilon, outer),
            [amplitude + 0.5 * curvature * epsilon**2, curvature * epsilon],
            method="DOP853",
            rtol=2.0e-10,
            atol=2.0e-12,
            events=(zero, large),
        )
        if not result.success or not np.all(np.isfinite(result.y)):
            raise RuntimeError("independent shooting integration failed")
        zero_time = result.t_events[0][0] if result.t_events[0].size else np.inf
        large_time = result.t_events[1][0] if result.t_events[1].size else np.inf
        if large_time < zero_time:
            return 1
        if zero_time < large_time:
            return -1
        return 1 if result.t[-1] * result.y[0, -1] > 0.0 else -1

    lower, upper = 0.8, 0.9995
    lower_sign, upper_sign = classify(lower), classify(upper)
    if lower_sign == upper_sign:
        raise RuntimeError("independent shooting bracket has no sign change")
    for _ in range(iterations):
        midpoint = 0.5 * (lower + upper)
        if classify(midpoint) == lower_sign:
            lower = midpoint
        else:
            upper = midpoint
    return 0.5 * (lower + upper)


def _gauss_solution(harmonics, amplitude, frequency_guess, previous=None):
    modes = tuple(harmonics)
    epsilon = 1.0e-3
    outer = 40.0
    nodes, weights = leggauss(96)
    tau = np.pi * (nodes + 1.0)
    basis = np.cos(np.outer(np.asarray(modes, dtype=float), tau))

    def project(coefficients):
        field = basis.T @ coefficients
        return basis @ (weights[:, None] * np.sin(field))

    if previous is None:
        radius = np.linspace(epsilon, outer, 360)
        state = np.zeros((2 * len(modes), radius.size))
        inverse_width = np.sqrt(1.0 - frequency_guess**2)
        state[0] = amplitude * np.exp(-inverse_width * radius)
        state[1] = -inverse_width * state[0]
    else:
        radius = previous.x
        state = np.zeros((2 * len(modes), radius.size))
        previous_modes = tuple(range(1, previous.y.shape[0], 2))
        # Previous solves are always the prefix (1), (1,3), ...; copy by row.
        state[: previous.y.shape[0]] = previous.y
        del previous_modes

    def equations(coordinate, values, parameter):
        frequency = float(parameter[0])
        nonlinear = project(values[0::2])
        derivative = np.empty_like(values)
        derivative[0::2] = values[1::2]
        for index, harmonic in enumerate(modes):
            derivative[2 * index + 1] = (
                -2.0 * values[2 * index + 1] / coordinate
                - (harmonic * frequency) ** 2 * values[2 * index]
                + nonlinear[index]
            )
        return derivative

    def boundary(left, right, parameter):
        frequency = float(parameter[0])
        nonlinear_left = project(left[0::2, None])[:, 0]
        residuals = []
        for index, harmonic in enumerate(modes):
            curvature = (
                nonlinear_left[index] - (harmonic * frequency) ** 2 * left[2 * index]
            ) / 3.0
            residuals.append(left[2 * index + 1] - epsilon * curvature)
        for index, harmonic in enumerate(modes):
            if harmonic * frequency < 1.0:
                inverse_width = np.sqrt(1.0 - (harmonic * frequency) ** 2)
                residuals.append(
                    right[2 * index + 1]
                    + (inverse_width + 1.0 / outer) * right[2 * index]
                )
            else:
                residuals.append(right[2 * index])
        residuals.append(left[0] - 0.5 * epsilon * left[1] - amplitude)
        return np.asarray(residuals)

    solution = solve_bvp(
        equations,
        boundary,
        radius,
        state,
        p=[frequency_guess],
        tol=2.0e-8,
        max_nodes=50_000,
    )
    if not solution.success or not np.all(np.isfinite(solution.y)):
        raise RuntimeError(f"independent Gauss BVP failed: {solution.message}")
    if not 0.0 < solution.p[0] < 1.0:
        raise RuntimeError("independent Gauss BVP left the sub-gap branch")
    return solution


def _gauss_ladder(shooting_frequency: float):
    previous = None
    solutions = []
    frequency = shooting_frequency
    for maximum in (1, 3, 5, 7, 9):
        modes = tuple(range(1, maximum + 1, 2))
        solution = _gauss_solution(modes, 2.5, frequency, previous)
        solutions.append(solution)
        previous = solution
        frequency = float(solution.p[0])
    return solutions


def _uniform_remainder(solution, harmonics) -> float:
    radius = np.linspace(1.0e-3, 40.0, 1601)
    amplitudes = solution.sol(radius)[0::2]
    tau = 2.0 * np.pi * np.arange(2048, dtype=float) / 2048.0
    basis = np.cos(np.outer(np.asarray(harmonics), tau))
    field = basis.T @ amplitudes
    retained = (2.0 / tau.size) * basis @ np.sin(field)
    remainder = np.sin(field) - basis.T @ retained
    return float(np.sqrt(np.mean(remainder[:, radius <= 12.0] ** 2)))


def _finite_difference_solution(reference, harmonics, points: int):
    modes = tuple(harmonics)
    radius = np.linspace(0.0, 40.0, points)
    spacing = float(radius[1] - radius[0])
    coefficients = reference.sol(radius)[0::2]
    initial = np.concatenate((coefficients.ravel(), reference.p))
    nodes, weights = leggauss(72)
    tau = np.pi * (nodes + 1.0)
    basis = np.cos(np.outer(np.asarray(modes, dtype=float), tau))
    variable_count = len(modes) * points + 1

    def residual(vector):
        amplitudes = vector[:-1].reshape(len(modes), points)
        frequency = float(vector[-1])
        field = basis.T @ amplitudes
        nonlinear = basis @ (weights[:, None] * np.sin(field))
        result = np.empty(variable_count)
        for index, harmonic in enumerate(modes):
            block = index * points
            result[block] = (
                6.0 * (amplitudes[index, 1] - amplitudes[index, 0]) / spacing**2
                + (harmonic * frequency) ** 2 * amplitudes[index, 0]
                - nonlinear[index, 0]
            )
            first = (
                amplitudes[index, 2:] - amplitudes[index, :-2]
            ) / (2.0 * spacing)
            second = (
                amplitudes[index, 2:]
                - 2.0 * amplitudes[index, 1:-1]
                + amplitudes[index, :-2]
            ) / spacing**2
            result[block + 1 : block + points - 1] = (
                second
                + 2.0 * first / radius[1:-1]
                + (harmonic * frequency) ** 2 * amplitudes[index, 1:-1]
                - nonlinear[index, 1:-1]
            )
            if harmonic == 1:
                inverse_width = np.sqrt(1.0 - frequency**2)
                derivative = (
                    3.0 * amplitudes[index, -1]
                    - 4.0 * amplitudes[index, -2]
                    + amplitudes[index, -3]
                ) / (2.0 * spacing)
                result[block + points - 1] = derivative + (
                    inverse_width + 1.0 / radius[-1]
                ) * amplitudes[index, -1]
            else:
                result[block + points - 1] = amplitudes[index, -1]
        result[-1] = amplitudes[0, 0] - 2.5
        return result

    sparsity = lil_matrix((variable_count, variable_count), dtype=int)
    parameter_column = variable_count - 1
    for index in range(len(modes)):
        block = index * points
        sparsity[block, parameter_column] = 1
        for other in range(len(modes)):
            sparsity[block, other * points] = 1
        sparsity[block, block + 1] = 1
        for radial_index in range(1, points - 1):
            row = block + radial_index
            sparsity[row, parameter_column] = 1
            sparsity[row, block + radial_index - 1 : block + radial_index + 2] = 1
            for other in range(len(modes)):
                sparsity[row, other * points + radial_index] = 1
        outer_row = block + points - 1
        sparsity[outer_row, parameter_column] = 1
        sparsity[outer_row, block + points - 3 : block + points] = 1
    sparsity[-1, 0] = 1
    lower = np.full(variable_count, -np.inf)
    upper = np.full(variable_count, np.inf)
    lower[-1], upper[-1] = 0.8, 0.9999
    result = least_squares(
        residual,
        initial,
        jac_sparsity=sparsity.tocsr(),
        bounds=(lower, upper),
        xtol=1.0e-8,
        ftol=1.0e-8,
        gtol=1.0e-8,
        max_nfev=500,
    )
    return result, float(result.x[-1]), float(np.sqrt(np.mean(result.fun**2)))


def _linear_tail_energy(kind: str, rate: float, outer: float) -> float:
    spacing = 0.01
    radius = np.arange(5.0 + 0.5 * spacing, outer, spacing)
    if kind == "radiative":
        amplitude = np.sin(rate * radius) / radius
        derivative = rate * np.cos(rate * radius) / radius - np.sin(
            rate * radius
        ) / radius**2
        angular = np.sqrt(1.0 + rate**2)
    else:
        amplitude = np.exp(-rate * radius) / radius
        derivative = -np.exp(-rate * radius) * (rate / radius + 1.0 / radius**2)
        angular = np.sqrt(1.0 - rate**2)
    averaged_density = 0.25 * (
        angular**2 * amplitude**2 + derivative**2 + amplitude**2
    )
    return float(4.0 * np.pi * spacing * np.sum(radius**2 * averaged_density))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--primary-evidence", type=Path, required=True)
    arguments = parser.parse_args()
    primary = yaml.safe_load(arguments.primary_evidence.read_text())
    source = arguments.source_file.read_text()
    ledger = CheckLedger("P052-INDEPENDENT")

    ledger.check("the reviewed QB1 source is hash pinned", _hash(arguments.source_file) == SOURCE_SHA256)
    shooting = _shooting_frequency(2.5)
    ledger.check(
        "independent shooting resolves the fundamental branch",
        abs(shooting - 0.976909) < 4.0e-6,
    )
    solutions = _gauss_ladder(shooting)
    frequencies = [float(solution.p[0]) for solution in solutions]
    ledger.check(
        "Gauss-projected BVP independently agrees with shooting at N=1",
        abs(frequencies[0] - shooting) < 4.0e-6,
    )
    primary_frequency = primary["baseline"]["levels"][-1]["omega"]
    ledger.check(
        "Gauss projection independently agrees with the DFT N=9 branch",
        abs(frequencies[-1] - primary_frequency) < 2.0e-7,
    )
    remainders = [
        _uniform_remainder(solution, tuple(range(1, maximum + 1, 2)))
        for solution, maximum in zip(solutions, (1, 3, 5, 7, 9))
    ]
    ledger.check(
        "the independently reconstructed full nonlinear remainder decreases at every level",
        all(fine < 0.2 * coarse for coarse, fine in zip(remainders, remainders[1:])),
    )
    ledger.check(
        "the N=9 independent core remainder is resolved below two times ten to the minus five",
        remainders[-1] < 2.0e-5,
    )
    finite_81 = _finite_difference_solution(solutions[2], (1, 3, 5), 81)
    finite_121 = _finite_difference_solution(solutions[2], (1, 3, 5), 121)
    finite_161 = _finite_difference_solution(solutions[2], (1, 3, 5), 161)
    finite_results = (finite_81, finite_121, finite_161)
    spacings = np.asarray([40.0 / 80.0, 40.0 / 120.0, 40.0 / 160.0])
    fitted_line = np.polyfit(
        np.square(spacings),
        np.asarray([result[1] for result in finite_results]),
        1,
    )
    extrapolated_frequency = float(fitted_line[1])
    fit_residual = float(
        np.max(
            np.abs(
                np.polyval(fitted_line, np.square(spacings))
                - np.asarray([result[1] for result in finite_results])
            )
        )
    )
    ledger.check(
        "finite-difference least squares independently converges on three radial grids",
        all(result[0].success and result[2] < 1.0e-6 for result in finite_results),
    )
    ledger.check(
        "the second-order finite-difference frequencies extrapolate to the Gauss BVP branch",
        abs(finite_161[1] - frequencies[2]) < abs(finite_121[1] - frequencies[2])
        < abs(finite_81[1] - frequencies[2])
        and fit_residual < 2.0e-6
        and abs(extrapolated_frequency - frequencies[2]) < 5.0e-6,
    )

    fundamental = frequencies[-1]
    inverse_width = np.sqrt(1.0 - fundamental**2)
    radiative_wavenumber = np.sqrt((3.0 * fundamental) ** 2 - 1.0)
    ledger.check(
        "the fundamental is evanescent while the third harmonic is radiative",
        inverse_width > 0.0 and 3.0 * fundamental > 1.0 and radiative_wavenumber > 0.0,
    )
    evanescent_100 = _linear_tail_energy("evanescent", inverse_width, 100.0)
    evanescent_200 = _linear_tail_energy("evanescent", inverse_width, 200.0)
    radiative_100 = _linear_tail_energy("radiative", radiative_wavenumber, 100.0)
    radiative_200 = _linear_tail_energy("radiative", radiative_wavenumber, 200.0)
    ledger.check(
        "an evanescent tail has converged radial energy",
        abs(evanescent_200 - evanescent_100) < 1.0e-12,
    )
    ledger.check(
        "a nonzero radiative one-over-r tail has linearly divergent radial energy",
        radiative_200 > 2.0 * radiative_100,
    )
    ledger.check(
        "the source uses the accepted IVP frequency as an inversion target",
        "target = 0.921" in source and "eigen_omega(A_star" in source,
    )
    ledger.check(
        "the source imposes a finite wall on every retained harmonic",
        "res.append(Yb[2 * idx])" in source and "R=40.0" in source,
    )
    ledger.check(
        "the source's truncation check observes frequency only",
        "converges = d35 < d13" in source and "omitted" not in source,
    )
    print(
        "independent frequencies:",
        f"shooting={shooting:.12f}",
        f"Gauss_N9={frequencies[-1]:.12f}",
        f"FD81_N5={finite_81[1]:.12f}",
        f"FD121_N5={finite_121[1]:.12f}",
        f"FD161_N5={finite_161[1]:.12f}",
        f"FD_h2_limit={extrapolated_frequency:.12f}",
    )
    print("independent remainder ladder:", remainders)
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
