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


def lattice_debye_energy(
    action_scale: Any,
    reference_speed: Any,
    length_scale: Any,
    speed_ratio: Any = 1,
) -> sp.Expr:
    """Return the declared lattice scale ``Theta=kappa*S*c/a``.

    This is a conditional Debye/zero-point premise. Dimensional analysis makes
    the monomial available but does not select it dynamically or determine the
    dimensionless speed ratio ``kappa``.
    """

    action = _positive(action_scale, "action_scale")
    speed = _positive(reference_speed, "reference_speed")
    length = _positive(length_scale, "length_scale")
    ratio = _positive(speed_ratio, "speed_ratio")
    return sp.simplify(ratio * action * speed / length)


def lattice_reduced_responses(
    action_scale: Any,
    reference_speed: Any,
    length_scale: Any,
    speed_ratio: Any = 1,
    mass_density_ratio: Any = sp.Rational(1, 2),
) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    """Compose declared lattice and Debye premises with co-scaled responses.

    Returns ``(Theta, epsilon, mu_inverse, mass_density)`` conditional on
    ``n=a**-3``, ``Theta=kappa*S*c/a``, the co-scaled response laws, and
    ``mass_density=mass_density_ratio*epsilon``.
    """

    action = _positive(action_scale, "action_scale")
    speed = _positive(reference_speed, "reference_speed")
    length = _positive(length_scale, "length_scale")
    ratio = _positive(speed_ratio, "speed_ratio")
    density_ratio = _positive(mass_density_ratio, "mass_density_ratio")
    number_density = length**-3
    thermal_scale = lattice_debye_energy(action, speed, length, ratio)
    epsilon = co_scaled_permittivity(number_density, thermal_scale, speed)
    inverse_mu = co_scaled_inverse_permeability(number_density, thermal_scale)
    return (
        thermal_scale,
        sp.simplify(epsilon),
        sp.simplify(inverse_mu),
        sp.simplify(density_ratio * epsilon),
    )
