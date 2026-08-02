from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.scale_constraints import (
    diagnose_log_constraints,
    generalized_least_squares,
    intersect_closed_intervals,
    positive_monomial_log_system,
    shift_log_references,
)


def test_od_v1_null_direction_mixes_scale_and_every_nuisance() -> None:
    matrix = sp.Matrix(
        [
            [1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
        ]
    )
    result = diagnose_log_constraints(
        matrix,
        [0, 0, 0, 0],
        provenance=("S5", "G5", "M1", "CF4"),
    )
    assert result.nullspace == (sp.ImmutableMatrix([-1, 1, 1, 1, 1]),)
    assert result.coordinate_identifiable == (False, False, False, False, False)
    assert result.linear.underdetermined


def test_coordinate_can_be_identified_without_unique_or_tall_system() -> None:
    result = diagnose_log_constraints(
        [[1, 0, 0], [0, 1, 0]],
        [2, 3],
        provenance=("first", "second"),
    )
    assert result.coordinate_identifiable == (True, True, False)
    assert not result.linear.unique
    assert not result.linear.overdetermined_by_count


def test_left_null_and_incremental_ledgers_separate_duplicate_from_conflict() -> None:
    agreeing = diagnose_log_constraints(
        [[1, -2], [2, -4], [0, 1]],
        [3, 6, 4],
        provenance=("original", "rescaled", "new-direction"),
    )
    assert agreeing.coefficient_ranks_by_row == (1, 1, 2)
    assert agreeing.augmented_ranks_by_row == (1, 1, 2)
    assert agreeing.coefficient_informative_rows == (True, False, True)
    assert agreeing.augmented_informative_rows == (True, False, True)
    assert agreeing.compatibility_residuals == (0,)
    assert agreeing.linear.consistent

    conflicting = diagnose_log_constraints(
        [[1, -2], [2, -4], [0, 1]],
        [3, 7, 4],
        provenance=("original", "conflicting-rescale", "new-direction"),
    )
    assert conflicting.coefficient_ranks_by_row == (1, 1, 2)
    assert conflicting.augmented_ranks_by_row == (1, 2, 3)
    assert conflicting.coefficient_informative_rows == (True, False, True)
    assert conflicting.augmented_informative_rows == (True, True, True)
    assert conflicting.compatibility_residuals != (0,)
    assert not conflicting.linear.consistent
    assert conflicting.coordinate_identifiable is None


def test_as4_rows_supply_two_directions_and_two_compatibility_tests() -> None:
    k = sp.symbols("k", nonzero=True, real=True)
    matrix = [[2, 0], [-4, 0], [-1, k], [-2, 2 * k]]
    rhs = sp.Matrix(sp.symbols("g r h s", real=True))
    result = diagnose_log_constraints(
        matrix,
        rhs,
        provenance=("gravity", "medium", "hadronic", "confinement"),
    )
    assert result.linear.coefficient_rank == 2
    assert result.linear.coefficient_row_dependencies == 2
    assert result.coefficient_informative_rows == (True, False, True, False)
    assert set(result.compatibility_residuals) == {2 * rhs[0] + rhs[1], -2 * rhs[2] + rhs[3]}


def test_as4_free_length_guard_does_not_reopen_nullity() -> None:
    k = sp.symbols("k", nonzero=True, real=True)
    result = diagnose_log_constraints(
        [[2, 0, 0], [-4, 0, 0], [-1, k, 1], [-2, 2 * k, 1]],
        [0, 0, 0, 0],
        provenance=("gravity", "medium", "hadronic", "confinement"),
    )
    assert result.linear.coefficient_rank == 3
    assert result.linear.solution_dimension == 0
    assert result.nullspace == ()
    assert result.coordinate_identifiable == (True, True, True)


def test_positive_monomial_conversion_requires_positive_dimensionless_ratios() -> None:
    y1, y2, c1, c2 = sp.symbols("y1 y2 c1 c2", positive=True)
    result = positive_monomial_log_system(
        [[2], [-1]],
        [y1, y2],
        [c1, c2],
        provenance=("row-a", "row-b"),
    )
    assert result.rhs == sp.ImmutableMatrix([sp.log(y1 / c1), sp.log(y2 / c2)])
    with pytest.raises(ValueError, match="declared positive"):
        positive_monomial_log_system(
            [[1]], [sp.Symbol("unknown_sign")], [1], provenance=("row",)
        )


def test_reference_shift_preserves_compatibility_residuals() -> None:
    system = diagnose_log_constraints(
        [[1], [2]], [3, 6], provenance=("one", "two")
    )
    shifted = shift_log_references(system, [sp.Rational(5, 2)])
    assert shifted.rhs == sp.ImmutableMatrix([sp.Rational(1, 2), 1])
    assert shifted.compatibility_residuals == system.compatibility_residuals == (0,)
    assert shifted.coordinate_identifiable == system.coordinate_identifiable == (True,)


def test_exact_gls_satisfies_normal_equations_and_declared_covariance() -> None:
    result = generalized_least_squares(
        [[1], [1]],
        [1, 3],
        sp.eye(2),
        provenance=("first", "second"),
        covariance_provenance="identity test covariance",
    )
    assert result.estimator == sp.ImmutableMatrix([2])
    assert result.residual == sp.ImmutableMatrix([-1, 1])
    assert result.normal_residual == sp.zeros(1, 1)
    assert result.chi_squared == 2
    assert result.degrees_of_freedom == 1
    assert result.residual_projector * result.rhs == result.residual
    assert result.residual_projector**2 == result.residual_projector
    assert result.residual_projector * result.design == sp.zeros(2, 1)
    assert result.provenance == ("first", "second")


def test_shared_covariance_changes_residual_weight_without_changing_row_rank() -> None:
    rho = sp.Rational(1, 2)
    covariance = sp.Matrix([[1, rho], [rho, 1]])
    result = generalized_least_squares(
        [[1], [1]],
        [1, 3],
        covariance,
        provenance=("first", "second"),
        covariance_provenance="shared test covariance",
    )
    assert result.estimator == sp.ImmutableMatrix([2])
    assert result.chi_squared == 4
    assert result.degrees_of_freedom == 1
    assert result.design.rank() == 1


@pytest.mark.parametrize(
    ("covariance", "message"),
    [
        ([[1, 2], [0, 1]], "symmetric"),
        ([[1, 1], [1, 1]], "positive definite"),
        ([[1, 2], [2, 1]], "positive definite"),
    ],
)
def test_gls_rejects_invalid_covariance(covariance, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        generalized_least_squares(
            [[1], [1]],
            [1, 2],
            covariance,
            provenance=("first", "second"),
            covariance_provenance="invalid test covariance",
        )


def test_gls_rejects_rank_deficient_parameterization() -> None:
    with pytest.raises(ValueError, match="full column rank"):
        generalized_least_squares(
            [[1, 1], [2, 2]],
            [1, 2],
            sp.eye(2),
            provenance=("first", "second"),
            covariance_provenance="identity test covariance",
        )


def test_exact_interval_intersection_separates_range_point_and_conflict() -> None:
    overlap = intersect_closed_intervals(
        [(0, 3), (1, 4), (sp.Rational(1, 2), 2)],
        provenance=("one", "two", "three"),
    )
    assert (overlap.lower, overlap.upper) == (1, 2)
    assert overlap.feasible and not overlap.point_identified and not overlap.contradiction
    assert overlap.active_lower_indices == (1,)
    assert overlap.active_upper_indices == (2,)

    point = intersect_closed_intervals(
        [(0, 1), (1, 2)], provenance=("one", "two")
    )
    assert point.feasible and point.point_identified and not point.contradiction
    assert (point.lower, point.upper) == (1, 1)

    conflict = intersect_closed_intervals(
        [(0, 1), (2, 3)], provenance=("one", "two")
    )
    assert not conflict.feasible and not conflict.point_identified and conflict.contradiction


def test_interval_guards_reject_malformed_or_undecidable_inputs() -> None:
    with pytest.raises(ValueError, match="at least one"):
        intersect_closed_intervals([], provenance=())
    with pytest.raises(ValueError, match="lower <= upper"):
        intersect_closed_intervals([(2, 1)], provenance=("bad",))
    with pytest.raises(ValueError, match="exactly decidable"):
        intersect_closed_intervals(
            [(0, sp.Symbol("upper", real=True))], provenance=("undecidable",)
        )


def test_exact_apis_reject_floating_inputs_and_missing_provenance() -> None:
    with pytest.raises(ValueError, match="exact real values"):
        diagnose_log_constraints([[1.0]], [2], provenance=("float",))
    with pytest.raises(ValueError, match="floating inputs"):
        generalized_least_squares(
            [[1], [1]],
            [1, 2],
            [[1.0, 0], [0, 1]],
            provenance=("one", "two"),
            covariance_provenance="float covariance",
        )
    with pytest.raises(ValueError, match="non-empty"):
        generalized_least_squares(
            [[1], [1]],
            [1, 2],
            sp.eye(2),
            provenance=("one", "two"),
            covariance_provenance="",
        )
    with pytest.raises(ValueError, match="name every"):
        intersect_closed_intervals([(0, 1), (0, 2)], provenance=("one",))
    with pytest.raises(ValueError, match="provably real"):
        diagnose_log_constraints(
            [[sp.Symbol("unknown_domain")]], [2], provenance=("unknown",)
        )


def test_row_provenance_and_shapes_are_mandatory() -> None:
    with pytest.raises(ValueError, match="name every"):
        diagnose_log_constraints([[1], [2]], [1, 2], provenance=("only-one",))
    with pytest.raises(ValueError, match="non-empty"):
        diagnose_log_constraints([[1]], [1], provenance=("",))
    with pytest.raises(ValueError, match="rhs"):
        diagnose_log_constraints([[1], [2]], [1], provenance=("one", "two"))
