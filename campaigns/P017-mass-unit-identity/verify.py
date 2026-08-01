#!/usr/bin/env python3
"""Exact equivalence and scope verifier for MR1 against C-SK-001."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.skyrme_relations import (
    conditional_anw_mass,
    conditional_topological_mass,
    matched_pion_coupling_ratio,
)
from substrate_framework.verification import CheckLedger


MR1_SHA256 = "d065f592390fe9322d27fbd2cf55262d8ccb8d45e6510cf8628058f716b6c875"


@dataclass(frozen=True)
class MassPair:
    """Coefficient and shared-factor powers for a conditional mass pair."""

    medium_coefficient: int
    skyrme_coefficient: int
    medium_shape_power: int
    skyrme_shape_power: int


def pair_has_accepted_ratio(candidate: MassPair) -> bool:
    """Return whether the candidate uniquely gives the C-SK-001 ratio."""

    shape, rest_energy, ratio = sp.symbols("b E_e X", positive=True)
    medium = (
        candidate.medium_coefficient
        * sp.pi**3
        * shape**candidate.medium_shape_power
        * rest_energy
    )
    skyrme = (
        candidate.skyrme_coefficient
        * sp.pi**2
        * shape**candidate.skyrme_shape_power
        * ratio
    )
    solutions = sp.solve(sp.Eq(medium, skyrme), ratio)
    return (
        len(solutions) == 1
        and sp.simplify(solutions[0] - 16 * sp.pi * rest_energy) == 0
        and shape not in solutions[0].free_symbols
    )


def run(source_file: Path) -> int:
    checks = CheckLedger("P017-MR1")
    payload = source_file.read_bytes()
    source_text = payload.decode("utf-8")
    checks.check(
        "the audited MR1 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == MR1_SHA256,
    )

    shape, rest_energy, pion_scale, coupling = sp.symbols(
        "b E_e F_pi e", positive=True
    )
    common = 12 * sp.pi**2 * shape
    medium_unit = 4 * sp.pi * rest_energy
    skyrme_unit = pion_scale / (4 * coupling)
    medium_mass = conditional_topological_mass(shape, rest_energy)
    skyrme_mass = conditional_anw_mass(shape, pion_scale, coupling)

    checks.check(
        "both accepted conditional masses factor through the same positive shape",
        sp.simplify(medium_mass - common * medium_unit) == 0
        and sp.simplify(skyrme_mass - common * skyrme_unit) == 0,
    )
    checks.check(
        "mass equality is exactly common factor times unit equality",
        sp.factor(medium_mass - skyrme_mass)
        == sp.factor(common * (medium_unit - skyrme_unit)),
    )
    checks.check(
        "positive common-factor cancellation proves both directions of unit equality",
        sp.simplify((medium_mass / common) - medium_unit) == 0
        and sp.simplify((skyrme_mass / common) - skyrme_unit) == 0
        and sp.simplify(
            (medium_mass - skyrme_mass).subs(
                pion_scale,
                16 * sp.pi * rest_energy * coupling,
            )
        )
        == 0,
    )

    matched_ratio = matched_pion_coupling_ratio(rest_energy)
    solved = sp.solve(sp.Eq(medium_mass, skyrme_mass), pion_scale)
    checks.check(
        "MR1's solved unit ratio is exactly the accepted C-SK-001 iff",
        len(solved) == 1
        and sp.simplify(solved[0] / coupling - matched_ratio) == 0
        and sp.simplify(
            medium_unit - skyrme_unit.subs(pion_scale, coupling * matched_ratio)
        )
        == 0,
    )
    checks.check(
        "the solved ratio is invariant only with respect to the shared shape premise",
        sp.diff(matched_ratio, shape) == 0
        and shape not in matched_ratio.free_symbols,
    )

    checks.mutation_sensitive(
        "the accepted coefficient and equal-power structure",
        pair_has_accepted_ratio,
        MassPair(48, 3, 1, 1),
        [
            MassPair(47, 3, 1, 1),
            MassPair(48, 4, 1, 1),
            MassPair(48, 3, 2, 1),
            MassPair(48, 3, 1, 2),
        ],
    )

    unit_one, unit_two = sp.symbols("U_1 U_2", positive=True)
    checks.check(
        "generic cancellation adds no stronger predicate than nonzero multiplication",
        sp.solve(sp.Eq(common * unit_one, common * unit_two), unit_one)
        == [unit_two],
    )
    checks.check(
        "the nonzero common-factor premise is load-bearing",
        sp.Eq((common * unit_one).subs(shape, 0), (common * unit_two).subs(shape, 0))
        is sp.S.true
        and sp.simplify(unit_one - unit_two) != 0,
    )

    allocation = sp.symbols("sector_allocation", real=True)
    matched_difference = sp.simplify(
        (medium_mass - skyrme_mass).subs(
            pion_scale,
            coupling * matched_ratio,
        )
    )
    checks.check(
        "the exact identity leaves every sector-allocation label unconstrained",
        matched_difference == 0
        and allocation not in matched_difference.free_symbols
        and sp.simplify(matched_difference.subs(allocation, 0))
        == sp.simplify(matched_difference.subs(allocation, 1)),
    )

    classical_shape = sp.Rational(12314, 10000)
    generalized_shape = sp.Rational(1436, 1000)
    checks.check(
        "MR1's two shape substitutions are instances of the exact cancellation",
        sp.simplify(
            solved[0].subs(shape, classical_shape)
            - solved[0].subs(shape, generalized_shape)
        )
        == 0
        and shape not in solved[0].free_symbols,
    )
    checks.check(
        "MR1's executable guard does not quarantine its corpus-specific shape inputs",
        "B_CL =" in source_text
        and "B_GEN =" in source_text
        and "FORBIDDEN =" in source_text
        and "B_CL" not in source_text.split("FORBIDDEN =", 1)[1].split("check(", 1)[0],
    )

    total = checks.finish()
    print(f"P017 MR1 EXACT AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
