from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.radial_energy import (
    capillary_barrier_height,
    capillary_critical_radius,
    capillary_energy,
    equivalent_quadratic_loading_parameters,
    frank_core_line_tension,
    frank_core_log_sensitivities,
    frank_quadratic_capillary_map,
    line_energy,
    monomial_loading_dimension_ledger,
    quadratic_capillary_identifiability_ledger,
    quadratic_loading_area_drive,
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


def test_capillary_barrier_is_relative_and_core_offset_cancels() -> None:
    radius, tension, pressure, core = sp.symbols(
        "R T P E_core",
        positive=True,
    )
    critical = capillary_critical_radius(tension, pressure)
    energy = capillary_energy(radius, tension, pressure, core)
    relative = sp.simplify(energy.subs(radius, critical) - energy.subs(radius, 0))
    assert capillary_barrier_height(tension, pressure) == sp.pi * tension**2 / pressure
    assert relative == capillary_barrier_height(tension, pressure)
    assert energy.subs(radius, critical) == core + relative


def test_frank_quadratic_capillary_map_retains_every_declared_input() -> None:
    stiffness, outer, core_cutoff, core_energy, coupling, amplitude, wave, thickness = (
        sp.symbols("K_F R_o r_c epsilon g A k l_m", positive=True)
    )
    strength = sp.symbols("s", real=True)
    tension = frank_core_line_tension(
        stiffness,
        strength,
        outer,
        core_cutoff,
        core_energy,
    )
    drive = quadratic_loading_area_drive(coupling, amplitude, wave, thickness)
    result = frank_quadratic_capillary_map(
        stiffness,
        strength,
        outer,
        core_cutoff,
        core_energy,
        coupling,
        amplitude,
        wave,
        thickness,
    )
    assert tension == sp.pi * stiffness * strength**2 * sp.log(outer / core_cutoff) + core_energy
    assert drive == coupling * amplitude**2 * wave**2 * thickness / 2
    assert result.line_tension == tension
    assert result.area_drive == drive
    expected_radius = 2 * tension / (
        coupling * amplitude**2 * wave**2 * thickness
    )
    expected_barrier = 2 * sp.pi * tension**2 / (
        coupling * amplitude**2 * wave**2 * thickness
    )
    assert sp.simplify(result.critical_radius - expected_radius) == 0
    assert sp.simplify(result.barrier_height - expected_barrier) == 0
    assert result.critical_radius.has(tension)
    assert result.barrier_height.has(tension**2)


def test_dimension_family_closes_without_selecting_amplitude_convention_or_law() -> None:
    alpha = sp.symbols("alpha", real=True)
    quadratic = monomial_loading_dimension_ledger(alpha)
    assert quadratic.base_dimensions == ("E", "L")
    assert quadratic.coupling_length_exponent == -2 * alpha - 1
    columns = {
        name: quadratic.dimension_matrix[:, index]
        for index, name in enumerate(quadratic.quantity_names)
    }
    assert columns["coupling"] + 2 * columns["amplitude"] + 2 * columns["wavenumber"] == sp.Matrix([1, -3])
    assert columns["bulk_bias"] + columns["thickness"] == columns["area_drive"]
    assert columns["line_tension"] - columns["area_drive"] == columns["critical_radius"]
    assert 2 * columns["line_tension"] - columns["area_drive"] == columns["barrier_height"]

    linear_amplitude = monomial_loading_dimension_ledger(
        0,
        amplitude_power=1,
        wavenumber_power=2,
    )
    quadratic_dimensionless_amplitude = monomial_loading_dimension_ledger(0)
    assert linear_amplitude.coupling_length_exponent == -1
    assert quadratic_dimensionless_amplitude.coupling_length_exponent == -1
    assert linear_amplitude.amplitude_power != quadratic_dimensionless_amplitude.amplitude_power


def test_identifiability_ledger_separates_effective_tension_from_drive_constituents() -> None:
    ledger = quadratic_capillary_identifiability_ledger()
    assert ledger.parameter_names == (
        "line_tension",
        "coupling",
        "amplitude",
        "wavenumber",
        "thickness",
    )
    assert ledger.exponent_matrix == sp.Matrix(
        [[1, -1, -2, -2, -1], [2, -1, -2, -2, -1]]
    )
    assert ledger.rank == 2
    assert len(ledger.nullspace) == 3
    assert ledger.coordinate_identifiable == (True, False, False, False, False)
    assert ledger.barrier_only_rank == 1
    assert len(ledger.barrier_only_nullspace) == 4
    assert ledger.barrier_only_coordinate_identifiable == (False,) * 5


def test_constructive_drive_rescaling_preserves_radius_and_barrier() -> None:
    coupling, amplitude, wave, thickness = sp.symbols(
        "g A k l_m",
        positive=True,
    )
    amplitude_scale, wave_scale, thickness_scale = sp.symbols(
        "rho_A rho_k rho_l",
        positive=True,
    )
    changed = equivalent_quadratic_loading_parameters(
        coupling,
        amplitude,
        wave,
        thickness,
        amplitude_factor=amplitude_scale,
        wavenumber_factor=wave_scale,
        thickness_factor=thickness_scale,
    )
    assert changed != (coupling, amplitude, wave, thickness)
    assert sp.simplify(
        quadratic_loading_area_drive(*changed)
        - quadratic_loading_area_drive(coupling, amplitude, wave, thickness)
    ) == 0


def test_frank_core_sensitivities_are_state_dependent_and_propagate() -> None:
    stiffness, strength, outer, core, core_energy = sp.symbols(
        "K_F s R_o r_c epsilon",
        positive=True,
    )
    ledger = frank_core_log_sensitivities(
        stiffness,
        strength,
        outer,
        core,
        core_energy,
    )
    parameters = (stiffness, strength, outer, core, core_energy)
    derived = tuple(
        sp.simplify(parameter * sp.diff(ledger.line_tension, parameter) / ledger.line_tension)
        for parameter in parameters
    )
    assert ledger.line_tension_log_elasticities == derived
    assert ledger.critical_radius_log_elasticities == derived
    assert ledger.barrier_height_log_elasticities == tuple(
        sp.simplify(2 * value) for value in derived
    )
    assert any(value.has(core_energy) for value in derived)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: line_energy(0, 1), "radius"),
        (lambda: line_energy(1, -1), "line_density"),
        (lambda: spherical_shell_energy(1, 0), "surface_density"),
        (lambda: capillary_energy(1, 1, 0), "pressure"),
        (lambda: capillary_energy(1, 1, 1, sp.I), "core_energy"),
        (lambda: capillary_critical_radius(-1, 1), "line_tension"),
        (lambda: capillary_barrier_height(1, -1), "pressure"),
        (lambda: frank_core_line_tension(1, 1, 1, 2, 1), "outer_cutoff"),
        (lambda: quadratic_loading_area_drive(1, 0, 1, 1), "amplitude"),
        (lambda: quadratic_loading_area_drive(1, 1, 0, 1), "wavenumber"),
        (
            lambda: equivalent_quadratic_loading_parameters(
                1,
                1,
                1,
                1,
                amplitude_factor=0,
            ),
            "amplitude_factor",
        ),
    ],
)
def test_numeric_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
