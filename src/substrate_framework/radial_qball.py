"""Conditional three-dimensional radial sine-potential Q-ball evidence.

The declared model is a smooth complex scalar ``Psi`` with density
``rho=Psi.conjugate()*Psi`` and potential ``U(rho)=1-cos(sqrt(rho))``.
For ``Psi(t,r)=f(r)*exp(-i*omega*t)`` its nonnegative radial branch obeys

``f'' + 2*f'/r = sin(f)/2 - omega**2*f``.

This module provides exact symbolic identities and explicitly finite-wall
numerical evidence.  It does not quantize the branch, identify its Noether
charge with electric charge, or make it a determinant field, asymptotic
particle, or substrate excitation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.interpolate import CubicSpline
from scipy.optimize import root_scalar
import sympy as sp

from .numerics import (
    BVPEvidence,
    IVPEvidence,
    NumericalFailure,
    SolverTolerances,
    solve_bvp_evidence,
    solve_ivp_evidence,
    trapezoid_integral,
)

FloatArray = NDArray[np.float64]
LOCALIZATION_FREQUENCY_LIMIT = float(1.0 / np.sqrt(2.0))


def _positive_finite(value: float, name: str) -> float:
    result = float(value)
    if not np.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return result


def _localized_frequency(value: float) -> float:
    frequency = _positive_finite(value, "frequency")
    if frequency >= LOCALIZATION_FREQUENCY_LIMIT:
        raise ValueError("frequency must be below the localization threshold 1/sqrt(2)")
    return frequency


def smooth_complex_potential(density: Any) -> sp.Expr:
    """Return the exact analytic potential ``1-cos(sqrt(rho))``."""

    rho = sp.sympify(density)
    return sp.sympify(1) - sp.cos(sp.sqrt(rho))


def smooth_complex_potential_derivative(density: Any) -> sp.Expr:
    """Return ``dU/drho`` with its removable value at ``rho=0`` filled in."""

    rho = sp.sympify(density)
    if rho.is_zero is True:
        return sp.Rational(1, 2)
    return sp.Piecewise(
        (sp.Rational(1, 2), sp.Eq(rho, 0)),
        (sp.sin(sp.sqrt(rho)) / (2 * sp.sqrt(rho)), True),
    )


def symbolic_radial_profile_residual(
    radius: sp.Symbol, profile: sp.Expr, frequency: Any
) -> sp.Expr:
    """Return the exact stationary radial equation with zero on shell."""

    omega = sp.sympify(frequency)
    f = sp.sympify(profile)
    return sp.simplify(
        sp.diff(f, radius, 2)
        + 2 * sp.diff(f, radius) / radius
        - sp.sin(f) / 2
        + omega**2 * f
    )


def symbolic_radial_reduced_lagrangian(
    radius: sp.Symbol, profile: sp.Expr, frequency: Any
) -> sp.Expr:
    """Return the stationary radial action density before the ``4*pi`` factor."""

    omega = sp.sympify(frequency)
    f = sp.sympify(profile)
    return sp.simplify(
        radius**2
        * (
            omega**2 * f**2
            - sp.diff(f, radius) ** 2
            - (1 - sp.cos(f))
        )
    )


def symbolic_radial_energy_density(
    radius: sp.Symbol, profile: sp.Expr, frequency: Any
) -> sp.Expr:
    """Return the stationary energy density before the ``4*pi`` factor."""

    omega = sp.sympify(frequency)
    f = sp.sympify(profile)
    return sp.simplify(
        radius**2
        * (omega**2 * f**2 + sp.diff(f, radius) ** 2 + 1 - sp.cos(f))
    )


def symbolic_radial_charge_density(
    radius: sp.Symbol, profile: sp.Expr, frequency: Any
) -> sp.Expr:
    """Return ``r**2*j**0`` for ``j^0=2*omega*f**2`` before ``4*pi``."""

    return sp.simplify(
        2 * sp.sympify(frequency) * radius**2 * sp.sympify(profile) ** 2
    )


def radial_profile_force(amplitude: ArrayLike, frequency: float) -> FloatArray:
    """Return ``sin(f)/2-omega**2*f`` for the declared radial equation."""

    omega = _localized_frequency(frequency)
    values = np.asarray(amplitude, dtype=np.float64)
    if np.any(~np.isfinite(values)):
        raise ValueError("amplitude must contain only finite values")
    return np.asarray(0.5 * np.sin(values) - omega**2 * values, dtype=np.float64)


def radial_tail_rate(frequency: float) -> float:
    """Return the small-amplitude inverse length ``sqrt(1/2-omega**2)``."""

    omega = _localized_frequency(frequency)
    return float(np.sqrt(0.5 - omega**2))


def regular_origin_state(
    central_amplitude: float, frequency: float, origin_epsilon: float
) -> FloatArray:
    """Return the regular radial Taylor state ``[f(epsilon),f'(epsilon)]``."""

    amplitude = _positive_finite(central_amplitude, "central_amplitude")
    epsilon = _positive_finite(origin_epsilon, "origin_epsilon")
    force = float(radial_profile_force(amplitude, frequency))
    return np.asarray(
        [amplitude + force * epsilon**2 / 6.0, force * epsilon / 3.0],
        dtype=np.float64,
    )


def radial_qball_rhs(
    radius: ArrayLike, state: ArrayLike, frequency: float
) -> FloatArray:
    """Evaluate the regular-domain first-order system for ``[f,f']``."""

    coordinate = np.asarray(radius, dtype=np.float64)
    values = np.asarray(state, dtype=np.float64)
    scalar_input = coordinate.ndim == 0
    coordinate = np.atleast_1d(coordinate)
    if np.any(~np.isfinite(coordinate)) or np.any(coordinate <= 0.0):
        raise ValueError("radius must contain positive finite values")
    if values.ndim == 1:
        values = values[:, None]
    if values.shape != (2, coordinate.size):
        raise ValueError("state must have shape (2, radius.size)")
    if np.any(~np.isfinite(values)):
        raise NumericalFailure("state contains non-finite values")
    amplitude, derivative = values
    second = radial_profile_force(amplitude, frequency) - 2.0 * derivative / coordinate
    result = np.vstack((derivative, second))
    return result[:, 0] if scalar_input else np.asarray(result, dtype=np.float64)


def finite_wall_boundary_residual(
    left_state: ArrayLike,
    right_state: ArrayLike,
    frequency: float,
    *,
    origin_epsilon: float,
) -> FloatArray:
    """Return regular-origin and outer Dirichlet BVP residuals."""

    left = np.asarray(left_state, dtype=np.float64)
    right = np.asarray(right_state, dtype=np.float64)
    if left.shape != (2,) or right.shape != (2,):
        raise ValueError("boundary states must each contain two values")
    epsilon = _positive_finite(origin_epsilon, "origin_epsilon")
    force = float(radial_profile_force(left[0], frequency))
    return np.asarray(
        [left[1] - force * epsilon / 3.0, right[0]], dtype=np.float64
    )


@dataclass(frozen=True)
class RadialQBallSolution:
    """Adaptive-collocation evidence for one truncated radial branch."""

    frequency: float
    origin_epsilon: float
    outer_radius: float
    initial_mesh_points: int
    tolerance: float
    central_guess: float
    width_guess: float
    evidence: BVPEvidence
    boundary_residuals: FloatArray
    off_grid_ode_residual_max_abs: float

    @property
    def central_amplitude(self) -> float:
        force = float(radial_profile_force(self.evidence.state[0, 0], self.frequency))
        return float(
            self.evidence.state[0, 0] - force * self.origin_epsilon**2 / 6.0
        )

    @property
    def maximum_boundary_residual(self) -> float:
        return float(np.max(np.abs(self.boundary_residuals), initial=0.0))

    def state_at(self, radius: ArrayLike) -> FloatArray:
        """Evaluate a cubic interpolant on the solved finite interval."""

        coordinate = np.asarray(radius, dtype=np.float64)
        if coordinate.ndim != 1 or np.any(~np.isfinite(coordinate)):
            raise ValueError("radius must be a finite one-dimensional array")
        if np.any(coordinate < self.origin_epsilon) or np.any(
            coordinate > self.outer_radius
        ):
            raise ValueError("radius lies outside the solved interval")
        spline = CubicSpline(self.evidence.coordinate, self.evidence.state, axis=1)
        return np.asarray(spline(coordinate), dtype=np.float64)


@dataclass(frozen=True)
class RadialQBallObservables:
    """Truncated radial integrals in the declared action normalization."""

    field_norm: float
    noether_charge: float
    gradient_term: float
    potential_term: float
    energy: float
    effective_potential_term: float
    pohozaev_residual: float
    normalized_pohozaev_residual: float


@dataclass(frozen=True)
class RadialQBallShootingSolution:
    """Independent DOP853 origin-to-wall shooting evidence."""

    frequency: float
    central_amplitude: float
    origin_epsilon: float
    outer_radius: float
    ivp: IVPEvidence
    root_converged: bool
    root_function_calls: int
    robin_residual: float


def _solution_diagnostics(
    evidence: BVPEvidence,
    frequency: float,
    origin_epsilon: float,
) -> tuple[FloatArray, float]:
    boundary = finite_wall_boundary_residual(
        evidence.state[:, 0],
        evidence.state[:, -1],
        frequency,
        origin_epsilon=origin_epsilon,
    )
    midpoints = 0.5 * (evidence.coordinate[:-1] + evidence.coordinate[1:])
    spline = CubicSpline(evidence.coordinate, evidence.state, axis=1)
    state = np.asarray(spline(midpoints), dtype=np.float64)
    derivative = np.asarray(spline(midpoints, 1), dtype=np.float64)
    residual = derivative - radial_qball_rhs(midpoints, state, frequency)
    maximum = float(np.max(np.abs(residual), initial=0.0))
    if not np.isfinite(maximum):
        raise NumericalFailure("off-grid ODE residual became non-finite")
    return boundary, maximum


def solve_radial_qball_bvp(
    *,
    frequency: float,
    origin_epsilon: float = 1.0e-6,
    outer_radius: float = 30.0,
    initial_mesh_points: int = 2001,
    tolerance: float = 1.0e-8,
    max_nodes: int = 50_000,
    central_guess: float = 6.2,
    width_guess: float = 4.0,
    minimum_central_amplitude: float = 1.0e-3,
) -> RadialQBallSolution:
    """Solve a nontrivial finite-wall radial branch by adaptive collocation."""

    omega = _localized_frequency(frequency)
    epsilon = _positive_finite(origin_epsilon, "origin_epsilon")
    outer = _positive_finite(outer_radius, "outer_radius")
    if epsilon >= outer:
        raise ValueError("origin_epsilon must be below outer_radius")
    points = int(initial_mesh_points)
    if points != initial_mesh_points or points < 20:
        raise ValueError("initial_mesh_points must be an integer of at least 20")
    tol = _positive_finite(tolerance, "tolerance")
    center = _positive_finite(central_guess, "central_guess")
    width = _positive_finite(width_guess, "width_guess")
    nontrivial = _positive_finite(
        minimum_central_amplitude, "minimum_central_amplitude"
    )

    coordinate = np.linspace(epsilon, outer, points, dtype=np.float64)
    amplitude = center * np.exp(-(coordinate / width) ** 2)
    derivative = -2.0 * coordinate * amplitude / width**2
    evidence = solve_bvp_evidence(
        lambda radius, state: radial_qball_rhs(radius, state, omega),
        lambda left, right: finite_wall_boundary_residual(
            left, right, omega, origin_epsilon=epsilon
        ),
        coordinate,
        np.vstack((amplitude, derivative)),
        tolerance=tol,
        max_nodes=max_nodes,
    )
    boundary, ode_residual = _solution_diagnostics(evidence, omega, epsilon)
    solution = RadialQBallSolution(
        omega,
        epsilon,
        outer,
        points,
        tol,
        center,
        width,
        evidence,
        boundary,
        ode_residual,
    )
    if abs(solution.central_amplitude) < nontrivial:
        raise NumericalFailure("BVP converged to the excluded trivial branch")
    return solution


def radial_qball_observables(
    solution: RadialQBallSolution, *, quadrature_points: int = 20_001
) -> RadialQBallObservables:
    """Integrate charge, energy, and Pohozaev terms on a uniform mesh."""

    points = int(quadrature_points)
    if points != quadrature_points or points < 1001:
        raise ValueError("quadrature_points must be an integer of at least 1001")
    radius = np.linspace(
        solution.origin_epsilon, solution.outer_radius, points, dtype=np.float64
    )
    amplitude, derivative = solution.state_at(radius)
    measure = 4.0 * np.pi * radius**2
    field_norm = trapezoid_integral(measure * amplitude**2, radius)
    gradient = trapezoid_integral(measure * derivative**2, radius)
    potential = trapezoid_integral(measure * (1.0 - np.cos(amplitude)), radius)
    omega = solution.frequency
    charge = 2.0 * omega * field_norm
    energy = gradient + omega**2 * field_norm + potential
    effective = potential - omega**2 * field_norm
    pohozaev = gradient + 3.0 * effective
    denominator = abs(gradient) + 3.0 * abs(effective)
    if denominator == 0.0:
        raise NumericalFailure("Pohozaev normalization vanished")
    values = np.asarray(
        [field_norm, charge, gradient, potential, energy, effective, pohozaev],
        dtype=np.float64,
    )
    if np.any(~np.isfinite(values)) or field_norm <= 0.0 or energy <= 0.0:
        raise NumericalFailure("radial observables are not finite and positive")
    return RadialQBallObservables(
        field_norm,
        charge,
        gradient,
        potential,
        energy,
        effective,
        pohozaev,
        abs(pohozaev) / denominator,
    )


def fit_radial_tail_rate(
    solution: RadialQBallSolution,
    *,
    fit_start: float,
    fit_stop: float,
    fit_points: int = 2001,
) -> float:
    """Fit ``log(r*f)`` on a declared positive, non-roundoff tail window."""

    start = _positive_finite(fit_start, "fit_start")
    stop = _positive_finite(fit_stop, "fit_stop")
    if start >= stop or start < solution.origin_epsilon or stop > solution.outer_radius:
        raise ValueError("tail window must lie inside the solved interval")
    points = int(fit_points)
    if points != fit_points or points < 20:
        raise ValueError("fit_points must be an integer of at least 20")
    radius = np.linspace(start, stop, points, dtype=np.float64)
    amplitude = solution.state_at(radius)[0]
    if np.any(amplitude <= 1.0e-12):
        raise NumericalFailure("tail window contains nonpositive or roundoff samples")
    slope, _intercept = np.polyfit(radius, np.log(radius * amplitude), 1)
    rate = float(-slope)
    if not np.isfinite(rate) or rate <= 0.0:
        raise NumericalFailure("fitted tail rate is not positive and finite")
    return rate


def shoot_radial_qball(
    *,
    frequency: float,
    central_bracket: tuple[float, float],
    origin_epsilon: float = 1.0e-6,
    outer_radius: float = 20.0,
    sample_points: int = 12_001,
    tolerances: SolverTolerances = SolverTolerances(
        rtol=1.0e-10, atol=1.0e-12, max_step=0.03
    ),
) -> RadialQBallShootingSolution:
    """Find a regular profile satisfying the asymptotic Robin condition."""

    omega = _localized_frequency(frequency)
    epsilon = _positive_finite(origin_epsilon, "origin_epsilon")
    outer = _positive_finite(outer_radius, "outer_radius")
    if epsilon >= outer:
        raise ValueError("origin_epsilon must be below outer_radius")
    if len(central_bracket) != 2:
        raise ValueError("central_bracket must contain two endpoints")
    lower = _positive_finite(central_bracket[0], "central_bracket lower")
    upper = _positive_finite(central_bracket[1], "central_bracket upper")
    if lower >= upper:
        raise ValueError("central_bracket must be strictly increasing")
    points = int(sample_points)
    if points != sample_points or points < 1001:
        raise ValueError("sample_points must be an integer of at least 1001")
    kappa = radial_tail_rate(omega)

    def integrate(center: float, sample_times: FloatArray | None = None) -> IVPEvidence:
        return solve_ivp_evidence(
            lambda radius, state: radial_qball_rhs(radius, state, omega),
            (epsilon, outer),
            regular_origin_state(center, omega, epsilon),
            sample_times=sample_times,
            tolerances=tolerances,
            method="DOP853",
        )

    def robin(center: float) -> float:
        terminal = integrate(center).state[:, -1]
        return float(terminal[1] + (kappa + 1.0 / outer) * terminal[0])

    lower_residual, upper_residual = robin(lower), robin(upper)
    if lower_residual == 0.0 or upper_residual == 0.0:
        raise ValueError("central_bracket endpoint is already a root")
    if np.signbit(lower_residual) == np.signbit(upper_residual):
        raise NumericalFailure("shooting bracket does not straddle a Robin residual root")
    root = root_scalar(
        robin,
        bracket=(lower, upper),
        method="brentq",
        xtol=1.0e-13,
        rtol=1.0e-14,
    )
    if not root.converged:
        raise NumericalFailure("shooting root solve did not converge")
    center = float(root.root)
    samples = np.linspace(epsilon, outer, points, dtype=np.float64)
    evidence = integrate(center, samples)
    terminal = evidence.state[:, -1]
    residual = float(terminal[1] + (kappa + 1.0 / outer) * terminal[0])
    if not np.isfinite(residual):
        raise NumericalFailure("shooting Robin residual became non-finite")
    return RadialQBallShootingSolution(
        omega,
        center,
        epsilon,
        outer,
        evidence,
        bool(root.converged),
        int(root.function_calls),
        residual,
    )


def shooting_observables(solution: RadialQBallShootingSolution) -> RadialQBallObservables:
    """Integrate the independent shooting samples without interpolation."""

    radius = solution.ivp.time
    amplitude, derivative = solution.ivp.state
    measure = 4.0 * np.pi * radius**2
    field_norm = trapezoid_integral(measure * amplitude**2, radius)
    gradient = trapezoid_integral(measure * derivative**2, radius)
    potential = trapezoid_integral(measure * (1.0 - np.cos(amplitude)), radius)
    omega = solution.frequency
    charge = 2.0 * omega * field_norm
    energy = gradient + omega**2 * field_norm + potential
    effective = potential - omega**2 * field_norm
    pohozaev = gradient + 3.0 * effective
    denominator = abs(gradient) + 3.0 * abs(effective)
    if denominator == 0.0:
        raise NumericalFailure("shooting Pohozaev normalization vanished")
    values = np.asarray(
        [field_norm, charge, gradient, potential, energy, effective, pohozaev],
        dtype=np.float64,
    )
    if np.any(~np.isfinite(values)) or field_norm <= 0.0 or energy <= 0.0:
        raise NumericalFailure("shooting observables are not finite and positive")
    return RadialQBallObservables(
        field_norm,
        charge,
        gradient,
        potential,
        energy,
        effective,
        pohozaev,
        abs(pohozaev) / denominator,
    )
