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
