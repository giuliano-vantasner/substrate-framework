#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed C-SG-005."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.sine_gordon import (
    breather_energy,
    breather_threshold_deficit,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class GapCandidate:
    threshold: int
    energy_coefficient: int
    power_numerator: int
    power_denominator: int


def gap_candidate_is_exact(candidate: GapCandidate) -> bool:
    omega = sp.symbols("omega", positive=True)
    power = sp.Rational(
        candidate.power_numerator, candidate.power_denominator
    )
    candidate_gap = (
        candidate.threshold
        - candidate.energy_coefficient * (1 - omega**2) ** power
    )
    expected_gap = 16 * (1 - sp.sqrt(1 - omega**2))
    return sp.simplify(candidate_gap - expected_gap) == 0


def run() -> int:
    checks = CheckLedger("C-SG-005")
    omega = sp.symbols("omega", positive=True)
    positive_width = sp.symbols("eta", positive=True)
    energy = breather_energy(omega)
    deficit = breather_threshold_deficit(omega)

    checks.check(
        "the threshold deficit has the exact closed form",
        sp.simplify(
            deficit - 16 * (1 - sp.sqrt(1 - omega**2))
        )
        == 0,
    )
    checks.check(
        "breather energy and deficit partition the threshold exactly",
        sp.simplify(energy + deficit - 16) == 0,
    )
    checks.check(
        "rationalization gives an explicitly positive open-domain form",
        sp.simplify(
            deficit
            - 16
            * omega**2
            / (1 + sp.sqrt(1 - omega**2))
        )
        == 0,
    )

    first_derivative = sp.diff(deficit, omega)
    checks.check(
        "the deficit is strictly increasing on 0<omega<1",
        sp.simplify(
            first_derivative
            - 16 * omega / sp.sqrt(1 - omega**2)
        )
        == 0
        and (16 * omega / positive_width).is_positive is True,
    )
    second_derivative = sp.diff(deficit, omega, 2)
    checks.check(
        "the deficit is strictly convex on 0<omega<1",
        sp.simplify(
            second_derivative
            - 16 / (1 - omega**2) ** sp.Rational(3, 2)
        )
        == 0
        and (16 / positive_width**3).is_positive is True,
    )
    checks.check(
        "the threshold-end limit is zero",
        sp.limit(deficit, omega, 0, dir="+") == 0,
    )
    checks.check(
        "the high-frequency endpoint limit is the full threshold",
        sp.limit(deficit, omega, 1, dir="-") == 16,
    )
    checks.check(
        "monotonicity and endpoint limits give the open bound 0<Delta<16",
        sp.limit(deficit, omega, 0, dir="+")
        < sp.limit(deficit, omega, 1, dir="-"),
    )
    checks.mutation_sensitive(
        "threshold, energy coefficient, and square-root power",
        gap_candidate_is_exact,
        GapCandidate(16, 16, 1, 2),
        [
            GapCandidate(8, 16, 1, 2),
            GapCandidate(16, 15, 1, 2),
            GapCandidate(16, 16, 1, 1),
        ],
    )

    total = checks.finish()
    print(f"P009 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
