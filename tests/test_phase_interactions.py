from __future__ import annotations

import math

import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.phase_interactions import (
    pairwise_phase_cosines,
    quartic_sech_pair_interaction,
    scalar_circle_packing,
    sech_pair_density_shape,
    sech_pair_mixed_cubic_shape,
)


def test_phase_interaction_public_api_is_exported() -> None:
    assert sf.QuarticSechPairInteraction is not None
    assert sf.ScalarCirclePacking is not None
    assert sf.quartic_sech_pair_interaction is quartic_sech_pair_interaction
    assert sf.scalar_circle_packing is scalar_circle_packing


def test_overlap_shapes_follow_independent_rational_substitution() -> None:
    separation = sp.log(3)
    t = sp.symbols("t", real=True)
    cosine_hyperbolic = sp.cosh(separation)
    sine_hyperbolic = sp.sinh(separation)
    direct_31 = sp.integrate(
        (1 - t**2) / (cosine_hyperbolic - sine_hyperbolic * t),
        (t, -1, 1),
    )
    direct_22 = sp.integrate(
        (1 - t**2) / (cosine_hyperbolic - sine_hyperbolic * t) ** 2,
        (t, -1, 1),
    )
    assert sp.simplify(direct_31 - sech_pair_mixed_cubic_shape(separation)) == 0
    assert sp.simplify(direct_22 - sech_pair_density_shape(separation)) == 0


def test_exact_pair_energy_retains_every_phase_power() -> None:
    d, c, amplitude, kappa = sp.symbols("d c A kappa", positive=True)
    result = quartic_sech_pair_interaction(d, c, amplitude, kappa)
    expected = -c * result.mixed_cubic_overlap / 6 - (
        1 + 2 * c**2
    ) * result.density_overlap / 12
    assert sp.simplify(result.interaction_energy - expected) == 0
    assert sp.diff(result.interaction_energy, c, 2) != 0
    perpendicular = quartic_sech_pair_interaction(d, 0, amplitude, kappa)
    assert sp.simplify(
        perpendicular.interaction_energy
        + perpendicular.density_overlap / 12
    ) == 0


def test_exact_formula_reproduces_source_values_without_quadrature() -> None:
    omega = 0.45
    kappa = math.sqrt(0.5 - omega**2)
    amplitude = 2.0 * math.sqrt(6.0) * kappa
    expected = {
        (6.0, 1.0): -3.557102022641099,
        (10.0, -1.0): 0.23597506089536688,
        (12.0, 0.0): -0.0014269303147464918,
    }
    for (distance, cosine), value in expected.items():
        result = quartic_sech_pair_interaction(
            distance, cosine, amplitude, kappa
        )
        assert float(result.interaction_energy) == pytest.approx(value, rel=2e-13)


def test_large_separation_rates_separate_leading_and_marginal_terms() -> None:
    s = sp.symbols("s", positive=True)
    j31 = sech_pair_mixed_cubic_shape(s)
    j22 = sech_pair_density_shape(s)
    assert sp.limit(sp.exp(s) * j31, s, sp.oo) == 4
    assert sp.limit(
        j22 / (16 * (s - 1) * sp.exp(-2 * s)), s, sp.oo
    ) == 1


@pytest.mark.parametrize(
    ("count", "optimum", "strict", "weak"),
    [
        (2, -1, True, True),
        (3, -sp.Rational(1, 2), True, True),
        (4, 0, False, True),
        (5, (sp.sqrt(5) - 1) / 4, False, False),
    ],
)
def test_scalar_circle_capacity_is_sharp(
    count: int,
    optimum: sp.Expr,
    strict: bool,
    weak: bool,
) -> None:
    result = scalar_circle_packing(count)
    assert sp.simplify(result.optimal_worst_pairwise_cosine - optimum) == 0
    assert max(result.regular_pairwise_cosines) == optimum
    assert result.strictly_negative_possible is strict
    assert result.nonpositive_possible is weak


def test_capacity_does_not_select_three_and_depends_on_complete_graph() -> None:
    assert scalar_circle_packing(2).strictly_negative_possible
    assert scalar_circle_packing(3).strictly_negative_possible
    four_cycle_phases = (0, sp.pi, 0, sp.pi)
    all_cosines = pairwise_phase_cosines(four_cycle_phases)
    cycle_cosines = tuple(
        sp.cos(four_cycle_phases[i] - four_cycle_phases[j])
        for i, j in ((0, 1), (1, 2), (2, 3), (3, 0))
    )
    assert all(value == -1 for value in cycle_cosines)
    assert max(all_cosines) == 1


def test_vector_internal_space_changes_the_capacity_problem() -> None:
    tetrahedron = [
        sp.Matrix(vector) / sp.sqrt(3)
        for vector in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
    ]
    dots = [
        sp.simplify(tetrahedron[i].dot(tetrahedron[j]))
        for i in range(4)
        for j in range(i + 1, 4)
    ]
    assert dots == [-sp.Rational(1, 3)] * 6
    assert not scalar_circle_packing(4).strictly_negative_possible


@pytest.mark.parametrize(
    "call",
    [
        lambda: quartic_sech_pair_interaction(0, 0, 1, 1),
        lambda: quartic_sech_pair_interaction(1, 2, 1, 1),
        lambda: quartic_sech_pair_interaction(1, 0, -1, 1),
        lambda: quartic_sech_pair_interaction(1, 0, 1, 0),
        lambda: pairwise_phase_cosines([0]),
        lambda: pairwise_phase_cosines([0, sp.I]),
        lambda: scalar_circle_packing(True),
        lambda: scalar_circle_packing(1),
    ],
)
def test_phase_interaction_inputs_are_typed(call) -> None:
    with pytest.raises((TypeError, ValueError)):
        call()
