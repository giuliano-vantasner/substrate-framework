from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.scale_transmutation import (
    common_length_rescaling,
    coupling_squared_from_length_ratio,
    one_loop_inverse_energy_length_ledger,
    two_length_log_constraint,
    two_length_speed_dimension_ledger,
)


def test_two_lengths_and_speed_have_one_ratio_kernel() -> None:
    ledger = two_length_speed_dimension_ledger()
    assert ledger.dimension_matrix == sp.Matrix([[1, 1, 1], [0, 0, -1]])
    assert ledger.rank == 2
    assert ledger.dimensionless_group_count == 1
    assert ledger.monomial_kernel == (sp.ImmutableMatrix([-1, 1, 0]),)
    assert ledger.dimension_matrix * ledger.monomial_kernel[0] == sp.zeros(2, 1)


def test_kernel_orientation_is_not_selected_by_dimensions() -> None:
    kernel = two_length_speed_dimension_ledger().monomial_kernel[0]
    assert kernel == sp.Matrix([-1, 1, 0])
    assert -kernel == sp.Matrix([1, -1, 0])
    assert two_length_speed_dimension_ledger().dimension_matrix * (-kernel) == sp.zeros(2, 1)


def test_one_loop_energy_and_equal_conversion_length_ratios_are_reciprocal() -> None:
    mu0, g2, b0, conversion = sp.symbols("mu0 g2 b0 K", positive=True)
    ledger = one_loop_inverse_energy_length_ledger(
        mu0,
        g2,
        b0,
        reference_conversion=conversion,
        transmuted_conversion=conversion,
    )
    exponent = 8 * sp.pi**2 / (b0 * g2)
    assert ledger.transmuted_energy == mu0 * sp.exp(-exponent)
    assert ledger.transmuted_to_reference_energy_ratio == sp.exp(-exponent)
    assert ledger.reference_length == conversion / mu0
    assert ledger.transmuted_length == conversion * sp.exp(exponent) / mu0
    assert ledger.transmuted_to_reference_length_ratio == sp.exp(exponent)
    assert sp.simplify(
        ledger.transmuted_to_reference_energy_ratio
        * ledger.transmuted_to_reference_length_ratio
        - 1
    ) == 0


def test_unequal_conversion_prefactors_remain_load_bearing() -> None:
    mu0, g2, b0, k0, k1 = sp.symbols("mu0 g2 b0 K0 K1", positive=True)
    ledger = one_loop_inverse_energy_length_ledger(
        mu0,
        g2,
        b0,
        reference_conversion=k0,
        transmuted_conversion=k1,
    )
    expected = k1 * sp.exp(8 * sp.pi**2 / (b0 * g2)) / k0
    assert ledger.transmuted_to_reference_length_ratio == expected
    assert sp.simplify(
        ledger.transmuted_to_reference_energy_ratio
        * ledger.transmuted_to_reference_length_ratio
        - k1 / k0
    ) == 0


def test_reference_energy_cancels_only_from_ratio() -> None:
    first = one_loop_inverse_energy_length_ledger(2, 3, 5)
    second = one_loop_inverse_energy_length_ledger(7, 3, 5)
    assert first.transmuted_to_reference_length_ratio == second.transmuted_to_reference_length_ratio
    assert first.reference_length != second.reference_length
    assert first.transmuted_length != second.transmuted_length


def test_source_opening_uv_ir_labels_are_incompatible_with_its_code_assignment() -> None:
    ledger = one_loop_inverse_energy_length_ledger(1, 2, 3)
    assert ledger.transmuted_energy < ledger.reference_energy
    assert ledger.transmuted_length > ledger.reference_length
    assert ledger.transmuted_to_reference_length_ratio > 1
    assert ledger.reference_to_transmuted_length_ratio < 1


def test_length_ratio_constraint_identifies_only_relative_coordinate() -> None:
    ratio = sp.symbols("R", positive=True)
    system = two_length_log_constraint(ratio, provenance="declared ratio")
    assert system.design == sp.Matrix([[-1, 1]])
    assert system.rhs == sp.Matrix([sp.log(ratio)])
    assert system.linear.coefficient_rank == 1
    assert system.linear.solution_dimension == 1
    assert system.nullspace == (sp.ImmutableMatrix([1, 1]),)
    assert system.coordinate_identifiable == (False, False)


def test_common_rescaling_leaves_ratio_and_constraint_residual_unchanged() -> None:
    ell0, ell1, rho = sp.symbols("ell0 ell1 rho", positive=True)
    changed0, changed1, ratio = common_length_rescaling(ell0, ell1, rho)
    assert ratio == ell1 / ell0
    assert sp.simplify(changed1 / changed0 - ratio) == 0
    assert sp.expand_log(
        sp.log(changed1) - sp.log(changed0) - sp.log(ell1 / ell0),
        force=True,
    ) == 0


def test_coupling_inverse_is_inference_from_supplied_ratio() -> None:
    ratio, b0 = sp.symbols("R b0", positive=True)
    inferred = coupling_squared_from_length_ratio(ratio, b0)
    assert inferred == 8 * sp.pi**2 / (b0 * sp.log(ratio))
    ledger = one_loop_inverse_energy_length_ledger(1, 3, 5)
    assert sp.simplify(ledger.inferred_coupling_squared - 3) == 0


def test_formal_limits_retain_free_coefficient_and_prefactor() -> None:
    g2 = sp.symbols("g2", positive=True)
    b0, prefactor = sp.symbols("b0 q", positive=True)
    ledger = one_loop_inverse_energy_length_ledger(
        1,
        g2,
        b0,
        transmuted_conversion=prefactor,
    )
    ratio = ledger.transmuted_to_reference_length_ratio
    assert sp.limit(ratio, g2, 0, dir="+") == sp.oo
    assert sp.limit(ratio, g2, sp.oo) == prefactor
    assert ratio.has(b0, g2, prefactor)


def test_wrong_direct_energy_to_length_orientation_fails() -> None:
    ledger = one_loop_inverse_energy_length_ledger(1, 2, 3)
    wrong_direct_ratio = ledger.transmuted_to_reference_energy_ratio
    assert wrong_direct_ratio < 1
    assert ledger.transmuted_to_reference_length_ratio > 1
    assert wrong_direct_ratio != ledger.transmuted_to_reference_length_ratio


def test_canonical_scale_transmutation_module_has_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/scale_transmutation.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: one_loop_inverse_energy_length_ledger(0, 1, 1), "positive"),
        (lambda: one_loop_inverse_energy_length_ledger(1, 0, 1), "positive"),
        (lambda: one_loop_inverse_energy_length_ledger(1, 1, -1), "positive"),
        (
            lambda: one_loop_inverse_energy_length_ledger(
                1, 1, 1, transmuted_conversion=0
            ),
            "positive",
        ),
        (lambda: coupling_squared_from_length_ratio(1, 2), "must exceed"),
        (lambda: coupling_squared_from_length_ratio(2, 0), "positive"),
        (lambda: two_length_log_constraint(0, provenance="x"), "positive"),
        (lambda: two_length_log_constraint(2, provenance=""), "non-empty"),
        (lambda: common_length_rescaling(1, 2, 0), "positive"),
    ],
)
def test_scale_transmutation_api_rejects_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
