#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed C-SG-008."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.sine_gordon import (
    boosted_breather_energy_momentum,
    boosted_breather_phase_components,
    breather_energy,
    breather_secant_action_scale,
    lorentz_factor,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class BoostCandidate:
    phase_frequency_factor: int
    wave_sign: int
    energy_factor: int
    momentum_gamma_power: int


def boost_candidate_is_exact(candidate: BoostCandidate) -> bool:
    omega = sp.symbols("omega", positive=True)
    velocity = sp.symbols("v", real=True)
    gamma = 1 / sp.sqrt(1 - velocity**2)
    rest_energy = 16 * sp.sqrt(1 - omega**2)
    scale = rest_energy / omega
    phase = (
        candidate.phase_frequency_factor * gamma * omega,
        candidate.wave_sign * gamma * omega * velocity,
    )
    energy_momentum = (
        candidate.energy_factor * gamma * rest_energy,
        gamma**candidate.momentum_gamma_power * rest_energy * velocity,
    )
    return (
        sp.simplify(energy_momentum[0] - scale * phase[0]) == 0
        and sp.simplify(energy_momentum[1] - scale * phase[1]) == 0
        and sp.simplify(phase[0] ** 2 - phase[1] ** 2 - omega**2) == 0
        and sp.simplify(
            energy_momentum[0] ** 2
            - energy_momentum[1] ** 2
            - rest_energy**2
        )
        == 0
    )


def run() -> int:
    checks = CheckLedger("C-SG-008")
    omega = sp.symbols("omega", positive=True)
    velocity = sp.symbols("v", real=True, nonzero=True)
    gamma = lorentz_factor(velocity)
    rest_energy = breather_energy(omega)
    scale = breather_secant_action_scale(omega)
    phase = boosted_breather_phase_components(omega, velocity)
    energy_momentum = boosted_breather_energy_momentum(omega, velocity)

    checks.check(
        "the Lorentz factor satisfies the exact boost normalization",
        sp.simplify(gamma**2 * (1 - velocity**2) - 1) == 0,
    )
    checks.check(
        "the boosted phase components follow from omega*gamma*(t-v*x)",
        sp.simplify(phase[0] - gamma * omega) == 0
        and sp.simplify(phase[1] - gamma * omega * velocity) == 0,
    )
    checks.check(
        "the boosted energy-momentum components follow the same Lorentz boost",
        sp.simplify(energy_momentum[0] - gamma * rest_energy) == 0
        and sp.simplify(
            energy_momentum[1] - gamma * rest_energy * velocity
        )
        == 0,
    )
    checks.check(
        "the full vectors are proportional by the accepted secant action scale",
        sp.simplify(energy_momentum[0] - scale * phase[0]) == 0
        and sp.simplify(energy_momentum[1] - scale * phase[1]) == 0,
    )
    checks.check(
        "the phase covector retains its rest-frequency invariant norm",
        sp.simplify(phase[0] ** 2 - phase[1] ** 2 - omega**2) == 0,
    )
    checks.check(
        "energy-momentum retains the accepted rest-energy invariant norm",
        sp.simplify(
            energy_momentum[0] ** 2
            - energy_momentum[1] ** 2
            - rest_energy**2
        )
        == 0,
    )
    checks.check(
        "the component-ratio form is a nonzero-velocity corollary",
        sp.simplify(energy_momentum[0] / phase[0] - scale) == 0
        and sp.simplify(energy_momentum[1] / phase[1] - scale) == 0,
    )
    checks.check(
        "phase velocity and the boost-family group derivative have the expected values",
        sp.simplify(phase[0] / phase[1] - 1 / velocity) == 0
        and sp.simplify(
            sp.diff(phase[0], velocity) / sp.diff(phase[1], velocity)
            - velocity
        )
        == 0,
    )

    rest_phase = boosted_breather_phase_components(omega, 0)
    rest_momentum = boosted_breather_energy_momentum(omega, 0)
    checks.check(
        "vector proportionality remains well defined in the rest limit",
        rest_phase == (omega, 0)
        and rest_momentum == (rest_energy, 0)
        and sp.simplify(rest_momentum[0] - scale * rest_phase[0]) == 0,
    )

    wrong_frequency = omega / gamma
    wrong_momentum = rest_energy * velocity
    checks.check(
        "a time-dilated frequency breaks the energy component proportionality",
        sp.simplify(energy_momentum[0] - scale * wrong_frequency) != 0,
    )
    checks.check(
        "a momentum missing the Lorentz factor breaks the spatial proportionality",
        sp.simplify(wrong_momentum - scale * phase[1]) != 0,
    )
    checks.mutation_sensitive(
        "phase frequency, wave sign, energy normalization, and momentum boost",
        boost_candidate_is_exact,
        BoostCandidate(1, 1, 1, 1),
        [
            BoostCandidate(2, 1, 1, 1),
            BoostCandidate(1, -1, 1, 1),
            BoostCandidate(1, 1, 2, 1),
            BoostCandidate(1, 1, 1, 0),
        ],
    )

    total = checks.finish()
    print(f"P012 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
