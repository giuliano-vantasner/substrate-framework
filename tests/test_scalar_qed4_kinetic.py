from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.dirac_vacuum_polarization import (
    dirac_qed4_zero_momentum_renormalization,
)
from substrate_framework.gauge_beta import (
    GaugeFactor,
    ProductMultiplet,
    product_gauge_coefficients,
)
from substrate_framework.vacuum_polarization import (
    matter_induced_kinetic_evidence,
    scalar_qed4_zero_momentum_renormalization,
    scalar_vacuum_polarization_master,
    scalar_ward_integrand_evidence,
)


def test_scalar_ward_identity_uses_bubble_and_seagull() -> None:
    evidence = scalar_ward_integrand_evidence()

    assert evidence.denominator_difference_residual == 0
    assert evidence.shifted_bubble_numerator_difference == 2 * evidence.transfer_component
    assert evidence.shifted_bubble_contraction != 0
    assert evidence.seagull_contraction == -evidence.shifted_bubble_contraction
    assert evidence.integrated_ward_residual == 0
    assert evidence.integrated_cancellation_requires_shift_invariance


def test_wrong_seagull_sign_breaks_scalar_ward_identity() -> None:
    evidence = scalar_ward_integrand_evidence()
    wrong_residual = sp.simplify(
        evidence.shifted_bubble_contraction - evidence.seagull_contraction
    )

    assert wrong_residual != 0


def test_scalar_master_has_complete_weight_and_dimension_ledger() -> None:
    dimension = sp.Symbol("d", positive=True)
    momentum2, mass2, charge = sp.symbols("Q M2 e", positive=True)
    evidence = scalar_vacuum_polarization_master(
        dimension,
        momentum2,
        mass2,
        charge,
        species_count=3,
    )
    x = evidence.parameter

    assert evidence.species_count == 3
    assert evidence.parameter_weight == 4 * x**2 - 4 * x + 1
    assert sp.simplify(evidence.delta - (mass2 + x * (1 - x) * momentum2)) == 0
    assert sp.simplify(evidence.prefactor - (
        -3
        * charge**2
        * sp.gamma(2 - dimension / 2)
        / (4 * sp.pi) ** (dimension / 2)
    )) == 0
    assert evidence.charge_squared_mass_dimension == 4 - dimension
    assert evidence.delta_power_mass_dimension == dimension - 4
    assert evidence.transverse_form_factor_mass_dimension == 0


def test_scalar_qed4_laurent_msbar_and_beta_are_exact() -> None:
    charge, mass2, scale2 = sp.symbols("e M2 mu2", positive=True)
    finite = sp.Symbol("c_fin", real=True)
    epsilon = sp.Symbol("epsilon", positive=True)
    evidence = scalar_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
        finite,
        species_count=2,
        regulator=epsilon,
    )
    common = charge**2 / (24 * sp.pi**2)

    assert evidence.parameter_weight_integral == sp.Rational(1, 3)
    assert sp.simplify(evidence.bare_form_factor - (
        -common
        * sp.gamma(epsilon)
        * (4 * sp.pi * scale2 / mass2) ** epsilon
    )) == 0
    assert evidence.laurent_pole_residue == -common
    assert evidence.renormalization_residual == 0
    assert sp.simplify(
        evidence.expected_renormalized_form_factor
        - (common * sp.log(mass2 / scale2) + finite)
    ) == 0
    assert evidence.mass_squared_log_slope == common
    assert evidence.mass_log_slope == 2 * common
    assert evidence.scale_squared_log_slope == -common
    assert evidence.scale_log_slope == -2 * common
    assert evidence.beta_coupling == charge**3 / (24 * sp.pi**2)
    assert evidence.connection_inverse_coupling_scale_slope == -1 / (
        12 * sp.pi**2
    )
    assert evidence.complex_scalar_matter_weight == sp.Rational(2, 3)


def test_scalar_and_dirac_slopes_have_exact_factor_four() -> None:
    charge, mass2, scale2 = sp.symbols("e M2 mu2", positive=True)
    scalar = scalar_qed4_zero_momentum_renormalization(charge, mass2, scale2)
    dirac = dirac_qed4_zero_momentum_renormalization(charge, mass2, scale2)

    assert sp.simplify(
        dirac.mass_squared_log_slope / scalar.mass_squared_log_slope
    ) == 4
    assert sp.simplify(
        dirac.scale_log_slope / scalar.scale_log_slope
    ) == 4


def test_derived_weights_match_the_accepted_generic_beta_ledger() -> None:
    scalar_weight, dirac_weight = sp.symbols("W_s W_f", nonnegative=True)
    ledger = product_gauge_coefficients(
        [GaugeFactor("u1", 0, is_abelian=True)],
        [
            ProductMultiplet("scalar", "complex_scalar", 1, (scalar_weight,), (0,)),
            ProductMultiplet("dirac_as_two_weyl", "weyl_fermion", 2, (dirac_weight,), (0,)),
        ],
    )
    evidence = matter_induced_kinetic_evidence(
        1,
        2,
        0,
        0,
        scalar_weight,
        dirac_weight,
    )

    assert ledger.one_loop_gauge == (0,)
    assert ledger.one_loop[0] == evidence.one_loop_coefficient
    assert evidence.scalar_coefficient == scalar_weight / 3
    assert evidence.dirac_coefficient == 4 * dirac_weight / 3


def test_affine_kinetic_family_retains_boundary_and_flow() -> None:
    scale, reference = sp.symbols("mu mu_ref", positive=True)
    local, finite = sp.symbols("Z_local c_fin", real=True)
    scalar_weight, dirac_weight = sp.symbols("W_s W_f", nonnegative=True)
    evidence = matter_induced_kinetic_evidence(
        scale,
        reference,
        local,
        finite,
        scalar_weight,
        dirac_weight,
    )
    expected_b = scalar_weight / 3 + 4 * dirac_weight / 3

    assert evidence.one_loop_coefficient == expected_b
    assert evidence.reference_value == local + finite
    assert sp.simplify(
        evidence.kinetic_coefficient
        - (local + finite + expected_b * sp.log(reference / scale) / (8 * sp.pi**2))
    ) == 0
    assert evidence.flow_residual == 0


def test_same_slope_allows_unequal_boundaries() -> None:
    evidence = matter_induced_kinetic_evidence(1, 2, 3, 5, 1, 1)
    formal_scale = evidence.formal_running_scale

    assert evidence.boundary_mutation_residual == 0
    assert sp.simplify(
        formal_scale
        * sp.diff(
            evidence.formal_kinetic_coefficient + evidence.boundary_mutation,
            formal_scale,
        )
        + evidence.running_coefficient
    ) == 0
    assert sp.simplify(
        evidence.boundary_mutated_kinetic_coefficient
        - evidence.kinetic_coefficient
    ) == evidence.boundary_mutation


def test_zero_matching_positivity_does_not_extend_to_general_boundary() -> None:
    zero_uv_above = matter_induced_kinetic_evidence(1, 2, 0, 0, 1, 0)
    zero_uv_below = matter_induced_kinetic_evidence(2, 1, 0, 0, 1, 0)
    positive_offset = matter_induced_kinetic_evidence(2, 1, 10, 0, 1, 0)
    negative_offset = matter_induced_kinetic_evidence(1, 2, -10, 0, 1, 0)

    assert zero_uv_above.zero_matching_kinetic_coefficient.is_positive is True
    assert zero_uv_below.zero_matching_kinetic_coefficient.is_negative is True
    assert positive_offset.kinetic_coefficient.is_positive is True
    assert negative_offset.kinetic_coefficient.is_negative is True
    assert zero_uv_above.zero_matching_is_separate_premise


def test_scheme_and_reference_coordinate_changes_preserve_total() -> None:
    evidence = matter_induced_kinetic_evidence(1, 2, 3, 5, 1, 1)

    assert evidence.scheme_decomposition_residual == 0
    assert evidence.reference_covariance_residual == 0
    assert evidence.transformed_reference_value != evidence.reference_value


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: scalar_qed4_zero_momentum_renormalization(0, 1, 1),
            "charge magnitude",
        ),
        (
            lambda: scalar_qed4_zero_momentum_renormalization(1, 0, 1),
            "mass squared",
        ),
        (
            lambda: scalar_qed4_zero_momentum_renormalization(1, 1, 1, species_count=0),
            "species count",
        ),
        (
            lambda: matter_induced_kinetic_evidence(0, 1, 0, 0, 1, 0),
            "scale",
        ),
        (
            lambda: matter_induced_kinetic_evidence(1, 1, 0, 0, -1, 0),
            "scalar weight",
        ),
        (
            lambda: matter_induced_kinetic_evidence(1, 1, sp.Float(1), 0, 1, 0),
            "exact",
        ),
    ],
)
def test_scalar_qed4_and_boundary_APIs_reject_hidden_domain_choices(
    call,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        call()
