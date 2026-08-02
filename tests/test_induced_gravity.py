from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

import substrate_framework as framework
from substrate_framework.induced_gravity import (
    cutoff_length_from_pure_induced_newton,
    effective_newton_from_inverse,
    gravity_source_normalization_ledger,
    induced_inverse_newton_ledger,
    induced_scaling_log_constraint,
    induced_scaling_null_rescaling,
    newton_dimension_ledger,
    normalized_gravity_source_coupling,
)


def test_induced_gravity_api_is_exported_from_package() -> None:
    assert framework.newton_dimension_ledger is newton_dimension_ledger
    assert framework.induced_inverse_newton_ledger is induced_inverse_newton_ledger
    assert framework.induced_scaling_log_constraint is induced_scaling_log_constraint
    assert (
        framework.gravity_source_normalization_ledger
        is gravity_source_normalization_ledger
    )


def test_newton_dimension_ledger_uses_declared_mlt_rows_and_ach_columns() -> None:
    ledger = newton_dimension_ledger()
    assert ledger.dimension_matrix == sp.Matrix(
        [[0, 0, 1], [1, 1, 2], [0, -1, -1]]
    )
    assert ledger.newton_dimension == sp.Matrix([-1, 3, -2])
    assert ledger.inverse_newton_dimension == sp.Matrix([1, -3, 2])


def test_newton_and_inverse_newton_monomial_powers_are_unique() -> None:
    ledger = newton_dimension_ledger()
    assert ledger.dimension_matrix.rank() == 3
    assert ledger.newton_exponents == sp.Matrix([2, 3, -1])
    assert ledger.inverse_newton_exponents == sp.Matrix([-2, -3, 1])
    assert ledger.dimension_matrix * ledger.newton_exponents == ledger.newton_dimension
    assert (
        ledger.dimension_matrix * ledger.inverse_newton_exponents
        == ledger.inverse_newton_dimension
    )


def test_newton_is_not_length_squared_times_a_dimensionless_number_in_mlt() -> None:
    ledger = newton_dimension_ledger()
    length_squared = sp.Matrix([0, 2, 0])
    assert ledger.newton_dimension - length_squared == sp.Matrix([-1, 1, -2])
    assert ledger.newton_dimension - length_squared != sp.zeros(3, 1)


def test_declared_induced_shift_and_cutoff_energy_forms_are_exactly_equal() -> None:
    a, s, c, hbar = sp.symbols("a s c hbar", positive=True)
    ledger = induced_inverse_newton_ledger(a, s, c, hbar)
    assert ledger.cutoff_energy == hbar * c / a
    assert ledger.induced_inverse_newton == s * hbar / (a**2 * c**3)
    assert sp.simplify(
        ledger.induced_inverse_newton
        - s * ledger.cutoff_energy**2 / (hbar * c**5)
    ) == 0
    assert ledger.pure_induced_newton == a**2 * c**3 / (hbar * s)


def test_dimensionless_induced_coefficient_remains_load_bearing() -> None:
    a, s, c, hbar = sp.symbols("a s c hbar", positive=True)
    newton = induced_inverse_newton_ledger(a, s, c, hbar).pure_induced_newton
    assert newton.has(s)
    assert sp.diff(newton, s) != 0
    assert sp.simplify(newton.subs(s, 2) / newton.subs(s, 1) - sp.Rational(1, 2)) == 0


def test_independent_baseline_adds_in_inverse_coupling_space() -> None:
    a, s, c, hbar, baseline = sp.symbols(
        "a s c hbar baseline", positive=True
    )
    ledger = induced_inverse_newton_ledger(
        a,
        s,
        c,
        hbar,
        baseline_inverse_newton=baseline,
    )
    assert ledger.total_inverse_newton == baseline + s * hbar / (a**2 * c**3)
    assert sp.diff(ledger.total_inverse_newton, baseline) == 1


def test_baseline_counterfamily_can_produce_any_supplied_total_inverse() -> None:
    a, s, c, hbar, target = sp.symbols("a s c hbar target", positive=True)
    shift = s * hbar / (a**2 * c**3)
    ledger = induced_inverse_newton_ledger(
        a,
        s,
        c,
        hbar,
        baseline_inverse_newton=target - shift,
    )
    assert ledger.total_inverse_newton == target
    assert effective_newton_from_inverse(ledger.total_inverse_newton) == 1 / target


def test_exact_cancellation_makes_effective_newton_inverse_invalid() -> None:
    shift = induced_inverse_newton_ledger(2, 3, 5, 7).induced_inverse_newton
    ledger = induced_inverse_newton_ledger(
        2,
        3,
        5,
        7,
        baseline_inverse_newton=-shift,
    )
    assert ledger.total_inverse_newton == 0
    with pytest.raises(ValueError, match="positive"):
        effective_newton_from_inverse(ledger.total_inverse_newton)


def test_induced_coefficient_sign_is_a_premise_not_a_dimension_result() -> None:
    positive = induced_inverse_newton_ledger(2, 1, 3, 5)
    negative = induced_inverse_newton_ledger(2, -1, 3, 5)
    assert positive.induced_inverse_newton > 0
    assert negative.induced_inverse_newton < 0
    assert negative.induced_inverse_newton == -positive.induced_inverse_newton


def test_cutoff_length_inverse_round_trips_only_after_supplying_coefficient() -> None:
    a, s, c, hbar, supplied_newton = sp.symbols(
        "a s c hbar supplied_newton", positive=True
    )
    independent_inverse = cutoff_length_from_pure_induced_newton(
        supplied_newton,
        s,
        c,
        hbar,
    )
    assert independent_inverse.has(s, supplied_newton)
    newton = induced_inverse_newton_ledger(a, s, c, hbar).pure_induced_newton
    inferred = cutoff_length_from_pure_induced_newton(newton, s, c, hbar)
    assert sp.refine(inferred, sp.Q.positive(a)) == a


def test_as3_log_row_leaves_a_coefficient_null_direction() -> None:
    ratio = sp.symbols("R", positive=True)
    system = induced_scaling_log_constraint(ratio, provenance="declared pure scaling")
    assert system.design == sp.Matrix([[2, -1]])
    assert system.rhs == sp.Matrix([sp.log(ratio)])
    assert system.linear.coefficient_rank == 1
    assert system.linear.solution_dimension == 1
    assert len(system.nullspace) == 1
    assert system.design * system.nullspace[0] == sp.zeros(1, 1)
    assert 2 * system.nullspace[0] == sp.Matrix([1, 2])
    assert system.coordinate_identifiable == (False, False)


def test_null_rescaling_changes_a_and_s_but_preserves_the_newton_ratio() -> None:
    a_ratio, s_ratio, rho = sp.symbols("a_ratio s_ratio rho", positive=True)
    changed_a, changed_s, invariant = induced_scaling_null_rescaling(
        a_ratio,
        s_ratio,
        rho,
    )
    assert invariant == a_ratio**2 / s_ratio
    assert sp.simplify(changed_a**2 / changed_s - invariant) == 0
    assert changed_a != a_ratio and changed_s != s_ratio


def test_mass_density_source_requires_a_c_inverse_squared_normalization() -> None:
    operator_dimension = [0, -2, 0]
    mass_density_dimension = [1, -3, 0]
    ledger = gravity_source_normalization_ledger(
        operator_dimension,
        mass_density_dimension,
    )
    assert ledger.required_coupling_dimension == sp.Matrix([-1, 1, 0])
    assert ledger.normalization_dimension == sp.Matrix([0, -2, 2])
    assert not ledger.dimensionless_normalization_allowed


def test_energy_density_source_requires_a_c_inverse_fourth_normalization() -> None:
    operator_dimension = [0, -2, 0]
    energy_density_dimension = [1, -1, -2]
    ledger = gravity_source_normalization_ledger(
        operator_dimension,
        energy_density_dimension,
    )
    assert ledger.required_coupling_dimension == sp.Matrix([-1, -1, 2])
    assert ledger.normalization_dimension == sp.Matrix([0, -4, 4])
    assert not ledger.dimensionless_normalization_allowed


def test_dimensionless_newton_normalization_requires_matching_source_units() -> None:
    operator_dimension = sp.Matrix([0, -2, 0])
    newton_dimension = newton_dimension_ledger().newton_dimension
    compatible_source = operator_dimension - newton_dimension
    ledger = gravity_source_normalization_ledger(
        operator_dimension,
        compatible_source,
    )
    assert ledger.required_coupling_dimension == newton_dimension
    assert ledger.normalization_dimension == sp.zeros(3, 1)
    assert ledger.dimensionless_normalization_allowed


def test_source_coupling_keeps_normalization_factor_explicit() -> None:
    newton, c = sp.symbols("G c", positive=True)
    coupling = normalized_gravity_source_coupling(newton, 8 * sp.pi / c**2)
    assert coupling == 8 * sp.pi * newton / c**2
    assert coupling.has(c)


def test_pure_induced_limits_do_not_select_a_physical_scale() -> None:
    a, s = sp.symbols("a s", positive=True)
    newton = induced_inverse_newton_ledger(a, s, 1, 1).pure_induced_newton
    assert sp.limit(newton, a, 0, dir="+") == 0
    assert sp.limit(newton, a, sp.oo) == sp.oo
    assert sp.limit(newton, s, 0, dir="+") == sp.oo
    assert sp.limit(newton, s, sp.oo) == 0


def test_canonical_induced_gravity_module_has_no_numpy_quadrature_alias() -> None:
    source = Path("src/substrate_framework/induced_gravity.py").read_text(
        encoding="utf-8"
    )
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: induced_inverse_newton_ledger(0, 1, 1, 1), "positive"),
        (lambda: induced_inverse_newton_ledger(1, 0, 1, 1), "nonzero"),
        (lambda: induced_inverse_newton_ledger(1, 1, -1, 1), "positive"),
        (lambda: induced_inverse_newton_ledger(1, 1, 1, 0), "positive"),
        (lambda: effective_newton_from_inverse(-1), "positive"),
        (lambda: cutoff_length_from_pure_induced_newton(0, 1, 1, 1), "positive"),
        (lambda: induced_scaling_log_constraint(0, provenance="x"), "positive"),
        (lambda: induced_scaling_log_constraint(1, provenance=""), "non-empty"),
        (lambda: induced_scaling_null_rescaling(1, 1, 0), "positive"),
        (lambda: gravity_source_normalization_ledger([1, 2], [1, 2, 3]), "M,L,T"),
        (lambda: normalized_gravity_source_coupling(0, 1), "positive"),
        (lambda: normalized_gravity_source_coupling(1, sp.I), "real"),
    ],
)
def test_induced_gravity_api_rejects_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
