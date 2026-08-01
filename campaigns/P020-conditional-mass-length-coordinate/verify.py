#!/usr/bin/env python3
"""Exact conditional unit-product verifier and EL3 scope audit."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.dimensional_analysis import (
    dimensionless_mass_coordinate,
    mass_coordinate_from_unit_product,
    mass_from_dimensionless_coordinate,
)
from substrate_framework.verification import CheckLedger


EL3_SHA256 = "ab4549b5c147113beec18c2513a42dfbdd34c25ad21d125dfa6d8e9d9f0de69d"


@dataclass(frozen=True)
class UnitProductCandidate:
    product_coefficient: sp.Expr
    mass_energy_coefficient: sp.Expr
    coupling_power: int


def candidate_is_exact(candidate: UnitProductCandidate) -> bool:
    coupling = sp.symbols("e", positive=True)
    coordinate = sp.simplify(
        candidate.product_coefficient
        / (candidate.mass_energy_coefficient * coupling**candidate.coupling_power)
    )
    return coordinate == 1 / (8 * sp.pi * coupling**2)


def run(source_file: Path) -> int:
    checks = CheckLedger("C-DIM-004")
    payload = source_file.read_bytes()
    checks.check(
        "the audited EL3 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == EL3_SHA256,
    )

    pion_scale, coupling, action, speed, length = sp.symbols(
        "F_pi e S c0 L", positive=True
    )
    natural_unit = pion_scale / (4 * coupling)
    natural_length = 2 / (coupling * pion_scale)
    checks.check(
        "the two declared Skyrme formulas have the exact natural-unit product",
        sp.simplify(natural_unit * natural_length - 1 / (2 * coupling**2))
        == 0,
    )

    unit = sp.symbols("U", positive=True)
    mass = sp.symbols("m", positive=True)
    product_equation = sp.Eq(
        unit * length,
        action * speed / (2 * coupling**2),
    )
    energy_equation = sp.Eq(unit, 4 * sp.pi * mass * speed**2)
    solved_mass = sp.solve(
        [product_equation, energy_equation],
        [unit, mass],
        dict=True,
    )[0][mass]
    checks.check(
        "stepwise elimination gives the exact conditional mass",
        solved_mass == action / (8 * sp.pi * coupling**2 * length * speed),
    )

    coordinate = mass_coordinate_from_unit_product(
        coupling,
        sp.Rational(1, 2),
        4 * sp.pi,
    )
    checks.check(
        "the declared coefficients give the exact C-DIM-003 coordinate",
        coordinate == 1 / (8 * sp.pi * coupling**2)
        and dimensionless_mass_coordinate(solved_mass, speed, action, length)
        == coordinate,
    )
    checks.check(
        "the inverse coordinate API reconstructs the conditional mass",
        mass_from_dimensionless_coordinate(coordinate, speed, action, length)
        == solved_mass,
    )
    checks.check(
        "the equivalent reduced-wavelength relation follows exactly",
        sp.simplify(action / (solved_mass * speed) - 8 * sp.pi * coupling**2 * length)
        == 0,
    )
    checks.check(
        "the dimensionless coupling remains a load-bearing input",
        sp.diff(coordinate, coupling) == -1 / (4 * sp.pi * coupling**3)
        and coupling in coordinate.free_symbols,
    )

    checks.mutation_sensitive(
        "unit-product coefficient, mass-energy coefficient, and coupling power",
        candidate_is_exact,
        UnitProductCandidate(sp.Rational(1, 2), 4 * sp.pi, 2),
        [
            UnitProductCandidate(1, 4 * sp.pi, 2),
            UnitProductCandidate(sp.Rational(1, 2), 2 * sp.pi, 2),
            UnitProductCandidate(sp.Rational(1, 2), 4 * sp.pi, 1),
            UnitProductCandidate(sp.Rational(1, 4), 4 * sp.pi, 2),
        ],
    )

    arbitrary_factor = sp.Function("f")(coupling)
    alternate_mass = arbitrary_factor * action / (speed * length)
    checks.check(
        "dimensional uniqueness does not select the coupling-dependent coefficient",
        coupling in alternate_mass.free_symbols
        and sp.diff(alternate_mass, arbitrary_factor) == action / (speed * length),
    )

    before = sp.Matrix(
        [
            [0, 1, 0, 1],
            [1, 2, 1, 0],
            [-1, -1, 0, 0],
        ]
    )
    after = before[:, :3]
    checks.check(
        "adding the mass column creates one dimensionless coordinate",
        before.rank() == after.rank() == 3
        and len(before.nullspace()) == 1
        and before.nullspace()[0] == sp.Matrix([1, -1, 1, 1])
        and after.nullspace() == [],
    )

    proton_mass, shape = sp.symbols("m_p b", positive=True)
    moved_import = proton_mass / (48 * sp.pi**3 * shape * speed**2)
    checks.check(
        "EL3's coupling-free form moves rather than eliminates free inputs",
        sp.diff(moved_import, proton_mass) != 0
        and sp.diff(moved_import, shape) != 0
        and {proton_mass, shape} <= moved_import.free_symbols,
    )

    total = checks.finish()
    print(f"P020 EL3 EXACT AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
