#!/usr/bin/env python3
"""Exact profile, charge, and implication audit for EM6."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.quartic_qball import (
    quartic_qball_amplitude,
    quartic_qball_charge,
    quartic_qball_charge_derivative,
    quartic_qball_inverse_width,
    quartic_qball_profile,
    quartic_qball_residual,
)
from substrate_framework.u1_charge import (
    stationary_phase_field,
    u1_current_components,
)
from substrate_framework.verification import CheckLedger


EM6_SHA256 = "926df2dc5014042472b3d47576af06676eb654d9da4634f147c7044d4e91f897"


@dataclass(frozen=True)
class ProfileCoefficients:
    inverse_width: sp.Expr
    amplitude: sp.Expr
    cubic_coefficient: sp.Expr


def run(source_file: Path) -> int:
    checks = CheckLedger("P031-EM6")
    payload = source_file.read_bytes()
    source_text = payload.decode("utf-8")
    checks.check(
        "the audited EM6 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == EM6_SHA256,
    )
    checks.check(
        "EM6 itself declares the quartic reduction and stationary ansatz",
        "DECLARED: the phi^4 small-amplitude reduction" in source_text
        and "stationary Q-ball ansatz" in source_text
        and "real nodeless f; 1+1D" in source_text,
    )

    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    profile = quartic_qball_profile(coordinate, frequency)
    checks.check(
        "the positive translated sech profile solves the declared ODE exactly",
        sp.simplify(quartic_qball_residual(profile, coordinate, frequency)) == 0,
    )

    shape = sp.symbols("s", positive=True)
    inverse_width, amplitude = sp.symbols("kappa A", positive=True)
    polynomial = sp.Poly(
        amplitude * inverse_width**2 * shape * (1 - 2 * shape**2)
        - (sp.Rational(1, 2) - frequency**2) * amplitude * shape
        + amplitude**3 * shape**3 / 12,
        shape,
    )
    linear_coefficient = polynomial.coeff_monomial(shape) / amplitude
    cubic_coefficient = polynomial.coeff_monomial(shape**3) / amplitude
    checks.check(
        "independent sech powers force both nonzero-ansatz coefficients",
        sp.solve(
            [linear_coefficient, cubic_coefficient],
            [inverse_width**2, amplitude**2],
            dict=True,
        )
        == [
            {
                inverse_width**2: sp.Rational(1, 2) - frequency**2,
                amplitude**2: 12 - 24 * frequency**2,
            }
        ],
    )
    checks.check(
        "the localized frequency domain is open and has positive width and amplitude",
        quartic_qball_inverse_width(sp.Rational(1, 2)) == sp.Rational(1, 2)
        and quartic_qball_amplitude(sp.Rational(1, 2)) == sp.sqrt(6),
    )
    checks.check(
        "the centered profile is even, stationary at its peak, and localized",
        sp.simplify(profile.subs(coordinate, -coordinate) - profile) == 0
        and sp.diff(profile, coordinate).subs(coordinate, 0) == 0
        and sp.limit(
            quartic_qball_profile(coordinate, sp.Rational(1, 2)),
            coordinate,
            sp.oo,
        )
        == 0
        and sp.limit(
            quartic_qball_profile(coordinate, sp.Rational(1, 2)),
            coordinate,
            -sp.oo,
        )
        == 0,
    )

    kappa = quartic_qball_inverse_width(frequency)
    first_integral = (
        sp.diff(profile, coordinate) ** 2
        - kappa**2 * profile**2
        + profile**4 / 24
    )
    checks.check(
        "the localized solution obeys the independently integrated first integral",
        sp.simplify(
            first_integral.subs(
                sp.tanh(kappa * coordinate) ** 2,
                1 - sp.sech(kappa * coordinate) ** 2,
            )
        )
        == 0,
    )

    time = sp.symbols("t", real=True)
    stationary = stationary_phase_field(profile, time, frequency)
    conjugate = profile * sp.exp(sp.I * frequency * time)
    density, flux = u1_current_components(
        stationary, conjugate, coordinate, time
    )
    checks.check(
        "C-U1-001 fixes positive stationary density and zero spatial flux",
        sp.simplify(density - 2 * frequency * profile**2) == 0
        and flux == 0,
    )

    scaled_coordinate = sp.symbols("u", real=True)
    scaled_density = sp.simplify(
        density.subs(coordinate, scaled_coordinate / kappa) / kappa
    ).subs(
        sp.sech(scaled_coordinate) ** 2,
        sp.cosh(scaled_coordinate) ** -2,
    )
    integrated_charge = sp.integrate(
        scaled_density, (scaled_coordinate, -sp.oo, sp.oo)
    )
    charge = quartic_qball_charge(frequency)
    checks.check(
        "the accepted-current integral gives the exact amplitude-aware charge",
        sp.simplify(integrated_charge - charge) == 0
        and sp.simplify(
            charge
            - 96
            * frequency
            * sp.sqrt(sp.Rational(1, 2) - frequency**2)
        )
        == 0,
    )
    checks.check(
        "the charge vanishes at both open endpoints",
        sp.limit(charge, frequency, 0, dir="+") == 0
        and sp.limit(
            charge,
            frequency,
            sp.sqrt(sp.Rational(1, 2)),
            dir="-",
        )
        == 0,
    )

    slope = quartic_qball_charge_derivative(frequency)
    expected_slope = (
        96
        * (sp.Rational(1, 2) - 2 * frequency**2)
        / sp.sqrt(sp.Rational(1, 2) - frequency**2)
    )
    checks.check(
        "the charge slope is exact and has one interior stationary point",
        sp.simplify(slope - sp.diff(charge, frequency)) == 0
        and sp.simplify(slope - expected_slope) == 0
        and sp.solve(sp.Eq(sp.factor(sp.together(slope)), 0), frequency)
        == [sp.Rational(1, 2)],
    )
    checks.check(
        "the charge rises, reaches 24, then falls on the two branches",
        quartic_qball_charge_derivative(sp.Rational(1, 4)) > 0
        and quartic_qball_charge(sp.Rational(1, 2)) == 24
        and quartic_qball_charge_derivative(sp.Rational(3, 5)) < 0,
    )

    def solves_declared_model(candidate: object) -> bool:
        coefficients = candidate
        assert isinstance(coefficients, ProfileCoefficients)
        trial = coefficients.amplitude * sp.sech(
            coefficients.inverse_width * coordinate
        )
        residual = sp.diff(trial, coordinate, 2) - (
            sp.Rational(1, 2) - frequency_value**2
        ) * trial + coefficients.cubic_coefficient * trial**3
        return sp.simplify(residual) == 0

    frequency_value = sp.Rational(1, 2)
    baseline = ProfileCoefficients(sp.Rational(1, 2), sp.sqrt(6), sp.Rational(1, 12))
    checks.mutation_sensitive(
        "width amplitude and quartic coefficient",
        solves_declared_model,
        baseline,
        [
            ProfileCoefficients(sp.sqrt(3) / 2, sp.sqrt(6), sp.Rational(1, 12)),
            ProfileCoefficients(sp.Rational(1, 2), sp.sqrt(6) / 2, sp.Rational(1, 12)),
            ProfileCoefficients(sp.Rational(1, 2), sp.sqrt(6), sp.Rational(1, 10)),
        ],
    )

    gaussian = sp.sqrt(6) * sp.exp(-coordinate**2 / 4)
    checks.check(
        "a Gaussian counterprofile fails the declared equation exactly",
        sp.simplify(
            quartic_qball_residual(gaussian, coordinate, frequency_value)
            .subs(coordinate, 0)
        )
        != 0,
    )
    em1_width_profile = sp.sqrt(6) * sp.sech(
        sp.sqrt(1 - frequency_value**2) * coordinate
    )
    checks.check(
        "EM1's breather width is not EM6's on-shell Q-ball width",
        sp.simplify(
            quartic_qball_residual(
                em1_width_profile, coordinate, frequency_value
            ).subs(coordinate, 0)
        )
        != 0,
    )

    real_field = sp.Function("f", real=True)(coordinate) * sp.cos(
        frequency * time
    )
    real_density, _ = u1_current_components(
        real_field, real_field, coordinate, time
    )
    checks.check(
        "a real field has zero U1 current but that identity is not a stability theorem",
        real_density == 0 and density != 0,
    )
    checks.check(
        "EM6 invokes VK without encoding a fluctuation spectrum or theorem hypotheses",
        "Vakhitov-Kolokolov criterion" in source_text
        and "eigenvalue" not in source_text
        and "fluctuation operator" not in source_text
        and "linearized operator" not in source_text,
    )
    checks.check(
        "EM6's forced-ontology predicate substitutes sampled slope for the missing theorem",
        "forced = real_field_Q_zero and complex_field_Q_nonzero and vk_stable_branch_exists"
        in source_text,
    )
    checks.check(
        "the cited D>=2 instability cannot directly settle the declared 1+1 profile",
        "real nodeless f; 1+1D" in source_text
        and "D >= 2" in source_text
        and "the instability is cited, not re-simulated" in source_text,
    )
    checks.check(
        "the two shooting resolutions change samples rather than solver accuracy",
        "def shoot(n_pts):" in source_text
        and "t_eval=xs" in source_text
        and "shoot(500)" in source_text
        and "shoot(2000)" in source_text
        and source_text.count("rtol=1e-11, atol=1e-13") == 1,
    )

    total = checks.finish()
    print(f"P031 EM6 QUARTIC-QBALL AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
