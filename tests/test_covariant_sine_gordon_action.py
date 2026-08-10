"""Exact tests for the covariant 3+1 sine-Gordon action and its fluctuation operator.

The oracle is exact SymPy: every check is an identity or a mutation that must
break a specific identity.  Backgrounds are flat (R=0) and FLRW (R!=0) so the
measure connection term and the curvature term are both exercised.
"""

from __future__ import annotations

import sympy as sp
from sympy.calculus.euler import euler_equations

import pytest

import substrate_framework as framework
from substrate_framework.covariant_sine_gordon_action import (
    CovariantSineGordonAction,
    CovariantSineGordonFluctuation,
    covariant_sine_gordon_action,
    covariant_sine_gordon_action_density,
    covariant_sine_gordon_field_equation,
    covariant_sine_gordon_fluctuation_operator,
    laplace_beltrami,
    ricci_scalar,
    sine_gordon_potential_scaled,
    sqrt_minus_g,
)
from substrate_framework.scalar_induced_newton import scalar_heat_kernel_a2
from substrate_framework.sine_gordon import sine_gordon_potential, sine_gordon_residual


COORDS = sp.symbols("t x y z", real=True)
T, X, Y, Z = COORDS
MINKOWSKI = sp.diag(-1, 1, 1, 1)


def _flrw_metric():
    scale = sp.Function("a")
    return sp.diag(-1, scale(T) ** 2, scale(T) ** 2, scale(T) ** 2), scale


def test_package_level_exports():
    assert framework.covariant_sine_gordon_action is covariant_sine_gordon_action
    assert framework.covariant_sine_gordon_field_equation is covariant_sine_gordon_field_equation
    assert framework.ricci_scalar is ricci_scalar
    assert framework.laplace_beltrami is laplace_beltrami


def test_flat_limit_reproduces_accepted_3plus1_sine_gordon():
    field = sp.Function("phi")(*COORDS)
    residual = covariant_sine_gordon_field_equation(
        field, MINKOWSKI, COORDS, non_minimal_coupling=sp.Rational(1, 6)
    )
    accepted = (
        sp.diff(field, T, 2)
        - sp.diff(field, X, 2)
        - sp.diff(field, Y, 2)
        - sp.diff(field, Z, 2)
        + sp.sin(field)
    )
    # box_g phi - V'(phi) is the negative of the (phi_tt - lap + sin) residual.
    assert sp.simplify(residual + accepted) == 0


def test_flat_limit_matches_accepted_1plus1_residual():
    field = sp.Function("phi")(T, X)
    residual = covariant_sine_gordon_field_equation(field, MINKOWSKI, COORDS)
    assert sp.simplify(residual + sine_gordon_residual(field, X, T)) == 0


def test_ricci_scalar_flat_is_zero():
    assert ricci_scalar(MINKOWSKI, COORDS) == 0


def test_ricci_scalar_flrw_matches_closed_form():
    metric, scale = _flrw_metric()
    expected = 6 * (
        sp.diff(scale(T), T, 2) / scale(T) + (sp.diff(scale(T), T) / scale(T)) ** 2
    )
    assert sp.simplify(ricci_scalar(metric, COORDS) - expected) == 0


def test_laplace_beltrami_flrw_has_hubble_friction():
    metric, scale = _flrw_metric()
    field = sp.Function("psi")(T)
    hubble = sp.diff(scale(T), T) / scale(T)
    expected = -(sp.diff(field, T, 2) + 3 * hubble * sp.diff(field, T))
    assert sp.simplify(laplace_beltrami(field, metric, COORDS) - expected) == 0


def test_constructor_euler_lagrange_equals_covariant_operator_flrw():
    metric, scale = _flrw_metric()
    field = sp.Function("psi")(T)
    action = covariant_sine_gordon_action(
        field, metric, COORDS, non_minimal_coupling=sp.Rational(1, 6)
    )
    assert isinstance(action, CovariantSineGordonAction)
    # The constructor internally requires euler == sqrt(-g)*field_equation; here
    # confirm the returned field_equation is the independent covariant operator.
    hubble = sp.diff(scale(T), T) / scale(T)
    curvature = ricci_scalar(metric, COORDS)
    independent = (
        -(sp.diff(field, T, 2) + 3 * hubble * sp.diff(field, T))
        - sp.sin(field)
        - sp.Rational(1, 6) * curvature * field
    )
    assert sp.simplify(action.field_equation - independent) == 0
    assert sp.simplify(action.euler_lagrange - action.sqrt_minus_g * action.field_equation) == 0


def test_fluctuation_endomorphism_is_rung1_heat_kernel_input():
    """Rung bridge: the second variation IS scalar_heat_kernel_a2's declared input."""
    metric, _ = _flrw_metric()
    field = sp.Function("psi")(T)
    xi = sp.Rational(1, 5)
    fluctuation = covariant_sine_gordon_fluctuation_operator(
        field, metric, COORDS, non_minimal_coupling=xi, mass_squared=1
    )
    assert isinstance(fluctuation, CovariantSineGordonFluctuation)
    curvature = ricci_scalar(metric, COORDS)
    # D = -box + E with E = V''(phi_bg) + xi R; V''(phi) = m^2 cos(phi).
    assert sp.simplify(fluctuation.endomorphism - (sp.cos(field) + xi * curvature)) == 0
    # At the vacuum the mass term is V''(0) = m^2.
    assert sp.simplify(fluctuation.endomorphism.subs(field, 0) - (1 + xi * curvature)) == 0
    assert fluctuation.vacuum_mass_squared == 1
    # The vacuum operator is exactly D_E = -nabla^2 + xi R + m^2 that rung-1 consumes.
    a2 = scalar_heat_kernel_a2(xi, mass_squared=fluctuation.vacuum_mass_squared)
    assert sp.simplify(a2.mass_squared - fluctuation.vacuum_mass_squared) == 0
    assert sp.simplify(a2.non_minimal_coupling - fluctuation.non_minimal_coupling) == 0
    # rung-1's curvature weight is 1/6 - xi in this shared convention.
    assert sp.simplify(a2.curvature_weight - (sp.Rational(1, 6) - xi)) == 0


def test_wrong_action_measure_breaks_field_equation():
    metric, _ = _flrw_metric()
    field = sp.Function("psi")(T)
    action = covariant_sine_gordon_action(
        field, metric, COORDS, non_minimal_coupling=sp.Rational(1, 6)
    )
    root = sqrt_minus_g(metric)
    wrong = covariant_sine_gordon_action_density(
        field,
        metric,
        COORDS,
        non_minimal_coupling=sp.Rational(1, 6),
        measure=sp.Integer(1),
    )
    euler_wrong = euler_equations(wrong, [field], [T])[0]
    mismatch = sp.simplify(
        (euler_wrong.lhs - euler_wrong.rhs) - root * action.field_equation
    )
    assert mismatch != 0
    # A correct measure would have produced exactly the Hubble-friction term.


def test_wrong_curvature_coupling_sign_breaks_field_equation():
    metric, _ = _flrw_metric()
    field = sp.Function("psi")(T)
    xi = sp.Rational(1, 6)
    action = covariant_sine_gordon_action(field, metric, COORDS, non_minimal_coupling=xi)
    root = sqrt_minus_g(metric)
    curvature = ricci_scalar(metric, COORDS)
    flipped = covariant_sine_gordon_action_density(
        field, metric, COORDS, non_minimal_coupling=xi, curvature_sign=-1
    )
    euler_flipped = euler_equations(flipped, [field], [T])[0]
    difference = sp.simplify(
        (euler_flipped.lhs - euler_flipped.rhs) - root * action.field_equation
    )
    assert difference != 0
    # The flip differs from the correct equation by exactly 2*xi*R*phi*sqrt(-g).
    assert sp.simplify(difference - root * 2 * xi * curvature * field) == 0


def test_minimal_coupling_has_no_curvature_term():
    metric, _ = _flrw_metric()
    field = sp.Function("psi")(T)
    residual = covariant_sine_gordon_field_equation(
        field, metric, COORDS, non_minimal_coupling=0
    )
    box = laplace_beltrami(field, metric, COORDS)
    assert sp.simplify(residual - (box - sp.sin(field))) == 0


def test_potential_composes_accepted_form_and_derivatives():
    phi = sp.Symbol("phi", real=True)
    mass = sp.Rational(3, 2)
    potential = sine_gordon_potential_scaled(phi, mass)
    assert sp.simplify(potential - mass * sine_gordon_potential(phi)) == 0
    assert sp.simplify(sp.diff(potential, phi) - mass * sp.sin(phi)) == 0
    assert sp.simplify(sp.diff(potential, phi, 2) - mass * sp.cos(phi)) == 0


def test_target_blindness_no_gravity_or_regulator_symbols():
    metric, _ = _flrw_metric()
    field = sp.Function("psi")(T)
    action = covariant_sine_gordon_action(field, metric, COORDS, non_minimal_coupling=sp.Rational(1, 6))
    forbidden = {"G", "G_N", "kappa", "Lambda", "Newton", "regulator", "cutoff"}
    for expression in (action.action_density, action.field_equation, action.fluctuation.endomorphism):
        names = {symbol.name for symbol in expression.free_symbols}
        names |= {function.func.__name__ for function in expression.atoms(sp.Function)}
        assert forbidden.isdisjoint(names)


def test_conformal_coupling_zeroes_rung1_curvature_weight():
    # At xi = 1/6 the shared convention's curvature weight vanishes.
    a2 = scalar_heat_kernel_a2(sp.Rational(1, 6), mass_squared=1)
    assert a2.curvature_weight == 0
    metric, _ = _flrw_metric()
    field = sp.Function("psi")(T)
    fluctuation = covariant_sine_gordon_fluctuation_operator(
        field, metric, COORDS, non_minimal_coupling=sp.Rational(1, 6)
    )
    curvature = ricci_scalar(metric, COORDS)
    assert sp.simplify(fluctuation.curvature_endomorphism - curvature / 6) == 0


def test_input_contracts_reject_ill_posed_arguments():
    field = sp.Function("phi")(*COORDS)
    with pytest.raises(ValueError):
        ricci_scalar(sp.eye(3), COORDS)  # not 4x4
    with pytest.raises(ValueError):
        covariant_sine_gordon_field_equation(field, sp.Matrix([[T, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]), COORDS)  # asymmetric
    with pytest.raises(ValueError):
        covariant_sine_gordon_field_equation(field, sp.zeros(4, 4), COORDS)  # singular
    with pytest.raises(ValueError):
        covariant_sine_gordon_field_equation(field, MINKOWSKI, COORDS, non_minimal_coupling=sp.Float("0.1"))  # inexact
    with pytest.raises(ValueError):
        covariant_sine_gordon_field_equation(field, MINKOWSKI, COORDS, mass_squared=0)  # not positive
    with pytest.raises(ValueError):
        foreign = sp.Function("phi")(sp.Symbol("w"))
        covariant_sine_gordon_action(foreign, MINKOWSKI, COORDS)  # foreign coordinate
