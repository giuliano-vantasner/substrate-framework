from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.gravity_scale_confrontation import (
    induced_coefficient_for_target_cutoff,
    inverse_newton_baseline_for_target,
    joint_gravity_transmutation_log_ledger,
    pure_gravity_cutoff_interval,
    solve_joint_with_fixed_coefficient_ratio,
)
from substrate_framework.induced_gravity import induced_inverse_newton_ledger


def test_supplied_coefficient_interval_has_exact_monotone_cutoff_image() -> None:
    ledger = pure_gravity_cutoff_interval(3, 1, 16, 2, 5)
    assert ledger.unit_coefficient_cutoff == sp.sqrt(30) / 4
    assert ledger.cutoff_lower == ledger.unit_coefficient_cutoff
    assert ledger.cutoff_upper == sp.sqrt(30)
    assert ledger.coefficient_interval_width == 15
    assert ledger.cutoff_interval_width == 3 * sp.sqrt(30) / 4


def test_widening_supplied_coefficient_interval_changes_only_its_image() -> None:
    narrow = pure_gravity_cutoff_interval(3, 1, 4, 2, 5)
    wide = pure_gravity_cutoff_interval(3, 1, 25, 2, 5)
    assert narrow.cutoff_lower == wide.cutoff_lower
    assert narrow.cutoff_upper == sp.sqrt(30) / 2
    assert wide.cutoff_upper == 5 * sp.sqrt(30) / 4
    assert wide.cutoff_upper > narrow.cutoff_upper


def test_any_positive_cutoff_target_has_a_pure_branch_coefficient_preimage() -> None:
    target, newton, speed, action = sp.symbols(
        "a_target G c hbar", positive=True
    )
    coefficient = induced_coefficient_for_target_cutoff(
        target, newton, speed, action
    )
    assert coefficient == target**2 * speed**3 / (action * newton)
    reconstructed = induced_inverse_newton_ledger(
        target, coefficient, speed, action
    )
    assert sp.simplify(reconstructed.pure_induced_newton - newton) == 0


def test_additive_baseline_realizes_any_supplied_positive_newton_total() -> None:
    target_newton, cutoff, speed, action = sp.symbols(
        "G_target a c hbar", positive=True
    )
    coefficient = sp.symbols("s", nonzero=True, real=True)
    baseline = inverse_newton_baseline_for_target(
        target_newton, cutoff, coefficient, speed, action
    )
    ledger = induced_inverse_newton_ledger(
        cutoff,
        coefficient,
        speed,
        action,
        baseline_inverse_newton=baseline,
    )
    assert sp.simplify(ledger.total_inverse_newton - 1 / target_newton) == 0


def test_joint_gravity_and_length_rows_have_one_exact_null_direction() -> None:
    ledger = joint_gravity_transmutation_log_ledger(
        sp.exp(2),
        sp.exp(4),
        8 * sp.pi**2,
        gravity_provenance="supplied Newton ratio",
        length_provenance="supplied long-length ratio",
    )
    assert ledger.exponent_coefficient == 1
    assert ledger.system.linear.coefficient_rank == 2
    assert ledger.system.linear.solution_dimension == 1
    assert ledger.system.linear.underdetermined
    assert ledger.system.coordinate_identifiable == (False, False, False)
    assert len(ledger.system.nullspace) == 1
    null_vector = ledger.system.nullspace[0]
    assert ledger.system.design * null_vector == sp.zeros(2, 1)
    assert null_vector == sp.ImmutableMatrix([-1, -2, 1])


def test_fixed_coefficient_row_makes_the_inverse_reconstruction_unique() -> None:
    solution = solve_joint_with_fixed_coefficient_ratio(
        sp.exp(2),
        sp.exp(4),
        1,
        8 * sp.pi**2,
        gravity_provenance="supplied Newton ratio",
        length_provenance="supplied long-length ratio",
        coefficient_provenance="supplied coefficient ratio",
    )
    assert solution.system.linear.coefficient_rank == 3
    assert solution.system.linear.unique
    assert solution.system.coordinate_identifiable == (True, True, True)
    assert solution.log_solution == sp.ImmutableMatrix([1, 0, 3])
    assert solution.cutoff_ratio == sp.E
    assert solution.inverse_coupling_squared == 3
    assert solution.inferred_coupling_squared == sp.Rational(1, 3)
    assert solution.positive_coupling_admissible is True
    assert solution.residuals == (0, 0, 0)


def test_coefficient_and_conversion_mutations_change_the_solved_inputs() -> None:
    base = solve_joint_with_fixed_coefficient_ratio(
        sp.exp(2),
        sp.exp(4),
        1,
        8 * sp.pi**2,
        gravity_provenance="G",
        length_provenance="L",
        coefficient_provenance="s",
    )
    coefficient_mutation = solve_joint_with_fixed_coefficient_ratio(
        sp.exp(2),
        sp.exp(4),
        sp.exp(2),
        8 * sp.pi**2,
        gravity_provenance="G",
        length_provenance="L",
        coefficient_provenance="mutated s",
    )
    conversion_mutation = solve_joint_with_fixed_coefficient_ratio(
        sp.exp(2),
        sp.exp(4),
        1,
        8 * sp.pi**2,
        conversion_ratio=sp.E,
        gravity_provenance="G",
        length_provenance="mutated conversion",
        coefficient_provenance="s",
    )
    assert coefficient_mutation.log_solution == sp.ImmutableMatrix([2, 2, 2])
    assert coefficient_mutation.inferred_coupling_squared == sp.Rational(1, 2)
    assert conversion_mutation.log_solution == sp.ImmutableMatrix([1, 0, 2])
    assert conversion_mutation.inferred_coupling_squared == sp.Rational(1, 2)
    assert base.log_solution != coefficient_mutation.log_solution
    assert base.log_solution != conversion_mutation.log_solution


def test_reversing_the_length_orientation_can_destroy_positive_coupling_domain() -> None:
    reversed_orientation = solve_joint_with_fixed_coefficient_ratio(
        sp.exp(2),
        sp.exp(-4),
        1,
        8 * sp.pi**2,
        gravity_provenance="G",
        length_provenance="reciprocal length mutation",
        coefficient_provenance="s",
    )
    assert reversed_orientation.log_solution == sp.ImmutableMatrix([1, 0, -5])
    assert reversed_orientation.inferred_coupling_squared == -sp.Rational(1, 5)
    assert reversed_orientation.positive_coupling_admissible is False


@pytest.mark.parametrize(
    "call",
    [
        lambda: pure_gravity_cutoff_interval(1, 2, 1, 1, 1),
        lambda: pure_gravity_cutoff_interval(1.0, 1, 2, 1, 1),
        lambda: induced_coefficient_for_target_cutoff(0, 1, 1, 1),
        lambda: inverse_newton_baseline_for_target(1, 1, 0, 1, 1),
        lambda: joint_gravity_transmutation_log_ledger(
            1,
            1,
            1,
            gravity_provenance="",
            length_provenance="L",
        ),
    ],
)
def test_exact_ledgers_reject_unproved_or_invalid_premises(call) -> None:
    with pytest.raises(ValueError):
        call()


def test_exact_confrontation_uses_no_numpy_quadrature_alias() -> None:
    source = Path(
        "src/substrate_framework/gravity_scale_confrontation.py"
    ).read_text(encoding="utf-8")
    assert "np." + "trapz" not in source
    assert "np." + "trapezoid" not in source
