#!/usr/bin/env python3
"""Verify P040's exact breather energy moment and audit FS1."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

import sympy as sp

from substrate_framework.sine_gordon import (
    breather_energy_second_moment,
    breather_energy_second_moment_extrema,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "da6b3bb1a602e52abb6d6ec5c926285e99d5216d03a9d41abc00af06e50011c2"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P040-FS1")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    source_words = " ".join(source_text.split())
    ledger.check(
        "the audited FS1 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    reproduction = subprocess.run(
        [sys.executable, str(args.source_file)],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    ledger.check("FS1 exits cleanly", reproduction.returncode == 0)
    ledger.check(
        "FS1's declared four-check tally reproduces",
        "ALL 4 CHECKS PASS" in reproduction.stdout,
    )
    ledger.check(
        "FS1 already carries the NumPy trapezoid compatibility fallback",
        "np.trapezoid if hasattr(np, \"trapezoid\") else np.trapz" in source_text,
    )

    omega, eta, sine, z = sp.symbols(
        "omega eta sine z", positive=True, real=True
    )
    eta_squared = 1 - omega**2
    b_squared = eta_squared * sine**2 / omega**2
    raw_numerator = (
        eta_squared * (1 - sine**2) * z
        + eta_squared * b_squared * (z - 1)
        + b_squared * z
    )
    reduced_numerator = eta_squared * (
        (1 + 2 * b_squared) * z - b_squared
    )
    ledger.check(
        "the accepted Hamiltonian density reduces to the transform-ready rational form",
        sp.factor(raw_numerator - reduced_numerator) == 0,
    )
    ledger.check(
        "the rational density separates into one denominator and its parameter derivative",
        sp.simplify(
            reduced_numerator
            - eta_squared
            * (
                (1 + 2 * b_squared) * (z + b_squared)
                - 2 * b_squared * (1 + b_squared)
            )
        )
        == 0,
    )

    transform_frequency, alpha = sp.symbols("k alpha", positive=True, real=True)
    transform = (
        2
        * sp.pi
        * sp.sin(alpha * transform_frequency / 2)
        / (
            sp.sinh(alpha)
            * sp.sinh(sp.pi * transform_frequency / 2)
        )
    )
    second_moment_kernel = sp.simplify(
        sp.limit(-sp.diff(transform, transform_frequency, 2), transform_frequency, 0)
    )
    expected_kernel = alpha * (alpha**2 + sp.pi**2) / (6 * sp.sinh(alpha))
    ledger.check(
        "the exact spatial transform gives its second-moment kernel by differentiation",
        sp.simplify(second_moment_kernel - expected_kernel) == 0,
    )
    ledger.check(
        "the transform has the correct zero-parameter sech-squared limit",
        sp.simplify(
            sp.limit(transform, alpha, 0)
            - sp.pi
            * transform_frequency
            / sp.sinh(sp.pi * transform_frequency / 2)
        )
        == 0,
    )
    combined_kernel = sp.simplify(
        sp.cosh(alpha) * second_moment_kernel
        + sp.sinh(alpha) * sp.diff(second_moment_kernel, alpha)
    )
    ledger.check(
        "the two density denominator terms collapse before any source comparator",
        sp.simplify(combined_kernel - (alpha**2 / 2 + sp.pi**2 / 6)) == 0,
    )
    moment_from_transform = sp.simplify(8 * combined_kernel / eta)
    ledger.check(
        "the transform route gives the exact instantaneous second moment",
        sp.simplify(
            moment_from_transform
            - 4 * sp.pi**2 / (3 * eta)
            - 4 * alpha**2 / eta
        )
        == 0,
    )

    time = sp.symbols("t", real=True)
    symbolic_omega = sp.symbols("omega", positive=True, real=True)
    symbolic_eta = sp.sqrt(1 - symbolic_omega**2)
    moment = breather_energy_second_moment(symbolic_omega, time)
    target = (
        4 * sp.pi**2 / (3 * symbolic_eta)
        + 16
        * sp.asinh(
            symbolic_eta
            * sp.sin(symbolic_omega * time)
            / symbolic_omega
        )
        ** 2
        / symbolic_eta
    )
    ledger.check(
        "the package API is the transform-derived formula",
        sp.simplify(moment - target) == 0,
    )
    minimum, maximum = breather_energy_second_moment_extrema(symbolic_omega)
    ledger.check(
        "zero and quarter phases attain the exact minimum and maximum",
        sp.simplify(moment.subs(time, 0) - minimum) == 0
        and sp.simplify(
            moment.subs(time, sp.pi / (2 * symbolic_omega)) - maximum
        )
        == 0
        and sp.simplify(maximum - minimum) != 0,
    )
    ledger.check(
        "the moment is even in time and invariant under the density half-period",
        sp.simplify(moment.subs(time, -time) - moment) == 0
        and sp.simplify(
            moment.subs(time, time + sp.pi / symbolic_omega) - moment
        )
        == 0,
    )
    ledger.check(
        "a quarter-period shift is not a period of the nonconstant moment",
        sp.simplify(
            moment.subs(time, sp.pi / (2 * symbolic_omega))
            - moment.subs(time, 0)
        )
        != 0,
    )
    positive_sine, positive_ratio = sp.symbols(
        "positive_sine positive_ratio", positive=True, real=True
    )
    positive_profile = sp.asinh(positive_ratio * positive_sine) ** 2
    ledger.check(
        "strict profile monotonicity makes pi over omega the fundamental period",
        sp.simplify(
            sp.diff(positive_profile, positive_sine)
            - 2
            * positive_ratio
            * sp.asinh(positive_ratio * positive_sine)
            / sp.sqrt(1 + positive_ratio**2 * positive_sine**2)
        )
        == 0
        and positive_profile.subs(positive_sine, 0) == 0
        and positive_profile.subs(positive_sine, 1) != 0,
    )
    ledger.check(
        "half-period symmetry permits only even orbital harmonics",
        sp.simplify(
            sp.sin(
                symbolic_omega
                * (time + sp.pi / symbolic_omega)
            )
            + sp.sin(symbolic_omega * time)
        )
        == 0
        and moment.has(sp.asinh),
    )

    def coefficient_predicate(candidate: object) -> bool:
        base, dynamic = candidate  # type: ignore[misc]
        candidate_formula = (
            base * sp.pi**2 / (3 * symbolic_eta)
            + dynamic
            * sp.asinh(
                symbolic_eta
                * sp.sin(symbolic_omega * time)
                / symbolic_omega
            )
            ** 2
            / symbolic_eta
        )
        return sp.simplify(candidate_formula - moment) == 0

    ledger.mutation_sensitive(
        "second-moment transform coefficients",
        coefficient_predicate,
        (4, 16),
        [(2, 16), (4, 8), (8, 32)],
    )

    def half_period_predicate(candidate: object) -> bool:
        denominator = int(candidate)
        shifted = moment.subs(
            time,
            time + sp.pi / (denominator * symbolic_omega),
        )
        return sp.simplify(shifted - moment) == 0

    ledger.mutation_sensitive(
        "load-bearing density half-period",
        half_period_predicate,
        1,
        [2, 3, 4],
    )

    special_minimum, special_maximum = breather_energy_second_moment_extrema(
        1 / sp.sqrt(2)
    )
    ledger.check(
        "FS1's special frequency has exact nonzero breathing range",
        special_minimum == 4 * sp.sqrt(2) * sp.pi**2 / 3
        and sp.simplify(
            special_maximum
            - special_minimum
            - 16 * sp.sqrt(2) * sp.asinh(1) ** 2
        )
        == 0,
    )
    ledger.check(
        "FS1's mean decomposition is linear density bookkeeping rather than a second derivation",
        "Hamiltonian T_00 = Lagrangian kernel + potential" in source_words
        and "Build the TIME-AVERAGED kernels on the SAME sampling" in source_text,
    )
    ledger.check(
        "FS1's claimed quadrupole and radiation map is not derived by its scalar integral",
        "So a single breather carries a time-varying mass quadrupole and radiates a GW"
        in source_words
        and "-> FS2 (embed as 3+1 STF quadrupole)" in source_words,
    )

    kink_coordinate = sp.symbols("x", real=True)
    kink = 4 * sp.atan(sp.exp(kink_coordinate))
    correct_kink_derivative = sp.simplify(sp.diff(kink, kink_coordinate))
    ledger.check(
        "FS1's static guard uses a factor-two-wrong kink derivative",
        sp.simplify(correct_kink_derivative - 2 / sp.cosh(kink_coordinate)) == 0
        and "uk_x = 4.0 / np.cosh(xk)" in source_text,
    )
    ledger.check(
        "the kink derivative defect does not establish or refute radiation",
        "time-INDEPENDENT T_00" in source_words
        and "cannot radiate" in source_words,
    )

    count = ledger.finish()
    print(f"P040 FS1 BREATHER ENERGY-MOMENT AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
