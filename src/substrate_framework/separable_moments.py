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
