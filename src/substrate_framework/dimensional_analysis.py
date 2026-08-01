"""Exact linear-algebra helpers for Buckingham-style monomial groups."""

from __future__ import annotations

from typing import Any

import sympy as sp


def dimensionless_monomial_basis(dimension_matrix: Any) -> tuple[sp.Matrix, ...]:
    """Return a basis for exponent vectors with zero total dimensions.

    Rows are base dimensions and columns are primitive quantities.
    """

    matrix = sp.Matrix(dimension_matrix)
    return tuple(matrix.nullspace())


def dimensionless_group_count(dimension_matrix: Any) -> int:
    """Return ``number_of_primitives - rank`` for a dimension matrix."""

    matrix = sp.Matrix(dimension_matrix)
    return matrix.cols - matrix.rank()


def monomial_exponents(
    dimension_matrix: Any, target_dimension: Any
) -> sp.Matrix:
    """Return the unique primitive exponents for a target dimension.

    Rows of ``dimension_matrix`` are base dimensions and columns are primitive
    quantities. A unique representation requires full column rank and the
    target to lie in the column span. Dimensionless coefficients are outside
    this exponent calculation and remain unconstrained.
    """

    matrix = sp.Matrix(dimension_matrix)
    target = sp.Matrix(target_dimension)
    if matrix.rows == 0 or matrix.cols == 0:
        raise ValueError("dimension_matrix must be non-empty")
    if target.cols != 1 or target.rows != matrix.rows:
        raise ValueError("target_dimension must be a column matching matrix rows")
    if matrix.rank() < matrix.cols:
        raise ValueError("target monomial exponents are not unique")
    if matrix.row_join(target).rank() > matrix.rank():
        raise ValueError("target dimension is outside the primitive span")
    solution, parameters = matrix.gauss_jordan_solve(target)
    if parameters.rows:
        raise ValueError("target monomial exponents are not unique")
    return sp.Matrix(solution)
