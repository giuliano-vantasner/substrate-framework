"""Exact conditional one-loop charged-Dirac vacuum-polarization ledgers.

The APIs in this module start from a separately declared free charged-Dirac
action, fermion determinant, one-loop expansion, and shift-invariant
gauge-preserving regulator.  They do not derive a physical charged excitation,
gauge group, bare Maxwell coefficient, subtraction condition, total kinetic
normalization, or dimensional lift for the substrate framework.

The tensor convention is

``Pi_mn(q) = (q^2*g_mn - q_m*q_n) * Pi2(q^2)``.

Thus ``Pi2`` is the transverse form factor, while ``q^2*Pi2`` is the
coefficient of the mixed transverse projector.  These objects have different
mass dimensions.  Integration dimension and integer spinor trace are explicit
independent inputs; this module never analytically continues
``2**floor(d/2)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import sympy as sp


def _positive(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_positive is not True:
        raise ValueError(f"{name} must be provably positive")
    return expression


def _nonnegative(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_nonnegative is not True:
        raise ValueError(f"{name} must be provably nonnegative")
    return expression


def _real(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_real is not True:
        raise ValueError(f"{name} must be provably real")
    return expression


def _positive_integer(value: Any, name: str) -> int:
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if value < 1:
        raise ValueError(f"{name} must be positive")
    return value


def _square_matrix(value: Sequence[Sequence[Any]], name: str) -> sp.ImmutableMatrix:
    matrix = sp.ImmutableMatrix(value)
    if matrix.rows != matrix.cols or matrix.rows < 1:
        raise ValueError(f"{name} must be a nonempty square matrix")
    return matrix


@dataclass(frozen=True)
class DiracWardIntegrandEvidence:
    """Exact free-propagator Ward contraction before loop integration."""

    propagator_p: sp.ImmutableMatrix
    propagator_p_plus_q: sp.ImmutableMatrix
    spectator_vertex: sp.ImmutableMatrix
    contracted_vertex: sp.ImmutableMatrix
    contracted_integrand_trace: sp.Expr
    shifted_integrand_difference: sp.Expr
    trace_cyclicity_residual: sp.Expr
    integrated_cancellation_requires_shift_invariance: bool


def dirac_ward_integrand_evidence(
    propagator_p: Sequence[Sequence[Any]],
    propagator_p_plus_q: Sequence[Sequence[Any]],
    spectator_vertex: Sequence[Sequence[Any]],
) -> DiracWardIntegrandEvidence:
    r"""Derive the free one-loop Ward integrand as a shifted difference.

    Let ``A=S(p)``, ``B=S(p+q)`` and let ``G`` be the uncontracted current
    vertex.  The declared free inverse-propagator identity is
    ``qslash=B**-1-A**-1``.  Direct matrix multiplication and trace cyclicity
    then give

    ``Tr[qslash*B*G*A] = Tr[G*A] - Tr[G*B]``.

    A common shift-invariant regulator makes the integrated right-hand side
    vanish after one loop-momentum translation.  The algebra returned here is
    the integrand derivation; the final regulator premise remains explicit.
    """

    left = _square_matrix(propagator_p, "propagator at p")
    right = _square_matrix(propagator_p_plus_q, "propagator at p+q")
    vertex = _square_matrix(spectator_vertex, "spectator vertex")
    if right.shape != left.shape or vertex.shape != left.shape:
        raise ValueError("propagators and vertex must have one common shape")
    if sp.simplify(left.det()) == 0 or sp.simplify(right.det()) == 0:
        raise ValueError("propagators must be invertible")

    contracted_vertex = sp.ImmutableMatrix(
        (right.inv() - left.inv()).applyfunc(sp.simplify)
    )
    contracted_trace = sp.simplify(
        sp.trace(contracted_vertex * right * vertex * left)
    )
    shifted_difference = sp.simplify(
        sp.trace(vertex * left) - sp.trace(vertex * right)
    )
    return DiracWardIntegrandEvidence(
        propagator_p=left,
        propagator_p_plus_q=right,
        spectator_vertex=vertex,
        contracted_vertex=contracted_vertex,
        contracted_integrand_trace=contracted_trace,
        shifted_integrand_difference=shifted_difference,
        trace_cyclicity_residual=sp.simplify(
            contracted_trace - shifted_difference
        ),
        integrated_cancellation_requires_shift_invariance=True,
    )


@dataclass(frozen=True)
class DiracVacuumPolarizationMaster:
    """Spacelike conditional Dirac-loop master with explicit trace scheme."""

    integration_dimension: sp.Expr
    spinor_trace: int
    euclidean_momentum_squared: sp.Expr
    mass_squared: sp.Expr
    charge_magnitude: sp.Expr
    parameter: sp.Symbol
    delta: sp.Expr
    parameter_integrand: sp.Expr
    prefactor: sp.Expr
    transverse_form_factor: sp.Expr
    minkowski_projector_coefficient: sp.Expr
    charge_squared_mass_dimension: sp.Expr
    delta_power_mass_dimension: sp.Expr
    transverse_form_factor_mass_dimension: sp.Expr
    projector_coefficient_mass_dimension: sp.Expr


def dirac_vacuum_polarization_master(
    integration_dimension: Any,
    spinor_trace: int,
    euclidean_momentum_squared: Any,
    mass_squared: Any,
    charge_magnitude: Any,
) -> DiracVacuumPolarizationMaster:
    r"""Return the exact spacelike Feynman-parameter master.

    Set ``Q=-q_M^2>0`` and
    ``Delta=M2+x*(1-x)*Q``.  For a declared integer spinor trace ``n_gamma``
    and a charge whose square has mass dimension ``4-d``, the source tensor
    convention gives

    ``Pi2(-Q) = -2*n_gamma*e^2/(4*pi)^(d/2) * Gamma(2-d/2)
    * Integral[x*(1-x)*Delta^(d/2-2), (x,0,1)]``.

    The integration dimension may be analytic, but ``spinor_trace`` is not
    inferred from it.  At even dimensions where the Gamma function has a
    pole, the returned bare expression remains divergent until a separately
    declared regulator and counterterm are supplied.
    """

    dimension = _positive(integration_dimension, "integration dimension")
    trace = _positive_integer(spinor_trace, "spinor trace")
    momentum_squared = _positive(
        euclidean_momentum_squared,
        "Euclidean momentum squared",
    )
    mass2 = _nonnegative(mass_squared, "mass squared")
    charge = _positive(charge_magnitude, "charge magnitude")

    x = sp.Symbol("x", real=True)
    delta = mass2 + x * (1 - x) * momentum_squared
    parameter_integrand = x * (1 - x) * delta ** (dimension / 2 - 2)
    prefactor = sp.simplify(
        -2
        * trace
        * charge**2
        * sp.gamma(2 - dimension / 2)
        / (4 * sp.pi) ** (dimension / 2)
    )
    form_factor = prefactor * sp.Integral(parameter_integrand, (x, 0, 1))
    charge_dimension = sp.simplify(4 - dimension)
    delta_dimension = sp.simplify(dimension - 4)
    return DiracVacuumPolarizationMaster(
        integration_dimension=dimension,
        spinor_trace=trace,
        euclidean_momentum_squared=momentum_squared,
        mass_squared=mass2,
        charge_magnitude=charge,
        parameter=x,
        delta=delta,
        parameter_integrand=parameter_integrand,
        prefactor=prefactor,
        transverse_form_factor=form_factor,
        minkowski_projector_coefficient=-momentum_squared * form_factor,
        charge_squared_mass_dimension=charge_dimension,
        delta_power_mass_dimension=delta_dimension,
        transverse_form_factor_mass_dimension=sp.simplify(
            charge_dimension + delta_dimension
        ),
        projector_coefficient_mass_dimension=sp.Integer(2),
    )


@dataclass(frozen=True)
class MasslessDiracQED2Evidence:
    """Exact nonzero-spacelike-momentum endpoint for one Dirac fermion."""

    master: DiracVacuumPolarizationMaster
    transverse_form_factor: sp.Expr
    minkowski_projector_coefficient: sp.Expr
    scalar_comparator_is_inapplicable: bool


def massless_dirac_qed2_evidence(
    euclidean_momentum_squared: Any,
    charge_magnitude: Any,
) -> MasslessDiracQED2Evidence:
    r"""Evaluate the ``d=2``, ``n_gamma=2``, ``M2=0`` fermion endpoint.

    For ``Q>0``, ``Pi2(-Q)=-e^2/(pi*Q)`` and the source-convention mixed
    projector coefficient ``q^2*Pi2`` is ``e^2/pi``.  This is a massless
    charged-Dirac result.  It does not apply to the complex-scalar bubble plus
    seagull in :mod:`substrate_framework.vacuum_polarization`.
    """

    master = dirac_vacuum_polarization_master(
        2,
        2,
        euclidean_momentum_squared,
        0,
        charge_magnitude,
    )
    evaluated = sp.simplify(
        master.prefactor
        * sp.integrate(
            master.parameter_integrand,
            (master.parameter, 0, 1),
        )
    )
    return MasslessDiracQED2Evidence(
        master=master,
        transverse_form_factor=evaluated,
        minkowski_projector_coefficient=sp.simplify(
            -master.euclidean_momentum_squared * evaluated
        ),
        scalar_comparator_is_inapplicable=True,
    )


@dataclass(frozen=True)
class DiracQED4ZeroMomentumRenormalization:
    """Fixed-four-spinor dimensional-regulator and counterterm ledger."""

    regulator: sp.Symbol
    charge_magnitude: sp.Expr
    mass_squared: sp.Expr
    renormalization_scale_squared: sp.Expr
    finite_local_counterterm: sp.Expr
    bare_form_factor: sp.Expr
    laurent_pole_residue: sp.Expr
    laurent_finite_part: sp.Expr
    msbar_local_counterterm: sp.Expr
    renormalized_limit_from_bare_plus_counterterm: sp.Expr
    expected_renormalized_form_factor: sp.Expr
    renormalization_residual: sp.Expr
    mass_squared_log_slope: sp.Expr
    mass_log_slope: sp.Expr
    scale_squared_log_slope: sp.Expr
    scale_log_slope: sp.Expr


def dirac_qed4_zero_momentum_renormalization(
    charge_magnitude: Any,
    mass_squared: Any,
    renormalization_scale_squared: Any,
    finite_local_counterterm: Any = 0,
    *,
    regulator: sp.Symbol | None = None,
) -> DiracQED4ZeroMomentumRenormalization:
    r"""Return the ``d=4-2*epsilon`` zero-momentum MS-bar family.

    Four spinor components are held fixed while only the integration dimension
    is continued.  With ``mu2`` denoting the squared regulator scale, the bare
    source-convention form factor is

    ``-e^2/(12*pi^2)*Gamma(epsilon)*(4*pi*mu2/M2)^epsilon``.

    The MS-bar pole subtraction still permits an arbitrary finite local
    counterterm.  Consequently this API derives the pole and logarithmic
    slopes, but deliberately cannot select a total Maxwell coefficient.
    """

    charge = _positive(charge_magnitude, "charge magnitude")
    mass2 = _positive(mass_squared, "mass squared")
    scale2 = _positive(
        renormalization_scale_squared,
        "renormalization scale squared",
    )
    finite = _real(finite_local_counterterm, "finite local counterterm")
    epsilon = regulator or sp.Symbol("epsilon", positive=True)
    if not isinstance(epsilon, sp.Symbol) or epsilon.is_positive is not True:
        raise ValueError("regulator must be a positive SymPy symbol")

    common = sp.simplify(charge**2 / (12 * sp.pi**2))
    bare = sp.simplify(
        -common
        * sp.gamma(epsilon)
        * (4 * sp.pi * scale2 / mass2) ** epsilon
    )
    residue = sp.simplify(sp.limit(epsilon * bare, epsilon, 0, dir="+"))
    finite_part = sp.expand(
        sp.expand_log(
            sp.limit(bare - residue / epsilon, epsilon, 0, dir="+"),
            force=True,
        )
    )
    counterterm = sp.simplify(
        common
        * (1 / epsilon - sp.EulerGamma + sp.log(4 * sp.pi))
        + finite
    )
    renormalized_limit = sp.expand(
        sp.expand_log(
            sp.limit(bare + counterterm, epsilon, 0, dir="+"),
            force=True,
        )
    )
    expected = sp.simplify(common * sp.log(mass2 / scale2) + finite)
    residual = sp.simplify(
        sp.expand_log(renormalized_limit - expected, force=True)
    )
    return DiracQED4ZeroMomentumRenormalization(
        regulator=epsilon,
        charge_magnitude=charge,
        mass_squared=mass2,
        renormalization_scale_squared=scale2,
        finite_local_counterterm=finite,
        bare_form_factor=bare,
        laurent_pole_residue=residue,
        laurent_finite_part=finite_part,
        msbar_local_counterterm=counterterm,
        renormalized_limit_from_bare_plus_counterterm=renormalized_limit,
        expected_renormalized_form_factor=expected,
        renormalization_residual=residual,
        mass_squared_log_slope=sp.simplify(
            mass2 * sp.diff(renormalized_limit, mass2)
        ),
        mass_log_slope=sp.simplify(
            2 * mass2 * sp.diff(renormalized_limit, mass2)
        ),
        scale_squared_log_slope=sp.simplify(
            scale2 * sp.diff(renormalized_limit, scale2)
        ),
        scale_log_slope=sp.simplify(
            2 * scale2 * sp.diff(renormalized_limit, scale2)
        ),
    )


@dataclass(frozen=True)
class DiracQED4SubtractedTimelikeEvidence:
    """Real finite subtraction strictly below the fermion-pair threshold."""

    charge_magnitude: sp.Expr
    timelike_mass_ratio: sp.Expr
    parameter: sp.Symbol
    logarithm_argument: sp.Expr
    parameter_integrand: sp.Expr
    subtracted_form_factor: sp.Expr
    cubic_series: sp.Expr
    linear_coefficient: sp.Expr
    quadratic_coefficient: sp.Expr
    cubic_coefficient: sp.Expr
    feynman_weight_maximum: sp.Expr
    first_branch_point: sp.Expr
    convergence_radius: sp.Expr
    above_threshold_requires_i0: bool


def dirac_qed4_subtracted_timelike_evidence(
    charge_magnitude: Any,
    timelike_mass_ratio: Any,
) -> DiracQED4SubtractedTimelikeEvidence:
    r"""Return ``Pi2(q^2)-Pi2(0)`` for ``0<=w=q^2/M2<4``.

    In the source tensor convention the exact finite expression is

    ``e^2/(2*pi^2) * Integral[x*(1-x)*log(1-w*x*(1-x)), (x,0,1)]``.

    Its real power series has radius four.  This API does not silently cross
    the branch point: above threshold the Minkowski ``-i0`` boundary value and
    a complex logarithm must be requested through a different, explicitly
    typed interface.
    """

    charge = _positive(charge_magnitude, "charge magnitude")
    ratio = _real(timelike_mass_ratio, "timelike mass ratio")
    if ratio.is_number and (
        ratio.is_nonnegative is not True or (4 - ratio).is_positive is not True
    ):
        raise ValueError("timelike mass ratio must satisfy 0 <= w < 4")
    if not ratio.is_number and ratio.is_nonnegative is not True:
        raise ValueError("symbolic timelike mass ratio must be nonnegative")

    x = sp.Symbol("x", real=True)
    weight = x * (1 - x)
    argument = sp.simplify(1 - ratio * weight)
    integrand = weight * sp.log(argument)
    prefactor = sp.simplify(charge**2 / (2 * sp.pi**2))
    exact = prefactor * sp.Integral(integrand, (x, 0, 1))
    series_integrand = sp.series(integrand, ratio, 0, 4).removeO()
    cubic_series = sp.simplify(
        prefactor * sp.integrate(series_integrand, (x, 0, 1))
    )
    expanded_series = sp.expand(cubic_series)
    return DiracQED4SubtractedTimelikeEvidence(
        charge_magnitude=charge,
        timelike_mass_ratio=ratio,
        parameter=x,
        logarithm_argument=argument,
        parameter_integrand=integrand,
        subtracted_form_factor=exact,
        cubic_series=cubic_series,
        linear_coefficient=sp.simplify(expanded_series.coeff(ratio, 1)),
        quadratic_coefficient=sp.simplify(expanded_series.coeff(ratio, 2)),
        cubic_coefficient=sp.simplify(expanded_series.coeff(ratio, 3)),
        feynman_weight_maximum=sp.Rational(1, 4),
        first_branch_point=sp.Integer(4),
        convergence_radius=sp.Integer(4),
        above_threshold_requires_i0=True,
    )


@dataclass(frozen=True)
class DiracRepresentationWeightEvidence:
    """Convention-invariant coupling and generator-trace composition."""

    coupling: sp.Expr
    generator_trace: sp.Expr
    generator_rescaling: sp.Expr
    original_loop_weight: sp.Expr
    rescaled_coupling: sp.Expr
    rescaled_generator_trace: sp.Expr
    rescaled_loop_weight: sp.Expr
    convention_residual: sp.Expr


def dirac_representation_weight_evidence(
    coupling: Any,
    generator_trace: Any,
    generator_rescaling: Any,
) -> DiracRepresentationWeightEvidence:
    """Return the invariant loop weight under a generator convention change.

    If ``T -> c*T`` at the generator level, then the quadratic trace changes
    as ``tr(T*T) -> c^2*tr(T*T)`` while the covariant-derivative coupling must
    change as ``g -> g/c``.  Only ``g^2*tr(T*T)`` is invariant.  This algebra
    does not select a representation, gauge group, or physical coupling.
    """

    gauge_coupling = _positive(coupling, "coupling")
    trace = _positive(generator_trace, "generator trace")
    rescaling = _positive(generator_rescaling, "generator rescaling")
    original = sp.simplify(gauge_coupling**2 * trace)
    rescaled_coupling = sp.simplify(gauge_coupling / rescaling)
    rescaled_trace = sp.simplify(rescaling**2 * trace)
    rescaled_weight = sp.simplify(rescaled_coupling**2 * rescaled_trace)
    return DiracRepresentationWeightEvidence(
        coupling=gauge_coupling,
        generator_trace=trace,
        generator_rescaling=rescaling,
        original_loop_weight=original,
        rescaled_coupling=rescaled_coupling,
        rescaled_generator_trace=rescaled_trace,
        rescaled_loop_weight=rescaled_weight,
        convention_residual=sp.simplify(rescaled_weight - original),
    )
