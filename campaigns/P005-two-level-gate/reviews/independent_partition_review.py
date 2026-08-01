#!/usr/bin/env python3
"""Independent partition-moment review for proposed C-TH-001.

This route intentionally does not import ``substrate_framework.thermal``.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("C-TH-001-INDEPENDENT")
    x = sp.symbols("x", real=True)
    partition = 1 + sp.exp(-x)
    lower_probability = 1 / partition
    upper_probability = sp.exp(-x) / partition

    checks.check(
        "partition probabilities normalize exactly",
        sp.simplify(lower_probability + upper_probability - 1) == 0,
    )
    occupation_mean = upper_probability
    occupation_second_moment = upper_probability
    variance = sp.simplify(
        occupation_second_moment - occupation_mean**2
    )
    checks.check(
        "direct two-state moments derive P*(1-P)",
        sp.simplify(variance - upper_probability * (1 - upper_probability))
        == 0,
    )
    checks.check(
        "partition susceptibility independently equals occupation variance",
        sp.simplify(
            (-sp.diff(upper_probability, x) - variance).rewrite(sp.exp)
        )
        == 0,
    )
    checks.check(
        "independent moments yield the exact symmetric sech gate",
        sp.simplify(
            (2 * variance - sp.sech(x / 2) ** 2 / 2).rewrite(sp.exp)
        )
        == 0,
    )

    y = sp.symbols("y", positive=True)
    gate_y = 2 * y / (1 + y) ** 2
    checks.check(
        "a square identity proves the global bound without point sampling",
        sp.simplify(
            sp.Rational(1, 2)
            - gate_y
            - (y - 1) ** 2 / (2 * (1 + y) ** 2)
        )
        == 0,
    )
    raw_factor = sp.exp(-x)
    checks.check(
        "an unnormalized Boltzmann factor fails the gate identity",
        sp.simplify(
            (
                2 * raw_factor * (1 - raw_factor)
                - sp.sech(x / 2) ** 2 / 2
            ).rewrite(sp.exp)
        )
        != 0,
    )
    checks.check(
        "a missing half-angle fails at an exact nonzero point",
        sp.simplify(
            (
                2 * variance - sp.sech(x) ** 2 / 2
            ).subs(x, sp.log(3))
        )
        != 0,
    )

    total = checks.finish()
    print(f"P005 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
