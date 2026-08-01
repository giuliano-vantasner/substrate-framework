#!/usr/bin/env python3
"""Independent marginal-energy construction for proposed C-SG-005.

This file intentionally does not import ``breather_threshold_deficit``.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.sine_gordon import breather_energy
from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("C-SG-005-INDEPENDENT")
    omega = sp.symbols("omega", positive=True)
    integration_frequency = sp.symbols("u", nonnegative=True)

    energy = breather_energy(omega)
    marginal_loss = (
        16
        * integration_frequency
        / sp.sqrt(1 - integration_frequency**2)
    )
    integrated_loss = sp.integrate(
        marginal_loss,
        (integration_frequency, 0, omega),
    )
    checks.check(
        "integrating the marginal energy loss independently constructs the deficit",
        sp.simplify(
            integrated_loss
            - 16 * (1 - sp.sqrt(1 - omega**2))
        )
        == 0,
    )
    checks.check(
        "the integral construction partitions the accepted threshold",
        sp.simplify(energy + integrated_loss - 16) == 0,
    )
    checks.check(
        "differentiating the independent integral recovers its positive integrand",
        sp.simplify(
            sp.diff(integrated_loss, omega)
            - 16 * omega / sp.sqrt(1 - omega**2)
        )
        == 0,
    )
    checks.check(
        "a wrong linear-power complement disagrees away from the endpoints",
        sp.simplify(
            integrated_loss.subs(omega, sp.Rational(3, 5))
            - (16 * omega**2).subs(omega, sp.Rational(3, 5))
        )
        != 0,
    )

    total = checks.finish()
    print(f"P009 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
