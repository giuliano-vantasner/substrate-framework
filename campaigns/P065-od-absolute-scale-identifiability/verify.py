"""Primary exact verifier for P065 scale-constraint claims and OD audit."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.scale_constraints import (
    diagnose_log_constraints,
    generalized_least_squares,
    intersect_closed_intervals,
    positive_monomial_log_system,
    shift_log_references,
)
from substrate_framework.verification import CheckLedger

OD_SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-19/"
    "bridge_OD_over_determination_test.py"
)
OD_SHA256 = "300259218ca36063625d42487dc1d8f00def4b5d58ef6ffc0b4dc174852fdeb6"
AS4_SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-21/"
    "bridge_AS4_over_determination_v2.py"
)
AS4_SHA256 = "cdcfea3ac26c932a3db792c864baa026c761555d3c0e34c7b1bc025ea962745f"


def _zero(value: object) -> bool:
    return sp.simplify(sp.sympify(value)) == 0


def main() -> int:
    ledger = CheckLedger("P065")
    ledger.check("hash-pinned OD source exists", OD_SOURCE.is_file())
    ledger.check(
        "hash-pinned OD source integrity",
        hashlib.sha256(OD_SOURCE.read_bytes()).hexdigest() == OD_SHA256,
    )
    ledger.check("hash-pinned AS4 source exists", AS4_SOURCE.is_file())
    ledger.check(
        "hash-pinned AS4 source integrity",
        hashlib.sha256(AS4_SOURCE.read_bytes()).hexdigest() == AS4_SHA256,
    )
    od_text = OD_SOURCE.read_text(encoding="utf-8")
    as4_text = AS4_SOURCE.read_text(encoding="utf-8")
    ledger.check(
        "OD physical independence is assigned rather than derived",
        "G5_S5_independent = True" in od_text,
    )
    ledger.check(
        "AS4 free-length guard asserts zero nullity despite underdetermined prose",
        "nullity_fab == 0" in as4_text
        and "extra free length re-opens a null direction" in as4_text,
    )

    od_matrix = sp.Matrix(
        [
            [1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
        ]
    )
    od = diagnose_log_constraints(
        od_matrix,
        [0, 0, 0, 0],
        provenance=("S5", "G5", "M1", "CF4"),
    )
    ledger.check(
        "OD exact null vector mixes scale with every nuisance coordinate",
        od.nullspace == (sp.ImmutableMatrix([-1, 1, 1, 1, 1]),)
        and od_matrix * od.nullspace[0] == sp.zeros(4, 1),
    )
    ledger.check(
        "OD identifies none of its five declared coordinates",
        od.coordinate_identifiable == (False, False, False, False, False)
        and od.linear.solution_dimension == 1,
    )
    partial = diagnose_log_constraints(
        [[1, 0, 0], [0, 1, 0]],
        [2, 3],
        provenance=("coordinate-zero", "coordinate-one"),
    )
    ledger.check(
        "coordinate identifiability is distinct from global uniqueness and row count",
        partial.coordinate_identifiable == (True, True, False)
        and partial.linear.underdetermined
        and not partial.linear.overdetermined_by_count,
    )
    ledger.mutation_sensitive(
        "target identification binds every coefficient-null component",
        lambda matrix: diagnose_log_constraints(
            matrix, [0, 0], provenance=("one", "two")
        ).coordinate_identifiable[0],
        [[1, 0, 0], [0, 1, 0]],
        [
            [[0, 1, 0], [0, 0, 1]],
            [[1, 1, 0], [2, 2, 0]],
        ],
    )

    duplicate = diagnose_log_constraints(
        [[1, -2], [2, -4], [0, 1]],
        [3, 6, 4],
        provenance=("original", "rescale", "new-direction"),
    )
    ledger.check(
        "incremental ledger refuses a consistent rescaled row as new coefficient information",
        duplicate.coefficient_ranks_by_row == (1, 1, 2)
        and duplicate.coefficient_informative_rows == (True, False, True)
        and duplicate.augmented_ranks_by_row == (1, 1, 2)
        and duplicate.compatibility_residuals == (0,),
    )
    conflicting = diagnose_log_constraints(
        [[1, -2], [2, -4], [0, 1]],
        [3, 7, 4],
        provenance=("original", "conflict", "new-direction"),
    )
    ledger.check(
        "dependent conflicting row adds augmented inconsistency but no coefficient direction",
        conflicting.coefficient_informative_rows == (True, False, True)
        and conflicting.augmented_informative_rows == (True, True, True)
        and not conflicting.linear.consistent
        and conflicting.coordinate_identifiable is None,
    )
    ledger.mutation_sensitive(
        "left-null compatibility binds the dependent right-hand side",
        lambda second_rhs: diagnose_log_constraints(
            [[1, -2], [2, -4]],
            [3, second_rhs],
            provenance=("original", "rescale"),
        ).linear.consistent,
        6,
        [5, 7, -6],
    )

    k = sp.Symbol("k", nonzero=True, real=True)
    g, r, h, s = sp.symbols("g r h s", real=True)
    as4 = diagnose_log_constraints(
        [[2, 0], [-4, 0], [-1, k], [-2, 2 * k]],
        [g, r, h, s],
        provenance=("gravity", "medium", "hadronic", "confinement"),
    )
    ledger.check(
        "AS4 supplies two coefficient directions and two compatibility tests",
        as4.linear.coefficient_rank == 2
        and as4.linear.coefficient_row_dependencies == 2
        and as4.coefficient_informative_rows == (True, False, True, False)
        and set(as4.compatibility_residuals) == {2 * g + r, -2 * h + s},
    )
    as4_consistent = diagnose_log_constraints(
        as4.design,
        [g, -2 * g, h, 2 * h],
        provenance=as4.provenance,
    )
    ledger.check(
        "AS4 compatibility requires both redundant observable relations",
        as4_consistent.linear.consistent
        and as4_consistent.coordinate_identifiable == (True, True)
        and as4_consistent.compatibility_residuals == (0, 0),
    )
    source_guard = diagnose_log_constraints(
        [[2, 0, 0], [-4, 0, 0], [-1, k, 1], [-2, 2 * k, 1]],
        [0, 0, 0, 0],
        provenance=as4.provenance,
    )
    actual_free_direction = diagnose_log_constraints(
        [[2, 0, 0], [-4, 0, 0], [-1, k, 1], [-2, 2 * k, 2]],
        [0, 0, 0, 0],
        provenance=as4.provenance,
    )
    ledger.check(
        "AS4 source guard pins its extra coordinate instead of reopening nullity",
        source_guard.linear.unique
        and source_guard.coordinate_identifiable == (True, True, True)
        and actual_free_direction.linear.solution_dimension == 1,
    )

    y1, y2, c1, c2 = sp.symbols("y1 y2 c1 c2", positive=True)
    monomial = positive_monomial_log_system(
        [[2], [-1]],
        [y1, y2],
        [c1, c2],
        provenance=("positive-row-one", "positive-row-two"),
    )
    ledger.check(
        "positive monomial ratios map to an exact logarithmic right-hand side",
        monomial.rhs
        == sp.ImmutableMatrix([sp.log(y1 / c1), sp.log(y2 / c2)]),
    )
    positivity_refused = False
    try:
        positive_monomial_log_system(
            [[1]], [sp.Symbol("unsigned")], [1], provenance=("unsigned",)
        )
    except ValueError:
        positivity_refused = True
    ledger.check("log conversion refuses an undeclared sign", positivity_refused)

    reference_system = diagnose_log_constraints(
        [[1], [2]], [3, 6], provenance=("row-one", "row-two")
    )
    shifted = shift_log_references(reference_system, [sp.Rational(5, 2)])
    ledger.check(
        "log-reference shift preserves compatibility and identifiability",
        shifted.rhs == sp.ImmutableMatrix([sp.Rational(1, 2), 1])
        and shifted.compatibility_residuals == reference_system.compatibility_residuals
        and shifted.coordinate_identifiable == reference_system.coordinate_identifiable,
    )

    gls = generalized_least_squares(
        [[1], [1]],
        [1, 3],
        sp.eye(2),
        provenance=("observation-one", "observation-two"),
        covariance_provenance="exact identity demonstration covariance",
    )
    ledger.check(
        "exact GLS estimator closes its normal equations",
        gls.estimator == sp.ImmutableMatrix([2])
        and gls.residual == sp.ImmutableMatrix([-1, 1])
        and gls.normal_residual == sp.zeros(1, 1)
        and gls.residual_projector * gls.rhs == gls.residual,
    )
    ledger.check(
        "exact GLS retains chi-square and residual degrees of freedom",
        gls.chi_squared == 2 and gls.degrees_of_freedom == 1,
    )
    shared = generalized_least_squares(
        [[1], [1]],
        [1, 3],
        [[1, sp.Rational(1, 2)], [sp.Rational(1, 2), 1]],
        provenance=("observation-one", "observation-two"),
        covariance_provenance="exact correlated demonstration covariance",
    )
    ledger.check(
        "declared shared covariance changes residual weight but not structural rank",
        shared.estimator == gls.estimator
        and shared.chi_squared == 4
        and shared.design.rank() == gls.design.rank() == 1,
    )
    ledger.mutation_sensitive(
        "GLS residual verdict binds the supplied covariance",
        lambda covariance: generalized_least_squares(
            [[1], [1]],
            [1, 3],
            covariance,
            provenance=("observation-one", "observation-two"),
            covariance_provenance="mutation covariance",
        ).chi_squared
        == 2,
        sp.eye(2),
        [
            sp.diag(2, 2),
            [[1, sp.Rational(1, 2)], [sp.Rational(1, 2), 1]],
        ],
    )
    covariance_guards = []
    for covariance in (
        [[1, 1], [1, 1]],
        [[1, 2], [0, 1]],
        [[1, 2], [2, 1]],
    ):
        try:
            generalized_least_squares(
                [[1], [1]],
                [1, 3],
                covariance,
                provenance=("observation-one", "observation-two"),
                covariance_provenance="invalid mutation covariance",
            )
        except ValueError:
            covariance_guards.append(True)
    ledger.check(
        "GLS refuses singular nonsymmetric and indefinite covariance",
        covariance_guards == [True, True, True],
    )

    overlap = intersect_closed_intervals(
        [(0, 3), (1, 4), (sp.Rational(1, 2), 2)],
        provenance=("interval-one", "interval-two", "interval-three"),
    )
    point = intersect_closed_intervals(
        [(0, 1), (1, 2)], provenance=("interval-one", "interval-two")
    )
    conflict = intersect_closed_intervals(
        [(0, 1), (2, 3)], provenance=("interval-one", "interval-two")
    )
    ledger.check(
        "closed intervals distinguish range point identification and contradiction",
        (overlap.lower, overlap.upper) == (1, 2)
        and overlap.feasible
        and not overlap.point_identified
        and point.point_identified
        and conflict.contradiction,
    )
    ledger.mutation_sensitive(
        "interval feasibility binds every supplied bound",
        lambda intervals: intersect_closed_intervals(
            intervals,
            provenance=tuple(f"mutation-{index}" for index in range(len(intervals))),
        ).feasible,
        [(0, 3), (1, 2)],
        [
            [(0, 1), (2, 3)],
            [(-2, -1), (0, 4)],
        ],
    )
    quadrature_aliases = ("np." + "trapz", "np." + "trapezoid")
    canonical_source = Path(
        "src/substrate_framework/scale_constraints.py"
    ).read_text(encoding="utf-8")
    ledger.check(
        "P065 exact algebra uses no NumPy quadrature alias",
        all(alias not in canonical_source for alias in quadrature_aliases),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
