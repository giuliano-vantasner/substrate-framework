"""Independent quadrature and ODE review for the P091 LB1 claim delta."""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

from substrate_framework.sine_gordon import (
    breather_damping_form_factor,
    breather_mean_kinetic_integral,
    phase_averaged_breather_energy_efold_time,
)
from substrate_framework.verification import CheckLedger


def direct_mean_kinetic(omega: float) -> float:
    """Integrate the exact field velocity over space and phase independently."""

    eta = math.sqrt(1.0 - omega**2)

    def spatial_integral(phase: float) -> float:
        sine_ratio = (eta / omega) * math.sin(phase)

        def positive_half(inverse_width_coordinate: float) -> float:
            inverse_cosh = 1.0 / math.cosh(inverse_width_coordinate)
            field_velocity = (
                4.0
                * eta
                * math.cos(phase)
                * inverse_cosh
                / (1.0 + (sine_ratio * inverse_cosh) ** 2)
            )
            return field_velocity**2 / eta

        return 2.0 * quad(
            positive_half,
            0.0,
            40.0,
            epsabs=1e-11,
            epsrel=1e-11,
            limit=200,
        )[0]

    quarter_integral = quad(
        spatial_integral,
        0.0,
        math.pi / 2.0,
        epsabs=1e-10,
        epsrel=1e-10,
        limit=200,
    )[0]
    return (2.0 / math.pi) * quarter_integral


def main() -> int:
    checks = CheckLedger("P091-INDEPENDENT")
    frequencies = (0.9, 0.7, 0.5, 0.1)
    direct_means = {omega: direct_mean_kinetic(omega) for omega in frequencies}
    expected_means = {
        omega: 16.0 * omega * math.acos(omega) for omega in frequencies
    }
    direct_form_factors = {
        omega: direct_means[omega] / (16.0 * math.sqrt(1.0 - omega**2))
        for omega in frequencies
    }
    expected_form_factors = {
        omega: omega * math.acos(omega) / math.sqrt(1.0 - omega**2)
        for omega in frequencies
    }
    checks.check(
        "independent field quadrature reproduces the mean kinetic identity",
        all(
            abs(direct_means[omega] - expected_means[omega]) < 2e-9
            for omega in frequencies
        ),
    )
    checks.check(
        "independent field quadrature reproduces the closed form factor",
        all(
            abs(direct_form_factors[omega] - expected_form_factors[omega]) < 2e-10
            for omega in frequencies
        ),
    )
    checks.check(
        "canonical APIs agree with the independently integrated field",
        all(
            abs(
                float(breather_mean_kinetic_integral(omega))
                - direct_means[omega]
            )
            < 2e-9
            and abs(
                float(breather_damping_form_factor(omega))
                - direct_form_factors[omega]
            )
            < 2e-10
            for omega in frequencies
        ),
    )
    checks.check(
        "independent samples have the exact monotone ordering",
        all(
            direct_form_factors[frequencies[index]]
            > direct_form_factors[frequencies[index + 1]]
            for index in range(len(frequencies) - 1)
        ),
    )

    omega_initial = 1.0 / math.sqrt(2.0)
    theta_initial = math.acos(omega_initial)
    gamma = 0.02
    action_initial = 16.0 * theta_initial
    integration = solve_ivp(
        lambda _time, state: -gamma * state,
        (0.0, 100.0),
        np.asarray([action_initial]),
        method="DOP853",
        rtol=1e-12,
        atol=1e-13,
        dense_output=True,
    )
    checks.check("independent action IVP solver exits successfully", integration.success)
    checks.check(
        "independent action IVP agrees with the analytic exponential",
        max(
            abs(
                float(integration.sol(time)[0])
                - action_initial * math.exp(-gamma * time)
            )
            for time in np.linspace(0.0, 100.0, 21)
        )
        < 2e-11,
    )

    initial_energy = 16.0 * math.sin(theta_initial)

    def reduced_energy(time: float) -> float:
        action = float(integration.sol(time)[0])
        return 16.0 * math.sin(action / 16.0)

    numeric_efold = brentq(
        lambda time: reduced_energy(time) - initial_energy / math.e,
        0.0,
        100.0,
        xtol=1e-13,
        rtol=1e-14,
    )
    canonical_efold = float(
        phase_averaged_breather_energy_efold_time(omega_initial, gamma)
    )
    instantaneous_time = 1.0 / (
        gamma
        * omega_initial
        * math.acos(omega_initial)
        / math.sqrt(1.0 - omega_initial**2)
    )
    checks.check(
        "independent root solve reproduces the integrated e-fold API",
        abs(numeric_efold - canonical_efold) < 2e-10,
    )
    checks.check(
        "integrated e-fold precedes the frozen initial tangent time",
        numeric_efold < instantaneous_time
        and gamma * (instantaneous_time - numeric_efold) > 0.1,
    )
    checks.mutation_sensitive(
        "energy crossing rejects frozen-D and small-amplitude times",
        lambda candidate_time: abs(
            reduced_energy(float(candidate_time)) / initial_energy - 1.0 / math.e
        )
        < 2e-11,
        numeric_efold,
        (instantaneous_time, 1.0 / gamma),
    )
    checks.mutation_sensitive(
        "field integral rejects a factor-two action normalization",
        lambda factor: all(
            abs(factor * expected_means[omega] - direct_means[omega]) < 2e-9
            for omega in frequencies
        ),
        1.0,
        (0.5, 2.0),
    )

    print("direct form factors:", direct_form_factors)
    print(
        "dimensionless e-fold times:",
        {"integrated": gamma * numeric_efold, "initial_tangent": gamma * instantaneous_time},
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
