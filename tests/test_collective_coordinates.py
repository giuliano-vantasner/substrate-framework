from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.collective_coordinates import (
    capillary_barrier_top_linearization,
    collective_coordinate_dimension_ledger,
    collective_coordinate_metric,
    reduced_collective_euler_lagrange,
    reduced_collective_lagrangian,
    stationary_collective_linearization,
    transform_collective_coordinate,
)


def test_gaussian_profile_has_finite_positive_pullback_metric() -> None:
    x, q = sp.symbols("x q", real=True)
    length, inertia_density = sp.symbols("ell lambda", positive=True)
    profile = sp.exp(-(x - q) ** 2 / (2 * length**2))
    result = collective_coordinate_metric(
        inertia_density,
        profile,
        x,
        q,
    )
    assert sp.simplify(
        result.profile_derivative - (x - q) * profile / length**2
    ) == 0
    assert sp.simplify(result.geometric_integral - sp.sqrt(sp.pi) / (2 * length)) == 0
    assert sp.simplify(
        result.inertia - inertia_density * sp.sqrt(sp.pi) / (2 * length)
    ) == 0


def test_dimensions_close_but_do_not_prove_profile_integrability() -> None:
    ledger = collective_coordinate_dimension_ledger()
    columns = {
        name: ledger.dimension_matrix[:, index]
        for index, name in enumerate(ledger.quantity_names)
    }
    assert columns["profile_derivative"] + columns["profile_derivative"] + columns["spatial_measure"] == columns["geometric_integral"]
    assert columns["inertia_density"] + columns["geometric_integral"] == columns["collective_inertia"]
    assert columns["potential_curvature"] - columns["collective_inertia"] == columns["spectral_ratio"]
    assert 2 * columns["rate"] == columns["spectral_ratio"]

    x, q = sp.symbols("x q", real=True)
    inertia_density = sp.symbols("lambda", positive=True)
    zero = collective_coordinate_metric(inertia_density, x**2, x, q)
    divergent = collective_coordinate_metric(inertia_density, q * x, x, q)
    assert zero.geometric_integral == 0
    assert divergent.geometric_integral is sp.oo


def test_variable_metric_euler_lagrange_has_connection_half_factor() -> None:
    q, qdot, qddot = sp.symbols("q qdot qddot", real=True)
    mass_scale, stiffness = sp.symbols("M0 k", positive=True)
    inertia = mass_scale * (1 + q**2)
    potential = stiffness * q**2 / 2
    assert reduced_collective_lagrangian(inertia, potential, qdot) == inertia * qdot**2 / 2 - potential
    assert reduced_collective_euler_lagrange(
        inertia,
        potential,
        q,
        qdot,
        qddot,
    ) == inertia * qddot + mass_scale * q * qdot**2 + stiffness * q


@pytest.mark.parametrize(
    ("curvature", "stability", "frequency", "rate"),
    [
        (sp.Integer(3), "stable", sp.sqrt(6) / 2, None),
        (sp.Integer(0), "neutral", sp.S.Zero, sp.S.Zero),
        (sp.Integer(-3), "unstable", None, sp.sqrt(6) / 2),
    ],
)
def test_stationary_curvature_sign_classification(
    curvature: sp.Expr,
    stability: str,
    frequency: sp.Expr | None,
    rate: sp.Expr | None,
) -> None:
    result = stationary_collective_linearization(2, curvature)
    assert result.stability == stability
    assert result.stable_angular_frequency == frequency
    assert result.instability_rate == rate
    assert result.characteristic_root_squared == -curvature / 2


def test_capillary_barrier_top_is_unstable_not_a_stable_mode() -> None:
    pressure, inertia = sp.symbols("P M", positive=True)
    result = capillary_barrier_top_linearization(pressure, inertia)
    assert result.curvature == -2 * sp.pi * pressure
    assert result.stability == "unstable"
    assert result.stable_angular_frequency is None
    assert sp.simplify(result.instability_rate - sp.sqrt(2 * sp.pi * pressure / inertia)) == 0
    assert result.characteristic_roots == (
        -sp.sqrt(2) * sp.sqrt(sp.pi) * sp.sqrt(pressure) / sp.sqrt(inertia),
        sp.sqrt(2) * sp.sqrt(sp.pi) * sp.sqrt(pressure) / sp.sqrt(inertia),
    )


def test_stationary_spectral_ratio_is_coordinate_invariant() -> None:
    q, Q = sp.symbols("q Q", real=True)
    inertia, stiffness, scale = sp.symbols("M k a", positive=True)
    potential = stiffness * q**2 / 2
    changed = transform_collective_coordinate(
        inertia,
        potential,
        q,
        Q,
        Q / scale,
    )
    assert changed.transformed_inertia == inertia / scale**2
    assert changed.stationary_hessian == stiffness / scale**2
    assert changed.stationary_spectral_ratio == stiffness / inertia
    assert changed.hessian_chain_term == 0


def test_nonstationary_hessian_has_an_extra_chain_term() -> None:
    q, Q = sp.symbols("q Q", positive=True)
    changed = transform_collective_coordinate(1, q**3, q, Q, Q**2)
    assert changed.hessian_chain_term == 6 * Q**4
    assert changed.transformed_hessian == sp.diff(Q**6, Q, 2)
    assert changed.transformed_hessian != changed.stationary_hessian


def test_common_action_scaling_cancels_but_inertia_only_scaling_does_not() -> None:
    mass, curvature, scale = sp.symbols("M K rho", positive=True)
    baseline = stationary_collective_linearization(mass, curvature)
    common = stationary_collective_linearization(scale * mass, scale * curvature)
    inertia_only = stationary_collective_linearization(scale * mass, curvature)
    assert common.spectral_ratio == baseline.spectral_ratio
    assert inertia_only.spectral_ratio == baseline.spectral_ratio / scale


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: collective_coordinate_metric(
                -1,
                sp.symbols("q") * sp.symbols("x"),
                sp.symbols("x"),
                sp.symbols("q"),
            ),
            "inertia_density",
        ),
        (lambda: stationary_collective_linearization(0, 1), "inertia_at_stationary_point"),
        (
            lambda: transform_collective_coordinate(
                1,
                sp.symbols("q") ** 2,
                sp.symbols("q"),
                sp.symbols("Q"),
                1,
            ),
            "locally invertible",
        ),
        (lambda: capillary_barrier_top_linearization(0, 1), "pressure"),
    ],
)
def test_numeric_and_mapping_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
