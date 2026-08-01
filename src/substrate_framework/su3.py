"""Exact invariants of the standard fundamental SU(3) representation."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class SU3Invariants:
    """Representation invariants in the ``T_a=lambda_a/2`` convention."""

    dynkin_index: sp.Expr
    fundamental_casimir: sp.Expr
    adjoint_casimir: sp.Expr


def fundamental_generators() -> tuple[sp.Matrix, ...]:
    """Return the eight Hermitian generators ``T_a=lambda_a/2``."""

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
    return tuple(matrix / 2 for matrix in gell_mann)


def _structure_constant(
    generators: tuple[sp.Matrix, ...], a: int, b: int, c: int
) -> sp.Expr:
    commutator = generators[a] * generators[b] - generators[b] * generators[a]
    return sp.simplify(-2 * sp.I * sp.trace(commutator * generators[c]))


def structure_constant(a: int, b: int, c: int) -> sp.Expr:
    """Return ``f_abc`` for ``[T_a,T_b]=i*f_abc*T_c`` (zero-based)."""

    if any(index < 0 or index >= 8 for index in (a, b, c)):
        raise IndexError("SU(3) generator index must lie in 0..7")
    return _structure_constant(fundamental_generators(), a, b, c)


@cache
def invariants() -> SU3Invariants:
    """Compute ``T_F``, ``C_F``, and ``C_A`` from explicit matrices."""

    generators = fundamental_generators()
    dynkin = sp.trace(generators[0] * generators[0])
    fundamental = sp.simplify(
        sum((generator * generator for generator in generators), sp.zeros(3))
    )
    adjoint_generators = tuple(
        sp.Matrix(
            8,
            8,
            lambda b, c: -sp.I * _structure_constant(generators, a, b, c),
        )
        for a in range(8)
    )
    adjoint = sp.simplify(
        sum((generator * generator for generator in adjoint_generators), sp.zeros(8))
    )
    if fundamental != fundamental[0, 0] * sp.eye(3):
        raise ValueError("fundamental Casimir is not scalar")
    if adjoint != adjoint[0, 0] * sp.eye(8):
        raise ValueError("adjoint Casimir is not scalar")
    return SU3Invariants(dynkin, fundamental[0, 0], adjoint[0, 0])


def conditional_one_loop_coefficient(
    flavor_count: Any,
    gauge_loop_weight: Any,
    matter_loop_weight: Any,
) -> sp.Expr:
    """Compose derived SU(3) invariants with declared one-loop weights."""

    flavors = sp.sympify(flavor_count)
    if flavors.is_number and (
        flavors.is_integer is not True or flavors.is_nonnegative is not True
    ):
        raise ValueError("flavor_count must be a nonnegative integer")
    gauge = sp.sympify(gauge_loop_weight)
    matter = sp.sympify(matter_loop_weight)
    values = invariants()
    return sp.simplify(
        gauge * values.adjoint_casimir
        - matter * values.dynkin_index * flavors
    )
