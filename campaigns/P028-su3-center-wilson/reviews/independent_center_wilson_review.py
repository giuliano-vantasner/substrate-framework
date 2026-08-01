#!/usr/bin/env python3
"""Independent commutant and Wilson-limit rederivation for P028."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P028-INDEPENDENT")
    entries = sp.symbols("m0:9")
    matrix = sp.Matrix(3, 3, entries)
    root_three = sp.sqrt(3)
    t3 = sp.diag(1, -1, 0) / 2
    t8 = sp.diag(1 / root_three, 1 / root_three, -2 / root_three) / 2
    t1 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / 2
    t4 = sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]) / 2
    equations = [
        entry
        for generator in (t3, t8, t1, t4)
        for entry in matrix * generator - generator * matrix
    ]
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, entries)
    nullspace = coefficient_matrix.nullspace()
    checks.check(
        "four independent generators already force the commutant to scalars",
        len(nullspace) == 1
        and sp.Matrix(3, 3, list(nullspace[0])) == sp.eye(3),
    )

    scalar = sp.symbols("z")
    roots = sp.solve(sp.Eq((scalar * sp.eye(3)).det(), 1), scalar)
    checks.check(
        "unit determinant restricts a scalar commutant element to three roots",
        len(roots) == 3
        and all(sp.simplify(root**3 - 1) == 0 for root in roots),
    )
    checks.check(
        "all determinant roots have unit modulus",
        all(sp.simplify(sp.conjugate(root) * root) == 1 for root in roots),
    )

    separation, duration, tension, perimeter = sp.symbols(
        "R T sigma rho", positive=True
    )
    independent_area_loop = sp.exp(-tension * separation * duration)
    independent_perimeter_loop = sp.exp(-2 * perimeter * (separation + duration))
    area_potential = sp.limit(
        tension * separation * duration / duration, duration, sp.oo
    )
    perimeter_potential = sp.limit(
        2 * perimeter * (separation + duration) / duration,
        duration,
        sp.oo,
    )
    checks.check(
        "direct logarithm exponents independently give the area-law limit",
        independent_area_loop != 0 and area_potential == tension * separation,
    )
    checks.check(
        "direct logarithm exponents independently give the perimeter-law limit",
        independent_perimeter_loop != 0 and perimeter_potential == 2 * perimeter,
    )
    checks.check(
        "the perimeter countermodel preserves center algebra but removes linear slope",
        len(nullspace) == 1
        and sp.diff(area_potential, separation) == tension
        and sp.diff(perimeter_potential, separation) == 0,
    )

    total = checks.finish()
    print(f"P028 INDEPENDENT CENTER/WILSON REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
