from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.dirac_vacuum_polarization import (
    dirac_qed4_subtracted_timelike_evidence,
    dirac_qed4_zero_momentum_renormalization,
    dirac_representation_weight_evidence,
    dirac_vacuum_polarization_master,
    dirac_ward_integrand_evidence,
    massless_dirac_qed2_evidence,
)


def test_ward_contraction_is_derived_as_a_shifted_trace_difference() -> None:
    a, b, c, d = sp.symbols("a b c d", real=True)
    e, f, g, h = sp.symbols("e f g h", real=True)
    u, v, w, z = sp.symbols("u v w z", real=True)
    propagator_p = [[a, b], [c, d]]
    propagator_p_plus_q = [[e, f], [g, h]]
    vertex = [[u, v], [w, z]]

    evidence = dirac_ward_integrand_evidence(
        propagator_p,
        propagator_p_plus_q,
        vertex,
    )

    assert evidence.trace_cyclicity_residual == 0
    assert evidence.contracted_integrand_trace == (
        evidence.shifted_integrand_difference
    )
    assert evidence.integrated_cancellation_requires_shift_invariance


def test_wrong_inverse_propagator_sign_breaks_the_ward_integrand_identity() -> None:
    left = sp.Matrix([[2, 1], [1, 1]])
    right = sp.Matrix([[3, 1], [2, 1]])
    vertex = sp.Matrix([[1, 2], [3, 5]])
    evidence = dirac_ward_integrand_evidence(left, right, vertex)
    wrong_contraction = sp.trace(
        (right.inv() + left.inv()) * right * vertex * left
    )

    assert evidence.trace_cyclicity_residual == 0
    assert sp.simplify(
        wrong_contraction - evidence.shifted_integrand_difference
    ) != 0


def test_general_master_keeps_integration_dimension_and_spinor_trace_separate() -> None:
    dimension = sp.Symbol("d", positive=True)
    momentum2, mass2, charge = sp.symbols("Q M2 e", positive=True)
    evidence = dirac_vacuum_polarization_master(
        dimension,
        7,
        momentum2,
        mass2,
        charge,
    )
    x = evidence.parameter

    assert evidence.spinor_trace == 7
    assert sp.simplify(
        evidence.delta - (mass2 + momentum2 * x * (1 - x))
    ) == 0
    assert sp.simplify(evidence.prefactor - (
        -14
        * charge**2
        * sp.gamma(2 - dimension / 2)
        / (4 * sp.pi) ** (dimension / 2)
    )) == 0
    assert evidence.charge_squared_mass_dimension == 4 - dimension
    assert evidence.delta_power_mass_dimension == dimension - 4
    assert evidence.transverse_form_factor_mass_dimension == 0
    assert evidence.projector_coefficient_mass_dimension == 2

    doubled_trace = dirac_vacuum_polarization_master(
        dimension,
        14,
        momentum2,
        mass2,
        charge,
    )
    assert doubled_trace.parameter_integrand == evidence.parameter_integrand
    assert sp.simplify(doubled_trace.prefactor - 2 * evidence.prefactor) == 0


def test_massless_dirac_qed2_endpoint_is_finite_and_not_the_scalar_limit() -> None:
    momentum2, charge = sp.symbols("Q e", positive=True)
    evidence = massless_dirac_qed2_evidence(momentum2, charge)

    assert evidence.master.integration_dimension == 2
    assert evidence.master.spinor_trace == 2
    assert evidence.master.mass_squared == 0
    assert evidence.transverse_form_factor == -charge**2 / (
        sp.pi * momentum2
    )
    assert evidence.minkowski_projector_coefficient == charge**2 / sp.pi
    assert evidence.scalar_comparator_is_inapplicable


def test_qed4_zero_momentum_laurent_and_msbar_family_are_exact() -> None:
    charge, mass2, scale2 = sp.symbols("e M2 mu2", positive=True)
    finite = sp.Symbol("c_fin", real=True)
    epsilon = sp.Symbol("epsilon", positive=True)
    evidence = dirac_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
        finite,
        regulator=epsilon,
    )
    common = charge**2 / (12 * sp.pi**2)

    assert sp.simplify(evidence.bare_form_factor - (
        -common
        * sp.gamma(epsilon)
        * (4 * sp.pi * scale2 / mass2) ** epsilon
    )) == 0
    assert evidence.laurent_pole_residue == -common
    assert sp.simplify(
        evidence.laurent_finite_part
        - common * (sp.log(mass2 / (4 * sp.pi * scale2)) + sp.EulerGamma)
    ) == 0
    assert evidence.renormalization_residual == 0
    assert sp.simplify(
        evidence.expected_renormalized_form_factor
        - (common * sp.log(mass2 / scale2) + finite)
    ) == 0
    assert evidence.mass_squared_log_slope == common
    assert evidence.mass_log_slope == 2 * common
    assert evidence.scale_squared_log_slope == -common
    assert evidence.scale_log_slope == -2 * common


def test_finite_local_counterterm_changes_total_but_not_pole_or_log_slope() -> None:
    charge, mass2, scale2, shift = sp.symbols(
        "e M2 mu2 delta_c",
        positive=True,
    )
    base = dirac_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
        0,
    )
    changed = dirac_qed4_zero_momentum_renormalization(
        charge,
        mass2,
        scale2,
        shift,
    )

    assert changed.laurent_pole_residue == base.laurent_pole_residue
    assert changed.mass_squared_log_slope == base.mass_squared_log_slope
    assert sp.simplify(
        changed.expected_renormalized_form_factor
        - base.expected_renormalized_form_factor
        - shift
    ) == 0


def test_below_threshold_subtraction_has_exact_coefficients_and_radius() -> None:
    charge = sp.Symbol("e", positive=True)
    ratio = sp.Symbol("w", nonnegative=True)
    evidence = dirac_qed4_subtracted_timelike_evidence(charge, ratio)
    common = charge**2 / (2 * sp.pi**2)

    assert evidence.linear_coefficient == -common / 30
    assert evidence.quadratic_coefficient == -common / 280
    assert evidence.cubic_coefficient == -common / 1890
    assert sp.simplify(evidence.cubic_series - (-common * (
        ratio / 30 + ratio**2 / 280 + ratio**3 / 1890
    ))) == 0
    assert evidence.feynman_weight_maximum == sp.Rational(1, 4)
    assert evidence.first_branch_point == 4
    assert evidence.convergence_radius == 4
    assert evidence.above_threshold_requires_i0


def test_subtracted_real_api_rejects_crossing_the_pair_threshold() -> None:
    charge = sp.Symbol("e", positive=True)

    with pytest.raises(ValueError, match="0 <= w < 4"):
        dirac_qed4_subtracted_timelike_evidence(charge, -1)
    with pytest.raises(ValueError, match="0 <= w < 4"):
        dirac_qed4_subtracted_timelike_evidence(charge, 4)
    with pytest.raises(ValueError, match="0 <= w < 4"):
        dirac_qed4_subtracted_timelike_evidence(charge, 5)


def test_representation_weight_is_invariant_only_under_paired_convention_change() -> None:
    coupling, trace, rescaling = sp.symbols("g T c", positive=True)
    evidence = dirac_representation_weight_evidence(
        coupling,
        trace,
        rescaling,
    )

    assert evidence.original_loop_weight == coupling**2 * trace
    assert evidence.rescaled_coupling == coupling / rescaling
    assert evidence.rescaled_generator_trace == rescaling**2 * trace
    assert evidence.convention_residual == 0
    assert sp.simplify(
        coupling**2 * evidence.rescaled_generator_trace
        - evidence.original_loop_weight
    ) != 0


def test_dirac_vacuum_polarization_apis_reject_hidden_domain_choices() -> None:
    positive = sp.Symbol("p", positive=True)
    nonnegative = sp.Symbol("w", nonnegative=True)

    with pytest.raises(ValueError, match="integration dimension"):
        dirac_vacuum_polarization_master(0, 2, positive, 0, positive)
    with pytest.raises(TypeError, match="integer"):
        dirac_vacuum_polarization_master(2, 2.0, positive, 0, positive)
    with pytest.raises(ValueError, match="Euclidean momentum squared"):
        dirac_vacuum_polarization_master(2, 2, 0, 0, positive)
    with pytest.raises(ValueError, match="mass squared"):
        dirac_vacuum_polarization_master(2, 2, positive, -1, positive)
    with pytest.raises(ValueError, match="charge magnitude"):
        massless_dirac_qed2_evidence(positive, 0)
    with pytest.raises(ValueError, match="provably real"):
        dirac_qed4_subtracted_timelike_evidence(positive, sp.Symbol("w"))
    assert nonnegative.is_nonnegative
