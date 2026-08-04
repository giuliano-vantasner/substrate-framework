import pytest
import sympy as sp

from substrate_framework.multiplet_charges import (
    ChargeMultiplet,
    charge_conjugate_multiplet,
    finite_multiplet_charge_ledger,
    infer_common_abelian_charge,
    multiplet_abelian_normalization_ledger,
)


def _supplied_five_row_table() -> tuple[ChargeMultiplet, ...]:
    return (
        ChargeMultiplet("Q_L", 3, (sp.Rational(1, 2), -sp.Rational(1, 2)), sp.Rational(1, 6)),
        ChargeMultiplet("u_R", 3, (0,), sp.Rational(2, 3)),
        ChargeMultiplet("d_R", 3, (0,), -sp.Rational(1, 3)),
        ChargeMultiplet("L", 1, (sp.Rational(1, 2), -sp.Rational(1, 2)), -sp.Rational(1, 2)),
        ChargeMultiplet("e_R", 1, (0,), -1),
    )


def test_supplied_five_row_table_has_exact_spectra_and_fifteen_states() -> None:
    ledger = finite_multiplet_charge_ledger(_supplied_five_row_table())
    assert tuple(spectrum.electric_charges for spectrum in ledger.spectra) == (
        (sp.Rational(2, 3), -sp.Rational(1, 3)),
        (sp.Rational(2, 3),),
        (-sp.Rational(1, 3),),
        (0, -1),
        (-1,),
    )
    assert ledger.state_count == 15
    assert ledger.trace_ledger.state_count == 15


def test_supplied_table_composes_the_accepted_flattened_trace_ledger() -> None:
    trace = finite_multiplet_charge_ledger(_supplied_five_row_table()).trace_ledger
    assert trace.trace_t3_squared == 2
    assert trace.trace_abelian_squared == sp.Rational(10, 3)
    assert trace.trace_cross == 0
    assert trace.trace_electric_squared == sp.Rational(16, 3)
    assert trace.trace_ratio == sp.Rational(3, 8)
    assert trace.decomposition_residual == 0


def test_target_spectrum_inversion_is_unique_only_inside_the_supplied_weights() -> None:
    quarks = infer_common_abelian_charge(
        (sp.Rational(1, 2), -sp.Rational(1, 2)),
        (sp.Rational(2, 3), -sp.Rational(1, 3)),
    )
    assert quarks.consistent
    assert quarks.candidate_abelian_charge == sp.Rational(1, 6)
    assert quarks.residuals == (0, 0)

    inconsistent = infer_common_abelian_charge(
        (sp.Rational(1, 2), -sp.Rational(1, 2)),
        (sp.Rational(2, 3), sp.Rational(2, 3)),
    )
    assert not inconsistent.consistent
    assert inconsistent.residuals[1] != 0


def test_alternative_target_spectrum_has_an_equally_exact_alternative_charge() -> None:
    alternative = infer_common_abelian_charge(
        (sp.Rational(1, 2), -sp.Rational(1, 2)),
        (sp.Rational(3, 2), sp.Rational(1, 2)),
    )
    assert alternative.consistent
    assert alternative.candidate_abelian_charge == 1
    assert alternative.reconstruction == (sp.Rational(3, 2), sp.Rational(1, 2))


def test_factor_two_convention_map_preserves_charges_and_coupled_coordinates() -> None:
    g = sp.Symbol("g", positive=True)
    mapping = multiplet_abelian_normalization_ledger(
        _supplied_five_row_table(),
        2,
        g,
    )
    assert mapping.rescaled_electric_coefficient == sp.Rational(1, 2)
    assert mapping.rescaled_abelian_coupling == g / 2
    assert mapping.rescaled_multiplets[0].abelian_charge == sp.Rational(1, 3)
    assert all(residual == 0 for row in mapping.charge_residuals for residual in row)
    assert mapping.covariant.trace_ledger.trace_electric_squared == sp.Rational(16, 3)
    assert mapping.flattened_normalization.coupled_trace_norm_residual == 0
    assert mapping.fixed_coefficient.spectra[0].electric_charges != (
        sp.Rational(2, 3),
        -sp.Rational(1, 3),
    )


def test_charge_conjugation_negates_weights_abelian_values_and_spectrum() -> None:
    original = _supplied_five_row_table()[0]
    conjugate = charge_conjugate_multiplet(original, label="Q_L_conj")
    base = finite_multiplet_charge_ledger((original,)).spectra[0]
    transformed = finite_multiplet_charge_ledger((conjugate,)).spectra[0]
    assert conjugate.spectator_multiplicity == original.spectator_multiplicity
    assert conjugate.t3_weights == tuple(-weight for weight in original.t3_weights)
    assert conjugate.abelian_charge == -original.abelian_charge
    assert transformed.electric_charges == tuple(-charge for charge in base.electric_charges)


def test_fifteen_is_a_supplied_table_count_not_a_completeness_theorem() -> None:
    baseline = finite_multiplet_charge_ledger(_supplied_five_row_table())
    missing_electron = finite_multiplet_charge_ledger(_supplied_five_row_table()[:-1])
    with_neutral_singlet = finite_multiplet_charge_ledger(
        _supplied_five_row_table() + (ChargeMultiplet("neutral_R", 1, (0,), 0),)
    )
    assert baseline.state_count == 15
    assert missing_electron.state_count == 14
    assert with_neutral_singlet.state_count == 16
    assert with_neutral_singlet.spectra[-1].electric_charges == (0,)


@pytest.mark.parametrize(
    "table",
    [
        (),
        (ChargeMultiplet("", 1, (0,), 0),),
        (ChargeMultiplet("x", 0, (0,), 0),),
        (ChargeMultiplet("x", True, (0,), 0),),
        (ChargeMultiplet("x", 1, (), 0),),
        (ChargeMultiplet("x", 1, (0.5,), 0),),
        (ChargeMultiplet("x", 1, (0,), 0.5),),
        (ChargeMultiplet("x", 1, (0,), 0), ChargeMultiplet("x", 1, (0,), 1)),
    ],
)
def test_invalid_multiplet_tables_are_rejected(table: tuple[ChargeMultiplet, ...]) -> None:
    with pytest.raises((TypeError, ValueError)):
        finite_multiplet_charge_ledger(table)


def test_inversion_and_conjugation_input_guards() -> None:
    with pytest.raises(ValueError, match="equal nonzero length"):
        infer_common_abelian_charge((0,), ())
    with pytest.raises(ValueError, match="provably nonzero"):
        infer_common_abelian_charge((0,), (1,), electric_coefficient=0)
    with pytest.raises(ValueError, match="non-empty"):
        charge_conjugate_multiplet(_supplied_five_row_table()[0], label="")
    with pytest.raises(ValueError, match="positive"):
        multiplet_abelian_normalization_ledger(_supplied_five_row_table(), -1, 1)
