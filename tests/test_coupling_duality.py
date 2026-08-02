from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.coupling_duality import (
    reciprocal_coefficient_for_fixed_target,
    reciprocal_coordinate_change_ledger,
    reciprocal_coupling_ledger,
)


def test_reciprocal_map_is_an_involution_with_constant_orbit_product() -> None:
    x, coefficient = sp.symbols("x A", positive=True)
    ledger = reciprocal_coupling_ledger(x, coefficient)
    assert ledger.dual_coordinate == coefficient / x
    assert ledger.double_dual_coordinate == x
    assert ledger.orbit_product == coefficient


def test_positive_fixed_point_is_conditional_on_the_coefficient() -> None:
    coefficient = sp.symbols("A", positive=True)
    ledger = reciprocal_coupling_ledger(2, coefficient)
    assert ledger.positive_fixed_point == sp.sqrt(coefficient)
    assert ledger.fixed_point_image == sp.sqrt(coefficient)
    assert ledger.fixed_point_residual == 0


def test_as6_coefficient_has_four_pi_as_its_conditional_fixed_point() -> None:
    ledger = reciprocal_coupling_ledger(3, 16 * sp.pi**2)
    assert ledger.positive_fixed_point == 4 * sp.pi
    assert ledger.fixed_point_residual == 0


def test_coefficient_mutation_changes_the_fixed_coordinate() -> None:
    baseline = reciprocal_coupling_ledger(2, 16 * sp.pi**2)
    mutation = reciprocal_coupling_ledger(2, 25 * sp.pi**2)
    assert baseline.positive_fixed_point == 4 * sp.pi
    assert mutation.positive_fixed_point == 5 * sp.pi
    assert mutation.positive_fixed_point != baseline.positive_fixed_point


def test_any_positive_target_can_be_encoded_as_a_fixed_point() -> None:
    target = sp.symbols("target", positive=True)
    coefficient = reciprocal_coefficient_for_fixed_target(target)
    ledger = reciprocal_coupling_ledger(target, coefficient)
    assert coefficient == target**2
    assert ledger.positive_fixed_point == target
    assert ledger.dual_coordinate == target


def test_generic_off_fixed_coordinate_is_still_a_valid_dual_pair() -> None:
    ledger = reciprocal_coupling_ledger(2, 9)
    assert ledger.dual_coordinate == sp.Rational(9, 2)
    assert ledger.double_dual_coordinate == 2
    assert ledger.positive_fixed_point == 3
    assert ledger.coupling_coordinate != ledger.positive_fixed_point


def test_coordinate_change_conjugates_the_map_and_rescales_coefficient() -> None:
    x, coefficient, rho = sp.symbols("x A rho", positive=True)
    ledger = reciprocal_coordinate_change_ledger(x, coefficient, rho)
    assert ledger.rescaled_coordinate == rho * x
    assert ledger.rescaled_duality_coefficient == rho**2 * coefficient
    assert ledger.rescaled_dual_coordinate == rho * coefficient / x
    assert (
        ledger.rescaled_dual_coordinate
        == ledger.conjugated_dual_coordinate
    )
    assert (
        ledger.rescaled_positive_fixed_point
        == ledger.conjugated_positive_fixed_point
    )
    assert ledger.coefficient_rescaling_ratio == rho**2
    assert ledger.fixed_point_rescaling_ratio == rho


def test_holding_coefficient_fixed_is_not_the_coordinate_conjugation() -> None:
    x, coefficient, rho = sp.symbols("x A rho", positive=True)
    ledger = reciprocal_coordinate_change_ledger(x, coefficient, rho)
    wrong_dual = sp.simplify(coefficient / ledger.rescaled_coordinate)
    assert sp.simplify(
        ledger.rescaled_dual_coordinate - wrong_dual
    ) != 0


def test_canonical_coupling_duality_uses_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/coupling_duality.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source


@pytest.mark.parametrize(
    "call",
    [
        lambda: reciprocal_coupling_ledger(0, 1),
        lambda: reciprocal_coupling_ledger(1, 0),
        lambda: reciprocal_coupling_ledger(sp.Symbol("unknown"), 1),
        lambda: reciprocal_coupling_ledger(
            1, sp.Symbol("negative", negative=True)
        ),
        lambda: reciprocal_coefficient_for_fixed_target(-1),
        lambda: reciprocal_coordinate_change_ledger(1, 1, 0),
    ],
)
def test_reciprocal_ledgers_require_explicitly_positive_inputs(call) -> None:
    with pytest.raises(ValueError, match="positive"):
        call()
