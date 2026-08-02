from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.spin1_mean_field import (
    cartesian_to_spin1,
    fixed_density_spin1_selection,
    spin1_cartesian_spin,
    spin1_expectation,
    spin1_invariant_residual,
    spin1_magnitude_squared,
    spin1_matrices,
    spin1_mean_field_energy,
    spin1_norm,
    spin1_orbit_ledger,
    spin1_singlet_amplitude,
    spin1_to_cartesian,
)


def test_standard_spin1_matrices_are_hermitian_and_obey_su2() -> None:
    fx, fy, fz = spin1_matrices()
    zero = sp.zeros(3)
    assert all(matrix.conjugate().T == matrix for matrix in (fx, fy, fz))
    assert sp.simplify(fx * fy - fy * fx - sp.I * fz) == zero
    assert sp.simplify(fy * fz - fz * fy - sp.I * fx) == zero
    assert sp.simplify(fz * fx - fx * fz - sp.I * fy) == zero
    assert sp.simplify(fx**2 + fy**2 + fz**2) == 2 * sp.eye(3)


def test_spherical_cartesian_maps_are_exact_inverses_and_preserve_norm() -> None:
    plus, zero, minus = sp.symbols("z_plus z_zero z_minus", complex=True)
    spinor = sp.ImmutableMatrix([plus, zero, minus])
    cartesian = spin1_to_cartesian(spinor)
    assert cartesian_to_spin1(cartesian).applyfunc(sp.simplify) == spinor
    cartesian_norm = sp.simplify((cartesian.conjugate().T * cartesian)[0])
    assert sp.simplify(cartesian_norm - spin1_norm(spinor)) == 0


def test_cartesian_cross_product_is_the_spin_expectation() -> None:
    ux, uy, uz, vx, vy, vz = sp.symbols("u_x u_y u_z v_x v_y v_z", real=True)
    vector = sp.ImmutableMatrix([ux + sp.I * vx, uy + sp.I * vy, uz + sp.I * vz])
    spinor = cartesian_to_spin1(vector)
    assert all(
        sp.simplify(left - right) == 0
        for left, right in zip(spin1_expectation(spinor), spin1_cartesian_spin(vector))
    )


def test_invariant_and_endpoint_orbits_hold_at_nonunit_density() -> None:
    density = sp.Integer(9)
    polar = sp.ImmutableMatrix([0, sp.sqrt(density), 0])
    ferro = sp.ImmutableMatrix([sp.sqrt(density), 0, 0])
    rotated_polar = sp.ImmutableMatrix([sp.sqrt(density / 2), 0, sp.sqrt(density / 2)])
    rotated_ferro = sp.ImmutableMatrix(
        [sp.sqrt(density) / 2, sp.sqrt(density / 2), sp.sqrt(density) / 2]
    )
    for state in (polar, ferro, rotated_polar, rotated_ferro):
        assert spin1_invariant_residual(state) == 0
        assert spin1_norm(state) == density
    assert spin1_orbit_ledger(polar).projective_orbit == "polar"
    assert spin1_orbit_ledger(rotated_polar).projective_orbit == "polar"
    assert spin1_orbit_ledger(ferro).projective_orbit == "ferromagnetic"
    assert spin1_orbit_ledger(rotated_ferro).projective_orbit == "ferromagnetic"
    assert spin1_magnitude_squared(polar) == 0
    assert spin1_magnitude_squared(ferro) == density**2


def test_singlet_amplitude_distinguishes_endpoints_and_intermediate_states() -> None:
    polar = (0, 1, 0)
    ferro = (1, 0, 0)
    intermediate = (sp.sqrt(3) / 2, 0, sp.Rational(1, 2))
    assert spin1_singlet_amplitude(polar) == 1
    assert spin1_singlet_amplitude(ferro) == 0
    result = spin1_orbit_ledger(intermediate)
    assert result.projective_orbit == "intermediate"
    assert 0 < result.spin_squared < 1
    assert 0 < result.singlet_squared < 1


def test_fixed_density_selection_includes_both_signs_and_zero_boundary() -> None:
    positive = fixed_density_spin1_selection(3, sp.Symbol("c_plus", positive=True))
    negative = fixed_density_spin1_selection(3, sp.Symbol("c_minus", negative=True))
    zero = fixed_density_spin1_selection(3, 0)
    assert positive.attainable_spin_squared == (0, 9)
    assert positive.minimizing_projective_orbits == ("polar",)
    assert positive.polar_minus_ferromagnetic_energy == -9 * positive.coupling / 2
    assert negative.minimizing_projective_orbits == ("ferromagnetic",)
    assert negative.minimum_energy == 9 * negative.coupling / 2
    assert zero.minimizing_projective_orbits == ("all_pure_spin1_rays",)
    assert zero.minimum_energy == zero.maximum_energy == 0


def test_energy_uses_state_density_squared_without_hidden_normalization() -> None:
    coupling = sp.Symbol("c2", real=True)
    unit_ferro = sp.ImmutableMatrix([1, 0, 0])
    scaled_ferro = 2 * unit_ferro
    assert spin1_mean_field_energy(unit_ferro, coupling) == coupling / 2
    assert spin1_mean_field_energy(scaled_ferro, coupling) == 8 * coupling


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: spin1_norm((1, 0)), "three components"),
        (lambda: spin1_orbit_ledger((0, 0, 0)), "positive"),
        (lambda: spin1_orbit_ledger(sp.eye(3)), "three components"),
        (lambda: fixed_density_spin1_selection(0, 1), "positive"),
        (
            lambda: fixed_density_spin1_selection(1, sp.Symbol("c2", real=True)),
            "sign",
        ),
        (lambda: spin1_mean_field_energy((1, 0, 0), sp.I), "real"),
    ],
)
def test_spin1_api_rejects_malformed_or_undecidable_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
