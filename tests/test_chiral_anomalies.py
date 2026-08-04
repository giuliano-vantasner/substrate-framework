import pytest
import sympy as sp

from substrate_framework.chiral_anomalies import (
    ChiralGaugeMultiplet,
    charge_conjugate_chiral_multiplet,
    chiral_anomaly_ledger,
    five_row_chiral_anomaly_ledger,
    five_row_local_anomaly_membership,
    five_row_local_anomaly_solution_variety,
)


def _displayed_charges() -> tuple[sp.Expr, ...]:
    return (
        sp.Rational(1, 6),
        -sp.Rational(2, 3),
        sp.Rational(1, 3),
        -sp.Rational(1, 2),
        sp.Integer(1),
    )


def test_displayed_five_row_table_reproduces_all_supplied_zeroes() -> None:
    ledger = five_row_chiral_anomaly_ledger(*_displayed_charges())
    assert ledger.local_coefficients == (0, 0, 0, 0, 0)
    assert ledger.factor_b_fundamental_doublet_count == 4
    assert ledger.factor_b_fundamental_doublet_parity_even
    assert ledger.all_supplied_conditions_cancel


def test_one_row_mutation_reopens_load_bearing_local_coefficients() -> None:
    charges = list(_displayed_charges())
    charges[4] = 0
    ledger = five_row_chiral_anomaly_ledger(*charges)
    assert ledger.abelian_cubed == -1
    assert ledger.mixed_gravity_squared_abelian == -1
    assert not ledger.local_anomalies_cancel


def test_common_rescaling_has_the_correct_homogeneous_degrees() -> None:
    lam = sp.symbols("lambda", real=True, nonzero=True)
    q, u, d, l, e = sp.symbols("q u d l e", real=True)
    base = five_row_chiral_anomaly_ledger(q, u, d, l, e)
    scaled = five_row_chiral_anomaly_ledger(
        lam * q,
        lam * u,
        lam * d,
        lam * l,
        lam * e,
    )
    assert sp.simplify(
        scaled.mixed_factor_a_squared_abelian
        - lam * base.mixed_factor_a_squared_abelian
    ) == 0
    assert sp.simplify(
        scaled.mixed_factor_b_squared_abelian
        - lam * base.mixed_factor_b_squared_abelian
    ) == 0
    assert sp.simplify(scaled.abelian_cubed - lam**3 * base.abelian_cubed) == 0
    assert sp.simplify(
        scaled.mixed_gravity_squared_abelian
        - lam * base.mixed_gravity_squared_abelian
    ) == 0
    assert scaled.factor_a_cubed == base.factor_a_cubed


def test_complete_elimination_retains_all_three_affine_lines() -> None:
    variety = five_row_local_anomaly_solution_variety()
    q, u, d, l, e = variety.charge_symbols
    assert variety.normalized_local_equations == (
        d + 2 * q + u,
        l + 3 * q,
        3 * d + e + 2 * l + 6 * q + 3 * u,
        3 * d**3 + e**3 + 2 * l**3 + 6 * q**3 + 3 * u**3,
    )
    assert variety.linear_solution == ((l, -3 * q), (e, 6 * q), (d, -2 * q - u))
    assert variety.reduced_cubic == 18 * q * (2 * q - u) * (4 * q + u)
    assert tuple(branch.name for branch in variety.branches) == (
        "displayed_line",
        "row_exchanged_line",
        "vectorlike_line",
    )


def test_every_parameterized_branch_annihilates_every_local_equation() -> None:
    variety = five_row_local_anomaly_solution_variety()
    for branch in variety.branches:
        membership = five_row_local_anomaly_membership(branch.charges)
        assert membership.is_solution
        assert branch.name in membership.matching_branches
        ledger = five_row_chiral_anomaly_ledger(*branch.charges)
        assert ledger.local_anomalies_cancel


def test_displayed_point_is_only_on_the_displayed_nonzero_component() -> None:
    membership = five_row_local_anomaly_membership(_displayed_charges())
    assert membership.is_solution
    assert membership.matching_branches == ("displayed_line",)


def test_row_exchanged_nonzero_solution_refutes_uniqueness_up_to_scale() -> None:
    charges = (
        sp.Rational(1, 6),
        sp.Rational(1, 3),
        -sp.Rational(2, 3),
        -sp.Rational(1, 2),
        1,
    )
    membership = five_row_local_anomaly_membership(charges)
    assert membership.is_solution
    assert membership.matching_branches == ("row_exchanged_line",)
    assert charges[1] != _displayed_charges()[1]


def test_vectorlike_line_is_not_a_rescaling_of_the_displayed_point() -> None:
    charges = (0, 1, -1, 0, 0)
    membership = five_row_local_anomaly_membership(charges)
    assert membership.is_solution
    assert membership.matching_branches == ("vectorlike_line",)
    assert charges[0] == 0 and _displayed_charges()[0] != 0


def test_origin_is_the_intersection_of_all_three_components() -> None:
    membership = five_row_local_anomaly_membership((0, 0, 0, 0, 0))
    assert membership.is_solution
    assert membership.matching_branches == (
        "displayed_line",
        "row_exchanged_line",
        "vectorlike_line",
    )


def test_global_and_cubic_nonabelian_conditions_do_not_select_charge_branch() -> None:
    for charges in (_displayed_charges(), (0, 1, -1, 0, 0)):
        ledger = five_row_chiral_anomaly_ledger(*charges)
        assert ledger.factor_a_cubed == 0
        assert ledger.factor_b_fundamental_doublet_count == 4
        assert ledger.factor_b_fundamental_doublet_parity_even


def test_chiral_conjugation_flips_odd_coefficients_but_not_quadratic_indices() -> None:
    row = ChiralGaugeMultiplet(
        "x",
        3,
        2,
        sp.Rational(1, 5),
        sp.Rational(1, 2),
        sp.Rational(1, 2),
        1,
        True,
    )
    conjugate = charge_conjugate_chiral_multiplet(row, label="x_bar")
    base = chiral_anomaly_ledger((row,))
    transformed = chiral_anomaly_ledger((conjugate,))
    assert conjugate.factor_a_quadratic_index == row.factor_a_quadratic_index
    assert conjugate.factor_b_quadratic_index == row.factor_b_quadratic_index
    assert transformed.mixed_factor_a_squared_abelian == -base.mixed_factor_a_squared_abelian
    assert transformed.mixed_factor_b_squared_abelian == -base.mixed_factor_b_squared_abelian
    assert transformed.abelian_cubed == -base.abelian_cubed
    assert transformed.mixed_gravity_squared_abelian == -base.mixed_gravity_squared_abelian
    assert transformed.factor_a_cubed == -base.factor_a_cubed
    assert (
        transformed.factor_b_fundamental_doublet_count
        == base.factor_b_fundamental_doublet_count
    )


def test_neutral_singlet_does_not_establish_carrier_completeness() -> None:
    neutral = ChiralGaugeMultiplet("n", 1, 1, 0, 0, 0, 0, False)
    charged_pair = (
        ChiralGaugeMultiplet("x", 1, 1, 1, 0, 0, 0, False),
        ChiralGaugeMultiplet("x_bar", 1, 1, -1, 0, 0, 0, False),
    )
    baseline = chiral_anomaly_ledger(charged_pair)
    extended = chiral_anomaly_ledger(charged_pair + (neutral,))
    assert extended.local_coefficients == baseline.local_coefficients
    assert extended.local_anomalies_cancel


def test_removing_one_fundamental_doublet_breaks_the_supplied_global_parity() -> None:
    half = sp.Rational(1, 2)
    rows = (
        ChiralGaugeMultiplet("Q", 3, 2, sp.Rational(1, 6), half, half, 1, True),
        ChiralGaugeMultiplet("u", 3, 1, -sp.Rational(2, 3), half, 0, -1, False),
        ChiralGaugeMultiplet("d", 3, 1, sp.Rational(1, 3), half, 0, -1, False),
    )
    ledger = chiral_anomaly_ledger(rows)
    assert ledger.factor_b_fundamental_doublet_count == 3
    assert not ledger.factor_b_fundamental_doublet_parity_even
    assert not ledger.all_supplied_conditions_cancel


def test_wrong_conjugate_cubic_sign_breaks_color_balance() -> None:
    half = sp.Rational(1, 2)
    rows = (
        ChiralGaugeMultiplet("Q", 3, 2, 0, half, half, 1, True),
        ChiralGaugeMultiplet("u_wrong", 3, 1, 0, half, 0, 1, False),
        ChiralGaugeMultiplet("d", 3, 1, 0, half, 0, -1, False),
    )
    assert chiral_anomaly_ledger(rows).factor_a_cubed == 2


@pytest.mark.parametrize(
    "table",
    [
        (),
        (ChiralGaugeMultiplet("", 1, 1, 0, 0, 0, 0, False),),
        (ChiralGaugeMultiplet("x", 0, 1, 0, 0, 0, 0, False),),
        (ChiralGaugeMultiplet("x", True, 1, 0, 0, 0, 0, False),),
        (ChiralGaugeMultiplet("x", 1, 1, 0.5, 0, 0, 0, False),),
        (ChiralGaugeMultiplet("x", 1, 1, 0, -1, 0, 0, False),),
        (ChiralGaugeMultiplet("x", 1, 1, 0, 0, 0, 0, 1),),
        (ChiralGaugeMultiplet("x", 1, 3, 0, 0, 0, 0, True),),
        (
            ChiralGaugeMultiplet("x", 1, 1, 0, 0, 0, 0, False),
            ChiralGaugeMultiplet("x", 1, 1, 0, 0, 0, 0, False),
        ),
    ],
)
def test_invalid_generic_tables_are_rejected(
    table: tuple[ChiralGaugeMultiplet, ...],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        chiral_anomaly_ledger(table)


def test_membership_and_conjugation_input_guards() -> None:
    with pytest.raises(ValueError, match="exactly five"):
        five_row_local_anomaly_membership((0, 0))
    with pytest.raises(ValueError, match="exact rather than floating"):
        five_row_local_anomaly_membership((0, 1.0, -1, 0, 0))
    with pytest.raises(ValueError, match="non-empty"):
        charge_conjugate_chiral_multiplet(
            ChiralGaugeMultiplet("x", 1, 1, 0, 0, 0, 0, False),
            label="",
        )
