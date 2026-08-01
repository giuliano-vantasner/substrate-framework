"""Conditional moments of a centered axisymmetric separable density.

The density construction is declared rather than dynamically generated.  This
module supplies exact moment algebra; it does not supply a conserved 3+1 stress
tensor, a field equation, or a gravitational interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from .conserved_moments import symmetric_trace_free
from .tt_angular import (
    frobenius_inner_product,
    tt_polarization_basis,
    tt_project_symmetric,
)


@dataclass(frozen=True)
class AxisymmetricSeparableMoments:
    """Second moments for longitudinal density times a transverse profile."""

    monopole: sp.Expr
    longitudinal_second_moment: sp.Expr
    transverse_axis_variance: sp.Expr
    transverse_axis_second_moment: sp.Expr
    second_moment: sp.Matrix
    trace_free_second_moment: sp.Matrix
    triple_normalized_quadrupole: sp.Matrix


@dataclass(frozen=True)
class AxisymmetricTTReadout:
    """TT projection and coefficients for an axisymmetric STF derivative."""

    inclination: sp.Expr
    direction: sp.Matrix
    first_transverse: sp.Matrix
    second_transverse: sp.Matrix
    projected_tensor: sp.Matrix
    normalized_plus_coordinate: sp.Expr
    normalized_cross_coordinate: sp.Expr
    conventional_plus_readout: sp.Expr
    conventional_cross_readout: sp.Expr


def axisymmetric_separable_moments(
    monopole: Any,
    longitudinal_second_moment: Any,
    transverse_axis_variance: Any,
) -> AxisymmetricSeparableMoments:
    """Return exact moments of a declared centered product density.

    The longitudinal axis is x.  The declared transverse profile is normalized,
    centered, axisymmetric, and has the per-axis variance
    ``integral(y**2*g)=integral(z**2*g)=transverse_axis_variance``.  Thus the
    radial transverse moment is twice this input.  The longitudinal density has
    total ``monopole`` and centered second moment
    ``longitudinal_second_moment``.
    """

    total = sp.sympify(monopole)
    longitudinal = sp.sympify(longitudinal_second_moment)
    variance = sp.sympify(transverse_axis_variance)
    transverse = sp.simplify(total * variance)
    second = sp.diag(longitudinal, transverse, transverse)
    trace_free = symmetric_trace_free(second)
    return AxisymmetricSeparableMoments(
        monopole=total,
        longitudinal_second_moment=longitudinal,
        transverse_axis_variance=variance,
        transverse_axis_second_moment=transverse,
        second_moment=second,
        trace_free_second_moment=trace_free,
        triple_normalized_quadrupole=sp.simplify(3 * trace_free),
    )


def axisymmetric_separable_stf_derivative(
    longitudinal_derivative: Any,
    quadrupole_scale: Any = 1,
) -> sp.Matrix:
    """Return a positive-order derivative of the separable STF tensor.

    ``quadrupole_scale=1`` is the normalized STF convention and scale three is
    the triple convention.  The constant monopole and transverse variance have
    already differentiated away.
    """

    derivative = sp.sympify(longitudinal_derivative)
    scale = sp.sympify(quadrupole_scale)
    return sp.simplify(
        scale
        * sp.diag(
            2 * derivative / 3,
            -derivative / 3,
            -derivative / 3,
        )
    )


def axisymmetric_stf_tt_readout(
    longitudinal_derivative: Any,
    inclination: Any,
) -> AxisymmetricTTReadout:
    """Project a normalized axisymmetric STF derivative at an inclination.

    The symmetry axis is x.  ``inclination`` is measured from that axis in the
    x-z plane.  The oriented transverse frame is
    ``p=(sin(i),0,-cos(i))`` and ``q=(0,1,0)``.  Normalized basis coordinates
    use C-GW-002; conventional matrix read-outs are smaller by ``sqrt(2)``.
    """

    derivative = sp.sympify(longitudinal_derivative)
    angle = sp.sympify(inclination)
    direction = sp.Matrix([sp.cos(angle), 0, sp.sin(angle)])
    first = sp.Matrix([sp.sin(angle), 0, -sp.cos(angle)])
    basis = tt_polarization_basis(direction, first)
    tensor = axisymmetric_separable_stf_derivative(derivative)
    projected = tt_project_symmetric(tensor, direction)
    plus = sp.simplify(frobenius_inner_product(projected, basis.plus))
    cross = sp.simplify(frobenius_inner_product(projected, basis.cross))
    return AxisymmetricTTReadout(
        inclination=angle,
        direction=basis.direction,
        first_transverse=basis.first_transverse,
        second_transverse=basis.second_transverse,
        projected_tensor=projected,
        normalized_plus_coordinate=plus,
        normalized_cross_coordinate=cross,
        conventional_plus_readout=sp.simplify(plus / sp.sqrt(2)),
        conventional_cross_readout=sp.simplify(cross / sp.sqrt(2)),
    )
