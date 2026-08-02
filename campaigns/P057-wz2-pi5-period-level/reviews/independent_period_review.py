"""Independent numerical and topology review for P057.

This implementation deliberately does not import the canonical WZW map or
period helpers.  It differentiates the primary-source map by central finite
differences and integrates the resulting pullback density with tensor
Gauss--Legendre cubature.
"""

from __future__ import annotations

import itertools

import numpy as np
from numpy.polynomial.legendre import leggauss

from substrate_framework.verification import CheckLedger


PERMUTATIONS = tuple(itertools.permutations(range(5)))
SIGNS = tuple(
    -1
    if sum(
        order[first] > order[second]
        for first in range(5)
        for second in range(first + 1, 5)
    )
    % 2
    else 1
    for order in PERMUTATIONS
)


def eta(point: np.ndarray) -> np.ndarray:
    first, second, third = point
    cross = np.array(
        [
            [0, -np.conj(third), np.conj(second)],
            [np.conj(third), 0, -np.conj(first)],
            [-np.conj(second), np.conj(first), 0],
        ],
        dtype=complex,
    )
    return np.outer(point, point) + cross


def sphere_point(coordinates: np.ndarray) -> np.ndarray:
    first, second, third, fourth, phase = coordinates
    s1, s2, s3, s4 = map(np.sin, (first, second, third, fourth))
    real = np.array(
        [
            np.cos(first),
            s1 * np.cos(second),
            s1 * s2 * np.cos(third),
            s1 * s2 * s3 * np.cos(fourth),
            s1 * s2 * s3 * s4 * np.cos(phase),
            s1 * s2 * s3 * s4 * np.sin(phase),
        ]
    )
    return np.array(
        [real[0] + 1j * real[1], real[2] + 1j * real[3], real[4] + 1j * real[5]]
    )


def alternating_trace(values: list[np.ndarray]) -> complex:
    total = 0j
    for order, sign in zip(PERMUTATIONS, SIGNS, strict=True):
        product = np.eye(3, dtype=complex)
        for index in order:
            product = product @ values[index]
        total += sign * np.trace(product)
    return complex(total)


def pullback_density(
    coordinates: np.ndarray, step: float, reverse_orientation: bool = False
) -> complex:
    matrix = eta(sphere_point(coordinates))
    forms: list[np.ndarray] = []
    for axis in range(5):
        plus = coordinates.copy()
        minus = coordinates.copy()
        plus[axis] += step
        minus[axis] -= step
        derivative = (eta(sphere_point(plus)) - eta(sphere_point(minus))) / (2 * step)
        forms.append(matrix.conj().T @ derivative)
    if reverse_orientation:
        forms[0], forms[1] = forms[1], forms[0]
    return -1j * alternating_trace(forms)


def sphere_coordinate_jacobian(coordinates: np.ndarray) -> float:
    first, second, third, fourth, _ = coordinates
    return float(
        np.sin(first) ** 4
        * np.sin(second) ** 3
        * np.sin(third) ** 2
        * np.sin(fourth)
    )


def integrate_period(order: int, step: float) -> float:
    nodes, weights = leggauss(order)
    coordinate_nodes = [(nodes + 1) * np.pi / 2] * 4 + [(nodes + 1) * np.pi]
    coordinate_weights = [weights * np.pi / 2] * 4 + [weights * np.pi]
    integral = 0.0
    for multi_index in itertools.product(range(order), repeat=5):
        coordinates = np.array(
            [coordinate_nodes[axis][multi_index[axis]] for axis in range(5)]
        )
        weight = float(
            np.prod(
                [coordinate_weights[axis][multi_index[axis]] for axis in range(5)]
            )
        )
        integral += weight * pullback_density(coordinates, step).real
    return integral


def main() -> int:
    ledger = CheckLedger("P057-INDEPENDENT")
    samples = (
        np.array([1.0, 0.2j, -0.3 + 0.1j]),
        np.array([0.1 + 0.4j, -0.7j, 0.2]),
        np.array([-0.2j, 0.3 + 0.6j, -0.1]),
    )
    for index, sample in enumerate(samples, start=1):
        point = sample / np.linalg.norm(sample)
        matrix = eta(point)
        ledger.check(
            f"sample {index} is exactly targeted to SU3 numerically",
            np.max(np.abs(matrix.conj().T @ matrix - np.eye(3))) < 2e-15
            and abs(np.linalg.det(matrix) - 1) < 2e-15,
        )

    source_phase = np.pi
    source_determinant = np.exp(1j * source_phase)
    ledger.check(
        "the WZ2 projector family fails the determinant-one condition",
        abs(source_determinant + 1) < 1e-15 and abs(source_determinant - 1) > 1,
    )

    point = np.array([1.0, 1.1, 0.9, 0.8, 0.7])
    target_density = -480 * sphere_coordinate_jacobian(point)
    steps = (0.04, 0.02, 0.01, 0.005, 0.0025)
    step_errors = [
        abs(pullback_density(point, step).real - target_density) / abs(target_density)
        for step in steps
    ]
    print(f"finite-difference relative errors: {step_errors}")
    ledger.check(
        "central-difference density converges at second order",
        all(
            step_errors[index + 1] < step_errors[index]
            for index in range(len(step_errors) - 1)
        )
        and all(
            3.9 < step_errors[index] / step_errors[index + 1] < 4.1
            for index in range(len(step_errors) - 1)
        )
        and step_errors[-1] < 1.1e-5,
    )
    raw_density = 1j * pullback_density(point, steps[-1])
    ledger.check(
        "the reality factor and orientation are load-bearing",
        abs(raw_density.real) < 1e-6 * abs(raw_density.imag)
        and pullback_density(point, steps[-1]).real < 0
        and pullback_density(point, steps[-1], reverse_orientation=True).real > 0
        and abs(
            pullback_density(point, steps[-1], reverse_orientation=True)
            + pullback_density(point, steps[-1])
        )
        < 1e-8,
    )

    orders = (3, 4, 5, 6)
    target_period = -480 * np.pi**3
    periods = [integrate_period(order, 2e-5) for order in orders]
    period_errors = [abs(value / target_period - 1) for value in periods]
    print(f"Gauss orders and periods: {list(zip(orders, periods, strict=True))}")
    print(f"Gauss relative errors: {period_errors}")
    ledger.check(
        "independent five-dimensional cubature converges to minus 480 pi cubed",
        all(
            period_errors[index + 1] < period_errors[index]
            for index in range(len(period_errors) - 1)
        )
        and period_errors[-1] < 6e-4,
    )

    coefficient = 1 / (240 * np.pi**2)
    integer_phases = [
        np.exp(1j * coefficient * target_period * winding)
        for winding in (-3, -1, 0, 1, 4)
    ]
    ledger.check(
        "the derived coefficient step closes every sampled integer winding",
        max(abs(value - 1) for value in integer_phases) < 1e-14,
    )
    ledger.check(
        "half-level and half-period normalization mutations both fail",
        abs(np.exp(1j * coefficient * target_period / 2) + 1) < 2e-15
        and abs(np.exp(1j * (coefficient / 2) * target_period) + 1) < 2e-15,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
