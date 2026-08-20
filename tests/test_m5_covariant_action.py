"""Exact regression and mutation tests for the conditional P239 action API."""

from __future__ import annotations

from itertools import combinations, product

import pytest
import sympy as sp

from substrate_framework.m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    cartan_inverse_metric_from_projector,
    clock_axis_constraint_residuals,
    completed_m5_hamiltonian_density,
    completed_m5_lagrangian_density,
    auxiliary_clock_constraint_density,
    auxiliary_clock_axis_lock_potential,
    double_two_form_contraction,
    dilaton_coupled_hamiltonian_density,
    dilaton_coupled_lagrangian_density,
    eta_commutator,
    exponential_matter_factor,
    m5_curvature_from_derivatives,
    m5_ldg_coefficients,
    projected_spatial_ldg_potential,
    projector_current_bilinear,
    projector_sigma_hamiltonian_density,
    projector_sigma_lagrangian_density,
    spectral_cartan_curvature_scalar,
    spectral_cartan_hamiltonian_density,
    spectral_cartan_inverse_metric,
    spectral_cartan_lagrangian_density,
    spectral_projector_from_eigenvalues,
    spectral_trace_potential,
    spacelike_projector_from_vector,
    scalar_current_hamiltonian_density,
    scalar_current_lagrangian_density,
    spectral_clock_branch_guard,
    timelike_spectral_scalar,
    wedge_inverse_metric,
)


PAIRS = tuple(combinations(range(4), 2))
ETA = sp.Matrix(MINKOWSKI_MOSTLY_PLUS)


def _rational_lorentz() -> sp.Matrix:
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = sp.Rational(5, 3)
    boost[0, 1] = boost[1, 0] = sp.Rational(4, 3)
    rotation = sp.eye(4)
    rotation[2, 2] = rotation[3, 3] = sp.Rational(3, 5)
    rotation[2, 3] = -sp.Rational(4, 5)
    rotation[3, 2] = sp.Rational(4, 5)
    return boost * rotation


def _pair_transform(covector_transform: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        6,
        6,
        lambda new, old: sp.expand(
            covector_transform[PAIRS[old][0], PAIRS[new][0]]
            * covector_transform[PAIRS[old][1], PAIRS[new][1]]
            - covector_transform[PAIRS[old][1], PAIRS[new][0]]
            * covector_transform[PAIRS[old][0], PAIRS[new][1]]
        ),
    )


def _tensor_from_pair_matrix(matrix: sp.Matrix) -> sp.ImmutableDenseNDimArray:
    tensor = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
    for row, (mu, nu) in enumerate(PAIRS):
        for column, (internal_a, internal_b) in enumerate(PAIRS):
            value = matrix[row, column]
            tensor[mu, nu, internal_a, internal_b] = value
            tensor[nu, mu, internal_a, internal_b] = -value
            tensor[mu, nu, internal_b, internal_a] = -value
            tensor[nu, mu, internal_b, internal_a] = value
    return sp.ImmutableDenseNDimArray(tensor)


def _transform_double_two_form(
    curvature: sp.NDimArray, transformation: sp.Matrix
) -> sp.ImmutableDenseNDimArray:
    covector = transformation.inv().T
    induced = _pair_transform(covector)
    matrix = sp.Matrix(
        6,
        6,
        lambda row, column: curvature[
            PAIRS[row][0], PAIRS[row][1], PAIRS[column][0], PAIRS[column][1]
        ],
    )
    return _tensor_from_pair_matrix(induced * matrix * induced.T)


def _source_derivatives() -> tuple[sp.Matrix, ...]:
    derivatives = []
    for mu in range(4):
        raw = sp.Matrix(
            4,
            4,
            lambda row, column: ((11 * mu + 7 * row - 3 * column) % 9) - 4,
        )
        derivatives.append(raw + raw.T)
    return tuple(derivatives)


def test_eta_commutator_and_curvature_have_only_source_symmetries() -> None:
    derivatives = _source_derivatives()
    curvature = m5_curvature_from_derivatives(derivatives)

    assert eta_commutator(derivatives[0], derivatives[1]) == sp.Matrix(
        curvature[0, 1, :, :]
    )
    assert all(
        curvature[mu, nu, internal_a, internal_b]
        == -curvature[nu, mu, internal_a, internal_b]
        for mu, nu, internal_a, internal_b in product(range(4), repeat=4)
    )
    assert all(
        curvature[mu, nu, internal_a, internal_b]
        == -curvature[mu, nu, internal_b, internal_a]
        for mu, nu, internal_a, internal_b in product(range(4), repeat=4)
    )
    assert any(
        curvature[mu, nu, internal_a, internal_b]
        != curvature[internal_a, internal_b, mu, nu]
        for mu, nu, internal_a, internal_b in product(range(4), repeat=4)
    )
    assert any(
        curvature[mu, nu, internal_a, internal_b]
        + curvature[nu, internal_a, mu, internal_b]
        + curvature[internal_a, mu, nu, internal_b]
        != 0
        for mu, nu, internal_a, internal_b in product(range(4), repeat=4)
    )

    nonsymmetric = list(derivatives)
    nonsymmetric[0] = sp.Matrix(nonsymmetric[0])
    nonsymmetric[0][0, 1] += 1
    with pytest.raises(ValueError, match="must be symmetric"):
        m5_curvature_from_derivatives(nonsymmetric)


def test_double_two_form_contraction_has_the_ordered_pair_normalization() -> None:
    pair_matrix = sp.zeros(6)
    pair_matrix[0, 1] = 3
    curvature = _tensor_from_pair_matrix(pair_matrix)
    euclidean = sp.eye(4)

    assert wedge_inverse_metric(euclidean) == sp.eye(6)
    assert double_two_form_contraction(curvature, euclidean, euclidean) == 36
    assert double_two_form_contraction(curvature, ETA, euclidean) == -36
    with pytest.raises(ValueError, match="shape"):
        double_two_form_contraction(
            sp.ImmutableDenseNDimArray.zeros(3, 3, 3, 3), ETA, euclidean
        )


def test_spectral_projector_and_cartan_metric_on_timelike_branch() -> None:
    eigenvalues = (sp.Integer(4), sp.Integer(1), sp.Rational(1, 3), sp.Integer(0))
    mixed_vacuum = sp.diag(*eigenvalues)
    order_parameter_vacuum = ETA * mixed_vacuum
    projector_vacuum = spectral_projector_from_eigenvalues(
        mixed_vacuum, eigenvalues[0], eigenvalues
    )

    assert projector_vacuum == sp.diag(1, 0, 0, 0)
    assert projector_vacuum**2 == projector_vacuum
    assert cartan_inverse_metric_from_projector(projector_vacuum) == sp.eye(4)
    assert spectral_cartan_inverse_metric(
        order_parameter_vacuum, eigenvalues[0], eigenvalues
    ) == sp.eye(4)

    transformation = _rational_lorentz()
    covector = transformation.inv().T
    transformed_order_parameter = covector * order_parameter_vacuum * covector.T
    transformed_mixed = ETA * transformed_order_parameter
    transformed_projector = spectral_projector_from_eigenvalues(
        transformed_mixed, eigenvalues[0], eigenvalues
    )
    expected_projector = transformation * projector_vacuum * transformation.inv()
    transformed_cartan = spectral_cartan_inverse_metric(
        transformed_order_parameter, eigenvalues[0], eigenvalues
    )

    assert sp.simplify(transformed_projector - expected_projector) == sp.zeros(4)
    assert transformed_projector**2 == transformed_projector
    assert sp.simplify(
        transformed_cartan - transformation * transformation.T
    ) == sp.zeros(4)
    assert all(
        determinant > 0
        for determinant in (
            transformed_cartan[:size, :size].det() for size in range(1, 5)
        )
    )

    repeated_spatial = spectral_projector_from_eigenvalues(
        sp.diag(4, 1, 1, 0), 4, (4, 1, 1, 0)
    )
    assert repeated_spatial == sp.diag(1, 0, 0, 0)

    with pytest.raises(ValueError, match="must occur exactly once"):
        spectral_projector_from_eigenvalues(
            sp.diag(4, 4, 1, 0), eigenvalues[0], (4, 4, 1, 0)
        )


def test_spectral_potential_and_cartan_action_are_exact_lorentz_scalars() -> None:
    transformation = _rational_lorentz()
    assert transformation.T * ETA * transformation == ETA
    covector = transformation.inv().T

    eigenvalues = (sp.Integer(4), sp.Integer(1), sp.Rational(1, 3), sp.Integer(0))
    order_parameter = ETA * sp.diag(5, 2, sp.Rational(1, 2), -1)
    transformed_order_parameter = covector * order_parameter * covector.T
    potential = spectral_trace_potential(order_parameter, eigenvalues)
    transformed_potential = spectral_trace_potential(
        transformed_order_parameter, eigenvalues
    )
    assert potential != 0
    assert sp.simplify(transformed_potential - potential) == 0

    vacuum = ETA * sp.diag(*eigenvalues)
    cartan = spectral_cartan_inverse_metric(vacuum, eigenvalues[0], eigenvalues)
    transformed_vacuum = covector * vacuum * covector.T
    transformed_cartan = spectral_cartan_inverse_metric(
        transformed_vacuum, eigenvalues[0], eigenvalues
    )
    pair_matrix = sp.Matrix(
        6,
        6,
        lambda row, column: ((5 * row - 2 * column + row * column) % 7) - 3,
    )
    curvature = _tensor_from_pair_matrix(pair_matrix)
    transformed_curvature = _transform_double_two_form(curvature, transformation)
    baseline = spectral_cartan_curvature_scalar(curvature, cartan)
    transformed = spectral_cartan_curvature_scalar(
        transformed_curvature, transformed_cartan
    )
    fixed_frobenius_mutation = spectral_cartan_curvature_scalar(
        transformed_curvature, sp.eye(4)
    )

    assert sp.simplify(transformed - baseline) == 0
    assert sp.simplify(fixed_frobenius_mutation - baseline) != 0


def test_projected_ldg_potential_is_covariant_and_exactly_m5_17_off_shell() -> None:
    beta, scale, g_value, time_stiffness = sp.symbols("beta scale g w_t", real=True)
    x, y, z, u, v, w = sp.symbols("x y z u v w", real=True)
    spatial = sp.Matrix([[x, u, v], [u, y, w], [v, w, z]])
    order_parameter = sp.diag(-g_value, 0, 0, 0)
    order_parameter[1:4, 1:4] = spatial
    projector = sp.diag(1, 0, 0, 0)

    a_value, b_value, c_value, vacuum_value = m5_ldg_coefficients(beta, scale)
    expected = sp.factor(
        a_value * sp.trace(spatial**2)
        - b_value * sp.trace(spatial**3)
        + c_value * sp.trace(spatial**2) ** 2
        - vacuum_value
    )
    potential = projected_spatial_ldg_potential(
        order_parameter,
        projector,
        beta,
        scale,
        g_value,
        time_stiffness,
    )
    assert sp.simplify(potential - expected) == 0

    transformation = _rational_lorentz()
    covector = transformation.inv().T
    transformed_order_parameter = covector * order_parameter * covector.T
    transformed_projector = transformation * projector * transformation.inv()
    transformed_potential = projected_spatial_ldg_potential(
        transformed_order_parameter,
        transformed_projector,
        beta,
        scale,
        g_value,
        time_stiffness,
    )
    assert sp.simplify(transformed_potential - potential) == 0

    vacuum = sp.diag(-g_value, 1, 0, 0)
    assert (
        projected_spatial_ldg_potential(
            vacuum,
            projector,
            beta,
            scale,
            g_value,
            time_stiffness,
        )
        == 0
    )
    assert sp.factor(
        projected_spatial_ldg_potential(
            sp.diag(-g_value, 0, 0, 0),
            projector,
            beta,
            scale,
            g_value,
            time_stiffness,
        )
    ) == sp.factor(scale * (1 - beta / 2))

    with pytest.raises(ValueError, match="must be spectral"):
        projected_spatial_ldg_potential(
            transformed_order_parameter,
            projector,
            beta,
            scale,
            g_value,
            time_stiffness,
        )


def test_timelike_dilaton_is_covariant_positive_and_exact_on_spatial_sector() -> None:
    g_value, alpha, kappa = sp.symbols("g alpha kappa", positive=True)
    projector = sp.diag(1, 0, 0, 0)
    spatial = sp.Matrix([[2, 1, 0], [1, -1, 1], [0, 1, 3]])
    order_parameter = sp.diag(-g_value, 0, 0, 0)
    order_parameter[1:4, 1:4] = spatial
    tau = timelike_spectral_scalar(order_parameter, projector)
    assert tau == g_value
    assert exponential_matter_factor(tau, g_value, alpha) == 1

    transformation = _rational_lorentz()
    inverse = transformation.inv()
    covector = inverse.T
    transformed_order_parameter = covector * order_parameter * covector.T
    transformed_projector = transformation * projector * inverse
    assert (
        sp.simplify(
            timelike_spectral_scalar(transformed_order_parameter, transformed_projector)
            - tau
        )
        == 0
    )

    derivatives = sp.Matrix([2, 3, -1, 4])
    transformed_derivatives = inverse.T * derivatives
    assert (
        sp.simplify(
            scalar_current_lagrangian_density(tuple(transformed_derivatives), kappa)
            - scalar_current_lagrangian_density(tuple(derivatives), kappa)
        )
        == 0
    )
    assert scalar_current_hamiltonian_density(tuple(derivatives), kappa) == 15 * kappa

    matter_lagrangian, matter_hamiltonian = sp.symbols("L_G H_G")
    zeros = (0, 0, 0, 0)
    assert (
        dilaton_coupled_lagrangian_density(
            matter_lagrangian, tau, g_value, alpha, zeros, kappa
        )
        == matter_lagrangian
    )
    assert (
        dilaton_coupled_hamiltonian_density(
            matter_hamiltonian, tau, g_value, alpha, zeros, kappa
        )
        == matter_hamiltonian
    )


def test_clock_branch_guard_preserves_uniaxial_sector_and_blocks_exchange() -> None:
    director, left, right, strength, epsilon = sp.symbols(
        "lambda_n lambda_theta lambda_phi zeta epsilon", positive=True
    )
    guard = spectral_clock_branch_guard(director, (left, right), strength)
    assert guard == spectral_clock_branch_guard(director, (right, left), strength)
    assert spectral_clock_branch_guard(director, (left, left), strength) == 0
    assert spectral_clock_branch_guard(1, (0, 0), strength) == 0
    assert (
        sp.limit(
            spectral_clock_branch_guard(1 + epsilon, (1, 0), strength),
            epsilon,
            0,
            dir="+",
        )
        == sp.oo
    )
    with pytest.raises(ValueError, match="exactly two"):
        spectral_clock_branch_guard(director, (left,), strength)


def test_auxiliary_clock_axis_constraints_are_exact_on_uniaxial_and_melt() -> None:
    vector = sp.Matrix([0, 1, 0, 0])
    timelike = sp.diag(1, 0, 0, 0)
    spatial = sp.diag(0, 1, 0, 0)
    projector = spacelike_projector_from_vector(vector)
    assert projector == sp.diag(0, 1, 0, 0)
    norm, orthogonality, idempotence, alignment = clock_axis_constraint_residuals(
        vector, timelike, spatial
    )
    assert norm == 0
    assert orthogonality == sp.zeros(4, 1)
    assert idempotence == sp.zeros(4)
    assert alignment == sp.zeros(4)
    assert (
        auxiliary_clock_constraint_density(
            norm,
            orthogonality,
            alignment,
            2,
            sp.Matrix([1, 2, 3, 4]),
            sp.eye(4),
        )
        == 0
    )

    isotropic_spatial = sp.diag(0, 3, 3, 3)
    alternate_vector = sp.Matrix([0, 0, sp.Rational(3, 5), sp.Rational(4, 5)])
    assert clock_axis_constraint_residuals(
        alternate_vector, timelike, isotropic_spatial
    )[-1] == sp.zeros(4)


def test_auxiliary_axis_lock_selects_aligned_uniaxial_clock_axis() -> None:
    director, left, right, strength = sp.symbols(
        "lambda_n lambda_theta lambda_phi zeta", real=True
    )
    spatial = sp.diag(0, director, left, right)
    aligned = sp.diag(0, 1, 0, 0)
    assert auxiliary_clock_axis_lock_potential(
        spatial, aligned, strength
    ) == strength * (left**2 + right**2)
    amplitude = sp.symbols("s", real=True)
    assert (
        auxiliary_clock_axis_lock_potential(
            sp.diag(0, amplitude, 0, 0), aligned, strength
        )
        == 0
    )
    permuted = sp.diag(0, 0, 1, 0)
    assert auxiliary_clock_axis_lock_potential(permuted, aligned, strength) == strength


def test_spatial_3x3_action_is_recovered_without_coefficient_change() -> None:
    pair_matrix = sp.zeros(6)
    spatial_pair_indices = (3, 4, 5)
    for row, column in product(spatial_pair_indices, repeat=2):
        pair_matrix[row, column] = row + 2 * column - 7
    curvature = _tensor_from_pair_matrix(pair_matrix)

    cartan_value = spectral_cartan_curvature_scalar(curvature, sp.eye(4))
    source_eta_value = double_two_form_contraction(curvature, ETA, ETA)
    assert cartan_value == source_eta_value

    mutated = sp.diag(1, 1, 1, 2)
    assert spectral_cartan_curvature_scalar(curvature, mutated) != source_eta_value


def test_source_clock_boost_channel_changes_from_negative_to_positive() -> None:
    omega = sp.symbols("omega", real=True)
    velocity = sp.diag(omega, 0, 0, 0)
    spatial_gradient = sp.zeros(4)
    spatial_gradient[0, 1] = spatial_gradient[1, 0] = 1
    zero = sp.zeros(4)
    derivatives = (velocity, spatial_gradient, zero, zero)
    curvature = m5_curvature_from_derivatives(derivatives)

    baseline_lagrangian = -sp.Rational(1, 2) * double_two_form_contraction(
        curvature, ETA, ETA
    )
    cartan_lagrangian = spectral_cartan_lagrangian_density(curvature, sp.eye(4))
    baseline_coefficient = sp.expand(baseline_lagrangian).coeff(omega, 2)
    cartan_coefficient = sp.expand(cartan_lagrangian).coeff(omega, 2)

    assert baseline_coefficient < 0
    assert cartan_coefficient > 0
    assert sp.simplify(cartan_coefficient + baseline_coefficient) == 0
    hamiltonian_coefficient = sp.expand(
        spectral_cartan_hamiltonian_density(curvature, sp.eye(4))
    ).coeff(omega, 2)
    assert hamiltonian_coefficient > 0


def test_projector_current_is_positive_covariant_and_spatially_inactive() -> None:
    boost_tangent = sp.zeros(4)
    boost_tangent[0, 1] = -1
    boost_tangent[1, 0] = 1
    zero = sp.zeros(4)
    derivatives = (2 * boost_tangent, 3 * boost_tangent, zero, zero)
    stiffness = sp.Integer(5)

    assert projector_current_bilinear(boost_tangent, boost_tangent) == 1
    assert projector_sigma_lagrangian_density(derivatives, stiffness) == -25
    assert projector_sigma_hamiltonian_density(derivatives, stiffness) == 65

    transformation = _rational_lorentz()
    inverse = transformation.inv()
    transformed_derivatives = tuple(
        sum(
            (
                inverse[source, target] * transformation * derivatives[source] * inverse
                for source in range(4)
            ),
            sp.zeros(4),
        )
        for target in range(4)
    )
    assert (
        sp.simplify(
            projector_sigma_lagrangian_density(transformed_derivatives, stiffness)
            - projector_sigma_lagrangian_density(derivatives, stiffness)
        )
        == 0
    )

    curvature = sp.ImmutableDenseNDimArray.zeros(4, 4, 4, 4)
    assert completed_m5_lagrangian_density(
        curvature, sp.eye(4), (zero, zero, zero, zero), stiffness
    ) == spectral_cartan_lagrangian_density(curvature, sp.eye(4))
    assert completed_m5_hamiltonian_density(
        curvature, sp.eye(4), derivatives, stiffness
    ) == projector_sigma_hamiltonian_density(derivatives, stiffness)
