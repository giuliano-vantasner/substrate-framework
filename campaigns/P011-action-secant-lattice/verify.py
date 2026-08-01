#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed C-SG-006/007."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.sine_gordon import (
    breather_action,
    breather_action_lattice_adjacent_gap,
    breather_action_lattice_energy,
    breather_action_lattice_frequency,
    breather_action_secant_ratio,
    breather_energy,
    breather_secant_action_scale,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class SecantCandidate:
    energy_coefficient: int
    frequency_power: int
    action_coefficient: int


def secant_candidate_is_exact(candidate: SecantCandidate) -> bool:
    omega = sp.symbols("omega", positive=True)
    width = sp.sqrt(1 - omega**2)
    scale = (
        candidate.energy_coefficient
        * width
        / omega**candidate.frequency_power
    )
    action = candidate.action_coefficient * sp.acos(omega)
    expected_scale = 16 * width / omega
    expected_ratio = omega * sp.acos(omega) / width
    return (
        sp.simplify(scale - expected_scale) == 0
        and sp.simplify(action / scale - expected_ratio) == 0
    )


@dataclass(frozen=True)
class LatticeCandidate:
    energy_coefficient: int
    angle_denominator: int
    next_offset: int


def lattice_candidate_is_exact(candidate: LatticeCandidate) -> bool:
    level = sp.symbols("n", positive=True, integer=True)
    quantum = sp.symbols("h", positive=True)
    angle = level * quantum / candidate.angle_denominator
    energy = candidate.energy_coefficient * sp.sin(angle)
    frequency = sp.cos(angle)
    next_energy = candidate.energy_coefficient * sp.sin(
        (level + candidate.next_offset)
        * quantum
        / candidate.angle_denominator
    )
    gap = sp.simplify(next_energy - energy)
    expected_energy = 16 * sp.sin(level * quantum / 16)
    expected_frequency = sp.cos(level * quantum / 16)
    expected_gap = 32 * sp.sin(quantum / 32) * sp.cos(
        (2 * level + 1) * quantum / 32
    )
    return (
        sp.simplify(energy - expected_energy) == 0
        and sp.simplify(frequency - expected_frequency) == 0
        and sp.trigsimp(gap - expected_gap) == 0
    )


def run() -> int:
    secant_checks = CheckLedger("C-SG-006")
    lattice_checks = CheckLedger("C-SG-007")
    omega = sp.symbols("omega", positive=True)
    width = sp.sqrt(1 - omega**2)
    energy = breather_energy(omega)
    action = breather_action(omega)
    scale = breather_secant_action_scale(omega)
    ratio = breather_action_secant_ratio(omega)

    secant_checks.check(
        "the energy-frequency secant scale has the exact closed form",
        sp.simplify(scale - 16 * width / omega) == 0,
    )
    secant_checks.check(
        "the secant scale is strictly decreasing across the open family",
        sp.simplify(sp.diff(scale, omega) + 16 / (omega**2 * width))
        == 0,
    )
    secant_checks.check(
        "the secant scale spans positive infinity down to zero",
        sp.limit(scale, omega, 0, dir="+") == sp.oo
        and sp.limit(scale, omega, 1, dir="-") == 0,
    )
    secant_checks.check(
        "the canonical-action to secant-scale ratio has the exact form",
        sp.simplify(ratio - omega * sp.acos(omega) / width) == 0,
    )
    secant_checks.check(
        "the ratio has endpoint limits zero and one",
        sp.limit(ratio, omega, 0, dir="+") == 0
        and sp.limit(ratio, omega, 1, dir="-") == 1,
    )

    positive_numerator = sp.acos(omega) - omega * width
    secant_checks.check(
        "the ratio derivative numerator decreases to zero at the upper endpoint",
        sp.simplify(sp.diff(positive_numerator, omega) + 2 * width) == 0
        and sp.limit(positive_numerator, omega, 1, dir="-") == 0,
    )
    secant_checks.check(
        "the ratio derivative is positive on the open family",
        sp.simplify(
            sp.diff(ratio, omega) - positive_numerator / width**3
        )
        == 0,
    )
    secant_checks.check(
        "the secant derivative gives omega cubed rather than the canonical frequency",
        sp.simplify(sp.diff(energy, omega) / sp.diff(scale, omega) - omega**3)
        == 0
        and sp.simplify(omega**3 - omega + omega * width**2) == 0,
    )
    secant_checks.mutation_sensitive(
        "energy coefficient, frequency power, and action coefficient",
        secant_candidate_is_exact,
        SecantCandidate(16, 1, 16),
        [
            SecantCandidate(8, 1, 16),
            SecantCandidate(16, 2, 16),
            SecantCandidate(16, 1, 8),
        ],
    )

    level = sp.symbols("n", positive=True, integer=True)
    quantum = sp.symbols("h", positive=True)
    lattice_energy = breather_action_lattice_energy(level, quantum)
    lattice_frequency = breather_action_lattice_frequency(level, quantum)
    adjacent_gap = breather_action_lattice_adjacent_gap(level, quantum)
    lattice_checks.check(
        "an imposed fixed action lattice gives the exact sine energy",
        sp.simplify(lattice_energy - 16 * sp.sin(level * quantum / 16))
        == 0,
    )
    lattice_checks.check(
        "the corresponding frequency is the exact cosine inverse map",
        sp.simplify(
            lattice_frequency - sp.cos(level * quantum / 16)
        )
        == 0,
    )
    lattice_checks.check(
        "the accepted open action range is equivalent to the strict level cutoff",
        sp.simplify(
            (8 * sp.pi - level * quantum) / quantum
            - (8 * sp.pi / quantum - level)
        )
        == 0,
    )

    continuous_level = sp.symbols("nu", positive=True)
    interpolated_energy = 16 * sp.sin(continuous_level * quantum / 16)
    interpolated_frequency = sp.cos(continuous_level * quantum / 16)
    lattice_checks.check(
        "the continuous interpolation derivative is h times its frequency",
        sp.simplify(
            sp.diff(interpolated_energy, continuous_level)
            - quantum * interpolated_frequency
        )
        == 0,
    )
    expected_gap = 32 * sp.sin(quantum / 32) * sp.cos(
        (2 * level + 1) * quantum / 32
    )
    lattice_checks.check(
        "the true adjacent level gap is the exact trigonometric finite difference",
        sp.trigsimp(adjacent_gap - expected_gap) == 0,
    )
    lattice_checks.check(
        "the adjacent gap is not the continuous derivative at the lower level",
        sp.simplify(
            adjacent_gap.subs({level: 2, quantum: sp.pi})
            - (
                quantum
                * sp.cos(level * quantum / 16)
            ).subs({level: 2, quantum: sp.pi})
        )
        != 0,
    )
    midpoint_frequency = sp.cos((2 * level + 1) * quantum / 32)
    lattice_checks.check(
        "the adjacent gap approaches h times the midpoint frequency for a fine lattice",
        sp.limit(
            adjacent_gap / (quantum * midpoint_frequency),
            quantum,
            0,
            dir="+",
        )
        == 1,
    )
    lattice_checks.mutation_sensitive(
        "energy coefficient, action angle, and adjacent-level offset",
        lattice_candidate_is_exact,
        LatticeCandidate(16, 16, 1),
        [
            LatticeCandidate(8, 16, 1),
            LatticeCandidate(16, 8, 1),
            LatticeCandidate(16, 16, 2),
        ],
    )

    secant_total = secant_checks.finish()
    lattice_total = lattice_checks.finish()
    print(f"P011 ALL {secant_total + lattice_total} CHECKS PASS")
    return secant_total + lattice_total


if __name__ == "__main__":
    run()
