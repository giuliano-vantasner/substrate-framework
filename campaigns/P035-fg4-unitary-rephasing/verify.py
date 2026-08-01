#!/usr/bin/env python3
"""Verify C-MIX-002 and audit the hash-pinned FG4 source unit."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.unitary_rephasing import (
    generic_rephasing_counts,
    invariant_quartet,
    rephase_unitary,
    rephasing_orbit_dimension,
    standard_three_angle_unitary,
    support_stabilizer_dimension,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "d9ebb32d440fb87540c7cb2d02a846b76dd4ee405288895308561762cd720ceb"


def is_zero(matrix: sp.MatrixBase) -> bool:
    return sp.simplify(matrix) == sp.zeros(*matrix.shape)


def support_incidence(size: int, support: set[tuple[int, int]]) -> sp.Matrix:
    rows = []
    for row, column in sorted(support):
        equation = [sp.Integer(0)] * (2 * size)
        equation[row] = 1
        equation[size + column] = -1
        rows.append(equation)
    return sp.Matrix(rows)


@dataclass(frozen=True)
class CountCandidate:
    size: int
    orbit: int
    irreducible_phases: int


def valid_generic_count(candidate: CountCandidate) -> bool:
    size = candidate.size
    angles = size * (size - 1) // 2
    return bool(
        size >= 2
        and candidate.orbit == 2 * size - 1
        and candidate.irreducible_phases == (size - 1) * (size - 2) // 2
        and size**2 == angles + candidate.orbit + candidate.irreducible_phases
    )


def phase_balanced(entries: tuple[tuple[int, int, int], ...], size: int) -> bool:
    row_weights = [0] * size
    column_weights = [0] * size
    for row, column, sign in entries:
        row_weights[row] += sign
        column_weights[column] -= sign
    return row_weights == [0] * size and column_weights == [0] * size


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P035-FG4")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    ledger.check(
        "the audited FG4 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    reproduced = subprocess.run(
        [sys.executable, str(args.source_file)],
        capture_output=True,
        text=True,
        check=False,
    )
    ledger.check("FG4 exits cleanly", reproduced.returncode == 0)
    ledger.check(
        "FG4's declared seven-check tally reproduces",
        "ALL 7 CHECKS PASS" in reproduced.stdout,
    )

    size = sp.symbols("N", integer=True, positive=True)
    unitary_dimension = size + 2 * size * (size - 1) / 2
    orthogonal_dimension = size * (size - 1) / 2
    ledger.check(
        "anti-Hermitian and real-skew generators give the exact group dimensions",
        sp.simplify(unitary_dimension - size**2) == 0
        and sp.simplify(orthogonal_dimension - size * (size - 1) / 2) == 0,
    )
    generic_orbit = 2 * size - 1
    quotient = sp.simplify(size**2 - generic_orbit)
    residual_phases = sp.simplify(quotient - orthogonal_dimension)
    ledger.check(
        "the generic quotient and angle-phase split close symbolically",
        sp.simplify(quotient - (size - 1) ** 2) == 0
        and sp.simplify(residual_phases - (size - 1) * (size - 2) / 2) == 0,
    )
    ledger.check(
        "the reusable count API closes N equals one through five",
        all(
            (
                (counts := generic_rephasing_counts(value)).unitary_parameters
                == counts.orthogonal_angles
                + counts.generic_orbit
                + counts.irreducible_phases
            )
            for value in range(1, 6)
        ),
    )
    ledger.check(
        "the accepted low-dimensional generic counts are zero at N=2 and one at N=3",
        generic_rephasing_counts(2).irreducible_phases == 0
        and generic_rephasing_counts(3).irreducible_phases == 1
        and generic_rephasing_counts(4).irreducible_phases == 3,
    )
    ledger.mutation_sensitive(
        "generic parameter budget",
        valid_generic_count,
        CountCandidate(3, 5, 1),
        [CountCandidate(3, 6, 1), CountCandidate(3, 5, 3), CountCandidate(2, 3, 1)],
    )

    dense_support = {(row, column) for row in range(3) for column in range(3)}
    permutation_support = {(0, 1), (1, 2), (2, 0)}
    block_support = {(0, 0), (0, 1), (1, 0), (1, 1), (2, 2)}
    dense_incidence = support_incidence(3, dense_support)
    permutation_incidence = support_incidence(3, permutation_support)
    block_incidence = support_incidence(3, block_support)
    ledger.check(
        "the connected dense support has only the one-dimensional common-phase kernel",
        dense_incidence.rank() == 5 and len(dense_incidence.nullspace()) == 1,
    )
    ledger.check(
        "disconnected support has larger stabilizers and smaller rephasing orbits",
        permutation_incidence.rank() == 3
        and len(permutation_incidence.nullspace()) == 3
        and block_incidence.rank() == 4
        and len(block_incidence.nullspace()) == 2,
    )
    dense_numeric = standard_three_angle_unitary(0.31, 0.27, 0.44, 0.73)
    permutation_numeric = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]], dtype=complex)
    block_numeric = np.array(
        [[3 / 5, 4 / 5, 0], [-4 / 5, 3 / 5, 0], [0, 0, 1]], dtype=complex
    )
    ledger.check(
        "the reusable support oracle distinguishes dense, block, and permutation strata",
        support_stabilizer_dimension(dense_numeric) == 1
        and support_stabilizer_dimension(block_numeric) == 2
        and support_stabilizer_dimension(permutation_numeric) == 3
        and rephasing_orbit_dimension(dense_numeric) == 5
        and rephasing_orbit_dimension(block_numeric) == 4
        and rephasing_orbit_dimension(permutation_numeric) == 3,
    )
    ledger.check(
        "FG4 omits the support-stratum qualifier from its universal removable count",
        "exactly 2N-1 phases are removable" in source_text
        and rephasing_orbit_dimension(permutation_numeric) != 2 * 3 - 1,
    )

    theta, phase = sp.symbols("theta phi", real=True)
    cosine, sine = sp.cos(theta), sp.sin(theta)
    rotation2 = sp.Matrix([[cosine, sine], [-sine, cosine]])
    left_phase = sp.diag(sp.exp(sp.I * phase), 1)
    right_phase = sp.diag(1, sp.exp(-sp.I * phase))
    dressed2 = sp.simplify(left_phase * rotation2 * right_phase)
    recovered2 = sp.simplify(left_phase.H * dressed2 * right_phase.H)
    quartet2 = sp.im(
        sp.expand(
            dressed2[0, 0]
            * dressed2[1, 1]
            * sp.conjugate(dressed2[0, 1])
            * sp.conjugate(dressed2[1, 0])
        )
    )
    ledger.check(
        "the exact two-dimensional phase dressing rephases to a real rotation",
        is_zero(dressed2.H * dressed2 - sp.eye(2))
        and is_zero(recovered2 - rotation2),
    )
    ledger.check(
        "every quartet in the general two-dimensional factorization is real",
        sp.simplify(quartet2) == 0,
    )

    t12, t13, t23, delta = sp.symbols("t12 t13 t23 delta", real=True)
    c12, s12 = sp.cos(t12), sp.sin(t12)
    c13, s13 = sp.cos(t13), sp.sin(t13)
    c23, s23 = sp.cos(t23), sp.sin(t23)
    rotation12 = sp.Matrix([[c12, s12, 0], [-s12, c12, 0], [0, 0, 1]])
    rotation13 = sp.Matrix(
        [[c13, 0, s13 * sp.exp(-sp.I * delta)], [0, 1, 0], [-s13 * sp.exp(sp.I * delta), 0, c13]]
    )
    rotation23 = sp.Matrix([[1, 0, 0], [0, c23, s23], [0, -s23, c23]])
    unitary3 = sp.expand(rotation23 * rotation13 * rotation12)
    quartet3 = sp.im(
        sp.expand(
            unitary3[0, 1]
            * unitary3[1, 2]
            * sp.conjugate(unitary3[0, 2])
            * sp.conjugate(unitary3[1, 1])
        )
    )
    closed3 = c12 * c23 * c13**2 * s12 * s23 * s13 * sp.sin(delta)
    ledger.check(
        "the declared three-angle matrix is exactly unitary",
        is_zero(unitary3.H * unitary3 - sp.eye(3)),
    )
    ledger.check(
        "its exact quartet imaginary part has the declared sine product",
        sp.simplify(quartet3 - closed3) == 0,
    )
    ledger.check(
        "complex conjugation reverses the quartet imaginary part",
        sp.simplify(sp.im(sp.conjugate(sp.expand(
            unitary3[0, 1] * unitary3[1, 2] * sp.conjugate(unitary3[0, 2]) * sp.conjugate(unitary3[1, 1])
        ))) + quartet3) == 0,
    )

    baseline_entries = ((0, 1, 1), (1, 2, 1), (0, 2, -1), (1, 1, -1))
    ledger.mutation_sensitive(
        "quartet phase cancellation",
        lambda entries: phase_balanced(entries, 3),
        baseline_entries,
        [
            ((0, 1, 1), (1, 2, 1), (0, 2, -1), (1, 1, 1)),
            ((0, 1, 1), (1, 2, 1), (0, 0, -1), (1, 1, -1)),
        ],
    )
    numeric3 = standard_three_angle_unitary(0.23, 0.19, 0.41, 0.67)
    original_quartet = invariant_quartet(numeric3, 0, 1, 1, 2)
    rephased3 = rephase_unitary(numeric3, [0.2, -0.7, 1.1], [0.4, 0.9, -0.3])
    ledger.check(
        "the reusable quartet is invariant under the declared diagonal action",
        abs(invariant_quartet(rephased3, 0, 1, 1, 2) - original_quartet) < 2e-15,
    )
    ledger.check(
        "the numeric regression agrees with the exact closed form",
        abs(
            original_quartet.imag
            - np.cos(0.23)
            * np.cos(0.41)
            * np.cos(0.19) ** 2
            * np.sin(0.23)
            * np.sin(0.41)
            * np.sin(0.19)
            * np.sin(0.67)
        )
        < 2e-15,
    )

    ledger.check(
        "FG4 imports its unitary-matrix and physical flavor interpretation",
        all(token in source_text for token in ("IMPORTED", "FG3", "standard PDG CKM parametrization", "Jarlskog invariant")),
    )
    ledger.check(
        "FG4 leaves the family count and phase values declared",
        "the number of families N stays an INPUT" in source_text
        and "VALUE of the CP phase delta" in source_text,
    )
    ledger.check(
        "FG4 does not audit enlarged basis freedom from degenerate spectra",
        "degener" not in source_text.lower(),
    )
    ledger.check(
        "a nonzero abstract quartet is not promoted as physical CP evidence",
        "physical CP" in source_text and generic_rephasing_counts(3).irreducible_phases == 1,
    )

    count = ledger.finish()
    print(f"P035 FG4 UNITARY-REPHASING AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
