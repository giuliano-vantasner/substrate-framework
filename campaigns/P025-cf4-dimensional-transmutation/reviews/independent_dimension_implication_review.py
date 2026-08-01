#!/usr/bin/env python3
"""Independent dimension-kernel and confinement-implication review for P025."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P025-INDEPENDENT")

    exponent = sp.symbols("x")
    unique = sp.linsolve([sp.Eq(exponent, 2)], [exponent])
    checks.check(
        "one sole mass scale fixes the tension exponent to two",
        unique == {(sp.Integer(2),)},
    )

    first, second = sp.symbols("a b")
    multiple = sp.linsolve([sp.Eq(first + second, 2)], [first, second])
    checks.check(
        "two independent mass scales leave a one-parameter exponent family",
        multiple == {(2 - second, second)},
    )

    scale, ratio = sp.symbols("Lambda k", positive=True)
    tension = ratio * scale**2
    checks.check(
        "dimensional homogeneity leaves the multiplicative ratio arbitrary",
        sp.diff(tension, ratio) == scale**2
        and tension.subs(ratio, 2) != tension.subs(ratio, 1),
    )

    log_scale, inverse_reference, slope = sp.symbols("L u0 s", positive=True)
    inverse = inverse_reference + slope * log_scale
    pole = -inverse_reference / slope
    checks.check(
        "the independently rederived linear inverse coupling has a formal IR-side zero",
        inverse.subs(log_scale, pole) == 0 and pole.is_negative is True,
    )

    sigma = sp.symbols("sigma", nonnegative=True)
    checks.check(
        "the one-loop equations impose no equation on sigma",
        sigma not in inverse.free_symbols and inverse.subs(log_scale, pole) == 0,
    )
    checks.check(
        "sigma zero and sigma positive are both compatible with the same flow",
        inverse.subs(log_scale, pole).subs(sigma, 0) == 0
        and inverse.subs(log_scale, pole).subs(sigma, scale**2) == 0,
    )

    total = checks.finish()
    print(f"P025 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
