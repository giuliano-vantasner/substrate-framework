from __future__ import annotations

from mpmath import mp
import pytest
import sympy as sp

from substrate_framework.flat_torus import (
    enumerate_translations_below,
    has_nondegenerate_matched_circles,
    laplacian_eigenspaces,
    matched_circle_angular_radius,
    matched_circle_geometries,
    reciprocal_wavevector,
    rectangular_epstein_partial_sum,
    rectangular_epstein_refinement,
    rectangular_torus_volume,
    scalar_laplacian_eigenvalue,
    shortest_translation_length,
    translation_squared_length,
)


SIDES = (1, sp.sqrt(2), sp.sqrt(3))


def test_rectangular_volume_and_reciprocal_modes_are_exact() -> None:
    assert rectangular_torus_volume(SIDES) == sp.sqrt(6)
    assert reciprocal_wavevector((1, -2, 3), SIDES) == (
        2 * sp.pi,
        -2 * sp.sqrt(2) * sp.pi,
        2 * sp.sqrt(3) * sp.pi,
    )
    assert scalar_laplacian_eigenvalue((1, -2, 3), SIDES) == 24 * sp.pi**2


def test_twist_is_one_fixed_boundary_condition_not_a_mixed_label_grid() -> None:
    half = (sp.Rational(1, 2),) * 3
    value = scalar_laplacian_eigenvalue((0, 0, 0), SIDES, twist=half)
    assert value == 11 * sp.pi**2 / 6

    eigenspaces = laplacian_eigenspaces(SIDES, 1, twist=half)
    assert eigenspaces[0].eigenvalue == 11 * sp.pi**2 / 6
    assert eigenspaces[0].multiplicity == 8


def test_periodic_spectral_gap_comes_from_the_longest_side() -> None:
    eigenspaces = laplacian_eigenspaces(SIDES, 1)
    assert eigenspaces[0].eigenvalue == 0
    assert eigenspaces[0].modes == ((0, 0, 0),)
    assert eigenspaces[1].eigenvalue == 4 * sp.pi**2 / 3
    assert eigenspaces[1].modes == ((0, 0, -1), (0, 0, 1))


def test_side_length_mutation_changes_only_its_reciprocal_component() -> None:
    baseline = reciprocal_wavevector((1, 1, 1), SIDES)
    mutated = reciprocal_wavevector(
        (1, 1, 1), (1, 2 * sp.sqrt(2), sp.sqrt(3))
    )
    assert mutated[0] == baseline[0]
    assert mutated[1] == baseline[1] / 2
    assert mutated[2] == baseline[2]


def test_translation_geometry_and_shortest_length_are_exact() -> None:
    assert translation_squared_length((1, -1, 2), SIDES) == 15
    assert shortest_translation_length(SIDES) == 1


def test_translation_cutoff_is_strict_and_complete_at_a_boundary() -> None:
    assert enumerate_translations_below((1, sp.sqrt(2)), 1) == ()
    translations = enumerate_translations_below((1, sp.sqrt(2)), sp.sqrt(2))
    assert tuple(item.index for item in translations) == ((-1, 0), (1, 0))


def test_translation_sign_quotient_returns_one_representative_per_pair() -> None:
    translations = enumerate_translations_below(
        (1, 1), sp.sqrt(2), unique_up_to_sign=True
    )
    assert tuple(item.index for item in translations) == ((0, 1), (1, 0))


def test_containment_excludes_only_nondegenerate_matched_circles() -> None:
    scale = sp.Rational(2857, 100)
    assert not has_nondegenerate_matched_circles(
        (scale, sp.sqrt(2) * scale, sp.sqrt(3) * scale),
        sp.Rational(141, 10),
    )
    assert has_nondegenerate_matched_circles(
        (28, 28 * sp.sqrt(2), 28 * sp.sqrt(3)), sp.Rational(141, 10)
    )
    assert not has_nondegenerate_matched_circles((2, 3, 4), 1)


def test_matched_circle_radius_has_correct_exact_limits() -> None:
    assert matched_circle_angular_radius(sp.sqrt(2), 1) == sp.pi / 4
    with pytest.raises(ValueError, match="strictly less"):
        matched_circle_angular_radius(2, 1)
    with pytest.raises(ValueError, match="positive"):
        matched_circle_angular_radius(0, 1)


def test_matched_circle_enumeration_combines_translation_and_radius() -> None:
    circles = matched_circle_geometries((1, 10), 1, unique_pairs=True)
    assert tuple(circle.translation.index for circle in circles) == ((1, 0),)
    assert circles[0].angular_radius == sp.pi / 3


def test_epstein_partial_sum_matches_independent_one_dimensional_sum() -> None:
    cutoff = 4
    actual = rectangular_epstein_partial_sum((2,), 2, cutoff, precision=60)
    expected = mp.fsum(
        2 * mp.mpf(n) ** -4 / 16 for n in range(1, cutoff + 1)
    )
    assert mp.almosteq(actual, expected)


def test_epstein_scale_power_is_load_bearing() -> None:
    baseline = rectangular_epstein_partial_sum(SIDES, 2, 3, precision=60)
    doubled = rectangular_epstein_partial_sum(
        tuple(2 * side for side in SIDES), 2, 3, precision=60
    )
    assert mp.almosteq(doubled, baseline / 16)


def test_epstein_refinement_reports_positive_unhidden_tail_increments() -> None:
    points = rectangular_epstein_refinement(SIDES, 2, (1, 2, 4), precision=60)
    assert tuple(point.max_index for point in points) == (1, 2, 4)
    assert points[0].increment is None
    assert points[1].increment is not None and points[1].increment > 0
    assert points[2].increment is not None and points[2].increment > 0
    assert points[2].increment < points[1].increment


@pytest.mark.parametrize(
    ("call", "match"),
    [
        (lambda: rectangular_torus_volume(()), "nonempty"),
        (lambda: reciprocal_wavevector((1, 2), SIDES), "length"),
        (
            lambda: reciprocal_wavevector((1, 2, 3), SIDES, twist=(0, 0)),
            "length",
        ),
        (
            lambda: scalar_laplacian_eigenvalue(
                (1, sp.Rational(1, 2), 0), SIDES
            ),
            "integer",
        ),
        (lambda: enumerate_translations_below((1, -2), 3), "positive"),
        (lambda: rectangular_epstein_partial_sum(SIDES, 1, 2), "dimension/2"),
        (lambda: rectangular_epstein_partial_sum(SIDES, 2, 0), "positive"),
        (
            lambda: rectangular_epstein_refinement(SIDES, 2, (2, 2)),
            "increasing",
        ),
    ],
)
def test_invalid_domains_are_rejected(call, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        call()
