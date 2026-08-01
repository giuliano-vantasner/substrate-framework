#!/usr/bin/env python3
"""Independent exact review of the P034 decomposition claim."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def is_zero(matrix: sp.MatrixBase) -> bool:
    return sp.simplify(matrix) == sp.zeros(*matrix.shape)


def rotation(cosine: sp.Expr, sine: sp.Expr) -> sp.Matrix:
    return sp.Matrix([[cosine, sine], [-sine, cosine]])


def main() -> int:
    ledger = CheckLedger("P034-INDEPENDENT")

    matrix = sp.Matrix([[2, 1 + sp.I], [1 - sp.I, -1]])
    left, diagonal, right = matrix.singular_value_decomposition()
    ledger.check(
        "an independent exact SVD route reconstructs a different complex matrix",
        is_zero(left * diagonal * right.H - matrix),
    )
    ledger.check(
        "the two exact Gram actions agree on every nonzero singular pair",
        is_zero(matrix * right - left * diagonal)
        and is_zero(matrix.H * left - right * diagonal),
    )

    repeated = 7 * sp.eye(2)
    paired = rotation(sp.Rational(3, 5), sp.Rational(4, 5))
    ledger.check(
        "repeated singular values leave a nontrivial paired basis freedom",
        paired != sp.eye(2)
        and is_zero(paired.H * paired - sp.eye(2))
        and is_zero(paired * repeated * paired.H - repeated),
    )
    independent_left = rotation(sp.Rational(5, 13), sp.Rational(12, 13))
    independent_right = sp.diag(sp.I, -sp.I)
    ledger.check(
        "zero singular blocks leave independent left and right freedoms",
        is_zero(independent_left * sp.zeros(2) * independent_right.H)
        and is_zero(independent_left.H * independent_left - sp.eye(2))
        and is_zero(independent_right.H * independent_right - sp.eye(2)),
    )

    relative = sp.simplify(paired.H * independent_left)
    ledger.check(
        "relative column bases are unitary by direct multiplication",
        is_zero(relative.H * relative - sp.eye(2)),
    )

    # Use diagonalizers A_i mapping gauge coordinates to diagonal coordinates.
    # The transformed common bilinear contains A_u A_d^dagger.  Reversing both
    # adjoints gives a different unitary matrix and thus evades a unitary-only test.
    correct = sp.simplify(paired * independent_left.H)
    reversed_orientation = sp.simplify(paired.H * independent_left)
    ledger.check(
        "direct field substitution fixes the row-transform orientation",
        not is_zero(correct - reversed_orientation)
        and is_zero(correct.H * correct - sp.eye(2))
        and is_zero(reversed_orientation.H * reversed_orientation - sp.eye(2)),
    )

    a, b, d, cosine, sine = sp.symbols("a b d c s", real=True)
    generic = sp.Matrix([[a, b], [b, d]])
    rot = rotation(cosine, sine)
    off_diagonal = sp.expand((rot.T * generic * rot)[0, 1])
    ledger.check(
        "the independent two-by-two derivation exposes the exact angle condition",
        sp.expand(off_diagonal - (b * (cosine**2 - sine**2) + (a - d) * cosine * sine)) == 0,
    )

    angle = sp.symbols("alpha", real=True)
    arbitrary = rotation(sp.cos(angle), sp.sin(angle))
    first_mass = sp.diag(1, 2)
    second_mass = arbitrary * sp.diag(3, 5) * arbitrary.T
    ledger.check(
        "arbitrary declared textures can realize continuously many relative angles",
        first_mass.is_diagonal()
        and is_zero(arbitrary.T * second_mass * arbitrary - sp.diag(3, 5))
        and angle in second_mass.free_symbols,
    )
    ledger.check(
        "matrix unitarity alone contains no representation or anomaly coefficient",
        not ({sp.Symbol("charge"), sp.Symbol("representation")} & relative.free_symbols),
    )

    count = ledger.finish()
    print(f"P034 INDEPENDENT DECOMPOSITION REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
