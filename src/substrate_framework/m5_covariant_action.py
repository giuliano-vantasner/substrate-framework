"""Conditional local M5 spectral-Cartan action primitives.

This module is the reusable implementation surface for proposal P239.  It is
not an accepted framework claim.  The construction applies on the open field
branch where the mixed order parameter ``X = eta^{-1} M`` has a simple real
eigenline that is timelike with respect to ``eta`` and is continuously
connected to the vacuum ``g`` eigenline.

For the spectral idempotent ``P_t`` of that line, the inverse Cartan metric is

``h^{ab} = eta^{ab} - 2 P_t^a_c eta^{cb}``.

Equivalently, if ``u`` is the normalized timelike eigenvector then
``P_t = -u (eta u)^T`` and ``h^{-1} = eta^{-1} + 2 u u^T``.  Thus ``h^{-1}``
is positive definite while remaining a covariant local algebraic function of
``M``.  The P239 action contracts the spacetime curvature pair with ``eta``
and its internal pair with ``h``.  Its selected potential uses the same
projector to lift the complete M5.17 spatial Landau-de Gennes potential to a
Lorentz scalar, rather than replacing that spatial functional by a merely
vacuum-matched spectral potential.  No fitted force or frequency parameter is
introduced here.
"""

from __future__ import annotations

from itertools import combinations, product
from typing import Iterable, Sequence

import sympy as sp


MINKOWSKI_MOSTLY_PLUS = sp.ImmutableMatrix(sp.diag(-1, 1, 1, 1))
TWO_FORM_PAIRS_4D = tuple(combinations(range(4), 2))


def _square_matrix(
    value: sp.MatrixBase | Sequence[Sequence[object]], name: str
) -> sp.Matrix:
    matrix = sp.Matrix(value)
    if matrix.rows != matrix.cols:
        raise ValueError(f"{name} must be square")
    return matrix


def _validate_same_dimension(*matrices: sp.MatrixBase) -> int:
    dimensions = {matrix.rows for matrix in matrices}
    if len(dimensions) != 1:
        raise ValueError("all matrices must have the same dimension")
    return next(iter(dimensions))


def eta_commutator(
    left: sp.MatrixBase | Sequence[Sequence[object]],
    right: sp.MatrixBase | Sequence[Sequence[object]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.ImmutableMatrix:
    """Return ``left eta^{-1} right - right eta^{-1} left`` exactly."""

    left_matrix = _square_matrix(left, "left")
    right_matrix = _square_matrix(right, "right")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    _validate_same_dimension(left_matrix, right_matrix, metric)
    if metric.det() == 0:
        raise ValueError("metric_covariant must be invertible")
    return sp.ImmutableMatrix(
        (
            left_matrix * metric.inv() * right_matrix
            - right_matrix * metric.inv() * left_matrix
        ).applyfunc(sp.expand)
    )


def m5_curvature_from_derivatives(
    derivatives: Sequence[sp.MatrixBase | Sequence[Sequence[object]]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.ImmutableDenseNDimArray:
    """Build ``F_{mu nu a b}=[D_mu,D_nu]_eta`` from symmetric ``D_mu``.

    The number of derivative matrices is required to equal the internal
    dimension.  This is the four-dimensional M5 index convention, generalized
    only enough to make shape failures explicit.
    """

    metric = _square_matrix(metric_covariant, "metric_covariant")
    derivative_matrices = tuple(
        _square_matrix(derivative, f"derivatives[{index}]")
        for index, derivative in enumerate(derivatives)
    )
    dimension = _validate_same_dimension(metric, *derivative_matrices)
    if len(derivative_matrices) != dimension:
        raise ValueError("one derivative matrix is required per spacetime index")
    if any(matrix != matrix.T for matrix in derivative_matrices):
        raise ValueError("M5 derivative matrices must be symmetric")

    components = [sp.Integer(0)] * (dimension**4)
    curvature = sp.MutableDenseNDimArray(components, (dimension,) * 4)
    for mu, nu in product(range(dimension), repeat=2):
        commutator = eta_commutator(
            derivative_matrices[mu], derivative_matrices[nu], metric
        )
        for internal_a, internal_b in product(range(dimension), repeat=2):
            curvature[mu, nu, internal_a, internal_b] = commutator[
                internal_a, internal_b
            ]
    return sp.ImmutableDenseNDimArray(curvature)


def wedge_inverse_metric(
    inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
) -> sp.ImmutableMatrix:
    """Return the inverse metric induced on unordered covariant two-form pairs."""

    metric = _square_matrix(inverse_metric, "inverse_metric")
    pairs = tuple(combinations(range(metric.rows), 2))
    induced = sp.Matrix(
        len(pairs),
        len(pairs),
        lambda row, column: sp.expand(
            metric[pairs[row][0], pairs[column][0]]
            * metric[pairs[row][1], pairs[column][1]]
            - metric[pairs[row][0], pairs[column][1]]
            * metric[pairs[row][1], pairs[column][0]]
        ),
    )
    return sp.ImmutableMatrix(induced)


def double_two_form_contraction(
    curvature: sp.NDimArray,
    spacetime_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
) -> sp.Expr:
    """Contract a double two-form without assuming pair exchange or Bianchi.

    Returns
    ``F_mnab F_rscd q^(mr) q^(ns) h^(ac) h^(bd)``.  The factor four below
    restores both ordered antisymmetric index pairs from their six-component
    representations.
    """

    spacetime_metric = _square_matrix(
        spacetime_inverse_metric, "spacetime_inverse_metric"
    )
    internal_metric = _square_matrix(internal_inverse_metric, "internal_inverse_metric")
    dimension = _validate_same_dimension(spacetime_metric, internal_metric)
    if tuple(curvature.shape) != (dimension,) * 4:
        raise ValueError("curvature shape must match both metric dimensions")

    pairs = tuple(combinations(range(dimension), 2))
    spacetime_wedge = wedge_inverse_metric(spacetime_metric)
    internal_wedge = wedge_inverse_metric(internal_metric)
    pair_curvature = sp.Matrix(
        len(pairs),
        len(pairs),
        lambda row, column: curvature[
            pairs[row][0], pairs[row][1], pairs[column][0], pairs[column][1]
        ],
    )
    contraction = 4 * sum(
        pair_curvature[left_space, left_internal]
        * spacetime_wedge[left_space, right_space]
        * internal_wedge[left_internal, right_internal]
        * pair_curvature[right_space, right_internal]
        for left_space, left_internal, right_space, right_internal in product(
            range(len(pairs)), repeat=4
        )
    )
    return sp.factor(contraction)


def spectral_projector_from_eigenvalues(
    mixed_order_parameter: sp.MatrixBase | Sequence[Sequence[object]],
    selected_eigenvalue: object,
    eigenvalues: Iterable[object],
) -> sp.ImmutableMatrix:
    """Return the simple-eigenvalue spectral idempotent by Lagrange product.

    ``eigenvalues`` are the local eigenvalue branches of ``X``, not frozen
    vacuum constants.  The caller is responsible for staying on a branch with
    a real, distinct selected eigenvalue.  Supplying fixed target eigenvalues
    away from the corresponding isospectral surface would not define a
    projector and is deliberately rejected by downstream premise checks.
    """

    mixed = _square_matrix(mixed_order_parameter, "mixed_order_parameter")
    spectrum = tuple(sp.sympify(value) for value in eigenvalues)
    selected = sp.sympify(selected_eigenvalue)
    if len(spectrum) != mixed.rows:
        raise ValueError("one local eigenvalue is required per matrix dimension")
    matching = [
        index
        for index, value in enumerate(spectrum)
        if sp.simplify(value - selected) == 0
    ]
    if len(matching) != 1:
        raise ValueError("selected_eigenvalue must occur exactly once")
    if any(
        sp.simplify(eigenvalue - selected) == 0
        for index, eigenvalue in enumerate(spectrum)
        if index != matching[0]
    ):
        raise ValueError("the selected spectral eigenvalue must be simple")

    projector = sp.eye(mixed.rows)
    for eigenvalue in spectrum:
        if sp.simplify(eigenvalue - selected) == 0:
            continue
        projector = (
            projector
            * (mixed - eigenvalue * sp.eye(mixed.rows))
            / (selected - eigenvalue)
        )
    return sp.ImmutableMatrix(projector.applyfunc(sp.factor))


def cartan_inverse_metric_from_projector(
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.ImmutableMatrix:
    """Return ``eta^{-1} - 2 P_t eta^{-1}`` for a timelike spectral projector."""

    projector = _square_matrix(timelike_projector, "timelike_projector")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    _validate_same_dimension(projector, metric)
    inverse_metric = metric.inv()
    return sp.ImmutableMatrix(
        (inverse_metric - 2 * projector * inverse_metric).applyfunc(sp.factor)
    )


def spectral_cartan_inverse_metric(
    order_parameter_covariant: sp.MatrixBase | Sequence[Sequence[object]],
    selected_eigenvalue: object,
    eigenvalues: Iterable[object],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.ImmutableMatrix:
    """Construct the local inverse Cartan metric from the selected M5 branch."""

    order_parameter = _square_matrix(
        order_parameter_covariant, "order_parameter_covariant"
    )
    metric = _square_matrix(metric_covariant, "metric_covariant")
    _validate_same_dimension(order_parameter, metric)
    if order_parameter != order_parameter.T:
        raise ValueError("the covariant M5 order parameter must be symmetric")
    mixed = metric.inv() * order_parameter
    projector = spectral_projector_from_eigenvalues(
        mixed, selected_eigenvalue, eigenvalues
    )
    return cartan_inverse_metric_from_projector(projector, metric)


def spectral_trace_potential(
    order_parameter_covariant: sp.MatrixBase | Sequence[Sequence[object]],
    target_eigenvalues: Iterable[object],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
    weights: Iterable[object] | None = None,
) -> sp.Expr:
    """Return the pinned M5 trace-power spectrum potential.

    For dimension ``n`` this is
    ``sum_{p=1}^n w_p (tr(X^p)-sum_i Lambda_i^p)^2`` with ``X=eta^-1 M``.
    """

    order_parameter = _square_matrix(
        order_parameter_covariant, "order_parameter_covariant"
    )
    metric = _square_matrix(metric_covariant, "metric_covariant")
    dimension = _validate_same_dimension(order_parameter, metric)
    targets = tuple(sp.sympify(value) for value in target_eigenvalues)
    if len(targets) != dimension:
        raise ValueError("one target eigenvalue is required per matrix dimension")
    potential_weights = (
        (sp.Integer(1),) * dimension
        if weights is None
        else tuple(sp.sympify(value) for value in weights)
    )
    if len(potential_weights) != dimension:
        raise ValueError("one trace-power weight is required per matrix dimension")

    mixed = metric.inv() * order_parameter
    return sp.factor(
        sum(
            potential_weights[power - 1]
            * (sp.trace(mixed**power) - sum(target**power for target in targets)) ** 2
            for power in range(1, dimension + 1)
        )
    )


def m5_ldg_coefficients(beta: object, scale: object) -> tuple[sp.Expr, ...]:
    """Return the source M5.17 ``(a,b,c,V_vac)`` coefficient tuple.

    The exact source relations are ``b=beta*c``,
    ``a=(3*b-4*c)/2``, and ``V_vac=a-b+c``.  Positivity and the physical
    vacuum claim require ``c>0`` and ``0<beta<2``; those inequalities are
    hypotheses on the caller's parameter domain rather than numerical clamps.
    """

    beta_value = sp.sympify(beta)
    c_value = sp.sympify(scale)
    b_value = beta_value * c_value
    a_value = sp.Rational(1, 2) * (3 * b_value - 4 * c_value)
    vacuum_value = a_value - b_value + c_value
    return tuple(map(sp.factor, (a_value, b_value, c_value, vacuum_value)))


def projected_spatial_ldg_potential(
    order_parameter_covariant: sp.MatrixBase | Sequence[Sequence[object]],
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    beta: object,
    scale: object,
    timelike_target_eigenvalue: object,
    timelike_stiffness: object,
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Lift the complete M5.17 spatial potential to the timelike branch.

    For ``X=eta^{-1} M``, its rank-one timelike spectral idempotent ``P_t``,
    ``Q=I-P_t``, and ``Y=Q X Q``, this returns

    ``a Tr(Y^2)-b Tr(Y^3)+c Tr(Y^2)^2-V_vac``
    ``+w_t(Tr(P_t X)-g)^2``.

    Every trace is invariant under the simultaneous Lorentz similarity of
    ``X`` and ``P_t``.  In the rest frame with a uniform time row, ``Y`` is
    exactly the embedded spatial block, so the first line is the complete
    off-shell M5.17 Landau-de Gennes potential without a coefficient change.
    The last term pins the selected time eigenvalue and is identically zero
    throughout that spatial sector.
    """

    order_parameter = _square_matrix(
        order_parameter_covariant, "order_parameter_covariant"
    )
    projector = _square_matrix(timelike_projector, "timelike_projector")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    dimension = _validate_same_dimension(order_parameter, projector, metric)
    if order_parameter != order_parameter.T:
        raise ValueError("the covariant M5 order parameter must be symmetric")
    if metric.det() == 0:
        raise ValueError("metric_covariant must be invertible")

    mixed = metric.inv() * order_parameter
    projector_defect = (projector**2 - projector).applyfunc(sp.simplify)
    if projector_defect != sp.zeros(dimension):
        raise ValueError("timelike_projector must be idempotent")
    if sp.simplify(sp.trace(projector) - 1) != 0:
        raise ValueError("timelike_projector must have rank one")
    commutator = (projector * mixed - mixed * projector).applyfunc(sp.simplify)
    if commutator != sp.zeros(dimension):
        raise ValueError("timelike_projector must be spectral for eta^-1 M")

    complement = sp.eye(dimension) - projector
    spatial_mixed = complement * mixed * complement
    trace_two = sp.trace(spatial_mixed**2)
    trace_three = sp.trace(spatial_mixed**3)
    a_value, b_value, c_value, vacuum_value = m5_ldg_coefficients(beta, scale)
    time_eigenvalue = sp.trace(projector * mixed)
    return sp.factor(
        a_value * trace_two
        - b_value * trace_three
        + c_value * trace_two**2
        - vacuum_value
        + sp.sympify(timelike_stiffness)
        * (time_eigenvalue - sp.sympify(timelike_target_eigenvalue)) ** 2
    )


def timelike_spectral_scalar(
    order_parameter_covariant: sp.MatrixBase | Sequence[Sequence[object]],
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the selected mixed-tensor eigenvalue ``tau=Tr(P_t eta^-1 M)``."""

    order_parameter = _square_matrix(
        order_parameter_covariant, "order_parameter_covariant"
    )
    projector = _square_matrix(timelike_projector, "timelike_projector")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    _validate_same_dimension(order_parameter, projector, metric)
    if metric.det() == 0:
        raise ValueError("metric_covariant must be invertible")
    return sp.factor(sp.trace(projector * metric.inv() * order_parameter))


def exponential_matter_factor(
    timelike_scalar: object,
    vacuum_value: object,
    coupling: object,
) -> sp.Expr:
    """Return the everywhere-positive Candidate-H factor ``exp(2 alpha(tau-g))``."""

    return sp.exp(
        2
        * sp.sympify(coupling)
        * (sp.sympify(timelike_scalar) - sp.sympify(vacuum_value))
    )


def spectral_clock_branch_guard(
    director_eigenvalue: object,
    tangent_eigenvalues: Sequence[object],
    strength: object,
) -> sp.Expr:
    """Return the positive Candidate-I guard on a simple clock branch.

    The term
    ``zeta*(lambda_theta-lambda_phi)^4 /``
    ``((lambda_n-lambda_theta)^2*(lambda_n-lambda_phi)^2)``
    is defined on the open branch where the selected director eigenvalue is
    distinct from both tangent eigenvalues.  It is exactly zero on every
    tangent-degenerate uniaxial M5.17 field, but diverges if a clock-active
    tangent splitting tries to exchange the selected director branch.
    """

    tangent = tuple(sp.sympify(value) for value in tangent_eigenvalues)
    if len(tangent) != 2:
        raise ValueError("exactly two tangent eigenvalues are required")
    director = sp.sympify(director_eigenvalue)
    tangent_left, tangent_right = tangent
    return sp.factor(
        sp.sympify(strength)
        * (tangent_left - tangent_right) ** 4
        / ((director - tangent_left) ** 2 * (director - tangent_right) ** 2)
    )


def spacelike_projector_from_vector(
    vector: Sequence[object] | sp.MatrixBase,
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.ImmutableMatrix:
    """Return the mixed projector ``P_N=N (N^T eta)``.

    It is idempotent when ``N^T eta N=1`` and transforms by similarity under
    Lorentz transformations.  Candidate J treats ``N`` as a constrained
    auxiliary clock-axis field, not as a new fitted source.
    """

    column = sp.Matrix(vector)
    if column.cols != 1:
        raise ValueError("vector must be a column")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    if column.rows != metric.rows:
        raise ValueError("vector and metric dimensions must match")
    return sp.ImmutableMatrix((column * column.T * metric).applyfunc(sp.factor))


def clock_axis_constraint_residuals(
    vector: Sequence[object] | sp.MatrixBase,
    timelike_projector: sp.MatrixBase | Sequence[Sequence[object]],
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
    metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> tuple[sp.Expr, sp.ImmutableMatrix, sp.ImmutableMatrix, sp.ImmutableMatrix]:
    """Return Candidate-J norm, orthogonality, idempotence, and alignment residuals."""

    column = sp.Matrix(vector)
    projector_t = _square_matrix(timelike_projector, "timelike_projector")
    spatial_mixed = _square_matrix(projected_spatial_mixed, "projected_spatial_mixed")
    metric = _square_matrix(metric_covariant, "metric_covariant")
    dimension = _validate_same_dimension(projector_t, spatial_mixed, metric)
    if column.shape != (dimension, 1):
        raise ValueError("vector dimension must match the projectors")
    projector_n = sp.Matrix(spacelike_projector_from_vector(column, metric))
    norm = sp.factor((column.T * metric * column)[0] - 1)
    orthogonality = sp.ImmutableMatrix((projector_t * column).applyfunc(sp.factor))
    idempotence = sp.ImmutableMatrix(
        (projector_n**2 - projector_n).applyfunc(sp.factor)
    )
    alignment = sp.ImmutableMatrix(
        (spatial_mixed * projector_n - projector_n * spatial_mixed).applyfunc(sp.factor)
    )
    return norm, orthogonality, idempotence, alignment


def auxiliary_clock_constraint_density(
    norm_residual: object,
    orthogonality_residual: Sequence[object] | sp.MatrixBase,
    alignment_residual: sp.MatrixBase | Sequence[Sequence[object]],
    norm_multiplier: object,
    orthogonality_multiplier_covariant: Sequence[object] | sp.MatrixBase,
    alignment_multiplier_mixed: sp.MatrixBase | Sequence[Sequence[object]],
) -> sp.Expr:
    """Contract Candidate-J constraint residuals with their local multipliers."""

    orthogonality = sp.Matrix(orthogonality_residual)
    orthogonality_multiplier = sp.Matrix(orthogonality_multiplier_covariant)
    alignment = _square_matrix(alignment_residual, "alignment_residual")
    alignment_multiplier = _square_matrix(
        alignment_multiplier_mixed, "alignment_multiplier_mixed"
    )
    if orthogonality.cols != 1 or orthogonality_multiplier.cols != 1:
        raise ValueError("orthogonality residual and multiplier must be columns")
    _validate_same_dimension(alignment, alignment_multiplier)
    if orthogonality.rows != alignment.rows:
        raise ValueError("all constraint dimensions must match")
    return sp.factor(
        sp.sympify(norm_multiplier) * sp.sympify(norm_residual)
        + (orthogonality_multiplier.T * orthogonality)[0]
        + sp.trace(alignment_multiplier * alignment)
    )


def auxiliary_clock_axis_lock_potential(
    projected_spatial_mixed: sp.MatrixBase | Sequence[Sequence[object]],
    clock_axis_projector: sp.MatrixBase | Sequence[Sequence[object]],
    strength: object,
) -> sp.Expr:
    """Return ``zeta*(Tr(Y^2)-Tr(P_N Y)^2)`` for Candidate K.

    Nonnegativity is claimed on the Candidate-J constraint surface where
    ``P_N`` is a rank-one spacelike eigenprojector of ``Y``.  There it equals
    ``zeta`` times the sum of squares of the two tangent eigenvalues.
    """

    spatial_mixed = _square_matrix(projected_spatial_mixed, "projected_spatial_mixed")
    projector = _square_matrix(clock_axis_projector, "clock_axis_projector")
    _validate_same_dimension(spatial_mixed, projector)
    selected_eigenvalue = sp.trace(projector * spatial_mixed)
    return sp.factor(
        sp.sympify(strength) * (sp.trace(spatial_mixed**2) - selected_eigenvalue**2)
    )


def scalar_current_lagrangian_density(
    scalar_derivatives: Sequence[object],
    stiffness: object,
    spacetime_metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return ``-kappa/2 eta^munu partial_mu tau partial_nu tau``."""

    metric = _square_matrix(spacetime_metric_covariant, "spacetime_metric_covariant")
    derivatives = tuple(sp.sympify(value) for value in scalar_derivatives)
    if len(derivatives) != metric.rows:
        raise ValueError("one scalar derivative is required per spacetime index")
    inverse_metric = metric.inv()
    return sp.factor(
        -sp.sympify(stiffness)
        * sum(
            inverse_metric[mu, nu] * derivatives[mu] * derivatives[nu]
            for mu, nu in product(range(metric.rows), repeat=2)
        )
        / 2
    )


def scalar_current_hamiltonian_density(
    scalar_derivatives: Sequence[object], stiffness: object
) -> sp.Expr:
    """Return the positive inertial-frame scalar-current Hamiltonian."""

    derivatives = tuple(sp.sympify(value) for value in scalar_derivatives)
    if not derivatives:
        raise ValueError("scalar_derivatives must not be empty")
    return sp.factor(sp.sympify(stiffness) * sum(value**2 for value in derivatives) / 2)


def dilaton_coupled_lagrangian_density(
    matter_lagrangian_density: object,
    timelike_scalar: object,
    vacuum_value: object,
    coupling: object,
    scalar_derivatives: Sequence[object],
    scalar_stiffness: object,
    spacetime_metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Compose the Candidate-H matter factor and timelike scalar current."""

    return sp.factor(
        exponential_matter_factor(timelike_scalar, vacuum_value, coupling)
        * sp.sympify(matter_lagrangian_density)
        + scalar_current_lagrangian_density(
            scalar_derivatives, scalar_stiffness, spacetime_metric_covariant
        )
    )


def dilaton_coupled_hamiltonian_density(
    matter_hamiltonian_density: object,
    timelike_scalar: object,
    vacuum_value: object,
    coupling: object,
    scalar_derivatives: Sequence[object],
    scalar_stiffness: object,
) -> sp.Expr:
    """Return the positive Candidate-H inertial-frame Hamiltonian density."""

    return sp.factor(
        exponential_matter_factor(timelike_scalar, vacuum_value, coupling)
        * sp.sympify(matter_hamiltonian_density)
        + scalar_current_hamiltonian_density(scalar_derivatives, scalar_stiffness)
    )


def spectral_cartan_curvature_scalar(
    curvature: sp.NDimArray,
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    spacetime_metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the P239 curvature scalar using eta externally and h internally."""

    spacetime_metric = _square_matrix(
        spacetime_metric_covariant, "spacetime_metric_covariant"
    )
    return double_two_form_contraction(
        curvature, spacetime_metric.inv(), internal_inverse_metric
    )


def spectral_cartan_lagrangian_density(
    curvature: sp.NDimArray,
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    spectrum_potential: object = 0,
    spacetime_metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the P239 density in the pinned unordered-spacetime-pair normalization.

    ``double_two_form_contraction`` sums both orders of the antisymmetric
    spacetime pair.  The factor one half therefore reproduces the source
    ``sum_{mu<nu}`` convention without changing the established 3x3
    coefficient.
    """

    return sp.factor(
        -sp.Rational(1, 2)
        * spectral_cartan_curvature_scalar(
            curvature, internal_inverse_metric, spacetime_metric_covariant
        )
        - sp.sympify(spectrum_potential)
    )


def spectral_cartan_hamiltonian_density(
    curvature: sp.NDimArray,
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    spectrum_potential: object = 0,
) -> sp.Expr:
    """Return the Legendre energy ``sum_{mu<nu}<F_munu,F_munu>_h + V``.

    The action's Cartan metric depends algebraically on ``M`` but not on its
    derivatives.  Consequently the time-space part remains homogeneous and
    quadratic in ``partial_0 M``; Euler's identity gives this Hamiltonian just
    as in the pinned M5.18 Legendre derivation.  Positivity is conditional on
    a positive-definite supplied internal Cartan metric and nonnegative
    potential.
    """

    dimension = _square_matrix(internal_inverse_metric, "internal_inverse_metric").rows
    return sp.factor(
        sp.Rational(1, 2)
        * double_two_form_contraction(
            curvature, sp.eye(dimension), internal_inverse_metric
        )
        + sp.sympify(spectrum_potential)
    )


def projector_current_bilinear(
    left_projector_derivative: sp.MatrixBase | Sequence[Sequence[object]],
    right_projector_derivative: sp.MatrixBase | Sequence[Sequence[object]],
) -> sp.Expr:
    """Return the positive target metric ``-tr(dP_left dP_right)/2``.

    On the rank-one timelike branch, write
    ``P_t=-u (eta u)^T`` with ``eta(u,u)=-1``.  Then this bilinear equals
    ``eta(du_left,du_right)``.  It is positive on a nonzero tangent vector
    and similarity-invariant under internal Lorentz transformations.
    """

    left = _square_matrix(left_projector_derivative, "left_projector_derivative")
    right = _square_matrix(right_projector_derivative, "right_projector_derivative")
    _validate_same_dimension(left, right)
    return sp.factor(-sp.trace(left * right) / 2)


def projector_sigma_lagrangian_density(
    projector_derivatives: Sequence[sp.MatrixBase | Sequence[Sequence[object]]],
    stiffness: object,
    spacetime_metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Return the minimal two-derivative timelike-projector density.

    ``L_P=-kappa eta^(mu nu) q(d_mu P,d_nu P)``.  The term vanishes for
    every time-row-uniform M5.17 field because its timelike projector is
    constant, while it supplies the boost sector's linearized massless
    operator.  ``stiffness`` must be positive for the Hamiltonian claim.
    """

    metric = _square_matrix(spacetime_metric_covariant, "spacetime_metric_covariant")
    derivatives = tuple(
        _square_matrix(derivative, f"projector_derivatives[{index}]")
        for index, derivative in enumerate(projector_derivatives)
    )
    dimension = _validate_same_dimension(metric, *derivatives)
    if len(derivatives) != dimension:
        raise ValueError("one projector derivative is required per spacetime index")
    inverse_metric = metric.inv()
    return sp.factor(
        -sp.sympify(stiffness)
        * sum(
            inverse_metric[mu, nu]
            * projector_current_bilinear(derivatives[mu], derivatives[nu])
            for mu, nu in product(range(dimension), repeat=2)
        )
    )


def projector_sigma_hamiltonian_density(
    projector_derivatives: Sequence[sp.MatrixBase | Sequence[Sequence[object]]],
    stiffness: object,
) -> sp.Expr:
    """Return ``kappa sum_mu q(d_mu P,d_mu P)`` in an inertial frame."""

    derivatives = tuple(
        _square_matrix(derivative, f"projector_derivatives[{index}]")
        for index, derivative in enumerate(projector_derivatives)
    )
    _validate_same_dimension(*derivatives)
    return sp.factor(
        sp.sympify(stiffness)
        * sum(
            projector_current_bilinear(derivative, derivative)
            for derivative in derivatives
        )
    )


def completed_m5_lagrangian_density(
    curvature: sp.NDimArray,
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    projector_derivatives: Sequence[sp.MatrixBase | Sequence[Sequence[object]]],
    projector_stiffness: object,
    spectrum_potential: object = 0,
    spacetime_metric_covariant: (
        sp.MatrixBase | Sequence[Sequence[object]]
    ) = MINKOWSKI_MOSTLY_PLUS,
) -> sp.Expr:
    """Compose the spectral-Cartan curvature and projector-current terms."""

    return sp.factor(
        spectral_cartan_lagrangian_density(
            curvature,
            internal_inverse_metric,
            spectrum_potential,
            spacetime_metric_covariant,
        )
        + projector_sigma_lagrangian_density(
            projector_derivatives,
            projector_stiffness,
            spacetime_metric_covariant,
        )
    )


def completed_m5_hamiltonian_density(
    curvature: sp.NDimArray,
    internal_inverse_metric: sp.MatrixBase | Sequence[Sequence[object]],
    projector_derivatives: Sequence[sp.MatrixBase | Sequence[Sequence[object]]],
    projector_stiffness: object,
    spectrum_potential: object = 0,
) -> sp.Expr:
    """Compose the nonnegative curvature, projector, and spectrum energies."""

    return sp.factor(
        spectral_cartan_hamiltonian_density(
            curvature, internal_inverse_metric, spectrum_potential
        )
        + projector_sigma_hamiltonian_density(
            projector_derivatives, projector_stiffness
        )
    )
