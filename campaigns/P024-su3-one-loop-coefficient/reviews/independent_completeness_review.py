#!/usr/bin/env python3
"""Independent SU(3) completeness review for P024."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def generators() -> tuple[sp.Matrix, ...]:
    i = sp.I
    matrices = (
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, -i, 0], [i, 0, 0], [0, 0, 0]]),
        sp.diag(1, -1, 0),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, -i], [0, 0, 0], [i, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -i], [0, i, 0]]),
        sp.diag(1, 1, -2) / sp.sqrt(3),
    )
    return tuple(matrix / 2 for matrix in matrices)


def run() -> int:
    checks = CheckLedger("P024-INDEPENDENT")
    basis = generators()
    completeness = True
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for ell in range(3):
                    left = sum(generator[i, j] * generator[k, ell] for generator in basis)
                    right = sp.Rational(1, 2) * (
                        int(i == ell) * int(j == k)
                        - sp.Rational(1, 3) * int(i == j) * int(k == ell)
                    )
                    completeness = completeness and sp.simplify(left - right) == 0
    checks.check("fundamental completeness holds componentwise", completeness)
    casimir = sum((generator * generator for generator in basis), sp.zeros(3))
    checks.check("completeness gives the fundamental Casimir", casimir == 4 * sp.eye(3) / 3)
    trace_sum = sum(sp.trace(generator * generator) for generator in basis)
    checks.check("the total trace independently fixes the Dynkin index", trace_sum == 4)
    flavors = sp.symbols("n_f", integer=True, nonnegative=True)
    coefficient = 11 - 2 * flavors / 3
    checks.check(
        "declared loop weights give the exact integer sign boundary",
        coefficient.subs(flavors, 16) > 0 and coefficient.subs(flavors, 17) < 0,
    )
    checks.check(
        "changing the matter weight changes the sign boundary",
        sp.solve(sp.Eq(11 - flavors / 2, 0), flavors)[0] == 22,
    )
    total = checks.finish()
    print(f"P024 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
