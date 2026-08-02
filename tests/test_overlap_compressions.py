from __future__ import annotations

from pathlib import Path

import pytest
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


def test_complex_mode_compression_uses_load_bearing_conjugation() -> None:
    x = sp.symbols("x", real=True)
    modes = (1 / sp.sqrt(2 * sp.pi), sp.exp(sp.I * x) / sp.sqrt(2 * sp.pi))
    ledger = multiplication_compression(
        modes,
        2 + sp.cos(x),
        x,
        lower=-sp.pi,
        upper=sp.pi,
    )
    assert ledger.gram_matrix == sp.eye(2)
    assert ledger.matrix == sp.Matrix([[2, sp.Rational(1, 2)], [sp.Rational(1, 2), 2]])
    wrong_gram = sp.Matrix(
        [
            [sp.integrate(left * right, (x, -sp.pi, sp.pi)) for right in modes]
            for left in modes
        ]
    )
    assert wrong_gram != sp.eye(2)


def test_constant_real_multiplier_compresses_to_constant_identity() -> None:
    x = sp.symbols("x", real=True)
    modes = (1 / sp.sqrt(2), sp.sqrt(sp.Rational(3, 2)) * x)
    ledger = multiplication_compression(modes, 7, x, lower=-1, upper=1)
    assert ledger.matrix == 7 * sp.eye(2)


def test_common_basis_change_is_unitary_similarity_and_preserves_spectrum() -> None:
    matrix = sp.Matrix([[1, 2], [2, 4]])
    unitary = sp.Matrix([[1, 1], [-1, 1]]) / sp.sqrt(2)
    transformed = unitary_similarity(matrix, unitary)
    assert transformed == sp.simplify(unitary.adjoint() * matrix * unitary)
    assert transformed != matrix
    assert transformed.charpoly().as_expr() == matrix.charpoly().as_expr()
    assert sp.trace(transformed) == sp.trace(matrix)
    assert transformed.det() == matrix.det()


@pytest.mark.parametrize(
    ("left", "profile", "right", "expected"),
    [
        (1, 1, -1, True),
        (-1, 1, 1, True),
        (1, -1, 1, True),
        (-1, -1, -1, True),
        (1, 1, 1, False),
        (-1, 1, -1, False),
    ],
)
def test_parity_selection_uses_all_three_factors(left, profile, right, expected) -> None:
    assert parity_forces_zero(left, profile, right) is expected


def test_actual_quartic_modes_give_exact_asymmetric_compression() -> None:
    amplitude, asymmetry, kappa = sp.symbols("A b kappa", positive=True)
    ledger = quartic_asymmetric_compression_ledger(amplitude, asymmetry, kappa)
    expected = sp.Matrix(
        [
            [9 * sp.pi * amplitude / 32, sp.sqrt(2) * amplitude * asymmetry / 5],
            [sp.sqrt(2) * amplitude * asymmetry / 5, 3 * sp.pi * amplitude / 16],
        ]
    )
    assert ledger.matrix == expected
    assert ledger.even_mode_norm == 4 / (3 * kappa)
    assert ledger.odd_mode_norm == 2 / (3 * kappa)
    assert ledger.even_profile_matrix + ledger.odd_profile_matrix == ledger.matrix


def test_actual_quartic_compression_is_width_independent() -> None:
    amplitude, asymmetry, kappa = sp.symbols("A b kappa", positive=True)
    matrix = quartic_asymmetric_compression_ledger(amplitude, asymmetry, kappa).matrix
    assert matrix.applyfunc(lambda entry: sp.diff(entry, kappa)) == sp.zeros(2)
    assert quartic_asymmetric_compression_ledger(amplitude, asymmetry, 1).matrix == (
        quartic_asymmetric_compression_ledger(amplitude, asymmetry, 7).matrix
    )


def test_odd_profile_parameter_is_necessary_and_sign_sensitive() -> None:
    amplitude, asymmetry = sp.symbols("A b", real=True)
    even = quartic_asymmetric_compression_ledger(amplitude, 0, 1)
    positive = quartic_asymmetric_compression_ledger(amplitude, asymmetry, 1)
    negative = quartic_asymmetric_compression_ledger(amplitude, -asymmetry, 1)
    assert even.matrix[0, 1] == 0
    assert positive.matrix[0, 1] == -negative.matrix[0, 1]
    assert positive.matrix[0, 0] == negative.matrix[0, 0]
    assert positive.matrix[1, 1] == negative.matrix[1, 1]


def test_actual_even_mode_is_not_mh3_sech_proxy() -> None:
    amplitude = sp.symbols("A", positive=True)
    actual = quartic_asymmetric_compression_ledger(amplitude, 0, 1).matrix[0, 0]
    source_proxy = sp.pi * amplitude / 4
    assert actual == 9 * sp.pi * amplitude / 32
    assert actual != source_proxy


def test_commutator_separates_matrix_difference_from_misalignment() -> None:
    diagonal_one = sp.diag(1, 2)
    diagonal_two = sp.diag(3, 5)
    rotated = sp.Matrix([[4, 1], [1, 4]])
    assert diagonal_one != diagonal_two
    assert commuting_hermitian(diagonal_one, diagonal_two)
    assert not commuting_hermitian(diagonal_one, rotated)
    assert matrix_commutator(diagonal_one, diagonal_two) == sp.zeros(2)
    assert matrix_commutator(diagonal_one, rotated) != sp.zeros(2)


def test_two_by_two_commutator_scalar_is_exact_criterion() -> None:
    a, b, d, e, f, h = sp.symbols("a b d e f h", real=True)
    first = sp.Matrix([[a, b], [b, d]])
    second = sp.Matrix([[e, f], [f, h]])
    scalar = real_symmetric_commutator_scalar(first, second)
    assert sp.expand(scalar - (b * (-e + h) + f * (a - d))) == 0
    assert matrix_commutator(first, second) == sp.Matrix([[0, scalar], [-scalar, 0]])


def test_equal_asymmetric_compressions_commute_but_different_ones_need_not() -> None:
    first = quartic_asymmetric_compression_ledger(1, sp.Rational(1, 3), 1).matrix
    equal_at_other_width = quartic_asymmetric_compression_ledger(
        1, sp.Rational(1, 3), 9
    ).matrix
    changed_asymmetry = quartic_asymmetric_compression_ledger(
        1, sp.Rational(1, 4), 1
    ).matrix
    assert first == equal_at_other_width
    assert commuting_hermitian(first, equal_at_other_width)
    assert not commuting_hermitian(first, changed_asymmetry)


def test_degenerate_spectrum_records_extra_arbitrary_basis_freedom() -> None:
    degenerate = spectral_multiplicity_ledger(3 * sp.eye(2))
    nondegenerate = spectral_multiplicity_ledger(sp.diag(1, 2))
    assert degenerate.degenerate_subspace_dimensions == (2,)
    assert degenerate.additional_unitary_parameters == 2
    assert nondegenerate.degenerate_subspace_dimensions == ()
    assert nondegenerate.additional_unitary_parameters == 0
    rotation = sp.Matrix([[0, 1], [-1, 0]])
    assert unitary_similarity(3 * sp.eye(2), rotation) == 3 * sp.eye(2)


def test_canonical_module_uses_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/overlap_compressions.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: multiplication_compression((), 1, sp.symbols("x", real=True)),
            "non-empty",
        ),
        (
            lambda: multiplication_compression((1,), 1, sp.symbols("x")),
            "real SymPy symbol",
        ),
        (
            lambda: multiplication_compression(
                (1,), sp.I, sp.symbols("x", real=True), lower=0, upper=1
            ),
            "provably real",
        ),
        (
            lambda: multiplication_compression(
                (2,), 1, sp.symbols("x", real=True), lower=0, upper=1
            ),
            "orthonormal",
        ),
        (lambda: unitary_similarity(sp.eye(2), [[1, 1], [0, 1]]), "unitary"),
        (lambda: parity_forces_zero(0, 1, -1), "parities"),
        (lambda: commuting_hermitian([[0, 1], [0, 0]], sp.eye(2)), "Hermitian"),
        (lambda: real_symmetric_commutator_scalar(sp.eye(3), sp.eye(3)), "2 by 2"),
        (lambda: spectral_multiplicity_ledger([[0, 1], [0, 0]]), "Hermitian"),
        (lambda: quartic_asymmetric_compression_ledger(1, 1, 0), "positive"),
    ],
)
def test_overlap_compression_api_rejects_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
