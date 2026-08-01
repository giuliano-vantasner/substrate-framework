from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.gauge_u1 import (
    finite_energy_winding_flux,
    gauged_scalar_kinetic_density,
    local_u1_transform,
    u1_covariant_commutator,
    u1_covariant_derivative,
    u1_field_strength,
    u1_holonomy,
)
from substrate_framework.u1_charge import u1_current_components


def test_arbitrary_local_transform_is_exactly_covariant() -> None:
    time, coordinate, coupling = sp.symbols("t x e", real=True, positive=True)
    field = sp.Function("Psi")(time, coordinate)
    chi = sp.Function("chi")(time, coordinate)
    a0 = sp.Function("A0")(time, coordinate)
    a1 = sp.Function("A1")(time, coordinate)
    transformed, transformed_connections = local_u1_transform(
        field, (a0, a1), chi, (time, coordinate), coupling
    )
    phase = sp.exp(sp.I * coupling * chi)
    for connection, transformed_connection, variable in zip(
        (a0, a1), transformed_connections, (time, coordinate), strict=True
    ):
        assert sp.simplify(
            u1_covariant_derivative(
                transformed, transformed_connection, variable, coupling
            )
            - phase
            * u1_covariant_derivative(field, connection, variable, coupling)
        ) == 0


def test_gauged_kinetic_density_is_invariant_and_sign_closed() -> None:
    time, coordinate, coupling = sp.symbols("t x e", real=True, positive=True)
    field = sp.Function("Psi")(time, coordinate)
    conjugate = sp.Function("Psi_conj")(time, coordinate)
    chi = sp.Function("chi")(time, coordinate)
    a0 = sp.Function("A0")(time, coordinate)
    a1 = sp.Function("A1")(time, coordinate)
    transformed, transformed_connections = local_u1_transform(
        field, (a0, a1), chi, (time, coordinate), coupling
    )
    transformed_conjugate = sp.exp(-sp.I * coupling * chi) * conjugate
    original = gauged_scalar_kinetic_density(
        field, conjugate, (a0, a1), (time, coordinate), coupling
    )
    changed = gauged_scalar_kinetic_density(
        transformed,
        transformed_conjugate,
        transformed_connections,
        (time, coordinate),
        coupling,
    )
    assert sp.simplify(changed - original) == 0

    bare = gauged_scalar_kinetic_density(
        field, conjugate, (0, 0), (time, coordinate), coupling
    )
    current0, current1 = u1_current_components(
        field, conjugate, coordinate, time
    )
    expected = coupling * (a0 * current0 + a1 * current1) + coupling**2 * (
        a0**2 - a1**2
    ) * field * conjugate
    assert sp.simplify(original - bare - expected) == 0


def test_curvature_is_invariant_and_controls_the_commutator() -> None:
    time, coordinate, coupling = sp.symbols("t x e", real=True, positive=True)
    field = sp.Function("Psi")(time, coordinate)
    chi = sp.Function("chi")(time, coordinate)
    a0 = sp.Function("A0")(time, coordinate)
    a1 = sp.Function("A1")(time, coordinate)
    _, transformed_connections = local_u1_transform(
        field, (a0, a1), chi, (time, coordinate), coupling
    )
    curvature = u1_field_strength(a0, a1, time, coordinate)
    assert sp.simplify(
        u1_field_strength(*transformed_connections, time, coordinate)
        - curvature
    ) == 0
    assert sp.simplify(
        u1_covariant_commutator(
            field, a0, a1, time, coordinate, coupling
        )
        + sp.I * coupling * curvature * field
    ) == 0

    potential = sp.Function("chi0")(time, coordinate)
    assert u1_field_strength(
        sp.diff(potential, time),
        sp.diff(potential, coordinate),
        time,
        coordinate,
    ) == 0
    assert u1_field_strength(0, time, time, coordinate) == 1


def test_integer_winding_flux_has_trivial_matter_holonomy() -> None:
    winding = sp.symbols("N", integer=True)
    coupling = sp.symbols("e", positive=True)
    flux = finite_energy_winding_flux(winding, coupling)
    assert flux == 2 * sp.pi * winding / coupling
    assert u1_holonomy(flux.subs(winding, 1), coupling) == 1
    assert u1_holonomy(sp.pi / coupling, coupling) == -1
    with pytest.raises(ValueError, match="integer"):
        finite_energy_winding_flux(sp.Rational(1, 2), coupling)


@pytest.mark.parametrize(
    "call",
    [
        lambda: u1_covariant_derivative(1, 1, sp.Symbol("x"), 0),
        lambda: finite_energy_winding_flux(1, 0),
        lambda: u1_holonomy(1, 0),
    ],
)
def test_coupling_must_be_positive(call) -> None:
    with pytest.raises(ValueError, match="coupling"):
        call()
