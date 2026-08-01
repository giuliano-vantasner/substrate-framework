#!/usr/bin/env python3
"""Verify P050's boundary-correlation theorem and audit NC3."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.boundary_correlations import (
    boundary_sign_correlation_density,
    right_half_line_topological_charge_change,
    sinusoidal_boundary_sign_correlation,
)
from substrate_framework.governance import load_yaml
from substrate_framework.sine_gordon import breather_field
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "dceed4b3d8f59daa75bbd6b31e9a726de99f180e252accb19f7d0ae625c5c9bd"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P050-NC3")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode("utf-8")
    reproduction = load_yaml(args.source_reproduction)
    ledger.check(
        "the audited NC3 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    ledger.check(
        "the predecessor executable exits successfully with all eighteen checks",
        reproduction.get("sha256") == EXPECTED_SOURCE_SHA256
        and reproduction.get("exit_code") == 0
        and reproduction.get("terminal_tally") == "ALL 18 CHECKS PASS",
    )

    u, v = sp.symbols("u v", real=True)
    density = boundary_sign_correlation_density(u, v)
    ledger.check(
        "the canonical density is the sign correlation of distinct boundary traces",
        density == sp.sign(u) * v,
    )
    ledger.check(
        "scalar-field sign reversal leaves the density unchanged",
        sp.simplify(boundary_sign_correlation_density(-u, -v) - density) == 0,
    )

    def coordinate_parity_sign_predicate(candidate: object) -> bool:
        spatial_sign = sp.sympify(candidate)
        parity_density = boundary_sign_correlation_density(u, spatial_sign * v)
        return bool(sp.simplify(parity_density + density) == 0)

    ledger.mutation_sensitive(
        "fixed-coordinate spatial-parity derivative sign",
        coordinate_parity_sign_predicate,
        -1,
        [0, 1],
    )
    ledger.check(
        "at a general boundary point parity also reflects the point",
        sp.simplify(
            boundary_sign_correlation_density(u, -v)
            + boundary_sign_correlation_density(u, v)
        )
        == 0,
    )

    right_outward_normal_derivative = -v
    mapped_left_outward_normal_derivative = -v
    ledger.check(
        "a simultaneously parity-mapped half-line normal is not the fixed coordinate channel",
        boundary_sign_correlation_density(u, right_outward_normal_derivative)
        == boundary_sign_correlation_density(
            u,
            mapped_left_outward_normal_derivative,
        )
        and sp.simplify(
            boundary_sign_correlation_density(u, -v) + density
        )
        == 0,
    )

    theta, delta = sp.symbols("theta delta", real=True)
    amplitude = sp.symbols("B", real=True)
    frequency = sp.symbols("omega", positive=True)
    split_integral = (
        sp.integrate(amplitude * sp.sin(theta + delta), (theta, 0, sp.pi))
        - sp.integrate(
            amplitude * sp.sin(theta + delta),
            (theta, sp.pi, 2 * sp.pi),
        )
    ) / frequency
    expected_sine_correlation = 4 * amplitude * sp.cos(delta) / frequency
    ledger.check(
        "direct half-cycle integration fixes the sine-convention correlation",
        sp.simplify(split_integral - expected_sine_correlation) == 0,
    )
    ledger.check(
        "the canonical harmonic API agrees and retains temporal orientation",
        sp.simplify(
            sinusoidal_boundary_sign_correlation(
                2,
                amplitude,
                frequency,
                delta,
            )
            - expected_sine_correlation
        )
        == 0
        and sp.simplify(
            sinusoidal_boundary_sign_correlation(
                -2,
                amplitude,
                frequency,
                delta,
            )
            + expected_sine_correlation
        )
        == 0,
    )

    def harmonic_factor_predicate(candidate: object) -> bool:
        factor = sp.sympify(candidate)
        return bool(
            sp.simplify(
                split_integral
                - factor * amplitude * sp.cos(delta) / frequency
            )
            == 0
        )

    ledger.mutation_sensitive(
        "harmonic half-cycle factor",
        harmonic_factor_predicate,
        4,
        [2, sp.pi],
    )

    def harmonic_frequency_power_predicate(candidate: object) -> bool:
        exponent = sp.sympify(candidate)
        proposed = 4 * amplitude * sp.cos(delta) * frequency**exponent
        return bool(sp.simplify(split_integral - proposed) == 0)

    ledger.mutation_sensitive(
        "harmonic frequency power",
        harmonic_frequency_power_predicate,
        -1,
        [0, 1],
    )

    cosine_split_integral = (
        sp.integrate(amplitude * sp.cos(theta + delta), (theta, 0, sp.pi))
        - sp.integrate(
            amplitude * sp.cos(theta + delta),
            (theta, sp.pi, 2 * sp.pi),
        )
    ) / frequency
    ledger.check(
        "a cosine trace requires the explicit quarter-cycle phase conversion",
        sp.simplify(cosine_split_integral + 4 * amplitude * sp.sin(delta) / frequency)
        == 0
        and sp.simplify(
            cosine_split_integral
            - 4 * amplitude * sp.cos(delta + sp.pi / 2) / frequency
        )
        == 0,
    )
    ledger.check(
        "NC3 prose and executable contain different unshifted trace conventions",
        "* B cos(w t + delta) dt" in source_text
        and "integrand_model = sgn_sin * B * sp.sin(w * t + delta)" in source_text,
    )

    alpha, beta = sp.symbols("alpha beta", real=True)
    ledger.check(
        "a common time-origin phase cancels and only relative phase remains",
        sp.simplify(
            sinusoidal_boundary_sign_correlation(
                1,
                amplitude,
                frequency,
                beta - alpha,
            )
            - 4 * amplitude * sp.cos(beta - alpha) / frequency
        )
        == 0,
    )
    ledger.check(
        "aligned, opposite, and quadrature phases have exact signed values",
        sinusoidal_boundary_sign_correlation(1, amplitude, frequency, 0)
        == 4 * amplitude / frequency
        and sinusoidal_boundary_sign_correlation(1, amplitude, frequency, sp.pi)
        == -4 * amplitude / frequency
        and sinusoidal_boundary_sign_correlation(
            1,
            amplitude,
            frequency,
            sp.pi / 2,
        )
        == 0,
    )

    boundary_change = sp.symbols("Delta_phi", real=True)
    charge_change = right_half_line_topological_charge_change(boundary_change)
    ledger.check(
        "right-half-line winding change is a separately named boundary-field integral",
        charge_change == -boundary_change / (2 * sp.pi),
    )

    def winding_coefficient_predicate(candidate: object) -> bool:
        coefficient = sp.sympify(candidate)
        proposed = coefficient * boundary_change / (2 * sp.pi)
        return bool(sp.simplify(proposed - charge_change) == 0)

    ledger.mutation_sensitive(
        "right-half-line winding orientation coefficient",
        winding_coefficient_predicate,
        -1,
        [0, 1, -2],
    )

    time = sp.symbols("t", real=True)
    period = 2 * sp.pi / frequency
    periodic_time_trace = 2 * sp.sin(frequency * time)
    periodic_field_change = sp.integrate(
        periodic_time_trace,
        (time, 0, period),
    )
    nonzero_correlation = sinusoidal_boundary_sign_correlation(
        2,
        3,
        frequency,
        0,
    )
    ledger.check(
        "nonzero sign correlation does not imply topological charge transfer",
        periodic_field_change == 0
        and right_half_line_topological_charge_change(periodic_field_change) == 0
        and nonzero_correlation == 12 / frequency,
    )
    ledger.check(
        "zero sign correlation does not imply zero boundary winding",
        sinusoidal_boundary_sign_correlation(1, 0, frequency, 0) == 0
        and right_half_line_topological_charge_change(2 * sp.pi) == -1,
    )
    ledger.check(
        "the sign correlation is continuously scalable and is not quantized",
        sinusoidal_boundary_sign_correlation(
            1,
            frequency / 8,
            frequency,
            0,
        )
        == sp.Rational(1, 2),
    )

    x = sp.symbols("x", real=True)
    exact_frequency = sp.Rational(3, 5)
    exact_period = 2 * sp.pi / exact_frequency
    centered = breather_field(x, time, exact_frequency)
    ledger.check(
        "the exact centered rest breather has no coordinate spatial channel at its center",
        sp.simplify(sp.diff(centered, x).subs(x, 0)) == 0,
    )
    shifted = breather_field(x - sp.Rational(1, 3), time, exact_frequency)
    boundary_time = sp.diff(shifted, time).subs(x, sp.Rational(2, 5))
    boundary_space = sp.diff(shifted, x).subs(x, sp.Rational(2, 5))
    boundary_density = boundary_sign_correlation_density(
        boundary_time,
        boundary_space,
    )
    reflected_density = boundary_sign_correlation_density(
        boundary_time.subs(time, exact_period - time),
        boundary_space.subs(time, exact_period - time),
    )
    ledger.check(
        "the exact rest breather correlation is period-antisymmetric at any fixed boundary",
        sp.simplify(boundary_time.subs(time, exact_period - time) - boundary_time)
        == 0
        and sp.simplify(
            boundary_space.subs(time, exact_period - time) + boundary_space
        )
        == 0
        and sp.simplify(reflected_density + boundary_density) == 0,
    )

    queue = load_yaml(args.migration_queue)
    dispositions = {
        unit["source_unit"]: unit["disposition"] for unit in queue["units"]
    }
    ledger.check(
        "NC3's physical dependency set remains outside accepted closure",
        all(
            dispositions[unit] == "pending_adjudication"
            for unit in ("G1", "G2", "NC4", "W1", "W3")
        ),
    )
    ledger.check(
        "observable oddness alone supplies no dynamics, boundary law, or state selection",
        coordinate_parity_sign_predicate(-1)
        and right_outward_normal_derivative == mapped_left_outward_normal_derivative
        and dispositions["W1"] == "pending_adjudication",
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
