from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework import (
    CoherentStateLedger,
    coherent_state_coefficient,
    coherent_state_intensity,
    coherent_state_ledger,
    coherent_state_number_modes,
    coherent_state_number_probability,
    coherent_state_overlap,
)
from substrate_framework.bosonic_fock import normalized_factorial_one_mass


def test_exact_complex_displacement_intensity() -> None:
    x, y = sp.symbols("x y", real=True)
    assert coherent_state_intensity(x + sp.I * y) == x**2 + y**2
    assert coherent_state_intensity(3 + 4 * sp.I) == 25


def test_coherent_coefficients_have_the_exact_gaussian_half_factor() -> None:
    alpha = 3 + 4 * sp.I
    intensity = sp.Integer(25)
    for order in range(7):
        assert coherent_state_coefficient(
            order,
            displacement=alpha,
        ) == sp.simplify(
            sp.exp(-intensity / 2)
            * alpha**order
            / sp.sqrt(sp.factorial(order))
        )


def test_number_probability_is_the_coefficient_modulus_square() -> None:
    alpha = 1 + 2 * sp.I
    for order in range(7):
        coefficient = coherent_state_coefficient(order, displacement=alpha)
        actual = sp.simplify(sp.conjugate(coefficient) * coefficient)
        expected = coherent_state_number_probability(order, displacement=alpha)
        assert sp.simplify(actual - expected) == 0


def test_positive_intensity_probability_reuses_the_accepted_mass() -> None:
    alpha = 1 + sp.I
    for order in range(8):
        assert coherent_state_number_probability(
            order,
            displacement=alpha,
        ) == normalized_factorial_one_mass(
            order,
            intensity=2,
            support="all_nonnegative",
        )


def test_raw_probability_sum_is_exactly_one() -> None:
    intensity = sp.symbols("S", positive=True)
    order = sp.symbols("n", integer=True, nonnegative=True)
    total = sp.summation(
        sp.exp(-intensity) * intensity**order / sp.factorial(order),
        (order, 0, sp.oo),
    )
    assert sp.simplify(total - 1) == 0


def test_annihilation_eigenvector_recurrence_is_exact() -> None:
    alpha = 2 - 3 * sp.I
    for order in range(7):
        left = sp.sqrt(order + 1) * coherent_state_coefficient(
            order + 1,
            displacement=alpha,
        )
        right = alpha * coherent_state_coefficient(order, displacement=alpha)
        assert sp.simplify(left - right) == 0


def test_vacuum_overlap_and_probability_are_distinct() -> None:
    ledger = coherent_state_ledger(displacement=2 * sp.I)
    assert ledger.vacuum_amplitude == sp.exp(-2)
    assert ledger.vacuum_probability == sp.exp(-4)


def test_zero_displacement_is_exactly_the_vacuum() -> None:
    ledger = coherent_state_ledger(displacement=0)
    assert ledger.occupation_support == "vacuum_only"
    assert coherent_state_number_probability(0, displacement=0) == 1
    for order in range(1, 5):
        assert coherent_state_number_probability(order, displacement=0) == 0
    assert coherent_state_number_modes(displacement=0) == (0,)


def test_nonzero_displacement_has_all_nonnegative_number_support() -> None:
    ledger = coherent_state_ledger(displacement=sp.I / 3)
    assert ledger.occupation_support == "all_nonnegative"
    for order in range(8):
        assert coherent_state_number_probability(
            order,
            displacement=sp.I / 3,
        ).is_positive


def test_phase_rotation_changes_amplitudes_not_number_probabilities() -> None:
    alpha = 2
    rotated = 2 * sp.I
    for order in range(6):
        assert coherent_state_number_probability(
            order,
            displacement=alpha,
        ) == coherent_state_number_probability(order, displacement=rotated)
    assert coherent_state_coefficient(1, displacement=alpha) != coherent_state_coefficient(
        1,
        displacement=rotated,
    )


def test_overlap_has_unit_diagonal_and_vacuum_specialization() -> None:
    alpha = 1 + 2 * sp.I
    assert sp.simplify(coherent_state_overlap(alpha, alpha) - 1) == 0
    assert coherent_state_overlap(0, alpha) == sp.exp(-sp.Rational(5, 2))


def test_overlap_conjugate_symmetry() -> None:
    alpha = 1 + 2 * sp.I
    beta = 3 - sp.I
    assert sp.simplify(
        coherent_state_overlap(alpha, beta)
        - sp.conjugate(coherent_state_overlap(beta, alpha))
    ) == 0


def test_ledger_records_exact_moments_and_interpretation_ceiling() -> None:
    ledger = coherent_state_ledger(displacement=3 + 4 * sp.I)
    assert isinstance(ledger, CoherentStateLedger)
    assert ledger.intensity == 25
    assert ledger.mean_occupation == 25
    assert ledger.occupation_variance == 25
    assert ledger.annihilation_eigenvalue == 3 + 4 * sp.I
    assert ledger.normalized
    assert ledger.physical_preparation_is_separate_premise
    assert ledger.classical_phase_map_is_separate_premise
    assert ledger.physical_process_probability_is_separate_premise


def test_number_modes_preserve_the_positive_integer_tie() -> None:
    assert coherent_state_number_modes(displacement=3 + 4 * sp.I) == (24, 25)
    assert coherent_state_number_modes(displacement=sp.Rational(3, 2)) == (2,)


def test_missing_gaussian_half_factor_fails_normalization() -> None:
    intensity = sp.symbols("S", positive=True)
    order = sp.symbols("n", integer=True, nonnegative=True)
    wrong_total = sp.summation(
        intensity**order / sp.factorial(order),
        (order, 0, sp.oo),
    )
    assert wrong_total == sp.exp(intensity)
    assert sp.simplify(wrong_total - 1) != 0


def test_missing_square_root_factorial_breaks_eigenvector_recurrence() -> None:
    alpha = sp.Integer(2)
    order = 3
    wrong_n = sp.exp(-2) * alpha**order / sp.factorial(order)
    wrong_next = sp.exp(-2) * alpha ** (order + 1) / sp.factorial(order + 1)
    assert sp.simplify(sp.sqrt(order + 1) * wrong_next - alpha * wrong_n) != 0


@pytest.mark.parametrize("bad", [0.25, 1 + 0.5 * sp.I])
def test_floating_displacements_are_rejected(bad: object) -> None:
    with pytest.raises(ValueError, match="exact"):
        coherent_state_intensity(bad)


def test_undecidable_displacement_is_rejected() -> None:
    alpha = sp.Symbol("alpha")
    with pytest.raises(ValueError, match="explicitly complex"):
        coherent_state_intensity(alpha)


def test_invalid_orders_are_rejected() -> None:
    for bad in (-1, sp.Rational(1, 2), 1.0):
        with pytest.raises(ValueError, match="nonnegative integer"):
            coherent_state_coefficient(bad, displacement=1)


def test_modes_require_decidable_rational_intensity() -> None:
    x = sp.symbols("x", real=True, nonzero=True)
    with pytest.raises(ValueError, match="positive rational"):
        coherent_state_number_modes(displacement=x)


def test_public_docstrings_preserve_physical_ceiling() -> None:
    text = " ".join(coherent_state_number_probability.__doc__.split())
    assert "not a probability that a material event" in text
    ledger_text = " ".join(coherent_state_ledger.__doc__.split())
    assert "does not imply an unbounded classical excursion" in ledger_text
