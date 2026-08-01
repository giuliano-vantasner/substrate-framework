"""Exact radial line, spherical-shell, and capillary energy utilities."""

from __future__ import annotations

from typing import Any

import sympy as sp


def _positive_quantity(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number and expression.is_positive is not True:
        raise ValueError(f"{name} must be positive")
    return expression


def _real_quantity(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number and expression.is_real is not True:
        raise ValueError(f"{name} must be real")
    return expression


def line_energy(radius: Any, line_density: Any) -> sp.Expr:
    """Return circumference-weighted line energy ``2*pi*R*lambda``."""

    radial_coordinate = _positive_quantity(radius, "radius")
    density = _positive_quantity(line_density, "line_density")
    return 2 * sp.pi * radial_coordinate * density


def spherical_shell_energy(radius: Any, surface_density: Any) -> sp.Expr:
    """Return spherical-area energy ``4*pi*R**2*sigma``."""

    radial_coordinate = _positive_quantity(radius, "radius")
    density = _positive_quantity(surface_density, "surface_density")
    return 4 * sp.pi * radial_coordinate**2 * density


def capillary_energy(
    radius: Any,
    line_tension: Any,
    pressure: Any,
    core_energy: Any = 0,
) -> sp.Expr:
    """Return ``2*pi*R*T - pi*R**2*P + E_core`` for positive ``R,T,P``."""

    radial_coordinate = _positive_quantity(radius, "radius")
    tension = _positive_quantity(line_tension, "line_tension")
    drive = _positive_quantity(pressure, "pressure")
    core = _real_quantity(core_energy, "core_energy")
    return 2 * sp.pi * radial_coordinate * tension - sp.pi * radial_coordinate**2 * drive + core


def capillary_critical_radius(line_tension: Any, pressure: Any) -> sp.Expr:
    """Return the unique stationary radius ``T/P`` of the capillary energy."""

    tension = _positive_quantity(line_tension, "line_tension")
    drive = _positive_quantity(pressure, "pressure")
    return sp.simplify(tension / drive)
