#!/usr/bin/env python3
"""Template for a mutation-sensitive claim verifier.

Claim:      <claim id and exact statement>
Depends:    <accepted claim ids and canonical imports>
Oracle:     <symbolic_verified | numeric_evidence | simulation_evidence>
Run:        PYTHONPATH=src python3 <this-file>

Keep reusable equations and solvers in ``substrate_framework``. This file should
assemble a candidate and test it, not duplicate canonical implementation.
"""

from __future__ import annotations

from substrate_framework.verification import CheckLedger


def derived_quantity(parameter: float) -> float:
    """Replace with an import from the canonical package."""

    return 2.0 * parameter


def run() -> int:
    checks = CheckLedger("CLAIM-ID")

    result = derived_quantity(3.0)
    checks.check("derived result has expected structural property", result > 0.0)

    checks.mutation_sensitive(
        "normalization-sensitive predicate",
        predicate=lambda value: value == 6.0,
        baseline=result,
        mutations=[derived_quantity(-3.0), result * 1.1],
    )

    # Add units, sign, symmetry, limiting-case, conservation, convergence, and
    # independent-route checks required by the claim. Never use a comparator as
    # the expected value of a first-principles derivation.
    return checks.finish()


if __name__ == "__main__":
    run()
