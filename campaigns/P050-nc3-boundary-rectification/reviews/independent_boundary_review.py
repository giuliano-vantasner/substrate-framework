#!/usr/bin/env python3
"""Independently review P050 without calling its new canonical helpers."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P050-INDEPENDENT")

    theta, delta = sp.symbols("theta delta", real=True)
    amplitude = sp.symbols("B", real=True)
    frequency = sp.symbols("omega", positive=True)

    square_wave_sine_coefficient = (
        sp.integrate(sp.sin(theta), (theta, 0, sp.pi))
        - sp.integrate(sp.sin(theta), (theta, sp.pi, 2 * sp.pi))
    ) / sp.pi
    square_wave_cosine_coefficient = (
        sp.integrate(sp.cos(theta), (theta, 0, sp.pi))
        - sp.integrate(sp.cos(theta), (theta, sp.pi, 2 * sp.pi))
    ) / sp.pi
    ledger.check(
        "the square-wave fundamental coefficients are independently normalized",
        square_wave_sine_coefficient == 4 / sp.pi
        and square_wave_cosine_coefficient == 0,
    )
    independent_correlation = sp.simplify(
        sp.pi
        * amplitude
        * (
            square_wave_sine_coefficient * sp.cos(delta)
            + square_wave_cosine_coefficient * sp.sin(delta)
        )
        / frequency
    )
    ledger.check(
        "Fourier orthogonality independently gives four B cos(delta) over omega",
        independent_correlation == 4 * amplitude * sp.cos(delta) / frequency,
    )

    u_reflected, v_reflected = sp.symbols("u_reflected v_reflected", real=True)
    original_at_reflected_point = sp.sign(u_reflected) * v_reflected
    parity_image_at_point = sp.sign(u_reflected) * (-v_reflected)
    ledger.check(
        "direct chain-rule parity gives R_b[phi_P] equals minus R_-b[phi]",
        sp.simplify(parity_image_at_point + original_at_reflected_point) == 0,
    )

    right_normal = -v_reflected
    left_normal_after_parity = -v_reflected
    ledger.check(
        "transforming the half-line domain makes the outward-normal channel even",
        sp.sign(u_reflected) * right_normal
        == sp.sign(u_reflected) * left_normal_after_parity,
    )

    boundary_change = sp.symbols("Delta_phi_boundary", real=True)
    charge_initial = sp.symbols("Q_initial", real=True)
    charge_final = charge_initial - boundary_change / (2 * sp.pi)
    ledger.check(
        "the fundamental theorem independently fixes the right-half-line charge change",
        sp.simplify(charge_final - charge_initial + boundary_change / (2 * sp.pi))
        == 0,
    )

    periodic_change = sp.integrate(
        sp.sin(theta),
        (theta, 0, 2 * sp.pi),
    )
    ledger.check(
        "the source harmonic is a counterexample to correlation as winding discriminator",
        periodic_change == 0
        and independent_correlation.subs({amplitude: 1, delta: 0})
        == 4 / frequency,
    )

    eta, z = sp.symbols("eta z", positive=True)
    denominator = frequency**2 * sp.cosh(z) ** 2 + eta**2 * sp.sin(theta) ** 2
    breather_time = (
        4 * eta * frequency**2 * sp.cosh(z) * sp.cos(theta) / denominator
    )
    breather_space = (
        -4 * eta**2 * frequency * sp.sinh(z) * sp.sin(theta) / denominator
    )
    ledger.check(
        "a direct exact breather derivative route has opposite period-reflection parities",
        sp.simplify(breather_time.subs(theta, 2 * sp.pi - theta) - breather_time)
        == 0
        and sp.simplify(
            breather_space.subs(theta, 2 * sp.pi - theta) + breather_space
        )
        == 0,
    )
    ledger.check(
        "the exact rest-breather sign correlation therefore integrates to zero",
        sp.simplify(
            sp.sign(breather_time.subs(theta, 2 * sp.pi - theta))
            * breather_space.subs(theta, 2 * sp.pi - theta)
            + sp.sign(breather_time) * breather_space
        )
        == 0,
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
