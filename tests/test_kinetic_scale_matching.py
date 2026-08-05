from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.kinetic_scale_matching import (
    inverse_length_scale_kinetic_evidence,
    one_loop_scale_matched_kinetic_evidence,
)


def test_arbitrary_length_map_retains_unequal_conversion_ratio() -> None:
    ell0, ell1, k0, k1 = sp.symbols("ell0 ell1 K0 K1", positive=True)
    local, finite = sp.symbols("Z_local c_fin", real=True)
    scalar, dirac = sp.symbols("W_s W_f", nonnegative=True)
    evidence = inverse_length_scale_kinetic_evidence(
        ell0,
        ell1,
        k0,
        k1,
        local,
        finite,
        scalar,
        dirac,
    )

    assert evidence.reference_energy == k0 / ell0
    assert evidence.evaluation_energy == k1 / ell1
    assert evidence.evaluation_to_reference_length_ratio == ell1 / ell0
    assert evidence.evaluation_to_reference_conversion_ratio == k1 / k0
    assert evidence.reference_to_evaluation_energy_ratio == k0 * ell1 / (k1 * ell0)
    assert evidence.energy_length_ratio_residual == 0
    assert evidence.scale_logarithm == sp.log(k0 * ell1 / (k1 * ell0))


def test_affine_boundary_survives_scale_composition() -> None:
    local, finite = sp.symbols("Z_local c_fin", real=True)
    scalar, dirac = sp.symbols("W_s W_f", nonnegative=True)
    evidence = inverse_length_scale_kinetic_evidence(
        2,
        7,
        3,
        5,
        local,
        finite,
        scalar,
        dirac,
    )
    coefficient = scalar / 3 + 4 * dirac / 3

    assert evidence.kinetic.reference_value == local + finite
    assert sp.simplify(
        evidence.kinetic.kinetic_coefficient
        - local
        - finite
        - coefficient * sp.log(sp.Rational(21, 10)) / (8 * sp.pi**2)
    ) == 0
    assert evidence.affine_composition_residual == 0
    assert evidence.kinetic.zero_matching_is_separate_premise


def test_fixed_length_conversion_mutation_changes_log_and_total() -> None:
    baseline = inverse_length_scale_kinetic_evidence(2, 10, 3, 5, 1, 0, 1, 0)
    mutated = inverse_length_scale_kinetic_evidence(2, 10, 6, 5, 1, 0, 1, 0)

    assert sp.simplify(mutated.scale_logarithm - baseline.scale_logarithm) == sp.log(2)
    assert mutated.kinetic.kinetic_coefficient != baseline.kinetic.kinetic_coefficient


def test_common_length_rescaling_preserves_log_but_not_absolute_energies() -> None:
    evidence = inverse_length_scale_kinetic_evidence(2, 10, 3, 5, 1, 0, 1, 0)

    assert evidence.common_rescaling_log_residual == 0
    assert evidence.rescaled_reference_energy == (
        evidence.reference_energy / evidence.common_length_rescaling
    )
    assert evidence.rescaled_evaluation_energy == (
        evidence.evaluation_energy / evidence.common_length_rescaling
    )


def test_consistent_one_loop_pairing_cancels_unequal_conversions() -> None:
    mu0, g2, b0 = sp.symbols("mu0 g2 b0", positive=True)
    k0, k1 = sp.symbols("K0 K1", positive=True)
    local, finite = sp.symbols("Z_local c_fin", real=True)
    scalar, dirac = sp.symbols("W_s W_f", positive=True)
    evidence = one_loop_scale_matched_kinetic_evidence(
        mu0,
        g2,
        b0,
        reference_conversion=k0,
        transmuted_conversion=k1,
        renormalized_local_coefficient=local,
        finite_matching_offset=finite,
        scalar_weight=scalar,
        dirac_weight=dirac,
    )
    coefficient = scalar / 3 + 4 * dirac / 3

    assert evidence.transmutation.transmuted_to_reference_length_ratio == (
        k1 * sp.exp(8 * sp.pi**2 / (b0 * g2)) / k0
    )
    assert evidence.matched.scale_logarithm == 8 * sp.pi**2 / (b0 * g2)
    assert evidence.scale_log_cancellation_residual == 0
    assert sp.simplify(
        evidence.general_kinetic_coefficient
        - local
        - finite
        - coefficient / (b0 * g2)
    ) == 0
    assert evidence.general_kinetic_residual == 0
    assert evidence.conversion_factors_need_not_be_equal


def test_zero_matching_inverse_is_conditional_and_exact() -> None:
    g2, b0, scalar, dirac = sp.symbols("g2 b0 W_s W_f", positive=True)
    evidence = one_loop_scale_matched_kinetic_evidence(
        11,
        g2,
        b0,
        reference_conversion=2,
        transmuted_conversion=7,
        renormalized_local_coefficient=3,
        finite_matching_offset=5,
        scalar_weight=scalar,
        dirac_weight=dirac,
    )
    coefficient = scalar / 3 + 4 * dirac / 3

    assert sp.simplify(
        evidence.zero_matching_kinetic_coefficient - coefficient / (b0 * g2)
    ) == 0
    assert evidence.zero_matching_residual == 0
    assert sp.simplify(
        evidence.zero_matching_inverse_kinetic_coordinate - b0 * g2 / coefficient
    ) == 0
    assert evidence.zero_matching_inverse_residual == 0
    assert evidence.general_kinetic_coefficient != evidence.zero_matching_kinetic_coefficient
    assert evidence.zero_matching_is_separate_premise
    assert evidence.physical_coupling_interpretation_is_separate_premise


def test_paired_conversion_changes_do_not_change_one_loop_log() -> None:
    first = one_loop_scale_matched_kinetic_evidence(
        13,
        2,
        3,
        reference_conversion=5,
        transmuted_conversion=7,
        renormalized_local_coefficient=0,
        finite_matching_offset=0,
        scalar_weight=1,
        dirac_weight=0,
    )
    second = one_loop_scale_matched_kinetic_evidence(
        13,
        2,
        3,
        reference_conversion=11,
        transmuted_conversion=17,
        renormalized_local_coefficient=0,
        finite_matching_offset=0,
        scalar_weight=1,
        dirac_weight=0,
    )

    assert first.matched.scale_logarithm == second.matched.scale_logarithm
    assert first.zero_matching_kinetic_coefficient == second.zero_matching_kinetic_coefficient
    assert first.transmutation.reference_length != second.transmutation.reference_length


def test_reversing_only_the_length_orientation_changes_the_generic_log() -> None:
    forward = inverse_length_scale_kinetic_evidence(2, 10, 3, 5, 0, 0, 1, 0)
    reversed_lengths = inverse_length_scale_kinetic_evidence(10, 2, 3, 5, 0, 0, 1, 0)

    assert forward.scale_logarithm != reversed_lengths.scale_logarithm
    assert sp.simplify(
        forward.reference_to_evaluation_energy_ratio
        * reversed_lengths.reference_to_evaluation_energy_ratio
        - sp.Rational(9, 25)
    ) == 0


def test_zero_matter_family_exists_but_inverse_branch_rejects_it() -> None:
    general = inverse_length_scale_kinetic_evidence(1, 2, 1, 1, 3, 5, 0, 0)
    assert general.kinetic.one_loop_coefficient == 0
    assert general.kinetic.kinetic_coefficient == 8
    assert general.kinetic.zero_matching_kinetic_coefficient == 0

    with pytest.raises(ValueError, match="total matter coefficient"):
        one_loop_scale_matched_kinetic_evidence(
            1,
            2,
            3,
            reference_conversion=1,
            transmuted_conversion=1,
            renormalized_local_coefficient=0,
            finite_matching_offset=0,
            scalar_weight=0,
            dirac_weight=0,
        )


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: inverse_length_scale_kinetic_evidence(0, 1, 1, 1, 0, 0, 1, 0),
            "reference length",
        ),
        (
            lambda: inverse_length_scale_kinetic_evidence(1, 1, 1, -1, 0, 0, 1, 0),
            "evaluation conversion",
        ),
        (
            lambda: one_loop_scale_matched_kinetic_evidence(
                sp.Float(1),
                2,
                3,
                reference_conversion=1,
                transmuted_conversion=1,
                renormalized_local_coefficient=0,
                finite_matching_offset=0,
                scalar_weight=1,
                dirac_weight=0,
            ),
            "exact",
        ),
        (
            lambda: one_loop_scale_matched_kinetic_evidence(
                1,
                0,
                3,
                reference_conversion=1,
                transmuted_conversion=1,
                renormalized_local_coefficient=0,
                finite_matching_offset=0,
                scalar_weight=1,
                dirac_weight=0,
            ),
            "coupling squared",
        ),
    ],
)
def test_scale_matching_rejects_hidden_domain_choices(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()


def test_scale_matching_module_has_no_numpy_quadrature_surface() -> None:
    source = Path("src/substrate_framework/kinetic_scale_matching.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source
