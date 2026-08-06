from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.hls_reduction import (
    conditional_hls_ksrf_matching,
    conditional_vector_current_sextic_matching,
    leading_hls_connection_reduction,
    su2_current_quartic,
    u2_invariant_metric,
)


def test_general_current_wedge_equals_gram_difference() -> None:
    a, b, c, d = sp.symbols("a b c d", real=True)
    evidence = su2_current_quartic(
        [
            [a, b, 0],
            [c, 0, d],
            [0, a, c],
        ]
    )
    assert sp.simplify(
        evidence.wedge_norm_squared
        - (evidence.invariant_one - evidence.invariant_two)
    ) == 0
    assert sp.simplify(
        evidence.trace_commutator_sum + 8 * evidence.wedge_norm_squared
    ) == 0


def test_source_linear_configuration_is_a_special_case_of_general_identity() -> None:
    a, b = sp.symbols("a b", real=True)
    evidence = su2_current_quartic([[0, 0, a], [b, 0, 0]])
    assert sp.simplify(evidence.invariant_one - (a**2 + b**2) ** 2) == 0
    assert evidence.invariant_two == a**4 + b**4
    assert evidence.wedge_norm_squared == 2 * a**2 * b**2
    assert evidence.trace_commutator_sum == -16 * a**2 * b**2


def test_rank_one_current_has_no_quartic_wedge() -> None:
    a, b, c = sp.symbols("a b c", real=True)
    evidence = su2_current_quartic([[a, b, c]])
    assert evidence.wedge_norm_squared == 0
    assert evidence.trace_commutator_sum == 0


def test_internal_and_spatial_orthogonal_changes_preserve_quartic() -> None:
    components = sp.Matrix([[1, 2, 0], [0, 1, 3], [2, 0, 1]])
    internal_rotation = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
    spatial_rotation = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
    baseline = su2_current_quartic(components)
    transformed = su2_current_quartic(
        spatial_rotation * components * internal_rotation
    )
    assert transformed.invariant_one == baseline.invariant_one
    assert transformed.invariant_two == baseline.invariant_two
    assert transformed.wedge_norm_squared == baseline.wedge_norm_squared
    assert transformed.trace_commutator_sum == baseline.trace_commutator_sum


def test_pauli_generator_half_normalization_is_load_bearing() -> None:
    a, b = sp.symbols("a b", real=True)
    canonical = su2_current_quartic([[a, 0, 0], [0, b, 0]])
    sigma1 = sp.Matrix([[0, 1], [1, 0]])
    sigma2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    first = sp.I * a * sigma1 / 2
    second = sp.I * b * sigma2 / 2
    commutator = first * second - second * first
    half_trace_ordered = 2 * sp.trace(commutator * commutator)
    assert canonical.trace_commutator_sum == -16 * a**2 * b**2
    assert sp.simplify(
        half_trace_ordered - canonical.trace_commutator_sum / 16
    ) == 0


def test_leading_hls_mass_stationarity_and_half_connection_curvature() -> None:
    a, b, g, kappa = sp.symbols("a b g kappa", positive=True)
    reduction = leading_hls_connection_reduction(
        [[a, 0, 0], [0, b, 0]],
        g,
        mass_coefficient=kappa,
    )
    assert reduction.stationary_vector_components == sp.Matrix(
        [[a / 2, 0, 0], [0, b / 2, 0]]
    )
    assert reduction.mass_stationarity_residual == sp.zeros(2, 3)
    assert reduction.mass_hessian == 2 * kappa * sp.eye(6)
    pair = reduction.curvature_pairs[0]
    assert pair.connection_curvature == -pair.current_commutator / 4


def test_leading_hls_curvature_matches_skyrme_with_e_equal_g() -> None:
    a, b, g = sp.symbols("a b g", positive=True)
    reduction = leading_hls_connection_reduction(
        [[a, 0, 0], [0, b, 0]],
        g,
    )
    assert sp.simplify(
        reduction.leading_curvature_energy
        - reduction.current_quartic.wedge_norm_squared / (4 * g**2)
    ) == 0
    assert reduction.leading_curvature_energy == a**2 * b**2 / (2 * g**2)
    assert reduction.matched_skyrme_energy == reduction.leading_curvature_energy
    assert reduction.matched_skyrme_coupling == g


def test_mass_coefficient_does_not_fake_the_leading_quartic_coefficient() -> None:
    g = sp.symbols("g", positive=True)
    low = leading_hls_connection_reduction([[1, 0, 0], [0, 1, 0]], g)
    high = leading_hls_connection_reduction(
        [[1, 0, 0], [0, 1, 0]],
        g,
        mass_coefficient=17,
    )
    assert low.stationary_vector_components == high.stationary_vector_components
    assert low.leading_curvature_energy == high.leading_curvature_energy
    assert low.mass_hessian != high.mass_hessian


def test_derivative_order_ledger_prevents_exact_full_vector_claim() -> None:
    reduction = leading_hls_connection_reduction(
        [[1, 0, 0], [0, 1, 0]],
        sp.Integer(2),
    )
    orders = reduction.derivative_orders
    assert orders.connection_curvature == 2
    assert orders.kinetic_eom_residual == 3
    assert orders.leading_field_correction == 3
    assert orders.leading_quartic_energy == 4
    assert orders.first_backreaction_energy == 6
    assert orders.first_backreaction_energy > orders.leading_quartic_energy


def test_conditional_ksrf_matching_keeps_dimensionless_ratio() -> None:
    mass, decay, parameter = sp.symbols("m F a", positive=True)
    matching = conditional_hls_ksrf_matching(
        mass,
        decay,
        hls_parameter=parameter,
    )
    assert matching.relation_residual == 0
    assert matching.gauge_coupling_squared == mass**2 / (parameter * decay**2)
    assert matching.gauge_coupling == mass / (sp.sqrt(parameter) * decay)
    assert matching.skyrme_coupling == matching.gauge_coupling
    assert matching.inverse_skyrme_coupling_squared == parameter * decay**2 / mass**2


def test_a_two_ksrf_value_is_dimensionless_and_not_fpi_over_two() -> None:
    matching = conditional_hls_ksrf_matching(
        sp.Integer(775),
        sp.Rational(924, 10),
    )
    assert matching.gauge_coupling == sp.Rational(3875, 462) * sp.sqrt(2) / 2
    assert 5.9 < float(matching.gauge_coupling) < 6.0
    assert matching.skyrme_coupling != sp.Rational(924, 20)


def test_hls_parameter_is_a_visible_conditional_input() -> None:
    at_one = conditional_hls_ksrf_matching(10, 2, hls_parameter=1)
    at_two = conditional_hls_ksrf_matching(10, 2, hls_parameter=2)
    assert at_one.gauge_coupling == 5
    assert at_two.gauge_coupling == 5 * sp.sqrt(2) / 2
    assert at_one.gauge_coupling != at_two.gauge_coupling


def test_u2_fundamental_trace_is_only_the_degenerate_metric_specialization() -> None:
    coefficient = sp.symbols("a", positive=True)
    metric = u2_invariant_metric(coefficient, coefficient)
    assert metric.fundamental_trace_gram == sp.eye(4) / 2
    assert metric.invariant_gram == coefficient * sp.eye(4)
    assert metric.single_trace_coefficient == 2 * coefficient
    assert metric.double_trace_coefficient == 0
    assert metric.singlet_triplet_degenerate


def test_u2_invariance_allows_a_positive_unequal_singlet_coefficient() -> None:
    metric = u2_invariant_metric(sp.Integer(2), sp.Integer(5))
    assert metric.invariant_gram == sp.diag(5, 2, 2, 2)
    assert metric.single_trace_coefficient == 4
    assert metric.double_trace_coefficient == 3
    assert not metric.singlet_triplet_degenerate

    theta = sp.symbols("theta", real=True)
    triplet_rotation = sp.diag(
        1,
        1,
        sp.cos(theta),
        sp.cos(theta),
    )
    triplet_rotation[2, 3] = -sp.sin(theta)
    triplet_rotation[3, 2] = sp.sin(theta)
    assert (
        triplet_rotation.T * metric.invariant_gram * triplet_rotation
        - metric.invariant_gram
    ).applyfunc(sp.simplify) == sp.zeros(4)


def test_vector_current_elimination_maps_both_sextic_conventions() -> None:
    mass, coupling = sp.symbols("m g", positive=True)
    matching = conditional_vector_current_sextic_matching(mass, coupling)
    assert matching.stationary_field_per_current == -coupling / mass**2
    assert matching.stationarity_residual == sp.zeros(1)
    assert matching.effective_current_coefficient == -coupling**2 / (2 * mass**2)
    assert matching.source_sextic_coupling == coupling / (sp.sqrt(2) * mass)
    assert matching.bps_sextic_coupling == coupling / (
        sp.sqrt(2) * sp.pi**2 * mass
    )
    assert matching.convention_ratio == sp.pi**2


def test_vector_matching_keeps_mass_and_coupling_visible() -> None:
    first = conditional_vector_current_sextic_matching(3, 2)
    same_ratio = conditional_vector_current_sextic_matching(6, 4)
    different_ratio = conditional_vector_current_sextic_matching(6, 2)
    assert first.source_sextic_coupling == same_ratio.source_sextic_coupling
    assert first.vector_mass != same_ratio.vector_mass
    assert first.current_coupling != same_ratio.current_coupling
    assert first.source_sextic_coupling != different_ratio.source_sextic_coupling


@pytest.mark.parametrize(
    ("triplet", "singlet"),
    [(0, 1), (1, 0), (-1, 1), (1, -1), (1.0, 1)],
)
def test_invalid_u2_metric_coefficients_are_rejected(
    triplet: object,
    singlet: object,
) -> None:
    with pytest.raises(ValueError):
        u2_invariant_metric(triplet, singlet)


@pytest.mark.parametrize(
    ("mass", "coupling"),
    [(0, 1), (1, 0), (-1, 1), (1, -1), (1.0, 1)],
)
def test_invalid_vector_current_inputs_are_rejected(
    mass: object,
    coupling: object,
) -> None:
    with pytest.raises(ValueError):
        conditional_vector_current_sextic_matching(mass, coupling)


@pytest.mark.parametrize(
    "components",
    [[], [[1, 2]], [[1, 2, 3, 4]], [[1.0, 0, 0]], [[sp.Symbol("z"), 0, 0]]],
)
def test_invalid_or_inexact_current_components_are_rejected(components: object) -> None:
    with pytest.raises(ValueError):
        su2_current_quartic(components)


@pytest.mark.parametrize("name", ["gauge_coupling", "mass_coefficient"])
def test_nonpositive_leading_reduction_parameters_are_rejected(name: str) -> None:
    kwargs = {name: 0}
    if name == "gauge_coupling":
        with pytest.raises(ValueError):
            leading_hls_connection_reduction([[1, 0, 0]], **kwargs)
    else:
        with pytest.raises(ValueError):
            leading_hls_connection_reduction(
                [[1, 0, 0]],
                1,
                **kwargs,
            )


def test_inexact_or_nonpositive_ksrf_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        conditional_hls_ksrf_matching(775.0, 92)
    with pytest.raises(ValueError):
        conditional_hls_ksrf_matching(775, -92)
    with pytest.raises(ValueError):
        conditional_hls_ksrf_matching(775, 92, hls_parameter=0)
