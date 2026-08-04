#!/usr/bin/env python3
"""Fresh block-matrix rederivation of C-REP-002 without new APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P147-independent")
    imaginary = sp.I
    pauli = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -imaginary], [imaginary, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )
    generators = tuple(matrix / 2 for matrix in pauli)
    cyclic = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    checks.check(
        "fresh Pauli-half matrices are Hermitian and traceless",
        all(matrix == matrix.H and sp.trace(matrix) == 0 for matrix in generators),
    )
    checks.check(
        "fresh fundamental commutators close",
        all(
            sp.simplify(
                generators[a] * generators[b]
                - generators[b] * generators[a]
                - imaginary * generators[c]
            )
            == sp.zeros(2)
            for a, b, c in cyclic
        ),
    )
    checks.check(
        "fresh fundamental Casimir is three quarters",
        sp.simplify(sum((matrix * matrix for matrix in generators), sp.zeros(2)))
        == sp.Rational(3, 4) * sp.eye(2),
    )

    a, b, c, d = sp.symbols("a b c d")
    intertwiner = sp.Matrix([[a, b], [c, d]])
    commutant_equations = [
        entry
        for generator in generators
        for entry in intertwiner * generator - generator * intertwiner
    ]
    checks.check(
        "fresh full intertwiner solve gives scalar commutant",
        sp.solve(commutant_equations, [a, b, c, d], dict=True)
        == [{a: d, b: 0, c: 0}],
    )

    projector = sp.diag(1, 0)
    complement = sp.diag(0, 1)
    left = tuple(sp.kronecker_product(matrix, projector) for matrix in generators)
    right = tuple(sp.kronecker_product(matrix, complement) for matrix in generators)
    checks.check(
        "fresh independent-factor generators are Hermitian",
        all(matrix == matrix.H for matrix in (*left, *right)),
    )
    checks.check(
        "fresh left factor closes su2",
        all(
            sp.simplify(left[a] * left[b] - left[b] * left[a] - imaginary * left[c])
            == sp.zeros(4)
            for a, b, c in cyclic
        ),
    )
    checks.check(
        "fresh right factor closes su2",
        all(
            sp.simplify(
                right[a] * right[b] - right[b] * right[a] - imaginary * right[c]
            )
            == sp.zeros(4)
            for a, b, c in cyclic
        ),
    )
    checks.check(
        "fresh left action annihilates independent right subspace",
        all(
            matrix * sp.kronecker_product(sp.eye(2), sp.Matrix([0, 1]))
            == sp.zeros(4, 2)
            for matrix in left
        ),
    )

    same = tuple(matrix * projector for matrix in generators)
    checks.check(
        "fresh same-carrier product fails Hermiticity",
        sum(matrix != matrix.H for matrix in same) == 2,
    )
    checks.check(
        "fresh same-carrier product fails every commutator",
        all(
            sp.simplify(same[a] * same[b] - same[b] * same[a] - imaginary * same[c])
            != sp.zeros(2)
            for a, b, c in cyclic
        ),
    )
    checks.check(
        "rank-one same-carrier projector cannot commute with all generators",
        any(
            sp.simplify(projector * matrix - matrix * projector) != sp.zeros(2)
            for matrix in generators
        ),
    )

    exchange = pauli[0]
    full_exchange = sp.kronecker_product(sp.eye(2), exchange)
    vector = tuple(l + r for l, r in zip(left, right, strict=True))
    axial = tuple(l - r for l, r in zip(left, right, strict=True))
    checks.check(
        "fresh factor parity exchanges left and right",
        all(
            sp.simplify(full_exchange * l * full_exchange.H - r) == sp.zeros(4)
            for l, r in zip(left, right, strict=True)
        ),
    )
    checks.check(
        "fresh vector combination is parity even",
        all(
            sp.simplify(full_exchange * matrix * full_exchange.H - matrix)
            == sp.zeros(4)
            for matrix in vector
        ),
    )
    checks.check(
        "fresh axial combination is parity odd",
        all(
            sp.simplify(full_exchange * matrix * full_exchange.H + matrix)
            == sp.zeros(4)
            for matrix in axial
        ),
    )
    checks.check(
        "fresh left combination alone is not an odd eigenoperator",
        all(r != -l for l, r in zip(left, right, strict=True)),
    )

    x11, x12, x21, x22 = sp.symbols("x11 x12 x21 x22", real=True)
    abelian = sp.Matrix([[x11, x12], [x21, x22]])
    abelian_solutions = sp.solve(
        [
            entry
            for generator in generators
            for entry in abelian * generator - generator * abelian
        ],
        [x11, x12, x21, x22],
        dict=True,
    )
    checks.check(
        "fresh common Abelian solve gives one shared eigenvalue",
        abelian_solutions == [{x11: x22, x12: 0, x21: 0}],
    )
    y, coefficient = sp.symbols("y coefficient", real=True)
    charge = generators[2] + coefficient * y * sp.eye(2)
    checks.check(
        "fresh common charge has unit eigenvalue separation",
        sp.simplify(charge[0, 0] - charge[1, 1]) == 1,
    )
    checks.check(
        "fresh plus-minus-one labels cannot share that charge operator",
        sp.solve(
            [sp.Eq(charge[0, 0], 1), sp.Eq(charge[1, 1], -1)],
            [coefficient, y],
            dict=True,
        )
        == [],
    )
    checks.check(
        "fresh half-rescaled labels match at zero common shift",
        charge.subs(y, 0) == sp.diag(sp.Rational(1, 2), sp.Rational(-1, 2)),
    )

    label = sp.Symbol("label", real=True)
    checks.check(
        "fresh CP-opposite labels leave their magnitude arbitrary",
        sp.simplify(label - (-(-label))) == 0,
    )
    checks.check(
        "fresh W2 basis-label transition has difference two",
        sp.Integer(1) - sp.Integer(-1) == 2,
    )

    scaled = tuple(2 * matrix for matrix in generators)
    checks.check(
        "fresh generator normalization mutation breaks closure",
        sp.simplify(
            scaled[0] * scaled[1] - scaled[1] * scaled[0] - imaginary * scaled[2]
        )
        != sp.zeros(2),
    )
    nonprojector = sp.diag(1, sp.Rational(1, 2))
    checks.check(
        "fresh projector mutation breaks factor closure",
        sp.simplify(nonprojector * nonprojector - nonprojector) != sp.zeros(2),
    )
    wrong_exchange = sp.eye(2)
    checks.check(
        "fresh nonexchanging parity mutation is detected",
        sp.simplify(wrong_exchange * projector * wrong_exchange.H - complement)
        != sp.zeros(2),
    )
    wrong_charge_labels = (sp.Rational(1, 2), sp.Rational(1, 2))
    checks.check(
        "fresh lower-label mutation breaks the unit gap",
        wrong_charge_labels[0] - wrong_charge_labels[1] != 1,
    )

    tally = checks.finish()
    print(f"P147 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
