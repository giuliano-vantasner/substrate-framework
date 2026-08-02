from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.wzw import (
    alternating_trace,
    antihermitian_generators,
    antihermitian_structure_constants,
    chevalley_eilenberg_differential,
    cochain_basis,
    extension_phase_ratio,
    glued_filling_period,
    hedgehog_winding_charge,
    hedgehog_winding_density,
    hedgehog_winding_radial_density,
    maurer_cartan_power_derivative_multiplier,
    sphere_extension_coefficient,
    sphere_extension_phase_ratio,
    su2_quaternion_column_projection_jacobian,
    su2_quaternion_embedding,
    su2_quaternion_embedding_differential,
    su2_quaternion_trace_three_period,
    su3_pi5_generator,
    su3_pi5_period_evidence,
    su3_real_trace_five_cochain,
    su3_sphere_trace_five_period,
    su3_trace_five_cohomology,
    su3_trace_power_cochain,
    su3_winding_current,
    su3_winding_current_coefficient,
    su3_winding_three_evidence,
    trace_power_cyclic_shift_sign,
    trace_power_derivative_multiplier,
)


def test_antihermitian_basis_matches_accepted_su3_convention() -> None:
    generators = antihermitian_generators()
    constants = antihermitian_structure_constants()
    assert all(generator.H == -generator for generator in generators)
    assert all(sp.trace(generator) == 0 for generator in generators)
    assert sp.trace(generators[0] * generators[0]) == -sp.Rational(1, 2)
    assert constants[0][1][2] == -1
    assert generators[0] * generators[1] - generators[1] * generators[0] == sum(
        (constants[0][1][index] * generators[index] for index in range(8)),
        sp.zeros(3),
    )


def test_trace_five_cochain_is_exactly_real_and_nonzero() -> None:
    raw = su3_trace_power_cochain(5)
    real = su3_real_trace_five_cochain()
    basis = cochain_basis(5)
    component = basis.index((0, 1, 2, 3, 4))
    assert raw == sp.I * real
    assert real[component] == -sp.Rational(15, 8)
    assert sum(value != 0 for value in real) == 9
    assert sp.simplify((real.T * real)[0]) == sp.Rational(75, 4)


def test_even_trace_power_guard_is_rejected_exactly() -> None:
    trace_four = su3_trace_power_cochain(4)
    trace_five = su3_trace_power_cochain(5)
    assert trace_four == sp.zeros(len(cochain_basis(4)), 1)
    assert trace_five != sp.zeros(len(cochain_basis(5)), 1)
    assert trace_power_cyclic_shift_sign(4) == -1
    assert trace_power_cyclic_shift_sign(5) == 1
    assert trace_power_derivative_multiplier(4) == 0
    assert trace_power_derivative_multiplier(5) == 5
    assert maurer_cartan_power_derivative_multiplier(4) == 0
    assert maurer_cartan_power_derivative_multiplier(5) == -1
    assert trace_power_derivative_multiplier(4) * trace_five == sp.zeros(
        len(cochain_basis(5)), 1
    )
    assert -4 * trace_five != sp.zeros(len(cochain_basis(5)), 1)


def test_exact_ce_complex_and_trace_five_cohomology() -> None:
    d4 = chevalley_eilenberg_differential(4)
    d5 = chevalley_eilenberg_differential(5)
    omega = su3_real_trace_five_cochain()
    evidence = su3_trace_five_cohomology()
    assert d5 * d4 == sp.zeros(28, 70)
    assert d5 * omega == sp.zeros(28, 1)
    assert evidence.differential_squares_to_zero
    assert evidence.trace_is_closed
    assert not evidence.trace_is_exact
    assert evidence.d4_rank == 35
    assert evidence.d5_rank == 20
    assert evidence.five_cocycle_dimension == 36
    assert evidence.fifth_cohomology_dimension == 1
    assert evidence.augmented_d4_trace_rank == 36


def test_trace_cochain_itself_separates_the_coboundary_image() -> None:
    d4 = chevalley_eilenberg_differential(4)
    omega = su3_real_trace_five_cochain()
    evidence = su3_trace_five_cohomology()
    assert omega.T * d4 == sp.zeros(1, 70)
    assert (omega.T * omega)[0] == sp.Rational(75, 4)
    assert evidence.trace_annihilates_coboundaries
    assert evidence.dual_separating_pairing == sp.Rational(75, 4)


def test_filling_gluing_and_phase_are_explicitly_conditional() -> None:
    first, second, coefficient = sp.symbols("I_B I_Bprime k", real=True)
    assert glued_filling_period(first, second) == first - second
    assert glued_filling_period(second, first) == -(first - second)
    assert extension_phase_ratio(coefficient, first, second) == sp.exp(
        sp.I * coefficient * (first - second)
    )
    integer_level = sp.Symbol("k", integer=True)
    integer_period = sp.Symbol("n", integer=True)
    assert extension_phase_ratio(
        integer_level, 2 * sp.pi * integer_period, 0
    ) == 1


def test_explicit_pi5_map_is_exactly_su3_on_the_unit_sphere() -> None:
    z1, z2, z3, w1, w2, w3 = sp.symbols("z1 z2 z3 w1 w2 w3")
    eta = su3_pi5_generator((z1, z2, z3)).xreplace(
        {sp.conjugate(z1): w1, sp.conjugate(z2): w2, sp.conjugate(z3): w3}
    )
    eta_adjoint = eta.T.xreplace(
        {z1: w1, z2: w2, z3: w3, w1: z1, w2: z2, w3: z3}
    )
    norm_squared = w1 * z1 + w2 * z2 + w3 * z3
    gram_residual = sp.expand(eta_adjoint * eta - sp.eye(3))
    assert sp.factor(eta.det()) == norm_squared**2
    z = sp.Matrix([z1, z2, z3])
    w = sp.Matrix([w1, w2, w3])
    assert gram_residual == sp.expand((norm_squared - 1) * (sp.eye(3) + w * z.T))
    assert su3_pi5_generator((1, 0, 0)).det() == 1


def test_generator_degree_is_independent_of_trace_period() -> None:
    evidence = su3_pi5_period_evidence()
    assert evidence.positive_preimage_jacobian == 8
    assert evidence.negative_preimage_jacobian == 8
    assert evidence.projection_degree == 2
    assert evidence.projection_degree != evidence.real_trace_density


def test_exact_pi5_period_has_no_hidden_factorial_or_factor_two() -> None:
    evidence = su3_pi5_period_evidence()
    assert evidence.raw_trace_density == -480 * sp.I
    assert evidence.real_trace_density == -480
    assert evidence.sphere_volume == sp.pi**3
    assert evidence.raw_trace_period == -480 * sp.I * sp.pi**3
    assert evidence.real_trace_period == -480 * sp.pi**3
    assert evidence.primitive_period_magnitude == 480 * sp.pi**3
    assert evidence.coefficient_lattice_step == 1 / (240 * sp.pi**2)
    assert su3_sphere_trace_five_period(-1) == 480 * sp.pi**3
    assert su3_sphere_trace_five_period(2) == -960 * sp.pi**3


def test_sphere_extension_level_lattice_and_mutations() -> None:
    level = sp.Symbol("level", integer=True)
    winding = sp.Symbol("winding", integer=True)
    assert sphere_extension_coefficient(level) == level / (240 * sp.pi**2)
    assert sphere_extension_phase_ratio(level, winding) == 1
    assert sphere_extension_phase_ratio(sp.Rational(1, 2), 1) == -1
    assert sp.simplify(
        sp.exp(
            sp.I
            * sphere_extension_coefficient(1)
            * (su3_sphere_trace_five_period(1) / 2)
        )
        + 1
    ) == 0


def test_wz2_projector_family_is_not_an_su3_map() -> None:
    phase = sp.symbols("F", real=True)
    determinant = sp.exp(sp.I * phase)
    assert sp.simplify(determinant.subs(phase, sp.pi) + 1) == 0
    assert sp.simplify(determinant - 1) != 0


def test_quaternion_embedding_is_exactly_su3_on_the_unit_sphere() -> None:
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", real=True)
    value = su2_quaternion_embedding((a0, a1, a2, a3))
    norm_squared = a0**2 + a1**2 + a2**2 + a3**2
    assert sp.factor(value.det()) == norm_squared
    assert sp.simplify(value.H * value) == sp.diag(norm_squared, norm_squared, 1)
    assert value.subs(a0, 1).subs({a1: 0, a2: 0, a3: 0}) == sp.eye(3)


def test_trace_three_cohomology_and_generator_period_are_exact() -> None:
    d2 = chevalley_eilenberg_differential(2)
    d3 = chevalley_eilenberg_differential(3)
    trace_three = su3_trace_power_cochain(3)
    evidence = su3_winding_three_evidence()
    assert d3 * d2 == sp.zeros(70, 28)
    assert d3 * trace_three == sp.zeros(70, 1)
    assert evidence.differential_squares_to_zero
    assert evidence.trace_is_closed
    assert not evidence.trace_is_exact
    assert evidence.d2_rank == 20
    assert evidence.d3_rank == 35
    assert evidence.three_cocycle_dimension == 21
    assert evidence.third_cohomology_dimension == 1
    assert evidence.trace_nonzero_components == 9
    assert evidence.trace_norm_squared == 9
    assert evidence.augmented_d2_trace_rank == 21
    assert evidence.column_projection_jacobian == 1
    assert evidence.column_projection_degree == 1
    assert evidence.raw_generator_density == 12
    assert evidence.sphere_volume == 2 * sp.pi**2
    assert evidence.raw_generator_period == 24 * sp.pi**2
    assert evidence.normalized_generator_period == -1
    assert evidence.current_coefficient == -1 / (24 * sp.pi**2)
    assert su2_quaternion_trace_three_period() == 24 * sp.pi**2
    assert su3_winding_current_coefficient() == -1 / (24 * sp.pi**2)


def test_quaternion_column_projection_has_positive_degree_one() -> None:
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", real=True)
    first_column = su2_quaternion_embedding((a0, a1, a2, a3))[:, 0]
    target_coordinates = sp.Matrix(
        [
            sp.re(first_column[0]),
            sp.im(first_column[0]),
            sp.re(first_column[1]),
            sp.im(first_column[1]),
        ]
    )
    jacobian = target_coordinates.jacobian((a0, a1, a2, a3))
    assert jacobian.det() == 1
    assert su2_quaternion_column_projection_jacobian() == jacobian.det()


def test_winding_current_orientation_and_closure_are_distinct() -> None:
    zero = sp.zeros(3)
    spatial = tuple(
        su2_quaternion_embedding_differential(tangent)
        for tangent in ((0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1))
    )
    current = su3_winding_current((zero, *spatial))
    reversed_current = su3_winding_current((zero, *spatial), orientation=-1)
    assert current == (-1 / (2 * sp.pi**2), 0, 0, 0)
    assert reversed_current == tuple(-value for value in current)
    assert alternating_trace(spatial) == 12
    assert su3_trace_power_cochain(4) == sp.zeros(len(cochain_basis(4)), 1)
    assert trace_power_derivative_multiplier(3) == 3
    assert maurer_cartan_power_derivative_multiplier(3) == -1
    assert trace_power_cyclic_shift_sign(4) == -1


def test_hedgehog_density_and_boundary_charge_have_sensitive_limits() -> None:
    radius = sp.symbols("r", positive=True)
    profile = sp.Function("F")(radius)
    local = hedgehog_winding_density(profile, radius)
    radial = hedgehog_winding_radial_density(profile, radius)
    assert local == -sp.sin(profile) ** 2 * sp.diff(profile, radius) / (
        2 * sp.pi**2 * radius**2
    )
    assert radial == -2 * sp.sin(profile) ** 2 * sp.diff(profile, radius) / sp.pi
    assert hedgehog_winding_charge(sp.pi, 0) == 1
    assert hedgehog_winding_charge(2 * sp.pi, 0) == 2
    assert hedgehog_winding_charge(0, 0) == 0
    assert hedgehog_winding_charge(sp.pi / 2, 0) == sp.Rational(1, 2)
    assert hedgehog_winding_charge(0, sp.pi) == -1


def test_winding_current_rejects_invalid_shapes_and_orientation() -> None:
    with pytest.raises(ValueError, match="orientation"):
        su3_winding_current((sp.zeros(2),) * 4, orientation=0)
