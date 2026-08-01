from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.conserved_moments import (
    axisymmetric_p2_density_second_moments,
    discrete_mass_moments,
    isolated_conserved_stress_moment_rates,
    spherical_density_second_moments,
    symmetric_trace_free,
)


def test_trace_free_projection_is_symmetric_traceless_and_idempotent() -> None:
    matrix = sp.Matrix([[1, 2, 0], [4, 5, 1], [0, 3, 7]])
    projected = symmetric_trace_free(matrix)
    assert projected == projected.T
    assert sp.trace(projected) == 0
    assert symmetric_trace_free(projected) == projected


def test_isolated_moment_rates_preserve_the_factor_two_and_stf_normalization() -> None:
    px, py, pz = sp.symbols("p_x p_y p_z")
    stress = sp.Matrix([[1, 2, 0], [2, 3, 1], [0, 1, 5]])
    rates = isolated_conserved_stress_moment_rates([px, py, pz], stress)
    assert rates.monopole_rate == 0
    assert rates.momentum_rate == sp.zeros(3, 1)
    assert rates.dipole_rate == sp.Matrix([px, py, pz])
    assert rates.dipole_acceleration == sp.zeros(3, 1)
    assert rates.second_moment_acceleration == 2 * stress
    assert rates.trace_free_second_moment_acceleration == symmetric_trace_free(2 * stress)
    assert rates.triple_normalized_quadrupole_acceleration == 3 * symmetric_trace_free(2 * stress)


def test_uniform_translation_has_affine_dipole_and_the_stress_identity() -> None:
    t = sp.symbols("t", real=True)
    masses = [sp.Integer(2), sp.Integer(3)]
    velocities = [sp.Matrix([1, -2, 0]), sp.Matrix([-1, 1, 2])]
    origins = [sp.Matrix([0, 1, 2]), sp.Matrix([2, 0, -1])]
    positions = [origin + velocity * t for origin, velocity in zip(origins, velocities)]
    moments = discrete_mass_moments(masses, positions)
    momentum = sum(
        (mass * velocity for mass, velocity in zip(masses, velocities)),
        sp.zeros(3, 1),
    )
    integrated_stress = sum(
        (
            mass * velocity * velocity.T
            for mass, velocity in zip(masses, velocities)
        ),
        sp.zeros(3),
    )
    rates = isolated_conserved_stress_moment_rates(momentum, integrated_stress)
    assert sp.diff(moments.monopole, t) == 0
    assert sp.diff(moments.dipole, t) == rates.dipole_rate
    assert sp.diff(moments.dipole, t, 2) == rates.dipole_acceleration
    assert sp.diff(moments.second_moment, t, 2) == rates.second_moment_acceleration


def test_source_quadrupole_convention_is_three_times_normalized_stf() -> None:
    moments = discrete_mass_moments([1, 1], [[1, 0, 0], [-1, 0, 0]])
    assert moments.triple_normalized_quadrupole == 3 * moments.trace_free_second_moment
    assert sp.trace(moments.triple_normalized_quadrupole) == 0


def test_a_static_anisotropic_quadrupole_is_not_a_radiation_verdict() -> None:
    t = sp.symbols("t")
    moments = discrete_mass_moments([1, 1], [[1, 0, 0], [-1, 0, 0]])
    assert moments.trace_free_second_moment != sp.zeros(3)
    assert sp.diff(moments.trace_free_second_moment, t, 2) == sp.zeros(3)


def test_spherical_density_has_isotropic_second_moment_and_zero_stf() -> None:
    scalar = sp.symbols("J", real=True)
    moments = spherical_density_second_moments(scalar)
    assert moments.second_moment == scalar * sp.eye(3) / 3
    assert sp.trace(moments.second_moment) == scalar
    assert moments.trace_free_second_moment == sp.zeros(3)
    assert moments.triple_normalized_quadrupole == sp.zeros(3)


def test_axisymmetric_p2_deformation_is_a_sensitive_nonzero_guard() -> None:
    scalar, amplitude = sp.symbols("J a", real=True)
    moments = axisymmetric_p2_density_second_moments(scalar, amplitude)
    assert moments.trace_free_second_moment == sp.diag(
        -amplitude * scalar / 15,
        -amplitude * scalar / 15,
        2 * amplitude * scalar / 15,
    )
    assert moments.triple_normalized_quadrupole == sp.diag(
        -amplitude * scalar / 5,
        -amplitude * scalar / 5,
        2 * amplitude * scalar / 5,
    )
    assert moments.triple_normalized_quadrupole.subs(amplitude, 0) == sp.zeros(3)


@pytest.mark.parametrize(
    ("momentum", "stress", "message"),
    [
        ([1, 2], sp.eye(3), "three components"),
        ([1, 2, 3], sp.eye(2), "3 by 3"),
        ([1, 2, 3], [[1, 1, 0], [0, 1, 0], [0, 0, 1]], "symmetric"),
    ],
)
def test_invalid_moment_inputs_are_rejected(momentum, stress, message) -> None:
    with pytest.raises(ValueError, match=message):
        isolated_conserved_stress_moment_rates(momentum, stress)


def test_discrete_moment_inputs_must_match() -> None:
    with pytest.raises(ValueError, match="equal nonzero length"):
        discrete_mass_moments([1], [])
    with pytest.raises(ValueError, match="three components"):
        discrete_mass_moments([1], [[0, 1]])
