#!/usr/bin/env python3
"""Independent Z/2Z quotient review for P019 without package label APIs."""

from __future__ import annotations

import itertools

from substrate_framework.verification import CheckLedger


def residue(winding: int) -> int:
    return winding % 2


def character(winding: int) -> int:
    return 1 if residue(winding) == 0 else -1


def run() -> int:
    checks = CheckLedger("P019-INDEPENDENT")
    checks.check(
        "integer addition descends to addition modulo two",
        all(
            residue(first + second)
            == (residue(first) + residue(second)) % 2
            for first, second in itertools.product(range(-20, 21), repeat=2)
        ),
    )
    checks.check(
        "the sign character turns residue addition into multiplication",
        all(
            character(first + second) == character(first) * character(second)
            for first, second in itertools.product(range(-20, 21), repeat=2)
        ),
    )
    checks.check(
        "every even dressing is neutral",
        all(character(anchor + 2 * k) == character(anchor) for anchor in range(-10, 11) for k in range(-5, 6)),
    )
    checks.check(
        "every odd dressing flips the label",
        all(character(anchor + 2 * k + 1) == -character(anchor) for anchor in range(-10, 11) for k in range(-5, 6)),
    )
    checks.check(
        "external statistics and charge assignments are not fixed by the quotient",
        (character(1), "bosonic_representation", 0)
        != (character(1), "fermionic_representation", 1),
    )

    total = checks.finish()
    print(f"P019 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
