from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.gordon_metric import (
    gordon_metric_mostly_plus,
    transverse_profile_einstein,
)


def test_rest_metric_inverse_determinants_and_null_speed() -> None:
    n = sp.symbols("n", positive=True)
    metric = gordon_metric_mostly_plus(n, [1, 0, 0, 0])
    assert metric.contravariant == sp.diag(-n**2, 1, 1, 1)
    assert metric.covariant == sp.diag(-1 / n**2, 1, 1, 1)
    assert metric.contravariant_determinant == -n**2
    assert metric.covariant_determinant == -1 / n**2
    assert metric.rest_phase_speed == 1 / n


def test_z_boost_metric_is_exactly_invertible_and_lorentzian_at_source_witness() -> None:
    velocity = sp.Rational(1, 2)
    gamma = 2 / sp.sqrt(3)
    metric = gordon_metric_mostly_plus(2, [gamma, 0, 0, gamma * velocity])
    assert (metric.contravariant * metric.covariant).applyfunc(sp.simplify) == sp.eye(4)
    assert metric.contravariant.det() == -4
    assert metric.covariant.det() == -sp.Rational(1, 4)
    assert metric.covariant.is_positive_definite is False


def test_transverse_profile_corrects_source_value_but_preserves_ratios() -> None:
    x = sp.symbols("x", real=True)
    n = sp.Function("n", positive=True)(x)
    result = transverse_profile_einstein(n, x, sp.Rational(1, 2))
    tensor = result.einstein_covariant
    witness = {n: 2, sp.diff(n, x): 1, sp.diff(n, x, 2): 0}
    at_zero = tensor.applyfunc(lambda entry: sp.simplify(entry.subs(witness)))
    assert at_zero[0, 0] == sp.Rational(1, 6)
    assert at_zero[0, 3] == -2 * at_zero[0, 0]
    assert at_zero[2, 2] == 3 * at_zero[0, 0]
    assert at_zero[3, 3] == 4 * at_zero[0, 0]
    assert at_zero[1, 1] == 0
    assert at_zero[0, 0] != sp.Rational(5, 6)


def test_constant_index_is_flat_for_every_admissible_constant_boost() -> None:
    x = sp.symbols("x", real=True)
    for velocity in (0, sp.Rational(1, 3), -sp.Rational(2, 3)):
        result = transverse_profile_einstein(sp.Integer(3), x, velocity)
        assert result.curvature_kernel == 0
        assert result.ricci_scalar == 0
        assert result.einstein_covariant == sp.zeros(4)


def test_correct_static_weak_index_expansion_differs_from_optical_family() -> None:
    epsilon = sp.symbols("epsilon", real=True)
    gordon = -1 / (1 + epsilon) ** 2
    optical = -1 / (1 + epsilon)
    assert sp.series(gordon, epsilon, 0, 2) == -1 + 2 * epsilon + sp.Order(epsilon**2)
    assert sp.series(optical, epsilon, 0, 2) == -1 + epsilon + sp.Order(epsilon**2)


def test_one_plus_one_breather_cannot_source_nonflat_z_boost_profile() -> None:
    x = sp.symbols("x", real=True)
    n = sp.Function("n", positive=True)(x)
    coupling, energy_density = sp.symbols("kappa rho", positive=True)
    result = transverse_profile_einstein(n, x, sp.Rational(1, 2))
    witness = {n: 2, sp.diff(n, x): 1, sp.diff(n, x, 2): 0}
    geometry = result.einstein_covariant.subs(witness)
    breather_t_t = energy_density
    breather_t_z = sp.Integer(0)
    inferred = sp.solve(sp.Eq(geometry[0, 0], coupling * breather_t_t), coupling)[0]
    assert inferred == 1 / (6 * energy_density)
    assert geometry[0, 3] != inferred * breather_t_z


@pytest.mark.parametrize(
    ("index", "velocity", "message"),
    [
        (0, 0, "refractive_index"),
        (-1, 0, "refractive_index"),
        (sp.Symbol("z"), 0, "refractive_index"),
        (1, 1, "velocity"),
        (1, -1, "velocity"),
        (1, sp.Rational(3, 2), "velocity"),
        (1.0, 0, "refractive_index"),
        (1, 0.5, "velocity"),
    ],
)
def test_profile_input_guards(index: object, velocity: object, message: str) -> None:
    x = sp.symbols("x", real=True)
    with pytest.raises(ValueError, match=message):
        transverse_profile_einstein(index, x, velocity)


def test_four_velocity_guards() -> None:
    with pytest.raises(ValueError, match="four_velocity_up"):
        gordon_metric_mostly_plus(2, [1, 0, 0])
    with pytest.raises(ValueError, match="norm -1"):
        gordon_metric_mostly_plus(2, [1, 0, 0, 1])
    with pytest.raises(ValueError, match="four_velocity_up"):
        gordon_metric_mostly_plus(2, [1.0, 0, 0, 0])
