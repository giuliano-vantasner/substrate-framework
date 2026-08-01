#!/usr/bin/env python3
"""Independent constraint-space and rotation review for P038."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def frobenius(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.simplify(
        sum(left[i, j] * right[i, j] for i in range(3) for j in range(3))
    )


def main() -> int:
    ledger = CheckLedger("P038-INDEPENDENT")
    hxx, hyy, hzz, hxy, hxz, hyz = sp.symbols(
        "h_xx h_yy h_zz h_xy h_xz h_yz", real=True
    )
    coordinates = sp.Matrix([hxx, hyy, hzz, hxy, hxz, hyz])
    tensor = sp.Matrix(
        [[hxx, hxy, hxz], [hxy, hyy, hyz], [hxz, hyz, hzz]]
    )
    direction = sp.Matrix([0, 0, 1])
    constraints = list(tensor * direction) + [sp.trace(tensor)]
    constraint_matrix, _ = sp.linear_eq_to_matrix(constraints, list(coordinates))
    nullspace = constraint_matrix.nullspace()
    ledger.check(
        "independent symmetric TT constraints have rank four and nullity two",
        constraint_matrix.rank() == 4 and len(nullspace) == 2,
    )
    ledger.check(
        "the complete constraint solution has only plus and cross coordinates",
        sp.linsolve(constraints, list(coordinates))
        == {( -hyy, hyy, 0, hxy, 0, 0)},
    )

    plus = sp.diag(1, -1, 0) / sp.sqrt(2)
    cross = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / sp.sqrt(2)
    ledger.check(
        "independent basis normalization gives unit norms and zero overlap",
        frobenius(plus, plus) == 1
        and frobenius(cross, cross) == 1
        and frobenius(plus, cross) == 0,
    )
    general_tt = sp.simplify(
        frobenius(tensor, plus) * plus + frobenius(tensor, cross) * cross
    )
    ledger.check(
        "basis reconstruction independently matches the solved constraint form",
        general_tt
        == sp.Matrix(
            [
                [(hxx - hyy) / 2, hxy, 0],
                [hxy, (-hxx + hyy) / 2, 0],
                [0, 0, 0],
            ]
        ),
    )

    angle = sp.symbols("psi", real=True)
    first = sp.Matrix([sp.cos(angle), sp.sin(angle), 0])
    second = sp.Matrix([-sp.sin(angle), sp.cos(angle), 0])
    direct_plus = sp.trigsimp((first * first.T - second * second.T) / sp.sqrt(2))
    direct_cross = sp.trigsimp((first * second.T + second * first.T) / sp.sqrt(2))
    ledger.check(
        "directly rotated vectors independently produce the double-angle basis",
        sp.simplify(
            direct_plus - sp.cos(2 * angle) * plus - sp.sin(2 * angle) * cross
        )
        == sp.zeros(3)
        and sp.simplify(
            direct_cross + sp.sin(2 * angle) * plus - sp.cos(2 * angle) * cross
        )
        == sp.zeros(3),
    )
    ledger.check(
        "a one-angle tensor rotation is an explicit counterexample",
        sp.simplify(
            direct_plus
            - sp.cos(angle) * plus
            - sp.sin(angle) * cross
        )
        != sp.zeros(3),
    )

    unnormalized_plus = sp.sqrt(2) * plus
    unnormalized_cross = sp.sqrt(2) * cross
    half_weighted = sp.simplify(
        frobenius(tensor, unnormalized_plus) * unnormalized_plus / 2
        + frobenius(tensor, unnormalized_cross) * unnormalized_cross / 2
    )
    unweighted = sp.simplify(
        frobenius(tensor, unnormalized_plus) * unnormalized_plus
        + frobenius(tensor, unnormalized_cross) * unnormalized_cross
    )
    ledger.check(
        "GW3's displayed basis requires half-weighted coefficient extraction",
        frobenius(unnormalized_plus, unnormalized_plus) == 2
        and frobenius(unnormalized_cross, unnormalized_cross) == 2
        and sp.simplify(half_weighted - general_tt) == sp.zeros(3)
        and sp.simplify(unweighted - 2 * general_tt) == sp.zeros(3)
        and sp.simplify(unweighted - general_tt) != sp.zeros(3),
    )
    time = sp.symbols("t", real=True)
    ledger.check(
        "a nonzero static TT tensor is a counterexample to image membership implying propagation",
        plus != sp.zeros(3)
        and plus * direction == sp.zeros(3, 1)
        and sp.trace(plus) == 0
        and sp.diff(plus, time) == sp.zeros(3),
    )
    count = ledger.finish()
    print(f"P038 INDEPENDENT CONSTRAINT-BASIS REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
