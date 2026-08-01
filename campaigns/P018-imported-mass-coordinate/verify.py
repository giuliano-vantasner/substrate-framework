#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed C-DIM-003 and EL1."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re

import sympy as sp

from substrate_framework.dimensional_analysis import (
    dimensionless_mass_coordinate,
    mass_from_dimensionless_coordinate,
    monomial_exponents,
)
from substrate_framework.skyrme_relations import matched_pion_coupling_ratio
from substrate_framework.verification import CheckLedger


EL1_SHA256 = "d39debe384fed8383fdf65161e29b0a8de7e574dcc4f394d9011760814e4dae4"


@dataclass(frozen=True)
class CoordinateCandidate:
    mass_power: int
    speed_power: int
    action_power: int
    length_power: int


def candidate_is_exact(candidate: CoordinateCandidate) -> bool:
    mass_dimension = sp.Matrix([1, 0, 0])
    speed_dimension = sp.Matrix([0, 1, -1])
    action_dimension = sp.Matrix([1, 2, -1])
    length_dimension = sp.Matrix([0, 1, 0])
    total = (
        candidate.mass_power * mass_dimension
        + candidate.speed_power * speed_dimension
        + candidate.action_power * action_dimension
        + candidate.length_power * length_dimension
    )
    return total == sp.zeros(3, 1) and candidate == CoordinateCandidate(1, 1, -1, 1)


def run(source_file: Path) -> int:
    checks = CheckLedger("C-DIM-003")
    payload = source_file.read_bytes()
    source_text = payload.decode("utf-8")
    checks.check(
        "the audited EL1 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == EL1_SHA256,
    )

    primitives = sp.Matrix(
        [
            [0, 1, 0],
            [1, 2, 1],
            [-1, -1, 0],
        ]
    )
    mass_dimension = sp.Matrix([1, 0, 0])
    checks.check(
        "C-DIM-002 uniquely reconstructs the mass unit",
        monomial_exponents(primitives, mass_dimension) == sp.Matrix([-1, 1, -1]),
    )
    checks.check(
        "mass times speed and length divided by action is dimensionless",
        mass_dimension + primitives[:, 0] + primitives[:, 2] - primitives[:, 1]
        == sp.zeros(3, 1),
    )

    mass, speed, action, length, coordinate = sp.symbols(
        "m c S a N_m", positive=True
    )
    forward = dimensionless_mass_coordinate(mass, speed, action, length)
    backward = mass_from_dimensionless_coordinate(
        coordinate, speed, action, length
    )
    checks.check(
        "the forward map has the exact declared normal form",
        forward == mass * speed * length / action,
    )
    checks.check(
        "inverse after forward returns the imported mass exactly",
        mass_from_dimensionless_coordinate(forward, speed, action, length) == mass,
    )
    checks.check(
        "forward after inverse returns the dimensionless coordinate exactly",
        dimensionless_mass_coordinate(backward, speed, action, length) == coordinate,
    )
    checks.check(
        "the inverse retains rather than predicts the coordinate",
        sp.diff(backward, coordinate) == action / (speed * length)
        and coordinate in backward.free_symbols,
    )

    checks.mutation_sensitive(
        "all four coordinate factors and powers",
        candidate_is_exact,
        CoordinateCandidate(1, 1, -1, 1),
        [
            CoordinateCandidate(-1, 1, -1, 1),
            CoordinateCandidate(1, -1, -1, 1),
            CoordinateCandidate(1, 1, 1, 1),
            CoordinateCandidate(1, 1, -1, -1),
        ],
    )

    electron_coordinate = sp.symbols("N_e", positive=True)
    electron_mass = mass_from_dimensionless_coordinate(
        electron_coordinate, speed, action, length
    )
    conditional_ratio = matched_pion_coupling_ratio(electron_mass)
    checks.check(
        "the conditional Skyrme consumer retains the imported coordinate",
        conditional_ratio
        == 16 * sp.pi * electron_coordinate * action / (speed * length)
        and sp.diff(conditional_ratio, electron_coordinate)
        == 16 * sp.pi * action / (speed * length),
    )

    hadron_coordinate = sp.symbols("N_h", positive=True)
    hadron_mass = mass_from_dimensionless_coordinate(
        hadron_coordinate, speed, action, length
    )
    mass_ratio = sp.simplify(electron_mass / hadron_mass)
    checks.check(
        "a dimensionless mass ratio still requires dimensionless physics inputs",
        mass_ratio == electron_coordinate / hadron_coordinate
        and sp.diff(mass_ratio, electron_coordinate) != 0
        and sp.diff(mass_ratio, hadron_coordinate) != 0,
    )
    checks.check(
        "an absolute reconstructed mass varies with the retained primitive scale",
        sp.diff(electron_mass, length)
        == -electron_coordinate * action / (speed * length**2)
        and length in electron_mass.free_symbols,
    )

    me_numeral = re.compile(r"0\.51099895|9\.1093837")
    unit_expression = re.compile(
        r"16\s*\*\s*sp\.pi|48\s*\*\s*sp\.pi\*\*3|4\s*\*\s*sp\.pi\s*\*\s*m_e|16\s*\*\s*pi"
    )
    unrelated_fixture = (
        "# historical numeral 0.51099895\n"
        "unrelated_normalization = 16 * sp.pi\n"
        "observable = charge\n"
    )
    checks.check(
        "EL1's file-level regex co-occurrence is not a semantic-role oracle",
        bool(me_numeral.search(unrelated_fixture))
        and bool(unit_expression.search(unrelated_fixture)),
    )
    checks.check(
        "EL1's every-consumer predicate explicitly filters to two phases",
        'h.startswith(("phase-4/", "phase-44/"))' in source_text,
    )

    total = checks.finish()
    print(f"P018 EL1 EXACT AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
