"""Exact utilities for a declared co-scaled electromagnetic response ansatz."""

from __future__ import annotations

from typing import Any

import sympy as sp


def _positive(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number and expression.is_positive is not True:
        raise ValueError(f"{name} must be positive")
    return expression


def co_scaled_permittivity(
    density: Any,
    thermal_scale: Any,
    reference_speed: Any,
) -> sp.Expr:
    """Return the declared response ``epsilon = rho*Theta/c**2``."""

    rho = _positive(density, "density")
    theta = _positive(thermal_scale, "thermal_scale")
    speed = _positive(reference_speed, "reference_speed")
    return rho * theta / speed**2


def co_scaled_inverse_permeability(
    density: Any,
    thermal_scale: Any,
) -> sp.Expr:
    """Return the declared response ``mu**-1 = rho*Theta``."""

    rho = _positive(density, "density")
    theta = _positive(thermal_scale, "thermal_scale")
    return rho * theta


def local_wave_speed(
    permittivity: Any,
    inverse_permeability: Any,
) -> sp.Expr:
    """Return ``1/sqrt(epsilon*mu) = sqrt(mu_inverse/epsilon)``."""

    epsilon = _positive(permittivity, "permittivity")
    inverse_mu = _positive(inverse_permeability, "inverse_permeability")
    return sp.sqrt(inverse_mu / epsilon)


def co_scaled_wave_speed(
    density: Any,
    thermal_scale: Any,
    reference_speed: Any,
) -> sp.Expr:
    """Return the wave speed of the declared co-scaled responses."""

    return sp.simplify(
        local_wave_speed(
            co_scaled_permittivity(
                density, thermal_scale, reference_speed
            ),
            co_scaled_inverse_permeability(density, thermal_scale),
        )
    )
