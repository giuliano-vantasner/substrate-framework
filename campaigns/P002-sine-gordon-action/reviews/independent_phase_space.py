#!/usr/bin/env python3
"""Independent field phase-space review for proposed C-SG-003.

This review intentionally does not import the proposed action APIs.  It
reconstructs the accepted breather, verifies the spatial antiderivative, and
computes ``(1/(2*pi))*int dt dx phi_t**2`` at two working precisions.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

from substrate_framework.verification import CheckLedger


def abbreviated_action(frequency: mp.mpf, decimal_places: int) -> mp.mpf:
    """Evaluate the phase-space line integral with the x integral analytic."""

    with mp.workdps(decimal_places):
        omega = mp.mpf(frequency)
        eta = mp.sqrt(1 - omega**2)

        def time_integrand(time: mp.mpf) -> mp.mpf:
            amplitude = (eta / omega) * mp.sin(omega * time)
            if amplitude == 0:
                spatial_factor = mp.mpf(2)
            else:
                denominator = 1 + amplitude**2
                spatial_factor = (
                    1 / denominator
                    + mp.asinh(amplitude)
                    / (amplitude * denominator ** mp.mpf("1.5"))
                )
            return 16 * eta * mp.cos(omega * time) ** 2 * spatial_factor

        period = 2 * mp.pi / omega
        abbreviated = mp.quad(time_integrand, [0, period / 2, period])
        return +abbreviated


def run() -> int:
    checks = CheckLedger("P002-INDEPENDENT-REVIEW")
    x, t = sp.symbols("x t", real=True)
    omega, eta, amplitude = sp.symbols("omega eta A", positive=True)
    y = sp.symbols("y", real=True)

    field = 4 * sp.atan(
        eta * sp.sin(omega * t) / (omega * sp.cosh(eta * x))
    )
    momentum = sp.diff(field, t)
    closed_momentum = (
        4
        * eta
        * sp.cos(omega * t)
        / sp.cosh(eta * x)
        / (
            1
            + (eta * sp.sin(omega * t) / omega) ** 2
            / sp.cosh(eta * x) ** 2
        )
    )
    checks.check(
        "the reconstructed canonical momentum is the exact field derivative",
        sp.simplify(momentum - closed_momentum) == 0,
    )

    scale = sp.sqrt(1 + amplitude**2)
    spatial_integrand = 1 / (scale**2 - amplitude**2 * y**2) ** 2
    antiderivative = (
        y / (2 * scale**2 * (scale**2 - amplitude**2 * y**2))
        + sp.atanh(amplitude * y / scale)
        / (2 * amplitude * scale**3)
    )
    checks.check(
        "the spatial phase-space integrand has the stated exact antiderivative",
        sp.simplify(sp.diff(antiderivative, y) - spatial_integrand) == 0,
    )
    definite_spatial = sp.simplify(
        antiderivative.subs(y, 1) - antiderivative.subs(y, -1)
    )
    expected_spatial = (
        1 / (1 + amplitude**2)
        + sp.atanh(amplitude / sp.sqrt(1 + amplitude**2))
        / (amplitude * (1 + amplitude**2) ** sp.Rational(3, 2))
    )
    checks.check(
        "the exact spatial endpoints preserve the phase-space normalization",
        sp.simplify(definite_spatial - expected_spatial) == 0,
    )

    anchors = (mp.mpf("0.3"), mp.mpf("0.5"), 1 / mp.sqrt(2), mp.mpf("0.9"))
    for frequency in anchors:
        low = abbreviated_action(frequency, 30)
        high = abbreviated_action(frequency, 50)
        with mp.workdps(50):
            target = 32 * mp.pi * mp.acos(frequency)
            high_relative_error = abs(high - target) / abs(target)
            refinement_delta = abs(high - low) / abs(target)
            checks.check(
                f"direct phase-space integral agrees at omega={mp.nstr(frequency, 8)}",
                high_relative_error < mp.mpf("1e-40"),
                f"relative_error={mp.nstr(high_relative_error, 8)}",
            )
            checks.check(
                f"30-to-50 digit refinement is stable at omega={mp.nstr(frequency, 8)}",
                refinement_delta < mp.mpf("1e-28"),
                f"refinement_delta={mp.nstr(refinement_delta, 8)}",
            )
            normalized = high / (2 * mp.pi)
            expected_action = 16 * mp.acos(frequency)
            checks.check(
                f"canonical 1/(2*pi) normalization yields J at omega={mp.nstr(frequency, 8)}",
                abs(normalized - expected_action) / abs(expected_action)
                < mp.mpf("1e-40"),
            )
            wrong_normalized = high / (4 * mp.pi)
            checks.check(
                f"factor-two normalization mutation fails at omega={mp.nstr(frequency, 8)}",
                abs(wrong_normalized - expected_action) / abs(expected_action)
                > mp.mpf("0.4"),
            )

    total = checks.finish()
    print(f"P002 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
