from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.massive_dipoles import (
    massive_triplet_dipole_extrema,
    massive_triplet_dipole_interaction,
    yukawa_radial_hessian,
)


def test_yukawa_hessian_coefficients_and_field_equation_are_exact() -> None:
    radius, mass = sp.symbols("R m", positive=True)
    ledger = yukawa_radial_hessian(radius, mass)
    green = sp.exp(-mass * radius) / (4 * sp.pi * radius)
    assert sp.simplify(ledger.green - green) == 0
    assert sp.simplify(ledger.transverse - sp.diff(green, radius) / radius) == 0
    assert sp.simplify(ledger.longitudinal - sp.diff(green, radius, 2)) == 0
    assert sp.simplify(
        ledger.anisotropic
        - (sp.diff(green, radius, 2) - sp.diff(green, radius) / radius)
    ) == 0
    assert sp.simplify(
        sp.diff(green, radius, 2)
        + 2 * sp.diff(green, radius) / radius
        - mass**2 * green
    ) == 0


def test_declared_orientations_reproduce_global_extrema() -> None:
    radius, mass, stiffness, strength = sp.symbols(
        "R m K P", positive=True
    )
    extrema = massive_triplet_dipole_extrema(
        radius, mass, stiffness, strength
    )
    direction = (0, 0, 1)
    for rotation, expected in (
        (extrema.most_attractive_orientation, extrema.most_attractive_energy),
        (extrema.most_repulsive_orientation, extrema.most_repulsive_energy),
        (extrema.identity_orientation, extrema.identity_energy),
    ):
        interaction = massive_triplet_dipole_interaction(
            radius,
            mass,
            stiffness,
            strength,
            direction,
            rotation,
        )
        assert sp.simplify(interaction.interaction_energy - expected) == 0


def test_identity_and_attractive_channel_have_opposite_signs() -> None:
    radius, mass, stiffness, strength = sp.symbols(
        "R m K P", positive=True
    )
    extrema = massive_triplet_dipole_extrema(
        radius, mass, stiffness, strength
    )
    green = sp.exp(-mass * radius) / (4 * sp.pi * radius)
    assert sp.simplify(
        extrema.identity_energy - strength**2 * mass**2 * green / stiffness
    ) == 0
    assert extrema.most_attractive_energy.could_extract_minus_sign()
    assert extrema.most_attractive_radial_force.could_extract_minus_sign()


def test_force_is_negative_energy_gradient_at_fixed_orientation() -> None:
    radius, mass, stiffness, strength = sp.symbols(
        "R m K P", positive=True
    )
    extrema = massive_triplet_dipole_extrema(
        radius, mass, stiffness, strength
    )
    assert sp.simplify(
        extrema.most_attractive_radial_force
        + sp.diff(extrema.most_attractive_energy, radius)
    ) == 0


def test_simultaneous_spatial_rotation_preserves_the_cross_energy() -> None:
    radius, mass, stiffness, strength = sp.symbols(
        "R m K P", positive=True
    )
    direction = sp.ImmutableMatrix((0, 0, 1))
    relative = sp.ImmutableMatrix(sp.diag(1, -1, -1))
    quarter_turn = sp.ImmutableMatrix(
        ((0, 0, 1), (0, 1, 0), (-1, 0, 0))
    )
    baseline = massive_triplet_dipole_interaction(
        radius, mass, stiffness, strength, direction, relative
    )
    rotated = massive_triplet_dipole_interaction(
        radius,
        mass,
        stiffness,
        strength,
        quarter_turn * direction,
        quarter_turn * relative * quarter_turn.T,
    )
    assert sp.simplify(
        rotated.interaction_energy - baseline.interaction_energy
    ) == 0


def test_massless_and_zero_source_limits_are_explicit() -> None:
    radius, mass, stiffness, strength = sp.symbols(
        "R m K P", positive=True
    )
    extrema = massive_triplet_dipole_extrema(
        radius, mass, stiffness, strength
    )
    assert sp.simplify(
        sp.limit(extrema.most_attractive_energy, mass, 0, dir="+")
        + strength**2 / (2 * sp.pi * stiffness * radius**3)
    ) == 0
    assert sp.simplify(
        sp.limit(extrema.most_attractive_radial_force, mass, 0, dir="+")
        + 3 * strength**2 / (2 * sp.pi * stiffness * radius**4)
    ) == 0
    zero = massive_triplet_dipole_extrema(radius, mass, stiffness, 0)
    assert zero.most_attractive_energy == 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: yukawa_radial_hessian(0, 1), "radius"),
        (lambda: yukawa_radial_hessian(1, -1), "mass"),
        (
            lambda: massive_triplet_dipole_interaction(
                1, 1, 1, 1, (1, 1, 0), sp.eye(3)
            ),
            "unit normalized",
        ),
        (
            lambda: massive_triplet_dipole_interaction(
                1, 1, 1, 1, (0, 0, 1), sp.diag(1, 1, -1)
            ),
            "determinant one",
        ),
    ],
)
def test_invalid_domains_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
