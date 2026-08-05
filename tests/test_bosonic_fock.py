from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.bosonic_fock import (
    bosonic_cosine_matrix_element,
    bosonic_cosine_matrix_element_square,
    bosonic_fock_rung,
    factorial_one_mass,
    factorial_one_modes,
    factorial_one_total_mass,
    normalized_factorial_one_mass,
    truncated_bosonic_fock_ladder,
)
from substrate_framework.cosine_vertices import vacuum_one_high_coefficient


def _raw_truncated_ladder(dimension: int) -> tuple[sp.Matrix, sp.Matrix]:
    annihilation = sp.zeros(dimension)
    for level in range(1, dimension):
        annihilation[level - 1, level] = sp.sqrt(level)
    return annihilation, annihilation.T


def test_infinite_rung_actions_and_factorial_induction_data() -> None:
    for level in range(21):
        rung = bosonic_fock_rung(level)
        assert rung.annihilation_coefficient == sp.sqrt(level)
        assert rung.creation_coefficient == sp.sqrt(level + 1)
        assert rung.number_coefficient == level
        assert rung.reverse_number_coefficient == level + 1
        assert rung.commutator_coefficient == 1
        assert rung.repeated_creation_vacuum_coefficient == sp.sqrt(
            sp.factorial(level)
        )
        assert rung.repeated_creation_vacuum_norm_squared == sp.factorial(level)
        assert rung.physical_rate_interpretation_is_separate_premise is True

    for level in range(20):
        left = bosonic_fock_rung(level).repeated_creation_vacuum_coefficient
        right = bosonic_fock_rung(level + 1).repeated_creation_vacuum_coefficient
        assert sp.simplify(right - sp.sqrt(level + 1) * left) == 0


def test_raw_matrix_construction_rederives_truncation_defect_and_trace() -> None:
    for dimension in range(1, 10):
        ledger = truncated_bosonic_fock_ladder(dimension)
        annihilation, creation = _raw_truncated_ladder(dimension)
        raw_commutator = annihilation * creation - creation * annihilation
        top = sp.zeros(dimension)
        top[dimension - 1, dimension - 1] = 1
        expected = sp.eye(dimension) - dimension * top
        assert ledger.annihilation == annihilation
        assert ledger.creation == creation
        assert ledger.commutator == raw_commutator
        assert ledger.commutator == expected
        assert ledger.expected_commutator == expected
        assert ledger.identity_minus_commutator == dimension * top
        assert ledger.commutator_trace == 0
        assert sp.trace(sp.eye(dimension)) == dimension
        assert ledger.full_identity_commutator_is_impossible is True
        assert isinstance(ledger.annihilation, sp.ImmutableDenseMatrix)


def test_explicit_repeated_creation_vectors_have_factorial_norm() -> None:
    dimension = 13
    _, creation = _raw_truncated_ladder(dimension)
    vacuum = sp.zeros(dimension, 1)
    vacuum[0] = 1
    state = vacuum
    for order in range(dimension):
        expected = sp.zeros(dimension, 1)
        expected[order] = sp.sqrt(sp.factorial(order))
        assert state == expected
        assert (state.T * state)[0] == sp.factorial(order)
        state = creation * state


def test_full_coordinate_power_vacuum_to_n_element_forces_all_creation() -> None:
    dimension = 20
    annihilation, creation = _raw_truncated_ladder(dimension)
    coordinate = annihilation + creation
    vacuum = sp.zeros(dimension, 1)
    vacuum[0] = 1
    for order in range(11):
        target = sp.zeros(1, dimension)
        target[0, order] = 1
        element = sp.simplify((target * coordinate**order * vacuum)[0])
        assert element == sp.sqrt(sp.factorial(order))


def test_conditional_cosine_composition_retains_parity_and_scales() -> None:
    amplitude, high_scale, low_scale = sp.symbols(
        "U h ell",
        real=True,
        nonzero=True,
    )
    for order in range(10):
        actual = bosonic_cosine_matrix_element(
            order,
            amplitude=amplitude,
            high_scale=high_scale,
            low_scale=low_scale,
        )
        direct = sp.simplify(
            vacuum_one_high_coefficient(
                order,
                amplitude=amplitude,
                high_scale=high_scale,
                low_scale=low_scale,
            )
            * sp.sqrt(sp.factorial(order))
        )
        assert sp.simplify(actual - direct) == 0
        square = bosonic_cosine_matrix_element_square(
            order,
            amplitude=amplitude,
            high_scale=high_scale,
            low_scale=low_scale,
        )
        if order % 2 == 0:
            assert actual == 0
            assert square == 0
        else:
            expected = (
                amplitude
                * (-1) ** ((order - 1) // 2)
                * high_scale
                * low_scale**order
                / sp.sqrt(sp.factorial(order))
            )
            assert sp.simplify(actual - expected) == 0
            assert sp.simplify(
                square
                - amplitude**2
                * high_scale**2
                * low_scale ** (2 * order)
                / sp.factorial(order)
            ) == 0


def test_factorial_one_supports_and_totals_are_distinct() -> None:
    intensity = sp.symbols("S", positive=True)
    assert factorial_one_mass(
        0,
        intensity=intensity,
        support="all_nonnegative",
    ) == 1
    assert factorial_one_mass(0, intensity=intensity, support="positive") == 0
    assert factorial_one_mass(2, intensity=intensity, support="positive_odd") == 0
    assert factorial_one_mass(
        3,
        intensity=intensity,
        support="positive_odd",
    ) == intensity**3 / 6

    assert factorial_one_total_mass(
        intensity=intensity,
        support="all_nonnegative",
    ) == sp.exp(intensity)
    assert factorial_one_total_mass(
        intensity=intensity,
        support="positive",
    ) == sp.exp(intensity) - 1
    assert factorial_one_total_mass(
        intensity=intensity,
        support="positive_odd",
    ) == sp.sinh(intensity)


def test_raw_series_rederive_every_factorial_one_normalizer() -> None:
    order = sp.symbols("n", integer=True, nonnegative=True)
    intensity = sp.symbols("S", positive=True)
    all_sum = sp.summation(intensity**order / sp.factorial(order), (order, 0, sp.oo))
    positive_sum = sp.summation(
        intensity**order / sp.factorial(order),
        (order, 1, sp.oo),
    )
    odd_sum = sum(
        intensity ** (2 * index + 1) / sp.factorial(2 * index + 1)
        for index in range(8)
    )
    assert all_sum == sp.exp(intensity)
    assert sp.simplify(positive_sum - (sp.exp(intensity) - 1)) == 0
    assert sp.series(sp.sinh(intensity) - odd_sum, intensity, 0, 17).removeO() == 0


def test_normalized_masses_use_the_declared_denominator() -> None:
    intensity = sp.symbols("S", positive=True)
    assert normalized_factorial_one_mass(
        0,
        intensity=intensity,
        support="all_nonnegative",
    ) == sp.exp(-intensity)
    assert normalized_factorial_one_mass(
        1,
        intensity=intensity,
        support="positive",
    ) == intensity / (sp.exp(intensity) - 1)
    assert normalized_factorial_one_mass(
        3,
        intensity=intensity,
        support="positive_odd",
    ) == intensity**3 / (6 * sp.sinh(intensity))
    assert normalized_factorial_one_mass(
        2,
        intensity=intensity,
        support="positive_odd",
    ) == 0


@pytest.mark.parametrize(
    ("intensity", "support", "expected"),
    [
        (sp.Rational(1, 2), "all_nonnegative", (0,)),
        (sp.Integer(1), "all_nonnegative", (0, 1)),
        (sp.Integer(5), "all_nonnegative", (4, 5)),
        (sp.Rational(1, 2), "positive", (1,)),
        (sp.Integer(1), "positive", (1,)),
        (sp.Integer(2), "positive", (1, 2)),
        (sp.Rational(5, 2), "positive", (2,)),
        (sp.Integer(5), "positive", (4, 5)),
        (sp.Integer(2), "positive_odd", (1,)),
        (sp.Rational(5, 2), "positive_odd", (3,)),
        (sp.Integer(5), "positive_odd", (5,)),
        (sp.Integer(7), "positive_odd", (7,)),
    ],
)
def test_exact_modes_and_integer_ties(
    intensity: sp.Rational,
    support: str,
    expected: tuple[int, ...],
) -> None:
    assert factorial_one_modes(  # type: ignore[arg-type]
        intensity=intensity,
        support=support,
    ) == expected

    grid = range(0, max(expected) + 12)
    values = [
        factorial_one_mass(  # type: ignore[arg-type]
            order,
            intensity=intensity,
            support=support,
        )
        for order in grid
    ]
    maximum = max(values)
    brute_modes = tuple(order for order, value in zip(grid, values) if value == maximum)
    assert brute_modes == expected


@pytest.mark.parametrize("bad_level", [-1, sp.Rational(1, 2), sp.Symbol("n")])
def test_invalid_levels_and_dimensions_are_rejected(bad_level: sp.Expr) -> None:
    with pytest.raises(ValueError):
        bosonic_fock_rung(bad_level)
    with pytest.raises(ValueError):
        truncated_bosonic_fock_ladder(bad_level)


@pytest.mark.parametrize(
    "bad_intensity",
    [0, -1, sp.Float(1), sp.Symbol("S", real=True)],
)
def test_invalid_or_inexact_mass_intensities_are_rejected(
    bad_intensity: sp.Expr | int,
) -> None:
    with pytest.raises(ValueError):
        factorial_one_mass(
            1,
            intensity=bad_intensity,
            support="positive",
        )


def test_invalid_support_modes_and_complex_scales_are_rejected() -> None:
    with pytest.raises(ValueError):
        factorial_one_mass(1, intensity=1, support="oddish")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        factorial_one_modes(intensity=sp.sqrt(2), support="positive")
    with pytest.raises(ValueError):
        bosonic_cosine_matrix_element(1, low_scale=sp.I)
