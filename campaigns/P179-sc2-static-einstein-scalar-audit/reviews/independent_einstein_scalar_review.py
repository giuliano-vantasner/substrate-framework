#!/usr/bin/env python3
"""Fresh SC2 rederivation without importing either proposed P179 module."""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
from scipy.special import expit, jv
import sympy as sp

from substrate_framework.verification import CheckLedger


def _curvature(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> sp.Matrix:
    dimension = len(coordinates)
    inverse = metric.inv().applyfunc(sp.simplify)
    christoffel = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coordinates[b])
                            + sp.diff(metric[d, b], coordinates[c])
                            - sp.diff(metric[b, c], coordinates[d])
                        )
                        / 2
                        for d in range(dimension)
                    )
                )
                for c in range(dimension)
            ]
            for b in range(dimension)
        ]
        for a in range(dimension)
    ]
    ricci = sp.zeros(dimension)
    for a in range(dimension):
        for b in range(dimension):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(christoffel[c][a][b], coordinates[c])
                    - sp.diff(christoffel[c][a][c], coordinates[b])
                    + sum(
                        christoffel[c][c][d] * christoffel[d][a][b]
                        - christoffel[c][b][d] * christoffel[d][a][c]
                        for d in range(dimension)
                    )
                    for c in range(dimension)
                )
            )
    scalar = sp.simplify(
        sum(
            inverse[a, b] * ricci[a, b]
            for a in range(dimension)
            for b in range(dimension)
        )
    )
    return (inverse * (ricci - metric * scalar / 2)).applyfunc(sp.simplify)


def _shoot() -> tuple[object, object, float, float]:
    amplitude = 3.0
    alpha = 0.03
    epsilon = 0.001

    def frequency(parameter: float) -> float:
        return float(expit(parameter))

    def origin(omega: float, phi_zero: float) -> np.ndarray:
        inverse_lapse = np.exp(-2.0 * phi_zero)
        density = 0.25 * omega**2 * amplitude**2 * inverse_lapse + 1.0 - jv(0, amplitude)
        pressure = 0.25 * omega**2 * amplitude**2 * inverse_lapse - (1.0 - jv(0, amplitude))
        second = (2.0 * jv(1, amplitude) - omega**2 * amplitude * inverse_lapse) / 3.0
        mass_cubic = alpha * density / 6.0
        phi_second = alpha * (density / 6.0 + pressure / 2.0)
        return np.asarray(
            [
                amplitude + 0.5 * second * epsilon**2,
                second * epsilon,
                mass_cubic * epsilon**3,
                phi_zero + 0.5 * phi_second * epsilon**2,
            ]
        )

    def rhs(radius: float, state: np.ndarray, omega: float) -> np.ndarray:
        a, derivative, mass, phi = state
        radial_metric = 1.0 - 2.0 * mass / radius
        if radial_metric <= 0.0:
            raise RuntimeError("independent shooting crossed a horizon")
        inverse_lapse = np.exp(-2.0 * phi)
        potential = 1.0 - jv(0, a)
        density = 0.25 * omega**2 * a**2 * inverse_lapse + 0.25 * radial_metric * derivative**2 + potential
        pressure = 0.25 * radial_metric * derivative**2 + 0.25 * omega**2 * a**2 * inverse_lapse - potential
        mass_prime = 0.5 * alpha * radius**2 * density
        phi_prime = (mass + 0.5 * alpha * radius**3 * pressure) / (radius * (radius - 2.0 * mass))
        metric_prime = 2.0 * mass / radius**2 - 2.0 * mass_prime / radius
        second = (
            (2.0 * jv(1, a) - omega**2 * inverse_lapse * a) / radial_metric
            - derivative * (phi_prime + metric_prime / (2.0 * radial_metric) + 2.0 / radius)
        )
        return np.asarray([derivative, second, mass_prime, phi_prime])

    def integrate(parameters: np.ndarray, outer: float):
        omega = frequency(float(parameters[0]))
        solution = solve_ivp(
            lambda radius, state: rhs(radius, state, omega),
            (epsilon, outer),
            origin(omega, float(parameters[1])),
            method="DOP853",
            rtol=1.0e-10,
            atol=1.0e-12,
            max_step=0.05,
        )
        if not solution.success:
            raise RuntimeError(solution.message)
        a, derivative, mass, phi = solution.y[:, -1]
        radial_metric = 1.0 - 2.0 * mass / outer
        tail_squared = (1.0 - omega**2 / radial_metric) / radial_metric
        if tail_squared <= 0.0:
            raise RuntimeError("independent shooting tail is not evanescent")
        wall = np.asarray(
            [
                derivative + (np.sqrt(tail_squared) + 1.0 / outer) * a,
                phi - 0.5 * np.log(radial_metric),
            ]
        )
        return solution, wall

    guess_frequency = 0.89
    parameters = np.asarray(
        [np.log(guess_frequency / (1.0 - guess_frequency)), -0.18]
    )
    fitted = None
    solution = None
    for outer in (10.0, 20.0, 30.0, 40.0):
        fitted = root(
            lambda values: integrate(values, outer)[1],
            parameters,
            method="hybr",
            tol=1.0e-10,
        )
        if not fitted.success:
            raise RuntimeError(f"R={outer}: {fitted.message}")
        parameters = np.asarray(fitted.x, dtype=np.float64)
        solution, _wall = integrate(parameters, outer)
    assert fitted is not None and solution is not None
    return fitted, solution, frequency(float(fitted.x[0])), float(fitted.x[1])


def main() -> int:
    checks = CheckLedger("P179/C-STG-002 independent")
    time, radius, theta, azimuth = sp.symbols("t r theta phi", real=True)
    positive_radius = sp.symbols("x", positive=True)
    mass = sp.Function("m", real=True)(positive_radius)
    lapse_exponent = sp.Function("Phi", real=True)(positive_radius)
    radial_metric = 1 - 2 * mass / positive_radius
    metric = sp.diag(
        -sp.exp(2 * lapse_exponent),
        1 / radial_metric,
        positive_radius**2,
        positive_radius**2 * sp.sin(theta) ** 2,
    )
    mixed_einstein = _curvature(
        metric, (time, positive_radius, theta, azimuth)
    )
    checks.check(
        "fresh Christoffel reconstruction yields the areal tt constraint",
        sp.simplify(
            mixed_einstein[0, 0]
            + 2 * sp.diff(mass, positive_radius) / positive_radius**2
        )
        == 0,
    )
    expected_rr = 2 * (
        positive_radius * (positive_radius - 2 * mass)
        * sp.diff(lapse_exponent, positive_radius)
        - mass
    ) / positive_radius**3
    checks.check(
        "fresh Christoffel reconstruction yields the areal rr constraint",
        sp.simplify(mixed_einstein[1, 1] - expected_rr) == 0,
    )

    omega = sp.symbols("Omega", positive=True)
    amplitude = sp.Function("a", real=True)(positive_radius)
    density = (
        omega**2 * amplitude**2 * sp.exp(-2 * lapse_exponent) / 4
        + radial_metric * sp.diff(amplitude, positive_radius) ** 2 / 4
        + 1
        - sp.besselj(0, amplitude)
    )
    pressure = (
        radial_metric * sp.diff(amplitude, positive_radius) ** 2 / 4
        + omega**2 * amplitude**2 * sp.exp(-2 * lapse_exponent) / 4
        - (1 - sp.besselj(0, amplitude))
    )
    tangential = (
        omega**2 * amplitude**2 * sp.exp(-2 * lapse_exponent) / 4
        - radial_metric * sp.diff(amplitude, positive_radius) ** 2 / 4
        - (1 - sp.besselj(0, amplitude))
    )
    scalar = sp.simplify(
        sp.diff(amplitude, positive_radius, 2)
        + (
            sp.diff(lapse_exponent, positive_radius)
            + sp.diff(radial_metric, positive_radius) / (2 * radial_metric)
            + 2 / positive_radius
        )
        * sp.diff(amplitude, positive_radius)
        + (
            omega**2 * amplitude * sp.exp(-2 * lapse_exponent)
            - 2 * sp.besselj(1, amplitude)
        )
        / radial_metric
    )
    conservation = sp.simplify(
        sp.diff(pressure, positive_radius)
        + (density + pressure) * sp.diff(lapse_exponent, positive_radius)
        + 2 * (pressure - tangential) / positive_radius
    )
    checks.check(
        "fresh canonical stress and scalar projection give the conservation factor",
        sp.simplify(
            sp.expand_func(
                conservation
                - radial_metric
                * sp.diff(amplitude, positive_radius)
                * scalar
                / 2
            )
        )
        == 0,
    )
    checks.check(
        "fresh Jacobi-Anger coefficients retain nonzero discarded harmonics",
        2 * sp.besselj(3, amplitude) != 0
        and sp.series(2 * sp.besselj(3, sp.Symbol("A")), sp.Symbol("A"), 0, 5).removeO()
        == sp.Symbol("A") ** 3 / 24,
    )
    rho_second = (
        -omega**2 * amplitude**2 * sp.exp(-2 * lapse_exponent) / 4
        + radial_metric * sp.diff(amplitude, positive_radius) ** 2 / 4
        + 2 * sp.besselj(2, amplitude)
    )
    checks.check(
        "fresh pointwise stress retains a generally nonzero second harmonic",
        rho_second != 0 and rho_second.subs(sp.diff(amplitude, positive_radius), 0) != 0,
    )

    phase = np.linspace(0.0, 2.0 * np.pi, 100_001)
    trial = 1.7
    average = np.trapezoid(1.0 - np.cos(trial * np.cos(phase)), phase) / (2.0 * np.pi)
    checks.check(
        "fresh current-NumPy quadrature reproduces the phase-averaged potential",
        abs(average - (1.0 - jv(0, trial))) < 2.0e-14,
    )

    fitted, solution, fitted_frequency, fitted_phi = _shoot()
    wall_mass = float(solution.y[2, -1])
    minimum_metric = float(np.min(1.0 - 2.0 * solution.y[2] / solution.t))
    checks.check(
        "fresh DOP853 root shooting converges with finite state and positive f",
        fitted.success
        and solution.success
        and np.all(np.isfinite(solution.y))
        and minimum_metric > 0.1,
    )
    checks.check(
        "fresh shooting lands on the finite-gravity subgap branch intrinsically",
        0.8 < fitted_frequency < 0.95
        and -0.3 < fitted_phi < -0.1
        and 0.2 < wall_mass < 0.4,
    )
    correct_second = np.asarray(
        [
            # Difference between the wrong-J1-sign and solved scalar RHS.
            4.0 * jv(1, value) / (1.0 - 2.0 * mass_value / radius_value)
            for radius_value, value, mass_value in zip(
                solution.t, solution.y[0], solution.y[2]
            )
        ]
    )
    checks.check(
        "fresh wrong-J1-sign mutation produces an order-one scalar defect",
        np.max(np.abs(correct_second)) > 0.1,
    )
    print(
        "INDEPENDENT",
        f"omega={fitted_frequency:.15g}",
        f"mass={wall_mass:.15g}",
        f"phi0={fitted_phi:.15g}",
        f"nfev={fitted.nfev}",
        f"minf={minimum_metric:.15g}",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
