#!/usr/bin/env python3
"""Independent product-density and finite-difference review for P041."""

from __future__ import annotations

import numpy as np
import sympy as sp

from substrate_framework.tt_angular import tt_project_symmetric
from substrate_framework.verification import CheckLedger


def centered_third(values: np.ndarray, step: float) -> np.ndarray:
    derivative = values
    for _ in range(3):
        next_derivative = np.full_like(derivative, np.nan)
        next_derivative[1:-1] = (derivative[2:] - derivative[:-2]) / (2 * step)
        derivative = next_derivative
    return derivative


def exact_special_moment(times: np.ndarray) -> np.ndarray:
    eta = 1.0 / np.sqrt(2.0)
    omega = eta
    return (
        4.0 * np.pi**2 / (3.0 * eta)
        + 16.0 / eta * np.arcsinh(np.sin(omega * times)) ** 2
    )


def main() -> int:
    ledger = CheckLedger("P041-INDEPENDENT")
    y, z, width = sp.symbols("y z s", real=True, positive=True)
    gaussian_y = sp.exp(-y**2 / (2 * width**2)) / (sp.sqrt(2 * sp.pi) * width)
    gaussian_z = sp.exp(-z**2 / (2 * width**2)) / (sp.sqrt(2 * sp.pi) * width)
    ledger.check(
        "direct one-dimensional Gaussian factors normalize independently",
        sp.integrate(gaussian_y, (y, -sp.oo, sp.oo)) == 1
        and sp.integrate(gaussian_z, (z, -sp.oo, sp.oo)) == 1,
    )
    ledger.check(
        "direct Gaussian integration gives per-axis variance s-squared and radial variance twice that",
        sp.simplify(sp.integrate(y**2 * gaussian_y, (y, -sp.oo, sp.oo)) - width**2)
        == 0
        and sp.simplify(sp.integrate(z**2 * gaussian_z, (z, -sp.oo, sp.oo)) - width**2)
        == 0,
    )
    ledger.check(
        "centering independently kills all transverse first and mixed moments",
        sp.integrate(y * gaussian_y, (y, -sp.oo, sp.oo)) == 0
        and sp.integrate(z * gaussian_z, (z, -sp.oo, sp.oo)) == 0,
    )

    total, longitudinal, variance = sp.symbols("M mu sigma2", real=True)
    direct_second = sp.diag(longitudinal, total * variance, total * variance)
    direct_stf = sp.simplify(direct_second - sp.eye(3) * sp.trace(direct_second) / 3)
    expected_stf = sp.diag(
        2 * (longitudinal - total * variance) / 3,
        -(longitudinal - total * variance) / 3,
        -(longitudinal - total * variance) / 3,
    )
    ledger.check(
        "independent trace removal gives the normalized axisymmetric STF tensor",
        sp.simplify(direct_stf - expected_stf) == sp.zeros(3),
    )
    derivative = sp.symbols("d", real=True)
    derivative_tensor = sp.diag(2 * derivative / 3, -derivative / 3, -derivative / 3)
    ledger.check(
        "independent projection gives an axial null and perpendicular plus-only image",
        tt_project_symmetric(derivative_tensor, [1, 0, 0]) == sp.zeros(3)
        and tt_project_symmetric(derivative_tensor, [0, 0, 1])
        == sp.diag(derivative / 2, -derivative / 2, 0),
    )

    frequency = 1.0 / np.sqrt(2.0)
    total_time = 4.0 * np.pi / frequency
    errors = []
    for points in (1000, 2000, 4000):
        times = np.linspace(0.0, total_time, points)
        step = times[1] - times[0]
        numerical = centered_third(exact_special_moment(times), step)
        interior = slice(8, -8)
        exact = np.asarray(
            sp.lambdify(
                sp.symbols("t", real=True),
                sp.diff(
                    4 * sp.sqrt(2) * sp.pi**2 / 3
                    + 16
                    * sp.sqrt(2)
                    * sp.asinh(sp.sin(sp.symbols("t", real=True) / sp.sqrt(2))) ** 2,
                    sp.symbols("t", real=True),
                    3,
                ),
                "numpy",
            )(times[interior]),
            dtype=float,
        )
        errors.append(float(np.max(np.abs(numerical[interior] - exact))))
    ledger.check(
        "independent repeated central differences converge at second order to the exact third derivative",
        errors[1] < errors[0]
        and errors[2] < errors[1]
        and errors[0] / errors[1] > 3.7
        and errors[1] / errors[2] > 3.7,
    )

    coordinate, second_transverse, third_transverse, time, epsilon = sp.symbols(
        "x y2 z2 tau epsilon", real=True
    )
    counter_density = sp.exp(
        -coordinate**2 - second_transverse**2 - third_transverse**2
    ) * (1 + epsilon * sp.cos(time) * (coordinate**2 - sp.Rational(1, 2)))
    counter_monopole = sp.integrate(
        counter_density,
        (coordinate, -sp.oo, sp.oo),
        (second_transverse, -sp.oo, sp.oo),
        (third_transverse, -sp.oo, sp.oo),
    )
    ledger.check(
        "constant total density does not by itself supply local conservation",
        sp.simplify(counter_monopole - sp.pi ** sp.Rational(3, 2)) == 0
        and sp.simplify(sp.diff(counter_density, time)) != 0,
    )
    ledger.check(
        "zero current is a concrete failed completion of that time-varying density",
        sp.simplify(
            sp.diff(counter_density, time).subs(
                {
                    coordinate: 0,
                    second_transverse: 0,
                    third_transverse: 0,
                    time: sp.pi / 2,
                }
            )
            - epsilon / 2
        )
        == 0,
    )

    count = ledger.finish()
    print(f"P041 INDEPENDENT PRODUCT-DENSITY REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
