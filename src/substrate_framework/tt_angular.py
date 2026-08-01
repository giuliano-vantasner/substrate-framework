"""Exact angular reduction for a declared transverse-traceless wave model.

This module proves projector and normalization algebra.  It deliberately does
not supply a gravitational field equation, a source-to-waveform map, or an
energy-flux law; callers must pass those conditional prefactors explicitly.
"""

from __future__ import annotations

from typing import Any

import sympy as sp

from .conserved_moments import symmetric_trace_free


def _symmetric_three(matrix: Any, name: str) -> sp.Matrix:
    value = sp.Matrix(matrix)
    if value.shape != (3, 3):
        raise ValueError(f"{name} must be 3 by 3")
    if sp.simplify(value - value.T) != sp.zeros(3):
        raise ValueError(f"{name} must be symmetric")
    return value


def _column_three(vector: Any, name: str) -> sp.Matrix:
    value = sp.Matrix(vector)
    if value.shape not in ((3, 1), (1, 3)):
        raise ValueError(f"{name} must have three components")
    return value if value.shape == (3, 1) else value.T


def transverse_projector(direction: Any) -> sp.Matrix:
    """Return ``I-n*n.T/(n.n)`` for a nonzero three-direction."""

    vector = _column_three(direction, "direction")
    norm_squared = sp.simplify(vector.dot(vector))
    if norm_squared == 0:
        raise ValueError("direction must be nonzero")
    return sp.simplify(sp.eye(3) - vector * vector.T / norm_squared)


def tt_project_symmetric(tensor: Any, direction: Any) -> sp.Matrix:
    """Project a symmetric spatial tensor transverse and trace-free.

    With ``P`` the rank-two transverse projector, this returns
    ``P*S*P - P*trace(P*S*P)/2``.  The factor one-half is the trace removal in
    the two-dimensional plane orthogonal to the line of sight.
    """

    source = _symmetric_three(tensor, "tensor")
    projector = transverse_projector(direction)
    transverse = sp.simplify(projector * source * projector)
    return sp.simplify(transverse - projector * sp.trace(transverse) / 2)


def frobenius_norm_squared(tensor: Any) -> sp.Expr:
    """Return the exact Cartesian contraction ``S_ij*S_ij``."""

    value = sp.Matrix(tensor)
    return sp.simplify(
        sum(
            (value[i, j] ** 2 for i in range(value.rows) for j in range(value.cols)),
            sp.Integer(0),
        )
    )


def integrated_tt_norm_squared(tensor: Any) -> sp.Expr:
    """Return the exact full-sphere integral of ``|TT_n(tensor)|^2``.

    For a symmetric spatial tensor ``S`` in three dimensions,

    ``integral_S2 |TT_n(S)|^2 dOmega = (8*pi/5)*|STF(S)|^2``.

    The result is invariant under adding a pure trace.
    """

    source = _symmetric_three(tensor, "tensor")
    trace_free = symmetric_trace_free(source)
    return sp.simplify(sp.Rational(8, 5) * sp.pi * frobenius_norm_squared(trace_free))


def conditional_tt_power(
    quadrupole_third_derivative: Any,
    waveform_prefactor: Any,
    flux_prefactor: Any,
) -> sp.Expr:
    """Reduce declared waveform and flux inputs to total angular power.

    The declared inputs are
    ``h_TT=(waveform_prefactor/r)*TT(Q_ddot)`` and
    ``dP/dOmega=flux_prefactor*r**2*<hdot_TT:hdot_TT>``.  This function
    performs only the exact angular contraction for the supplied instantaneous
    or already-averaged third derivative.
    """

    wave = sp.sympify(waveform_prefactor)
    flux = sp.sympify(flux_prefactor)
    return sp.simplify(
        flux * wave**2 * integrated_tt_norm_squared(quadrupole_third_derivative)
    )


def waveform_prefactor_for_quadrupole_convention(
    normalized_stf_waveform_prefactor: Any,
    quadrupole_scale: Any,
) -> sp.Expr:
    """Convert a waveform coefficient when ``Q=scale*I_STF``.

    Preserving the same field requires the coefficient multiplying ``Q`` to be
    the coefficient multiplying ``I_STF`` divided by ``scale``.
    """

    prefactor = sp.sympify(normalized_stf_waveform_prefactor)
    scale = sp.sympify(quadrupole_scale)
    if scale == 0:
        raise ValueError("quadrupole_scale must be nonzero")
    return sp.simplify(prefactor / scale)


def harmonic_stf_third_derivative_average(
    cosine_amplitude: Any,
    sine_amplitude: Any,
    angular_frequency: Any,
) -> sp.Expr:
    """Average ``|d^3/dt^3(C cos wt + S sin wt)|^2`` over one cycle.

    Only the symmetric trace-free parts enter a TT contraction.  Exact cycle
    orthogonality gives ``w**6*(|STF(C)|**2+|STF(S)|**2)/2``.
    """

    cosine = symmetric_trace_free(_symmetric_three(cosine_amplitude, "cosine_amplitude"))
    sine = symmetric_trace_free(_symmetric_three(sine_amplitude, "sine_amplitude"))
    frequency = sp.sympify(angular_frequency)
    return sp.simplify(
        frequency**6
        * (frobenius_norm_squared(cosine) + frobenius_norm_squared(sine))
        / 2
    )
