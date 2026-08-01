#!/usr/bin/env python3
"""Independent tensor reconstruction for proposed C-OG-001/002.

This file intentionally does not import ``substrate_framework.optical_geometry``.
It constructs connections, curvature, the scalar wave operator, and geodesic
acceleration directly from the metric definitions.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def christoffels(metric: sp.Matrix, coordinates: list[sp.Symbol]) -> list:
    dimension = len(coordinates)
    inverse = metric.inv()
    result = [
        [[sp.S.Zero for _ in range(dimension)] for _ in range(dimension)]
        for _ in range(dimension)
    ]
    for upper in range(dimension):
        for first in range(dimension):
            for second in range(dimension):
                result[upper][first][second] = sp.simplify(
                    sum(
                        inverse[upper, index]
                        * (
                            sp.diff(metric[index, second], coordinates[first])
                            + sp.diff(metric[index, first], coordinates[second])
                            - sp.diff(metric[first, second], coordinates[index])
                        )
                        for index in range(dimension)
                    )
                    / 2
                )
    return result


def ricci_scalar(metric: sp.Matrix, coordinates: list[sp.Symbol]) -> sp.Expr:
    dimension = len(coordinates)
    inverse = metric.inv()
    connection = christoffels(metric, coordinates)
    ricci = sp.zeros(dimension)
    for first in range(dimension):
        for second in range(dimension):
            ricci[first, second] = sp.simplify(
                sum(
                    sp.diff(connection[index][first][second], coordinates[index])
                    - sp.diff(connection[index][first][index], coordinates[second])
                    + sum(
                        connection[index][index][inner]
                        * connection[inner][first][second]
                        - connection[index][second][inner]
                        * connection[inner][first][index]
                        for inner in range(dimension)
                    )
                    for index in range(dimension)
                )
            )
    return sp.simplify(
        sum(
            inverse[first, second] * ricci[first, second]
            for first in range(dimension)
            for second in range(dimension)
        )
    )


def scalar_box(
    scalar: sp.Expr, metric: sp.Matrix, coordinates: list[sp.Symbol]
) -> sp.Expr:
    dimension = len(coordinates)
    inverse = metric.inv()
    connection = christoffels(metric, coordinates)
    return sp.simplify(
        sum(
            inverse[first, second]
            * (
                sp.diff(scalar, coordinates[first], coordinates[second])
                - sum(
                    connection[inner][first][second]
                    * sp.diff(scalar, coordinates[inner])
                    for inner in range(dimension)
                )
            )
            for first in range(dimension)
            for second in range(dimension)
        )
    )


def run() -> int:
    geometry_checks = CheckLedger("C-OG-001-INDEPENDENT")
    potential_checks = CheckLedger("C-OG-002-INDEPENDENT")
    t, x = sp.symbols("t x", real=True)
    c0 = sp.symbols("c0", positive=True)
    n = sp.Function("n", positive=True)(x)
    metric = sp.diag(-1 / n, n / c0**2)

    reconstructed_curvature = ricci_scalar(metric, [t, x])
    expected_curvature = c0**2 * (
        n * sp.diff(n, x, 2) - 2 * sp.diff(n, x) ** 2
    ) / n**3
    geometry_checks.check(
        "Christoffel-to-Ricci reconstruction gives the claimed curvature",
        sp.simplify(reconstructed_curvature - expected_curvature) == 0,
    )
    reconstructed_box = scalar_box(sp.log(n), metric, [t, x])
    geometry_checks.check(
        "independently reconstructed tensor Box(log(n)) equals Ricci curvature",
        sp.simplify(reconstructed_box - reconstructed_curvature) == 0,
    )

    connection = christoffels(metric, [t, x])
    slow_acceleration = sp.simplify(-connection[1][0][0])
    geometry_checks.check(
        "the metric connection independently gives c0^2*n_x/(2*n^3)",
        sp.simplify(
            slow_acceleration - c0**2 * sp.diff(n, x) / (2 * n**3)
        )
        == 0,
    )

    alpha = sp.symbols("alpha", positive=True)
    concrete_index = 1 + alpha * x
    wrong_scalar = concrete_index
    concrete_metric = sp.diag(
        -1 / concrete_index, concrete_index / c0**2
    )
    wrong_residual = sp.simplify(
        scalar_box(wrong_scalar, concrete_metric, [t, x])
        - ricci_scalar(concrete_metric, [t, x])
    )
    geometry_checks.check(
        "the predecessor's concrete f(n)=n counterexample is genuinely off shell",
        wrong_residual != 0,
    )

    potential = sp.Function("Phi")(x)
    tf_index = 1 / (1 + 2 * potential / c0**2)
    tf_metric = sp.diag(-1 / tf_index, tf_index / c0**2)
    tf_connection = christoffels(tf_metric, [t, x])
    exact_drift = sp.simplify(-tf_connection[1][0][0])
    potential_checks.check(
        "direct Christoffel substitution gives the exact conditional drift",
        sp.simplify(
            exact_drift
            + (1 + 2 * potential / c0**2) * sp.diff(potential, x)
        )
        == 0,
    )

    radius, theta, azimuth = sp.symbols("r theta azimuth", positive=True)
    radial_index = 1 + radius**2
    metric_4d = sp.diag(
        -1 / radial_index,
        radial_index,
        radial_index * radius**2,
        radial_index * radius**2 * sp.sin(theta) ** 2,
    )
    coordinates_4d = [t, radius, theta, azimuth]
    residual_4d = sp.simplify(
        scalar_box(sp.log(radial_index), metric_4d, coordinates_4d)
        - ricci_scalar(metric_4d, coordinates_4d)
    )
    geometry_checks.check(
        "an explicit 3+1 radial optical metric rejects dimensional overextension",
        residual_4d != 0 and sp.simplify(residual_4d.subs(radius, 1)) != 0,
    )

    geometry_total = geometry_checks.finish()
    potential_total = potential_checks.finish()
    print(
        f"P004 INDEPENDENT REVIEW ALL {geometry_total + potential_total} CHECKS PASS"
    )
    return geometry_total + potential_total


if __name__ == "__main__":
    run()
