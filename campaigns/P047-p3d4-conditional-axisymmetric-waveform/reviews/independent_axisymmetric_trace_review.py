#!/usr/bin/env python3
"""Independent P047 tensor and finite-difference rederivation."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.governance import load_yaml
from substrate_framework.radial_sine_gordon import gaussian_radial_seed
from substrate_framework.sine_gordon_l_modes import (
    evolve_radial_background_with_linearized_mode,
    regular_l_mode_gaussian_seed,
)
from substrate_framework.verification import CheckLedger


SECOND_WEIGHTS = np.array(
    [1 / 90, -3 / 20, 3 / 2, -49 / 18, 3 / 2, -3 / 20, 1 / 90],
    dtype=float,
)
THIRD_WEIGHTS = np.array(
    [1 / 8, -1, 13 / 8, 0, -13 / 8, 1, -1 / 8],
    dtype=float,
)


def direct_derivative(values: np.ndarray, spacing: float, order: int) -> np.ndarray:
    weights = SECOND_WEIGHTS if order == 2 else THIRD_WEIGHTS
    derivative = np.full_like(values, np.nan)
    for index in range(3, values.size - 3):
        derivative[index] = (
            np.dot(weights, values[index - 3 : index + 4]) / spacing**order
        )
    return derivative


def rms(values: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(values))))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary-result", type=Path, required=True)
    args = parser.parse_args()
    primary = load_yaml(args.primary_result)
    ledger = CheckLedger("P047-INDEPENDENT")

    nodes = list(range(-3, 4))
    exact_second = sp.finite_diff_weights(2, nodes, 0)[2][-1]
    exact_third = sp.finite_diff_weights(3, nodes, 0)[3][-1]
    ledger.check(
        "independent polynomial moment equations derive both seven-point stencils",
        exact_second == [
            sp.Rational(1, 90),
            -sp.Rational(3, 20),
            sp.Rational(3, 2),
            -sp.Rational(49, 18),
            sp.Rational(3, 2),
            -sp.Rational(3, 20),
            sp.Rational(1, 90),
        ]
        and exact_third == [
            sp.Rational(1, 8),
            -1,
            sp.Rational(13, 8),
            0,
            -sp.Rational(13, 8),
            1,
            -sp.Rational(1, 8),
        ],
    )

    polynomial_time = np.linspace(-2.0, 2.0, 81)
    polynomial = polynomial_time**6 - 3.0 * polynomial_time**4
    second = direct_derivative(polynomial, polynomial_time[1] - polynomial_time[0], 2)
    third = direct_derivative(polynomial, polynomial_time[1] - polynomial_time[0], 3)
    interior = slice(3, -3)
    ledger.check(
        "the direct stencils exactly differentiate their load-bearing polynomial limit",
        np.allclose(
            second[interior],
            30.0 * polynomial_time[interior] ** 4
            - 36.0 * polynomial_time[interior] ** 2,
            atol=2.0e-9,
        )
        and np.allclose(
            third[interior],
            120.0 * polynomial_time[interior] ** 3
            - 72.0 * polynomial_time[interior],
            atol=2.0e-9,
        ),
    )

    amplitude = sp.symbols("alpha", real=True)
    axis = sp.Matrix([1, 2, 2]) / 3
    direction = sp.Matrix([2, -1, 2]) / 3
    projector = sp.eye(3) - direction * direction.T
    tensor = amplitude * (axis * axis.T - sp.eye(3) / 3)
    transverse = sp.simplify(projector * tensor * projector)
    projected = sp.simplify(
        transverse - projector * sp.trace(transverse) / 2
    )
    first = sp.simplify(
        (axis - axis.dot(direction) * direction)
        / sp.sqrt(1 - axis.dot(direction) ** 2)
    )
    second_transverse = sp.simplify(direction.cross(first))
    conventional_plus = sp.simplify(
        (first.dot(projected * first) - second_transverse.dot(projected * second_transverse))
        / 2
    )
    conventional_cross = sp.simplify(first.dot(projected * second_transverse))
    sine_squared = sp.simplify(1 - axis.dot(direction) ** 2)
    ledger.check(
        "direct projector algebra gives sine-squared plus and zero cross",
        sp.simplify(conventional_plus - amplitude * sine_squared / 2) == 0
        and conventional_cross == 0,
    )
    axis_projector = sp.eye(3) - axis * axis.T
    axis_transverse = sp.simplify(axis_projector * tensor * axis_projector)
    axis_tt = sp.simplify(
        axis_transverse - axis_projector * sp.trace(axis_transverse) / 2
    )
    ledger.check(
        "direct projection along the arbitrary symmetry axis is exactly null",
        axis_tt == sp.zeros(3),
    )

    q3, coupling = sp.symbols("q3 G", real=True, nonzero=True)
    triple_norm = sp.Rational(3, 2) * q3**2
    angular_integral = sp.Rational(8, 5) * sp.pi * triple_norm
    correct_power = sp.simplify(
        1 / (32 * sp.pi * coupling)
        * (2 * coupling / 3) ** 2
        * angular_integral
    )
    source_power = coupling * triple_norm / 5
    ledger.check(
        "independent flux contraction gives G qthird squared/30 for triple Qzz",
        sp.simplify(correct_power - coupling * q3**2 / 30) == 0,
    )
    ledger.check(
        "using G/5 directly on the triple tensor is independently ninefold high",
        sp.simplify(source_power / correct_power - 9) == 0,
    )

    spacing = 0.1
    radius = spacing * np.arange(801)
    result = evolve_radial_background_with_linearized_mode(
        gaussian_radial_seed(radius, 3.0, 4.0),
        regular_l_mode_gaussian_seed(
            radius,
            ell=2,
            amplitude=0.2,
            width=4.0,
        ),
        spacing=spacing,
        final_time=40.0,
        ell=2,
        courant=0.4,
        sample_interval=0.16,
    )
    sample_spacing = float(result.time[1] - result.time[0])
    qzz = result.p2_triple_stf_zz_coefficient
    q_second = direct_derivative(qzz, sample_spacing, 2)
    q_third = direct_derivative(qzz, sample_spacing, 3)
    interpreted = (result.time >= 5.0) & (result.time <= 35.0)
    direct_second_rms = rms(q_second[interpreted])
    direct_third_rms = rms(q_third[interpreted])
    direct_wave_rms = rms(q_second[interpreted] / 2.0)
    direct_power_mean = float(np.mean(np.square(q_third[interpreted]) / 30.0))
    reference = primary["numeric_scope"]

    def relative(value: float, expected: float) -> float:
        return abs(value - expected) / abs(expected)

    derivative_errors = (
        relative(
            direct_second_rms,
            reference["triple_qzz_over_epsilon_second_rms"],
        ),
        relative(
            direct_third_rms,
            reference["triple_qzz_over_epsilon_third_rms"],
        ),
    )
    ledger.check(
        "direct seven-point derivatives reproduce both primary RMS traces below ten percent",
        max(derivative_errors) < 0.10,
        f"second/third relative errors={derivative_errors}",
    )
    conditional_errors = (
        relative(
            direct_wave_rms,
            reference["conditional_edge_on_waveform_R_over_G_epsilon_rms"],
        ),
        relative(
            direct_power_mean,
            reference["conditional_power_over_G_epsilon_squared_mean"],
        ),
    )
    ledger.check(
        "direct finite differences reproduce the conditional waveform and power coefficients",
        max(conditional_errors) < 0.10,
        f"waveform/power relative errors={conditional_errors}",
    )
    ledger.check(
        "the independent trace is finite, endpoint-excluded, and boundary quiet",
        result.completed
        and np.all(np.isfinite(q_second[interpreted]))
        and np.all(np.isfinite(q_third[interpreted]))
        and result.max_boundary_background < 3.0e-19
        and result.max_boundary_mode < 4.0e-19,
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
