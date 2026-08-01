#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed claim C-RG-001."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.radial_energy import (
    capillary_critical_radius,
    capillary_energy,
    line_energy,
    spherical_shell_energy,
)
from substrate_framework.sine_gordon import breather_energy
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class LineCandidate:
    circumference_factor: int
    radial_power: int


def is_declared_line_energy(candidate: LineCandidate) -> bool:
    radius, density, scale = sp.symbols("R lambda a", positive=True)
    energy = candidate.circumference_factor * sp.pi * radius ** candidate.radial_power * density
    declared = 2 * sp.pi * radius * density
    return (
        sp.simplify(energy - declared) == 0
        and sp.simplify(energy.subs(radius, scale * radius) - scale * energy) == 0
        and radius not in sp.diff(energy, radius).free_symbols
    )


def line_coefficients_give_identity(candidate_tension: sp.Expr) -> bool:
    radius, omega = sp.symbols("R omega", positive=True)
    breather_density = 16 * sp.sqrt(1 - omega**2)
    return sp.simplify(
        2 * sp.pi * radius * candidate_tension
        - 2 * sp.pi * radius * breather_density
    ) == 0


def capillary_candidate_is_maximum(pressure_multiplier: int) -> bool:
    radius, tension, pressure = sp.symbols("R T P", positive=True)
    drive = pressure_multiplier * pressure
    energy = 2 * sp.pi * radius * tension - sp.pi * radius**2 * drive
    stationary = tension / drive if drive != 0 else sp.nan
    return (
        drive != 0
        and sp.simplify(sp.diff(energy, radius).subs(radius, stationary)) == 0
        and sp.diff(energy, radius, 2).is_negative is True
    )


def run() -> int:
    checks = CheckLedger("C-RG-001")
    radius, density, surface_density, scale = sp.symbols(
        "R lambda sigma a", positive=True
    )
    tension, pressure = sp.symbols("T P", positive=True)
    core = sp.symbols("E_core", real=True)

    line = line_energy(radius, density)
    shell = spherical_shell_energy(radius, surface_density)
    full_capillary = capillary_energy(radius, tension, pressure, core)

    checks.check(
        "circumference line energy is exactly homogeneous of degree one",
        sp.simplify(line.subs(radius, scale * radius) - scale * line) == 0,
    )
    checks.check(
        "line energy obeys the degree-one Euler identity",
        sp.simplify(radius * sp.diff(line, radius) - line) == 0,
    )
    checks.check(
        "line marginal energy is constant in radius and positive",
        sp.diff(line, radius) == 2 * sp.pi * density
        and radius not in sp.diff(line, radius).free_symbols
        and sp.diff(line, radius).is_positive is True,
    )
    checks.check(
        "positive line energy has no stationary radius",
        sp.solve(sp.Eq(sp.diff(line, radius), 0), radius) == [],
    )

    checks.check(
        "spherical-shell energy is exactly homogeneous of degree two",
        sp.simplify(shell.subs(radius, scale * radius) - scale**2 * shell) == 0,
    )
    checks.check(
        "shell energy obeys the degree-two Euler identity",
        sp.simplify(radius * sp.diff(shell, radius) - 2 * shell) == 0,
    )
    checks.check(
        "shell marginal energy carries an explicit radius factor",
        sp.diff(shell, radius) == 8 * sp.pi * radius * surface_density
        and radius in sp.diff(shell, radius).free_symbols,
    )
    checks.check(
        "the shell fails the degree-one line predicate",
        sp.simplify(shell.subs(radius, scale * radius) - scale * shell) != 0,
    )

    scaling_residual = sp.factor(
        full_capillary.subs(radius, scale * radius) - scale * full_capillary
    )
    expected_residual = sp.factor(
        (1 - scale) * core
        + sp.pi * pressure * radius**2 * scale * (1 - scale)
    )
    checks.check(
        "the full capillary form is not the isolated homogeneous line term",
        sp.simplify(scaling_residual - expected_residual) == 0
        and scaling_residual != 0,
    )
    critical = capillary_critical_radius(tension, pressure)
    checks.check(
        "the positive-pressure capillary energy has stationary radius T/P",
        critical == tension / pressure
        and sp.simplify(sp.diff(full_capillary, radius).subs(radius, critical)) == 0,
    )
    capillary_peak = sp.simplify(full_capillary.subs(radius, critical))
    checks.check(
        "the capillary stationary radius is the unique strict global maximum",
        sp.diff(full_capillary, radius, 2) == -2 * sp.pi * pressure
        and sp.simplify(
            capillary_peak
            - full_capillary
            - sp.pi * pressure * (radius - critical) ** 2
        )
        == 0,
    )

    omega = sp.symbols("omega", positive=True)
    breather_density = breather_energy(omega)
    breather_ring = line_energy(radius, breather_density)
    checks.check(
        "the conditional breather ring uses the accepted C-SG-002 coefficient",
        sp.simplify(
            breather_ring
            - 32 * sp.pi * radius * sp.sqrt(1 - omega**2)
        )
        == 0,
    )
    checks.check(
        "the conditional breather line has the accepted endpoint limits",
        sp.limit(breather_ring, omega, 0, dir="+") == 32 * sp.pi * radius
        and sp.limit(breather_ring, omega, 1, dir="-") == 0,
    )

    line_difference = sp.factor(
        line_energy(radius, tension) - breather_ring
    )
    checks.check(
        "the two line instantiations differ only by their independent densities",
        sp.simplify(
            line_difference - 2 * sp.pi * radius * (tension - breather_density)
        )
        == 0,
    )
    checks.check(
        "equality of both line energies is equivalent to explicit coefficient equality",
        sp.solve(sp.Eq(line_difference, 0), tension) == [breather_density],
    )

    checks.mutation_sensitive(
        "circumference factor and radial degree",
        is_declared_line_energy,
        LineCandidate(2, 1),
        [LineCandidate(4, 1), LineCandidate(2, 0), LineCandidate(2, 2)],
    )
    checks.mutation_sensitive(
        "coefficient equality must be explicit",
        line_coefficients_give_identity,
        16 * sp.sqrt(1 - omega**2),
        [tension, 32 * sp.sqrt(1 - omega**2)],
    )
    checks.mutation_sensitive(
        "capillary critical point is a maximum only for positive drive",
        capillary_candidate_is_maximum,
        1,
        [-1, 0],
    )

    total = checks.finish()
    print(f"P006 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
