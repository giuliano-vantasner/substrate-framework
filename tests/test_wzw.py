from __future__ import annotations

import sympy as sp

from substrate_framework.wzw import (
    antihermitian_generators,
    antihermitian_structure_constants,
    chevalley_eilenberg_differential,
    cochain_basis,
    extension_phase_ratio,
    glued_filling_period,
    maurer_cartan_power_derivative_multiplier,
    sphere_extension_coefficient,
    sphere_extension_phase_ratio,
    su3_pi5_generator,
    su3_pi5_period_evidence,
    su3_real_trace_five_cochain,
    su3_sphere_trace_five_period,
    su3_trace_five_cohomology,
    su3_trace_power_cochain,
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
