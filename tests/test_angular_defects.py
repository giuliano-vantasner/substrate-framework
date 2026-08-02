from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.angular_defects import (
    annular_angular_energy,
    equal_split_shell_ledger,
    full_polar_deck_transformation,
    full_polar_loop_class,
    half_quantum_pair_ledger,
    polar_topology_ledger,
    projective_rp2_loop_class,
)


def test_annular_uniform_winding_energy_has_exact_log_normalization() -> None:
    assert annular_angular_energy(3, sp.Rational(1, 2), 1, 16) == 3 * sp.pi * sp.log(2)
    assert annular_angular_energy(2, 1, 1, sp.E) == 2 * sp.pi


def test_fixed_charge_split_retains_a_common_far_field() -> None:
    result = equal_split_shell_ledger(1, 1, 2, 1, 4, 16)
    assert result.near_energy == sp.pi * sp.log(2)
    assert sp.simplify(result.far_energy - 2 * sp.pi * sp.log(2)) == 0
    assert sp.simplify(result.unsplit_field_energy - 4 * sp.pi * sp.log(2)) == 0
    assert result.field_energy_ratio == sp.Rational(3, 4)
    assert result.independent_copy_ratio == sp.Rational(1, 2)


def test_independent_copy_ratio_occurs_only_when_the_far_shell_vanishes() -> None:
    coincident = equal_split_shell_ledger(1, 1, 2, 1, 1, 16)
    boundary_separated = equal_split_shell_ledger(1, 1, 2, 1, 16, 16)
    assert coincident.field_energy_ratio == 1
    assert boundary_separated.field_energy_ratio == sp.Rational(1, 2)
    assert coincident.far_energy == coincident.unsplit_field_energy
    assert boundary_separated.far_energy == 0


def test_core_energies_can_reverse_the_split_preference() -> None:
    no_core = equal_split_shell_ledger(1, 1, 2, 1, 4, 16)
    costly_halves = equal_split_shell_ledger(
        1, 1, 2, 1, 4, 16, piece_core_energy=sp.pi, unsplit_core_energy=0
    )
    assert no_core.split_minus_unsplit < 0
    assert costly_halves.split_minus_unsplit > 0


def test_projective_and_full_polar_generator_squares_are_distinct() -> None:
    topology = polar_topology_ledger()
    assert topology.projective_fundamental_group == "Z2"
    assert topology.full_polar_fundamental_group == "Z"
    assert projective_rp2_loop_class(1) == 1
    assert projective_rp2_loop_class(2) == 0
    assert full_polar_loop_class(1) == 1
    assert full_polar_loop_class(2) == 2
    first = full_polar_deck_transformation(1)
    second = full_polar_deck_transformation(2)
    assert first.director_sign == -1 and first.phase_shift == sp.pi
    assert second.director_sign == 1 and second.phase_shift == 2 * sp.pi


def test_half_pair_ratio_depends_on_director_stiffness_and_cores() -> None:
    equal = half_quantum_pair_ledger(1, 1, 1, sp.E)
    softer_director = half_quantum_pair_ledger(1, sp.Rational(1, 2), 1, sp.E)
    core_reversed = half_quantum_pair_ledger(
        1,
        sp.Rational(1, 2),
        1,
        sp.E,
        half_core_energy=sp.pi,
        integer_core_energy=0,
    )
    assert equal.zero_core_field_ratio == 1
    assert equal.pair_minus_integer == 0
    assert softer_director.zero_core_field_ratio == sp.Rational(3, 4)
    assert softer_director.pair_minus_integer < 0
    assert core_reversed.pair_minus_integer > 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: annular_angular_energy(0, 1, 1, 2), "positive"),
        (lambda: annular_angular_energy(1, sp.I, 1, 2), "real"),
        (lambda: annular_angular_energy(1, 1, 2, 1), "greater"),
        (lambda: equal_split_shell_ledger(1, 1, 0, 1, 2, 4), "positive concrete"),
        (lambda: equal_split_shell_ledger(1, 1, 2, 1, 5, 4), "must not exceed"),
        (
            lambda: equal_split_shell_ledger(1, 1, 2, 1, 2, 4, piece_core_energy=-1),
            "nonnegative",
        ),
        (lambda: full_polar_deck_transformation(sp.Rational(1, 2)), "integer"),
        (lambda: half_quantum_pair_ledger(1, 0, 1, 2), "positive"),
    ],
)
def test_angular_defect_api_rejects_untyped_or_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
