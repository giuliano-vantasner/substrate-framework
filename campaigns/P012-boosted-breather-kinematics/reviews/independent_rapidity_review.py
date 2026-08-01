#!/usr/bin/env python3
"""Independent rapidity reconstruction for proposed C-SG-008.

This route does not import the proposed boost APIs.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("C-SG-008-INDEPENDENT")
    rapidity = sp.symbols("rapidity", real=True)
    omega = sp.symbols("omega", positive=True)
    rest_energy = 16 * sp.sqrt(1 - omega**2)
    scale = rest_energy / omega
    phase = (
        omega * sp.cosh(rapidity),
        omega * sp.sinh(rapidity),
    )
    energy_momentum = (
        rest_energy * sp.cosh(rapidity),
        rest_energy * sp.sinh(rapidity),
    )

    checks.check(
        "rapidity gives componentwise proportionality without velocity ratios",
        sp.simplify(energy_momentum[0] - scale * phase[0]) == 0
        and sp.simplify(energy_momentum[1] - scale * phase[1]) == 0,
    )
    checks.check(
        "the hyperbolic identity fixes the phase invariant norm",
        sp.trigsimp(phase[0] ** 2 - phase[1] ** 2 - omega**2) == 0,
    )
    checks.check(
        "the same hyperbolic identity fixes the energy-momentum norm",
        sp.trigsimp(
            energy_momentum[0] ** 2
            - energy_momentum[1] ** 2
            - rest_energy**2
        )
        == 0,
    )
    checks.check(
        "zero rapidity has a regular rest vector even though spatial ratios are undefined",
        tuple(item.subs(rapidity, 0) for item in phase) == (omega, 0)
        and tuple(item.subs(rapidity, 0) for item in energy_momentum)
        == (rest_energy, 0),
    )
    checks.check(
        "reversing only the phase spatial sign breaks vector proportionality",
        sp.simplify(energy_momentum[1] + scale * phase[1]) != 0,
    )

    total = checks.finish()
    print(f"P012 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
