#!/usr/bin/env python3
"""Independent inverse-map and input-ledger review for P023."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P023-INDEPENDENT")
    scale, length, exponent, shape, offset, target = sp.symbols(
        "Sc a z b kappa E", positive=True
    )
    energy = offset * scale * sp.exp(-exponent) / (
        48 * sp.pi**3 * shape * length
    )
    solved_offset = sp.solve(sp.Eq(energy, target), offset)[0]
    checks.check(
        "direct inversion makes the required offset proportional to the target",
        sp.diff(solved_offset, target) == solved_offset / target,
    )
    solved_length = sp.solve(sp.Eq(energy, target), length)[0]
    checks.check(
        "direct inversion makes the required length inversely proportional to the target",
        sp.diff(solved_length, target) == -solved_length / target,
    )
    checks.check(
        "either inverse composes back to the same target",
        sp.simplify(energy.subs(offset, solved_offset) - target) == 0
        and sp.simplify(energy.subs(length, solved_length) - target) == 0,
    )
    checks.check(
        "the forward formula retains every declared symbol",
        energy.free_symbols == {scale, length, exponent, shape, offset},
    )
    ratio = sp.symbols("R", positive=True)
    checks.check(
        "the ratio comparator fixes the shape rather than eliminating it",
        sp.solve(sp.Eq(48 * sp.pi**3 * shape, ratio), shape)[0]
        == ratio / (48 * sp.pi**3),
    )
    total = checks.finish()
    print(f"P023 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
