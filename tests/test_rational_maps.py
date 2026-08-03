from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import sympy as sp

from substrate_framework.rational_maps import (
    axial_rational_map_angular_integral,
    exact_rational_map_degree,
    rational_map_angular_lower_bound,
    rational_map_sphere_integrals,
    rotate_rational_map_about_axis,
)


def test_exact_degree_reduces_common_polynomial_factor() -> None:
    reduced = exact_rational_map_degree([1, 1, 0], [1, 1])
    assert reduced.numerator_degree == 2
    assert reduced.denominator_degree == 1
    assert reduced.common_factor_degree == 1
    assert reduced.degree == 1
    assert not reduced.is_coprime
    assert sp.simplify(reduced.reduced_numerator / reduced.reduced_denominator - sp.Symbol("z")) == 0


def test_cubic_map_is_exactly_coprime_and_degree_four() -> None:
    coefficient = 2 * sp.I * sp.sqrt(3)
    evidence = exact_rational_map_degree(
        [1, 0, coefficient, 0, 1],
        [1, 0, -coefficient, 0, 1],
    )
    assert evidence.is_coprime
    assert evidence.degree == 4


def test_axial_family_exact_controls_and_bound() -> None:
    assert axial_rational_map_angular_integral(1) == 1
    assert sp.simplify(axial_rational_map_angular_integral(2) - (sp.pi + sp.Rational(8, 3))) == 0
    for degree in range(1, 7):
        assert axial_rational_map_angular_integral(degree) >= rational_map_angular_lower_bound(degree)


def test_identity_map_cubature_is_exact_to_roundoff() -> None:
    evidence = rational_map_sphere_integrals(
        [1.0, 0.0],
        [1.0],
        declared_degree=1,
        polar_order=12,
        azimuthal_order=20,
    )
    assert evidence.normalized_area == pytest.approx(1.0, abs=2.0e-15)
    assert evidence.angular_integral == pytest.approx(1.0, abs=2.0e-15)
    assert evidence.degree_area_relative_error < 2.0e-15


def test_degree_two_cubature_converges_to_exact_axial_value() -> None:
    exact = float(axial_rational_map_angular_integral(2))
    coarse = rational_map_sphere_integrals(
        [1.0, 0.0, 0.0],
        [1.0],
        declared_degree=2,
        polar_order=12,
        azimuthal_order=20,
    )
    fine = rational_map_sphere_integrals(
        [1.0, 0.0, 0.0],
        [1.0],
        declared_degree=2,
        polar_order=24,
        azimuthal_order=40,
    )
    assert abs(fine.angular_integral - exact) < abs(coarse.angular_integral - exact)
    assert fine.angular_integral == pytest.approx(exact, rel=2.0e-12)
    assert fine.normalized_area == pytest.approx(2.0, rel=2.0e-12)


def test_cubic_map_refines_and_is_axis_rotation_invariant() -> None:
    coefficient = 2j * np.sqrt(3.0)
    numerator = np.array([1.0, 0.0, coefficient, 0.0, 1.0])
    denominator = np.array([1.0, 0.0, -coefficient, 0.0, 1.0])
    middle = rational_map_sphere_integrals(
        numerator,
        denominator,
        declared_degree=4,
        polar_order=24,
        azimuthal_order=48,
    )
    fine = rational_map_sphere_integrals(
        numerator,
        denominator,
        declared_degree=4,
        polar_order=40,
        azimuthal_order=80,
    )
    rotated_numerator, rotated_denominator = rotate_rational_map_about_axis(
        numerator,
        denominator,
        domain_angle=0.37,
        target_angle=-0.52,
    )
    rotated = rational_map_sphere_integrals(
        rotated_numerator,
        rotated_denominator,
        declared_degree=4,
        polar_order=40,
        azimuthal_order=80,
    )
    assert abs(fine.normalized_area - 4.0) < abs(middle.normalized_area - 4.0)
    assert fine.normalized_area == pytest.approx(4.0, rel=2.0e-10)
    assert fine.angular_integral > 16.0
    assert rotated.angular_integral == pytest.approx(fine.angular_integral, rel=2.0e-11)
    assert rotated.normalized_area == pytest.approx(fine.normalized_area, rel=2.0e-11)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: exact_rational_map_degree([1.0, 0.0], [1]), "must be exact"),
        (lambda: axial_rational_map_angular_integral(0), "positive integer"),
        (
            lambda: rational_map_sphere_integrals([], [1], declared_degree=1),
            "nonempty",
        ),
        (
            lambda: rational_map_sphere_integrals([1, 0], [1], declared_degree=1, polar_order=3),
            "at least four",
        ),
    ],
)
def test_invalid_rational_map_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()


def test_canonical_module_has_no_numpy_trapezoid_alias() -> None:
    source = Path("src/substrate_framework/rational_maps.py").read_text(encoding="utf-8")
    assert "np.tr" + "apz" not in source
