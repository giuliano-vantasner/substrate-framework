"""Exact tests for the narrowly harvested issue #28 ensemble atoms."""

from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.flux_tube_ensemble import (
    isotropic_average_equation_of_state,
    orientation_average_nn,
    tube_longitudinal_pressure,
    tube_transverse_pressure,
)


def test_tube_pressures_for_inverse_quartic_density() -> None:
    coefficient = sp.Symbol("c", positive=True)
    length = sp.Symbol("L", positive=True)
    density = -coefficient * length**-4
    assert sp.simplify(tube_transverse_pressure(coefficient) - density) == 0
    assert sp.simplify(tube_longitudinal_pressure(coefficient) + density) == 0


def test_isotropic_average_w_is_one_third_for_either_sign() -> None:
    assert isotropic_average_equation_of_state(1) == sp.Rational(1, 3)
    assert isotropic_average_equation_of_state(-1) == sp.Rational(1, 3)
    with pytest.raises(ValueError, match="coefficient must be nonzero"):
        isotropic_average_equation_of_state(0)


def test_orientation_average_is_delta_over_three() -> None:
    for i in range(3):
        for j in range(3):
            expected = sp.Rational(1, 3) if i == j else sp.Integer(0)
            assert orientation_average_nn(i, j) == expected
    with pytest.raises(ValueError, match="orientation indices"):
        orientation_average_nn(-1, 0)
