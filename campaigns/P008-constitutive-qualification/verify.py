#!/usr/bin/env python3
"""Exact, comparator-free verifier for proposed C-MED-001 and C-SK-001."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp
from sympy.physics import units as units
from sympy.physics.units.systems.si import SI

from substrate_framework.constitutive import (
    co_scaled_inverse_permeability,
    co_scaled_permittivity,
    co_scaled_wave_speed,
)
from substrate_framework.skyrme_relations import (
    conditional_anw_mass,
    conditional_topological_mass,
    matched_pion_coupling_ratio,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class ResponseExponents:
    epsilon_density: int
    inverse_mu_density: int
    epsilon_thermal: int
    inverse_mu_thermal: int


def response_speed_is_scale_independent(
    candidate: ResponseExponents,
) -> bool:
    density, thermal, speed = sp.symbols("rho Theta c", positive=True)
    epsilon = (
        density**candidate.epsilon_density
        * thermal**candidate.epsilon_thermal
        / speed**2
    )
    inverse_mu = (
        density**candidate.inverse_mu_density
        * thermal**candidate.inverse_mu_thermal
    )
    wave_speed = sp.sqrt(inverse_mu / epsilon)
    density_sensitivity = sp.simplify(
        density * sp.diff(sp.log(wave_speed), density)
    )
    thermal_sensitivity = sp.simplify(
        thermal * sp.diff(sp.log(wave_speed), thermal)
    )
    return density_sensitivity == 0 and thermal_sensitivity == 0


@dataclass(frozen=True)
class MassFormulaCandidate:
    topological_prefactor: int
    anw_prefactor: int
    topological_b1_power: int
    anw_b1_power: int


def mass_match_gives_declared_ratio(candidate: MassFormulaCandidate) -> bool:
    coefficient, rest_energy, ratio = sp.symbols(
        "B1 E_e ratio", positive=True
    )
    topological_mass = (
        candidate.topological_prefactor
        * sp.pi**3
        * coefficient**candidate.topological_b1_power
        * rest_energy
    )
    anw_mass = (
        candidate.anw_prefactor
        * sp.pi**2
        * coefficient**candidate.anw_b1_power
        * ratio
    )
    solutions = sp.solve(sp.Eq(anw_mass, topological_mass), ratio)
    return (
        solutions == [16 * sp.pi * rest_energy]
        and coefficient not in solutions[0].free_symbols
    )


def run() -> int:
    medium_checks = CheckLedger("C-MED-001")
    skyrme_checks = CheckLedger("C-SK-001")

    density, thermal, speed = sp.symbols("rho Theta c", positive=True)
    epsilon = co_scaled_permittivity(density, thermal, speed)
    inverse_mu = co_scaled_inverse_permeability(density, thermal)
    wave_speed = co_scaled_wave_speed(density, thermal, speed)
    medium_checks.check(
        "the declared responses have exact product epsilon*mu=1/c^2",
        sp.simplify(epsilon / inverse_mu - 1 / speed**2) == 0,
    )
    medium_checks.check(
        "common density and thermal factors cancel from local wave speed",
        wave_speed == speed,
    )
    medium_checks.check(
        "both logarithmic scale sensitivities vanish exactly",
        sp.simplify(density * sp.diff(sp.log(wave_speed), density)) == 0
        and sp.simplify(thermal * sp.diff(sp.log(wave_speed), thermal)) == 0,
    )
    medium_checks.check(
        "density and thermal gradients cannot source an index within this ansatz",
        sp.diff(wave_speed, density) == 0
        and sp.diff(wave_speed, thermal) == 0,
    )
    medium_checks.mutation_sensitive(
        "matched response exponents are load-bearing",
        response_speed_is_scale_independent,
        ResponseExponents(1, 1, 1, 1),
        [
            ResponseExponents(1, 2, 1, 1),
            ResponseExponents(1, 1, 1, 2),
            ResponseExponents(2, 1, 1, 1),
        ],
    )

    coefficient, rest_energy, pion_scale, coupling = sp.symbols(
        "B1 E_e F_pi e", positive=True
    )
    topological_mass = conditional_topological_mass(
        coefficient, rest_energy
    )
    anw_mass = conditional_anw_mass(
        coefficient, pion_scale, coupling
    )
    solved_pion_scale = sp.solve(
        sp.Eq(anw_mass, topological_mass), pion_scale
    )
    skyrme_checks.check(
        "matching the two conditional premises solves F_pi exactly",
        solved_pion_scale
        == [16 * sp.pi * coupling * rest_energy],
    )
    solved_ratio = sp.simplify(solved_pion_scale[0] / coupling)
    skyrme_checks.check(
        "the matched conditional ratio is 16*pi times electron rest energy",
        solved_ratio == matched_pion_coupling_ratio(rest_energy),
    )
    skyrme_checks.check(
        "the shared hedgehog coefficient cancels exactly",
        coefficient not in solved_ratio.free_symbols,
    )
    skyrme_checks.check(
        "substitution of the ratio proves the reverse implication",
        sp.simplify(
            topological_mass
            - anw_mass.subs(
                pion_scale,
                coupling * matched_pion_coupling_ratio(rest_energy),
            )
        )
        == 0,
    )

    ratio_with_units = matched_pion_coupling_ratio(
        units.electron_rest_mass * units.speed_of_light**2
    )
    dimension_system = SI.get_dimension_system()
    ratio_dimension = dimension_system.get_dimensional_dependencies(
        SI.get_dimensional_expr(ratio_with_units)
    )
    energy_dimension = dimension_system.get_dimensional_dependencies(
        SI.get_dimensional_expr(units.joule)
    )
    skyrme_checks.check(
        "the conditional ratio has energy dimension",
        ratio_dimension == energy_dimension,
    )
    skyrme_checks.mutation_sensitive(
        "both prefactors and shared B1 powers are load-bearing",
        mass_match_gives_declared_ratio,
        MassFormulaCandidate(48, 3, 1, 1),
        [
            MassFormulaCandidate(24, 3, 1, 1),
            MassFormulaCandidate(48, 6, 1, 1),
            MassFormulaCandidate(48, 3, 2, 1),
            MassFormulaCandidate(48, 3, 1, 2),
        ],
    )

    medium_total = medium_checks.finish()
    skyrme_total = skyrme_checks.finish()
    total = medium_total + skyrme_total
    print(f"P008 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
