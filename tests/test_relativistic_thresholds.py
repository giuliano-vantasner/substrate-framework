from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.relativistic_thresholds import (
    TwoBodyThresholdLedger,
    two_body_threshold_ledger,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility


def test_symbolic_threshold_ledger_closes_and_derives_mass_shell_defect() -> None:
    mass1, mass2 = sp.symbols("m1 m2", positive=True)
    rapidity = sp.symbols("theta", real=True)
    ledger = two_body_threshold_ledger(mass1, mass2, rapidity)

    assert isinstance(ledger, TwoBodyThresholdLedger)
    assert ledger.threshold_four_momentum == sp.ImmutableMatrix((mass1 + mass2, 0))
    assert ledger.observed_four_momentum == sp.ImmutableMatrix(
        (mass1 * sp.cosh(rapidity), mass1 * sp.sinh(rapidity))
    )
    assert ledger.residual_four_momentum == sp.ImmutableMatrix(
        (
            mass1 + mass2 - mass1 * sp.cosh(rapidity),
            -mass1 * sp.sinh(rapidity),
        )
    )
    assert ledger.observed_mass_shell_residual == 0
    assert ledger.four_momentum_closure == sp.zeros(2, 1)
    assert sp.simplify(
        ledger.residual_mass_shell_defect
        - 2 * mass1 * (mass1 + mass2) * (1 - sp.cosh(rapidity))
    ) == 0


def test_zero_rapidity_is_the_two_particle_threshold_configuration() -> None:
    ledger = two_body_threshold_ledger(8, 8, 0)
    assert ledger.observed_four_momentum == sp.ImmutableMatrix((8, 0))
    assert ledger.residual_four_momentum == sp.ImmutableMatrix((8, 0))
    assert ledger.residual_invariant_mass_squared == 64
    assert ledger.residual_mass_shell_defect == 0


def test_nonzero_exact_rapidity_breaks_the_second_mass_shell() -> None:
    ledger = two_body_threshold_ledger(8, 8, sp.log(2))
    observed = ledger.observed_four_momentum.applyfunc(
        lambda value: sp.simplify(value.rewrite(sp.exp))
    )
    residual = ledger.residual_four_momentum.applyfunc(
        lambda value: sp.simplify(value.rewrite(sp.exp))
    )
    assert observed == sp.ImmutableMatrix((10, 6))
    assert residual == sp.ImmutableMatrix((6, -6))
    assert sp.simplify(ledger.residual_invariant_mass_squared.rewrite(sp.exp)) == 0
    assert sp.simplify(ledger.residual_mass_shell_defect.rewrite(sp.exp)) == -64
    assert residual[0] < 8


def test_unequal_masses_have_the_same_zero_recoil_equality_condition() -> None:
    ledger = two_body_threshold_ledger(3, 5, sp.log(2))
    observed = ledger.observed_four_momentum.applyfunc(
        lambda value: sp.simplify(value.rewrite(sp.exp))
    )
    assert observed == sp.ImmutableMatrix(
        (sp.Rational(15, 4), sp.Rational(9, 4))
    )
    defect = sp.simplify(ledger.residual_mass_shell_defect.rewrite(sp.exp))
    assert defect == -12
    assert defect < 0


def test_momentum_sign_mutation_does_not_repair_the_energy_mass_shell() -> None:
    ledger = two_body_threshold_ledger(8, 8, sp.log(2))
    wrong_same_sign_momentum = -ledger.residual_four_momentum[1]
    wrong_invariant = (
        ledger.residual_four_momentum[0] ** 2 - wrong_same_sign_momentum**2
    )
    assert wrong_invariant == ledger.residual_invariant_mass_squared
    assert wrong_invariant != ledger.residual_target_mass**2


def test_above_threshold_energy_is_a_load_bearing_missing_premise() -> None:
    ledger = two_body_threshold_ledger(8, 8, sp.log(2))
    observed_energy, observed_momentum = ledger.observed_four_momentum
    hidden_on_shell_energy = sp.sqrt(8**2 + observed_momentum**2)
    required_total_energy = sp.simplify(observed_energy + hidden_on_shell_energy)
    assert required_total_energy == 20
    assert required_total_energy > ledger.threshold_four_momentum[0]


@pytest.mark.parametrize(
    "call",
    [
        lambda: two_body_threshold_ledger(0, 1, 0),
        lambda: two_body_threshold_ledger(1, -1, 0),
        lambda: two_body_threshold_ledger(sp.Symbol("m"), 1, 0),
        lambda: two_body_threshold_ledger(1.0, 1, 0),
        lambda: two_body_threshold_ledger(1, 1, 0.25),
        lambda: two_body_threshold_ledger(1, 1, sp.Symbol("theta")),
    ],
)
def test_threshold_ledger_requires_exact_explicit_domains(call) -> None:
    with pytest.raises(ValueError, match="positive|exact|real"):
        call()


def test_threshold_module_has_no_numpy_integration_compatibility_shape() -> None:
    path = Path("src/substrate_framework/relativistic_thresholds.py")
    audit = audit_numpy_trapezoid_compatibility(
        path.read_text(encoding="utf-8"), filename=str(path)
    )
    assert audit.legacy_references == 0
    assert audit.current_references == 0
    assert audit.eager_legacy_default_fallbacks == 0
