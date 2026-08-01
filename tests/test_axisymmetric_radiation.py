from __future__ import annotations

import numpy as np
import pytest

from substrate_framework.axisymmetric_radiation import (
    conditional_axisymmetric_radiation_coefficients,
)


def test_normalized_and_triple_axial_eigenvalue_traces_are_convention_invariant() -> None:
    triple_second = np.array([-4.0, 0.0, 5.0])
    triple_third = np.array([2.0, -3.0, 7.0])
    triple = conditional_axisymmetric_radiation_coefficients(
        triple_second,
        triple_third,
        inclination=np.pi / 3.0,
        quadrupole_scale=3.0,
    )
    normalized = conditional_axisymmetric_radiation_coefficients(
        triple_second / 3.0,
        triple_third / 3.0,
        inclination=np.pi / 3.0,
        quadrupole_scale=1.0,
    )
    np.testing.assert_allclose(
        triple.conventional_plus_R_over_G,
        normalized.conventional_plus_R_over_G,
    )
    np.testing.assert_allclose(triple.power_over_G, normalized.power_over_G)


def test_triple_qzz_formula_axis_null_and_wrong_convention_mutation() -> None:
    second = np.array([2.0, -4.0])
    third = np.array([3.0, 5.0])
    edge = conditional_axisymmetric_radiation_coefficients(
        second,
        third,
        inclination=np.pi / 2.0,
        quadrupole_scale=3.0,
    )
    axis = conditional_axisymmetric_radiation_coefficients(
        second,
        third,
        inclination=0.0,
        quadrupole_scale=3.0,
    )
    wrong = conditional_axisymmetric_radiation_coefficients(
        second,
        third,
        inclination=np.pi / 2.0,
        quadrupole_scale=1.0,
    )
    np.testing.assert_allclose(edge.conventional_plus_R_over_G, second / 2.0)
    np.testing.assert_allclose(edge.power_over_G, third**2 / 30.0)
    assert np.array_equal(edge.conventional_cross_R_over_G, np.zeros(2))
    assert np.array_equal(axis.conventional_plus_R_over_G, np.zeros(2))
    assert np.array_equal(axis.conventional_cross_R_over_G, np.zeros(2))
    np.testing.assert_allclose(
        wrong.conventional_plus_R_over_G,
        3.0 * edge.conventional_plus_R_over_G,
    )
    np.testing.assert_allclose(wrong.power_over_G, 9.0 * edge.power_over_G)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: conditional_axisymmetric_radiation_coefficients(
                [1.0], [1.0, 2.0], inclination=0.2, quadrupole_scale=3.0
            ),
            "same shape",
        ),
        (
            lambda: conditional_axisymmetric_radiation_coefficients(
                [1.0], [2.0], inclination=np.nan, quadrupole_scale=3.0
            ),
            "inclination",
        ),
        (
            lambda: conditional_axisymmetric_radiation_coefficients(
                [1.0], [2.0], inclination=0.2, quadrupole_scale=0.0
            ),
            "quadrupole_scale",
        ),
    ],
)
def test_invalid_conditional_axisymmetric_trace_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
