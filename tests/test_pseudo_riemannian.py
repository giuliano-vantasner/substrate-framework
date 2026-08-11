"""Exact tests for the dimension-aware coordinate-geometry API."""

from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.covariant_sine_gordon_action import (
    christoffel_symbols,
    ricci_scalar,
    ricci_tensor,
)
from substrate_framework.pseudo_riemannian import (
    exact_metric_matrix,
    metric_christoffel_from_derivatives,
    metric_christoffel_symbols,
    metric_ricci_scalar,
    metric_ricci_tensor,
)


def test_unit_two_sphere_has_expected_exact_curvature() -> None:
    theta, phi = sp.symbols("theta phi", real=True)
    metric = sp.diag(1, sp.sin(theta) ** 2)

    tensor = metric_ricci_tensor(metric, (theta, phi))

    assert sp.simplify(tensor - metric) == sp.zeros(2)
    assert sp.simplify(metric_ricci_scalar(metric, (theta, phi)) - 2) == 0


def test_local_derivative_connection_matches_coordinate_derivation() -> None:
    x, y, z = sp.symbols("x y z", real=True)
    coordinates = (x, y, z)
    metric = sp.diag(-1, (1 + x) ** 2, (2 + y) ** 2)
    point = {x: 1, y: 1, z: 0}
    gamma_coordinate = metric_christoffel_symbols(metric, coordinates)
    metric_at_point = metric.subs(point)
    derivatives = sp.MutableDenseNDimArray.zeros(3, 3, 3)
    for rho, coordinate in enumerate(coordinates):
        for mu in range(3):
            for nu in range(3):
                derivatives[rho, mu, nu] = sp.diff(
                    metric[mu, nu], coordinate
                ).subs(point)

    gamma_local = metric_christoffel_from_derivatives(
        metric_at_point.inv(), derivatives
    )

    for upper in range(3):
        for mu in range(3):
            for nu in range(3):
                assert sp.simplify(
                    gamma_local[upper, mu, nu]
                    - gamma_coordinate[upper][mu][nu].subs(point)
                ) == 0


def test_covariant_sine_gordon_geometry_wrappers_preserve_results_and_shape() -> None:
    t, x, y, z = sp.symbols("t x y z", real=True)
    scale = sp.Function("a", positive=True)(t)
    metric = sp.diag(-1, scale**2, scale**2, scale**2)
    coordinates = (t, x, y, z)

    generic_gamma = metric_christoffel_symbols(metric, coordinates)
    legacy_gamma = christoffel_symbols(metric, coordinates)

    assert isinstance(legacy_gamma, list)
    assert legacy_gamma[0][1][1] == generic_gamma[0][1][1]
    assert ricci_tensor(metric, coordinates) == metric_ricci_tensor(
        metric, coordinates
    )
    assert ricci_scalar(metric, coordinates) == metric_ricci_scalar(
        metric, coordinates
    )


def test_geometry_contract_rejects_wrong_inputs() -> None:
    x, y = sp.symbols("x y", real=True)
    with pytest.raises(ValueError, match="symmetric"):
        exact_metric_matrix([[1, 1], [0, 1]])
    with pytest.raises(ValueError, match="floating"):
        exact_metric_matrix([[1.0, 0], [0, 1]])
    with pytest.raises(ValueError, match="invertible"):
        exact_metric_matrix([[1, 1], [1, 1]])
    with pytest.raises(ValueError, match="distinct"):
        metric_christoffel_symbols(sp.eye(2), (x, x))
    with pytest.raises(ValueError, match="shape"):
        metric_christoffel_from_derivatives(sp.eye(2), [[[0]]])

    nonsymmetric_derivatives = sp.MutableDenseNDimArray.zeros(2, 2, 2)
    nonsymmetric_derivatives[0, 0, 1] = 1
    with pytest.raises(ValueError, match="symmetric"):
        metric_christoffel_from_derivatives(
            sp.eye(2), nonsymmetric_derivatives
        )
