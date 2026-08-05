import numpy as np
import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.rational_map_stability import (
    degree_two_rational_map_hessian,
    degree_two_rational_map_quadratic_form,
)


def test_rational_map_stability_public_api_is_exported():
    assert sf.degree_two_rational_map_hessian is degree_two_rational_map_hessian
    assert sf.degree_two_rational_map_quadratic_form is degree_two_rational_map_quadratic_form


def test_degree_two_chart_has_exact_stationary_positive_semidefinite_hessian():
    evidence = degree_two_rational_map_hessian()
    assert evidence.angular_functional == sp.pi + sp.Rational(8, 3)
    assert evidence.gradient == sp.zeros(10, 1)
    assert evidence.hessian == evidence.hessian.T
    assert evidence.hessian.is_positive_semidefinite is True
    assert evidence.hessian_rank == 5
    assert evidence.hessian_nullity == 5
    expected = (
        (sp.S.Zero, 5),
        (sp.pi, 1),
        (sp.pi + sp.Rational(16, 3), 2),
        (7 * sp.pi + sp.Rational(64, 3), 2),
    )
    for value, count in expected:
        assert sum(sp.simplify(item - value) == 0 for item in evidence.eigenvalues) == count


def test_exact_kernel_is_the_five_dimensional_symmetry_tangent_span():
    evidence = degree_two_rational_map_hessian()
    assert evidence.symmetry_rank == 5
    assert evidence.symmetry_residual == sp.zeros(10, 5)
    assert evidence.kernel_is_exact_symmetry_span
    nullspace = sp.Matrix.hstack(*evidence.hessian.nullspace())
    assert sp.Matrix.hstack(nullspace, evidence.symmetry_tangents).rank() == 5
    for tangent in evidence.symmetry_tangents.columnspace():
        assert degree_two_rational_map_quadratic_form(tangent) == 0


def test_exact_complement_has_the_positive_curvature_spectrum():
    evidence = degree_two_rational_map_hessian()
    restricted = sp.simplify(
        evidence.positive_complement.T
        * evidence.hessian
        * evidence.positive_complement
    )
    assert evidence.positive_complement.rank() == 5
    assert evidence.positive_on_declared_complement
    assert restricted == sp.diag(
        4 * (sp.pi / 2 + sp.Rational(8, 3)),
        4 * (sp.pi / 2 + sp.Rational(8, 3)),
        4 * (sp.Rational(32, 3) + 7 * sp.pi / 2),
        4 * (sp.Rational(32, 3) + 7 * sp.pi / 2),
        sp.pi,
    )


def test_source_finite_difference_positive_modes_converge_to_exact_values():
    evidence = degree_two_rational_map_hessian()
    exact = np.array([float(item) for item in evidence.positive_eigenvalues])
    source = np.array([3.14191, 8.47528, 8.47528, 43.3256, 43.3256])
    assert np.allclose(source, exact, rtol=3e-5, atol=4e-4)
    assert min(exact) > 2.5


def test_coordinate_congruence_preserves_rank_and_quadratic_inertia():
    evidence = degree_two_rational_map_hessian()
    change = sp.diag(2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    transformed = change.T * evidence.hessian * change
    assert transformed.rank() == 5
    assert len(transformed.nullspace()) == 5
    coordinates = sp.Matrix(sp.symbols("x0:10", real=True))
    a = sp.pi / 2 + sp.Rational(8, 3)
    b = sp.Rational(32, 3) + 7 * sp.pi / 2
    expected_form = (
        a * (2 * coordinates[0] + 17 * coordinates[6]) ** 2
        + a * (3 * coordinates[1] - 19 * coordinates[7]) ** 2
        + b * (5 * coordinates[2] + 11 * coordinates[4]) ** 2
        + b * (7 * coordinates[3] - 13 * coordinates[5]) ** 2
        + sp.pi * (23 * coordinates[8]) ** 2
    )
    assert sp.expand((coordinates.T * transformed * coordinates)[0] - expected_form) == 0


def test_negative_curvature_and_nonstationary_mutations_break_the_verdict():
    evidence = degree_two_rational_map_hessian()
    direction = sp.zeros(10, 1)
    direction[8] = 1
    negative_mutation = evidence.hessian - 2 * sp.pi * direction * direction.T
    assert (direction.T * negative_mutation * direction)[0] == -sp.pi
    assert negative_mutation.is_positive_semidefinite is False
    mutated_gradient = evidence.gradient + direction
    assert mutated_gradient != sp.zeros(10, 1)


def test_degree_two_quadratic_form_rejects_wrong_dimension():
    with pytest.raises(ValueError, match="ten chart coordinates"):
        degree_two_rational_map_quadratic_form(sp.zeros(9, 1))
