from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.explicit_breaking import (
    conditional_gmor_evidence,
    matched_local_curvature_potentials,
    periodic_potential_evidence,
    su2_trace_breaking_evidence,
)


def test_periodic_potential_derives_series_curvature_and_generalized_mass() -> None:
    field = sp.Symbol("phi", real=True)
    amplitude, scale, kinetic = sp.symbols("A F K", positive=True)
    evidence = periodic_potential_evidence(field, amplitude, scale, kinetic)
    assert evidence.value_at_origin == 0
    assert evidence.slope_at_origin == 0
    assert evidence.period == 2 * sp.pi * scale
    assert evidence.curvature_at_origin == amplitude / scale**2
    assert evidence.fourth_derivative_at_origin == -amplitude / scale**4
    assert evidence.sixth_order_series == (
        amplitude * field**2 / (2 * scale**2)
        - amplitude * field**4 / (24 * scale**4)
        + amplitude * field**6 / (720 * scale**6)
    )
    assert evidence.generalized_mass_squared == amplitude / (kinetic * scale**2)


def test_equal_local_curvature_does_not_identify_global_potential() -> None:
    field = sp.Symbol("phi", real=True)
    curvature, scale = sp.symbols("h F", positive=True)
    evidence = matched_local_curvature_potentials(field, curvature, scale)
    assert evidence.hessian_difference_at_origin == 0
    assert evidence.periodic_shift_residual == 0
    assert evidence.quadratic_shift_residual != 0
    assert evidence.fourth_derivative_difference_at_origin == -curvature / scale**2
    assert evidence.periodic_potential != evidence.quadratic_potential


def test_skyrme_trace_and_kinetic_prefactors_give_coordinate_covariant_mass() -> None:
    field = sp.Symbol("pi", real=True)
    scale, mass = sp.symbols("F_pi m_pi", positive=True)
    half_coordinate = su2_trace_breaking_evidence(
        field,
        scale,
        1,
        scale**2 / 16,
        mass**2 * scale**2 / 8,
    )
    canonical_coordinate = su2_trace_breaking_evidence(
        field,
        scale,
        2,
        scale**2 / 16,
        mass**2 * scale**2 / 8,
    )
    assert half_coordinate.trace_u_minus_identity == 2 * sp.cos(field / scale) - 2
    assert half_coordinate.kinetic_coefficient == sp.Rational(1, 4)
    assert half_coordinate.potential_curvature == mass**2 / 4
    assert half_coordinate.generalized_mass_squared == mass**2
    assert canonical_coordinate.trace_u_minus_identity == (
        2 * sp.cos(2 * field / scale) - 2
    )
    assert canonical_coordinate.kinetic_coefficient == 1
    assert canonical_coordinate.potential_curvature == mass**2
    assert canonical_coordinate.generalized_mass_squared == mass**2
    assert half_coordinate.generalized_mass_coordinate_residual == 0
    assert canonical_coordinate.generalized_mass_coordinate_residual == 0


def test_pg2_mixed_normalization_changes_the_generalized_mass_by_four() -> None:
    field = sp.Symbol("pi", real=True)
    scale, mass = sp.symbols("F_pi m_pi", positive=True)
    pg2_potential = periodic_potential_evidence(
        field,
        mass**2 * scale**2,
        scale,
        sp.Rational(1, 4),
    )
    trace_pair = su2_trace_breaking_evidence(
        field,
        scale,
        1,
        scale**2 / 16,
        mass**2 * scale**2 / 8,
    )
    assert pg2_potential.curvature_at_origin == mass**2
    assert pg2_potential.generalized_mass_squared == 4 * mass**2
    assert trace_pair.generalized_mass_squared == mass**2
    required_trace_prefactor = pg2_potential.amplitude / 2
    assert (
        sp.simplify(required_trace_prefactor / trace_pair.lagrangian_trace_prefactor)
        == 4
    )


def test_conditional_gmor_exposes_scaling_and_continuous_free_input_family() -> None:
    mass_sum, decay_scale, factor = sp.symbols("m_q F c", positive=True)
    condensate = sp.Symbol("Sigma", negative=True)
    evidence = conditional_gmor_evidence(
        mass_sum,
        condensate,
        decay_scale,
        convention_factor=factor,
    )
    assert evidence.mass_squared == -factor * mass_sum * condensate / decay_scale**2
    assert evidence.relation_residual == 0
    assert evidence.quark_mass_log_exponent == 1
    assert evidence.condensate_log_exponent == 1
    assert evidence.decay_scale_log_exponent == -2
    assert evidence.convention_factor_log_exponent == 1
    assert evidence.zero_quark_mass_limit == 0
    assert evidence.scale_condensate_degeneracy_residual == 0
    assert evidence.mass_squared.is_positive is True


def test_sign_and_normalization_mutations_change_load_bearing_results() -> None:
    field = sp.Symbol("phi", real=True)
    amplitude, scale = sp.symbols("A F", positive=True)
    positive = periodic_potential_evidence(field, amplitude, scale, 1)
    negative = periodic_potential_evidence(field, -amplitude, scale, 1)
    rescaled_kinetic = periodic_potential_evidence(field, amplitude, scale, 4)
    assert positive.generalized_mass_squared == amplitude / scale**2
    assert negative.generalized_mass_squared == -amplitude / scale**2
    assert rescaled_kinetic.generalized_mass_squared == amplitude / (4 * scale**2)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: periodic_potential_evidence(sp.Symbol("x"), 1, 0, 1),
            "coordinate scale",
        ),
        (
            lambda: periodic_potential_evidence(sp.Symbol("x"), 1, 1, -1),
            "kinetic coefficient",
        ),
        (
            lambda: su2_trace_breaking_evidence(sp.Symbol("x"), 1, 1, -1, 1),
            "kinetic prefactor",
        ),
        (
            lambda: conditional_gmor_evidence(0, -1, 1),
            "quark mass sum",
        ),
    ],
)
def test_unproved_or_invalid_normalizations_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
