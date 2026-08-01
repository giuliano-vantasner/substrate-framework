"""Finite-time numerical evolution for the normalized 1+1 sine-Gordon PDE.

The exact framework convention is ``phi_tt-phi_xx+sin(phi)=0``.  This module
provides two deliberately separate numerical surfaces:

* a periodic centered spatial discretization with leapfrog and adaptive
  method-of-lines time integrators, useful for exact-solution convergence and
  independent-method checks;
* a half-line-style finite interval with prescribed left Neumann data and a
  first-order outgoing condition at the right endpoint, useful for auditing
  driven-boundary experiments.

Every result is finite-grid and finite-time evidence.  Endpoint field
differences are named as such because they become topological charges only
when the relevant endpoints satisfy the hypotheses of the accepted
topological-current claim.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .numerics import (
    NumericalFailure,
    SolverTolerances,
    solve_method_of_lines,
    trapezoid_integral,
)

FloatArray = NDArray[np.float64]
ScalarTrace = Callable[[float], float]


@dataclass(frozen=True)
class PeriodicSineGordonEvolution:
    """Sampled periodic evolution and energy diagnostics."""

    coordinate: FloatArray
    time: FloatArray
    field: FloatArray
    velocity: FloatArray
    energy: FloatArray
    method: str
    spatial_step: float
    time_step: float | None
    function_evaluations: int | None


@dataclass(frozen=True)
class DrivenSineGordonEvolution:
    """Finite-time driven-Neumann evolution with explicit flux diagnostics."""

    coordinate: FloatArray
    final_field: FloatArray
    final_velocity: FloatArray
    boundary_time: FloatArray
    boundary_field: FloatArray
    boundary_velocity: FloatArray
    boundary_coordinate_derivative: FloatArray
    initial_energy: float
    final_energy: float
    cumulative_left_work: float
    cumulative_right_flux: float
    energy_balance_residual: float
    endpoint_field_difference: float
    endpoint_charge_coordinate: float
    bulk_start: float
    bulk_endpoint_field_difference: float
    bulk_endpoint_charge_coordinate: float
    boundary_sign_correlation: float
    spatial_step: float
    time_step: float | None
    method: str
    function_evaluations: int | None


def moving_breather_samples(
    coordinate: ArrayLike,
    time: float,
    omega: float,
    velocity: float = 0.0,
    center: float = 0.0,
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Return exact moving-breather ``(phi,phi_t,phi_x)`` samples.

    The phase convention is the Lorentz transform of the accepted rest
    breather.  ``velocity`` is the center velocity, so a negative value moves
    the center toward decreasing coordinate.
    """

    x = _real_vector(coordinate, "coordinate")
    instant = _finite_scalar(time, "time")
    frequency = _open_unit_scalar(omega, "omega")
    speed = _open_signed_unit_scalar(velocity, "velocity")
    origin = _finite_scalar(center, "center")

    inverse_width = np.sqrt(1.0 - frequency**2)
    gamma = 1.0 / np.sqrt(1.0 - speed**2)
    xi = gamma * (x - origin - speed * instant)
    tau = gamma * (instant - speed * (x - origin))
    numerator = inverse_width * np.sin(frequency * tau)
    denominator = frequency * np.cosh(inverse_width * xi)
    norm = np.square(numerator) + np.square(denominator)
    if np.any(norm == 0.0) or not np.all(np.isfinite(norm)):
        raise NumericalFailure("moving-breather evaluation lost finite normalization")

    field = 4.0 * np.arctan2(numerator, denominator)
    dxi_dt = -gamma * speed
    dtau_dt = gamma
    dnum_dt = inverse_width * frequency * np.cos(frequency * tau) * dtau_dt
    dden_dt = frequency * inverse_width * np.sinh(inverse_width * xi) * dxi_dt
    velocity_samples = 4.0 * (
        denominator * dnum_dt - numerator * dden_dt
    ) / norm

    dxi_dx = gamma
    dtau_dx = -gamma * speed
    dnum_dx = inverse_width * frequency * np.cos(frequency * tau) * dtau_dx
    dden_dx = frequency * inverse_width * np.sinh(inverse_width * xi) * dxi_dx
    spatial_derivative = 4.0 * (
        denominator * dnum_dx - numerator * dden_dx
    ) / norm
    return (
        np.asarray(field, dtype=np.float64),
        np.asarray(velocity_samples, dtype=np.float64),
        np.asarray(spatial_derivative, dtype=np.float64),
    )


def endpoint_charge_coordinate(field_lower: float, field_upper: float) -> float:
    """Return ``(phi_upper-phi_lower)/(2*pi)`` without asserting vacuum data."""

    lower = _finite_scalar(field_lower, "field_lower")
    upper = _finite_scalar(field_upper, "field_upper")
    return float((upper - lower) / (2.0 * np.pi))


def sampled_boundary_sign_correlation(
    time: ArrayLike,
    boundary_velocity: ArrayLike,
    boundary_coordinate_derivative: ArrayLike,
) -> float:
    """Integrate ``sign(phi_t)*phi_x`` on a sampled boundary trace."""

    samples = _strict_time(time)
    velocity = _same_shape_vector(boundary_velocity, samples, "boundary_velocity")
    derivative = _same_shape_vector(
        boundary_coordinate_derivative,
        samples,
        "boundary_coordinate_derivative",
    )
    return trapezoid_integral(np.sign(velocity) * derivative, samples)


def periodic_sine_gordon_energy(
    field: ArrayLike,
    velocity: ArrayLike,
    spatial_step: float,
) -> float:
    """Return the centered-grid periodic Hamiltonian energy."""

    phi = _real_vector(field, "field")
    pi = _same_shape_vector(velocity, phi, "velocity")
    dx = _positive_scalar(spatial_step, "spatial_step")
    # The forward-edge difference is the discrete gradient whose variational
    # derivative is the centered Laplacian used by both periodic evolvers.
    # A centered nodal derivative would be a useful continuum estimator but
    # would not be the semi-discrete invariant of this operator.
    derivative = (np.roll(phi, -1) - phi) / dx
    density = (
        0.5 * np.square(pi)
        + 0.5 * np.square(derivative)
        + 1.0
        - np.cos(phi)
    )
    result = float(dx * np.sum(density))
    if not np.isfinite(result):
        raise NumericalFailure("periodic sine-Gordon energy became non-finite")
    return result


def evolve_periodic_sine_gordon_leapfrog(
    coordinate: ArrayLike,
    initial_field: ArrayLike,
    initial_velocity: ArrayLike,
    final_time: float,
    requested_time_step: float,
    *,
    sample_stride: int = 1,
) -> PeriodicSineGordonEvolution:
    """Evolve the periodic centered semi-discretization by velocity Verlet."""

    x, dx = _uniform_periodic_coordinate(coordinate)
    phi = _same_shape_vector(initial_field, x, "initial_field").copy()
    velocity = _same_shape_vector(initial_velocity, x, "initial_velocity").copy()
    duration = _positive_scalar(final_time, "final_time")
    proposed_step = _positive_scalar(requested_time_step, "requested_time_step")
    stride = _positive_integer(sample_stride, "sample_stride")
    steps = max(1, int(np.ceil(duration / proposed_step)))
    dt = duration / steps
    if dt / dx > 1.0:
        raise ValueError("periodic leapfrog requires time_step/spatial_step <= 1")

    sample_steps = set(range(0, steps + 1, stride))
    sample_steps.add(steps)
    times: list[float] = [0.0]
    fields: list[FloatArray] = [phi.copy()]
    velocities: list[FloatArray] = [velocity.copy()]
    energies: list[float] = [periodic_sine_gordon_energy(phi, velocity, dx)]

    acceleration = _periodic_acceleration(phi, dx)
    half_velocity = velocity + 0.5 * dt * acceleration
    for step in range(1, steps + 1):
        phi = phi + dt * half_velocity
        acceleration = _periodic_acceleration(phi, dx)
        velocity = half_velocity + 0.5 * dt * acceleration
        half_velocity = half_velocity + dt * acceleration
        if not np.all(np.isfinite(phi)) or not np.all(np.isfinite(velocity)):
            raise NumericalFailure(f"periodic leapfrog failed at step {step}")
        if step in sample_steps:
            times.append(step * dt)
            fields.append(phi.copy())
            velocities.append(velocity.copy())
            energies.append(periodic_sine_gordon_energy(phi, velocity, dx))

    return PeriodicSineGordonEvolution(
        coordinate=x,
        time=np.asarray(times, dtype=np.float64),
        field=np.asarray(fields, dtype=np.float64),
        velocity=np.asarray(velocities, dtype=np.float64),
        energy=np.asarray(energies, dtype=np.float64),
        method="periodic-centered-velocity-verlet",
        spatial_step=dx,
        time_step=dt,
        function_evaluations=None,
    )


def evolve_periodic_sine_gordon_mol(
    coordinate: ArrayLike,
    initial_field: ArrayLike,
    initial_velocity: ArrayLike,
    sample_times: ArrayLike,
    *,
    tolerances: SolverTolerances = SolverTolerances(),
    method: str = "DOP853",
) -> PeriodicSineGordonEvolution:
    """Evolve the same periodic spatial operator with an adaptive IVP method."""

    x, dx = _uniform_periodic_coordinate(coordinate)
    phi0 = _same_shape_vector(initial_field, x, "initial_field")
    velocity0 = _same_shape_vector(initial_velocity, x, "initial_velocity")
    times = _strict_time(sample_times)
    if times[0] != 0.0:
        raise ValueError("sample_times must begin at zero")
    point_count = x.size

    def rhs(_time: float, state: FloatArray) -> FloatArray:
        phi = state[:point_count]
        velocity = state[point_count:]
        return np.concatenate((velocity, _periodic_acceleration(phi, dx)))

    evidence = solve_method_of_lines(
        rhs,
        (float(times[0]), float(times[-1])),
        np.concatenate((phi0, velocity0)),
        sample_times=times,
        tolerances=tolerances,
        method=method,
    )
    fields = evidence.state[:point_count].T
    velocities = evidence.state[point_count:].T
    energies = np.asarray(
        [
            periodic_sine_gordon_energy(field, velocity, dx)
            for field, velocity in zip(fields, velocities)
        ],
        dtype=np.float64,
    )
    return PeriodicSineGordonEvolution(
        coordinate=x,
        time=evidence.time,
        field=fields,
        velocity=velocities,
        energy=energies,
        method=f"periodic-centered-{method}",
        spatial_step=dx,
        time_step=None,
        function_evaluations=evidence.function_evaluations,
    )


def evolve_driven_sine_gordon_leapfrog(
    coordinate: ArrayLike,
    initial_field: ArrayLike,
    initial_velocity: ArrayLike,
    left_neumann: ScalarTrace,
    final_time: float,
    requested_time_step: float,
    *,
    bulk_start: float,
) -> DrivenSineGordonEvolution:
    """Evolve a left-Neumann/right-outgoing finite-interval experiment.

    The grid includes both endpoints and its measured spacing is used by every
    stencil.  The left ghost value enforces ``phi_x=left_neumann(t)`` to second
    order.  The right endpoint uses the declared first-order Sommerfeld update
    ``phi_t+phi_x=0``; no extra cells are overwritten.
    """

    x, dx = _uniform_inclusive_coordinate(coordinate)
    phi_previous = _same_shape_vector(initial_field, x, "initial_field").copy()
    velocity0 = _same_shape_vector(initial_velocity, x, "initial_velocity").copy()
    duration = _positive_scalar(final_time, "final_time")
    proposed_step = _positive_scalar(requested_time_step, "requested_time_step")
    lower_bulk = _finite_scalar(bulk_start, "bulk_start")
    if not x[0] < lower_bulk < x[-1]:
        raise ValueError("bulk_start must lie strictly inside the coordinate domain")
    steps = max(3, int(np.ceil(duration / proposed_step)))
    dt = duration / steps
    courant = dt / dx
    if courant > 1.0:
        raise ValueError("driven leapfrog requires time_step/spatial_step <= 1")

    drive0 = _finite_scalar(left_neumann(0.0), "left_neumann(0)")
    acceleration0 = _neumann_left_acceleration(phi_previous, dx, drive0)
    phi_current = (
        phi_previous + dt * velocity0 + 0.5 * dt**2 * acceleration0
    )
    phi_current[-1] = phi_previous[-1] - courant * (
        phi_previous[-1] - phi_previous[-2]
    )
    _require_finite(phi_current, "first driven leapfrog step")

    initial_energy = _interval_energy(phi_previous, velocity0, x, drive0)
    trace_time: list[float] = []
    trace_field: list[float] = []
    trace_velocity: list[float] = []
    trace_derivative: list[float] = []
    left_power: list[float] = []
    right_power: list[float] = []

    for step in range(1, steps):
        time = step * dt
        drive = _finite_scalar(left_neumann(time), "left_neumann(time)")
        acceleration = _neumann_left_acceleration(phi_current, dx, drive)
        phi_next = 2.0 * phi_current - phi_previous + dt**2 * acceleration
        phi_next[-1] = phi_current[-1] - courant * (
            phi_current[-1] - phi_current[-2]
        )
        velocity_current = (phi_next - phi_previous) / (2.0 * dt)
        right_derivative = (phi_current[-1] - phi_current[-2]) / dx
        _require_finite(phi_next, f"driven leapfrog step {step + 1}")
        _require_finite(velocity_current, f"driven velocity step {step}")

        trace_time.append(time)
        trace_field.append(float(phi_current[0]))
        trace_velocity.append(float(velocity_current[0]))
        trace_derivative.append(drive)
        left_power.append(float(-velocity_current[0] * drive))
        right_power.append(float(velocity_current[-1] * right_derivative))
        phi_previous = phi_current
        phi_current = phi_next

    final_velocity = (phi_current - phi_previous) / dt
    final_drive = _finite_scalar(left_neumann(duration), "left_neumann(final_time)")
    final_energy = _interval_energy(phi_current, final_velocity, x, final_drive)
    times = np.asarray(trace_time, dtype=np.float64)
    velocities = np.asarray(trace_velocity, dtype=np.float64)
    derivatives = np.asarray(trace_derivative, dtype=np.float64)
    left_work = trapezoid_integral(left_power, times)
    outgoing_flux = trapezoid_integral(right_power, times)
    energy_residual = final_energy - initial_energy - left_work - outgoing_flux

    bulk_index = int(np.searchsorted(x, lower_bulk, side="left"))
    endpoint_difference = float(phi_current[-1] - phi_current[0])
    bulk_difference = float(phi_current[-1] - phi_current[bulk_index])
    return DrivenSineGordonEvolution(
        coordinate=x,
        final_field=np.asarray(phi_current, dtype=np.float64),
        final_velocity=np.asarray(final_velocity, dtype=np.float64),
        boundary_time=times,
        boundary_field=np.asarray(trace_field, dtype=np.float64),
        boundary_velocity=velocities,
        boundary_coordinate_derivative=derivatives,
        initial_energy=initial_energy,
        final_energy=final_energy,
        cumulative_left_work=left_work,
        cumulative_right_flux=outgoing_flux,
        energy_balance_residual=float(energy_residual),
        endpoint_field_difference=endpoint_difference,
        endpoint_charge_coordinate=endpoint_charge_coordinate(
            phi_current[0], phi_current[-1]
        ),
        bulk_start=float(x[bulk_index]),
        bulk_endpoint_field_difference=bulk_difference,
        bulk_endpoint_charge_coordinate=endpoint_charge_coordinate(
            phi_current[bulk_index], phi_current[-1]
        ),
        boundary_sign_correlation=sampled_boundary_sign_correlation(
            times,
            velocities,
            derivatives,
        ),
        spatial_step=dx,
        time_step=dt,
        method="left-neumann-right-sommerfeld-leapfrog",
        function_evaluations=None,
    )


def evolve_driven_sine_gordon_mol(
    coordinate: ArrayLike,
    initial_field: ArrayLike,
    initial_velocity: ArrayLike,
    left_neumann: ScalarTrace,
    sample_times: ArrayLike,
    *,
    bulk_start: float,
    tolerances: SolverTolerances = SolverTolerances(),
    method: str = "DOP853",
) -> DrivenSineGordonEvolution:
    """Evolve the driven problem with an adaptive method-of-lines route.

    The centered interior and left ghost-point operators match the leapfrog
    route.  The right Sommerfeld condition is evolved as
    ``pi_t=-pi_x`` at the boundary, a distinct time-integration formulation
    suitable for a method cross-check.  Flux quadrature uses the caller's
    declared sample times, which must therefore be refined independently when
    an energy-balance number is load-bearing.
    """

    x, dx = _uniform_inclusive_coordinate(coordinate)
    phi0 = _same_shape_vector(initial_field, x, "initial_field")
    velocity0 = _same_shape_vector(initial_velocity, x, "initial_velocity")
    times = _strict_time(sample_times)
    if times[0] != 0.0:
        raise ValueError("sample_times must begin at zero")
    lower_bulk = _finite_scalar(bulk_start, "bulk_start")
    if not x[0] < lower_bulk < x[-1]:
        raise ValueError("bulk_start must lie strictly inside the coordinate domain")
    point_count = x.size

    def rhs(time: float, state: FloatArray) -> FloatArray:
        phi = state[:point_count]
        velocity = state[point_count:]
        drive = _finite_scalar(left_neumann(time), "left_neumann(time)")
        acceleration = _neumann_left_acceleration(phi, dx, drive)
        acceleration[-1] = -(velocity[-1] - velocity[-2]) / dx
        return np.concatenate((velocity, acceleration))

    evidence = solve_method_of_lines(
        rhs,
        (float(times[0]), float(times[-1])),
        np.concatenate((phi0, velocity0)),
        sample_times=times,
        tolerances=tolerances,
        method=method,
    )
    fields = evidence.state[:point_count]
    velocities = evidence.state[point_count:]
    final_field = fields[:, -1]
    final_velocity = velocities[:, -1]
    derivative_trace = np.asarray([left_neumann(time) for time in times], dtype=np.float64)
    _require_finite(derivative_trace, "left Neumann trace")
    left_power = -velocities[0] * derivative_trace
    right_derivative = (fields[-1] - fields[-2]) / dx
    right_power = velocities[-1] * right_derivative
    left_work = trapezoid_integral(left_power, times)
    outgoing_flux = trapezoid_integral(right_power, times)
    initial_energy = _interval_energy(phi0, velocity0, x, derivative_trace[0])
    final_energy = _interval_energy(
        final_field,
        final_velocity,
        x,
        derivative_trace[-1],
    )
    bulk_index = int(np.searchsorted(x, lower_bulk, side="left"))
    endpoint_difference = float(final_field[-1] - final_field[0])
    bulk_difference = float(final_field[-1] - final_field[bulk_index])
    return DrivenSineGordonEvolution(
        coordinate=x,
        final_field=np.asarray(final_field, dtype=np.float64),
        final_velocity=np.asarray(final_velocity, dtype=np.float64),
        boundary_time=times,
        boundary_field=np.asarray(fields[0], dtype=np.float64),
        boundary_velocity=np.asarray(velocities[0], dtype=np.float64),
        boundary_coordinate_derivative=derivative_trace,
        initial_energy=initial_energy,
        final_energy=final_energy,
        cumulative_left_work=left_work,
        cumulative_right_flux=outgoing_flux,
        energy_balance_residual=float(
            final_energy - initial_energy - left_work - outgoing_flux
        ),
        endpoint_field_difference=endpoint_difference,
        endpoint_charge_coordinate=endpoint_charge_coordinate(
            final_field[0], final_field[-1]
        ),
        bulk_start=float(x[bulk_index]),
        bulk_endpoint_field_difference=bulk_difference,
        bulk_endpoint_charge_coordinate=endpoint_charge_coordinate(
            final_field[bulk_index], final_field[-1]
        ),
        boundary_sign_correlation=sampled_boundary_sign_correlation(
            times,
            velocities[0],
            derivative_trace,
        ),
        spatial_step=dx,
        time_step=None,
        method=f"left-neumann-right-sommerfeld-{method}",
        function_evaluations=evidence.function_evaluations,
    )


def gaussian_sine_neumann_drive(
    amplitude: float,
    angular_frequency: float,
    center_time: float,
    width: float,
    phase: float,
) -> ScalarTrace:
    """Return a declared Gaussian-enveloped sinusoidal Neumann trace."""

    scale = _finite_scalar(amplitude, "amplitude")
    frequency = _positive_scalar(angular_frequency, "angular_frequency")
    center = _finite_scalar(center_time, "center_time")
    sigma = _positive_scalar(width, "width")
    phase_value = _finite_scalar(phase, "phase")

    def drive(time: float) -> float:
        instant = _finite_scalar(time, "time")
        envelope = np.exp(-0.5 * ((instant - center) / sigma) ** 2)
        return float(
            scale * envelope * np.sin(frequency * (instant - center) + phase_value)
        )

    return drive


def _periodic_acceleration(field: FloatArray, spatial_step: float) -> FloatArray:
    laplacian = (
        np.roll(field, -1) - 2.0 * field + np.roll(field, 1)
    ) / spatial_step**2
    return np.asarray(laplacian - np.sin(field), dtype=np.float64)


def _neumann_left_acceleration(
    field: FloatArray,
    spatial_step: float,
    left_derivative: float,
) -> FloatArray:
    acceleration = np.empty_like(field)
    acceleration[1:-1] = (
        field[2:] - 2.0 * field[1:-1] + field[:-2]
    ) / spatial_step**2 - np.sin(field[1:-1])
    acceleration[0] = (
        2.0 * (field[1] - field[0]) / spatial_step**2
        - 2.0 * left_derivative / spatial_step
        - np.sin(field[0])
    )
    acceleration[-1] = 0.0
    return acceleration


def _interval_energy(
    field: FloatArray,
    velocity: FloatArray,
    coordinate: FloatArray,
    left_derivative: float,
) -> float:
    spatial_derivative = np.empty_like(field)
    spatial_derivative[0] = left_derivative
    spatial_derivative[1:-1] = (
        field[2:] - field[:-2]
    ) / (2.0 * (coordinate[1] - coordinate[0]))
    spatial_derivative[-1] = (
        field[-1] - field[-2]
    ) / (coordinate[1] - coordinate[0])
    density = (
        0.5 * np.square(velocity)
        + 0.5 * np.square(spatial_derivative)
        + 1.0
        - np.cos(field)
    )
    return trapezoid_integral(density, coordinate)


def _uniform_periodic_coordinate(coordinate: ArrayLike) -> tuple[FloatArray, float]:
    x = _real_vector(coordinate, "coordinate")
    if x.size < 5:
        raise ValueError("periodic coordinate requires at least five points")
    return x, _uniform_spacing(x)


def _uniform_inclusive_coordinate(coordinate: ArrayLike) -> tuple[FloatArray, float]:
    x = _real_vector(coordinate, "coordinate")
    if x.size < 5:
        raise ValueError("coordinate requires at least five points")
    return x, _uniform_spacing(x)


def _uniform_spacing(coordinate: FloatArray) -> float:
    differences = np.diff(coordinate)
    if np.any(differences <= 0.0):
        raise ValueError("coordinate must be strictly increasing")
    spacing = float(np.mean(differences))
    if not np.allclose(differences, spacing, rtol=1.0e-11, atol=1.0e-13):
        raise ValueError("coordinate must be uniformly spaced")
    return spacing


def _strict_time(values: ArrayLike) -> FloatArray:
    time = _real_vector(values, "time")
    if time.size < 2 or np.any(np.diff(time) <= 0.0):
        raise ValueError("time must contain at least two increasing samples")
    return time


def _same_shape_vector(values: ArrayLike, reference: FloatArray, name: str) -> FloatArray:
    vector = _real_vector(values, name)
    if vector.shape != reference.shape:
        raise ValueError(f"{name} must match the reference shape")
    return vector


def _real_vector(values: ArrayLike, name: str) -> FloatArray:
    vector = np.asarray(values, dtype=np.float64)
    if vector.ndim != 1 or vector.size == 0:
        raise ValueError(f"{name} must be a nonempty one-dimensional array")
    _require_finite(vector, name)
    return vector


def _require_finite(values: FloatArray, name: str) -> None:
    if not np.all(np.isfinite(values)):
        raise NumericalFailure(f"{name} contains non-finite values")


def _finite_scalar(value: float, name: str) -> float:
    scalar = float(value)
    if not np.isfinite(scalar):
        raise ValueError(f"{name} must be finite")
    return scalar


def _positive_scalar(value: float, name: str) -> float:
    scalar = _finite_scalar(value, name)
    if scalar <= 0.0:
        raise ValueError(f"{name} must be positive")
    return scalar


def _open_unit_scalar(value: float, name: str) -> float:
    scalar = _finite_scalar(value, name)
    if not 0.0 < scalar < 1.0:
        raise ValueError(f"{name} must satisfy 0 < {name} < 1")
    return scalar


def _open_signed_unit_scalar(value: float, name: str) -> float:
    scalar = _finite_scalar(value, name)
    if not abs(scalar) < 1.0:
        raise ValueError(f"{name} must satisfy abs({name}) < 1")
    return scalar


def _positive_integer(value: int, name: str) -> int:
    if isinstance(value, bool) or int(value) != value or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)
