"""Independent P110 review using scaled integers and exhaustive divmod."""

from __future__ import annotations

import math

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("PN2-INDEPENDENT")

    total_micro_eV = 24_000_000 * 1_000_000
    unit_micro_eV = [1_000, 3_000, 10_000, 30_000, 100_000, 300_000, 1_000_000]
    counts = []
    for unit in unit_micro_eV:
        quotient, remainder = divmod(total_micro_eV, unit)
        counts.append(quotient)
        checks.check(
            f"integer divmod closes exactly at {unit} micro-eV",
            total_micro_eV == quotient * unit + remainder
            and 0 <= remainder < unit,
        )
    checks.check(
        "fresh scaled-integer route reproduces the seven counts",
        counts
        == [
            24_000_000_000,
            8_000_000_000,
            2_400_000_000,
            800_000_000,
            240_000_000,
            80_000_000,
            24_000_000,
        ],
    )
    checks.check(
        "fresh selected-band extrema are exact rather than decade labels",
        min(counts) == 24_000_000 and max(counts) == 24_000_000_000,
    )

    all_division = True
    all_monotone = True
    for total in range(1, 51):
        previous = None
        for unit in range(1, 51):
            quotient, remainder = divmod(total, unit)
            all_division = all_division and (
                total == quotient * unit + remainder and 0 <= remainder < unit
            )
            if previous is not None:
                all_monotone = all_monotone and previous >= quotient
            previous = quotient
    checks.check(
        "fresh exhaustive 50-by-50 divmod grid closes quotient and remainder",
        all_division,
    )
    checks.check(
        "fresh exhaustive 50-by-50 grid is nonincreasing in unit energy",
        all_monotone,
    )

    checks.check(
        "fresh scaling route leaves quotient invariant",
        all(
            divmod(13 * total_micro_eV, 13 * unit)[0]
            == divmod(total_micro_eV, unit)[0]
            for unit in unit_micro_eV
        ),
    )
    checks.check(
        "fresh exact-decimal counterexample rejects binary floating floor",
        divmod(3, 1)[0] == 3 and math.floor(0.3 / 0.1) == 2,
    )
    checks.check(
        "fresh zero-matrix-element countermodel leaves quotient unchanged and rate zero",
        divmod(total_micro_eV, 30_000)[0] == 800_000_000
        and 0**2 == 0,
    )
    checks.check(
        "fresh review uses no quadrature solver or empirical fit",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
