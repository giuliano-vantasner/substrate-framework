from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.retarded_wave import (
    retarded_point_source_radiation,
    static_point_source_countermodel,
)


def test_retarded_solution_reproduces_delta_source_and_outgoing_characteristics() -> None:
    A, B, c, q = sp.symbols("A B c q", positive=True)
    result = retarded_point_source_radiation(A, B, c, q)
    assert result.equation_delta_coefficient == B * q / A
    assert result.field_primitive_coefficient == B / (2 * A * c)
    assert result.derivative_jump == -B * q / (A * c**2)
    assert sp.simplify(result.time_derivative + c * result.right_space_derivative) == 0
    assert sp.simplify(result.time_derivative - c * result.left_space_derivative) == 0


def test_two_sided_flux_equals_local_source_work() -> None:
    A, B, c, q = sp.symbols("A B c q", positive=True)
    result = retarded_point_source_radiation(A, B, c, q)
    one_side = B**2 * q**2 / (4 * A * c)
    assert result.right_outward_flux == one_side
    assert result.left_outward_flux == one_side
    assert result.total_outward_power == B**2 * q**2 / (2 * A * c)
    assert result.source_work_rate == result.total_outward_power


def test_source_sign_changes_field_but_not_power_and_zero_source_is_quiet() -> None:
    positive = retarded_point_source_radiation(3, 2, 5, 7)
    negative = retarded_point_source_radiation(3, -2, 5, 7)
    zero = retarded_point_source_radiation(3, 2, 5, 0)
    assert negative.time_derivative == -positive.time_derivative
    assert negative.derivative_jump == -positive.derivative_jump
    assert negative.total_outward_power == positive.total_outward_power
    assert zero.time_derivative == 0
    assert zero.total_outward_power == 0


def test_field_rescaling_preserves_equation_and_physical_power() -> None:
    A, B, c, q, scale = sp.symbols("A B c q s", positive=True)
    baseline = retarded_point_source_radiation(A, B, c, q)
    rescaled = retarded_point_source_radiation(A / scale**2, B / scale, c, q)
    assert sp.simplify(rescaled.time_derivative - scale * baseline.time_derivative) == 0
    assert sp.simplify(rescaled.total_outward_power - baseline.total_outward_power) == 0


def test_static_countermodel_has_same_source_jump_but_no_flux() -> None:
    A, B, c, q = sp.symbols("A B c q", positive=True)
    retarded = retarded_point_source_radiation(A, B, c, q)
    static = static_point_source_countermodel(A, B, c, q)
    assert static.equation_delta_coefficient == retarded.equation_delta_coefficient
    assert static.derivative_jump == retarded.derivative_jump
    assert static.absolute_value_coefficient == -B * q / (2 * A * c**2)
    assert static.total_outward_power == 0
    assert retarded.total_outward_power != static.total_outward_power


def test_g1_normalization_mutation_exposes_derivative_and_factor_four_errors() -> None:
    kappa, q, qdot = sp.symbols("kappa q qdot", positive=True)
    corrected = retarded_point_source_radiation(1 / kappa, 1, 1, q)
    g1_checked_expression = kappa * qdot**2 / 8
    assert corrected.time_derivative == kappa * q / 2
    assert corrected.total_outward_power == kappa * q**2 / 2
    assert sp.simplify(
        corrected.total_outward_power.subs(q, qdot) / g1_checked_expression
    ) == 4
    assert corrected.total_outward_power.subs(q, 1).subs(qdot, 0) != (
        g1_checked_expression.subs(qdot, 0)
    )


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        ((1.0, 1, 1, 1), "kinetic_coefficient"),
        ((1, 1.0, 1, 1), "source_coupling"),
        ((1, 1, 1.0, 1), "wave_speed"),
        ((1, 1, 1, 1.0), "source_amplitude"),
        ((0, 1, 1, 1), "kinetic_coefficient"),
        ((1, 1, -1, 1), "wave_speed"),
        ((1, sp.Symbol("z"), 1, 1), "source_coupling"),
    ],
)
def test_invalid_or_inexact_inputs_are_rejected(
    arguments: tuple[object, object, object, object], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        retarded_point_source_radiation(*arguments)


def test_static_countermodel_uses_same_input_guards() -> None:
    with pytest.raises(ValueError, match="wave_speed"):
        static_point_source_countermodel(1, 1, 0, 1)
