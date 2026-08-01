from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.flux_tube import (
    charge_for_slope_equality,
    endpoint_force_slope,
    endpoint_potential,
    spherical_field,
    tube_energy_slope,
    tube_field_energy,
    uniform_tube_field,
)


def test_fixed_area_flux_gives_distinct_exact_linear_slopes() -> None:
    flux, area, charge, length = sp.symbols("Phi A q L", positive=True)
    assert uniform_tube_field(flux, area) == flux / area
    assert tube_energy_slope(flux, area) == flux**2 / (2 * area)
    assert tube_field_energy(length, flux, area) == flux**2 * length / (
        2 * area
    )
    assert endpoint_force_slope(charge, flux, area) == charge * flux / area
    assert endpoint_potential(length, charge, flux, area) == (
        charge * flux * length / area
    )


def test_energy_and_endpoint_slopes_have_an_explicit_equality_condition() -> None:
    flux, area, charge = sp.symbols("Phi A q", positive=True)
    equality = sp.solve(
        sp.Eq(
            tube_energy_slope(flux, area),
            endpoint_force_slope(charge, flux, area),
        ),
        charge,
    )
    assert equality == [flux / 2]
    assert charge_for_slope_equality(flux) == flux / 2
    assert endpoint_force_slope(flux, flux, area) == 2 * tube_energy_slope(
        flux, area
    )


def test_spherical_spreading_is_not_a_constant_field() -> None:
    flux, radius = sp.symbols("Phi r", positive=True)
    field = spherical_field(flux, radius)
    assert field == flux / (4 * sp.pi * radius**2)
    assert sp.diff(field, radius) != 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: uniform_tube_field(0, 1), "flux"),
        (lambda: uniform_tube_field(1, 0), "cross_section"),
        (lambda: tube_field_energy(0, 1, 1), "length"),
        (lambda: endpoint_force_slope(0, 1, 1), "charge"),
        (lambda: spherical_field(1, 0), "radius"),
    ],
)
def test_positive_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
