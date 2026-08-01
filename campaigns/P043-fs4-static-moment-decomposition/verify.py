#!/usr/bin/env python3
"""Verify FS4's duplicate constant-offset result and audit its scope."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

import sympy as sp

from substrate_framework.governance import load_yaml
from substrate_framework.separable_moments import (
    axisymmetric_separable_moments,
    axisymmetric_separable_stf_derivative,
    axisymmetric_stf_tt_readout,
)
from substrate_framework.sine_gordon import breather_energy_second_moment
from substrate_framework.tt_angular import conditional_tt_power
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "2f3c1b02bbad06bded6a38d0e1c203b2ba9c71c63adea34645d041b820feb129"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument(
        "--source-reproduction",
        type=Path,
        help="reuse a hash-matched durable reproduction record",
    )
    args = parser.parse_args()
    ledger = CheckLedger("P043-FS4")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    source_words = " ".join(source_text.split())
    ledger.check(
        "the audited FS4 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    if args.source_reproduction is None:
        reproduction = subprocess.run(
            [sys.executable, str(args.source_file)],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        reproduction_exit = reproduction.returncode
        reproduction_tally = reproduction.stdout
    else:
        reproduction_record = load_yaml(args.source_reproduction)
        if reproduction_record.get("sha256") != EXPECTED_SOURCE_SHA256:
            raise ValueError("source reproduction record does not match FS4 hash")
        reproduction_exit = reproduction_record.get("exit_code")
        reproduction_tally = str(reproduction_record.get("terminal_tally", ""))
    ledger.check("FS4 exits cleanly", reproduction_exit == 0)
    ledger.check(
        "FS4's declared five-check tally reproduces",
        "ALL 5 CHECKS PASS" in reproduction_tally,
    )
    ledger.check(
        "FS4 uses the current trapezoid API with an older-version fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source_text,
    )

    time = sp.symbols("t", real=True)
    constant = sp.symbols("c", real=True)
    moment = sp.Function("mu")(time)
    for order in (1, 2, 3, 4):
        ledger.check(
            f"accepted moment derivatives of order {order} ignore an arbitrary constant offset",
            sp.diff(moment + constant, time, order)
            == sp.diff(moment, time, order),
        )

    mass, variance = sp.symbols("M sigma2", positive=True, real=True)
    full = axisymmetric_separable_moments(mass, moment + constant, variance)
    modulation = axisymmetric_separable_moments(mass, moment, variance)
    for order in (1, 2, 3):
        ledger.check(
            f"normalized and triple separable STF derivatives of order {order} ignore the offset",
            sp.simplify(
                full.trace_free_second_moment.diff(time, order)
                - modulation.trace_free_second_moment.diff(time, order)
            )
            == sp.zeros(3)
            and sp.simplify(
                full.triple_normalized_quadrupole.diff(time, order)
                - modulation.triple_normalized_quadrupole.diff(time, order)
            )
            == sp.zeros(3),
        )

    third = sp.diff(moment, time, 3)
    coupling = sp.symbols("G", positive=True, real=True)
    flux = 1 / (32 * sp.pi * coupling)
    normalized_third = axisymmetric_separable_stf_derivative(third)
    full_power = conditional_tt_power(normalized_third, 2 * coupling, flux)
    shifted_third = sp.diff(moment + constant, time, 3)
    shifted_power = conditional_tt_power(
        axisymmetric_separable_stf_derivative(shifted_third),
        2 * coupling,
        flux,
    )
    ledger.check(
        "C-GW-004 conditional power is exactly invariant under the constant offset",
        sp.simplify(full_power - shifted_power) == 0
        and sp.simplify(full_power - 2 * coupling * third**2 / 15) == 0,
    )
    inclination = sp.symbols("i", real=True)
    full_readout = axisymmetric_stf_tt_readout(
        sp.diff(moment + constant, time, 2),
        inclination,
    )
    modulation_readout = axisymmetric_stf_tt_readout(
        sp.diff(moment, time, 2),
        inclination,
    )
    ledger.check(
        "C-GW-004 conditional TT readouts are exactly invariant under the constant offset",
        sp.simplify(
            full_readout.projected_tensor - modulation_readout.projected_tensor
        )
        == sp.zeros(3)
        and sp.simplify(
            full_readout.normalized_plus_coordinate
            - modulation_readout.normalized_plus_coordinate
        )
        == 0,
    )

    epsilon = sp.symbols("epsilon", nonzero=True, real=True)
    cubic_offset = epsilon * time**3
    ledger.check(
        "a time-dependent cubic offset breaks third-derivative and power invariance",
        sp.diff(moment + cubic_offset, time, 3) - third == 6 * epsilon
        and sp.simplify(
            conditional_tt_power(
                axisymmetric_separable_stf_derivative(
                    sp.diff(moment + cubic_offset, time, 3)
                ),
                2 * coupling,
                flux,
            )
            - full_power
        )
        != 0,
    )
    quadratic_offset = epsilon * time**2
    ledger.check(
        "a time-dependent quadratic offset breaks second-derivative waveform invariance",
        sp.diff(moment + quadratic_offset, time, 2)
        - sp.diff(moment, time, 2)
        == 2 * epsilon,
    )
    parameter = sp.symbols("omega", positive=True, real=True)
    parameter_constant = sp.Function("c")(parameter)
    ledger.check(
        "parameter dependence alone remains time constant at fixed family member",
        sp.diff(moment + parameter_constant, time, 3) == third,
    )

    mean, candidate_piece = sp.symbols("mu_bar candidate_piece", real=True)
    ledger.check(
        "a constant mean admits infinitely many algebraic two-piece decompositions",
        sp.simplify(candidate_piece + (mean - candidate_piece) - mean) == 0
        and sp.diff(candidate_piece + (mean - candidate_piece), time, 3) == 0,
    )
    ledger.check(
        "constant cancellation cannot select one piece as a form factor",
        sp.simplify(
            sp.diff(candidate_piece, time, 3)
            - sp.diff(2 * candidate_piece, time, 3)
        )
        == 0
        and candidate_piece != 2 * candidate_piece,
    )

    special_frequency = sp.sqrt(2) / 2
    exact_moment = breather_energy_second_moment(special_frequency, time)
    exact_shifted = exact_moment + constant
    ledger.check(
        "the accepted exact breather specialization needs no sampled replay for offset cancellation",
        sp.simplify(
            sp.diff(exact_shifted, time, 3) - sp.diff(exact_moment, time, 3)
        )
        == 0,
    )

    ledger.check(
        "FS4 imports rather than computes the purported form-factor value",
        "NEG_WPP = 13.957728" in source_text
        and "phase3; STATIC" in source_text
        and "def neg_wpp" not in source_text.lower(),
    )
    ledger.check(
        "FS4 tests form-factor membership only by an inequality against a sampled mean",
        "wpp_inside_mubar = (NEG_WPP < mu_bar_num) and (NEG_WPP > 0)" in source_text,
    )
    ledger.check(
        "FS4's symbolic decomposition declares two arbitrary constants before differentiating",
        "pot_mom = sp.symbols(\"pot_mom\", real=True)" in source_text
        and "mu_bar_decomp = wpp_sym + pot_mom" in source_text
        and "ddd_mubar = sp.diff(mu_bar_decomp, t, 3)" in source_text,
    )
    ledger.check(
        "FS4's full-versus-modulation numerical route repeats one finite-difference operator",
        "P_full_num = power_from_mu(mu_series, dt, EDGE)" in source_text
        and "P_delta_num = power_from_mu(delta_mu_series, dt, EDGE)" in source_text,
    )
    ledger.check(
        "FS4 retains FS3's triple-tensor coefficient and strict-positivity defects",
        "Qxx = 2.0 * mu_series - 2.0 * I_PERP" in source_text
        and "return (Geff / 5.0)" in source_text
        and "both_positive = np.min(P_full_num) > 0.0" in source_text,
    )
    ledger.check(
        "FS4's wrong-attribution guard rejects a fabricated formula rather than deriving dynamics",
        "P_wrong = (Geff / 5.0) * (NEG_WPP**2) * (2.0 * WB_val)**6" in source_text
        and "fabricated" in source_words,
    )
    ledger.check(
        "FS4's claimed T2C and G4 ceiling lift has no accepted dependency closure",
        "T2-C's & G4's structural-only/by-hand ceilings" in source_text
        and "partial_mu T" not in source_text
        and "Euler-Lagrange" not in source_text,
    )

    count = ledger.finish()
    print(f"P043 FS4 STATIC-MOMENT DUPLICATION AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
