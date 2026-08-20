"""Tests for the P239 symmetry-reduced stationary-field implementation."""

from __future__ import annotations

import numpy as np
import pytest
import sympy as sp

from substrate_framework.m5_covariant_action import (
    projector_sigma_hamiltonian_density,
    spectral_cartan_hamiltonian_density,
    spectral_trace_potential,
)
from substrate_framework.m5_stationary_fields import (
    M5RadialParameters,
    m5_axis_representative_densities,
    m5_radial_densities,
    m5_radial_observables,
)


ETA = sp.diag(-1, 1, 1, 1)


def _generator(entries: tuple[tuple[int, int, int], ...]) -> sp.Matrix:
    result = sp.zeros(4)
    for row, column, value in entries:
        result[row, column] = value
    return result


G1 = _generator(((2, 3, -1), (3, 2, 1)))
G2 = _generator(((1, 3, 1), (3, 1, -1)))
G3 = _generator(((1, 2, -1), (2, 1, 1)))


def test_radial_density_matches_direct_exact_action_at_a_point() -> None:
    parameters = M5RadialParameters()
    radius = np.array([2.0, 3.0])
    profiles = np.array(
        [
            [0.2, 0.1],
            [0.8, 0.9],
            [0.4, 0.35],
            [0.1, 0.05],
        ]
    )
    derivatives = np.array(
        [
            [0.07, 0.04],
            [0.03, 0.02],
            [-0.02, -0.01],
            [0.01, 0.005],
        ]
    )
    densities = m5_axis_representative_densities(
        radius, profiles, derivatives, parameters
    )

    r = sp.Integer(2)
    chi = sp.Rational(1, 5)
    chi_prime = sp.Rational(7, 100)
    eigenvalues = tuple(sp.Rational(str(value)) for value in profiles[1:, 0])
    eigenvalue_derivatives = tuple(
        sp.Rational(str(value)) for value in derivatives[1:, 0]
    )
    cosine = sp.cosh(chi)
    sine = sp.sinh(chi)
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = cosine
    boost[0, 1] = boost[1, 0] = sine
    inverse_boost = boost.inv()
    boost_derivative = sp.zeros(4)
    boost_derivative[0, 0] = boost_derivative[1, 1] = sine
    boost_derivative[0, 1] = boost_derivative[1, 0] = cosine
    inverse_boost_derivative = sp.zeros(4)
    inverse_boost_derivative[0, 0] = inverse_boost_derivative[1, 1] = sine
    inverse_boost_derivative[0, 1] = inverse_boost_derivative[1, 0] = -cosine
    diagonal = sp.diag(-4, *eigenvalues)
    diagonal_derivative = sp.diag(0, *eigenvalue_derivatives)
    order_parameter = boost * diagonal * boost
    radial_derivative = (
        chi_prime
        * (boost_derivative * diagonal * boost + boost * diagonal * boost_derivative)
        + boost * diagonal_derivative * boost
    )
    azimuthal_derivative = (G3 * order_parameter + order_parameter * G3.T) / r
    polar_derivative = -(G2 * order_parameter + order_parameter * G2.T) / r
    clock_derivative = G1 * order_parameter + order_parameter * G1.T
    field_derivatives = (
        clock_derivative,
        radial_derivative,
        azimuthal_derivative,
        polar_derivative,
    )
    curvature = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for left in range(4):
        for right in range(4):
            matrix = (
                field_derivatives[left] * ETA * field_derivatives[right]
                - field_derivatives[right] * ETA * field_derivatives[left]
            )
            for internal_left in range(4):
                for internal_right in range(4):
                    curvature[left, right, internal_left, internal_right] = matrix[
                        internal_left, internal_right
                    ]
    inverse_cartan = inverse_boost * inverse_boost
    direct_curvature_and_inertia = spectral_cartan_hamiltonian_density(
        sp.ImmutableDenseNDimArray(curvature), inverse_cartan
    )

    projector_0 = sp.diag(1, 0, 0, 0)
    projector = inverse_boost * projector_0 * boost
    projector_derivatives = (
        sp.zeros(4),
        chi_prime
        * (
            inverse_boost_derivative * projector_0 * boost
            + inverse_boost * projector_0 * boost_derivative
        ),
        (G3 * projector - projector * G3) / r,
        -(G2 * projector - projector * G2) / r,
    )
    direct_projector = projector_sigma_hamiltonian_density(projector_derivatives, 1)
    direct_potential = spectral_trace_potential(
        diagonal,
        (4, 1, sp.Rational(3, 10), 0),
        metric_covariant=ETA,
    )

    np.testing.assert_allclose(
        densities.curvature[0] + densities.inertia[0],
        float(direct_curvature_and_inertia),
        rtol=2.0e-13,
        atol=2.0e-13,
    )
    np.testing.assert_allclose(
        densities.projector[0], float(direct_projector), rtol=2.0e-13
    )
    np.testing.assert_allclose(
        densities.potential[0], float(direct_potential), rtol=2.0e-13
    )


def test_projector_density_has_the_expected_radial_hedgehog_form() -> None:
    parameters = M5RadialParameters(projector_stiffness=3.0)
    radius = np.array([1.5, 2.5])
    rapidity = np.array([0.2, -0.3])
    rapidity_prime = np.array([0.07, -0.04])
    profiles = np.vstack((rapidity, np.ones(2), np.full(2, 0.3), np.zeros(2)))
    derivatives = np.vstack((rapidity_prime, np.zeros((3, 2))))
    densities = m5_axis_representative_densities(
        radius, profiles, derivatives, parameters
    )
    expected = 3.0 * (rapidity_prime**2 + 2.0 * np.sinh(rapidity) ** 2 / radius**2)
    np.testing.assert_allclose(densities.projector, expected, rtol=2.0e-13)


def test_angular_average_matches_axis_for_a_genuinely_spherical_profile() -> None:
    parameters = M5RadialParameters(spatial_eigenvalues=(1.0, 0.3, 0.3))
    radius = np.array([1.5, 2.5])
    profiles = np.array([[0.2, 0.1], [0.8, 0.9], [0.4, 0.35], [0.4, 0.35]])
    derivatives = np.array([[0.07, 0.04], [0.03, 0.02], [-0.02, -0.01], [-0.02, -0.01]])
    representative = m5_axis_representative_densities(
        radius, profiles, derivatives, parameters
    )
    averaged = m5_radial_densities(
        radius,
        profiles,
        derivatives,
        parameters,
        polar_quadrature_count=5,
        azimuthal_quadrature_count=10,
    )
    for name in ("projector", "curvature", "potential", "inertia"):
        np.testing.assert_allclose(
            getattr(averaged, name),
            getattr(representative, name),
            rtol=2.0e-12,
            atol=2.0e-12,
        )


def test_fixed_j_observables_use_the_derived_inertia_relation() -> None:
    radius = np.linspace(0.1, 4.0, 80)
    rapidity = 0.2 * radius * np.exp(-radius)
    profiles = np.vstack(
        (
            rapidity,
            np.ones_like(radius),
            np.full_like(radius, 0.3),
            np.zeros_like(radius),
        )
    )
    derivatives = np.vstack(
        (
            0.2 * (1.0 - radius) * np.exp(-radius),
            np.zeros((3, radius.size)),
        )
    )
    densities = m5_radial_densities(radius, profiles, derivatives)
    observables = m5_radial_observables(radius, densities, angular_momentum=5.0)

    assert observables.inertia > 0.0
    assert observables.frequency == pytest.approx(5.0 / (2.0 * observables.inertia))
    assert observables.rotational_energy == pytest.approx(
        25.0 / (4.0 * observables.inertia)
    )
    assert observables.total_energy == pytest.approx(
        observables.static_energy + observables.rotational_energy
    )


def test_radial_inputs_reject_the_wrong_branch_and_zero_momentum() -> None:
    with pytest.raises(ValueError, match="must be simple"):
        M5RadialParameters(timelike_eigenvalue=1.0)
    radius = np.array([1.0, 2.0])
    profiles = np.vstack((np.zeros(2), np.ones(2), np.full(2, 0.3), np.zeros(2)))
    derivatives = np.zeros((4, 2))
    densities = m5_radial_densities(radius, profiles, derivatives)
    with pytest.raises(ValueError, match="angular_momentum"):
        m5_radial_observables(radius, densities, angular_momentum=0.0)
