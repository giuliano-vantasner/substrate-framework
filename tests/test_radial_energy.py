from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.radial_energy import (
    capillary_critical_radius,
    capillary_energy,
    line_energy,
    spherical_shell_energy,
)


def test_exact_radial_energy_forms() -> None:
    radius, line_density, surface_density = sp.symbols(
        "R lambda sigma", positive=True
    )
    assert line_energy(radius, line_density) == 2 * sp.pi * radius * line_density
    assert spherical_shell_energy(radius, surface_density) == (
        4 * sp.pi * radius**2 * surface_density
    )


def test_capillary_critical_radius_is_a_strict_maximum() -> None:
    radius, tension, pressure = sp.symbols("R T P", positive=True)
    energy = capillary_energy(radius, tension, pressure)
    critical = capillary_critical_radius(tension, pressure)
    assert critical == tension / pressure
    assert sp.simplify(sp.diff(energy, radius).subs(radius, critical)) == 0
    assert sp.diff(energy, radius, 2) == -2 * sp.pi * pressure


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: line_energy(0, 1), "radius"),
        (lambda: line_energy(1, -1), "line_density"),
        (lambda: spherical_shell_energy(1, 0), "surface_density"),
        (lambda: capillary_energy(1, 1, 0), "pressure"),
        (lambda: capillary_energy(1, 1, 1, sp.I), "core_energy"),
        (lambda: capillary_critical_radius(-1, 1), "line_tension"),
    ],
)
def test_numeric_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
