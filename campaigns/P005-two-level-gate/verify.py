#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed claim C-TH-001."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.thermal import (
    symmetric_two_level_gate,
    two_level_occupation_variance,
    two_level_upper_occupation,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class GateCandidate:
    occupation_normalizer: int
    gate_multiplier: int
    argument_divisor: int
    shape_denominator: int


def gate_candidate_is_exact(candidate: GateCandidate) -> bool:
    x = sp.symbols("x", real=True)
    probability = 1 / (candidate.occupation_normalizer + sp.exp(x))
    gate = candidate.gate_multiplier * probability * (1 - probability)
    shape = (
        sp.sech(x / candidate.argument_divisor) ** 2
        / candidate.shape_denominator
    )
    return sp.simplify((gate - shape).rewrite(sp.exp)) == 0


def run() -> int:
    checks = CheckLedger("C-TH-001")
    x = sp.symbols("x", real=True)
    probability = two_level_upper_occupation(x)
    variance = two_level_occupation_variance(x)
    gate = symmetric_two_level_gate(x)

    checks.check(
        "normalized upper occupation equals the partition-function form",
        sp.simplify(
            probability - sp.exp(-x) / (1 + sp.exp(-x))
        )
        == 0,
    )
    checks.check(
        "occupation variance has exact quarter-sech-squared form",
        sp.simplify(
            (variance - sp.sech(x / 2) ** 2 / 4).rewrite(sp.exp)
        )
        == 0,
    )
    checks.check(
        "negative occupation susceptibility equals its variance",
        sp.simplify(
            (-sp.diff(probability, x) - variance).rewrite(sp.exp)
        )
        == 0,
    )
    checks.check(
        "symmetric gate has exact half-sech-squared form",
        sp.simplify(
            (gate - sp.sech(x / 2) ** 2 / 2).rewrite(sp.exp)
        )
        == 0,
    )
    checks.check(
        "the gate is exactly even in the signed splitting",
        sp.simplify((gate.subs(x, -x) - gate).rewrite(sp.exp)) == 0,
    )

    derivative_target = -sp.sech(x / 2) ** 2 * sp.tanh(x / 2) / 2
    checks.check(
        "the exact derivative is negative for x>0 and positive for x<0",
        sp.simplify((sp.diff(gate, x) - derivative_target).rewrite(sp.exp)) == 0,
    )
    y = sp.symbols("y", positive=True)
    exponential_gate = 2 * y / (1 + y) ** 2
    global_gap = sp.simplify(sp.Rational(1, 2) - exponential_gate)
    checks.check(
        "the global maximum gap is a nonnegative square",
        sp.simplify(
            global_gap - (y - 1) ** 2 / (2 * (1 + y) ** 2)
        )
        == 0,
    )
    checks.check(
        "the maximum is one half at zero splitting",
        gate.subs(x, 0) == sp.Rational(1, 2),
    )
    checks.check(
        "the gate vanishes at both infinite-splitting limits",
        sp.limit(gate, x, sp.oo) == 0
        and sp.limit(gate, x, -sp.oo) == 0,
    )

    amplitude = sp.symbols("A", real=True)
    checks.check(
        "a macroscopic sech-squared shape equals 2*A times the normalized gate",
        sp.simplify(
            (
                amplitude * sp.sech(x / 2) ** 2
                - 2 * amplitude * gate
            ).rewrite(sp.exp)
        )
        == 0,
    )
    checks.mutation_sensitive(
        "occupation normalization, gate factor, half-angle, and shape factor",
        gate_candidate_is_exact,
        GateCandidate(1, 2, 2, 2),
        [
            GateCandidate(0, 2, 2, 2),
            GateCandidate(1, 1, 2, 2),
            GateCandidate(1, 2, 1, 2),
            GateCandidate(1, 2, 2, 1),
        ],
    )

    total = checks.finish()
    print(f"P005 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
