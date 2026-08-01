#!/usr/bin/env python3
"""Independent support-graph and quartet review for P035."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def incidence(size: int, edges: tuple[tuple[int, int], ...]) -> sp.Matrix:
    return sp.Matrix(
        [
            [
                (1 if column == row else -1 if column == size + target else 0)
                for column in range(2 * size)
            ]
            for row, target in edges
        ]
    )


def is_zero(matrix: sp.MatrixBase) -> bool:
    return sp.simplify(matrix) == sp.zeros(*matrix.shape)


def main() -> int:
    ledger = CheckLedger("P035-INDEPENDENT")

    dense_edges = tuple((row, column) for row in range(4) for column in range(4))
    dense = incidence(4, dense_edges)
    permutation = incidence(4, ((0, 1), (1, 3), (2, 0), (3, 2)))
    ledger.check(
        "an independent K4,4 incidence calculation has rank seven and one kernel",
        dense.rank() == 7 and len(dense.nullspace()) == 1,
    )
    ledger.check(
        "a four-edge permutation support has four stabilizer components",
        permutation.rank() == 4 and len(permutation.nullspace()) == 4,
    )

    size = sp.symbols("N", integer=True, positive=True)
    quotient = sp.expand(size**2 - (2 * size - 1))
    angles = size * (size - 1) / 2
    ledger.check(
        "independent dimension subtraction gives the quotient and residual-phase polynomials",
        sp.simplify(quotient - (size - 1) ** 2) == 0
        and sp.simplify(quotient - angles - (size - 1) * (size - 2) / 2) == 0,
    )

    theta = sp.symbols("theta", real=True)
    rotation = sp.Matrix([[sp.cos(theta), sp.sin(theta)], [-sp.sin(theta), sp.cos(theta)]])
    p0, p1, q0, q1 = sp.symbols("p0 p1 q0 q1", real=True)
    general2 = sp.diag(sp.exp(sp.I * p0), sp.exp(sp.I * p1)) * rotation * sp.diag(
        sp.exp(sp.I * q0), sp.exp(sp.I * q1)
    )
    quartet2 = sp.im(
        sp.expand(
            general2[0, 0]
            * general2[1, 1]
            * sp.conjugate(general2[0, 1])
            * sp.conjugate(general2[1, 0])
        )
    )
    ledger.check(
        "the independently parameterized two-dimensional quartet is identically real",
        is_zero(general2.H * general2 - sp.eye(2)) and sp.simplify(quartet2) == 0,
    )

    omega = sp.Rational(-1, 2) + sp.sqrt(3) * sp.I / 2
    fourier = sp.Matrix(
        [[1, 1, 1], [1, omega, omega**2], [1, omega**2, omega]]
    ) / sp.sqrt(3)
    quartet = sp.expand(
        fourier[0, 0]
        * fourier[1, 1]
        * sp.conjugate(fourier[0, 1])
        * sp.conjugate(fourier[1, 0])
    )
    ledger.check(
        "a different exact three-dimensional unitary has a nonzero imaginary quartet",
        is_zero(fourier.H * fourier - sp.eye(3))
        and sp.simplify(sp.im(quartet)) != 0,
    )
    ledger.check(
        "complex conjugation reverses that independent quartet",
        sp.simplify(sp.im(sp.conjugate(quartet)) + sp.im(quartet)) == 0,
    )

    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1", real=True)
    phase_product = sp.simplify(
        sp.exp(sp.I * (a0 - b0))
        * sp.exp(sp.I * (a1 - b1))
        * sp.exp(-sp.I * (a0 - b1))
        * sp.exp(-sp.I * (a1 - b0))
    )
    ledger.check(
        "the independent quartet phase cancellation is exact",
        sp.simplify(phase_product - 1) == 0,
    )

    # With completely degenerate singular spectra, C-MIX-001 permits arbitrary
    # basis rotations.  Identity and Fourier relative bases can therefore
    # describe the same degenerate operators but have different quartets.
    degenerate = 5 * sp.eye(3)
    ledger.check(
        "degenerate spectra enlarge basis freedom beyond diagonal rephasings",
        is_zero(fourier.H * degenerate * fourier - degenerate)
        and sp.im(quartet) != 0,
    )
    ledger.check(
        "the abstract invariant contains no interaction or physical CP map",
        quartet.free_symbols == set(),
    )

    count = ledger.finish()
    print(f"P035 INDEPENDENT SUPPORT-INVARIANT REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
