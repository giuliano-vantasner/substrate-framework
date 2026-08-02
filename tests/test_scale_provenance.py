from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.scale_provenance import (
    one_loop_scale_provenance_ledger,
    reference_energy_for_target_inverse_length,
    reference_energy_for_target_transmuted_energy,
    speed_action_length_dimension_ledger,
    unit_coordinate_ledger,
)


def test_speed_and_action_do_not_span_a_length_target() -> None:
    ledger = speed_action_length_dimension_ledger()
    assert ledger.base_dimensions == ("M", "L", "T")
    assert ledger.primitive_names == ("c", "hbar")
    assert ledger.primitive_dimension_matrix == sp.Matrix(
        [[0, 1], [1, 2], [-1, -1]]
    )
    assert ledger.length_target == sp.Matrix([0, 1, 0])
    assert ledger.without_length.coefficient_rank == 2
    assert ledger.without_length.augmented_rank == 3
    assert not ledger.without_length.consistent


def test_adjoining_the_length_target_only_selects_that_primitive() -> None:
    ledger = speed_action_length_dimension_ledger()
    assert ledger.with_length_primitive_names == ("c", "hbar", "a")
    assert ledger.with_length_dimension_matrix == sp.Matrix(
        [[0, 1, 0], [1, 2, 1], [-1, -1, 0]]
    )
    assert ledger.with_length.consistent and ledger.with_length.unique
    assert ledger.with_length_exponents == sp.Matrix([0, 0, 1])


def test_wrong_row_column_convention_is_exposed() -> None:
    ledger = speed_action_length_dimension_ledger()
    source_rows = ledger.with_length_dimension_matrix.T
    assert source_rows.rank() == ledger.with_length_dimension_matrix.rank()
    assert source_rows.shape == (3, 3)
    assert source_rows != ledger.with_length_dimension_matrix
    assert source_rows[0, :] == sp.Matrix([[0, 1, -1]])


def test_reference_rescaling_changes_absolute_scale_and_inverse_length() -> None:
    mu0, g2, b0, conversion, rho = sp.symbols(
        "mu0 g2 b0 K rho", positive=True
    )
    ledger = one_loop_scale_provenance_ledger(
        mu0,
        g2,
        b0,
        conversion=conversion,
        reference_rescaling=rho,
    )
    exponent = 8 * sp.pi**2 / (b0 * g2)
    assert ledger.transmuted_energy == mu0 * sp.exp(-exponent)
    assert ledger.inverse_energy_length == conversion * sp.exp(exponent) / mu0
    assert ledger.transmuted_to_reference_energy_ratio == sp.exp(-exponent)
    assert ledger.transmuted_energy_rescaling_ratio == rho
    assert ledger.inverse_length_rescaling_ratio == 1 / rho


def test_reference_and_beta_inputs_are_load_bearing() -> None:
    mu0, g2, b0, conversion = sp.symbols("mu0 g2 b0 K", positive=True)
    ledger = one_loop_scale_provenance_ledger(
        mu0, g2, b0, conversion=conversion, reference_rescaling=2
    )
    assert sp.diff(ledger.transmuted_energy, mu0) != 0
    assert sp.diff(ledger.transmuted_energy, g2) != 0
    assert sp.diff(ledger.transmuted_energy, b0) != 0
    assert sp.diff(ledger.inverse_energy_length, conversion) != 0


def test_arbitrary_transmuted_energy_target_round_trips() -> None:
    target, g2, b0 = sp.symbols("Lambda_target g2 b0", positive=True)
    mu0 = reference_energy_for_target_transmuted_energy(target, g2, b0)
    ledger = one_loop_scale_provenance_ledger(
        mu0, g2, b0, conversion=1, reference_rescaling=2
    )
    assert sp.simplify(ledger.transmuted_energy - target) == 0
    assert mu0.has(target)


def test_arbitrary_inverse_length_target_round_trips() -> None:
    target, g2, b0, conversion = sp.symbols("a_target g2 b0 K", positive=True)
    mu0 = reference_energy_for_target_inverse_length(
        target, g2, b0, conversion=conversion
    )
    ledger = one_loop_scale_provenance_ledger(
        mu0,
        g2,
        b0,
        conversion=conversion,
        reference_rescaling=2,
    )
    assert sp.simplify(ledger.inverse_energy_length - target) == 0
    assert mu0.has(target)


def test_inverse_energy_orientation_rejects_source_reciprocal() -> None:
    ledger = one_loop_scale_provenance_ledger(
        1, 2, 3, conversion=1, reference_rescaling=2
    )
    assert ledger.transmuted_to_reference_energy_ratio < 1
    assert ledger.inverse_energy_length > 1
    assert (
        ledger.inverse_energy_length
        != ledger.transmuted_to_reference_energy_ratio
    )


def test_unit_rescaling_changes_only_the_numeric_coordinate() -> None:
    quantity, unit, rho = sp.symbols("Q u rho", positive=True)
    ledger = unit_coordinate_ledger(quantity, unit, rho)
    assert ledger.coordinate == quantity / unit
    assert ledger.rescaled_unit_standard == rho * unit
    assert ledger.rescaled_coordinate == quantity / (rho * unit)
    assert ledger.coordinate_rescaling_ratio == 1 / rho
    assert sp.simplify(
        ledger.coordinate * ledger.unit_standard - ledger.quantity
    ) == 0
    assert sp.simplify(
        ledger.rescaled_coordinate * ledger.rescaled_unit_standard
        - ledger.quantity
    ) == 0


def test_canonical_scale_provenance_has_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/scale_provenance.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: one_loop_scale_provenance_ledger(
                0, 1, 1, conversion=1, reference_rescaling=1
            ),
            "positive",
        ),
        (
            lambda: one_loop_scale_provenance_ledger(
                1, 1, 1, conversion=0, reference_rescaling=1
            ),
            "positive",
        ),
        (
            lambda: one_loop_scale_provenance_ledger(
                1, 1, 1, conversion=1, reference_rescaling=0
            ),
            "positive",
        ),
        (
            lambda: reference_energy_for_target_transmuted_energy(0, 1, 1),
            "positive",
        ),
        (
            lambda: reference_energy_for_target_inverse_length(
                1, 1, 1, conversion=-1
            ),
            "positive",
        ),
        (lambda: unit_coordinate_ledger(1, 0, 1), "positive"),
    ],
)
def test_scale_provenance_rejects_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
