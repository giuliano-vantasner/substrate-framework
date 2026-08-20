"""Focused P240 tests for the issue-146 kinetic-axis candidate."""

from itertools import product

import sympy as sp

from substrate_framework.m5_kinetic_axis import (
    alternating_sextic_lagrangian_density,
    alternating_three_current,
    axis_pontryagin_pseudoscalar,
    axis_weighted_pontryagin_lagrangian_density,
    fixed_j_derrick_energy,
    kinetic_axis_comoving_hamiltonian_density,
    kinetic_axis_lagrangian_density,
    spatial_curvature_hamiltonian_density,
    spatial_curvature_lagrangian_density,
    spatial_covariant_metric_from_timelike_projector,
    spatial_inverse_metric_from_timelike_projector,
    timelike_skyrme_lagrangian_density,
)
from substrate_framework.m5_covariant_action import (
    double_two_form_contraction,
    m5_curvature_from_derivatives,
)


ETA = sp.diag(-1, 1, 1, 1)
P_T = sp.diag(1, 0, 0, 0)
P_N = sp.diag(0, 1, 0, 0)
ZERO = sp.zeros(4)


def _generator(left: int, right: int) -> sp.Matrix:
    result = sp.zeros(4)
    result[left, right] = -1
    result[right, left] = 1
    return result


def _symmetric_current_preimage(
    spatial: sp.Matrix, current: sp.Matrix
) -> sp.Matrix:
    result = sp.zeros(4)
    for left in range(4):
        for right in range(left + 1, 4):
            if current[left, right] != 0:
                result[left, right] = result[right, left] = (
                    current[left, right]
                    / (spatial[left, left] - spatial[right, right])
                )
    return result


def test_l1_is_static_3x3_null_and_has_positive_physical_clock_inertia():
    n, tangent_left, tangent_right = sp.symbols(
        "n tangent_left tangent_right", real=True
    )
    kappa = sp.symbols("kappa", positive=True)
    spatial = sp.diag(0, n, tangent_left, tangent_right)
    clock = _generator(2, 3) * spatial - spatial * _generator(2, 3)
    derivatives = (clock, ZERO, ZERO, ZERO)
    expected = kappa * n**2 * (tangent_left - tangent_right) ** 2
    assert sp.simplify(
        kinetic_axis_lagrangian_density(
            P_T, P_N, spatial, derivatives, kappa
        )
        - expected
    ) == 0
    assert sp.simplify(
        kinetic_axis_comoving_hamiltonian_density(
            P_T, P_N, spatial, clock, kappa
        )
        - expected
    ) == 0
    arbitrary_spatial_derivatives = tuple(
        sp.diag(0, index + 1, 2 * index + 1, 3 * index + 1)
        for index in range(3)
    )
    assert (
        kinetic_axis_lagrangian_density(
            P_T,
            P_N,
            spatial,
            (ZERO, *arbitrary_spatial_derivatives),
            kappa,
        )
        == 0
    )


def test_l1_is_lorentz_covariant_with_the_derivative_covector():
    kappa = sp.symbols("kappa", positive=True)
    spatial = sp.diag(0, 2, sp.Rational(1, 3), -sp.Rational(1, 4))
    derivative = _generator(2, 3) * spatial - spatial * _generator(2, 3)
    derivatives = (derivative, ZERO, ZERO, ZERO)
    baseline = kinetic_axis_lagrangian_density(
        P_T, P_N, spatial, derivatives, kappa
    )
    transformation = sp.eye(4)
    transformation[0, 0] = transformation[1, 1] = sp.Rational(5, 3)
    transformation[0, 1] = transformation[1, 0] = sp.Rational(4, 3)
    assert transformation.T * ETA * transformation == ETA
    inverse = transformation.inv()
    transformed_derivatives = tuple(
        sp.simplify(
            sum(
                (
                    inverse[rho, mu]
                    * transformation
                    * derivatives[rho]
                    * inverse
                    for rho in range(4)
                ),
                ZERO,
            )
        )
        for mu in range(4)
    )
    transformed = kinetic_axis_lagrangian_density(
        transformation * P_T * inverse,
        transformation * P_N * inverse,
        transformation * spatial * inverse,
        transformed_derivatives,
        kappa,
    )
    assert sp.simplify(transformed - baseline) == 0


def test_l1_beats_l2_quartic_on_the_wrong_axis_and_l2_needs_sextic_repair():
    kappa = sp.symbols("kappa", positive=True)
    spatial = sp.diag(0, 1, 0, 0)
    zero_axis = sp.diag(0, 0, 1, 0)
    derivative = _generator(1, 3) * spatial - spatial * _generator(1, 3)
    derivatives = (derivative, ZERO, ZERO, ZERO)
    assert kinetic_axis_lagrangian_density(
        P_T, zero_axis, spatial, derivatives, kappa
    ) == 0
    assert timelike_skyrme_lagrangian_density(
        P_T, spatial, derivatives, kappa
    ) == kappa
    assert timelike_skyrme_lagrangian_density(
        P_T, spatial, derivatives, kappa, axis_projector=zero_axis
    ) == 0


def test_skyrme_commutator_is_the_unique_positive_gap_trace_representative():
    eigenvalues = sp.symbols("lambda_1:4", real=True)
    z12, z13, z23 = sp.symbols("z12 z13 z23", real=True)
    spatial = sp.diag(*eigenvalues)
    derivative = sp.Matrix([[0, z12, z13], [z12, 0, z23], [z13, z23, 0]])
    current = spatial * derivative - derivative * spatial
    commutator_form = -sp.trace(current**2) / 2
    trace_form = sp.trace(spatial**2 * derivative**2) - sp.trace(
        spatial * derivative * spatial * derivative
    )
    gap_form = sum(
        (eigenvalues[left] - eigenvalues[right]) ** 2
        * derivative[left, right] ** 2
        for left in range(3)
        for right in range(left + 1, 3)
    )
    assert sp.simplify(commutator_form - trace_form) == 0
    assert sp.simplify(commutator_form - gap_form) == 0


def test_axis_weighted_skyrme_is_inequivalent_to_homogeneous_pontryagin():
    n, left, right, omega = sp.symbols(
        "n lambda_theta lambda_phi omega", real=True
    )
    kappa = sp.symbols("kappa", positive=True)
    spatial = sp.diag(0, n, left, right)
    clock = omega * (_generator(2, 3) * spatial - spatial * _generator(2, 3))
    derivatives = (clock, ZERO, ZERO, ZERO)
    skyrme = timelike_skyrme_lagrangian_density(
        P_T, spatial, derivatives, kappa, axis_projector=P_N
    )
    assert sp.simplify(
        skyrme - kappa * n**2 * omega**2 * (left - right) ** 4
    ) == 0
    curvature = m5_curvature_from_derivatives(derivatives)
    assert all(curvature[index] == 0 for index in product(range(4), repeat=4))
    assert axis_pontryagin_pseudoscalar(curvature, P_N, sp.eye(4)) == 0


def test_alternating_sextic_uses_the_dynamic_spatial_metric_off_rest_slice():
    rapidity, kappa = sp.symbols("rapidity kappa", real=True)
    spatial = sp.diag(0, 1, 2, 4)
    axis = sp.diag(0, 0, 0, 1)
    target_currents = (
        _generator(2, 3),
        _generator(3, 1),
        _generator(1, 2),
        ZERO,
    )
    derivatives = tuple(
        _symmetric_current_preimage(spatial, current)
        for current in target_currents
    )
    assert tuple(
        spatial * derivative - derivative * spatial
        for derivative in derivatives
    ) == target_currents
    alternating = alternating_three_current(target_currents)
    assert alternating[:3, 0] == sp.zeros(3, 1)
    assert alternating[3] != 0
    baseline = alternating_sextic_lagrangian_density(
        P_T, axis, spatial, derivatives, kappa
    )

    boost = sp.eye(4)
    boost[0, 0] = boost[3, 3] = sp.cosh(rapidity)
    boost[0, 3] = boost[3, 0] = sp.sinh(rapidity)
    inverse = boost.inv()
    projector_t = inverse * P_T * boost
    transformed_axis = inverse * axis * boost
    transformed_spatial = inverse * spatial * boost
    transformed_derivatives = tuple(
        inverse * derivative * boost for derivative in derivatives
    )
    spatial_metric = spatial_covariant_metric_from_timelike_projector(projector_t)
    assert sp.simplify(spatial_metric - spatial_metric.T) == ZERO
    transformed = alternating_sextic_lagrangian_density(
        projector_t,
        transformed_axis,
        transformed_spatial,
        transformed_derivatives,
        kappa,
    )
    assert sp.simplify(transformed - baseline * sp.cosh(rapidity) ** 2) == 0
    assert sp.simplify(sp.diff(transformed, rapidity, 2).subs(rapidity, 0)) == (
        2 * baseline
    )
    assert sp.simplify(
        sp.trace(transformed_axis * transformed_spatial)
        - sp.trace(axis * spatial)
    ) == 0


def test_opposite_axis_conjugation_is_not_the_mixed_similarity():
    rapidity = sp.symbols("rapidity", real=True)
    spatial = sp.diag(0, 1, 2, 4)
    axis = sp.diag(0, 0, 0, 1)
    boost = sp.eye(4)
    boost[0, 0] = boost[3, 3] = sp.cosh(rapidity)
    boost[0, 3] = boost[3, 0] = sp.sinh(rapidity)
    inverse = boost.inv()
    transformed_spatial = inverse * spatial * boost
    correct_axis = inverse * axis * boost
    wrong_axis = boost * axis * inverse
    assert sp.simplify(
        sp.trace(correct_axis * transformed_spatial) - 4
    ) == 0
    assert sp.simplify(
        sp.trace(wrong_axis * transformed_spatial) - 4
    ) != 0


def test_l1_fixed_j_scale_ledger_has_a_finite_strict_minimum():
    radius = sp.symbols("R", positive=True)
    curvature, current, potential, inertia, momentum = sp.symbols(
        "A C B I_0 J", positive=True
    )
    energy = fixed_j_derrick_energy(
        radius, curvature, current, potential, inertia, momentum
    )
    assert sp.limit(energy, radius, 0, dir="+") == sp.oo
    assert sp.limit(energy, radius, sp.oo) == sp.oo
    assert sp.simplify(
        sp.diff(energy, radius, 2)
        - (
            2 * curvature / radius**3
            + 6 * potential * radius
            + 3 * momentum**2 / (inertia * radius**5)
        )
    ) == 0


def test_l1_replaces_the_axis_blind_time_curvature_channel():
    from itertools import combinations

    pairs = tuple(combinations(range(4), 2))

    def tensor_from_pairs(pair_matrix):
        tensor = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
        for row, (mu, nu) in enumerate(pairs):
            for column, (a, b) in enumerate(pairs):
                value = pair_matrix[row, column]
                tensor[mu, nu, a, b] = value
                tensor[nu, mu, a, b] = -value
                tensor[mu, nu, b, a] = -value
                tensor[nu, mu, b, a] = value
        return sp.ImmutableDenseNDimArray(tensor)

    assert spatial_inverse_metric_from_timelike_projector(P_T) == sp.diag(
        0, 1, 1, 1
    )
    spatial_pairs = sp.zeros(6)
    spatial_pairs[3, 3] = 2
    spatial_pairs[4, 5] = -1
    spatial_curvature = tensor_from_pairs(spatial_pairs)
    assert spatial_curvature_lagrangian_density(
        spatial_curvature, P_T, sp.eye(4)
    ) == -sp.Rational(1, 2) * double_two_form_contraction(
        spatial_curvature, ETA, sp.eye(4)
    )
    time_pairs = sp.zeros(6)
    time_pairs[0, 0] = 1
    time_curvature = tensor_from_pairs(time_pairs)
    assert spatial_curvature_hamiltonian_density(
        time_curvature, P_T, sp.eye(4)
    ) == 0


def test_l2_axis_pontryagin_square_is_the_healthy_static_null_route():
    from itertools import combinations

    pairs = tuple(combinations(range(4), 2))

    def tensor_from_pairs(pair_matrix):
        tensor = sp.MutableDenseNDimArray.zeros(4, 4, 4, 4)
        for row, (mu, nu) in enumerate(pairs):
            for column, (a, b) in enumerate(pairs):
                value = pair_matrix[row, column]
                tensor[mu, nu, a, b] = value
                tensor[nu, mu, a, b] = -value
                tensor[mu, nu, b, a] = -value
                tensor[nu, mu, b, a] = value
        return sp.ImmutableDenseNDimArray(tensor)

    static_pairs = sp.zeros(6)
    static_pairs[3, 4] = 2
    static_pairs[5, 3] = -1
    static_curvature = tensor_from_pairs(static_pairs)
    assert axis_pontryagin_pseudoscalar(
        static_curvature, P_N, sp.eye(4)
    ) == 0

    dynamic_pairs = static_pairs.copy()
    dynamic_pairs[0, 3] = 1
    dynamic_pairs[2, 5] = -2
    dynamic_curvature = tensor_from_pairs(dynamic_pairs)
    spatial = sp.diag(0, 1, sp.Rational(1, 3), 0)
    gamma = sp.symbols("gamma", positive=True)
    density = axis_weighted_pontryagin_lagrangian_density(
        dynamic_curvature, P_N, spatial, sp.eye(4), gamma
    )
    assert density.is_nonnegative is True
    zero_axis = sp.diag(0, 0, 0, 1)
    assert axis_weighted_pontryagin_lagrangian_density(
        dynamic_curvature, zero_axis, spatial, sp.eye(4), gamma
    ) == 0
