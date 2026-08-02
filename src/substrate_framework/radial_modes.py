"""Conditional radial-profile and fluctuation-mode machinery.

The exact APIs derive a self-adjoint radial Hessian from a declared reduced
energy.  The numerical APIs solve one declared massless Option-C hedgehog
model and finite-box regressions of its Hessian.  A classical box spectrum is
not a particle spectrum: the model's continuum threshold is zero, and no
spin, quantization, mass scale, or Roper identification is supplied here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import sympy as sp
from numpy.typing import ArrayLike, NDArray
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh

from .numerics import SolverTolerances, solve_ivp_evidence, trapezoid_integral

FloatArray = NDArray[np.float64]


def _positive_float(value: Any, name: str) -> float:
    result = float(value)
    if not np.isfinite(result) or result <= 0.0:
        raise ValueError(f"{name} must be positive and finite")
    return result


def _positive_symbolic(value: Any, name: str) -> sp.Expr:
    result = sp.sympify(value)
    if result.is_number and result.is_positive is not True:
        raise ValueError(f"{name} must be positive")
    return result


def _sample_vector(values: ArrayLike, name: str) -> FloatArray:
    result = np.asarray(values, dtype=np.float64)
    if result.ndim != 1 or result.size < 4:
        raise ValueError(f"{name} must be a one-dimensional array with at least four entries")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    return result


def option_c_radial_energy_density(
    field: Any,
    radial_derivative: Any,
    radius: Any,
) -> sp.Expr:
    """Return the declared dimensionless Option-C static density for ``r>0``.

    The full static energy is ``4*pi*integral density dr``.  This declaration
    is a conditional reduced model, not a derived physical Skyrme action.
    """

    f = sp.sympify(field)
    fp = sp.sympify(radial_derivative)
    r = sp.sympify(radius)
    return sp.simplify(
        (r**2 + 2 * sp.sin(f) ** 2) * fp**2
        + 2 * sp.sin(f) ** 2
        + sp.sin(f) ** 4 / r**2
    )


def option_c_euler_lagrange_residual(profile: Any, radius: sp.Symbol) -> sp.Expr:
    """Return the exact static Euler--Lagrange residual for the declared model."""

    if not isinstance(radius, sp.Symbol):
        raise ValueError("radius must be a SymPy symbol")
    f = sp.sympify(profile)
    fp = sp.diff(f, radius)
    fpp = sp.diff(f, radius, 2)
    return sp.simplify(
        (radius**2 + 2 * sp.sin(f) ** 2) * fpp
        + 2 * radius * fp
        + sp.sin(2 * f) * (fp**2 - 1)
        - sp.sin(2 * f) * sp.sin(f) ** 2 / radius**2
    )


@dataclass(frozen=True)
class RadialSecondVariationEvidence:
    """Exact coefficients of the integrated radial quadratic form.

    Before integration by parts, the quadratic coefficient contains a mixed
    ``eta*eta'`` term.  ``mixed_boundary_correction`` is the term that must be
    added to the local half-Hessian after integrating that mixed term.  It
    cannot be discarded merely because the background is stationary.
    """

    gradient_coefficient: sp.Expr
    local_half_hessian: sp.Expr
    mixed_coefficient: sp.Expr
    mixed_boundary_correction: sp.Expr
    potential_coefficient: sp.Expr
    kinetic_weight: sp.Expr


def option_c_second_variation(
    profile: Any,
    radius: sp.Symbol,
) -> RadialSecondVariationEvidence:
    """Derive the exact self-adjoint second variation about ``profile``.

    With ``f -> f + epsilon*eta``, the coefficient of ``epsilon**2`` is
    ``A*eta'**2 + B*eta*eta' + D*eta**2``.  Endpoint-fixed integration by
    parts gives ``A*eta'**2 + (D-B'/2)*eta**2``.  The returned kinetic weight
    is the separately declared Lorentz-mirrored coefficient ``A``.
    """

    if not isinstance(radius, sp.Symbol):
        raise ValueError("radius must be a SymPy symbol")
    f = sp.sympify(profile)
    fp = sp.diff(f, radius)
    fpp = sp.diff(f, radius, 2)
    sf = sp.sin(f)
    cf = sp.cos(f)
    c2f = sp.cos(2 * f)

    gradient = sp.simplify(radius**2 + 2 * sf**2)
    local = sp.simplify(
        2 * c2f
        + 2 * c2f * fp**2
        + 2 * sf**2 * (3 * cf**2 - sf**2) / radius**2
    )
    mixed = sp.simplify(4 * sp.sin(2 * f) * fp)
    correction = sp.simplify(-sp.diff(mixed, radius) / 2)
    potential = sp.simplify(local + correction)

    # Keep the expanded f'' form visible to catch a silently omitted mixed term.
    expected_correction = sp.simplify(-4 * c2f * fp**2 - 2 * sp.sin(2 * f) * fpp)
    if sp.simplify(correction - expected_correction) != 0:
        raise AssertionError("internal mixed-term derivation is inconsistent")
    return RadialSecondVariationEvidence(
        gradient_coefficient=gradient,
        local_half_hessian=local,
        mixed_coefficient=mixed,
        mixed_boundary_correction=correction,
        potential_coefficient=potential,
        kinetic_weight=gradient,
    )


def apply_option_c_radial_hessian(
    mode: Any,
    profile: Any,
    radius: sp.Symbol,
) -> sp.Expr:
    """Apply ``-(A*eta')' + C*eta`` for the exact self-adjoint Hessian."""

    eta = sp.sympify(mode)
    evidence = option_c_second_variation(profile, radius)
    return sp.simplify(
        -sp.diff(evidence.gradient_coefficient * sp.diff(eta, radius), radius)
        + evidence.potential_coefficient * eta
    )


def radial_green_boundary_form(
    first_mode: Any,
    second_mode: Any,
    gradient_coefficient: Any,
    radius: sp.Symbol,
) -> sp.Expr:
    """Return the endpoint Green form ``A*(u*v'-u'*v)``."""

    if not isinstance(radius, sp.Symbol):
        raise ValueError("radius must be a SymPy symbol")
    u = sp.sympify(first_mode)
    v = sp.sympify(second_mode)
    coefficient = sp.sympify(gradient_coefficient)
    return sp.simplify(
        coefficient * (u * sp.diff(v, radius) - sp.diff(u, radius) * v)
    )


def derrick_scale_tangent(profile: Any, radius: sp.Symbol) -> sp.Expr:
    """Return ``d/ds f(exp(s)*r)|s=0 = r*f'(r)`` exactly."""

    if not isinstance(radius, sp.Symbol):
        raise ValueError("radius must be a SymPy symbol")
    return sp.simplify(radius * sp.diff(sp.sympify(profile), radius))


@dataclass(frozen=True)
class DerrickScalingEvidence:
    """Exact two-/four-derivative energy along logarithmic scale ``s``."""

    scaled_energy: sp.Expr
    slope_at_origin: sp.Expr
    curvature_at_origin: sp.Expr
    stationary_condition: sp.Expr


def derrick_scaling_evidence(
    two_derivative_energy: Any,
    four_derivative_energy: Any,
    logarithmic_scale: Any,
) -> DerrickScalingEvidence:
    """Return ``E(s)=exp(-s)*E2+exp(s)*E4`` and its exact derivatives."""

    e2 = _positive_symbolic(two_derivative_energy, "two_derivative_energy")
    e4 = _positive_symbolic(four_derivative_energy, "four_derivative_energy")
    scale = sp.sympify(logarithmic_scale)
    energy = sp.exp(-scale) * e2 + sp.exp(scale) * e4
    slope = sp.simplify(sp.diff(energy, scale).subs(scale, 0))
    curvature = sp.simplify(sp.diff(energy, scale, 2).subs(scale, 0))
    return DerrickScalingEvidence(
        scaled_energy=energy,
        slope_at_origin=slope,
        curvature_at_origin=curvature,
        stationary_condition=sp.simplify(e4 - e2),
    )


def option_c_continuum_threshold() -> sp.Integer:
    """Return the exact massless far-field threshold ``Omega**2=0``.

    As ``f,f' -> 0``, ``A/W -> 1`` and ``C/W -> 2/r**2 -> 0``.  The
    half-line radial operator therefore has the massless continuum beginning
    at zero; a positive Dirichlet-box level is not below that threshold.
    """

    return sp.Integer(0)


def is_below_continuum(eigenvalue: Any, threshold: Any) -> bool:
    """Return whether a numeric eigenvalue lies strictly below a threshold."""

    value = float(eigenvalue)
    edge = float(threshold)
    if not np.isfinite(value) or not np.isfinite(edge):
        raise ValueError("eigenvalue and threshold must be finite")
    return value < edge


def option_c_hedgehog_rhs(radius: float, state: ArrayLike) -> FloatArray:
    """Return the declared first-order Option-C hedgehog system for ``r>0``."""

    r = _positive_float(radius, "radius")
    values = np.asarray(state, dtype=np.float64)
    if values.shape != (2,) or not np.all(np.isfinite(values)):
        raise ValueError("state must contain finite field and derivative entries")
    field, derivative = values
    sine = np.sin(field)
    sine_twice = np.sin(2.0 * field)
    coefficient = r**2 + 2.0 * sine**2
    second = (
        -2.0 * r * derivative
        - sine_twice * (derivative**2 - 1.0)
        + sine_twice * sine**2 / r**2
    ) / coefficient
    return np.asarray((derivative, second), dtype=np.float64)


@dataclass(frozen=True)
class HedgehogProfileEvidence:
    """Resolution-bounded shooting evidence for the declared profile."""

    radius: FloatArray
    field: FloatArray
    radial_derivative: FloatArray
    shooting_slope: float
    outer_tail_residual: float
    two_derivative_energy: float
    four_derivative_energy: float
    energy_coefficient: float
    method: str
    function_evaluations: int


def option_c_energy_components(
    radius: ArrayLike,
    field: ArrayLike,
    radial_derivative: ArrayLike,
) -> tuple[float, float]:
    """Return the declared two- and four-derivative static energies."""

    r = _sample_vector(radius, "radius")
    f = _sample_vector(field, "field")
    fp = _sample_vector(radial_derivative, "radial_derivative")
    if r.shape != f.shape or r.shape != fp.shape:
        raise ValueError("radius, field, and radial_derivative must have equal shapes")
    if np.any(r <= 0.0) or np.any(np.diff(r) <= 0.0):
        raise ValueError("radius must be positive and strictly increasing")
    sine_squared = np.sin(f) ** 2
    e2_density = r**2 * fp**2 + 2.0 * sine_squared
    e4_density = 2.0 * sine_squared * fp**2 + sine_squared**2 / r**2
    return (
        4.0 * np.pi * trapezoid_integral(e2_density, r),
        4.0 * np.pi * trapezoid_integral(e4_density, r),
    )


def solve_option_c_hedgehog(
    *,
    inner_radius: float = 1.0e-4,
    outer_radius: float = 30.0,
    sample_points: int = 3001,
    slope_bracket: tuple[float, float] = (1.5, 2.5),
    tolerances: SolverTolerances = SolverTolerances(
        rtol=1.0e-10,
        atol=1.0e-12,
        max_step=0.02,
    ),
) -> HedgehogProfileEvidence:
    """Shoot the massless hedgehog with a two-power asymptotic Robin tail.

    The origin data use ``f(eps)=pi-C*eps`` and ``f'(eps)=-C``.  The fitted
    slope satisfies ``R*f'(R)+2*f(R)=0``, matching the massless ``r**-2``
    tail instead of forcing the field to vanish at a finite wall.
    """

    inner = _positive_float(inner_radius, "inner_radius")
    outer = _positive_float(outer_radius, "outer_radius")
    if outer <= inner:
        raise ValueError("outer_radius must exceed inner_radius")
    if isinstance(sample_points, bool) or int(sample_points) != sample_points:
        raise ValueError("sample_points must be an integer")
    points = int(sample_points)
    if points < 101:
        raise ValueError("sample_points must be at least 101")
    low = _positive_float(slope_bracket[0], "slope_bracket lower bound")
    high = _positive_float(slope_bracket[1], "slope_bracket upper bound")
    if high <= low:
        raise ValueError("slope_bracket must be strictly increasing")

    endpoint_times = np.asarray((inner, outer), dtype=np.float64)

    def integrate(slope: float, sample_times: FloatArray):
        initial = np.asarray((np.pi - slope * inner, -slope), dtype=np.float64)
        return solve_ivp_evidence(
            option_c_hedgehog_rhs,
            (inner, outer),
            initial,
            sample_times=sample_times,
            tolerances=tolerances,
            method="DOP853",
        )

    def tail_residual(slope: float) -> float:
        endpoint = integrate(slope, endpoint_times)
        return float(outer * endpoint.state[1, -1] + 2.0 * endpoint.state[0, -1])

    low_residual = tail_residual(low)
    high_residual = tail_residual(high)
    if low_residual * high_residual >= 0.0:
        raise ValueError("slope_bracket does not bracket the asymptotic residual root")
    slope = float(brentq(tail_residual, low, high, xtol=1.0e-12, rtol=1.0e-12))
    radius = np.linspace(inner, outer, points, dtype=np.float64)
    solution = integrate(slope, radius)
    field = solution.state[0]
    derivative = solution.state[1]
    tail = float(outer * derivative[-1] + 2.0 * field[-1])
    e2, e4 = option_c_energy_components(radius, field, derivative)
    return HedgehogProfileEvidence(
        radius=radius,
        field=field,
        radial_derivative=derivative,
        shooting_slope=slope,
        outer_tail_residual=tail,
        two_derivative_energy=e2,
        four_derivative_energy=e4,
        energy_coefficient=(e2 + e4) / (12.0 * np.pi**2),
        method="DOP853 shooting with r*f'+2*f Robin tail",
        function_evaluations=solution.function_evaluations,
    )


def option_c_operator_coefficients(
    radius: ArrayLike,
    field: ArrayLike,
    radial_derivative: ArrayLike,
    second_radial_derivative: ArrayLike,
) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """Return numeric ``A, C, W`` and the source-omitted mixed correction."""

    r = _sample_vector(radius, "radius")
    f = _sample_vector(field, "field")
    fp = _sample_vector(radial_derivative, "radial_derivative")
    fpp = _sample_vector(second_radial_derivative, "second_radial_derivative")
    if not (r.shape == f.shape == fp.shape == fpp.shape):
        raise ValueError("all coefficient inputs must have equal shapes")
    if np.any(r <= 0.0) or np.any(np.diff(r) <= 0.0):
        raise ValueError("radius must be positive and strictly increasing")
    sine = np.sin(f)
    cosine = np.cos(f)
    cosine_twice = np.cos(2.0 * f)
    gradient = r**2 + 2.0 * sine**2
    local = (
        2.0 * cosine_twice
        + 2.0 * cosine_twice * fp**2
        + 2.0 * sine**2 * (3.0 * cosine**2 - sine**2) / r**2
    )
    correction = -4.0 * cosine_twice * fp**2 - 2.0 * np.sin(2.0 * f) * fpp
    potential = local + correction
    return gradient, potential, gradient.copy(), correction


@dataclass(frozen=True)
class FiniteBoxSpectrumEvidence:
    """Generalized linear-FEM spectrum on an explicitly finite Dirichlet box."""

    lower_bound: float
    upper_bound: float
    points: int
    eigenvalues: tuple[float, ...]
    relative_residuals: tuple[float, ...]
    node_counts: tuple[int, ...]
    continuum_threshold: float
    below_continuum: tuple[bool, ...]


def _mode_node_count(mode: FloatArray) -> int:
    scale = float(np.max(np.abs(mode), initial=0.0))
    if scale == 0.0:
        return 0
    retained = mode[np.abs(mode) > 1.0e-8 * scale]
    if retained.size < 2:
        return 0
    return int(np.count_nonzero(retained[:-1] * retained[1:] < 0.0))


def solve_radial_finite_box_spectrum(
    radius: ArrayLike,
    gradient_coefficient: ArrayLike,
    potential_coefficient: ArrayLike,
    kinetic_weight: ArrayLike,
    *,
    mode_count: int = 4,
    continuum_threshold: float = 0.0,
    eigensolver_tolerance: float = 1.0e-10,
) -> FiniteBoxSpectrumEvidence:
    """Solve a self-adjoint generalized radial problem with endpoint Dirichlet data.

    Linear finite elements use midpoint coefficient averages and consistent
    mass matrices.  The finite-box classification is kept separate from the
    caller-supplied continuum threshold.
    """

    r = _sample_vector(radius, "radius")
    a = _sample_vector(gradient_coefficient, "gradient_coefficient")
    c = _sample_vector(potential_coefficient, "potential_coefficient")
    w = _sample_vector(kinetic_weight, "kinetic_weight")
    if not (r.shape == a.shape == c.shape == w.shape):
        raise ValueError("all finite-element inputs must have equal shapes")
    if np.any(r <= 0.0) or np.any(np.diff(r) <= 0.0):
        raise ValueError("radius must be positive and strictly increasing")
    if np.any(a <= 0.0) or np.any(w <= 0.0):
        raise ValueError("gradient coefficient and kinetic weight must be positive")
    if isinstance(mode_count, bool) or int(mode_count) != mode_count or mode_count < 1:
        raise ValueError("mode_count must be a positive integer")
    interior_size = r.size - 2
    modes = int(mode_count)
    if modes >= interior_size:
        raise ValueError("mode_count must be smaller than the interior dimension")
    tolerance = _positive_float(eigensolver_tolerance, "eigensolver_tolerance")
    threshold = float(continuum_threshold)
    if not np.isfinite(threshold):
        raise ValueError("continuum_threshold must be finite")

    spacing = np.diff(r)
    a_mid = (a[:-1] + a[1:]) / 2.0
    c_mid = (c[:-1] + c[1:]) / 2.0
    w_mid = (w[:-1] + w[1:]) / 2.0
    stiffness_diag = np.zeros(r.size, dtype=np.float64)
    mass_diag = np.zeros(r.size, dtype=np.float64)
    stiffness_off = -a_mid / spacing + c_mid * spacing / 6.0
    mass_off = w_mid * spacing / 6.0
    element_stiffness_diag = a_mid / spacing + c_mid * spacing / 3.0
    element_mass_diag = w_mid * spacing / 3.0
    stiffness_diag[:-1] += element_stiffness_diag
    stiffness_diag[1:] += element_stiffness_diag
    mass_diag[:-1] += element_mass_diag
    mass_diag[1:] += element_mass_diag

    off_k = stiffness_off[1:-1]
    off_m = mass_off[1:-1]
    matrix_k = diags(
        (off_k, stiffness_diag[1:-1], off_k),
        offsets=(-1, 0, 1),
        format="csr",
    )
    matrix_m = diags(
        (off_m, mass_diag[1:-1], off_m),
        offsets=(-1, 0, 1),
        format="csr",
    )
    initial_vector = np.linspace(1.0, 2.0, interior_size, dtype=np.float64)
    eigenvalues, eigenvectors = eigsh(
        matrix_k,
        k=modes,
        M=matrix_m,
        which="SA",
        tol=tolerance,
        v0=initial_vector,
    )
    order = np.argsort(eigenvalues)
    eigenvalues = np.asarray(eigenvalues[order], dtype=np.float64)
    eigenvectors = np.asarray(eigenvectors[:, order], dtype=np.float64)
    residuals: list[float] = []
    nodes: list[int] = []
    for index, value in enumerate(eigenvalues):
        vector = eigenvectors[:, index]
        left = matrix_k @ vector
        right = value * (matrix_m @ vector)
        scale = np.linalg.norm(left) + abs(value) * np.linalg.norm(matrix_m @ vector)
        residuals.append(float(np.linalg.norm(left - right) / max(scale, 1.0e-300)))
        nodes.append(_mode_node_count(vector))
    return FiniteBoxSpectrumEvidence(
        lower_bound=float(r[0]),
        upper_bound=float(r[-1]),
        points=int(r.size),
        eigenvalues=tuple(float(value) for value in eigenvalues),
        relative_residuals=tuple(residuals),
        node_counts=tuple(nodes),
        continuum_threshold=threshold,
        below_continuum=tuple(value < threshold for value in eigenvalues),
    )


@dataclass(frozen=True)
class ClassicalModeScaleLedger:
    """Conditional conversion from a classical eigenvalue to an energy ratio."""

    dimensionless_eigenvalue: sp.Expr
    dimensionless_frequency: sp.Expr
    inverse_time_scale: sp.Expr
    action_scale: sp.Expr
    background_energy_scale: sp.Expr
    background_dimensionless_energy: sp.Expr
    one_quantum_gap: sp.Expr
    background_energy: sp.Expr
    gap_to_background_ratio: sp.Expr


def classical_mode_scale_ledger(
    dimensionless_eigenvalue: Any,
    inverse_time_scale: Any,
    action_scale: Any,
    background_energy_scale: Any,
    background_dimensionless_energy: Any,
) -> ClassicalModeScaleLedger:
    """Expose every premise in a one-quantum harmonic-gap interpretation.

    The conditional rule ``gap=S*nu*sqrt(lambda)`` is declared here for
    bookkeeping; the classical Hessian does not derive quantization or the
    action scale ``S``.  Unless a separate premise relates ``S*nu`` to the
    background energy scale, the gap-to-background ratio remains free.
    """

    eigenvalue = _positive_symbolic(dimensionless_eigenvalue, "dimensionless_eigenvalue")
    time_scale = _positive_symbolic(inverse_time_scale, "inverse_time_scale")
    quantum = _positive_symbolic(action_scale, "action_scale")
    energy_scale = _positive_symbolic(background_energy_scale, "background_energy_scale")
    dimensionless_energy = _positive_symbolic(
        background_dimensionless_energy,
        "background_dimensionless_energy",
    )
    frequency = sp.sqrt(eigenvalue)
    gap = sp.simplify(quantum * time_scale * frequency)
    background = sp.simplify(energy_scale * dimensionless_energy)
    return ClassicalModeScaleLedger(
        dimensionless_eigenvalue=eigenvalue,
        dimensionless_frequency=frequency,
        inverse_time_scale=time_scale,
        action_scale=quantum,
        background_energy_scale=energy_scale,
        background_dimensionless_energy=dimensionless_energy,
        one_quantum_gap=gap,
        background_energy=background,
        gap_to_background_ratio=sp.simplify(gap / background),
    )
