"""Primary exact verifier for the P075 AS4 source adjudication."""

from __future__ import annotations

import sympy as sp

from substrate_framework.scale_constraints import (
    diagnose_log_constraints,
    generalized_least_squares,
)
from substrate_framework.verification import CheckLedger


PROVENANCE = ("gravity", "medium", "hadronic", "confinement")


def _zero(value: object) -> bool:
    return sp.simplify(sp.sympify(value)) == 0


def _source_pose_predicate(matrix: sp.Matrix, k: sp.Expr) -> bool:
    """Reproduce AS4.1's actual partial matrix predicate."""

    return bool(
        matrix.shape == (4, 2)
        and matrix[0, :] == sp.Matrix([[2, 0]])
        and matrix[2, 1] == k
        and matrix[3, 1] == 2 * k
    )


def _source_rank_predicate(matrix: sp.Matrix) -> bool:
    """Reproduce AS4.2's coefficient-only verdict."""

    rank = int(matrix.rank())
    return rank == matrix.cols and matrix.rows > matrix.cols and matrix.cols - rank == 0


def main() -> int:
    ledger = CheckLedger("P075")
    k = sp.Symbol("k", positive=True)
    g, r, h, s = sp.symbols("g r h s", real=True)
    design = sp.Matrix([[2, 0], [-4, 0], [-1, k], [-2, 2 * k]])
    rhs = sp.Matrix([g, r, h, s])

    generic = diagnose_log_constraints(design, rhs, provenance=PROVENANCE)
    ledger.check(
        "AS4 coefficient matrix has two directions and two row dependencies",
        generic.linear.equations == 4
        and generic.linear.unknowns == 2
        and generic.linear.coefficient_rank == 2
        and generic.linear.coefficient_row_dependencies == 2
        and generic.nullspace == (),
    )
    ledger.check(
        "only the gravity and hadronic rows add coefficient directions in source order",
        generic.coefficient_ranks_by_row == (1, 1, 2, 2)
        and generic.coefficient_informative_rows == (True, False, True, False),
    )
    ledger.check(
        "left-nullspace derives both compatibility relations",
        len(generic.left_nullspace) == 2
        and set(generic.compatibility_residuals) == {2 * g + r, -2 * h + s}
        and all(vector.T * design == sp.zeros(1, 2) for vector in generic.left_nullspace),
    )
    ledger.check(
        "generic symbolic right-hand sides make AS4 inconsistent rather than uniquely solved",
        generic.linear.augmented_rank == 3
        and not generic.linear.consistent
        and not generic.linear.unique
        and generic.linear.solution_dimension is None
        and generic.coordinate_identifiable is None,
    )

    compatible_rhs = sp.Matrix([g, -2 * g, h, 2 * h])
    compatible = diagnose_log_constraints(
        design, compatible_rhs, provenance=PROVENANCE
    )
    solution = sp.linsolve((design, compatible_rhs))
    ledger.check(
        "compatible supplied rows conditionally identify both coordinates",
        compatible.linear.coefficient_rank == compatible.linear.augmented_rank == 2
        and compatible.linear.unique
        and compatible.coordinate_identifiable == (True, True)
        and compatible.compatibility_residuals == (0, 0)
        and solution == {(g / 2, (g + 2 * h) / (2 * k))},
    )
    ledger.mutation_sensitive(
        "each dependent right-hand side is load-bearing for compatibility",
        lambda values: diagnose_log_constraints(
            design, values, provenance=PROVENANCE
        ).linear.consistent,
        compatible_rhs,
        [
            sp.Matrix([g, -2 * g + 1, h, 2 * h]),
            sp.Matrix([g, -2 * g, h, 2 * h + 1]),
            sp.Matrix([g, -2 * g - 1, h, 2 * h - 1]),
        ],
    )

    expected_residuals = {2 * g + r, -2 * h + s}

    def exact_as4_relations(candidate: object) -> bool:
        result = diagnose_log_constraints(candidate, rhs, provenance=PROVENANCE)
        return (
            result.linear.coefficient_rank == 2
            and set(result.compatibility_residuals) == expected_residuals
        )

    ledger.mutation_sensitive(
        "coefficient mutations change the advertised compatibility relations",
        exact_as4_relations,
        design,
        [
            sp.Matrix([[2, 0], [-3, 0], [-1, k], [-2, 2 * k]]),
            sp.Matrix([[2, 0], [-4, 0], [-3, k], [-2, 2 * k]]),
            sp.Matrix([[2, 0], [-4, 0], [-1, k], [-2, 3 * k]]),
        ],
    )

    pose_mutations = (
        sp.Matrix([[2, 0], [-3, 0], [-1, k], [-2, 2 * k]]),
        sp.Matrix([[2, 0], [-4, 0], [-7, k], [-2, 2 * k]]),
        sp.Matrix([[2, 0], [-4, 0], [-1, k], [9, 2 * k]]),
    )
    ledger.check(
        "AS4.1's source predicate is insensitive to three load-bearing x coefficients",
        _source_pose_predicate(design, k)
        and all(_source_pose_predicate(candidate, k) for candidate in pose_mutations),
    )
    ledger.check(
        "AS4.2's source verdict cannot distinguish compatible from incompatible right-hand sides",
        _source_rank_predicate(design)
        and compatible.linear.consistent
        and not generic.linear.consistent,
    )
    wrong_medium = 7 * g + h
    wrong_confinement = -3 * g + 5 * h
    ledger.check(
        "AS4.4's symbol-occurrence predicate accepts wrong prediction coefficients",
        wrong_medium.has(g)
        and wrong_confinement.has(h)
        and wrong_medium != -2 * g
        and wrong_confinement != 2 * h,
    )

    source_guard_design = sp.Matrix(
        [[2, 0, 0], [-4, 0, 0], [-1, k, 1], [-2, 2 * k, 1]]
    )
    source_guard = diagnose_log_constraints(
        source_guard_design, [0, 0, 0, 0], provenance=PROVENANCE
    )
    ledger.check(
        "AS4.G1's actual matrix pins its extra coordinate instead of reopening nullity",
        source_guard.linear.coefficient_rank == 3
        and source_guard.linear.solution_dimension == 0
        and source_guard.linear.unique
        and source_guard.coordinate_identifiable == (True, True, True),
    )
    reopened_design = source_guard_design.copy()
    reopened_design[3, 2] = 2
    reopened = diagnose_log_constraints(
        reopened_design, [0, 0, 0, 0], provenance=PROVENANCE
    )
    ledger.check(
        "a corrected proportional free-length row actually reopens one null direction",
        reopened.linear.coefficient_rank == 2
        and reopened.linear.solution_dimension == 1
        and len(reopened.nullspace) == 1
        and reopened_design * reopened.nullspace[0] == sp.zeros(4, 1),
    )

    correct_dimensions = sp.Matrix(
        [
            [0, 1, 0],
            [1, 2, -1],
            [0, 1, -1],
        ]
    )
    source_dimensions = sp.Matrix(
        [
            [1, 0, 0],
            [1, 2, -1],
            [0, 1, -1],
        ]
    )
    ledger.check(
        "correct M,L,T rows for a,hbar,c are full rank with no dimensionless monomial",
        correct_dimensions.det() == 1
        and correct_dimensions.rank() == 3
        and correct_dimensions.cols - correct_dimensions.rank() == 0,
    )
    ledger.check(
        "AS4.G2's rank-only predicate misses its wrong dimension row for a",
        source_dimensions[0, :] != correct_dimensions[0, :]
        and source_dimensions.rank() == correct_dimensions.rank() == 3,
    )

    nuisance_design = sp.Matrix(
        [
            [2, 0, -1, 0, 0],
            [-4, 0, 0, -1, 0],
            [-1, k, 0, 0, 0],
            [-2, 2 * k, 0, 0, -1],
        ]
    )
    nuisance = diagnose_log_constraints(
        nuisance_design,
        [0, 0, 0, 0],
        provenance=(
            "gravity with free log s_G",
            "medium with free log kappa_s",
            "hadronic",
            "confinement with free log c_CF4",
        ),
    )
    ledger.check(
        "restoring AS4's admitted residual coefficients reopens a scale-coupling null direction",
        nuisance.linear.coefficient_rank == 4
        and nuisance.linear.solution_dimension == 1
        and nuisance.coordinate_identifiable[:2] == (False, False)
        and len(nuisance.nullspace) == 1
        and nuisance_design * nuisance.nullspace[0] == sp.zeros(4, 1),
    )

    x = sp.Symbol("x", real=True)
    baseline, induced = sp.symbols("B S", positive=True)
    total_g = 1 / (baseline + induced * sp.exp(-2 * x))
    log_slope = sp.simplify(sp.diff(sp.log(total_g), x))
    ledger.check(
        "an allowed additive inverse-G baseline destroys AS4's constant gravity log row",
        _zero(log_slope.subs(baseline, 0) - 2)
        and not _zero(log_slope - 2)
        and _zero(log_slope - 2 * induced * sp.exp(-2 * x) / (baseline + induced * sp.exp(-2 * x))),
    )

    relabeled = diagnose_log_constraints(
        design,
        compatible_rhs,
        provenance=("fabricated-one", "fabricated-two", "fabricated-three", "fabricated-four"),
    )
    ledger.check(
        "unchanged algebra under fabricated labels proves provenance is an external obligation",
        relabeled.design == compatible.design
        and relabeled.rhs == compatible.rhs
        and relabeled.linear == compatible.linear
        and relabeled.provenance != compatible.provenance,
    )

    observations = sp.Matrix([2, -3, 3, 7])
    identity_gls = generalized_least_squares(
        design,
        observations,
        sp.eye(4),
        provenance=PROVENANCE,
        covariance_provenance="declared identity audit covariance",
    )
    scaled_gls = generalized_least_squares(
        design,
        observations,
        sp.diag(1, 4, 1, 9),
        provenance=PROVENANCE,
        covariance_provenance="declared unequal audit covariance",
    )
    ledger.check(
        "declared covariance supplies a residual ledger but not source independence",
        identity_gls.degrees_of_freedom == scaled_gls.degrees_of_freedom == 2
        and identity_gls.normal_residual == scaled_gls.normal_residual == sp.zeros(2, 1)
        and identity_gls.chi_squared > 0
        and scaled_gls.chi_squared > 0
        and identity_gls.chi_squared != scaled_gls.chi_squared,
    )
    ledger.check(
        "a compatible supplied observation vector has zero exact GLS residual",
        generalized_least_squares(
            design,
            [2, -4, 3, 6],
            sp.eye(4),
            provenance=PROVENANCE,
            covariance_provenance="declared identity compatibility covariance",
        ).chi_squared
        == 0,
    )

    a, beta2 = sp.symbols("a beta2", positive=True)
    fitted_symbol = sp.Symbol("a_from_observation", positive=True)
    ledger.check(
        "AS4.0's free-symbol introspection cannot detect a symbolic fitted input",
        all(item.is_number is not True for item in (a, beta2, sp.log(a), 1 / beta2))
        and fitted_symbol.is_number is not True,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
