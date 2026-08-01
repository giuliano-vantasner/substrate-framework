#!/usr/bin/env python3
"""Exact coefficient and geometry audit for CF2 fixed-flux linearity."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.flux_tube import (
    charge_for_slope_equality,
    endpoint_force_slope,
    endpoint_potential,
    spherical_field,
    tube_energy_slope,
    tube_field_energy,
    uniform_tube_field,
)
from substrate_framework.verification import CheckLedger


CF2_SHA256 = "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a"


@dataclass(frozen=True)
class EnergyConvention:
    coefficient: sp.Expr
    area_power: sp.Expr


def run(source_file: Path) -> int:
    checks = CheckLedger("C-FLX-001")
    checks.check(
        "the audited CF2 source is the hash-pinned candidate unit",
        hashlib.sha256(source_file.read_bytes()).hexdigest() == CF2_SHA256,
    )

    flux, area, charge, length = sp.symbols("Phi A q L", positive=True)
    field = uniform_tube_field(flux, area)
    checks.check(
        "uniform-cap Gauss data recover flux exactly",
        field == flux / area and sp.simplify(field * area - flux) == 0,
    )
    checks.check(
        "fixed area makes the declared tube field length-independent",
        sp.diff(field, length) == 0 and length not in field.free_symbols,
    )

    energy_slope = tube_energy_slope(flux, area)
    energy = tube_field_energy(length, flux, area)
    checks.check(
        "field energy is exactly linear with slope Phi squared over two A",
        energy_slope == flux**2 / (2 * area)
        and energy == energy_slope * length
        and sp.diff(energy, length) == energy_slope
        and sp.diff(energy, length, 2) == 0,
    )

    def energy_convention_matches(candidate: EnergyConvention) -> bool:
        candidate_field = flux / area**candidate.area_power
        recovered = sp.simplify(candidate_field * area)
        candidate_slope = sp.simplify(
            candidate.coefficient * candidate_field**2 * area
        )
        return recovered == flux and candidate_slope == flux**2 / (2 * area)

    checks.mutation_sensitive(
        "Gauss area power and field-energy one-half",
        energy_convention_matches,
        EnergyConvention(sp.Rational(1, 2), 1),
        [
            EnergyConvention(1, 1),
            EnergyConvention(sp.Rational(1, 4), 1),
            EnergyConvention(sp.Rational(1, 2), 2),
        ],
    )

    force_slope = endpoint_force_slope(charge, flux, area)
    endpoint_work = endpoint_potential(length, charge, flux, area)
    checks.check(
        "endpoint work is separately linear with slope q Phi over A",
        force_slope == charge * flux / area
        and endpoint_work == force_slope * length
        and sp.diff(endpoint_work, length) == force_slope
        and sp.diff(endpoint_work, length, 2) == 0,
    )
    equality_charge = sp.solve(sp.Eq(energy_slope, force_slope), charge)
    checks.check(
        "energy and endpoint slopes agree iff q equals Phi over two",
        equality_charge == [flux / 2]
        and charge_for_slope_equality(flux) == flux / 2,
    )
    checks.check(
        "the natural q equals Phi assignment is a factor-two counterexample",
        endpoint_force_slope(flux, flux, area) == 2 * energy_slope,
    )
    checks.mutation_sensitive(
        "charge-flux equality condition",
        lambda candidate: sp.simplify(
            endpoint_force_slope(candidate, flux, area) - energy_slope
        )
        == 0,
        flux / 2,
        [flux, flux / 4],
    )

    reference_area, reference_length = sp.symbols("A0 L0", positive=True)
    variable_area = reference_area * (1 + length / reference_length)
    variable_field = sp.simplify(flux / variable_area)
    local_energy_slope = sp.simplify(flux**2 / (2 * variable_area))
    ell = sp.symbols("ell", positive=True)
    variable_energy = sp.integrate(
        local_energy_slope,
        (length, 0, ell),
    )
    checks.check(
        "a length-dependent area destroys constant field and linear energy",
        sp.diff(variable_field, length) != 0
        and sp.diff(variable_energy, ell, 2) != 0,
    )
    checks.check(
        "the expanding-area energy is logarithmic rather than linear",
        sp.simplify(
            variable_energy
            - flux**2
            * reference_length
            * sp.log(1 + ell / reference_length)
            / (2 * reference_area)
        )
        == 0,
    )

    radius = sp.symbols("r", positive=True)
    radial_field = spherical_field(flux, radius)
    coulomb_potential = charge * flux / (4 * sp.pi * radius)
    checks.check(
        "spherical spreading gives a nonconstant inverse-square field",
        radial_field == flux / (4 * sp.pi * radius**2)
        and sp.diff(radial_field, radius) != 0,
    )
    checks.check(
        "the corresponding Coulomb potential is curved and vanishes at infinity",
        sp.diff(coulomb_potential, radius, 2) != 0
        and sp.limit(coulomb_potential, radius, sp.oo) == 0,
    )

    tension = sp.symbols("sigma", positive=True)
    effective_area = sp.simplify(flux**2 / (2 * tension))
    checks.check(
        "matching a separate tension only defines an effective area",
        sp.simplify(tube_energy_slope(flux, effective_area) - tension) == 0
        and sp.diff(effective_area, tension) != 0,
    )
    checks.check(
        "CF2 never checks the declared endpoint charge in its tube-energy path",
        charge not in energy.free_symbols and charge not in energy_slope.free_symbols,
    )

    total = checks.finish()
    print(f"P027 CF2 FIXED-FLUX AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
