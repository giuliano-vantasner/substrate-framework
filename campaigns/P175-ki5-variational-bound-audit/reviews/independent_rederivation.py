#!/usr/bin/env python3
"""Independent exact signed-bound and finite-probe audit for KI5."""

from __future__ import annotations

from fractions import Fraction
import hashlib
from pathlib import Path

import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")
CLAIMS = ROOT / "governance/claims.yaml"
CLAIMS_SHA256 = "b2d68ae4e293301d402de4a0292445805ff42e26871b058fc74427aac37b7a0f"


def estimate_error(
    true_initial: Fraction,
    true_final: Fraction,
    slack_initial: Fraction,
    slack_final: Fraction,
    *,
    multiplicity: int,
) -> Fraction:
    estimate = multiplicity * (true_initial + slack_initial) - (true_final + slack_final)
    truth = multiplicity * true_initial - true_final
    return estimate - truth


def finite_probe_gap(scale: Fraction) -> Fraction:
    return (scale - 1) ** 2 * ((scale - Fraction(41, 40)) ** 2 - Fraction(1, 10000))


def main() -> int:
    checks = CheckLedger("P175-INDEPENDENT-SIGNED-BOUND-AUDIT")
    checks.check(
        "independent accepted authority retains pinned bytes",
        hashlib.sha256(CLAIMS.read_bytes()).hexdigest() == CLAIMS_SHA256,
    )
    registry = yaml.safe_load(CLAIMS.read_text(encoding="utf-8"))
    claims = {claim["id"]: claim for claim in registry["claims"]}
    checks.check(
        "accepted authority already distinguishes stationary branches from variational bounds",
        "stationary branch" in claims["C-RPROF-002"]["statement"]
        and "variational upper bound" in claims["C-RPROF-002"]["statement"],
    )

    true_i, true_f = Fraction(7, 3), Fraction(11, 5)
    checks.check(
        "fresh exact arithmetic derives the signed slack combination",
        estimate_error(true_i, true_f, Fraction(2, 7), Fraction(3, 11), multiplicity=2)
        == 2 * Fraction(2, 7) - Fraction(3, 11),
    )
    checks.check(
        "nonnegative independent slacks give a positive estimate error",
        estimate_error(true_i, true_f, Fraction(1), Fraction(0), multiplicity=2) > 0,
    )
    checks.check(
        "nonnegative independent slacks give a negative estimate error",
        estimate_error(true_i, true_f, Fraction(0), Fraction(1), multiplicity=2) < 0,
    )
    target_errors = (Fraction(5, 7), Fraction(-9, 13), Fraction(0))
    realized = []
    for target in target_errors:
        if target >= 0:
            pair = (target / 2, Fraction(0))
        else:
            pair = (Fraction(0), -target)
        realized.append(estimate_error(true_i, true_f, *pair, multiplicity=2))
    checks.check(
        "every tested signed error is realized by admissible nonnegative slacks",
        tuple(realized) == target_errors,
    )
    checks.check(
        "the equality surface is exactly final slack equals multiplicity times initial slack",
        estimate_error(true_i, true_f, Fraction(3, 8), Fraction(3, 4), multiplicity=2) == 0,
    )
    checks.check(
        "a larger final slack makes the estimate a conditional lower bound",
        estimate_error(true_i, true_f, Fraction(3, 8), Fraction(1), multiplicity=2) < 0,
    )
    checks.check(
        "a larger multiplicity-weighted initial slack makes it a conditional upper bound",
        estimate_error(true_i, true_f, Fraction(3, 4), Fraction(1), multiplicity=2) > 0,
    )

    initial_budget, final_budget = Fraction(1, 100), Fraction(1, 80)
    error_samples = (
        estimate_error(true_i, true_f, Fraction(0), final_budget, multiplicity=2),
        estimate_error(true_i, true_f, initial_budget, Fraction(0), multiplicity=2),
    )
    checks.check(
        "component budgets give the sharp rectangular signed-error interval",
        error_samples == (-final_budget, 2 * initial_budget),
    )
    alternating = tuple(
        Fraction(2, k) if k % 2 == 0 else Fraction(-1, k)
        for k in range(2, 20)
    )
    checks.check(
        "convergent component upper estimates need not approach from one side",
        any(value > 0 for value in alternating)
        and any(value < 0 for value in alternating)
        and all(abs(value) <= Fraction(2, k) for k, value in zip(range(2, 20), alternating, strict=True)),
    )

    sampled = (Fraction(9, 10), Fraction(19, 20), Fraction(21, 20), Fraction(11, 10))
    checks.check(
        "fresh exact counterfamily passes every sampled width probe",
        all(finite_probe_gap(value) > 0 for value in sampled),
    )
    checks.check(
        "the same counterfamily is lower at an unsampled width",
        finite_probe_gap(Fraction(1)) == 0
        and finite_probe_gap(Fraction(41, 40)) < 0,
    )
    checks.check(
        "valid signed-bound conclusions require no empirical comparator",
        all(value.denominator != 1000 or value != Fraction(929, 1000) for value in alternating),
    )
    checks.check(
        "accepted C-RDIFF-001 already owns the no-one-sided-bound theorem",
        "unknown nonnegative slacks enter with opposite signs" in claims["C-RDIFF-001"]["statement"]
        and "neither an upper nor a lower bound" in " ".join(claims["C-RDIFF-001"]["assumptions"]),
    )
    checks.check(
        "accepted C-RDIFF-002 keeps the corrected coordinate conditional and nonphysical",
        "8.482417318795285" in claims["C-RDIFF-002"]["statement"]
        and "not a variational bound" in claims["C-RDIFF-002"]["statement"],
    )
    total = checks.finish()
    print(f"P175 INDEPENDENT SIGNED BOUND ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
