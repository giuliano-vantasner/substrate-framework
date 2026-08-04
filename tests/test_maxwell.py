from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.maxwell import (
    maxwell_euler_lagrange,
    static_maxwell_point_source,
)


def test_declared_maxwell_action_varies_to_the_sourced_equation() -> None:
    time, x, y = sp.symbols("t x y", real=True)
    coordinates = (time, x, y)
    potential = tuple(
        sp.Function(f"A{index}")(*coordinates) for index in range(3)
    )
    current = tuple(
        sp.Function(f"j{index}")(*coordinates) for index in range(3)
    )
    kappa = sp.Symbol("kappa", positive=True)
    ledger = maxwell_euler_lagrange(
        potential,
        current,
        coordinates,
        sp.diag(1, -1, -1),
        kappa,
    )

    assert all(residual == 0 for residual in ledger.derivation_residuals)
    assert all(residual == 0 for residual in ledger.bianchi_residuals)
    assert ledger.continuity_identity == 0
    assert ledger.source_only_euler_residuals == tuple(-entry for entry in current)
    assert ledger.field_strength == -ledger.field_strength.T


def test_static_potential_sign_follows_the_same_action_convention() -> None:
    time, x = sp.symbols("t x", real=True)
    temporal_potential = sp.Function("A0")(time, x)
    phi = sp.Function("phi")(x)
    spatial_potential = sp.Function("A1")(time, x)
    rho = sp.Function("rho")(x)
    kappa = sp.Symbol("kappa", positive=True)

    general = maxwell_euler_lagrange(
        (temporal_potential, spatial_potential),
        (rho, 0),
        (time, x),
        sp.diag(1, -1),
        kappa,
    )
    correct_static = sp.simplify(
        general.expected_field_equation_residuals[0]
        .subs(spatial_potential, 0)
        .subs(temporal_potential, phi)
        .doit()
    )
    assert correct_static == -kappa * sp.diff(phi, x, 2) - rho

    wrong_static = sp.simplify(
        general.expected_field_equation_residuals[0]
        .subs(spatial_potential, 0)
        .subs(temporal_potential, -phi)
        .doit()
    )
    assert wrong_static == kappa * sp.diff(phi, x, 2) - rho
    assert wrong_static != correct_static


def test_three_dimensional_point_source_has_source_normalized_coulomb_force() -> None:
    radius = sp.Symbol("r", positive=True)
    source, probe, kappa = sp.symbols("Q q kappa", positive=True)
    ledger = static_maxwell_point_source(3, radius, source, probe, kappa)

    assert ledger.unit_sphere_area == 4 * sp.pi
    assert ledger.potential == source / (4 * sp.pi * kappa * radius)
    assert ledger.radial_electric_field == source / (
        4 * sp.pi * kappa * radius**2
    )
    assert ledger.potential_energy == source * probe / (
        4 * sp.pi * kappa * radius
    )
    assert ledger.radial_force == source * probe / (
        4 * sp.pi * kappa * radius**2
    )
    assert ledger.radial_harmonic_residual == 0
    assert ledger.normalized_source_flux == source
    assert ledger.decays_at_infinity
    assert ledger.inverse_square_force


def test_decay_does_not_uniquely_select_three_spatial_dimensions() -> None:
    radius = sp.Symbol("r", positive=True)
    source, probe, kappa = sp.symbols("Q q kappa", positive=True)
    three = static_maxwell_point_source(3, radius, source, probe, kappa)
    four = static_maxwell_point_source(4, radius, source, probe, kappa)

    assert three.decays_at_infinity and four.decays_at_infinity
    assert three.inverse_square_force and not four.inverse_square_force
    assert four.unit_sphere_area == 2 * sp.pi**2
    assert four.potential == source / (4 * sp.pi**2 * kappa * radius**2)
    assert four.radial_electric_field == source / (
        2 * sp.pi**2 * kappa * radius**3
    )
    assert sp.limit(four.potential, radius, sp.oo) == 0
    assert four.normalized_source_flux == source


def test_two_and_one_dimensional_branches_keep_boundary_data_explicit() -> None:
    radius = sp.Symbol("r", positive=True)
    reference = sp.Symbol("r0", positive=True)
    source, probe, kappa, phi0 = sp.symbols(
        "Q q kappa phi0", positive=True
    )
    two = static_maxwell_point_source(
        2,
        radius,
        source,
        probe,
        kappa,
        reference_radius=reference,
        reference_potential=phi0,
    )
    one = static_maxwell_point_source(
        1,
        radius,
        source,
        probe,
        kappa,
        reference_potential=phi0,
    )

    assert two.potential == phi0 - source * sp.log(radius / reference) / (
        2 * sp.pi * kappa
    )
    assert two.radial_electric_field == source / (2 * sp.pi * kappa * radius)
    assert two.normalized_source_flux == source
    assert two.radial_harmonic_residual == 0
    assert not two.decays_at_infinity
    assert two.potential_radial_power is None

    assert one.potential == phi0 - source * radius / (2 * kappa)
    assert one.radial_electric_field == source / (2 * kappa)
    assert one.normalized_source_flux == source
    assert one.radial_harmonic_residual == 0
    assert not one.decays_at_infinity


def test_source_probe_and_kinetic_mutations_move_distinct_outputs() -> None:
    radius = sp.Symbol("r", positive=True)
    baseline = static_maxwell_point_source(3, radius, 2, 3, 5)
    reversed_source = static_maxwell_point_source(3, radius, -2, 3, 5)
    reversed_probe = static_maxwell_point_source(3, radius, 2, -3, 5)
    doubled_kinetic = static_maxwell_point_source(3, radius, 2, 3, 10)
    zero_source = static_maxwell_point_source(3, radius, 0, 3, 5)
    zero_probe = static_maxwell_point_source(3, radius, 2, 0, 5)

    assert reversed_source.radial_electric_field == -baseline.radial_electric_field
    assert reversed_source.radial_force == -baseline.radial_force
    assert reversed_probe.radial_electric_field == baseline.radial_electric_field
    assert reversed_probe.radial_force == -baseline.radial_force
    assert doubled_kinetic.radial_electric_field == baseline.radial_electric_field / 2
    assert doubled_kinetic.radial_force == baseline.radial_force / 2
    assert zero_source.radial_electric_field == zero_source.radial_force == 0
    assert zero_probe.radial_electric_field == baseline.radial_electric_field
    assert zero_probe.radial_force == 0


def test_maxwell_api_rejects_hidden_domain_and_boundary_choices() -> None:
    radius = sp.Symbol("r", positive=True)
    with pytest.raises(TypeError, match="integer"):
        static_maxwell_point_source(sp.Symbol("d"), radius, 1, 1)
    with pytest.raises(ValueError, match="positive"):
        static_maxwell_point_source(0, radius, 1, 1)
    with pytest.raises(ValueError, match="reference radius"):
        static_maxwell_point_source(2, radius, 1, 1)
    with pytest.raises(ValueError, match="zero-at-infinity"):
        static_maxwell_point_source(3, radius, 1, 1, reference_potential=1)
    with pytest.raises(ValueError, match="kinetic coefficient"):
        static_maxwell_point_source(3, radius, 1, 1, 0)

    time, x = sp.symbols("t x", real=True)
    potential = (
        sp.Function("A0")(time, x),
        sp.Function("A1")(time, x),
    )
    current = (
        sp.Function("j0")(time, x),
        sp.Function("j1")(time, x),
    )
    with pytest.raises(ValueError, match="symmetric"):
        maxwell_euler_lagrange(
            potential,
            current,
            (time, x),
            sp.Matrix([[1, 1], [0, -1]]),
        )
    with pytest.raises(ValueError, match="invertible"):
        maxwell_euler_lagrange(
            potential,
            current,
            (time, x),
            sp.diag(1, 0),
        )
