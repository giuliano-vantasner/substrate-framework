"""Primary exact and regression verifier for P072 / C-OVL-003."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.overlap_compressions import (
    commuting_hermitian,
    matrix_commutator,
    multiplication_compression,
    parity_forces_zero,
    quartic_asymmetric_compression_ledger,
    real_symmetric_commutator_scalar,
    spectral_multiplicity_ledger,
    unitary_similarity,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_MH3_overlap_feeds_mixing.py"
)
SOURCE_SHA256 = "f33ab10dadee8ae4f747328f1fc593733942d18ccdb280ca6f21c3961e03c425"


def source_proxy_matrix(
    amplitude: sp.Expr,
    asymmetry: sp.Expr,
    inverse_width: sp.Expr,
) -> sp.Matrix:
    """Reconstruct MH3's matrix from its width-bearing exact integrals."""

    i2 = 2 / inverse_width
    i3 = sp.pi / (2 * inverse_width)
    i4 = 4 / (3 * inverse_width)
    i5 = 3 * sp.pi / (8 * inverse_width)
    even_norm = i2
    odd_norm = sp.simplify(i2 - i4)
    odd_raw = sp.simplify(i3 - i5)
    return sp.simplify(
        sp.Matrix(
            [
                [amplitude * i3 / even_norm, amplitude * asymmetry * odd_raw / sp.sqrt(even_norm * odd_norm)],
                [amplitude * asymmetry * odd_raw / sp.sqrt(even_norm * odd_norm), amplitude * odd_raw / odd_norm],
            ]
        )
    )


def main() -> int:
    ledger = CheckLedger("P072")

    source_bytes = SOURCE.read_bytes()
    ledger.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    source_text = source_bytes.decode("utf-8")
    ledger.check(
        "source changes both width and asymmetry",
        "kap_u = sp.Rational(1, 2)" in source_text
        and "kap_d = sp.Rational(2, 3)" in source_text
        and "b_u = sp.Rational(1, 3)" in source_text
        and "b_d = sp.Rational(1, 4)" in source_text,
    )
    ledger.check(
        "source relative product uses row transforms as column bases",
        "Uleft = sp.simplify(Umat.H)" in source_text
        and "V = sp.simplify(ULu.H * ULd)" in source_text,
    )
    ledger.check(
        "source shared-parameter verdict is a literal assertion",
        "shared_parameter_set = True" in source_text,
    )
    ledger.check(
        "source and canonical module avoid numpy quadrature aliases",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "np.trapz"
        not in Path("src/substrate_framework/overlap_compressions.py").read_text(
            encoding="utf-8"
        )
        and "np.trapezoid"
        not in Path("src/substrate_framework/overlap_compressions.py").read_text(
            encoding="utf-8"
        ),
    )

    amplitude, asymmetry, kappa = sp.symbols("A b kappa", positive=True)
    source_matrix = source_proxy_matrix(amplitude, asymmetry, kappa)
    ledger.check(
        "MH3 exact source reduction",
        source_matrix
        == sp.pi
        * amplitude
        * sp.Matrix([[4, sp.sqrt(3) * asymmetry], [sp.sqrt(3) * asymmetry, 3]])
        / 16,
    )
    ledger.check(
        "MH3 source matrix has zero width derivative",
        source_matrix.applyfunc(lambda entry: sp.diff(entry, kappa)) == sp.zeros(2),
    )
    ledger.check(
        "MH3 source trace and determinant",
        sp.trace(source_matrix) == 7 * sp.pi * amplitude / 16
        and sp.simplify(
            source_matrix.det()
            - 3
            * sp.pi**2
            * amplitude**2
            * (4 - asymmetry**2)
            / 256
        )
        == 0,
    )
    ledger.check(
        "width-only mutation leaves MH3 texture unchanged",
        source_proxy_matrix(1, sp.Rational(1, 3), sp.Rational(1, 2))
        == source_proxy_matrix(1, sp.Rational(1, 3), sp.Rational(2, 3)),
    )
    ledger.check(
        "asymmetry mutation changes MH3 texture",
        source_proxy_matrix(1, sp.Rational(1, 3), sp.Rational(1, 2))
        != source_proxy_matrix(1, sp.Rational(1, 4), sp.Rational(1, 2)),
    )
    ledger.check(
        "source matrices fail to commute only when asymmetry changes",
        not commuting_hermitian(
            source_proxy_matrix(1, sp.Rational(1, 3), sp.Rational(1, 2)),
            source_proxy_matrix(1, sp.Rational(1, 4), sp.Rational(2, 3)),
        )
        and commuting_hermitian(
            source_proxy_matrix(1, sp.Rational(1, 3), sp.Rational(1, 2)),
            source_proxy_matrix(2, sp.Rational(1, 3), sp.Rational(2, 3)),
        ),
    )

    x = sp.symbols("x", real=True)
    fourier_modes = (
        1 / sp.sqrt(2 * sp.pi),
        sp.exp(sp.I * x) / sp.sqrt(2 * sp.pi),
    )
    compression = multiplication_compression(
        fourier_modes,
        2 + sp.cos(x),
        x,
        lower=-sp.pi,
        upper=sp.pi,
    )
    expected_compression = sp.Matrix(
        [[2, sp.Rational(1, 2)], [sp.Rational(1, 2), 2]]
    )
    ledger.check("complex Fourier modes are orthonormal", compression.gram_matrix == sp.eye(2))
    ledger.check("real multiplier compression is Hermitian", compression.matrix == expected_compression)
    ledger.check(
        "Rayleigh bounds hold in soluble compression",
        compression.matrix.eigenvals()
        == {sp.Rational(3, 2): 1, sp.Rational(5, 2): 1},
    )
    wrong_gram = sp.Matrix(
        [
            [
                sp.integrate(left * right, (x, -sp.pi, sp.pi))
                for right in fourier_modes
            ]
            for left in fourier_modes
        ]
    )
    ledger.check(
        "omitted-conjugation mutation breaks orthonormality",
        wrong_gram != sp.eye(2),
    )
    constant = multiplication_compression(
        fourier_modes,
        7,
        x,
        lower=-sp.pi,
        upper=sp.pi,
    )
    ledger.check("constant multiplier gives constant identity", constant.matrix == 7 * sp.eye(2))
    zero = multiplication_compression(
        fourier_modes,
        0,
        x,
        lower=-sp.pi,
        upper=sp.pi,
    )
    ledger.check("zero multiplier gives zero compression", zero.matrix == sp.zeros(2))

    basis_change = sp.Matrix([[1, 1], [-1, 1]]) / sp.sqrt(2)
    transformed = unitary_similarity(compression.matrix, basis_change)
    ledger.check(
        "common basis change alters entries covariantly",
        transformed == basis_change.adjoint() * compression.matrix * basis_change
        and transformed != compression.matrix,
    )
    ledger.check(
        "basis change preserves characteristic polynomial",
        transformed.charpoly().as_expr() == compression.matrix.charpoly().as_expr(),
    )
    ledger.check(
        "basis change preserves trace and determinant",
        sp.trace(transformed) == sp.trace(compression.matrix)
        and transformed.det() == compression.matrix.det(),
    )

    ledger.check("even profile kills even-odd cross overlap", parity_forces_zero(1, 1, -1))
    ledger.check("odd profile permits even-odd cross overlap", not parity_forces_zero(1, -1, -1))
    ledger.check("odd profile kills same-parity overlap", parity_forces_zero(1, -1, 1))

    actual = quartic_asymmetric_compression_ledger(amplitude, asymmetry, kappa)
    actual_expected = sp.Matrix(
        [
            [9 * sp.pi * amplitude / 32, sp.sqrt(2) * amplitude * asymmetry / 5],
            [sp.sqrt(2) * amplitude * asymmetry / 5, 3 * sp.pi * amplitude / 16],
        ]
    )
    ledger.check("actual C-QBL-003 compression derived", actual.matrix == actual_expected)
    ledger.check(
        "actual C-QBL-003 mode norms derived",
        actual.even_mode_norm == 4 / (3 * kappa)
        and actual.odd_mode_norm == 2 / (3 * kappa),
    )
    ledger.check(
        "actual compression has zero width derivative",
        actual.matrix.applyfunc(lambda entry: sp.diff(entry, kappa)) == sp.zeros(2),
    )
    ledger.check(
        "even profile restores exact parity block",
        quartic_asymmetric_compression_ledger(amplitude, 0, kappa).matrix
        == sp.diag(9 * sp.pi * amplitude / 32, 3 * sp.pi * amplitude / 16),
    )
    ledger.check(
        "odd-profile sign mutation flips only cross entries",
        actual.matrix[0, 1]
        == -quartic_asymmetric_compression_ledger(
            amplitude, -asymmetry, kappa
        ).matrix[0, 1]
        and actual.matrix[0, 0]
        == quartic_asymmetric_compression_ledger(
            amplitude, -asymmetry, kappa
        ).matrix[0, 0],
    )
    ledger.check(
        "actual accepted even mode rejects source proxy",
        actual.matrix[0, 0] == 9 * sp.pi * amplitude / 32
        and actual.matrix[0, 0] != source_matrix[0, 0],
    )

    first = quartic_asymmetric_compression_ledger(
        1, sp.Rational(1, 3), sp.Rational(1, 2)
    ).matrix
    width_changed = quartic_asymmetric_compression_ledger(
        1, sp.Rational(1, 3), sp.Rational(2, 3)
    ).matrix
    asymmetry_changed = quartic_asymmetric_compression_ledger(
        1, sp.Rational(1, 4), sp.Rational(2, 3)
    ).matrix
    ledger.check("actual width-only change leaves matrix equal", first == width_changed)
    ledger.check("equal actual matrices commute", commuting_hermitian(first, width_changed))
    ledger.check(
        "changed asymmetry creates nonzero commutator",
        not commuting_hermitian(first, asymmetry_changed),
    )
    actual_scalar = real_symmetric_commutator_scalar(first, asymmetry_changed)
    ledger.check(
        "actual commutator scalar tracks asymmetry difference",
        sp.simplify(actual_scalar - 3 * sp.sqrt(2) * sp.pi * (sp.Rational(1, 4) - sp.Rational(1, 3)) / 160)
        == 0,
    )
    diagonal_one = sp.diag(1, 2)
    diagonal_two = sp.diag(4, 9)
    ledger.check(
        "different Hermitian matrices can share an eigenbasis",
        diagonal_one != diagonal_two and commuting_hermitian(diagonal_one, diagonal_two),
    )
    ledger.check(
        "matrix difference is not a commutator oracle",
        matrix_commutator(diagonal_one, diagonal_two) == sp.zeros(2),
    )

    identity_ledger = spectral_multiplicity_ledger(sp.eye(2))
    ledger.check(
        "degenerate block exposes extra basis freedom",
        identity_ledger.degenerate_subspace_dimensions == (2,)
        and identity_ledger.additional_unitary_parameters == 2,
    )
    arbitrary_rotation = sp.Matrix([[0, 1], [-1, 0]])
    ledger.check(
        "degenerate matrix permits arbitrary rotation",
        unitary_similarity(sp.eye(2), arbitrary_rotation) == sp.eye(2),
    )
    phase = sp.diag(1, sp.I)
    permutation = sp.Matrix([[0, 1], [1, 0]])
    ledger.check(
        "independent eigenvector phase can make an equal-matrix relative basis nonidentity",
        phase != sp.eye(2) and unitary_similarity(diagonal_one, phase) == diagonal_one,
    )
    ledger.check(
        "independent eigenvector ordering can make an equal-matrix relative basis nonidentity",
        permutation != sp.eye(2)
        and unitary_similarity(diagonal_one, permutation) == sp.diag(2, 1),
    )
    ledger.check(
        "unitarity alone cannot establish nontrivial invariant misalignment",
        unitary_similarity(sp.eye(2), phase) == sp.eye(2)
        and phase.adjoint() * phase == sp.eye(2),
    )

    ledger.check(
        "source declares no Yukawa Lagrangian or charged-current operator",
        "L_yukawa" not in source_text and "charged_current" not in source_text,
    )
    ledger.check(
        "source matrix alone cannot establish its physical labels",
        "shared_parameter_set = True" in source_text
        and "b_d = sp.Rational(1, 4)" in source_text,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
