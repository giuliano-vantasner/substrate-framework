#!/usr/bin/env python3
"""Fresh exact derivation of CF3 center and conditional loop consequences."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class ScalarCenter:
    phase: sp.Expr
    matrix_size: int
    proposed_order: int


@dataclass(frozen=True)
class LoopExponent:
    sign: int
    separation_power: int
    duration_power: int


def main() -> int:
    checks = CheckLedger("P169-INDEPENDENT-CENTER-LOOP")
    entries = sp.symbols("m0:9")
    candidate = sp.Matrix(3, 3, entries)
    root_three = sp.sqrt(3)
    generators = (
        sp.diag(1, -1, 0) / 2,
        sp.diag(1 / root_three, 1 / root_three, -2 / root_three) / 2,
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / 2,
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]) / 2,
    )
    equations = [
        entry
        for generator in generators
        for entry in candidate * generator - generator * candidate
    ]
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, entries)
    nullspace = coefficient_matrix.nullspace()
    checks.check(
        "an independent generating subset forces the complex commutant to scalars",
        len(nullspace) == 1
        and sp.Matrix(3, 3, list(nullspace[0])) == sp.eye(3),
    )
    checks.check(
        "the independent commutant calculation has rank eight and nullity one",
        coefficient_matrix.rank() == 8
        and len(entries) - coefficient_matrix.rank() == 1,
    )

    scalar = sp.symbols("z")
    determinant = (scalar * sp.eye(3)).det()
    roots = sp.solve(sp.Eq(determinant, 1), scalar)
    checks.check(
        "determinant one restricts the scalar commutant to exactly three roots",
        determinant == scalar**3
        and len(roots) == 3
        and all(sp.simplify(root**3 - 1) == 0 for root in roots),
    )
    checks.check(
        "every determinant root is unitary and no listed root is duplicated",
        all(sp.simplify(sp.conjugate(root) * root) == 1 for root in roots)
        and len({sp.srepr(root) for root in roots}) == 3,
    )
    omega = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2
    center = tuple(sp.simplify(omega**power) * sp.eye(3) for power in range(3))
    checks.check(
        "independent center multiplication is cyclic addition modulo three",
        all(
            sp.simplify(center[a] * center[b] - center[(a + b) % 3])
            == sp.zeros(3)
            for a in range(3)
            for b in range(3)
        ),
    )

    def is_correct_center(candidate_model: object) -> bool:
        assert isinstance(candidate_model, ScalarCenter)
        matrix = candidate_model.phase * sp.eye(candidate_model.matrix_size)
        return bool(
            candidate_model.matrix_size == 3
            and candidate_model.proposed_order == 3
            and matrix != sp.eye(3)
            and sp.simplify(matrix.det()) == 1
            and sp.simplify(matrix.H * matrix) == sp.eye(3)
            and sp.simplify(matrix**candidate_model.proposed_order) == sp.eye(3)
        )

    checks.mutation_sensitive(
        "independent dimension determinant and order guard",
        is_correct_center,
        ScalarCenter(omega, 3, 3),
        [
            ScalarCenter(-1, 3, 3),
            ScalarCenter(sp.I, 3, 3),
            ScalarCenter(omega, 2, 3),
            ScalarCenter(omega, 3, 2),
        ],
    )

    vector = sp.Matrix(sp.symbols("v0:3"))
    matrix = sp.Matrix(3, 3, sp.symbols("x0:9"))
    z = omega * sp.eye(3)
    checks.check(
        "independent fundamental action acquires omega",
        z * vector == omega * vector and omega != 1,
    )
    checks.check(
        "independent center conjugation cancels on every matrix",
        sp.simplify(z * matrix * z.inv() - matrix) == sp.zeros(3),
    )
    checks.check(
        "independent abstract characters compose modulo three",
        all(
            sp.simplify(omega ** (a % 3) * omega ** (b % 3) - omega ** ((a + b) % 3))
            == 0
            for a in range(3)
            for b in range(3)
        ),
    )

    separation, duration, tension, perimeter = sp.symbols(
        "R T sigma rho", positive=True
    )
    area_loop = sp.exp(-tension * separation * duration)
    perimeter_loop = sp.exp(-2 * perimeter * (separation + duration))
    area_potential = sp.simplify(
        -sp.limit(sp.log(area_loop) / duration, duration, sp.oo)
    )
    perimeter_potential = sp.simplify(
        -sp.limit(sp.log(perimeter_loop) / duration, duration, sp.oo)
    )
    checks.check(
        "direct logarithmic area limit gives the conditional linear potential",
        area_potential == tension * separation
        and sp.diff(area_potential, separation) == tension
        and sp.diff(area_potential, separation, 2) == 0,
    )
    checks.check(
        "direct logarithmic perimeter limit gives the conditional constant potential",
        perimeter_potential == 2 * perimeter
        and sp.diff(perimeter_potential, separation) == 0,
    )
    checks.check(
        "area and perimeter premises have distinct separation slopes",
        sp.diff(area_potential, separation)
        != sp.diff(perimeter_potential, separation),
    )

    def extracts_positive_linear(candidate_exponent: object) -> bool:
        assert isinstance(candidate_exponent, LoopExponent)
        loop = sp.exp(
            candidate_exponent.sign
            * tension
            * separation**candidate_exponent.separation_power
            * duration**candidate_exponent.duration_power
        )
        potential = sp.simplify(
            -sp.limit(sp.log(loop) / duration, duration, sp.oo)
        )
        return sp.simplify(potential - tension * separation) == 0

    checks.mutation_sensitive(
        "independent area exponent sign and powers",
        extracts_positive_linear,
        LoopExponent(-1, 1, 1),
        [
            LoopExponent(1, 1, 1),
            LoopExponent(-1, 0, 1),
            LoopExponent(-1, 1, 0),
        ],
    )
    checks.check(
        "center derivation is independent of every loop parameter",
        not set().union(*(entry.free_symbols for element in center for entry in element)).intersection(
            {separation, duration, tension, perimeter}
        ),
    )
    checks.check(
        "both loop results remain conditional on free positive coefficients",
        tension in area_potential.free_symbols
        and perimeter in perimeter_potential.free_symbols,
    )
    checks.check(
        "the same completed center coexists with both loop countermodels",
        len(center) == 3
        and area_potential == tension * separation
        and perimeter_potential == 2 * perimeter,
    )

    total = checks.finish()
    print(f"P169 INDEPENDENT CENTER/LOOP REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
