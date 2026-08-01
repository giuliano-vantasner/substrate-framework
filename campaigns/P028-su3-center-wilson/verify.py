#!/usr/bin/env python3
"""Exact SU(3)-center and conditional Wilson-loop audit for CF3."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.su3 import (
    center_conjugation,
    center_element,
    center_elements,
    fundamental_commutant_basis,
    fundamental_generators,
    triality_phase,
)
from substrate_framework.verification import CheckLedger
from substrate_framework.wilson_loops import (
    rectangular_area_law,
    rectangular_perimeter_law,
    static_potential_from_loop,
)


CF3_SHA256 = "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d"


@dataclass(frozen=True)
class CenterCandidate:
    phase: sp.Expr
    order: int


def run(source_file: Path) -> int:
    checks = CheckLedger("P028")
    checks.check(
        "the audited CF3 source is the hash-pinned candidate unit",
        hashlib.sha256(source_file.read_bytes()).hexdigest() == CF3_SHA256,
    )

    generators = fundamental_generators()
    commutant = fundamental_commutant_basis()
    checks.check(
        "the exact fundamental commutant is one-dimensional and scalar",
        commutant == (sp.eye(3),),
    )

    elements = center_elements()
    checks.check(
        "the scalar unit-determinant commutant supplies exactly three elements",
        len(elements) == 3
        and len({sp.srepr(element) for element in elements}) == 3,
    )
    checks.check(
        "every listed center element is unitary with determinant one",
        all(
            sp.simplify(element.H * element) == sp.eye(3)
            and sp.simplify(element.det()) == 1
            for element in elements
        ),
    )
    checks.check(
        "every listed element commutes with every fundamental generator",
        all(
            element * generator == generator * element
            for element in elements
            for generator in generators
        ),
    )
    checks.check(
        "center multiplication closes as addition modulo three",
        all(
            sp.simplify(
                center_element(a) * center_element(b) - center_element(a + b)
            )
            == sp.zeros(3)
            for a in range(3)
            for b in range(3)
        ),
    )

    def is_nontrivial_order_three(candidate: CenterCandidate) -> bool:
        matrix = sp.simplify(candidate.phase) * sp.eye(3)
        return bool(
            candidate.order == 3
            and matrix != sp.eye(3)
            and sp.simplify(matrix.H * matrix) == sp.eye(3)
            and sp.simplify(matrix.det()) == 1
            and sp.simplify(matrix**candidate.order) == sp.eye(3)
        )

    omega = center_element(1)[0, 0]
    checks.mutation_sensitive(
        "nontrivial center phase, determinant constraint, and order",
        is_nontrivial_order_three,
        CenterCandidate(omega, 3),
        [
            CenterCandidate(-1, 3),
            CenterCandidate(sp.I, 3),
            CenterCandidate(omega, 2),
        ],
    )

    vector = sp.Matrix(sp.symbols("v0:3"))
    checks.check(
        "the fundamental sector acquires the nontrivial center phase",
        center_element() * vector == omega * vector
        and triality_phase(1) == omega,
    )
    generic_matrix = sp.Matrix(3, 3, sp.symbols("x0:9"))
    checks.check(
        "center conjugation is exactly trivial on matrix-valued adjoint action",
        center_conjugation(generic_matrix) == generic_matrix
        and triality_phase(0) == 1,
    )
    checks.check(
        "tensor-product trialities compose modulo three",
        all(
            sp.simplify(triality_phase(a) * triality_phase(b))
            == triality_phase(a + b)
            for a in range(3)
            for b in range(3)
        ),
    )

    separation, duration, tension, perimeter = sp.symbols(
        "R T sigma rho", positive=True
    )
    area_loop = rectangular_area_law(separation, duration, tension)
    area_potential = static_potential_from_loop(area_loop, duration)
    checks.check(
        "the declared area law conditionally extracts a linear potential",
        area_loop == sp.exp(-tension * separation * duration)
        and area_potential == tension * separation
        and sp.diff(area_potential, separation) == tension
        and sp.diff(area_potential, separation, 2) == 0,
    )

    def extracts_positive_linear_slope(candidate: sp.Expr) -> bool:
        potential = static_potential_from_loop(candidate, duration)
        return bool(
            sp.simplify(potential - tension * separation) == 0
            and sp.diff(potential, separation) == tension
        )

    checks.mutation_sensitive(
        "area-law exponent sign and area product",
        extracts_positive_linear_slope,
        area_loop,
        [
            sp.exp(tension * separation * duration),
            sp.exp(-tension * (separation + duration)),
            sp.exp(-tension * duration),
        ],
    )

    perimeter_loop = rectangular_perimeter_law(
        separation, duration, perimeter
    )
    perimeter_potential = static_potential_from_loop(perimeter_loop, duration)
    checks.check(
        "the declared perimeter law conditionally extracts a bounded potential",
        perimeter_loop == sp.exp(-2 * perimeter * (separation + duration))
        and perimeter_potential == 2 * perimeter
        and sp.diff(perimeter_potential, separation) == 0,
    )
    checks.check(
        "the same accepted center algebra is compatible with both loop ansatzes",
        commutant == (sp.eye(3),)
        and area_potential != perimeter_potential
        and sp.diff(area_potential, separation) != sp.diff(
            perimeter_potential, separation
        ),
    )
    checks.check(
        "neither loop ansatz enters the derivation of the center",
        not any(
            symbol in set().union(*(entry.free_symbols for entry in element))
            for symbol in (separation, duration, tension, perimeter)
            for element in elements
        ),
    )

    total = checks.finish()
    print(f"P028 CF3 CENTER/WILSON AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
