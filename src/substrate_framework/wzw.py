"""Exact SU(3) trace-five-form and conditional filling algebra.

This module contains mathematical differential-form statements only.  It does
not derive a WZW level, a period normalization, a baryon current, a gauge
anomaly, or a physical substrate identification.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from itertools import combinations, permutations
from typing import Any, Sequence

import sympy as sp

from .su3 import fundamental_generators, structure_constant


CochainIndex = tuple[int, ...]
StructureConstants = tuple[tuple[tuple[sp.Expr, ...], ...], ...]


@dataclass(frozen=True)
class SU3TraceFiveCohomology:
    """Exact finite-dimensional evidence for the invariant trace five-form."""

    algebra_dimension: int
    four_cochain_dimension: int
    five_cochain_dimension: int
    six_cochain_dimension: int
    d4_rank: int
    d5_rank: int
    five_cocycle_dimension: int
    fifth_cohomology_dimension: int
    trace_nonzero_components: int
    trace_norm_squared: sp.Expr
    augmented_d4_trace_rank: int
    dual_separating_pairing: sp.Expr
    differential_squares_to_zero: bool
    trace_is_closed: bool
    trace_is_exact: bool
    trace_annihilates_coboundaries: bool


def cochain_basis(degree: int, dimension: int = 8) -> tuple[CochainIndex, ...]:
    """Return the ordered exterior-cochain basis of a declared dimension."""

    if not isinstance(degree, int) or not isinstance(dimension, int):
        raise TypeError("degree and dimension must be integers")
    if dimension < 0 or degree < 0 or degree > dimension:
        raise ValueError("require 0 <= degree <= dimension")
    return tuple(combinations(range(dimension), degree))


def _alternating_sign(indices: Sequence[int]) -> int:
    if len(set(indices)) != len(indices):
        return 0
    inversions = sum(
        indices[first] > indices[second]
        for first in range(len(indices))
        for second in range(first + 1, len(indices))
    )
    return -1 if inversions % 2 else 1


def alternating_trace(matrices: Sequence[Any]) -> sp.Expr:
    """Return the unnormalized alternating trace of square matrices.

    For matrix-valued one-forms this is the coefficient convention
    ``sum_perm sgn(perm) Tr(M_p1 ... M_pk)``.  No hidden ``1/k!`` is applied.
    """

    values = tuple(sp.Matrix(matrix) for matrix in matrices)
    if not values:
        raise ValueError("at least one matrix is required")
    shape = values[0].shape
    if shape[0] != shape[1] or any(value.shape != shape for value in values):
        raise ValueError("matrices must be square and share one shape")
    total = sp.Integer(0)
    for order in permutations(range(len(values))):
        product = sp.eye(shape[0])
        for index in order:
            product *= values[index]
        total += _alternating_sign(order) * sp.trace(product)
    return sp.simplify(total)


@cache
def antihermitian_generators() -> tuple[sp.ImmutableMatrix, ...]:
    """Return ``E_a=i*T_a`` for C-LIE-001's Hermitian generators."""

    return tuple(sp.ImmutableMatrix(sp.I * value) for value in fundamental_generators())


@cache
def antihermitian_structure_constants() -> StructureConstants:
    """Return real ``c_ab^d`` for ``[E_a,E_b]=c_ab^d E_d``.

    Since ``E_a=i*T_a`` and C-LIE-001 uses
    ``[T_a,T_b]=i*f_abc*T_c``, this basis has ``c_ab^d=-f_abd``.
    """

    return tuple(
        tuple(
            tuple(sp.simplify(-structure_constant(a, b, d)) for d in range(8))
            for b in range(8)
        )
        for a in range(8)
    )


def _validated_structure_constants(values: Any) -> StructureConstants:
    constants = tuple(
        tuple(tuple(sp.sympify(entry) for entry in row) for row in plane)
        for plane in values
    )
    dimension = len(constants)
    if dimension == 0 or any(len(plane) != dimension for plane in constants):
        raise ValueError("structure constants must be a nonempty cubic array")
    if any(len(row) != dimension for plane in constants for row in plane):
        raise ValueError("structure constants must be a nonempty cubic array")
    return constants


def _build_ce_differential(
    degree: int, constants: StructureConstants
) -> sp.ImmutableSparseMatrix:
    """Build ``d:C^degree -> C^(degree+1)`` in increasing-index bases."""

    dimension = len(constants)
    if not isinstance(degree, int):
        raise TypeError("degree must be an integer")
    if degree < 0 or degree >= dimension:
        raise ValueError("require 0 <= degree < algebra dimension")
    domain = cochain_basis(degree, dimension)
    codomain = cochain_basis(degree + 1, dimension)
    domain_position = {indices: position for position, indices in enumerate(domain)}
    entries: dict[tuple[int, int], sp.Expr] = {}

    for row, arguments in enumerate(codomain):
        for first in range(degree + 1):
            for second in range(first + 1, degree + 1):
                remaining = [
                    arguments[position]
                    for position in range(degree + 1)
                    if position not in (first, second)
                ]
                pair_sign = (-1) ** (first + second)
                for bracket_index, coefficient in enumerate(
                    constants[arguments[first]][arguments[second]]
                ):
                    if coefficient == 0:
                        continue
                    cochain_arguments = [bracket_index, *remaining]
                    reorder_sign = _alternating_sign(cochain_arguments)
                    if reorder_sign == 0:
                        continue
                    column = domain_position[tuple(sorted(cochain_arguments))]
                    key = (row, column)
                    entries[key] = sp.simplify(
                        entries.get(key, 0)
                        + pair_sign * reorder_sign * coefficient
                    )
    return sp.ImmutableSparseMatrix(len(codomain), len(domain), entries)


@cache
def _canonical_ce_differential(degree: int) -> sp.ImmutableSparseMatrix:
    return _build_ce_differential(degree, antihermitian_structure_constants())


def chevalley_eilenberg_differential(
    degree: int,
    constants: Any | None = None,
) -> sp.ImmutableSparseMatrix:
    """Return the exact invariant-cochain differential.

    The default is the anti-Hermitian SU(3) basis derived from C-LIE-001.
    An explicit cubic structure-constant array may be supplied for independent
    algebra checks and mutation-sensitive verification.
    """

    if constants is None:
        return _canonical_ce_differential(degree)
    return _build_ce_differential(degree, _validated_structure_constants(constants))


@cache
def su3_trace_power_cochain(degree: int) -> sp.ImmutableDenseMatrix:
    """Return ``Alt Tr(E_a1...E_ak)`` on increasing SU(3) basis tuples."""

    basis = cochain_basis(degree, 8)
    generators = antihermitian_generators()
    return sp.ImmutableDenseMatrix(
        [alternating_trace(tuple(generators[index] for index in item)) for item in basis]
    )


@cache
def su3_real_trace_five_cochain() -> sp.ImmutableDenseMatrix:
    """Return the real cochain ``-i Alt Tr(theta^5)``.

    The factor ``-i`` converts the imaginary trace of five anti-Hermitian
    generators into a real differential form.  Period normalization remains
    deliberately unspecified.
    """

    return sp.ImmutableDenseMatrix(
        [sp.simplify(-sp.I * value) for value in su3_trace_power_cochain(5)]
    )


def trace_power_cyclic_shift_sign(power: int) -> int:
    """Return the graded sign for moving one odd one-form past ``power-1``."""

    if not isinstance(power, int):
        raise TypeError("power must be an integer")
    if power < 1:
        raise ValueError("power must be positive")
    return (-1) ** (power - 1)


def trace_power_derivative_multiplier(power: int) -> int:
    """Return the coefficient of ``Tr(dL L^(power-1))`` in ``d Tr(L^power)``.

    The exterior derivative contributes alternating Leibniz signs.  After
    graded cyclic reordering the coefficient is ``power`` for odd powers and
    zero for even powers.  In particular, the tempting formula
    ``d Tr(L^4)=4 Tr(dL L^3)`` is false: all four terms cancel.
    """

    if not isinstance(power, int):
        raise TypeError("power must be an integer")
    if power < 1:
        raise ValueError("power must be positive")
    return sum(
        (-1) ** (position + position * (power + 1 - position))
        for position in range(power)
    )


def maurer_cartan_power_derivative_multiplier(power: int) -> int:
    """Return the coefficient in ``d(L^power)=c L^(power+1)`` under ``dL=-L^2``.

    This is a matrix-valued identity before taking a trace.  The coefficient
    is zero for even ``power`` and minus one for odd ``power``.
    """

    if not isinstance(power, int):
        raise TypeError("power must be an integer")
    if power < 1:
        raise ValueError("power must be positive")
    return -sum((-1) ** position for position in range(power))


@cache
def su3_trace_five_cohomology() -> SU3TraceFiveCohomology:
    """Derive exact invariant and global non-exactness evidence.

    The returned rank statements concern the left-invariant
    Chevalley-Eilenberg complex.  For compact SU(3), if this left-invariant
    form had a global primitive, averaging that primitive with normalized Haar
    measure would give a left-invariant primitive.  Thus ``trace_is_exact`` is
    also the global de Rham exactness verdict under that standard averaging
    theorem.
    """

    d4 = chevalley_eilenberg_differential(4)
    d5 = chevalley_eilenberg_differential(5)
    trace_five = su3_real_trace_five_cochain()
    d4_rank = int(d4.rank())
    d5_rank = int(d5.rank())
    augmented_rank = int(d4.row_join(trace_five).rank())
    trace_norm_squared = sp.simplify((trace_five.T * trace_five)[0])
    dual_pairing = trace_norm_squared
    trace_annihilates = trace_five.T * d4 == sp.zeros(1, d4.cols)
    five_cocycle_dimension = len(cochain_basis(5, 8)) - d5_rank
    return SU3TraceFiveCohomology(
        algebra_dimension=8,
        four_cochain_dimension=len(cochain_basis(4, 8)),
        five_cochain_dimension=len(cochain_basis(5, 8)),
        six_cochain_dimension=len(cochain_basis(6, 8)),
        d4_rank=d4_rank,
        d5_rank=d5_rank,
        five_cocycle_dimension=five_cocycle_dimension,
        fifth_cohomology_dimension=five_cocycle_dimension - d4_rank,
        trace_nonzero_components=sum(value != 0 for value in trace_five),
        trace_norm_squared=trace_norm_squared,
        augmented_d4_trace_rank=augmented_rank,
        dual_separating_pairing=dual_pairing,
        differential_squares_to_zero=(d5 * d4 == sp.zeros(d5.rows, d4.cols)),
        trace_is_closed=(d5 * trace_five == sp.zeros(d5.rows, 1)),
        trace_is_exact=(augmented_rank == d4_rank),
        trace_annihilates_coboundaries=trace_annihilates,
    )


def glued_filling_period(first_integral: Any, second_integral: Any) -> sp.Expr:
    """Return the oriented closed-cycle integral ``I(B)-I(B')``.

    This is a gluing identity, not a claim that the period is nonzero,
    integral, or normalized to a particular value.
    """

    return sp.simplify(sp.sympify(first_integral) - sp.sympify(second_integral))


def extension_phase_ratio(
    coefficient: Any,
    first_integral: Any,
    second_integral: Any,
) -> sp.Expr:
    """Return the phase ratio between two declared extension integrals."""

    return sp.simplify(
        sp.exp(
            sp.I
            * sp.sympify(coefficient)
            * glued_filling_period(first_integral, second_integral)
        )
    )
