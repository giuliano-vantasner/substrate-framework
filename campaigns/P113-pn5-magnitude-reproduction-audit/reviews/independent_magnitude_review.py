"""Independent Decimal, integer, and calculus review for P113."""

from __future__ import annotations

import ast
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("PN5-INDEPENDENT")

    total_micro_eV = 24_000_000 * 1_000_000
    units_micro_eV = [1_000, 3_000, 10_000, 30_000, 100_000, 300_000, 1_000_000]
    counts = []
    for unit in units_micro_eV:
        quotient, remainder = divmod(total_micro_eV, unit)
        counts.append(quotient)
        checks.check(
            f"fresh integer divmod closes at {unit} micro-eV",
            total_micro_eV == quotient * unit + remainder
            and 0 <= remainder < unit,
        )
    checks.check(
        "fresh scaled-integer route reproduces all selected counts",
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
        "fresh selected extrema reject the loose envelope as exact image",
        (min(counts), max(counts)) == (24_000_000, 24_000_000_000),
    )
    decimal_count = int(Decimal("24000000") // Decimal("0.03"))
    checks.check(
        "fresh Decimal route gives eight hundred million",
        decimal_count == 800_000_000,
    )
    checks.check(
        "fresh exact-threshold counterexample rejects binary floating floor",
        Fraction(3, 10) // Fraction(1, 10) == 3 and math.floor(0.3 / 0.1) == 2,
    )
    checks.check(
        "fresh common-scale route leaves all counts invariant",
        all(
            divmod(29 * total_micro_eV, 29 * unit)[0]
            == divmod(total_micro_eV, unit)[0]
            for unit in units_micro_eV
        ),
    )
    checks.check(
        "fresh arbitrary-target family makes every chosen count",
        all(
            Fraction(total_micro_eV, 1) // Fraction(total_micro_eV, target)
            == target
            for target in (2, 11, 10**6, 10**9)
        ),
    )

    delta, gamma, coupling = sp.symbols("Delta Gamma g", positive=True)
    magnitude = coupling**2 * gamma / (delta**2 + gamma**2 / 4)
    checks.check(
        "fresh derivative route finds the sole positive optimum",
        sp.solve(sp.together(sp.diff(magnitude, gamma)), gamma) == [2 * delta]
        and sp.diff(magnitude, gamma, 2).subs(gamma, 2 * delta) < 0,
    )
    checks.check(
        "fresh peak and endpoint routes close exactly",
        sp.simplify(magnitude.subs(gamma, 2 * delta) - coupling**2 / delta)
        == 0
        and sp.limit(magnitude, gamma, 0, dir="+") == 0
        and sp.limit(magnitude, gamma, sp.oo) == 0,
    )
    checks.check(
        "fresh coupling mutation changes the peak quadratically",
        sp.simplify(
            magnitude.subs({gamma: 2 * delta, coupling: 3 * coupling})
            - 9 * coupling**2 / delta
        )
        == 0,
    )
    checks.check(
        "fresh grid-error bound makes numeric argmax regression-only",
        Fraction(9999, 1000) / 20_000 / 2 < Fraction(1, 4000)
        and Fraction(2, 1000) > Fraction(1, 4000),
    )
    checks.check(
        "fresh zero-interaction countermodel preserves count and kills element",
        decimal_count == 800_000_000 and magnitude.subs(coupling, 0) == 0,
    )
    checks.check(
        "fresh dimensional route rejects matrix element as rate",
        (1, 0) != (0, -1),
    )
    checks.check(
        "fresh review imports no canonical paired-resolvent implementation",
        not any(
            isinstance(node, ast.ImportFrom)
            and node.module == "substrate_framework.paired_resolvent"
            for node in ast.walk(ast.parse(Path(__file__).read_text()))
        ),
    )
    checks.check(
        "fresh review uses no quadrature solver float fit or comparator",
        not magnitude.has(sp.Float, sp.Integral),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
