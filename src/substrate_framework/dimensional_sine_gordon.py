"""Exact conditional reduction of a dimensional cosine field model.

The declared density is

``lambda*u_t**2/2 - tension*u_x**2/2 - mu*(1-cos(u))``

for a dimensionless real field and physical space and time coordinates. This
module derives its coefficient ratios and the pullback of the accepted
normalized sine-Gordon breather. It does not derive the density from a
material, select any coefficient, or remove the common coefficient scale.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp

from .sine_gordon import (
    breather_action,
    breather_energy,
    breather_field,
    breather_inverse_width,
)


def _positive_exact(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact rather than floating")
    if expression.is_real is not True or expression.is_positive is not True:
        raise ValueError(f"{name} must be provably positive and real")
    return expression


def _normalized_frequency(value: Any) -> sp.Expr:
    frequency = sp.sympify(value)
    if frequency.has(sp.Float):
        raise ValueError("frequency must be exact rather than floating")
    if frequency.is_number and (
        frequency.is_real is not True
        or not bool(frequency > 0)
        or not bool(frequency < 1)
    ):
        raise ValueError("frequency must satisfy 0 < frequency < 1")
    if frequency.is_real is False:
        raise ValueError("frequency must be real")
    return frequency


@dataclass(frozen=True)
class DimensionalSineGordonCoefficients:
    """Positive coefficients of the declared dimensional density."""

    inertia: sp.Expr
    gradient: sp.Expr
    onsite: sp.Expr


@dataclass(frozen=True)
class DimensionalSineGordonScales:
    """Ratios and dimensional normalization scales of the declared model."""

    signal_speed: sp.Expr
    gap_frequency: sp.Expr
    length: sp.Expr
    energy: sp.Expr
    action: sp.Expr


@dataclass(frozen=True)
class DimensionalBreatherObservables:
    """Exact physical-coordinate observables of a pulled-back breather."""

    angular_frequency: sp.Expr
    period: sp.Expr
    inverse_width: sp.Expr
    profile_length: sp.Expr
    energy: sp.Expr
    action: sp.Expr


def _validated_coefficients(
    coefficients: DimensionalSineGordonCoefficients,
) -> DimensionalSineGordonCoefficients:
    """Validate a coefficient record even when its dataclass was built directly."""

    if not isinstance(coefficients, DimensionalSineGordonCoefficients):
        raise TypeError("coefficients must be a DimensionalSineGordonCoefficients record")
    return dimensional_sine_gordon_coefficients(
        coefficients.inertia,
        coefficients.gradient,
        coefficients.onsite,
    )


def dimensional_sine_gordon_coefficients(
    inertia: Any,
    gradient: Any,
    onsite: Any,
) -> DimensionalSineGordonCoefficients:
    """Return the exact positive coefficients in canonical field order."""

    return DimensionalSineGordonCoefficients(
        inertia=_positive_exact(inertia, "inertia"),
        gradient=_positive_exact(gradient, "gradient"),
        onsite=_positive_exact(onsite, "onsite"),
    )


def dimensional_sine_gordon_scales(
    coefficients: DimensionalSineGordonCoefficients,
) -> DimensionalSineGordonScales:
    r"""Return ``c``, ``omega_0``, ``ell``, and energy/action scales.

    For coefficients ``(lambda,T,mu)``,
    ``c=sqrt(T/lambda)``, ``omega_0=sqrt(mu/lambda)``,
    ``ell=sqrt(T/mu)``, ``E_scale=sqrt(T*mu)``, and
    ``J_scale=sqrt(lambda*T)``.
    """

    lam = _positive_exact(coefficients.inertia, "inertia")
    tension = _positive_exact(coefficients.gradient, "gradient")
    mu = _positive_exact(coefficients.onsite, "onsite")
    return DimensionalSineGordonScales(
        signal_speed=sp.sqrt(tension / lam),
        gap_frequency=sp.sqrt(mu / lam),
        length=sp.sqrt(tension / mu),
        energy=sp.sqrt(tension * mu),
        action=sp.sqrt(lam * tension),
    )


def dimensional_sine_gordon_coefficients_from_speed_gap(
    inertia_scale: Any,
    signal_speed: Any,
    gap_frequency: Any,
) -> DimensionalSineGordonCoefficients:
    r"""Return the coefficient ray at supplied ``lambda``, ``c``, ``omega_0``.

    The inverse family is
    ``(lambda,T,mu)=(lambda,lambda*c**2,lambda*omega_0**2)``.
    Thus ``c`` and ``omega_0`` do not determine the common positive scale.
    """

    lam = _positive_exact(inertia_scale, "inertia_scale")
    speed = _positive_exact(signal_speed, "signal_speed")
    gap = _positive_exact(gap_frequency, "gap_frequency")
    return dimensional_sine_gordon_coefficients(
        lam,
        lam * speed**2,
        lam * gap**2,
    )


def rescale_dimensional_sine_gordon_coefficients(
    coefficients: DimensionalSineGordonCoefficients,
    multiplier: Any,
) -> DimensionalSineGordonCoefficients:
    """Apply a common positive multiplier to all three coefficients."""

    factor = _positive_exact(multiplier, "multiplier")
    return dimensional_sine_gordon_coefficients(
        factor * coefficients.inertia,
        factor * coefficients.gradient,
        factor * coefficients.onsite,
    )


def dimensional_sine_gordon_lagrangian_density(
    field: Any,
    coordinate: sp.Symbol,
    time: sp.Symbol,
    coefficients: DimensionalSineGordonCoefficients,
) -> sp.Expr:
    """Return the declared dimensional cosine Lagrangian density."""

    expression = sp.sympify(field)
    validated = _validated_coefficients(coefficients)
    return (
        validated.inertia * sp.diff(expression, time) ** 2 / 2
        - validated.gradient * sp.diff(expression, coordinate) ** 2 / 2
        - validated.onsite * (1 - sp.cos(expression))
    )


def dimensional_sine_gordon_hamiltonian_density(
    field: Any,
    coordinate: sp.Symbol,
    time: sp.Symbol,
    coefficients: DimensionalSineGordonCoefficients,
) -> sp.Expr:
    """Return the positive Noether energy density for constant coefficients."""

    expression = sp.sympify(field)
    validated = _validated_coefficients(coefficients)
    return (
        validated.inertia * sp.diff(expression, time) ** 2 / 2
        + validated.gradient * sp.diff(expression, coordinate) ** 2 / 2
        + validated.onsite * (1 - sp.cos(expression))
    )


def dimensional_sine_gordon_residual(
    field: Any,
    coordinate: sp.Symbol,
    time: sp.Symbol,
    coefficients: DimensionalSineGordonCoefficients,
) -> sp.Expr:
    """Return ``lambda*u_tt-T*u_xx+mu*sin(u)``."""

    expression = sp.sympify(field)
    validated = _validated_coefficients(coefficients)
    return (
        validated.inertia * sp.diff(expression, time, 2)
        - validated.gradient * sp.diff(expression, coordinate, 2)
        + validated.onsite * sp.sin(expression)
    )


def dimensional_sine_gordon_normalized_coordinates(
    coordinate: Any,
    time: Any,
    coefficients: DimensionalSineGordonCoefficients,
) -> tuple[sp.Expr, sp.Expr]:
    """Return ``(X,tau)=(x/ell,omega_0*t)``."""

    scales = dimensional_sine_gordon_scales(coefficients)
    return (
        sp.sympify(coordinate) / scales.length,
        scales.gap_frequency * sp.sympify(time),
    )


def dimensional_sine_gordon_physical_coordinates(
    normalized_coordinate: Any,
    normalized_time: Any,
    coefficients: DimensionalSineGordonCoefficients,
) -> tuple[sp.Expr, sp.Expr]:
    """Return ``(x,t)=(ell*X,tau/omega_0)``."""

    scales = dimensional_sine_gordon_scales(coefficients)
    return (
        scales.length * sp.sympify(normalized_coordinate),
        sp.sympify(normalized_time) / scales.gap_frequency,
    )


def dimensional_breather_field(
    coordinate: Any,
    time: Any,
    frequency: Any,
    coefficients: DimensionalSineGordonCoefficients,
) -> sp.Expr:
    """Pull the accepted normalized rest breather into physical coordinates."""

    normalized_frequency = _normalized_frequency(frequency)
    normalized_x, normalized_t = dimensional_sine_gordon_normalized_coordinates(
        coordinate,
        time,
        coefficients,
    )
    return breather_field(normalized_x, normalized_t, normalized_frequency)


def dimensional_breather_observables(
    frequency: Any,
    coefficients: DimensionalSineGordonCoefficients,
) -> DimensionalBreatherObservables:
    """Return physical frequency, period, profile scales, energy, and action."""

    normalized_frequency = _normalized_frequency(frequency)
    scales = dimensional_sine_gordon_scales(coefficients)
    eta = breather_inverse_width(normalized_frequency)
    angular_frequency = normalized_frequency * scales.gap_frequency
    return DimensionalBreatherObservables(
        angular_frequency=angular_frequency,
        period=2 * sp.pi / angular_frequency,
        inverse_width=eta / scales.length,
        profile_length=scales.length / eta,
        energy=scales.energy * breather_energy(normalized_frequency),
        action=scales.action * breather_action(normalized_frequency),
    )


def dimensional_sine_gordon_log_ratio_jacobian() -> sp.ImmutableMatrix:
    r"""Return derivatives of ``log(c,omega_0,ell)`` by coefficient logs.

    Column order is ``(lambda,T,mu)``. The matrix has rank two and right
    nullspace spanned by ``(1,1,1)``, the common-multiplier direction.
    """

    return sp.ImmutableMatrix(
        [
            [-sp.Rational(1, 2), sp.Rational(1, 2), 0],
            [-sp.Rational(1, 2), 0, sp.Rational(1, 2)],
            [0, sp.Rational(1, 2), -sp.Rational(1, 2)],
        ]
    )


def dimensional_sine_gordon_coefficient_dimension_matrix() -> sp.ImmutableMatrix:
    r"""Return coefficient dimensions over rows ``(energy,length,time)``.

    Columns are ``(lambda,T,mu)`` with dimensions
    ``E*time**2/length``, ``E*length``, and ``E/length``. This matrix is
    full rank; dimensional independence and parameter identifiability remain
    different questions.
    """

    return sp.ImmutableMatrix(
        [
            [1, 1, 1],
            [-1, 1, -1],
            [2, 0, 0],
        ]
    )
