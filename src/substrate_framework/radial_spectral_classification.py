"""Exact central-radial spectral typing and soluble finite-wall calibration.

The exact APIs distinguish a regular half-line radial problem from a finite
Dirichlet ball.  The numerical root helper only calibrates a supplied
spherical-Bessel bracket; it is not a half-line eigensolver and it does not
turn a time-averaged operator into a Floquet or nonlinear mode problem.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import sympy as sp
from scipy.optimize import brentq
from scipy.special import spherical_jn


def _angular_momentum(value: Any) -> int:
    if isinstance(value, bool) or int(value) != value or value < 0:
        raise ValueError("angular_momentum must be a nonnegative integer")
    return int(value)


def _positive_finite(value: Any, name: str) -> float:
    result = float(value)
    if not np.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return result


@dataclass(frozen=True)
class RadialLiouvilleEvidence:
    """Exact three-dimensional central-radial Liouville ledger for ``r>0``."""

    angular_momentum: int
    radial_mode: sp.Expr
    radial_residual: sp.Expr
    transformed_residual: sp.Expr
    scaled_residual_difference: sp.Expr
    radial_norm_density: sp.Expr
    transformed_norm_density: sp.Expr
    norm_density_difference: sp.Expr
    regular_radial_power: int
    regular_transformed_power: int


def central_radial_liouville_evidence(
    transformed_mode: Any,
    potential: Any,
    spectral_value: Any,
    radius: sp.Symbol,
    angular_momentum: int,
) -> RadialLiouvilleEvidence:
    """Return the exact ``chi=r*g`` reduction and radial-norm identity.

    The original residual is
    ``-g''-2*g'/r+ell*(ell+1)*g/r**2+(V-E)*g``.  Multiplication by ``r``
    after substituting ``g=chi/r`` gives the returned transformed residual.
    For real modes, the radial norm densities obey ``r**2*g**2=chi**2``.
    """

    if not isinstance(radius, sp.Symbol):
        raise ValueError("radius must be a SymPy symbol")
    ell = _angular_momentum(angular_momentum)
    chi = sp.sympify(transformed_mode)
    v = sp.sympify(potential)
    eigenvalue = sp.sympify(spectral_value)
    g = chi / radius
    radial_residual = sp.simplify(
        -sp.diff(g, radius, 2)
        - 2 * sp.diff(g, radius) / radius
        + ell * (ell + 1) * g / radius**2
        + (v - eigenvalue) * g
    )
    transformed_residual = sp.simplify(
        -sp.diff(chi, radius, 2)
        + (ell * (ell + 1) / radius**2 + v - eigenvalue) * chi
    )
    scaled_difference = sp.simplify(radius * radial_residual - transformed_residual)
    radial_density = sp.simplify(radius**2 * g**2)
    transformed_density = sp.simplify(chi**2)
    norm_difference = sp.simplify(radial_density - transformed_density)
    if scaled_difference != 0 or norm_difference != 0:
        raise AssertionError("internal radial Liouville identity is inconsistent")
    return RadialLiouvilleEvidence(
        angular_momentum=ell,
        radial_mode=g,
        radial_residual=radial_residual,
        transformed_residual=transformed_residual,
        scaled_residual_difference=scaled_difference,
        radial_norm_density=radial_density,
        transformed_norm_density=transformed_density,
        norm_density_difference=norm_difference,
        regular_radial_power=ell,
        regular_transformed_power=ell + 1,
    )


@dataclass(frozen=True)
class RadialThresholdFormEvidence:
    """Exact quadratic-form density measured from a supplied threshold."""

    angular_momentum: int
    centrifugal_term: sp.Expr
    excess_potential: sp.Expr
    quadratic_form_density: sp.Expr


def radial_threshold_form_evidence(
    transformed_mode: Any,
    potential: Any,
    continuum_threshold: Any,
    radius: sp.Symbol,
    angular_momentum: int,
) -> RadialThresholdFormEvidence:
    """Return the conditional form for ``H-continuum_threshold``.

    If the returned ``excess_potential`` is nonnegative almost everywhere and
    the self-adjoint boundary form vanishes, integration of the returned
    density is nonnegative.  This function derives the implication; it does
    not pretend that finite sampling proves the pointwise premise.
    """

    if not isinstance(radius, sp.Symbol):
        raise ValueError("radius must be a SymPy symbol")
    ell = _angular_momentum(angular_momentum)
    chi = sp.sympify(transformed_mode)
    v = sp.sympify(potential)
    threshold = sp.sympify(continuum_threshold)
    centrifugal = sp.Integer(ell * (ell + 1)) / radius**2
    excess = sp.simplify(centrifugal + v - threshold)
    density = sp.simplify(sp.diff(chi, radius) ** 2 + excess * chi**2)
    return RadialThresholdFormEvidence(
        angular_momentum=ell,
        centrifugal_term=centrifugal,
        excess_potential=excess,
        quadratic_form_density=density,
    )


@dataclass(frozen=True)
class VacuumDirichletBallEvidence:
    """Exact spherical-Bessel calibration on a regular Dirichlet ball."""

    angular_momentum: int
    radius: sp.Expr
    continuum_threshold: sp.Expr
    spherical_bessel_zero: sp.Expr
    wavenumber: sp.Expr
    spectral_value: sp.Expr
    radial_mode: sp.Expr
    differential_residual: sp.Expr
    outer_boundary_value: sp.Expr


def vacuum_dirichlet_ball_evidence(
    radius: Any,
    continuum_threshold: Any,
    spherical_bessel_zero: Any,
    radial_coordinate: sp.Symbol,
    angular_momentum: int,
) -> VacuumDirichletBallEvidence:
    """Return the exact regular vacuum mode conditional on a Bessel zero.

    For a positive ball radius ``R`` and a supplied positive zero ``z`` of
    spherical ``j_ell``, the regular radial mode is ``j_ell(z*r/R)`` and the
    spectral value is ``mu_squared+(z/R)**2``.  The returned boundary value
    makes the root premise explicit instead of hiding a fitted decimal.
    """

    if not isinstance(radial_coordinate, sp.Symbol):
        raise ValueError("radial_coordinate must be a SymPy symbol")
    ell = _angular_momentum(angular_momentum)
    ball_radius = sp.sympify(radius)
    if ball_radius.is_number and ball_radius.is_positive is not True:
        raise ValueError("radius must be positive")
    zero = sp.sympify(spherical_bessel_zero)
    if zero.is_number and zero.is_positive is not True:
        raise ValueError("spherical_bessel_zero must be positive")
    threshold = sp.sympify(continuum_threshold)
    r = radial_coordinate
    k = sp.simplify(zero / ball_radius)
    exact_k = sp.Dummy("k", positive=True)
    argument = exact_k * r
    order = sp.Rational(2 * ell + 1, 2)
    exact_radial_mode = sp.sqrt(sp.pi / (2 * argument)) * sp.besselj(order, argument)
    spectral_value = sp.simplify(threshold + k**2)
    exact_residual = sp.simplify(
        -sp.diff(exact_radial_mode, r, 2)
        - 2 * sp.diff(exact_radial_mode, r) / r
        + ell * (ell + 1) * exact_radial_mode / r**2
        - exact_k**2 * exact_radial_mode
    )
    if exact_residual != 0:
        raise AssertionError("internal spherical-Bessel residual is inconsistent")
    radial_mode = exact_radial_mode.subs(exact_k, k)
    return VacuumDirichletBallEvidence(
        angular_momentum=ell,
        radius=ball_radius,
        continuum_threshold=threshold,
        spherical_bessel_zero=zero,
        wavenumber=k,
        spectral_value=spectral_value,
        radial_mode=radial_mode,
        differential_residual=sp.Integer(0),
        outer_boundary_value=sp.simplify(radial_mode.subs(r, ball_radius)),
    )


@dataclass(frozen=True)
class BracketedBesselZeroEvidence:
    """Resolution-bounded root evidence for one supplied sign-changing bracket."""

    angular_momentum: int
    bracket: tuple[float, float]
    zero: float
    absolute_residual: float
    iterations: int
    function_calls: int


def bracketed_spherical_bessel_zero(
    angular_momentum: int,
    bracket: tuple[float, float],
    *,
    absolute_tolerance: float = 1.0e-13,
) -> BracketedBesselZeroEvidence:
    """Find one spherical-Bessel zero in an explicit sign-changing bracket."""

    ell = _angular_momentum(angular_momentum)
    if len(bracket) != 2:
        raise ValueError("bracket must contain two endpoints")
    lower = _positive_finite(bracket[0], "bracket lower endpoint")
    upper = _positive_finite(bracket[1], "bracket upper endpoint")
    if upper <= lower:
        raise ValueError("bracket must be strictly increasing")
    tolerance = _positive_finite(absolute_tolerance, "absolute_tolerance")
    lower_value = float(spherical_jn(ell, lower))
    upper_value = float(spherical_jn(ell, upper))
    if lower_value * upper_value >= 0.0:
        raise ValueError("bracket must have a strict spherical-Bessel sign change")
    zero, result = brentq(
        lambda value: float(spherical_jn(ell, value)),
        lower,
        upper,
        xtol=tolerance,
        rtol=4.0 * np.finfo(np.float64).eps,
        full_output=True,
        disp=True,
    )
    return BracketedBesselZeroEvidence(
        angular_momentum=ell,
        bracket=(lower, upper),
        zero=float(zero),
        absolute_residual=abs(float(spherical_jn(ell, zero))),
        iterations=int(result.iterations),
        function_calls=int(result.function_calls),
    )


@dataclass(frozen=True)
class EndpointDecayEvidence:
    """Value and provenance typing for one endpoint-decay predicate."""

    peak_amplitude: float
    endpoint_amplitude: float
    amplitude_floor: float
    relative_tolerance: float
    passes: bool
    endpoint_forced: bool
    endpoint_value_is_discriminating: bool


def endpoint_decay_evidence(
    peak_amplitude: Any,
    endpoint_amplitude: Any,
    *,
    amplitude_floor: float = 1.0e-3,
    relative_tolerance: float = 1.0e-3,
    endpoint_forced: bool = False,
) -> EndpointDecayEvidence:
    """Evaluate an endpoint test while preserving whether zero was imposed.

    A forced endpoint can make the arithmetic predicate pass, but its value is
    then not independent evidence of decay or half-line localization.
    """

    peak = abs(float(peak_amplitude))
    endpoint = abs(float(endpoint_amplitude))
    if not np.isfinite(peak) or not np.isfinite(endpoint):
        raise ValueError("amplitudes must be finite")
    floor = _positive_finite(amplitude_floor, "amplitude_floor")
    tolerance = _positive_finite(relative_tolerance, "relative_tolerance")
    if tolerance >= 1.0:
        raise ValueError("relative_tolerance must be smaller than one")
    if not isinstance(endpoint_forced, bool):
        raise ValueError("endpoint_forced must be boolean")
    passes = bool(peak > floor and endpoint < tolerance * peak)
    return EndpointDecayEvidence(
        peak_amplitude=peak,
        endpoint_amplitude=endpoint,
        amplitude_floor=floor,
        relative_tolerance=tolerance,
        passes=passes,
        endpoint_forced=endpoint_forced,
        endpoint_value_is_discriminating=not endpoint_forced,
    )


def hard_zero_endpoint_counterexample(
    peak_amplitude: Any,
    *,
    amplitude_floor: float = 1.0e-3,
    relative_tolerance: float = 1.0e-3,
) -> EndpointDecayEvidence:
    """Return the forced-zero outcome for any supplied interior peak."""

    return endpoint_decay_evidence(
        peak_amplitude,
        0.0,
        amplitude_floor=amplitude_floor,
        relative_tolerance=relative_tolerance,
        endpoint_forced=True,
    )
