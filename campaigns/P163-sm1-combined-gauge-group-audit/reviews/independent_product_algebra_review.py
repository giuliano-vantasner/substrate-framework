#!/usr/bin/env python3
"""Fresh exact review of the SM1 local algebra and global-group boundary."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(matrix: sp.MatrixBase) -> bool:
    return sp.Matrix(matrix).applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def _commutator(first: sp.MatrixBase, second: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix(first * second - second * first).applyfunc(sp.simplify)


def _fresh_generators() -> tuple[tuple[sp.Matrix, ...], tuple[sp.Matrix, ...]]:
    imaginary = sp.I
    root_three = sp.sqrt(3)
    gell_mann = (
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, -imaginary, 0], [imaginary, 0, 0], [0, 0, 0]]),
        sp.diag(1, -1, 0),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, -imaginary], [0, 0, 0], [imaginary, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -imaginary], [0, imaginary, 0]]),
        sp.diag(1 / root_three, 1 / root_three, -2 / root_three),
    )
    pauli = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -imaginary], [imaginary, 0]]),
        sp.diag(1, -1),
    )
    return tuple(matrix / 2 for matrix in gell_mann), tuple(
        matrix / 2 for matrix in pauli
    )


def run() -> int:
    checks = CheckLedger("P163-INDEPENDENT")
    color, isospin = _fresh_generators()
    color_embedded = tuple(
        sp.kronecker_product(generator, sp.eye(2)) for generator in color
    )
    isospin_embedded = tuple(
        sp.kronecker_product(sp.eye(3), generator) for generator in isospin
    )
    abelian = sp.eye(6)

    color_residuals = []
    for first in range(8):
        for second in range(8):
            constants = tuple(
                sp.simplify(
                    -2
                    * sp.I
                    * sp.trace(_commutator(color[first], color[second]) * color[target])
                )
                for target in range(8)
            )
            reconstructed = sp.I * sum(
                (
                    constants[target] * color_embedded[target]
                    for target in range(8)
                ),
                sp.zeros(6),
            )
            color_residuals.append(
                _commutator(color_embedded[first], color_embedded[second])
                - reconstructed
            )
    checks.check(
        "fresh all-pair SU3 embedding closes",
        len(color_residuals) == 64 and all(_zero(value) for value in color_residuals),
    )
    isospin_residuals = tuple(
        _commutator(isospin_embedded[first], isospin_embedded[second])
        - sp.I
        * sum(
            (
                sp.LeviCivita(first, second, target) * isospin_embedded[target]
                for target in range(3)
            ),
            sp.zeros(6),
        )
        for first in range(3)
        for second in range(3)
    )
    checks.check(
        "fresh all-pair SU2 embedding closes",
        len(isospin_residuals) == 9
        and all(_zero(value) for value in isospin_residuals),
    )
    cross = tuple(
        _commutator(first, second)
        for first in color_embedded
        for second in isospin_embedded
    ) + tuple(
        _commutator(generator, abelian)
        for generator in color_embedded + isospin_embedded
    )
    checks.check(
        "fresh thirty-five cross brackets vanish",
        len(cross) == 35 and all(_zero(value) for value in cross),
    )

    columns = tuple(
        sp.Matrix(generator).reshape(36, 1)
        for generator in color_embedded + isospin_embedded + (abelian,)
    )
    full_matrix = sp.Matrix.hstack(*columns)
    zero_weight_matrix = sp.Matrix.hstack(*columns[:-1], sp.zeros(36, 1))
    checks.check(
        "fresh nonzero versus zero Abelian weight changes rank twelve to eleven",
        full_matrix.rank() == 12 and zero_weight_matrix.rank() == 11,
    )

    entries = sp.symbols("m0:36")
    candidate = sp.Matrix(6, 6, entries)
    equations = tuple(
        entry
        for generator in color_embedded + isospin_embedded
        for entry in candidate * generator - generator * candidate
    )
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, entries)
    commutant = coefficient_matrix.nullspace()
    checks.check(
        "fresh joint commutant has dimension one",
        len(commutant) == 1 and coefficient_matrix.rank() == 35,
    )
    normalized = sp.Matrix(commutant[0] / next(value for value in commutant[0] if value != 0)).reshape(6, 6)
    checks.check("fresh joint commutant basis is identity", normalized == sp.eye(6))

    mixed = sp.kronecker_product(color[0], isospin[0])
    checks.check(
        "fresh mixed tensor fails the common-commutant test",
        any(
            not _zero(_commutator(mixed, generator))
            for generator in color_embedded + isospin_embedded
        ),
    )
    alternate_scalar = sp.Rational(7, 3) * sp.eye(6)
    checks.check(
        "fresh scalar normalization family all commute",
        all(
            _zero(_commutator(alternate_scalar, generator))
            for generator in color_embedded + isospin_embedded
        ),
    )

    full_turn_one = sp.simplify(sp.exp(2 * sp.pi * sp.I * 1)) * sp.eye(6)
    full_turn_half = sp.simplify(sp.exp(2 * sp.pi * sp.I * sp.Rational(1, 2))) * sp.eye(6)
    checks.check(
        "fresh compact U1 period separates integer and half weights",
        full_turn_one == sp.eye(6) and full_turn_half == -sp.eye(6),
    )

    omega = -sp.Rational(1, 2) + sp.sqrt(3) * sp.I / 2
    color_center = omega * sp.eye(3)
    isospin_center = -sp.eye(2)
    abelian_phase = -sp.conjugate(omega)
    central_action = sp.simplify(
        abelian_phase * sp.kronecker_product(color_center, isospin_center)
    )
    checks.check(
        "fresh tensor representation has a nontrivial finite central kernel",
        central_action == sp.eye(6)
        and color_center != sp.eye(3)
        and isospin_center != sp.eye(2)
        and abelian_phase != 1,
    )
    checks.check(
        "fresh local rank cannot distinguish direct product from central quotient",
        full_matrix.rank() == 12
        and sp.simplify(abelian_phase**6) == 1,
    )

    coordinate = sp.symbols("x", real=True)
    local_parameter = sp.Function("alpha")(coordinate)
    field = sp.Function("psi")(coordinate)
    phase = sp.exp(sp.I * local_parameter)
    residual = sp.simplify(
        sp.diff(phase * field, coordinate) - phase * sp.diff(field, coordinate)
    )
    checks.check(
        "fresh constant-phase norm does not imply local derivative covariance",
        residual == sp.I * phase * field * sp.diff(local_parameter, coordinate)
        and residual != 0,
    )

    first_coupling, second_coupling, third_coupling = sp.symbols(
        "g3 g2 g1", positive=True
    )
    connection = (
        first_coupling * color_embedded[0]
        + second_coupling * isospin_embedded[0]
        + third_coupling * abelian
    )
    checks.check(
        "fresh three couplings remain independent declared coordinates",
        sp.simplify(sp.diff(connection, first_coupling) - color_embedded[0])
        == sp.zeros(6)
        and sp.simplify(sp.diff(connection, second_coupling) - isospin_embedded[0])
        == sp.zeros(6)
        and sp.simplify(sp.diff(connection, third_coupling) - abelian)
        == sp.zeros(6),
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P163 INDEPENDENT ALL {result} CHECKS PASS")
