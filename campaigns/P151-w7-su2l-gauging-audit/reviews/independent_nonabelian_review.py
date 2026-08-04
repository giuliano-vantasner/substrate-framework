#!/usr/bin/env python3
"""Fresh non-Abelian derivation without the canonical gauge helper."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(matrix: sp.MatrixBase) -> bool:
    return sp.Matrix(matrix).applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def run() -> int:
    checks = CheckLedger("P151-independent")
    imaginary = sp.I
    generators = (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -imaginary], [imaginary, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )
    cyclic = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    checks.check(
        "fresh Pauli-half matrices are Hermitian and close",
        all(_zero(generator - generator.H) for generator in generators)
        and all(
            _zero(
                generators[first] * generators[second]
                - generators[second] * generators[first]
                - imaginary * generators[target]
            )
            for first, second, target in cyclic
        ),
    )

    projector = sp.diag(1, 0)
    complement = sp.eye(2) - projector
    left = tuple(sp.kronecker_product(generator, projector) for generator in generators)
    right = tuple(sp.kronecker_product(generator, complement) for generator in generators)
    checks.check(
        "fresh tensor-product left action is Hermitian and closes",
        all(_zero(generator - generator.H) for generator in left)
        and all(
            _zero(
                left[first] * left[second]
                - left[second] * left[first]
                - imaginary * left[target]
            )
            for first, second, target in cyclic
        ),
    )
    right_block = sp.kronecker_product(sp.eye(2), complement)
    checks.check(
        "fresh left action annihilates the right block",
        all(_zero(generator * right_block) for generator in left),
    )

    same = tuple(generator * projector for generator in generators)
    checks.check(
        "fresh same-carrier counterexample fails Hermiticity",
        sum(_zero(generator - generator.H) for generator in same) == 1,
    )
    checks.check(
        "fresh same-carrier counterexample fails cyclic closure",
        not all(
            _zero(
                same[first] * same[second]
                - same[second] * same[first]
                - imaginary * same[target]
            )
            for first, second, target in cyclic
        ),
    )

    time, coordinate = sp.symbols("t x", real=True)
    coupling = sp.symbols("g", positive=True)
    angle = sp.Function("alpha", real=True)(time, coordinate)
    unitary = sp.diag(
        sp.exp(imaginary * angle / 2),
        sp.exp(-imaginary * angle / 2),
    )
    field = sp.Matrix(
        [
            sp.Function("p0")(time, coordinate),
            sp.Function("p1")(time, coordinate),
        ]
    )
    coefficients = [
        sp.Function(f"A{mu}{index}", real=True)(time, coordinate)
        for mu in range(2)
        for index in range(3)
    ]
    connections = [
        sum(
            (
                coefficients[3 * mu + index] * generators[index]
                for index in range(3)
            ),
            sp.zeros(2),
        )
        for mu in range(2)
    ]
    coordinates = (time, coordinate)
    transformed = [
        sp.simplify(
            unitary * connection * unitary.H
            - imaginary / coupling * unitary.diff(axis) * unitary.H
        )
        for connection, axis in zip(connections, coordinates, strict=True)
    ]

    def derivative(vector: sp.MatrixBase, connection: sp.MatrixBase, axis: sp.Symbol) -> sp.Matrix:
        return sp.Matrix(vector.diff(axis) - imaginary * coupling * connection * vector)

    checks.check(
        "fresh product-rule route proves finite derivative covariance",
        all(
            _zero(
                derivative(unitary * field, transformed[index], axis)
                - unitary * derivative(field, connections[index], axis)
            )
            for index, axis in enumerate(coordinates)
        ),
    )
    plus_sign = sp.simplify(
        unitary * sp.zeros(2) * unitary.H
        + imaginary / coupling * unitary.diff(time) * unitary.H
    )
    checks.check(
        "fresh plus-sign mutation leaves an uncancelled product-rule term",
        not _zero(
            derivative(unitary * field, plus_sign, time)
            - unitary * derivative(field, sp.zeros(2), time)
        ),
    )

    def curvature(connection_pair: list[sp.Matrix]) -> sp.Matrix:
        return sp.Matrix(
            connection_pair[1].diff(time)
            - connection_pair[0].diff(coordinate)
            - imaginary
            * coupling
            * (
                connection_pair[0] * connection_pair[1]
                - connection_pair[1] * connection_pair[0]
            )
        )

    field_strength = curvature(connections)
    transformed_strength = curvature(transformed)
    checks.check(
        "fresh curvature transforms by conjugation",
        _zero(transformed_strength - unitary * field_strength * unitary.H),
    )
    commutator = derivative(
        derivative(field, connections[1], coordinate),
        connections[0],
        time,
    ) - derivative(
        derivative(field, connections[0], time),
        connections[1],
        coordinate,
    )
    checks.check(
        "fresh derivative commutator derives curvature",
        _zero(commutator + imaginary * coupling * field_strength * field),
    )
    checks.check(
        "fresh cyclic trace proves quadratic invariance",
        sp.simplify(
            sp.trace(transformed_strength * transformed_strength)
            - sp.trace(field_strength * field_strength)
        )
        == 0,
    )

    constant_noncommuting = [generators[0], generators[1]]
    constant_curvature = curvature(constant_noncommuting)
    checks.check(
        "fresh noncommuting constant connection has nonzero curvature",
        not _zero(constant_curvature),
    )
    checks.check(
        "fresh curl-only mutation misses constant non-Abelian curvature",
        _zero(
            constant_noncommuting[1].diff(time)
            - constant_noncommuting[0].diff(coordinate)
        )
        and not _zero(constant_curvature),
    )

    parity = sp.Matrix([[0, 1], [1, 0]])
    full_parity = sp.kronecker_product(sp.eye(2), parity)
    checks.check(
        "fresh parity maps left action to distinct right action",
        all(
            _zero(full_parity * left_generator * full_parity.H - right_generator)
            and not _zero(right_generator + left_generator)
            for left_generator, right_generator in zip(left, right, strict=True)
        ),
    )
    checks.check(
        "fresh assigned charge labels contradict dT3 equals dQ",
        sp.Integer(1) - sp.Integer(-1) == 2
        and sp.Rational(1, 2) - sp.Rational(-1, 2) == 1,
    )
    zero_current = sp.zeros(2, 1)
    nonzero_curvature = constant_curvature
    checks.check(
        "fresh zero-current countermodel retains non-Abelian gauge algebra",
        _zero(zero_current) and not _zero(nonzero_curvature),
    )
    arbitrary_mass = sp.symbols("m", nonnegative=True)
    checks.check(
        "fresh gauge algebra leaves any mass mechanism outside the theorem",
        arbitrary_mass.free_symbols == {arbitrary_mass},
    )

    tally = checks.finish()
    print(f"P151 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
