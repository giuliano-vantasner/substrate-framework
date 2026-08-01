from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.linear_systems import diagnose_linear_system


def test_unique_square_system() -> None:
    result = diagnose_linear_system([[1, 0], [0, 1]], [2, 3])
    assert result.consistent
    assert result.unique
    assert not result.underdetermined
    assert result.solution_dimension == 0
    assert not result.overdetermined_by_count


def test_tall_system_count_does_not_decide_consistency() -> None:
    coefficients = [[1, 0], [0, 1], [1, 1]]
    consistent = diagnose_linear_system(coefficients, [2, 3, 5])
    inconsistent = diagnose_linear_system(coefficients, [2, 3, 6])
    assert consistent.overdetermined_by_count and consistent.unique
    assert inconsistent.overdetermined_by_count and not inconsistent.consistent
    assert inconsistent.solution_dimension is None


def test_underdetermined_system_has_positive_solution_dimension() -> None:
    result = diagnose_linear_system([[1, 1, 0], [0, 0, 1]], [2, 3])
    assert result.consistent
    assert result.underdetermined
    assert not result.unique
    assert result.solution_dimension == 1


def test_duplicate_row_consistency_depends_on_rhs() -> None:
    row = [[1, -2], [1, -2]]
    agreeing = diagnose_linear_system(row, [3, 3])
    disagreeing = diagnose_linear_system(row, [3, 4])
    assert agreeing.consistent and agreeing.underdetermined
    assert agreeing.coefficient_rank == agreeing.augmented_rank == 1
    assert agreeing.coefficient_row_dependencies == 1
    assert not disagreeing.consistent
    assert disagreeing.coefficient_rank == 1
    assert disagreeing.augmented_rank == 2


@pytest.mark.parametrize(
    ("coefficients", "rhs", "message"),
    [
        ([], [], "coefficients"),
        ([[]], [[]], "coefficients"),
        ([[1, 2]], [1, 2], "rhs"),
        ([[1], [2]], [[1, 2], [3, 4]], "rhs"),
    ],
)
def test_invalid_shapes_are_rejected(coefficients, rhs, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        diagnose_linear_system(coefficients, rhs)


def test_symbolic_exact_rank_is_retained() -> None:
    slope = sp.symbols("k", nonzero=True)
    result = diagnose_linear_system(
        [[-1, slope], [-1, slope]],
        [sp.Symbol("r"), sp.Symbol("r")],
    )
    assert result.coefficient_rank == 1
    assert result.augmented_rank == 1
