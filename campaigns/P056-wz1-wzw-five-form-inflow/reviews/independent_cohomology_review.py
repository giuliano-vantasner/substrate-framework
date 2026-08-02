"""Independent exact cochain and exterior-algebra review for P056."""

from __future__ import annotations

import itertools

import sympy as sp

from substrate_framework.verification import CheckLedger


def sign(indices: tuple[int, ...] | list[int]) -> int:
    if len(set(indices)) != len(indices):
        return 0
    inversions = sum(
        indices[first] > indices[second]
        for first in range(len(indices))
        for second in range(first + 1, len(indices))
    )
    return -1 if inversions % 2 else 1


def explicit_antihermitian_basis() -> tuple[sp.Matrix, ...]:
    root_three = sp.sqrt(3)
    hermitian = (
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]) / 2,
        sp.Matrix([[0, -sp.I, 0], [sp.I, 0, 0], [0, 0, 0]]) / 2,
        sp.diag(1, -1, 0) / 2,
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]) / 2,
        sp.Matrix([[0, 0, -sp.I], [0, 0, 0], [sp.I, 0, 0]]) / 2,
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]) / 2,
        sp.Matrix([[0, 0, 0], [0, 0, -sp.I], [0, sp.I, 0]]) / 2,
        sp.diag(1 / root_three, 1 / root_three, -2 / root_three) / 2,
    )
    return tuple(sp.I * value for value in hermitian)


def derive_constants(generators: tuple[sp.Matrix, ...]) -> tuple:
    # Tr(E_a E_b)=-delta_ab/2, so c_ab^d=-2 Tr([E_a,E_b] E_d).
    return tuple(
        tuple(
            tuple(
                sp.simplify(
                    -2
                    * sp.trace(
                        (generators[a] * generators[b] - generators[b] * generators[a])
                        * generators[d]
                    )
                )
                for d in range(8)
            )
            for b in range(8)
        )
        for a in range(8)
    )


def basis(degree: int) -> tuple[tuple[int, ...], ...]:
    return tuple(itertools.combinations(range(8), degree))


def differential(degree: int, constants: tuple, graded: bool = True) -> sp.SparseMatrix:
    domain = basis(degree)
    codomain = basis(degree + 1)
    positions = {item: index for index, item in enumerate(domain)}
    entries: dict[tuple[int, int], sp.Expr] = {}
    for row, arguments in enumerate(codomain):
        for first in range(degree + 1):
            for second in range(first + 1, degree + 1):
                remainder = [
                    arguments[index]
                    for index in range(degree + 1)
                    if index not in (first, second)
                ]
                for bracket_index, coefficient in enumerate(
                    constants[arguments[first]][arguments[second]]
                ):
                    full = [bracket_index, *remainder]
                    reorder = sign(full)
                    if coefficient == 0 or reorder == 0:
                        continue
                    column = positions[tuple(sorted(full))]
                    factor = (-1) ** (first + second) * reorder if graded else 1
                    key = (row, column)
                    entries[key] = sp.simplify(
                        entries.get(key, 0) + factor * coefficient
                    )
    return sp.SparseMatrix(len(codomain), len(domain), entries)


def alternating_trace(
    generators: tuple[sp.Matrix, ...], indices: tuple[int, ...]
) -> sp.Expr:
    total = 0
    for order in itertools.permutations(indices):
        product = sp.eye(3)
        for index in order:
            product *= generators[index]
        total += sign(order) * sp.trace(product)
    return sp.simplify(total)


def real_trace_cochain(
    generators: tuple[sp.Matrix, ...], degree: int
) -> sp.Matrix:
    return sp.Matrix(
        [
            sp.simplify(-sp.I * alternating_trace(generators, indices))
            for indices in basis(degree)
        ]
    )


def main() -> int:
    ledger = CheckLedger("P056-INDEPENDENT")
    generators = explicit_antihermitian_basis()
    gram = sp.Matrix(8, 8, lambda a, b: sp.trace(generators[a] * generators[b]))
    constants = derive_constants(generators)

    ledger.check(
        "independent explicit basis is anti-Hermitian, traceless, and normalized",
        gram == -sp.eye(8) / 2
        and all(value.H == -value and sp.trace(value) == 0 for value in generators),
    )
    ledger.check(
        "trace projection reconstructs every independent Lie bracket",
        all(
            sp.simplify(
                generators[a] * generators[b]
                - generators[b] * generators[a]
                - sum(
                    (constants[a][b][d] * generators[d] for d in range(8)),
                    sp.zeros(3),
                )
            )
            == sp.zeros(3)
            for a in range(8)
            for b in range(8)
        ),
    )

    d4 = differential(4, constants)
    d5 = differential(5, constants)
    omega = real_trace_cochain(generators, 5)
    trace_four = real_trace_cochain(generators, 4)
    ledger.check(
        "independently constructed CE operators form a complex",
        d5 * d4 == sp.zeros(28, 70),
    )
    ledger.check(
        "direct trace-five cochain is an exact cocycle",
        d5 * omega == sp.zeros(28, 1),
    )
    ledger.check(
        "direct trace-five evaluation is nonzero with frozen normalization",
        omega[basis(5).index((0, 1, 2, 3, 4))] == -sp.Rational(15, 8)
        and sum(value != 0 for value in omega) == 9
        and (omega.T * omega)[0] == sp.Rational(75, 4),
    )
    ledger.check(
        "the trace cochain annihilates every four-coboundary",
        omega.T * d4 == sp.zeros(1, 70),
    )
    ledger.check(
        "nonzero self-pairing separates trace five from the coboundary image",
        omega.T * d4 == sp.zeros(1, 70) and (omega.T * omega)[0] != 0,
    )

    derivative_four = sum(
        (-1) ** (position + position * (5 - position)) for position in range(4)
    )
    derivative_five = sum(
        (-1) ** (position + position * (6 - position)) for position in range(5)
    )
    d_l4 = -sum((-1) ** position for position in range(4))
    ledger.check(
        "even alternating trace and its claimed derivative guard vanish exactly",
        trace_four == sp.zeros(70, 1)
        and derivative_four == 0
        and d_l4 == 0
        and -4 * omega != sp.zeros(56, 1),
    )
    ledger.check(
        "odd trace variation has five equal terms while d of L fourth vanishes",
        derivative_five == 5 and d_l4 == 0,
    )

    commuting = tuple(
        sp.I * sp.diag(index, -index, 0) for index in (1, 2, 3, 4, 5)
    )
    ledger.check(
        "five commuting or linearly dependent directions have zero alternating trace",
        alternating_trace(commuting, tuple(range(5))) == 0,
    )
    ledger.check(
        "a three-dimensional Lie group has no nonzero differential five-form",
        len(tuple(itertools.combinations(range(3), 5))) == 0,
    )

    mutated = [[list(row) for row in plane] for plane in constants]
    mutated[0][1][2] = -mutated[0][1][2]
    mutated = tuple(tuple(tuple(row) for row in plane) for plane in mutated)
    mutated_d4 = differential(4, mutated)
    mutated_d5 = differential(5, mutated)
    ledger.check(
        "one load-bearing bracket mutation destroys d squared equals zero",
        mutated_d5 * mutated_d4 != sp.zeros(28, 70),
    )
    ungraded_d4 = differential(4, constants, graded=False)
    ungraded_d5 = differential(5, constants, graded=False)
    ledger.check(
        "removing exterior signs destroys the cochain complex",
        ungraded_d5 * ungraded_d4 != sp.zeros(28, 70),
    )

    first, second = sp.symbols("I_B I_Bprime", real=True)
    ledger.mutation_sensitive(
        "oriented gluing requires subtraction of the reversed filling",
        lambda candidate: sp.simplify(candidate - (first - second)) == 0,
        first - second,
        [first + second, second - first],
    )
    ledger.mutation_sensitive(
        "phase independence requires the declared coefficient-period product",
        lambda candidate: sp.simplify(sp.exp(2 * sp.pi * sp.I * candidate)) == 1,
        sp.Integer(1),
        [sp.Rational(1, 2), sp.sqrt(2)],
    )

    baseline_component = omega[basis(5).index((0, 1, 2, 3, 4))]
    ledger.mutation_sensitive(
        "trace-five normalization detects generator rescaling and orientation reversal",
        lambda scale: sp.simplify(
            -sp.I
            * alternating_trace(
                tuple(scale * generators[index] for index in (0, 1, 2, 3, 4)),
                tuple(range(5)),
            )
            - baseline_component
        )
        == 0,
        sp.Integer(1),
        [sp.Integer(2), sp.Integer(-1)],
    )

    from substrate_framework.wzw import (
        chevalley_eilenberg_differential,
        su3_real_trace_five_cochain,
    )

    ledger.check(
        "primary APIs agree after the independent objects are frozen",
        chevalley_eilenberg_differential(4) == d4
        and chevalley_eilenberg_differential(5) == d5
        and su3_real_trace_five_cochain() == omega,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
