#!/usr/bin/env python3
"""Exact linear-system diagnostic and EL5 scope verifier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.linear_systems import diagnose_linear_system
from substrate_framework.verification import CheckLedger


EL5_SHA256 = "5684f2aba979501c81dc12c1afcc51c29cbeb7eb676678b76208cfcd23f01d1f"


@dataclass(frozen=True)
class DuplicateCandidate:
    row_multiplier: int
    rhs_delta: int


def candidate_is_exact_duplicate_consistency(candidate: DuplicateCandidate) -> bool:
    first_row = sp.Matrix([[1, -2]])
    second_row = candidate.row_multiplier * first_row
    matrix = first_row.col_join(second_row)
    result = diagnose_linear_system(matrix, [3, 3 + candidate.rhs_delta])
    return matrix.row(0) == matrix.row(1) and result.consistent


def run(source_file: Path) -> int:
    checks = CheckLedger("C-LIN-001")
    checks.check(
        "the audited EL5 source is the hash-pinned candidate unit",
        hashlib.sha256(source_file.read_bytes()).hexdigest() == EL5_SHA256,
    )

    unique = diagnose_linear_system([[1, 0], [0, 1]], [2, 3])
    checks.check(
        "a full-column-rank consistent system is unique",
        unique.consistent
        and unique.unique
        and unique.solution_dimension == 0,
    )
    underdetermined = diagnose_linear_system([[1, 1, 0]], [2])
    checks.check(
        "a consistent rank-deficient system is underdetermined",
        underdetermined.consistent
        and underdetermined.underdetermined
        and underdetermined.solution_dimension == 2,
    )
    inconsistent = diagnose_linear_system([[1, 0], [1, 0]], [1, 2])
    checks.check(
        "augmented rank above coefficient rank means inconsistent",
        not inconsistent.consistent
        and inconsistent.coefficient_rank == 1
        and inconsistent.augmented_rank == 2
        and inconsistent.solution_dimension is None,
    )

    tall_matrix = [[1, 0], [0, 1], [1, 1]]
    tall_consistent = diagnose_linear_system(tall_matrix, [2, 3, 5])
    tall_inconsistent = diagnose_linear_system(tall_matrix, [2, 3, 6])
    checks.check(
        "more equations than unknowns can still give a unique consistent system",
        tall_consistent.overdetermined_by_count
        and tall_consistent.unique
        and tall_consistent.consistent,
    )
    checks.check(
        "the same coefficient matrix can instead be inconsistent",
        tall_inconsistent.overdetermined_by_count
        and not tall_inconsistent.consistent
        and tall_consistent.coefficient_rank == tall_inconsistent.coefficient_rank,
    )

    agreeing = diagnose_linear_system([[1, -2], [1, -2]], [3, 3])
    disagreeing = diagnose_linear_system([[1, -2], [1, -2]], [3, 4])
    checks.check(
        "an exact duplicate row with equal right-hand sides is redundant and consistent",
        agreeing.consistent
        and agreeing.coefficient_rank == agreeing.augmented_rank == 1
        and agreeing.coefficient_row_dependencies == 1,
    )
    checks.check(
        "an exact duplicate row with unequal right-hand sides is inconsistent",
        not disagreeing.consistent
        and disagreeing.coefficient_rank == 1
        and disagreeing.augmented_rank == 2,
    )
    checks.mutation_sensitive(
        "duplicate-row identity and right-hand-side agreement",
        candidate_is_exact_duplicate_consistency,
        DuplicateCandidate(1, 0),
        [
            DuplicateCandidate(2, 0),
            DuplicateCandidate(1, 1),
            DuplicateCandidate(-1, 0),
        ],
    )

    coefficient = sp.symbols("b0", positive=True)
    slope = 8 * sp.pi**2 / coefficient
    rows = [
        [2, 0],
        [-4, 0],
        [-1, -slope],
        [-2, -2 * slope],
    ]
    with_duplicate = rows + [[-1, -slope]]
    source_four = diagnose_linear_system(rows, [0, 0, 0, 0])
    source_five = diagnose_linear_system(with_duplicate, [0, 0, 0, 0, 0])
    checks.check(
        "EL5's added coefficient row preserves rank, nullity, and uniqueness for consistent offsets",
        source_four.coefficient_rank == source_five.coefficient_rank == 2
        and source_four.solution_dimension == source_five.solution_dimension == 0
        and source_four.unique
        and source_five.unique,
    )
    checks.check(
        "the added source row increases coefficient dependencies rather than unknowns",
        source_four.coefficient_row_dependencies == 2
        and source_five.coefficient_row_dependencies == 3
        and source_four.unknowns == source_five.unknowns == 2,
    )

    restored = [
        [2, 0, 0],
        [-4, 0, 0],
        [-1, -slope, 0],
        [-2, -2 * slope, 0],
        [-1, -slope, 1],
    ]
    restored_status = diagnose_linear_system(restored, [0, 0, 0, 0, 0])
    checks.check(
        "EL5's actual restored-electron matrix has no reopened null direction",
        restored_status.coefficient_rank == 3
        and restored_status.solution_dimension == 0
        and restored_status.unique
        and not restored_status.underdetermined,
    )
    odv1 = [
        [1, 1, 0, 0, 0],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
    ]
    odv1_status = diagnose_linear_system(odv1, [0, 0, 0, 0])
    checks.check(
        "the separate OD-v1-shaped matrix is underdetermined",
        odv1_status.coefficient_rank == 4
        and odv1_status.solution_dimension == 1
        and odv1_status.underdetermined,
    )
    checks.check(
        "the restored-electron and OD-v1 controls are logically different systems",
        restored_status.equations == 5
        and restored_status.unknowns == 3
        and odv1_status.equations == 4
        and odv1_status.unknowns == 5,
    )

    shape, hadronic_offset, mass_hadronic, mass_electron = sp.symbols(
        "b kappa_h m_had m_e", positive=True
    )
    ratio = 48 * sp.pi**3 * shape / hadronic_offset
    checks.check(
        "EL5's conditional ratio is exact algebra but retains both source inputs",
        sp.diff(ratio, shape) != 0
        and sp.diff(ratio, hadronic_offset) != 0
        and {shape, hadronic_offset} <= ratio.free_symbols,
    )
    desired_ratio = sp.symbols("R", positive=True)
    selected_offset = sp.solve(sp.Eq(ratio, desired_ratio), hadronic_offset)[0]
    checks.check(
        "an unpinned hadronic offset can reproduce any positive mass ratio",
        selected_offset == 48 * sp.pi**3 * shape / desired_ratio,
    )
    checks.check(
        "the mass relation is conditional rather than a free-parameter-free prediction",
        sp.solve(
            sp.Eq(mass_hadronic / mass_electron, ratio),
            mass_hadronic,
        )[0]
        == 48 * sp.pi**3 * mass_electron * shape / hadronic_offset,
    )

    total = checks.finish()
    print(f"P022 EL5 EXACT AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
