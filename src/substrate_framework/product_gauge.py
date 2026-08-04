"""Exact local product-gauge Lie-algebra representation ledgers.

The standard fundamental SU(3) and SU(2) factors can act on
``C^3 tensor C^2`` through separate tensor factors.  A nonzero scalar matrix
then supplies one faithful local ``u(1)`` generator.  This finite-dimensional
construction determines a Lie algebra representation only.  It does not pick
a global direct product or discrete quotient, a compact-U(1) normalization,
matter fields, an action, gauge bosons, currents, couplings, or a physical
Standard Model interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Any, Sequence

import sympy as sp

from .su2_doublets import su2_fundamental_ledger
from .su3 import fundamental_generators, structure_constant


def _immutable_simplified(value: Any) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(sp.Matrix(value).applyfunc(sp.simplify))


def _zero_matrix(value: sp.MatrixBase) -> bool:
    matrix = _immutable_simplified(value)
    return matrix == sp.zeros(*matrix.shape)


def _exact_real_nonzero(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact")
    if expression.is_real is not True:
        raise ValueError(f"{name} must be explicitly real")
    if expression.is_zero is not False:
        qualifier = "provably nonzero" if expression.is_zero is None else "nonzero"
        raise ValueError(f"{name} must be {qualifier}")
    return sp.simplify(expression)


def _positive_exact(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact")
    if expression.is_real is not True or expression.is_positive is not True:
        raise ValueError(f"{name} must be explicitly positive")
    return sp.simplify(expression)


def _exact_entries(values: Sequence[Any], expected: int, name: str) -> tuple[sp.Expr, ...]:
    if len(values) != expected:
        raise ValueError(f"{name} must contain exactly {expected} entries")
    expressions = tuple(sp.sympify(value) for value in values)
    if any(expression.has(sp.Float) for expression in expressions):
        raise ValueError(f"{name} must contain exact entries")
    return tuple(sp.simplify(expression) for expression in expressions)


def _commutator(first: sp.MatrixBase, second: sp.MatrixBase) -> sp.ImmutableMatrix:
    return _immutable_simplified(first * second - second * first)


def _normalized_nullspace_basis(matrix: sp.MatrixBase) -> tuple[sp.ImmutableMatrix, ...]:
    basis: list[sp.ImmutableMatrix] = []
    for vector in matrix.nullspace():
        pivot = next(entry for entry in vector if entry != 0)
        normalized = sp.Matrix(vector / pivot)
        basis.append(_immutable_simplified(normalized.reshape(6, 6)))
    return tuple(basis)


@cache
def _joint_commutant_basis(
    generators: tuple[sp.ImmutableMatrix, ...],
) -> tuple[sp.ImmutableMatrix, ...]:
    entries = sp.symbols("m0:36")
    candidate = sp.Matrix(6, 6, entries)
    equations = tuple(
        entry
        for generator in generators
        for entry in candidate * generator - generator * candidate
    )
    coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, entries)
    return _normalized_nullspace_basis(coefficient_matrix)


@dataclass(frozen=True)
class StandardProductGaugeAlgebraLedger:
    """Exact standard tensor-factor ``su3 + su2 + u1`` local algebra data."""

    abelian_weight: sp.Expr
    color_generators: tuple[sp.ImmutableMatrix, ...]
    isospin_generators: tuple[sp.ImmutableMatrix, ...]
    color_embeddings: tuple[sp.ImmutableMatrix, ...]
    isospin_embeddings: tuple[sp.ImmutableMatrix, ...]
    abelian_generator: sp.ImmutableMatrix
    generators: tuple[sp.ImmutableMatrix, ...]
    color_commutator_residuals: tuple[sp.ImmutableMatrix, ...]
    isospin_commutator_residuals: tuple[sp.ImmutableMatrix, ...]
    cross_commutator_residuals: tuple[sp.ImmutableMatrix, ...]
    flattened_generator_matrix: sp.ImmutableMatrix
    generator_rank: int
    joint_commutant_basis: tuple[sp.ImmutableMatrix, ...]
    compact_u1_full_turn: sp.ImmutableMatrix
    compact_u1_full_turn_residual: sp.ImmutableMatrix
    compact_u1_single_valued: bool

    def factor_commutator_residuals(self, candidate: Any) -> tuple[sp.ImmutableMatrix, ...]:
        """Return commutators of a 6-by-6 candidate with both non-Abelian factors."""

        matrix = sp.Matrix(candidate)
        if matrix.shape != (6, 6):
            raise ValueError("candidate must be 6 by 6")
        if any(entry.has(sp.Float) for entry in matrix):
            raise ValueError("candidate must contain exact entries")
        return tuple(
            _commutator(matrix, generator)
            for generator in self.color_embeddings + self.isospin_embeddings
        )


@dataclass(frozen=True)
class ProductGaugeConnectionComponent:
    """One declared algebra-valued connection component split by factor."""

    couplings: tuple[sp.Expr, sp.Expr, sp.Expr]
    color_components: tuple[sp.Expr, ...]
    isospin_components: tuple[sp.Expr, ...]
    abelian_component: sp.Expr
    color_term: sp.ImmutableMatrix
    isospin_term: sp.ImmutableMatrix
    abelian_term: sp.ImmutableMatrix
    total: sp.ImmutableMatrix


def standard_product_gauge_algebra(
    abelian_weight: Any,
) -> StandardProductGaugeAlgebraLedger:
    r"""Construct the standard faithful local ``su(3)+su(2)+u(1)`` representation.

    The supplied Abelian weight must be exact, explicitly real, and provably
    nonzero.  Faithfulness here is a Lie-algebra statement: the twelve embedded
    matrices have rank twelve.  Under the separately chosen compact-U(1)
    parameter period ``theta ~ theta+2*pi``, ``compact_u1_single_valued`` records
    whether ``exp(2*pi*i*weight)`` is one.  That global condition is not inferred
    from the local algebra.
    """

    weight = _exact_real_nonzero(abelian_weight, "abelian weight")
    color = tuple(_immutable_simplified(generator) for generator in fundamental_generators())
    isospin = su2_fundamental_ledger().generators
    identity_three = sp.eye(3)
    identity_two = sp.eye(2)
    identity_six = sp.eye(6)
    color_embeddings = tuple(
        _immutable_simplified(sp.kronecker_product(generator, identity_two))
        for generator in color
    )
    isospin_embeddings = tuple(
        _immutable_simplified(sp.kronecker_product(identity_three, generator))
        for generator in isospin
    )
    abelian = _immutable_simplified(weight * identity_six)
    generators = color_embeddings + isospin_embeddings + (abelian,)

    color_residuals = tuple(
        _immutable_simplified(
            _commutator(color_embeddings[first], color_embeddings[second])
            - sp.I
            * sum(
                (
                    structure_constant(first, second, target)
                    * color_embeddings[target]
                    for target in range(8)
                ),
                sp.zeros(6),
            )
        )
        for first in range(8)
        for second in range(8)
    )
    isospin_residuals = tuple(
        _immutable_simplified(
            _commutator(isospin_embeddings[first], isospin_embeddings[second])
            - sp.I
            * sum(
                (
                    sp.LeviCivita(first, second, target)
                    * isospin_embeddings[target]
                    for target in range(3)
                ),
                sp.zeros(6),
            )
        )
        for first in range(3)
        for second in range(3)
    )
    cross_residuals = tuple(
        _commutator(color_generator, isospin_generator)
        for color_generator in color_embeddings
        for isospin_generator in isospin_embeddings
    ) + tuple(
        _commutator(generator, abelian)
        for generator in color_embeddings + isospin_embeddings
    )
    columns = tuple(sp.Matrix(generator).reshape(36, 1) for generator in generators)
    flattened = sp.ImmutableMatrix(sp.Matrix.hstack(*columns))
    commutant = _joint_commutant_basis(color_embeddings + isospin_embeddings)
    full_turn_phase = sp.simplify(sp.exp(2 * sp.pi * sp.I * weight))
    full_turn = _immutable_simplified(full_turn_phase * identity_six)
    full_turn_residual = _immutable_simplified(full_turn - identity_six)
    return StandardProductGaugeAlgebraLedger(
        abelian_weight=weight,
        color_generators=color,
        isospin_generators=isospin,
        color_embeddings=color_embeddings,
        isospin_embeddings=isospin_embeddings,
        abelian_generator=abelian,
        generators=generators,
        color_commutator_residuals=color_residuals,
        isospin_commutator_residuals=isospin_residuals,
        cross_commutator_residuals=cross_residuals,
        flattened_generator_matrix=flattened,
        generator_rank=int(flattened.rank()),
        joint_commutant_basis=commutant,
        compact_u1_full_turn=full_turn,
        compact_u1_full_turn_residual=full_turn_residual,
        compact_u1_single_valued=_zero_matrix(full_turn_residual),
    )


def product_gauge_connection_component(
    algebra: StandardProductGaugeAlgebraLedger,
    color_components: Sequence[Any],
    isospin_components: Sequence[Any],
    abelian_component: Any,
    couplings: Sequence[Any],
) -> ProductGaugeConnectionComponent:
    """Return one supplied algebra-valued connection component.

    This is a linear finite-matrix construction.  It does not supply a
    coordinate derivative, transformation law, action, or field equation.
    """

    if not isinstance(algebra, StandardProductGaugeAlgebraLedger):
        raise TypeError("algebra must be a StandardProductGaugeAlgebraLedger")
    color_values = _exact_entries(color_components, 8, "color components")
    isospin_values = _exact_entries(isospin_components, 3, "isospin components")
    abelian_value = sp.sympify(abelian_component)
    if abelian_value.has(sp.Float):
        raise ValueError("abelian component must be exact")
    if len(couplings) != 3:
        raise ValueError("couplings must contain exactly three entries")
    strengths = tuple(
        _positive_exact(value, f"coupling {index}")
        for index, value in enumerate(couplings)
    )
    color_term = _immutable_simplified(
        strengths[0]
        * sum(
            (
                component * generator
                for component, generator in zip(
                    color_values, algebra.color_embeddings, strict=True
                )
            ),
            sp.zeros(6),
        )
    )
    isospin_term = _immutable_simplified(
        strengths[1]
        * sum(
            (
                component * generator
                for component, generator in zip(
                    isospin_values, algebra.isospin_embeddings, strict=True
                )
            ),
            sp.zeros(6),
        )
    )
    abelian_term = _immutable_simplified(
        strengths[2] * abelian_value * algebra.abelian_generator
    )
    total = _immutable_simplified(color_term + isospin_term + abelian_term)
    return ProductGaugeConnectionComponent(
        couplings=(strengths[0], strengths[1], strengths[2]),
        color_components=color_values,
        isospin_components=isospin_values,
        abelian_component=sp.simplify(abelian_value),
        color_term=color_term,
        isospin_term=isospin_term,
        abelian_term=abelian_term,
        total=total,
    )
