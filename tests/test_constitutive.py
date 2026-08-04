from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.constitutive import (
    co_scaled_inverse_permeability,
    co_scaled_permittivity,
    co_scaled_wave_speed,
    lattice_debye_energy,
    lattice_reduced_responses,
    local_wave_speed,
    mechanical_medium_conversion,
    si_constitutive_dimension_ledger,
)


def test_co_scaled_responses_cancel_from_wave_speed() -> None:
    density, thermal, speed = sp.symbols("rho Theta c", positive=True)
    epsilon = co_scaled_permittivity(density, thermal, speed)
    inverse_mu = co_scaled_inverse_permeability(density, thermal)
    assert sp.simplify(epsilon / inverse_mu - 1 / speed**2) == 0
    assert co_scaled_wave_speed(density, thermal, speed) == speed


def test_local_wave_speed_uses_inverse_permeability() -> None:
    assert local_wave_speed(sp.Rational(2, 9), 2) == 3


def test_conditional_lattice_reduction_retains_all_coefficients() -> None:
    action, speed, length, ratio = sp.symbols("S c a kappa", positive=True)
    thermal, epsilon, inverse_mu, mass_density = lattice_reduced_responses(
        action, speed, length, ratio
    )
    assert thermal == ratio * action * speed / length
    assert epsilon == ratio * action / (length**4 * speed)
    assert inverse_mu == ratio * action * speed / length**4
    assert mass_density == ratio * action / (2 * length**4 * speed)
    assert sp.simplify(epsilon / inverse_mu - 1 / speed**2) == 0


def test_declared_debye_energy_keeps_speed_ratio_free() -> None:
    action, speed, length = sp.symbols("S c a", positive=True)
    assert (
        lattice_debye_energy(action, speed, length, 3)
        == 3 * action * speed / length
    )


def test_si_constitutive_dimensions_require_a_dimensioned_conversion() -> None:
    ledger = si_constitutive_dimension_ledger()
    assert ledger.base_dimensions == ("M", "L", "T", "I")
    assert ledger.permittivity == sp.ImmutableMatrix([-1, -3, 4, 2])
    assert ledger.inverse_permeability == sp.ImmutableMatrix([-1, -1, 2, 2])
    assert ledger.mass_density == sp.ImmutableMatrix([1, -3, 0, 0])
    assert ledger.stiffness == ledger.energy_density == sp.ImmutableMatrix(
        [1, -1, -2, 0]
    )
    assert ledger.mechanical_conversion == sp.ImmutableMatrix([2, 0, -4, -2])
    assert ledger.mass_density - ledger.permittivity == ledger.mechanical_conversion
    assert (
        ledger.stiffness - ledger.inverse_permeability
        == ledger.mechanical_conversion
    )
    assert ledger.newton_over_speed_squared == sp.ImmutableMatrix([-1, 1, 0, 0])


def test_common_conversion_preserves_speed_but_not_absolute_scale() -> None:
    epsilon, inverse_mu, conversion, strain, scale = sp.symbols(
        "epsilon mu_inv Lambda xi s", positive=True
    )
    baseline = mechanical_medium_conversion(
        epsilon,
        inverse_mu,
        conversion,
        strain_amplitude=strain,
    )
    rescaled = mechanical_medium_conversion(
        epsilon,
        inverse_mu,
        scale * conversion,
        strain_amplitude=strain,
    )
    assert baseline.mass_density == conversion * epsilon
    assert baseline.stiffness == conversion * inverse_mu
    assert baseline.mechanical_speed_squared == inverse_mu / epsilon
    assert baseline.mechanical_speed_squared == baseline.electromagnetic_speed_squared
    assert baseline.speed_squared_ratio == 1
    assert baseline.strain_energy_density == conversion * inverse_mu * strain**2 / 2
    assert baseline.mass_equivalent_density == conversion * epsilon * strain**2 / 2
    assert rescaled.mechanical_speed_squared == baseline.mechanical_speed_squared
    assert rescaled.mass_density == scale * baseline.mass_density
    assert rescaled.stiffness == scale * baseline.stiffness
    assert rescaled.strain_energy_density == scale * baseline.strain_energy_density


def test_unequal_conversion_factors_change_the_mechanical_wave_speed() -> None:
    epsilon, inverse_mu, inertia, stiffness = sp.symbols(
        "epsilon mu_inv a b", positive=True
    )
    ledger = mechanical_medium_conversion(
        epsilon,
        inverse_mu,
        inertia,
        stiffness_conversion=stiffness,
    )
    assert ledger.speed_squared_ratio == stiffness / inertia
    assert ledger.mechanical_speed_squared == (
        stiffness * inverse_mu / (inertia * epsilon)
    )
    assert sp.solve(
        sp.Eq(
            ledger.mechanical_speed_squared,
            ledger.electromagnetic_speed_squared,
        ),
        stiffness,
    ) == [inertia]


def test_unit_strain_energy_is_not_the_inertial_density() -> None:
    epsilon, inverse_mu, conversion = sp.symbols(
        "epsilon mu_inv Lambda", positive=True
    )
    ledger = mechanical_medium_conversion(epsilon, inverse_mu, conversion)
    assert ledger.mass_equivalent_density == conversion * epsilon / 2
    assert ledger.mass_equivalent_density != ledger.mass_density
    doubled_strain = mechanical_medium_conversion(
        epsilon,
        inverse_mu,
        conversion,
        strain_amplitude=2,
    )
    assert doubled_strain.strain_energy_density == 4 * ledger.strain_energy_density
    assert doubled_strain.mass_equivalent_density == 4 * ledger.mass_equivalent_density


@pytest.mark.parametrize(
    ("kwargs", "exception", "message"),
    [
        ({"permittivity": 0, "inverse_permeability": 1, "inertia_conversion": 1}, ValueError, "permittivity"),
        ({"permittivity": 1, "inverse_permeability": -1, "inertia_conversion": 1}, ValueError, "inverse_permeability"),
        ({"permittivity": 1, "inverse_permeability": 1, "inertia_conversion": 0}, ValueError, "inertia_conversion"),
        ({"permittivity": sp.Rational(1, 2), "inverse_permeability": 1, "inertia_conversion": 1.0}, TypeError, "inertia_conversion"),
        ({"permittivity": 1, "inverse_permeability": 1, "inertia_conversion": 1, "strain_amplitude": 0.5}, TypeError, "strain_amplitude"),
    ],
)
def test_mechanical_conversion_requires_exact_domain_inputs(
    kwargs, exception, message: str
) -> None:
    with pytest.raises(exception, match=message):
        mechanical_medium_conversion(**kwargs)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: co_scaled_permittivity(0, 1, 1), "density"),
        (lambda: co_scaled_inverse_permeability(1, -1), "thermal_scale"),
        (lambda: co_scaled_wave_speed(1, 1, 0), "reference_speed"),
        (lambda: local_wave_speed(-1, 1), "permittivity"),
    ],
)
def test_numeric_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
