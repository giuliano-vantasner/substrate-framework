"""Exact normalized sine-Gordon breather definitions.

The convention is

``phi_tt - phi_xx + sin(phi) = 0``

with Hamiltonian density ``(phi_t**2 + phi_x**2)/2 + 1 - cos(phi)``.
Coordinates and fields are dimensionless (``c = m = beta = 1``).  Breather
frequencies lie in the open interval ``0 < omega < 1``.
"""

from __future__ import annotations

from typing import Any

import sympy as sp


def _frequency(omega: Any) -> sp.Expr:
    value = sp.sympify(omega)
    if value.is_number:
        if value.is_real is not True or not 0.0 < float(value) < 1.0:
            raise ValueError("omega must be real and satisfy 0 < omega < 1")
    return value


def _action(action: Any) -> sp.Expr:
    value = sp.sympify(action)
    if value.is_number:
        if value.is_real is not True or not 0.0 < float(value) < float(8 * sp.pi):
            raise ValueError("action must be real and satisfy 0 < action < 8*pi")
    return value


def breather_inverse_width(omega: Any) -> sp.Expr:
    """Return ``eta = sqrt(1 - omega**2)`` in normalized units."""

    frequency = _frequency(omega)
    return sp.sqrt(1 - frequency**2)


def breather_field_with_width(x: Any, t: Any, omega: Any, eta: Any) -> sp.Expr:
    """Return the direct arctangent profile for an explicit inverse width.

    This lower-level construction is on shell only when
    ``eta**2 + omega**2 = 1``.  Exposing ``eta`` makes that load-bearing
    relation available to verifier mutations without redefining the profile.
    """

    coordinate = sp.sympify(x)
    time = sp.sympify(t)
    frequency = _frequency(omega)
    inverse_width = sp.sympify(eta)
    argument = (
        inverse_width
        * sp.sin(frequency * time)
        / (frequency * sp.cosh(inverse_width * coordinate))
    )
    return 4 * sp.atan(argument)


def breather_field(x: Any, t: Any, omega: Any) -> sp.Expr:
    """Return the exact rest-frame breather field for ``0 < omega < 1``."""

    frequency = _frequency(omega)
    return breather_field_with_width(
        x, t, frequency, breather_inverse_width(frequency)
    )


def sine_gordon_residual(field: Any, x: sp.Symbol, t: sp.Symbol) -> sp.Expr:
    """Return ``phi_tt - phi_xx + sin(phi)`` for a symbolic field."""

    expression = sp.sympify(field)
    return sp.diff(expression, t, 2) - sp.diff(expression, x, 2) + sp.sin(expression)


def hamiltonian_density(field: Any, x: sp.Symbol, t: sp.Symbol) -> sp.Expr:
    """Return the normalized sine-Gordon Hamiltonian density."""

    expression = sp.sympify(field)
    return (
        sp.diff(expression, t) ** 2 / 2
        + sp.diff(expression, x) ** 2 / 2
        + 1
        - sp.cos(expression)
    )


def breather_energy(omega: Any) -> sp.Expr:
    """Return the exact conserved rest energy ``16*sqrt(1-omega**2)``."""

    return 16 * breather_inverse_width(omega)


def breather_period(omega: Any) -> sp.Expr:
    """Return the time period ``2*pi/omega``."""

    return 2 * sp.pi / _frequency(omega)


def breather_peak_amplitude(omega: Any) -> sp.Expr:
    """Return the positive peak field amplitude at the spatial center."""

    frequency = _frequency(omega)
    return 4 * sp.atan(breather_inverse_width(frequency) / frequency)


def breather_action(omega: Any) -> sp.Expr:
    """Return the canonical action variable ``J = 16*acos(omega)``."""

    return 16 * sp.acos(_frequency(omega))


def breather_frequency_from_action(action: Any) -> sp.Expr:
    """Return ``omega = cos(J/16)`` for ``0 < J < 8*pi``."""

    return sp.cos(_action(action) / 16)


def breather_energy_from_action(action: Any) -> sp.Expr:
    """Return ``E = 16*sin(J/16)`` for ``0 < J < 8*pi``."""

    return 16 * sp.sin(_action(action) / 16)


def breather_mean_gradient_integral(omega: Any) -> sp.Expr:
    """Return the period average of ``integral(phi_x**2, x)``.

    This is the squared-gradient integral itself, not the half-weighted
    gradient contribution to the Hamiltonian.
    """

    frequency = _frequency(omega)
    return sp.simplify(
        breather_energy(frequency) - frequency * breather_action(frequency)
    )
