#!/usr/bin/env python3
"""Independent direct-field review route for proposed C-SG-004.

The review intentionally does not import the proposed gradient API or action
API.  It reconstructs the accepted field, derives the fixed-time spatial
integral, and performs refined period and direct double quadrature.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

from substrate_framework.verification import CheckLedger


def closed_candidate(frequency: mp.mpf) -> mp.mpf:
    eta = mp.sqrt(1 - frequency**2)
    return 16 * (eta - frequency * mp.acos(frequency))


def spatial_gradient_integral(time: mp.mpf, frequency: mp.mpf) -> mp.mpf:
    eta = mp.sqrt(1 - frequency**2)
    amplitude = (eta / frequency) * mp.sin(frequency * time)
    if amplitude == 0:
        return mp.mpf(0)
    return 16 * eta * (
        1
        - mp.asinh(amplitude)
        / (amplitude * mp.sqrt(1 + amplitude**2))
    )


def averaged_spatial_integral(frequency: mp.mpf, decimal_places: int) -> mp.mpf:
    with mp.workdps(decimal_places):
        omega = mp.mpf(frequency)
        period = 2 * mp.pi / omega
        value = mp.quad(
            lambda time: spatial_gradient_integral(time, omega),
            [0, period / 4, period / 2, 3 * period / 4, period],
        ) / period
        return +value


def direct_double_integral(frequency: mp.mpf, decimal_places: int) -> mp.mpf:
    with mp.workdps(decimal_places):
        omega = mp.mpf(frequency)
        eta = mp.sqrt(1 - omega**2)
        period = 2 * mp.pi / omega

        def field_gradient(coordinate: mp.mpf, time: mp.mpf) -> mp.mpf:
            amplitude = (eta / omega) * mp.sin(omega * time)
            profile = amplitude * mp.sech(eta * coordinate)
            return (
                -4
                * eta
                * amplitude
                * mp.sech(eta * coordinate)
                * mp.tanh(eta * coordinate)
                / (1 + profile**2)
            )

        def time_slice(time: mp.mpf) -> mp.mpf:
            return mp.quad(
                lambda coordinate: field_gradient(coordinate, time) ** 2,
                [-mp.inf, 0, mp.inf],
            )

        value = mp.quad(
            time_slice,
            [0, period / 4, period / 2, 3 * period / 4, period],
        ) / period
        return +value


def run() -> int:
    checks = CheckLedger("P003-INDEPENDENT-REVIEW")
    x, t = sp.symbols("x t", real=True)
    eta, omega, amplitude, y = sp.symbols(
        "eta omega A y", positive=True
    )
    field = 4 * sp.atan(
        eta * sp.sin(omega * t) / (omega * sp.cosh(eta * x))
    )
    field_gradient = sp.diff(field, x)
    closed_gradient = (
        -4
        * eta
        * amplitude
        / sp.cosh(eta * x)
        * sp.tanh(eta * x)
        / (1 + amplitude**2 / sp.cosh(eta * x) ** 2)
    )
    checks.check(
        "the reconstructed field gradient has the exact closed form",
        sp.simplify(
            field_gradient.subs(
                sp.sin(omega * t), amplitude * omega / eta
            )
            - closed_gradient
        )
        == 0,
    )

    denominator = 1 + amplitude**2 - amplitude**2 * y**2
    transformed = amplitude**2 * y**2 / denominator**2
    scale = sp.sqrt(1 + amplitude**2)
    antiderivative = (
        y / (2 * denominator)
        - sp.atanh(amplitude * y / scale)
        / (2 * amplitude * scale)
    )
    checks.check(
        "the transformed squared-gradient integrand has an exact antiderivative",
        sp.simplify(sp.diff(antiderivative, y) - transformed) == 0,
    )
    definite = sp.simplify(
        antiderivative.subs(y, 1) - antiderivative.subs(y, -1)
    )
    fixed_time_target = 1 - sp.atanh(amplitude / scale) / (
        amplitude * scale
    )
    checks.check(
        "the spatial endpoints yield the stated fixed-time integral factor",
        sp.simplify(definite - fixed_time_target) == 0,
    )

    anchors = (
        mp.mpf("0.2"),
        mp.mpf("0.5"),
        1 / mp.sqrt(2),
        mp.mpf("0.9"),
    )
    for frequency in anchors:
        low = averaged_spatial_integral(frequency, 30)
        high = averaged_spatial_integral(frequency, 50)
        with mp.workdps(50):
            target = closed_candidate(frequency)
            relative_error = abs(high - target) / abs(target)
            refinement_delta = abs(high - low) / abs(target)
            label = mp.nstr(frequency, 8)
            checks.check(
                f"averaged spatial integral agrees at omega={label}",
                relative_error < mp.mpf("1e-40"),
                f"relative_error={mp.nstr(relative_error, 8)}",
            )
            checks.check(
                f"30-to-50 digit refinement is stable at omega={label}",
                refinement_delta < mp.mpf("1e-28"),
                f"refinement_delta={mp.nstr(refinement_delta, 8)}",
            )
            checks.check(
                f"half-gradient mutation fails at omega={label}",
                abs(high / 2 - target) / abs(target) > mp.mpf("0.4"),
            )

    direct = direct_double_integral(mp.mpf("0.5"), 30)
    with mp.workdps(30):
        direct_target = closed_candidate(mp.mpf("0.5"))
        checks.check(
            "direct nested field quadrature agrees at omega=0.5",
            abs(direct - direct_target) / abs(direct_target) < mp.mpf("1e-24"),
        )

    total = checks.finish()
    print(f"P003 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
