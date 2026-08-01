from __future__ import annotations

import sympy as sp

from substrate_framework.separable_moments import axisymmetric_separable_moments
from substrate_framework.tt_angular import (
    frobenius_inner_product,
    frobenius_norm_squared,
    tt_polarization_basis,
    tt_project_symmetric,
)


def test_axisymmetric_product_density_moments_and_variance_convention() -> None:
    mass, longitudinal, variance = sp.symbols("M mu sigma2", real=True)
    result = axisymmetric_separable_moments(mass, longitudinal, variance)
    transverse = mass * variance
    assert result.transverse_axis_second_moment == transverse
    assert result.second_moment == sp.diag(longitudinal, transverse, transverse)
    assert result.trace_free_second_moment == sp.diag(
        sp.Rational(2, 3) * (longitudinal - transverse),
        -sp.Rational(1, 3) * (longitudinal - transverse),
        -sp.Rational(1, 3) * (longitudinal - transverse),
    )
    assert result.triple_normalized_quadrupole == 3 * result.trace_free_second_moment


def test_constant_transverse_width_drops_out_of_every_positive_time_derivative() -> None:
    time = sp.symbols("t", real=True)
    mass, variance = sp.symbols("M sigma2", constant=True)
    longitudinal = sp.Function("mu")(time)
    result = axisymmetric_separable_moments(mass, longitudinal, variance)
    for order in (1, 2, 3, 4):
        derivative = result.trace_free_second_moment.diff(time, order)
        scalar = sp.diff(longitudinal, time, order)
        assert derivative == sp.diag(2 * scalar / 3, -scalar / 3, -scalar / 3)
        assert sp.simplify(frobenius_norm_squared(derivative) - 2 * scalar**2 / 3) == 0
        assert sp.simplify(
            frobenius_norm_squared(3 * derivative) - 6 * scalar**2
        ) == 0


def test_axis_and_perpendicular_tt_geometry_is_exact() -> None:
    derivative = sp.symbols("d", real=True)
    tensor = sp.diag(2 * derivative / 3, -derivative / 3, -derivative / 3)
    assert tt_project_symmetric(tensor, [1, 0, 0]) == sp.zeros(3)
    perpendicular = tt_project_symmetric(tensor, [0, 0, 1])
    assert perpendicular == sp.diag(derivative / 2, -derivative / 2, 0)
    basis = tt_polarization_basis([0, 0, 1], [1, 0, 0])
    assert sp.simplify(
        frobenius_inner_product(perpendicular, basis.plus)
        - derivative / sp.sqrt(2)
    ) == 0
    assert frobenius_inner_product(perpendicular, basis.cross) == 0
