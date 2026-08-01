"""Exact boundary sign correlations and half-line winding conversion.

The sign correlation defined here is a boundary observable, not a topological
charge.  The two are kept as separately named APIs because no algebraic
implication relates them without additional boundary dynamics.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def _real_scalar(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number and expression.is_real is not True:
        raise ValueError(f"{name} must be real")
    return expression


def _positive_frequency(value: Any) -> sp.Expr:
    frequency = _real_scalar(value, "angular_frequency")
    if frequency.is_number and not float(frequency) > 0.0:
        raise ValueError("angular_frequency must be positive")
    return frequency


def boundary_sign_correlation_density(
    boundary_time_derivative: Any,
    boundary_coordinate_derivative: Any,
) -> sp.Expr:
    """Return ``sign(phi_t)*phi_x`` for declared boundary traces.

    The second argument is the derivative in a fixed coordinate direction. It
    is not automatically an outward-normal derivative of a physical domain.
    """

    time_derivative = _real_scalar(
        boundary_time_derivative,
        "boundary_time_derivative",
    )
    coordinate_derivative = _real_scalar(
        boundary_coordinate_derivative,
        "boundary_coordinate_derivative",
    )
    return sp.sign(time_derivative) * coordinate_derivative


def sinusoidal_boundary_sign_correlation(
    time_amplitude: Any,
    coordinate_amplitude: Any,
    angular_frequency: Any,
    relative_phase: Any,
) -> sp.Expr:
    """Return the exact full-period correlation for two sinusoidal traces.

    The convention is ``phi_t=A*sin(theta)`` and
    ``phi_x=B*sin(theta+delta)`` over one period, where ``delta`` is the
    supplied relative phase.  The result is
    ``4*sign(A)*B*cos(delta)/omega``.  A cosine convention for the second
    trace requires the corresponding explicit phase shift.
    """

    temporal_amplitude = _real_scalar(time_amplitude, "time_amplitude")
    spatial_amplitude = _real_scalar(
        coordinate_amplitude,
        "coordinate_amplitude",
    )
    frequency = _positive_frequency(angular_frequency)
    phase = _real_scalar(relative_phase, "relative_phase")
    return sp.simplify(
        4 * sp.sign(temporal_amplitude) * spatial_amplitude * sp.cos(phase)
        / frequency
    )


def right_half_line_topological_charge_change(
    boundary_field_change: Any,
) -> sp.Expr:
    """Return ``-Delta(phi_boundary)/(2*pi)`` on a right half-line.

    This conversion uses the orientation ``epsilon**01=+1`` and domain
    ``x >= b``.  It additionally assumes the field at positive infinity is
    time independent, so the boundary field change is the complete integrated
    topological flux.
    """

    field_change = _real_scalar(boundary_field_change, "boundary_field_change")
    return sp.simplify(-field_change / (2 * sp.pi))
