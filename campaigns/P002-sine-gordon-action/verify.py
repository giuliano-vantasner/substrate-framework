#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed claim C-SG-003."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.sine_gordon import (
    breather_action,
    breather_energy,
    breather_energy_from_action,
    breather_frequency_from_action,
    breather_period,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class ActionCandidate:
    """A small candidate family used only to test verifier sensitivity."""

    coefficient: int
    offset: int
    function: str = "acos"


def candidate_expression(candidate: ActionCandidate, omega: sp.Symbol) -> sp.Expr:
    function = {"acos": sp.acos, "asin": sp.asin}[candidate.function]
    return candidate.coefficient * function(omega) + candidate.offset


def satisfies_action_definition(candidate: ActionCandidate) -> bool:
    """Require both the action-angle ODE and the zero-action endpoint."""

    omega = sp.symbols("omega", positive=True)
    trial = candidate_expression(candidate, omega)
    energy = breather_energy(omega)
    differential_identity = sp.simplify(
        sp.diff(trial, omega) * omega - sp.diff(energy, omega)
    )
    endpoint = sp.limit(trial, omega, 1, dir="-")
    return differential_identity == 0 and endpoint == 0


def run() -> int:
    checks = CheckLedger("C-SG-003")
    omega = sp.symbols("omega", positive=True)
    action = sp.symbols("J", positive=True)

    energy = breather_energy(omega)
    period = breather_period(omega)
    required_derivative = sp.simplify(sp.diff(energy, omega) * period / (2 * sp.pi))
    checks.check(
        "accepted energy and period derive dJ/domega = -16/sqrt(1-omega^2)",
        sp.simplify(required_derivative + 16 / sp.sqrt(1 - omega**2)) == 0,
    )

    raw_antiderivative = sp.integrate(required_derivative, omega)
    checks.check(
        "exact calculus integrates the action-angle differential relation",
        sp.simplify(sp.diff(raw_antiderivative, omega) - required_derivative) == 0,
    )
    endpoint_constant = sp.simplify(-sp.limit(raw_antiderivative, omega, 1, dir="-"))
    derived_action = sp.simplify(raw_antiderivative + endpoint_constant)
    checks.check(
        "the vanishing-amplitude endpoint uniquely fixes the additive constant",
        sp.limit(derived_action, omega, 1, dir="-") == 0,
    )
    checks.check(
        "the integrated result equals the canonical action API",
        sp.trigsimp(derived_action.rewrite(sp.acos) - breather_action(omega)) == 0,
        f"derived={derived_action}",
    )

    canonical_action = breather_action(omega)
    checks.check(
        "dJ/dE equals T/(2*pi) exactly",
        sp.simplify(
            sp.diff(canonical_action, omega) / sp.diff(energy, omega)
            - period / (2 * sp.pi)
        )
        == 0,
    )
    checks.check(
        "the energy-action derivative is the breather frequency",
        sp.simplify(sp.diff(energy, omega) / sp.diff(canonical_action, omega) - omega)
        == 0,
    )
    checks.mutation_sensitive(
        "action coefficient, endpoint, and branch",
        satisfies_action_definition,
        ActionCandidate(coefficient=16, offset=0, function="acos"),
        [
            ActionCandidate(coefficient=15, offset=0, function="acos"),
            ActionCandidate(coefficient=16, offset=1, function="acos"),
            ActionCandidate(coefficient=16, offset=0, function="asin"),
        ],
    )

    checks.check(
        "the kink-pair endpoint has action supremum 8*pi",
        sp.limit(canonical_action, omega, 0, dir="+") == 8 * sp.pi,
    )
    checks.check(
        "the harmonic endpoint has zero action",
        sp.limit(canonical_action, omega, 1, dir="-") == 0,
    )
    checks.check(
        "the action decreases strictly across 0 < omega < 1",
        sp.simplify(sp.diff(canonical_action, omega) + 16 / sp.sqrt(1 - omega**2))
        == 0,
    )

    inverse_frequency = breather_frequency_from_action(action)
    action_energy = breather_energy_from_action(action)
    checks.check(
        "the inverse frequency branch is omega = cos(J/16)",
        inverse_frequency == sp.cos(action / 16),
    )
    checks.check(
        "the inverse energy branch is E = 16*sin(J/16)",
        action_energy == 16 * sp.sin(action / 16),
    )
    checks.check(
        "frequency inversion recovers every symbolic breather frequency",
        sp.simplify(breather_frequency_from_action(canonical_action) - omega) == 0,
    )
    checks.check(
        "energy inversion recovers the accepted breather energy",
        sp.simplify(breather_energy_from_action(canonical_action) - energy) == 0,
    )
    checks.check(
        "the inverse energy derivative recovers omega on 0 < J < 8*pi",
        sp.simplify(sp.diff(action_energy, action) - inverse_frequency) == 0,
    )

    total = checks.finish()
    print(f"P002 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
