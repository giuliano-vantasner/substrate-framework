"""Exact scope-limited tests for standard Lorentz stabilizer algebras."""

from __future__ import annotations

import sympy as sp

from substrate_framework.lorentz_little_groups import (
    little_group_algebra_2plus1,
    little_group_algebra_3plus1,
)


def _commutator(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right - right * left


def test_2plus1_stabilizers_and_null_rotation_are_exact() -> None:
    ledger = little_group_algebra_2plus1()
    (rotation,) = ledger.massive_generators
    (null_rotation,) = ledger.massless_generators

    assert rotation * ledger.standard_massive_momentum == sp.zeros(3, 1)
    assert null_rotation * ledger.standard_null_momentum == sp.zeros(3, 1)
    assert all(
        boost * ledger.standard_massive_momentum != sp.zeros(3, 1)
        for boost in ledger.nonstabilizing_boosts
    )

    mutated = ledger.nonstabilizing_boosts[1] - rotation
    assert mutated * ledger.standard_null_momentum != sp.zeros(3, 1)


def test_3plus1_massive_so3_and_massless_iso2_commutators() -> None:
    ledger = little_group_algebra_3plus1()
    j1, j2, j3 = ledger.massive_generators
    t1, t2, null_j3 = ledger.massless_generators

    assert _commutator(j1, j2) == -j3
    assert _commutator(j2, j3) == -j1
    assert _commutator(j3, j1) == -j2
    assert null_j3 == j3
    assert _commutator(t1, t2) == sp.zeros(4)
    assert _commutator(j3, t1) == -t2
    assert _commutator(j3, t2) == t1

    wrong_t1 = ledger.nonstabilizing_boosts[0] - j2
    assert wrong_t1 * ledger.standard_null_momentum != sp.zeros(4, 1)


def test_ledgers_do_not_encode_representation_classification() -> None:
    fields = set(little_group_algebra_3plus1().__dataclass_fields__)

    assert fields.isdisjoint(
        {"helicity", "spin", "anyon", "continuous_spin", "parity"}
    )
