"""Symmetry-reduced stationary fields for the conditional P239 M5 action.

The ansatz is a Lorentz-orbit biaxial hedgehog.  At ``t=0`` and on the
positive x axis its covariant order parameter is

``M = B_1(chi) diag(-g, lambda_1, lambda_2, lambda_3) B_1(chi)^T``.

Spatial rotations carry this representative to every angular direction;
rotation about the radial first eigenaxis is the clock coordinate.  The four
radial profiles ``(chi, lambda_1, lambda_2, lambda_3)`` are varied.  Regularity
requires ``chi(0)=0`` and coincident spatial eigenvalues at the origin.  The
vacuum values are imposed at the outer boundary.

This module is proposal infrastructure, not accepted framework authority.
It deliberately exposes the density decomposition and solver diagnostics so
claim-level evidence can apply mesh, domain, basis, and mutation oracles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

from .numerics import NumericalFailure, trapezoid_integral


FloatArray = NDArray[np.float64]
_ETA = np.diag([-1.0, 1.0, 1.0, 1.0])
_P0 = np.diag([1.0, 0.0, 0.0, 0.0])


def _generator(entries: Sequence[tuple[int, int, float]]) -> FloatArray:
    result = np.zeros((4, 4), dtype=np.float64)
    for row, column, value in entries:
        result[row, column] = value
    return result


_CLOCK_GENERATOR = _generator(((2, 3, -1.0), (3, 2, 1.0)))
_POLAR_GENERATOR = _generator(((1, 3, 1.0), (3, 1, -1.0)))
_AZIMUTHAL_GENERATOR = _generator(((1, 2, -1.0), (2, 1, 1.0)))


@dataclass(frozen=True)
class M5RadialParameters:
    """Coefficients and preferred spectrum for the radial P239 action."""

    timelike_eigenvalue: float = 4.0
    spatial_eigenvalues: tuple[float, float, float] = (1.0, 0.3, 0.0)
    projector_stiffness: float = 1.0
    spectrum_weights: tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    boost_axis: int = 1

    def __post_init__(self) -> None:
        values = np.asarray(
            (
                self.timelike_eigenvalue,
                *self.spatial_eigenvalues,
                self.projector_stiffness,
                *self.spectrum_weights,
            ),
            dtype=np.float64,
        )
        if not np.all(np.isfinite(values)):
            raise ValueError("M5 radial parameters must be finite")
        if self.projector_stiffness <= 0.0:
            raise ValueError("projector_stiffness must be positive")
        if any(weight <= 0.0 for weight in self.spectrum_weights):
            raise ValueError("spectrum_weights must be positive")
        if any(
            self.timelike_eigenvalue == spatial for spatial in self.spatial_eigenvalues
        ):
            raise ValueError("the selected timelike eigenvalue must be simple")
        if self.boost_axis not in (1, 2, 3):
            raise ValueError("boost_axis must be one of the three spatial axes")


@dataclass(frozen=True)
class M5RadialDensities:
    """Pointwise inertial-frame energy components of the radial ansatz."""

    projector: FloatArray
    curvature: FloatArray
    potential: FloatArray
    inertia: FloatArray

    @property
    def static(self) -> FloatArray:
        return self.projector + self.curvature + self.potential


@dataclass(frozen=True)
class M5RadialObservables:
    """Integrated static and fixed-angular-momentum observables."""

    static_energy: float
    projector_energy: float
    curvature_energy: float
    potential_energy: float
    inertia: float
    angular_momentum: float
    rotational_energy: float
    total_energy: float
    frequency: float


@dataclass(frozen=True)
class M5RadialSolution:
    """A relaxed spline profile with explicit numerical diagnostics."""

    control_radius: FloatArray
    control_values: FloatArray
    radius: FloatArray
    profiles: FloatArray
    profile_derivatives: FloatArray
    observables: M5RadialObservables
    optimizer_success: bool
    optimizer_message: str
    iterations: int
    function_evaluations: int
    stationarity_inf_norm: float
    selected_branch_gap: float


def _real_vector(values: ArrayLike, name: str) -> FloatArray:
    result = np.asarray(values, dtype=np.float64)
    if result.ndim != 1 or result.size < 2:
        raise ValueError(
            f"{name} must be a one-dimensional array with at least two points"
        )
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be finite")
    return result


def _profile_arrays(
    values: ArrayLike, derivatives: ArrayLike, size: int
) -> tuple[FloatArray, FloatArray]:
    profiles = np.asarray(values, dtype=np.float64)
    slopes = np.asarray(derivatives, dtype=np.float64)
    if profiles.shape != (4, size) or slopes.shape != (4, size):
        raise ValueError(
            "profiles and derivatives must both have shape (4, len(radius))"
        )
    if not np.all(np.isfinite(profiles)) or not np.all(np.isfinite(slopes)):
        raise ValueError("profiles and derivatives must be finite")
    return profiles, slopes


def _batch_action(generator: FloatArray, matrices: FloatArray) -> FloatArray:
    return np.matmul(generator, matrices) + np.matmul(matrices, generator.T)


def _batch_commutator(left: FloatArray, right: FloatArray) -> FloatArray:
    return np.matmul(np.matmul(left, _ETA), right) - np.matmul(
        np.matmul(right, _ETA), left
    )


def _internal_cartan_norm(
    curvature: FloatArray, inverse_cartan: FloatArray
) -> FloatArray:
    return np.einsum(
        "nab,ncd,nac,nbd->n",
        curvature,
        curvature,
        inverse_cartan,
        inverse_cartan,
        optimize=True,
    )


def m5_axis_representative_densities(
    radius: ArrayLike,
    profiles: ArrayLike,
    profile_derivatives: ArrayLike,
    parameters: M5RadialParameters = M5RadialParameters(),
) -> M5RadialDensities:
    """Evaluate one positive-x-axis representative of the hedgehog density.

    Profile order is ``(chi, lambda_1, lambda_2, lambda_3)``.  The returned
    inertia multiplies ``omega**2`` in the Hamiltonian.  This is useful for
    exact component tests.  It equals the angular average only when the
    configuration is genuinely spherical; a biaxial moving frame generally
    is not, so stationary calculations use :func:`m5_radial_densities`.
    """

    points = _real_vector(radius, "radius")
    if np.any(points <= 0.0) or np.any(np.diff(points) <= 0.0):
        raise ValueError("radius must be strictly positive and increasing")
    values, slopes = _profile_arrays(profiles, profile_derivatives, points.size)
    rapidity, lambda_1, lambda_2, lambda_3 = values
    rapidity_prime, lambda_1_prime, lambda_2_prime, lambda_3_prime = slopes
    sample_count = points.size

    cosine = np.cosh(rapidity)
    sine = np.sinh(rapidity)
    boost_axis = parameters.boost_axis
    boost = np.broadcast_to(np.eye(4), (sample_count, 4, 4)).copy()
    boost[:, 0, 0] = boost[:, boost_axis, boost_axis] = cosine
    boost[:, 0, boost_axis] = boost[:, boost_axis, 0] = sine
    inverse_boost = np.broadcast_to(np.eye(4), (sample_count, 4, 4)).copy()
    inverse_boost[:, 0, 0] = inverse_boost[:, boost_axis, boost_axis] = cosine
    inverse_boost[:, 0, boost_axis] = inverse_boost[:, boost_axis, 0] = -sine
    boost_derivative = np.zeros_like(boost)
    boost_derivative[:, 0, 0] = boost_derivative[:, boost_axis, boost_axis] = sine
    boost_derivative[:, 0, boost_axis] = boost_derivative[:, boost_axis, 0] = cosine
    inverse_boost_derivative = np.zeros_like(boost)
    inverse_boost_derivative[:, 0, 0] = inverse_boost_derivative[
        :, boost_axis, boost_axis
    ] = sine
    inverse_boost_derivative[:, 0, boost_axis] = inverse_boost_derivative[
        :, boost_axis, 0
    ] = -cosine

    diagonal = np.zeros_like(boost)
    diagonal[:, 0, 0] = -parameters.timelike_eigenvalue
    diagonal[:, 1, 1] = lambda_1
    diagonal[:, 2, 2] = lambda_2
    diagonal[:, 3, 3] = lambda_3
    diagonal_derivative = np.zeros_like(boost)
    diagonal_derivative[:, 1, 1] = lambda_1_prime
    diagonal_derivative[:, 2, 2] = lambda_2_prime
    diagonal_derivative[:, 3, 3] = lambda_3_prime

    order_parameter = np.matmul(np.matmul(boost, diagonal), boost)
    radial_derivative = rapidity_prime[:, None, None] * (
        np.matmul(np.matmul(boost_derivative, diagonal), boost)
        + np.matmul(np.matmul(boost, diagonal), boost_derivative)
    ) + np.matmul(np.matmul(boost, diagonal_derivative), boost)
    azimuthal_derivative = (
        _batch_action(_AZIMUTHAL_GENERATOR, order_parameter) / points[:, None, None]
    )
    polar_derivative = (
        -_batch_action(_POLAR_GENERATOR, order_parameter) / points[:, None, None]
    )
    clock_derivative = _batch_action(_CLOCK_GENERATOR, order_parameter)
    field_derivatives = (
        clock_derivative,
        radial_derivative,
        azimuthal_derivative,
        polar_derivative,
    )
    inverse_cartan = np.matmul(inverse_boost, inverse_boost)

    curvature_density = np.zeros(sample_count)
    inertia_density = np.zeros(sample_count)
    for left in range(1, 4):
        for right in range(left + 1, 4):
            curvature = _batch_commutator(
                field_derivatives[left], field_derivatives[right]
            )
            curvature_density += _internal_cartan_norm(curvature, inverse_cartan)
    for spatial in range(1, 4):
        curvature = _batch_commutator(field_derivatives[0], field_derivatives[spatial])
        inertia_density += _internal_cartan_norm(curvature, inverse_cartan)

    projector = np.matmul(np.matmul(inverse_boost, _P0), boost)
    radial_projector = rapidity_prime[:, None, None] * (
        np.matmul(np.matmul(inverse_boost_derivative, _P0), boost)
        + np.matmul(np.matmul(inverse_boost, _P0), boost_derivative)
    )
    azimuthal_projector = (
        np.matmul(_AZIMUTHAL_GENERATOR, projector)
        - np.matmul(projector, _AZIMUTHAL_GENERATOR)
    ) / points[:, None, None]
    polar_projector = (
        -(
            np.matmul(_POLAR_GENERATOR, projector)
            - np.matmul(projector, _POLAR_GENERATOR)
        )
        / points[:, None, None]
    )
    clock_projector = np.matmul(_CLOCK_GENERATOR, projector) - np.matmul(
        projector, _CLOCK_GENERATOR
    )
    projector_density = parameters.projector_stiffness * sum(
        -0.5 * np.einsum("nab,nba->n", derivative, derivative)
        for derivative in (
            radial_projector,
            azimuthal_projector,
            polar_projector,
        )
    )
    inertia_density += (
        -0.5
        * parameters.projector_stiffness
        * np.einsum("nab,nba->n", clock_projector, clock_projector)
    )

    local_eigenvalues = np.stack(
        (
            np.full(sample_count, parameters.timelike_eigenvalue),
            lambda_1,
            lambda_2,
            lambda_3,
        ),
        axis=1,
    )
    target_eigenvalues = np.asarray(
        (parameters.timelike_eigenvalue, *parameters.spatial_eigenvalues)
    )
    potential_density = np.zeros(sample_count)
    for power, weight in enumerate(parameters.spectrum_weights, start=1):
        residual = np.sum(local_eigenvalues**power, axis=1) - np.sum(
            target_eigenvalues**power
        )
        potential_density += weight * residual**2

    arrays = (
        projector_density,
        curvature_density,
        potential_density,
        inertia_density,
    )
    if not all(np.all(np.isfinite(array)) for array in arrays):
        raise NumericalFailure("radial density evaluation became non-finite")
    return M5RadialDensities(*arrays)


def _rotation_from_generator(generator: FloatArray, angle: FloatArray) -> FloatArray:
    generator_squared = generator @ generator
    return (
        np.eye(4)[None]
        + np.sin(angle)[:, None, None] * generator[None]
        + (1.0 - np.cos(angle))[:, None, None] * generator_squared[None]
    )


def _rotation_derivative(generator: FloatArray, angle: FloatArray) -> FloatArray:
    generator_squared = generator @ generator
    return (
        np.cos(angle)[:, None, None] * generator[None]
        + np.sin(angle)[:, None, None] * generator_squared[None]
    )


def _angular_frame_quadrature(
    polar_count: int, azimuthal_count: int
) -> tuple[
    FloatArray, FloatArray, FloatArray, tuple[FloatArray, FloatArray, FloatArray]
]:
    if polar_count < 2 or azimuthal_count < 4:
        raise ValueError(
            "angular quadrature requires polar_count>=2 and azimuthal_count>=4"
        )
    cosine_polar, polar_weights = np.polynomial.legendre.leggauss(polar_count)
    azimuth = (np.arange(azimuthal_count) + 0.5) * 2.0 * np.pi / azimuthal_count
    u, phi = np.meshgrid(cosine_polar, azimuth, indexing="ij")
    u = u.ravel()
    phi = phi.ravel()
    weights = np.repeat(polar_weights[:, None], azimuthal_count, axis=1).ravel() * (
        2.0 * np.pi / azimuthal_count
    )
    transverse = np.sqrt(1.0 - u**2)
    directions = np.stack(
        (transverse * np.cos(phi), transverse * np.sin(phi), u), axis=1
    )
    polar_angle = -np.arctan2(u, transverse)
    rotation_z = _rotation_from_generator(_AZIMUTHAL_GENERATOR, phi)
    rotation_y = _rotation_from_generator(_POLAR_GENERATOR, polar_angle)
    derivative_z = _rotation_derivative(_AZIMUTHAL_GENERATOR, phi)
    derivative_y = _rotation_derivative(_POLAR_GENERATOR, polar_angle)
    frame = np.matmul(rotation_z, rotation_y)

    rho = transverse
    gradient_phi = np.stack(
        (-np.sin(phi) / rho, np.cos(phi) / rho, np.zeros_like(phi)), axis=1
    )
    gradient_theta = np.stack(
        (
            u * np.cos(phi),
            u * np.sin(phi),
            -rho,
        ),
        axis=1,
    )
    frame_derivatives = []
    for axis in range(3):
        frame_derivatives.append(
            np.matmul(derivative_z, rotation_y) * gradient_phi[:, axis, None, None]
            + np.matmul(rotation_z, derivative_y) * gradient_theta[:, axis, None, None]
        )
    return directions, weights, frame, tuple(frame_derivatives)


def m5_radial_densities(
    radius: ArrayLike,
    profiles: ArrayLike,
    profile_derivatives: ArrayLike,
    parameters: M5RadialParameters = M5RadialParameters(),
    *,
    polar_quadrature_count: int = 4,
    azimuthal_quadrature_count: int = 8,
) -> M5RadialDensities:
    """Angular-average the exact selected action on the biaxial hedgehog.

    The moving frame is ``R_z(phi) R_y(theta) R_x(omega t)`` and the boost is
    applied along the selected eigenframe axis.  Cartesian derivatives include
    the full angular connection before contraction.  Gauss--Legendre nodes
    avoid the coordinate poles; periodic midpoint nodes cover azimuth.
    """

    points = _real_vector(radius, "radius")
    if np.any(points <= 0.0) or np.any(np.diff(points) <= 0.0):
        raise ValueError("radius must be strictly positive and increasing")
    values, slopes = _profile_arrays(profiles, profile_derivatives, points.size)
    rapidity, lambda_1, lambda_2, lambda_3 = values
    rapidity_prime, lambda_1_prime, lambda_2_prime, lambda_3_prime = slopes
    radial_count = points.size
    directions, angular_weights, frame, frame_derivatives = _angular_frame_quadrature(
        polar_quadrature_count, azimuthal_quadrature_count
    )
    direction_count = directions.shape[0]

    cosine = np.cosh(rapidity)
    sine = np.sinh(rapidity)
    boost_axis = parameters.boost_axis
    boost = np.broadcast_to(np.eye(4), (radial_count, 4, 4)).copy()
    boost[:, 0, 0] = boost[:, boost_axis, boost_axis] = cosine
    boost[:, 0, boost_axis] = boost[:, boost_axis, 0] = sine
    inverse_boost = np.broadcast_to(np.eye(4), (radial_count, 4, 4)).copy()
    inverse_boost[:, 0, 0] = inverse_boost[:, boost_axis, boost_axis] = cosine
    inverse_boost[:, 0, boost_axis] = inverse_boost[:, boost_axis, 0] = -sine
    boost_derivative = np.zeros_like(boost)
    boost_derivative[:, 0, 0] = boost_derivative[:, boost_axis, boost_axis] = sine
    boost_derivative[:, 0, boost_axis] = boost_derivative[:, boost_axis, 0] = cosine
    inverse_boost_derivative = np.zeros_like(boost)
    inverse_boost_derivative[:, 0, 0] = inverse_boost_derivative[
        :, boost_axis, boost_axis
    ] = sine
    inverse_boost_derivative[:, 0, boost_axis] = inverse_boost_derivative[
        :, boost_axis, 0
    ] = -cosine

    diagonal = np.zeros_like(boost)
    diagonal[:, 0, 0] = -parameters.timelike_eigenvalue
    diagonal[:, 1, 1] = lambda_1
    diagonal[:, 2, 2] = lambda_2
    diagonal[:, 3, 3] = lambda_3
    diagonal_derivative = np.zeros_like(boost)
    diagonal_derivative[:, 1, 1] = lambda_1_prime
    diagonal_derivative[:, 2, 2] = lambda_2_prime
    diagonal_derivative[:, 3, 3] = lambda_3_prime
    eigenframe_field = np.matmul(np.matmul(boost, diagonal), boost)
    eigenframe_radial = rapidity_prime[:, None, None] * (
        np.matmul(np.matmul(boost_derivative, diagonal), boost)
        + np.matmul(np.matmul(boost, diagonal), boost_derivative)
    ) + np.matmul(np.matmul(boost, diagonal_derivative), boost)
    eigenframe_clock = _batch_action(_CLOCK_GENERATOR, eigenframe_field)
    eigenframe_cartan = np.matmul(inverse_boost, inverse_boost)
    eigenframe_projector = np.matmul(np.matmul(inverse_boost, _P0), boost)
    eigenframe_projector_radial = rapidity_prime[:, None, None] * (
        np.matmul(np.matmul(inverse_boost_derivative, _P0), boost)
        + np.matmul(np.matmul(inverse_boost, _P0), boost_derivative)
    )
    eigenframe_projector_clock = np.matmul(
        _CLOCK_GENERATOR, eigenframe_projector
    ) - np.matmul(eigenframe_projector, _CLOCK_GENERATOR)

    rotation = frame[None]
    rotation_transpose = np.swapaxes(rotation, -1, -2)
    radial_field = eigenframe_field[:, None]
    field = np.matmul(np.matmul(rotation, radial_field), rotation_transpose)
    radial_field_derivative = eigenframe_radial[:, None]
    clock_field_derivative = np.matmul(
        np.matmul(rotation, eigenframe_clock[:, None]), rotation_transpose
    )
    cartan = np.matmul(
        np.matmul(rotation, eigenframe_cartan[:, None]), rotation_transpose
    )
    projector = np.matmul(
        np.matmul(rotation, eigenframe_projector[:, None]), rotation_transpose
    )
    radial_projector_derivative = eigenframe_projector_radial[:, None]
    clock_projector_derivative = np.matmul(
        np.matmul(rotation, eigenframe_projector_clock[:, None]),
        rotation_transpose,
    )

    spatial_field_derivatives = []
    spatial_projector_derivatives = []
    for axis in range(3):
        frame_derivative = frame_derivatives[axis][None]
        frame_derivative_transpose = np.swapaxes(frame_derivative, -1, -2)
        connection_field = (
            np.matmul(np.matmul(frame_derivative, radial_field), rotation_transpose)
            + np.matmul(np.matmul(rotation, radial_field), frame_derivative_transpose)
        ) / points[:, None, None, None]
        transported_radial = (
            np.matmul(np.matmul(rotation, radial_field_derivative), rotation_transpose)
            * directions[None, :, axis, None, None]
        )
        spatial_field_derivatives.append(connection_field + transported_radial)

        connection_projector = (
            np.matmul(
                np.matmul(frame_derivative, eigenframe_projector[:, None]),
                rotation_transpose,
            )
            + np.matmul(
                np.matmul(rotation, eigenframe_projector[:, None]),
                frame_derivative_transpose,
            )
        ) / points[:, None, None, None]
        transported_projector = (
            np.matmul(
                np.matmul(rotation, radial_projector_derivative), rotation_transpose
            )
            * directions[None, :, axis, None, None]
        )
        spatial_projector_derivatives.append(
            connection_projector + transported_projector
        )

    flat_cartan = cartan.reshape(-1, 4, 4)
    flat_spatial = tuple(
        derivative.reshape(-1, 4, 4) for derivative in spatial_field_derivatives
    )
    flat_clock = clock_field_derivative.reshape(-1, 4, 4)
    curvature_density = np.zeros((radial_count, direction_count))
    inertia_density = np.zeros((radial_count, direction_count))
    for left in range(3):
        for right in range(left + 1, 3):
            curvature = _batch_commutator(flat_spatial[left], flat_spatial[right])
            curvature_density += _internal_cartan_norm(curvature, flat_cartan).reshape(
                radial_count, direction_count
            )
    for spatial in range(3):
        curvature = _batch_commutator(flat_clock, flat_spatial[spatial])
        inertia_density += _internal_cartan_norm(curvature, flat_cartan).reshape(
            radial_count, direction_count
        )

    projector_density = np.zeros((radial_count, direction_count))
    for derivative in spatial_projector_derivatives:
        projector_density += -0.5 * np.einsum("rdab,rdba->rd", derivative, derivative)
    projector_density *= parameters.projector_stiffness
    inertia_density += (
        -0.5
        * parameters.projector_stiffness
        * np.einsum(
            "rdab,rdba->rd",
            clock_projector_derivative,
            clock_projector_derivative,
        )
    )

    normalization = 4.0 * np.pi
    averaged_projector = (
        np.einsum("rd,d->r", projector_density, angular_weights) / normalization
    )
    averaged_curvature = (
        np.einsum("rd,d->r", curvature_density, angular_weights) / normalization
    )
    averaged_inertia = (
        np.einsum("rd,d->r", inertia_density, angular_weights) / normalization
    )

    local_eigenvalues = np.stack(
        (
            np.full(radial_count, parameters.timelike_eigenvalue),
            lambda_1,
            lambda_2,
            lambda_3,
        ),
        axis=1,
    )
    target_eigenvalues = np.asarray(
        (parameters.timelike_eigenvalue, *parameters.spatial_eigenvalues)
    )
    potential_density = np.zeros(radial_count)
    for power, weight in enumerate(parameters.spectrum_weights, start=1):
        residual = np.sum(local_eigenvalues**power, axis=1) - np.sum(
            target_eigenvalues**power
        )
        potential_density += weight * residual**2
    arrays = (
        averaged_projector,
        averaged_curvature,
        potential_density,
        averaged_inertia,
    )
    if not all(np.all(np.isfinite(array)) for array in arrays):
        raise NumericalFailure("angular radial density evaluation became non-finite")
    return M5RadialDensities(*arrays)


def m5_radial_observables(
    radius: ArrayLike,
    densities: M5RadialDensities,
    angular_momentum: float,
) -> M5RadialObservables:
    """Integrate the radial density and perform the fixed-J Legendre step."""

    points = _real_vector(radius, "radius")
    momentum = float(angular_momentum)
    if not np.isfinite(momentum) or momentum <= 0.0:
        raise ValueError("angular_momentum must be positive and finite")
    measure = 4.0 * np.pi * points**2
    projector_energy = trapezoid_integral(measure * densities.projector, points)
    curvature_energy = trapezoid_integral(measure * densities.curvature, points)
    potential_energy = trapezoid_integral(measure * densities.potential, points)
    inertia = trapezoid_integral(measure * densities.inertia, points)
    if inertia <= 0.0:
        raise NumericalFailure("radial clock inertia must be positive")
    static_energy = projector_energy + curvature_energy + potential_energy
    rotational_energy = momentum**2 / (4.0 * inertia)
    frequency = momentum / (2.0 * inertia)
    return M5RadialObservables(
        static_energy=static_energy,
        projector_energy=projector_energy,
        curvature_energy=curvature_energy,
        potential_energy=potential_energy,
        inertia=inertia,
        angular_momentum=momentum,
        rotational_energy=rotational_energy,
        total_energy=static_energy + rotational_energy,
        frequency=frequency,
    )


def _profiles_from_controls(
    control_radius: FloatArray,
    control_values: FloatArray,
    sample_radius: FloatArray,
) -> tuple[FloatArray, FloatArray]:
    profiles = []
    derivatives = []
    for index in range(4):
        boundary = ((2, 0.0), (1, 0.0)) if index == 0 else ((1, 0.0), (1, 0.0))
        spline = CubicSpline(control_radius, control_values[index], bc_type=boundary)
        profiles.append(spline(sample_radius))
        derivatives.append(spline(sample_radius, 1))
    return np.asarray(profiles), np.asarray(derivatives)


def _unpack_controls(
    variables: FloatArray,
    control_count: int,
    parameters: M5RadialParameters,
) -> FloatArray:
    controls = np.zeros((4, control_count), dtype=np.float64)
    controls[0, -1] = 0.0
    controls[1:, -1] = parameters.spatial_eigenvalues
    controls[1:, 0] = variables[0]
    controls[:, 1:-1] = variables[1:].reshape(4, control_count - 2)
    return controls


def _initial_controls(
    control_radius: FloatArray,
    parameters: M5RadialParameters,
    boost_amplitude: float,
) -> FloatArray:
    target = np.asarray(parameters.spatial_eigenvalues)
    core = float(np.mean(target))
    melt = control_radius**2 / (1.0 + control_radius**2)
    controls = np.zeros((4, control_radius.size), dtype=np.float64)
    controls[0] = boost_amplitude * control_radius * np.exp(-control_radius / 2.0)
    controls[1:] = core + (target[:, None] - core) * melt
    controls[0, 0] = controls[0, -1] = 0.0
    controls[1:, 0] = core
    controls[1:, -1] = target
    return controls


def _pack_controls(controls: FloatArray) -> FloatArray:
    return np.concatenate(([controls[1, 0]], controls[:, 1:-1].ravel()))


def relax_m5_radial_hedgehog(
    *,
    angular_momentum: float,
    parameters: M5RadialParameters = M5RadialParameters(),
    domain_radius: float = 12.0,
    control_count: int = 7,
    quadrature_count: int = 220,
    boost_amplitudes: Sequence[float] = (0.0, 0.25, -0.25),
    initial_control_values: ArrayLike | None = None,
    maximum_iterations: int = 400,
) -> M5RadialSolution:
    """Relax all four radial profiles in a smooth spline basis.

    Multiple signed boost starts expose the even-profile stationary point.
    Basis and quadrature refinement remain claim-level responsibilities; this
    function returns one solve with enough diagnostics to perform them.
    """

    outer = float(domain_radius)
    if not np.isfinite(outer) or outer <= 0.0:
        raise ValueError("domain_radius must be positive and finite")
    if control_count < 5:
        raise ValueError("control_count must be at least five")
    if quadrature_count < 4 * control_count:
        raise ValueError("quadrature_count must be at least four times control_count")
    if maximum_iterations <= 0:
        raise ValueError("maximum_iterations must be positive")
    starts = tuple(float(value) for value in boost_amplitudes)
    if not starts or not all(np.isfinite(value) for value in starts):
        raise ValueError("boost_amplitudes must contain finite starts")

    control_radius = np.linspace(0.0, outer, control_count)
    sample_radius = np.linspace(max(outer * 1.0e-5, 1.0e-6), outer, quadrature_count)

    def evaluate(
        variables: FloatArray,
    ) -> tuple[M5RadialObservables, FloatArray, FloatArray]:
        controls = _unpack_controls(variables, control_count, parameters)
        profiles, derivatives = _profiles_from_controls(
            control_radius, controls, sample_radius
        )
        densities = m5_radial_densities(
            sample_radius, profiles, derivatives, parameters
        )
        observables = m5_radial_observables(sample_radius, densities, angular_momentum)
        return observables, profiles, derivatives

    def objective(variables: FloatArray) -> float:
        try:
            value = evaluate(variables)[0].total_energy
        except (FloatingPointError, NumericalFailure, ValueError):
            return 1.0e100
        return value if np.isfinite(value) else 1.0e100

    variable_bounds = [(-0.5, 1.5)]
    variable_bounds.extend([(-2.0, 2.0)] * (control_count - 2))
    variable_bounds.extend([(-0.5, 1.5)] * (3 * (control_count - 2)))
    initial_states = [
        _pack_controls(_initial_controls(control_radius, parameters, amplitude))
        for amplitude in starts
    ]
    if initial_control_values is not None:
        supplied = np.asarray(initial_control_values, dtype=np.float64)
        if supplied.shape != (4, control_count) or not np.all(np.isfinite(supplied)):
            raise ValueError(
                "initial_control_values must be finite with shape (4, control_count)"
            )
        if (
            supplied[0, 0] != 0.0
            or supplied[0, -1] != 0.0
            or not np.allclose(supplied[1:, 0], supplied[1, 0])
            or not np.allclose(supplied[1:, -1], parameters.spatial_eigenvalues)
        ):
            raise ValueError("initial_control_values violate radial boundary data")
        initial_states.insert(0, _pack_controls(supplied))

    best = None
    for initial in initial_states:
        result = minimize(
            objective,
            initial,
            method="L-BFGS-B",
            bounds=variable_bounds,
            options={
                "maxiter": maximum_iterations,
                "ftol": 1.0e-12,
                "gtol": 1.0e-7,
                "maxls": 40,
            },
        )
        if best is None or result.fun < best.fun:
            best = result
    if best is None:
        raise NumericalFailure("no radial optimization was attempted")

    controls = _unpack_controls(best.x, control_count, parameters)
    observables, profiles, derivatives = evaluate(best.x)
    spatial_profiles = profiles[1:]
    selected_branch_gap = float(
        np.min(np.abs(parameters.timelike_eigenvalue - spatial_profiles))
    )
    stationarity = float(np.max(np.abs(best.jac))) if best.jac is not None else np.inf
    return M5RadialSolution(
        control_radius=control_radius,
        control_values=controls,
        radius=sample_radius,
        profiles=profiles,
        profile_derivatives=derivatives,
        observables=observables,
        optimizer_success=bool(best.success),
        optimizer_message=str(best.message),
        iterations=int(best.nit),
        function_evaluations=int(best.nfev),
        stationarity_inf_norm=stationarity,
        selected_branch_gap=selected_branch_gap,
    )
