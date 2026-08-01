#!/usr/bin/env python3
"""Independent first-variation, connection, and virial review for P007.

This file intentionally does not import the new variational or collective modules.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def christoffels(
    metric: sp.Matrix, coordinates: list[sp.Symbol]
) -> list[list[list[sp.Expr]]]:
    dimension = len(coordinates)
    inverse = metric.inv()
    return [
        [
            [
                sp.simplify(
                    sum(
                        inverse[upper, inner]
                        * (
                            sp.diff(metric[inner, second], coordinates[first])
                            + sp.diff(metric[inner, first], coordinates[second])
                            - sp.diff(metric[first, second], coordinates[inner])
                        )
                        for inner in range(dimension)
                    )
                    / 2
                )
                for second in range(dimension)
            ]
            for first in range(dimension)
        ]
        for upper in range(dimension)
    ]


def run() -> int:
    variational_checks = CheckLedger("C-VAR-001-INDEPENDENT")
    collective_checks = CheckLedger("C-CC-001-INDEPENDENT")
    virial_checks = CheckLedger("C-VIR-001-INDEPENDENT")

    time = sp.symbols("t", real=True)
    epsilon, fixed_scale = sp.symbols("epsilon A", real=True, nonzero=True)
    path = sp.Function("q", real=True)(time)
    variation = sp.Function("h", real=True)(time)
    potential = sp.Function("V")
    varied_path = path + epsilon * variation
    base_integrand = (
        sp.diff(varied_path, time) ** 2 / 2 - potential(varied_path)
    )
    first_variation = sp.diff(base_integrand, epsilon).subs(epsilon, 0)
    scaled_first_variation = sp.diff(
        fixed_scale**3 * base_integrand, epsilon
    ).subs(epsilon, 0)
    variational_checks.check(
        "directional first variation independently factors any fixed scale",
        sp.simplify(scaled_first_variation - fixed_scale**3 * first_variation)
        == 0,
    )
    dependent_scale = varied_path
    dependent_first_variation = sp.diff(
        dependent_scale * base_integrand, epsilon
    ).subs(epsilon, 0)
    variational_checks.check(
        "a path-dependent multiplier adds an independent variation term",
        sp.simplify(
            dependent_first_variation - path * first_variation
        )
        != 0,
    )

    coordinate_time, position = sp.symbols("tau x", real=True)
    signal_speed = sp.symbols("c0", positive=True)
    index = sp.Function("n", positive=True)(position)
    metric = sp.diag(-1 / index, index / signal_speed**2)
    connection = christoffels(metric, [coordinate_time, position])
    velocity = sp.symbols("v", real=True)
    coordinate_acceleration = sp.simplify(
        -connection[1][0][0]
        - 2 * connection[1][0][1] * velocity
        - connection[1][1][1] * velocity**2
        + velocity
        * (
            connection[0][0][0]
            + 2 * connection[0][0][1] * velocity
            + connection[0][1][1] * velocity**2
        )
    )
    expected = (
        signal_speed**2 - 3 * index**2 * velocity**2
    ) * sp.diff(index, position) / (2 * index**3)
    collective_checks.check(
        "direct Christoffel reconstruction gives the full coordinate-time acceleration",
        sp.simplify(coordinate_acceleration - expected) == 0,
    )
    collective_checks.check(
        "the independently reconstructed slow limit retains the index gradient",
        sp.simplify(
            coordinate_acceleration.subs(velocity, 0)
            - signal_speed**2
            * sp.diff(index, position)
            / (2 * index**3)
        )
        == 0,
    )

    energy_scale, alpha = sp.symbols("E0 alpha", positive=True)
    slow_wrong_lagrangian = (
        -energy_scale / sp.sqrt(index)
        + index ** sp.Rational(3, 2) * velocity**2 / (2 * signal_speed**2)
    )
    inertial_coefficient = sp.diff(
        slow_wrong_lagrangian, velocity, 2
    )
    static_force = sp.diff(
        slow_wrong_lagrangian.subs(velocity, 0), position
    )
    initial_acceleration = sp.simplify(static_force / inertial_coefficient)
    collective_checks.check(
        "independent slow expansion gives an E0-sensitive mixed-scale acceleration",
        sp.simplify(
            initial_acceleration
            - energy_scale
            * signal_speed**2
            * sp.diff(index, position)
            / (2 * index**3)
        )
        == 0
        and sp.simplify(
            initial_acceleration
            .subs(sp.diff(index, position), alpha)
            .subs(index, 1)
            .subs(energy_scale, 2)
            - initial_acceleration
            .subs(sp.diff(index, position), alpha)
            .subs(index, 1)
            .subs(energy_scale, 1)
        )
        == signal_speed**2 * alpha / 2,
    )

    width_slope, energy_slope = sp.symbols("w_s e_s", real=True)
    recovered_a = sp.simplify(width_slope - energy_slope)
    recovered_b = sp.simplify(-(width_slope + energy_slope))
    virial_checks.check(
        "inverting the slope map independently gives a=w-e and b=-(w+e)",
        sp.simplify(
            (recovered_a - recovered_b) / 2 - width_slope
        )
        == 0
        and sp.simplify(
            -(recovered_a + recovered_b) / 2 - energy_slope
        )
        == 0,
    )
    virial_checks.check(
        "the inverted half-slope target gives Option C and not A or B",
        recovered_a.subs(
            {width_slope: -sp.Rational(1, 2), energy_slope: -sp.Rational(1, 2)}
        )
        == 0
        and recovered_b.subs(
            {width_slope: -sp.Rational(1, 2), energy_slope: -sp.Rational(1, 2)}
        )
        == 1,
    )

    variational_total = variational_checks.finish()
    collective_total = collective_checks.finish()
    virial_total = virial_checks.finish()
    total = variational_total + collective_total + virial_total
    print(f"P007 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
