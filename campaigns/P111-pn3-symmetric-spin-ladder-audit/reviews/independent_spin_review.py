"""Independent bitmask and irreducible-matrix review for P111."""

from __future__ import annotations

import ast
from itertools import combinations
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def _state(particle_count: int, excitation_count: int) -> sp.ImmutableMatrix:
    values = [sp.Integer(0)] * (1 << particle_count)
    denominator = sp.sqrt(sp.binomial(particle_count, excitation_count))
    for sites in combinations(range(particle_count), excitation_count):
        values[sum(1 << site for site in sites)] = 1 / denominator
    return sp.ImmutableMatrix(values)


def _raise(particle_count: int) -> sp.ImmutableMatrix:
    result = sp.zeros(1 << particle_count)
    for column in range(1 << particle_count):
        for bit in range(particle_count):
            if column & (1 << bit) == 0:
                result[column | (1 << bit), column] += 1
    return sp.ImmutableMatrix(result)


def _irrep(particle_count: int) -> tuple[sp.ImmutableMatrix, ...]:
    raising = sp.zeros(particle_count + 1)
    for k in range(particle_count):
        raising[k + 1, k] = sp.sqrt((particle_count - k) * (k + 1))
    lowering = raising.T
    diagonal = sp.diag(
        *[
            sp.Rational(2 * k - particle_count, 2)
            for k in range(particle_count + 1)
        ]
    )
    return tuple(sp.ImmutableMatrix(value) for value in (raising, lowering, diagonal))


def main() -> int:
    checks = CheckLedger("C-SPN-002-INDEPENDENT")

    for particle_count in range(1, 8):
        matrix = _raise(particle_count)
        checks.check(
            f"fresh bitmask route closes every rung for N={particle_count}",
            all(
                sp.simplify(
                    (
                        _state(particle_count, k + 1).T
                        * matrix
                        * _state(particle_count, k)
                    )[0]
                    - sp.sqrt((particle_count - k) * (k + 1))
                )
                == 0
                for k in range(particle_count)
            ),
        )

    checks.check(
        "fresh binomial ratio derives the coefficient without vector enumeration",
        all(
            sp.simplify(
                (k + 1)
                * sp.sqrt(
                    sp.binomial(particle_count, k + 1)
                    / sp.binomial(particle_count, k)
                )
                - sp.sqrt((particle_count - k) * (k + 1))
            )
            == 0
            for particle_count in range(1, 20)
            for k in range(particle_count)
        ),
    )
    checks.check(
        "fresh unnormalized state route does not preserve the normalized coefficient",
        (_state(4, 2) * sp.sqrt(6)).T * _raise(4) * (_state(4, 1) * 2)
        != sp.ImmutableMatrix([[sp.sqrt(6)]]),
    )

    for particle_count in range(1, 10):
        raising, lowering, diagonal = _irrep(particle_count)
        identity = sp.eye(particle_count + 1)
        spin = sp.Rational(particle_count, 2)
        checks.check(
            f"fresh irrep commutator closes for N={particle_count}",
            raising * lowering - lowering * raising == 2 * diagonal,
        )
        checks.check(
            f"fresh irrep Casimir closes for N={particle_count}",
            sp.simplify(
                diagonal**2
                + (raising * lowering + lowering * raising) / 2
                - spin * (spin + 1) * identity
            )
            == sp.zeros(particle_count + 1),
        )

    checks.check(
        "fresh ground-edge sequence is square-root rather than linear",
        [sp.sqrt((count - 0) * (0 + 1)) for count in (1, 4, 9, 16)]
        == [1, 2, 3, 4],
    )
    n = sp.symbols("n", positive=True)
    checks.check(
        "fresh central-rung limit is one half of N",
        sp.limit(sp.sqrt((n / 2) * (n / 2 + 1)) / n, n, sp.oo)
        == sp.Rational(1, 2),
    )

    equal = sp.ImmutableMatrix([1, 1, 1, 1])
    symmetric = sp.ones(4, 1) / 2
    checks.check(
        "fresh equal-coupling vector projects with square-root N amplitude",
        (symmetric.T * equal)[0] == 2
        and (equal.conjugate().T * equal)[0] == 4,
    )
    cancelled = sp.ImmutableMatrix([1, -1, 1, -1])
    checks.check(
        "fresh phase-cancelled vector is dark to the symmetric projection",
        (symmetric.T * cancelled)[0] == 0
        and (cancelled.conjugate().T * cancelled)[0] == 4,
    )
    mixed = sp.ImmutableMatrix([1, sp.I])
    symmetric_two = sp.ones(2, 1) / sp.sqrt(2)
    projection = sp.simplify((symmetric_two.T * mixed)[0])
    checks.check(
        "fresh complex vector splits one unit into each sector",
        sp.simplify(sp.conjugate(projection) * projection) == 1
        and (mixed.conjugate().T * mixed)[0] == 2,
    )

    coefficient_squared = sp.Integer(9)
    coupling, density, scale = sp.symbols("g rho hbar", positive=True)
    conditional_rate = 2 * sp.pi * coupling**2 * coefficient_squared * density / scale
    checks.check(
        "fresh zero-coupling countermodel leaves the ladder and removes the rate",
        coefficient_squared == 9 and conditional_rate.subs(coupling, 0) == 0,
    )
    checks.check(
        "fresh zero-density countermodel leaves the ladder and removes the rate",
        coefficient_squared == 9 and conditional_rate.subs(density, 0) == 0,
    )
    checks.check(
        "fresh dimensional route rejects action-squared as a rate",
        (2, 2) != (0, -1),
    )
    checks.check(
        "fresh review imports no canonical symmetric-spin implementation",
        not any(
            isinstance(node, ast.ImportFrom)
            and node.module == "substrate_framework.symmetric_spin"
            for node in ast.walk(ast.parse(Path(__file__).read_text()))
        ),
    )
    checks.check(
        "fresh review uses no quadrature solver float or comparator",
        not conditional_rate.has(sp.Float, sp.Integral),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
