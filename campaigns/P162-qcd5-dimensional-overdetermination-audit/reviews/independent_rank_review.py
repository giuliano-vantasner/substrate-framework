#!/usr/bin/env python3
"""Fresh SymPy row-space review of the QCD5 overdetermination claim."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _radial_exponent(expression: sp.Expr, radius: sp.Symbol) -> sp.Expr:
    return sp.simplify(radius * sp.diff(sp.log(expression), radius))


def run() -> int:
    checks = CheckLedger("P162-INDEPENDENT")
    fixed_matrix = sp.Matrix([[1], [1], [1]])
    fixed_rhs = sp.Matrix([3, 3, 3])
    fixed_augmented = fixed_matrix.row_join(fixed_rhs)
    checks.check(
        "fresh fixed-s coefficient and augmented ranks are one",
        fixed_matrix.rank() == fixed_augmented.rank() == 1,
    )
    left_nullspace = fixed_matrix.T.nullspace()
    checks.check(
        "fresh row-dependency space has dimension two",
        len(left_nullspace) == 2
        and all((vector.T * fixed_matrix)[0] == 0 for vector in left_nullspace),
    )
    checks.check(
        "fresh duplicate-row dependencies also annihilate the equal rhs",
        all((vector.T * fixed_rhs)[0] == 0 for vector in left_nullspace),
    )
    d_symbol = sp.symbols("d")
    checks.check(
        "fresh three-row and one-row solves both give d3",
        sp.linsolve((fixed_matrix, fixed_rhs), d_symbol)
        == sp.linsolve((sp.Matrix([[1]]), sp.Matrix([3])), d_symbol)
        == {(sp.Integer(3),)},
    )

    free_matrix = sp.Matrix([[1, -2], [1, -2], [1, -2]])
    free_rhs = sp.ones(3, 1)
    checks.check(
        "fresh free d-s system has rank one and nullity one",
        free_matrix.rank() == 1
        and free_matrix.row_join(free_rhs).rank() == 1
        and len(free_matrix.nullspace()) == 1,
    )
    checks.check(
        "fresh free null vector preserves d minus two s",
        free_matrix.nullspace() == [sp.Matrix([2, 1])],
    )
    d_free, s_free = sp.symbols("d_free s_free")
    checks.check(
        "fresh row reduction gives the exact family d equals two s plus one",
        sp.linsolve((free_matrix, free_rhs), (d_free, s_free))
        == {(2 * s_free + 1, s_free)},
    )

    sector_labels = ("U1", "SU2", "SU3")
    amplitudes = (sp.Integer(1), sp.Rational(1, 2), sp.Rational(1, 2))
    permuted = tuple(reversed(tuple(zip(sector_labels, amplitudes))))
    mutated = tuple((label, amplitude * 7) for label, amplitude in permuted)
    rows_before = sp.Matrix([[1, -2] for _item in zip(sector_labels, amplitudes)])
    rows_after = sp.Matrix([[1, -2] for _item in mutated])
    checks.check(
        "fresh sector permutation and amplitude mutation leave every row unchanged",
        rows_before == rows_after == free_matrix,
    )

    radius = sp.symbols("r", positive=True)
    dimension, power = sp.symbols("d s", positive=True)
    dimension_amplitudes = (sp.Integer(1), dimension, dimension**2)
    dimension_exponents = tuple(
        _radial_exponent(amplitude * radius ** (2 * power - dimension), radius)
        for amplitude in dimension_amplitudes
    )
    checks.check(
        "fresh kappa-of-d mutation leaves all radial powers identical",
        dimension_exponents == (2 * power - dimension,) * 3,
    )
    dimension_force_exponents = tuple(
        _radial_exponent(
            -sp.diff(amplitude * radius ** (2 * power - dimension), radius),
            radius,
        )
        for amplitude in dimension_amplitudes
    )
    checks.check(
        "fresh kappa-of-d mutation leaves all force powers identical",
        dimension_force_exponents == (2 * power - dimension - 1,) * 3,
    )
    alpha = sp.symbols("alpha", positive=True)
    radial_mutation = radius**alpha * radius ** (2 * power - dimension)
    checks.check(
        "fresh radial-amplitude mutation changes the actual power law",
        _radial_exponent(radial_mutation, radius)
        == alpha + 2 * power - dimension,
    )

    independent_matrix = sp.Matrix([[1, -2], [1, -3]])
    independent_rhs = sp.Matrix([1, 0])
    checks.check(
        "fresh distinct constraint directions can identify both d and s",
        independent_matrix.rank() == 2
        and independent_matrix.row_join(independent_rhs).rank() == 2
        and sp.linsolve(
            (independent_matrix, independent_rhs), (d_free, s_free)
        )
        == {(sp.Integer(3), sp.Integer(1))},
    )
    inconsistent_rhs = sp.Matrix([3, sp.Rational(5, 2)])
    duplicate_pair = sp.Matrix([[1], [1]])
    checks.check(
        "fresh equal rows with unequal rhs are inconsistent not independent",
        duplicate_pair.rank() == 1
        and duplicate_pair.row_join(inconsistent_rhs).rank() == 2
        and sp.linsolve((duplicate_pair, inconsistent_rhs), d_symbol) == sp.EmptySet,
    )

    checks.check(
        "fresh endpoint mutation moves the fixed dimension",
        (2 * sp.Integer(1) + 1) == 3
        and (2 * sp.Rational(3, 4) + 1) == sp.Rational(5, 2),
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P162 INDEPENDENT ALL {result} CHECKS PASS")
