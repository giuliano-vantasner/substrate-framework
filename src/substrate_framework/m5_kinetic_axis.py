"""Conditional P240 kinetic-axis candidates for the M5 4x4 action.

This module implements the two issue-147 candidate families selected for the
issue-146 P240 campaign.  It is proposal infrastructure, not accepted
framework authority.

Let ``X = eta^{-1} M``, let ``P_t`` be its selected rank-one timelike mixed
projector, ``Q = I-P_t``, and let ``Y = Q X Q`` be the projected spatial mixed
tensor.  A constrained rank-one spacelike projector ``P_N`` labels the clock
axis.  The L1 density is

``-kappa/2 Tr(P_N Y)^2 P_t^{mu nu} Tr(Z_mu Z_nu)``,

where ``Z_mu = Q (partial_mu Y) Q`` and
``P_t^{mu nu} = (P_t eta^{-1})^{mu nu}``.  In the comoving frame it is a
nonnegative time-derivative norm.  It vanishes identically for every static
uniform-time-row 3x3 field, gives positive localized clock inertia when the
selected physical axis has nonzero eigenvalue and the tangent eigenvalues
split, and assigns zero inertia to a selected zero-eigenline escape.

The L2 family replaces the derivative norm by the Skyrme-like current
``[Y,Z_mu]``.  Its quartic member is axis blind.  Multiplication by
``Tr(P_N Y)^2`` produces the eligible sextic repair, at greater field order
than L1.  Positivity statements are conditional on the declared timelike and
spacelike projector constraints and on ``Y`` and its projected derivatives
being self-adjoint on the positive spatial subspace.
"""

from __future__ import annotations

from itertools import product
from typing import Sequence

import sympy as sp

from .m5_covariant_action import MINKOWSKI_MOSTLY_PLUS
from .m5_covariant_action import double_two_form_contraction


def _square_matrix(
    value: sp.MatrixBase | Sequence[Sequence[object]], name: str
) -> sp.Matrix:
    matrix = sp.Matrix(value)
    if matrix.rows != matrix.cols:
        raise ValueError(f"{name} must be square")
    return matrix


def _common_dimension(*matrices: sp.MatrixBase) -> int:
    dimensions = {matrix.rows for matrix in matrices}
    if len(dimensions) != 1:
        raise ValueError("all matrices must have the same dimension")
    return next(iter(dimensions))


def _candidate_data(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    axis_projector: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_derivatives: Sequence[
        sp.MatrixBase | Sequence[Sequence[object]]
    ],
    metric_covariant: sp.MatrixBase | Sequence[Sequence[object]],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix, tuple[sp.Matrix, ...], sp.Matrix]:
    projector_t = _square_matrix(timelike_projector, "timelike_projector")
    projector_n = _square_matrix(axis_projector, "axis_projector")
    spatial = _square_matrix(projected_spatial_mixed, "projected_spatial_mixed")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    derivatives = tuple(
        _square_matrix(derivative, f"projected_spatial_derivatives[{index}]")
        for index, derivative in enumerate(projected_spatial_derivatives)
    )
    dimension = _common_dimension(
        projector_t, projector_n, spatial, metric, *derivatives
    )
    if len(derivatives) != dimension:
        raise ValueError("one projected spatial derivative is required per index")
    if metric.det() == 0:
        raise ValueError("metric_covariant must be invertible")
    return projector_t, projector_n, spatial, derivatives, metric


def axis_eigenvalue(
    axis_projector: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
) -> sp.Expr:
    """Return the selected spatial eigenvalue ``Tr(P_N Y)``.

    It is an eigenvalue only on the declared constraint surface
    ``[P_N,Y]=0`` with rank-one ``P_N``.  The trace remains a Lorentz
    similarity scalar before that constraint is imposed.
    """

    projector = _square_matrix(axis_projector, "axis_projector")
    spatial = _square_matrix(projected_spatial_mixed, "projected_spatial_mixed")
    _common_dimension(projector, spatial)
    return sp.factor(sp.trace(projector * spatial))


def spatial_inverse_metric_from_timelike_projector(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.ImmutableMatrix:
    """Return the positive-spatial contravariant metric ``eta^-1-P_t eta^-1``.

    In the comoving frame it is ``diag(0,1,1,1)``.  Because ``P_t`` follows
    the M-derived timelike eigenline, the result transforms as a contravariant
    rank-two tensor and introduces no external preferred frame.
    """

    projector = _square_matrix(timelike_projector, "timelike_projector")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    _common_dimension(projector, metric)
    if metric.det() == 0:
        raise ValueError("metric_covariant must be invertible")
    inverse = metric.inv()
    return sp.ImmutableMatrix((inverse - projector * inverse).applyfunc(sp.factor))


def spatial_covariant_metric_from_timelike_projector(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.ImmutableMatrix:
    """Return ``q_ab=eta_ab-(eta P_t)_ab`` for the selected time line.

    If ``P_t=-u (eta u)^T`` with ``u.eta.u=-1``, this is
    ``eta+(eta u)(eta u)^T``.  It is symmetric, annihilates ``u``, and is the
    covariant positive-spatial metric required to contract a contravariant
    current.  In the comoving frame it is ``diag(0,1,1,1)``.
    """

    projector = _square_matrix(timelike_projector, "timelike_projector")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    _common_dimension(projector, metric)
    if metric.det() == 0:
        raise ValueError("metric_covariant must be invertible")
    return sp.ImmutableMatrix((metric - metric * projector).applyfunc(sp.factor))


def spatial_curvature_lagrangian_density(
    curvature: sp.NDimArray,
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the L1 action's spatial-only curvature density.

    This replaces, rather than supplements, the old external Minkowski
    contraction.  In a static uniform-time-row frame it is exactly the full
    source 3x3 curvature density.  Curvature with one timelike spacetime leg
    is removed and the selected L1 derivative norm supplies the complete
    clock kinetic channel.
    """

    spatial_inverse = spatial_inverse_metric_from_timelike_projector(
        timelike_projector, metric_covariant
    )
    return sp.factor(
        -sp.Rational(1, 2)
        * double_two_form_contraction(
            curvature, spatial_inverse, internal_inverse_metric
        )
    )


def spatial_curvature_hamiltonian_density(
    curvature: sp.NDimArray,
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the nonnegative spatial-curvature Hamiltonian contribution."""

    return -spatial_curvature_lagrangian_density(
        curvature,
        timelike_projector,
        internal_inverse_metric,
        metric_covariant,
    )


def spatially_projected_derivatives(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    derivatives: Sequence[sp.MatrixBase | Sequence[Sequence[object]]],
) -> tuple[sp.ImmutableMatrix, ...]:
    """Return ``Q derivative_mu Q`` for ``Q=I-P_t`` exactly."""

    projector = _square_matrix(timelike_projector, "timelike_projector")
    matrices = tuple(
        _square_matrix(derivative, f"derivatives[{index}]")
        for index, derivative in enumerate(derivatives)
    )
    dimension = _common_dimension(projector, *matrices)
    if len(matrices) != dimension:
        raise ValueError("one derivative is required per spacetime index")
    complement = sp.eye(dimension) - projector
    return tuple(
        sp.ImmutableMatrix((complement * derivative * complement).applyfunc(sp.factor))
        for derivative in matrices
    )


def kinetic_axis_lagrangian_density(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    axis_projector: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_derivatives: Sequence[
        sp.MatrixBase | Sequence[Sequence[object]]
    ],
    stiffness: object,
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the L1 field-dependent kinetic-axis density.

    The derivative covector is contracted only along the M-derived timelike
    line.  In its comoving frame the density is
    ``kappa/2 * Tr(P_N Y)^2 * Tr(Z_0^2)``.  For positive ``kappa`` this is a
    nonnegative Hamiltonian contribution on the declared spatial
    self-adjoint branch.  No positivity is inferred for unconstrained input
    matrices.
    """

    projector_t, projector_n, spatial, derivatives, metric = _candidate_data(
        timelike_projector,
        axis_projector,
        projected_spatial_mixed,
        projected_spatial_derivatives,
        metric_covariant,
    )
    projected = spatially_projected_derivatives(projector_t, derivatives)
    timelike_contravariant = projector_t * metric.inv()
    selected = axis_eigenvalue(projector_n, spatial)
    contraction = sum(
        timelike_contravariant[mu, nu] * sp.trace(projected[mu] * projected[nu])
        for mu, nu in product(range(metric.rows), repeat=2)
    )
    return sp.factor(-sp.sympify(stiffness) * selected**2 * contraction / 2)


def kinetic_axis_comoving_hamiltonian_density(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    axis_projector: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
    comoving_time_derivative: sp.MatrixBase | Sequence[Sequence[object]],
    stiffness: object,
) -> sp.Expr:
    """Return the L1 Hamiltonian for a pure comoving-time derivative."""

    projector_t = _square_matrix(timelike_projector, "timelike_projector")
    projector_n = _square_matrix(axis_projector, "axis_projector")
    spatial = _square_matrix(projected_spatial_mixed, "projected_spatial_mixed")
    derivative = _square_matrix(comoving_time_derivative, "comoving_time_derivative")
    dimension = _common_dimension(projector_t, projector_n, spatial, derivative)
    complement = sp.eye(dimension) - projector_t
    projected = complement * derivative * complement
    selected = axis_eigenvalue(projector_n, spatial)
    return sp.factor(
        sp.sympify(stiffness) * selected**2 * sp.trace(projected**2) / 2
    )


def timelike_skyrme_lagrangian_density(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_derivatives: Sequence[
        sp.MatrixBase | Sequence[Sequence[object]]
    ],
    stiffness: object,
    *,
    axis_projector: sp.MatrixBase | Sequence[Sequence[object]] | None = None,
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the L2 quartic current or its axis-weighted sextic repair.

    The current is ``K_mu=[Y,Q(partial_mu Y)Q]`` and its positive spatial
    target metric is ``q(K_mu,K_nu)=-Tr(K_mu K_nu)/2``.  With no
    ``axis_projector`` the density is quartic and axis blind.  Supplying
    ``axis_projector`` multiplies it by ``Tr(P_N Y)^2`` and gives the sextic
    wrong-axis-sensitive member.
    """

    projector_t = _square_matrix(timelike_projector, "timelike_projector")
    spatial = _square_matrix(projected_spatial_mixed, "projected_spatial_mixed")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    derivatives = tuple(
        _square_matrix(derivative, f"projected_spatial_derivatives[{index}]")
        for index, derivative in enumerate(projected_spatial_derivatives)
    )
    dimension = _common_dimension(projector_t, spatial, metric, *derivatives)
    if len(derivatives) != dimension:
        raise ValueError("one projected spatial derivative is required per index")
    if metric.det() == 0:
        raise ValueError("metric_covariant must be invertible")
    projected = spatially_projected_derivatives(projector_t, derivatives)
    currents = tuple(spatial * derivative - derivative * spatial for derivative in projected)
    timelike_contravariant = projector_t * metric.inv()
    contraction = sum(
        timelike_contravariant[mu, nu]
        * (-sp.trace(currents[mu] * currents[nu]) / 2)
        for mu, nu in product(range(dimension), repeat=2)
    )
    weight = sp.Integer(1)
    if axis_projector is not None:
        weight = axis_eigenvalue(axis_projector, spatial) ** 2
    return sp.factor(-sp.sympify(stiffness) * weight * contraction)


def alternating_three_current(
    currents: Sequence[sp.MatrixBase | Sequence[Sequence[object]]],
) -> sp.ImmutableMatrix:
    """Return ``B^mu=epsilon^(mu nu rho sigma)Tr(K_nu K_rho K_sigma)/6``.

    This four-dimensional current is cubic in the supplied mixed-matrix
    currents.  The normalization removes the six permutations of the three
    complementary indices.
    """

    matrices = tuple(
        _square_matrix(current, f"currents[{index}]")
        for index, current in enumerate(currents)
    )
    dimension = _common_dimension(*matrices)
    if dimension != 4 or len(matrices) != 4:
        raise ValueError("the alternating current requires four 4x4 currents")
    return sp.ImmutableMatrix(
        4,
        1,
        lambda mu, _: sp.factor(
            sum(
                sp.LeviCivita(mu, nu, rho, sigma)
                * sp.trace(matrices[nu] * matrices[rho] * matrices[sigma])
                for nu, rho, sigma in product(range(4), repeat=3)
            )
            / 6
        ),
    )


def alternating_sextic_lagrangian_density(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    axis_projector: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_derivatives: Sequence[
        sp.MatrixBase | Sequence[Sequence[object]]
    ],
    stiffness: object,
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the axis-weighted alternating derivative-sextic density.

    With ``Z_mu=Q(partial_mu Y)Q``, ``K_mu=[Y,Z_mu]``, and
    ``B^mu=epsilon Tr(K K K)/6``, the density is
    ``kappa Tr(P_N Y)^2 q_mu_nu B^mu B^nu``.  The full covariant spatial
    metric ``q(P_t)`` is load-bearing away from the comoving zero-boost slice;
    replacing it by a bare sum of coordinate spatial components is not an
    equivalent field functional.
    """

    projector_t, projector_n, spatial, derivatives, metric = _candidate_data(
        timelike_projector,
        axis_projector,
        projected_spatial_mixed,
        projected_spatial_derivatives,
        metric_covariant,
    )
    projected = spatially_projected_derivatives(projector_t, derivatives)
    currents = tuple(
        spatial * derivative - derivative * spatial for derivative in projected
    )
    alternating = alternating_three_current(currents)
    spatial_metric = spatial_covariant_metric_from_timelike_projector(
        projector_t, metric
    )
    selected = axis_eigenvalue(projector_n, spatial)
    return sp.factor(
        sp.sympify(stiffness)
        * selected**2
        * (alternating.T * spatial_metric * alternating)[0]
    )


def axis_pontryagin_pseudoscalar(
    curvature: sp.NDimArray,
    axis_projector: sp.MatrixBase | Sequence[Sequence[object]],
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
) -> sp.Expr:
    r"""Return the axis-inserted external Pontryagin pseudoscalar.

    The frozen normalization is

    ``P_N(F)=epsilon^(mu nu rho sigma) F_(mu nu a b) F_(rho sigma c d)``
    ``       * (P_N h)^(a c) h^(b d) / 8``.

    The external epsilon forces one curvature factor to carry a timelike
    spacetime leg and the other to carry a complementary spatial pair.  It is
    therefore exactly zero on every static 3x3 field.  For source curvature
    ``F=[D_mu,D_nu]_eta`` it is linear in ``D_0``.  It is a scalar under
    proper Lorentz transformations and flips under parity.
    """

    projector = _square_matrix(axis_projector, "axis_projector")
    internal_metric = _square_matrix(
        internal_inverse_metric, "internal_inverse_metric"
    )
    dimension = _common_dimension(projector, internal_metric)
    if dimension != 4 or tuple(curvature.shape) != (4, 4, 4, 4):
        raise ValueError("the axis Pontryagin invariant requires four dimensions")
    axis_metric = projector * internal_metric
    value = sum(
        sp.LeviCivita(mu, nu, rho, sigma)
        * curvature[mu, nu, internal_a, internal_b]
        * curvature[rho, sigma, internal_c, internal_d]
        * axis_metric[internal_a, internal_c]
        * internal_metric[internal_b, internal_d]
        for mu, nu, rho, sigma, internal_a, internal_b, internal_c, internal_d in product(
            range(4), repeat=8
        )
    )
    return sp.factor(value / 8)


def axis_weighted_pontryagin_lagrangian_density(
    curvature: sp.NDimArray,
    axis_projector: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    strength: object,
) -> sp.Expr:
    r"""Return the parity-even L2 quartic-curvature clock density.

    ``L_L2 = gamma/2 * Tr(P_N Y)^2 * P_N(F)^2``.

    For positive ``gamma`` this is nonnegative and, because ``P_N(F)`` is
    linear in the clock velocity, its Legendre Hamiltonian equals the density.
    The eigenvalue weight makes the density zero on a selected zero-eigenline.
    Static 3x3 and Coulomb fields have zero pseudoscalar before the weight is
    evaluated.
    """

    selected = axis_eigenvalue(axis_projector, projected_spatial_mixed)
    pseudoscalar = axis_pontryagin_pseudoscalar(
        curvature, axis_projector, internal_inverse_metric
    )
    return sp.factor(sp.sympify(strength) * selected**2 * pseudoscalar**2 / 2)


def fixed_j_derrick_energy(
    scale: object,
    curvature_coefficient: object,
    current_coefficient: object,
    potential_coefficient: object,
    inertia_coefficient: object,
    angular_momentum: object,
) -> sp.Expr:
    """Return the P240 fixed-J scale ledger.

    For a three-dimensional profile ``Y(x/R)``, the M5 curvature, positive
    two-derivative current, potential, and L1 inertia scale respectively as
    ``R^-1``, ``R``, ``R^3``, and ``R^3``.  With the convention
    ``E_rot=J^2/(4 I)``, this returns
    ``A/R + C R + B R^3 + J^2/(4 I0 R^3)``.  Positivity and existence of an
    actual stationary field are caller obligations.
    """

    radius = sp.sympify(scale)
    curvature = sp.sympify(curvature_coefficient)
    current = sp.sympify(current_coefficient)
    potential = sp.sympify(potential_coefficient)
    inertia = sp.sympify(inertia_coefficient)
    momentum = sp.sympify(angular_momentum)
    return sp.factor(
        curvature / radius
        + current * radius
        + potential * radius**3
        + momentum**2 / (4 * inertia * radius**3)
    )
