#!/usr/bin/env python3
"""Independent row-reduction review for P022."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P022-INDEPENDENT")
    slope = sp.symbols("k", nonzero=True)
    duplicate = sp.Matrix([[-1, slope], [-1, slope]])
    checks.check(
        "row reduction exposes one pivot for duplicate coefficients",
        duplicate.rref()[1] == (0,),
    )
    agreeing = duplicate.row_join(sp.Matrix([3, 3]))
    disagreeing = duplicate.row_join(sp.Matrix([3, 4]))
    checks.check(
        "equal duplicate offsets preserve one augmented pivot",
        agreeing.rref()[1] == (0,),
    )
    checks.check(
        "unequal duplicate offsets create a second augmented pivot",
        disagreeing.rref()[1] == (0, 2),
    )

    restored = sp.Matrix(
        [
            [2, 0, 0],
            [-4, 0, 0],
            [-1, slope, 0],
            [-2, 2 * slope, 0],
            [-1, slope, 1],
        ]
    )
    checks.check(
        "the restored-electron matrix independently has three pivots",
        len(restored.rref()[1]) == 3,
    )
    odv1 = sp.Matrix(
        [
            [1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
        ]
    )
    checks.check(
        "the separate OD-v1 matrix has four pivots and one free column",
        len(odv1.rref()[1]) == 4 and odv1.cols - len(odv1.rref()[1]) == 1,
    )

    shape, offset, target = sp.symbols("b kappa R", positive=True)
    checks.check(
        "the claimed ratio can be matched by selecting the free offset",
        sp.solve(sp.Eq(48 * sp.pi**3 * shape / offset, target), offset)[0]
        == 48 * sp.pi**3 * shape / target,
    )

    total = checks.finish()
    print(f"P022 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
