#!/usr/bin/env python3
"""Verify C-MIX-001 and audit the hash-pinned FG3 source unit."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.matrix_decompositions import (
    biunitary_decomposition,
    gram_eigenvalues,
    real_symmetric_rotation,
    relative_left_basis,
    unitarity_residual,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "5030cf63716914a0effe2d89de2510c14a1c081784ffa2abfd73d24d982ea7cb"


def is_zero(matrix: sp.MatrixBase) -> bool:
    return sp.simplify(matrix) == sp.zeros(*matrix.shape)


@dataclass(frozen=True)
class NumericSVD:
    left: np.ndarray
    diagonal: np.ndarray
    right: np.ndarray
    matrix: np.ndarray


def valid_numeric_svd(candidate: NumericSVD) -> bool:
    tolerance = 2e-12
    diagonalized = candidate.left.conj().T @ candidate.matrix @ candidate.right
    reconstructed = candidate.left @ candidate.diagonal @ candidate.right.conj().T
    off_diagonal = candidate.diagonal.copy()
    count = min(off_diagonal.shape)
    off_diagonal[np.arange(count), np.arange(count)] = 0.0
    diagonal_values = np.diag(candidate.diagonal[:count, :count]).real
    return bool(
        unitarity_residual(candidate.left) < tolerance
        and unitarity_residual(candidate.right) < tolerance
        and np.max(np.abs(diagonalized - candidate.diagonal)) < tolerance
        and np.max(np.abs(reconstructed - candidate.matrix)) < tolerance
        and np.max(np.abs(off_diagonal)) < tolerance
        and np.all(diagonal_values >= 0.0)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P034-FG3")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    ledger.check(
        "the audited FG3 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    reproduced = subprocess.run(
        [sys.executable, str(args.source_file)],
        capture_output=True,
        text=True,
        check=False,
    )
    ledger.check("FG3 exits cleanly", reproduced.returncode == 0)
    ledger.check(
        "FG3's declared six-check tally reproduces",
        "ALL 6 CHECKS PASS" in reproduced.stdout,
    )

    exact_matrix = sp.Matrix([[1 + sp.I, -1], [0, 1 - sp.I]])
    exact_left, exact_diagonal, exact_right = exact_matrix.singular_value_decomposition()
    ledger.check(
        "an independently computed exact complex SVD reconstructs its matrix",
        is_zero(exact_left * exact_diagonal * exact_right.H - exact_matrix),
    )
    ledger.check(
        "the exact column-basis convention diagonalizes as U-dagger M V",
        is_zero(exact_left.H * exact_matrix * exact_right - exact_diagonal),
    )
    ledger.check(
        "the exact square singular-vector bases are unitary",
        is_zero(exact_left.H * exact_left - sp.eye(2))
        and is_zero(exact_right.H * exact_right - sp.eye(2)),
    )
    singular_values = tuple(sp.simplify(exact_diagonal[i, i]) for i in range(2))
    ledger.check(
        "the exact singular values are nonnegative square roots of both Gram spectra",
        set(singular_values) == {sp.Integer(1), sp.Integer(2)}
        and set((exact_matrix * exact_matrix.H).eigenvals()) == {sp.Integer(1), sp.Integer(4)}
        and set((exact_matrix.H * exact_matrix).eigenvals()) == {sp.Integer(1), sp.Integer(4)},
    )

    rectangular_exact = sp.Matrix([[1, 2, 3], [2, 4, 6]])
    r_left, r_diagonal, r_right = rectangular_exact.singular_value_decomposition()
    ledger.check(
        "the exact theorem includes rectangular rank-deficient matrices",
        rectangular_exact.rank() == 1
        and is_zero(r_left * r_diagonal * r_right.H - rectangular_exact)
        and len(rectangular_exact.nullspace()) == 2
        and len(rectangular_exact.H.nullspace()) == 1,
    )
    ledger.check(
        "the rectangular Gram matrices share their sole nonzero eigenvalue",
        set((rectangular_exact * rectangular_exact.H).eigenvals()) == {sp.Integer(0), sp.Integer(70)}
        and set((rectangular_exact.H * rectangular_exact).eigenvals()) == {sp.Integer(0), sp.Integer(70)},
    )

    complex_rotation = sp.Matrix([[1, sp.I], [sp.I, 1]]) / sp.sqrt(2)
    repeated = 3 * sp.eye(2)
    ledger.check(
        "a repeated nonzero singular block admits a paired unitary basis rotation",
        is_zero(complex_rotation.H * complex_rotation - sp.eye(2))
        and is_zero(complex_rotation * repeated * complex_rotation.H - repeated),
    )
    other_rotation = sp.Matrix([[sp.Rational(3, 5), sp.Rational(4, 5)], [-sp.Rational(4, 5), sp.Rational(3, 5)]])
    ledger.check(
        "left and right null bases are independently nonunique for the zero matrix",
        is_zero(complex_rotation * sp.zeros(2) * other_rotation.H)
        and is_zero(complex_rotation.H * complex_rotation - sp.eye(2))
        and is_zero(other_rotation.H * other_rotation - sp.eye(2)),
    )

    numeric_matrix = np.array([[1 + 2j, -3j], [2, 1 - 1j]], dtype=complex)
    numeric = biunitary_decomposition(numeric_matrix)
    baseline = NumericSVD(numeric.left, numeric.diagonal, numeric.right, numeric_matrix)
    swapped_right = numeric.right[:, ::-1]
    scaled_left = 1.01 * numeric.left
    shifted_diagonal = numeric.diagonal.copy()
    shifted_diagonal[0, 0] *= 1.1
    ledger.mutation_sensitive(
        "SVD reconstruction and basis checks",
        valid_numeric_svd,
        baseline,
        [
            NumericSVD(numeric.left, shifted_diagonal, numeric.right, numeric_matrix),
            NumericSVD(numeric.left, numeric.diagonal, swapped_right, numeric_matrix),
            NumericSVD(scaled_left, numeric.diagonal, numeric.right, numeric_matrix),
        ],
    )

    rectangular_numeric = np.array(
        [[1 + 1j, 2], [2 + 2j, 4], [-1j, 3]], dtype=complex
    )
    rectangular = biunitary_decomposition(rectangular_numeric)
    rank_deficient = biunitary_decomposition(np.array(rectangular_exact.tolist(), dtype=complex))
    ledger.check(
        "the reusable full-basis API covers rectangular and zero-singular-value cases",
        rectangular.left.shape == (3, 3)
        and rectangular.right.shape == (2, 2)
        and np.max(np.abs(rectangular.reconstruct() - rectangular_numeric)) < 2e-12
        and rank_deficient.singular_values[-1] < 1e-12,
    )
    left_gram, right_gram = gram_eigenvalues(rectangular_numeric)
    ledger.check(
        "the numeric Gram regression preserves the common nonzero squared spectrum",
        np.allclose(left_gram[:2], rectangular.singular_values**2, atol=2e-12)
        and np.allclose(right_gram, rectangular.singular_values**2, atol=2e-12)
        and abs(left_gram[-1]) < 2e-12,
    )

    first = np.asarray(numeric.left)
    second = np.asarray(biunitary_decomposition(np.array([[0, -1 + 1j], [-1 - 1j, 1j]])).left)
    relative = relative_left_basis(first, second)
    ledger.check(
        "a relative column-basis matrix is exactly unitary up to solver roundoff",
        unitarity_residual(relative) < 2e-12,
    )
    ledger.check(
        "identical ordered bases give the identity",
        np.allclose(relative_left_basis(first, first), np.eye(2), atol=2e-12),
    )
    try:
        relative_left_basis(1.1 * first, second)
    except ValueError:
        nonunitary_rejected = True
    else:
        nonunitary_rejected = False
    ledger.check("the reusable API rejects a fabricated nonunitary basis", nonunitary_rejected)

    # FG3 returns A_i with A_i M_i B_i^dagger=D_i, so mass=A_i*gauge.
    # Direct substitution in a common charged bilinear yields A_u A_d^dagger,
    # whereas FG3 computes A_u^dagger A_d.  Both are unitary, hence its checks
    # cannot distinguish the convention error.
    transform_up = other_rotation
    transform_down = sp.Matrix(
        [[sp.Rational(5, 13), sp.Rational(12, 13)], [-sp.Rational(12, 13), sp.Rational(5, 13)]]
    )
    consistent_relative = sp.simplify(transform_up * transform_down.H)
    fg3_relative = sp.simplify(transform_up.H * transform_down)
    ledger.check(
        "FG3's returned diagonalizer and its mixing formula use incompatible orientations",
        "Uleft = sp.simplify(Umat.H)" in source_text
        and "V = sp.simplify(ULu.H * ULd)" in source_text
        and not is_zero(consistent_relative - fg3_relative),
    )
    ledger.check(
        "unitarity alone is insensitive to FG3's orientation defect",
        is_zero(consistent_relative.H * consistent_relative - sp.eye(2))
        and is_zero(fg3_relative.H * fg3_relative - sp.eye(2)),
    )

    def convention_predicate(candidate: sp.MatrixBase) -> bool:
        return is_zero(candidate - consistent_relative)

    ledger.mutation_sensitive(
        "field-rotation convention",
        convention_predicate,
        consistent_relative,
        [fg3_relative, transform_up.H * transform_down.H],
    )

    symmetric_exact = sp.Matrix(
        [[sp.Integer(1), sp.Rational(1, 2)], [sp.Rational(1, 2), sp.Integer(2)]]
    )
    theta = sp.pi / 8
    rotation = sp.Matrix([[sp.cos(theta), sp.sin(theta)], [-sp.sin(theta), sp.cos(theta)]])
    rotated = sp.simplify(rotation.T * symmetric_exact * rotation)
    ledger.check(
        "the real symmetric two-by-two formula diagonalizes in its declared convention",
        sp.simplify(sp.tan(2 * theta) - 1) == 0
        and rotated[0, 1] == 0
        and rotated[1, 0] == 0
        and is_zero(rotation.T * rotation - sp.eye(2)),
    )
    numeric_rotation = real_symmetric_rotation(symmetric_exact.tolist())
    ledger.check(
        "the reusable rotation API agrees with the exact pi-over-eight case",
        abs(numeric_rotation.angle - np.pi / 8) < 2e-15
        and np.max(np.abs(numeric_rotation.diagonalized - np.diag(np.diag(numeric_rotation.diagonalized)))) < 2e-15,
    )
    try:
        real_symmetric_rotation([[1, sp.I], [-sp.I, 2]])
    except (TypeError, ValueError):
        complex_rejected = True
    else:
        complex_rejected = False
    ledger.check("the real symmetric formula is not extended to a generic complex texture", complex_rejected)

    sector_shift = sp.pi / 12
    second_sector = sp.Matrix(
        [[sp.cos(sector_shift), sp.sin(sector_shift)], [-sp.sin(sector_shift), sp.cos(sector_shift)]]
    )
    ledger.check(
        "one sector's diagonalizing angle does not determine a two-sector mixing angle",
        not is_zero(rotation.H * second_sector - rotation.H),
    )

    ledger.check(
        "FG3 explicitly imports every physical current and fermion premise",
        all(token in source_text for token in ("IMPORTED", "M1", "SM2", "SM3", "W3/W7")),
    )
    ledger.check(
        "FG3 inserts rather than derives its two Yukawa textures",
        "Yu = sp.Matrix" in source_text
        and "Yd = sp.Matrix" in source_text
        and "ABSOLUTE Yukawa couplings y_ij" in source_text,
    )
    ledger.check(
        "FG3's anomaly check assumes a symbolic per-generation coefficient",
        'A_gen = sp.Symbol("A_gen")' in source_text
        and "anomaly_mass_basis = A_gen * trace_VdV" in source_text,
    )
    ledger.check(
        "FG3 excludes zero singular values instead of proving the general theorem",
        "Requires the m_i nonzero" in source_text,
    )

    count = ledger.finish()
    print(f"P034 FG3 MATRIX-DECOMPOSITION AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
