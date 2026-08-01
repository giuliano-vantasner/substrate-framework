#!/usr/bin/env python3
"""Verify P037's exact TT angular theorem and audit GW2's normalization."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

import sympy as sp

from substrate_framework.tt_angular import (
    conditional_tt_power,
    frobenius_norm_squared,
    harmonic_stf_third_derivative_average,
    integrated_tt_norm_squared,
    transverse_projector,
    tt_project_symmetric,
    waveform_prefactor_for_quadrupole_convention,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "b41bf49ed7c13e22defc4c70003dad400ffcebcb6c04e852883e2e331badc1d7"
)


def _sphere_integral(expression: sp.Expr, theta: sp.Symbol, phi: sp.Symbol) -> sp.Expr:
    return sp.simplify(
        sp.integrate(
            sp.integrate(expression * sp.sin(theta), (phi, 0, 2 * sp.pi)),
            (theta, 0, sp.pi),
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P037-GW2")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    ledger.check(
        "the audited GW2 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    reproduction = subprocess.run(
        [sys.executable, str(args.source_file)],
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    ledger.check("GW2 exits cleanly", reproduction.returncode == 0)
    ledger.check("GW2's declared eight-check tally reproduces", "ALL 8 CHECKS PASS" in reproduction.stdout)
    ledger.check(
        "GW2 itself classifies the retarded waveform as imported",
        "IMPORTED:      the retarded TT quadrupole WAVEFORM" in source_text,
    )
    ledger.check(
        "GW2 itself classifies the Isaacson flux as imported",
        "ISAACSON energy flux" in source_text and "as STANDARD" in source_text,
    )

    theta, phi = sp.symbols("theta phi", real=True)
    direction = sp.Matrix(
        [
            sp.sin(theta) * sp.cos(phi),
            sp.sin(theta) * sp.sin(phi),
            sp.cos(theta),
        ]
    )
    ledger.check(
        "the representative rank-two sphere moment is four pi over three",
        _sphere_integral(direction[0] ** 2, theta, phi) == sp.Rational(4, 3) * sp.pi,
    )
    ledger.check(
        "the independent rank-four representatives fix four pi over fifteen",
        _sphere_integral(direction[0] ** 4, theta, phi) == sp.Rational(4, 5) * sp.pi
        and _sphere_integral(direction[0] ** 2 * direction[1] ** 2, theta, phi)
        == sp.Rational(4, 15) * sp.pi,
    )

    rational_direction = sp.Matrix([2, 3, 6])
    projector = transverse_projector(rational_direction)
    source_tensor = sp.Matrix([[3, 2, 1], [2, -1, 4], [1, 4, 5]])
    projected = tt_project_symmetric(source_tensor, rational_direction)
    ledger.check(
        "the reusable transverse projector is exact and idempotent",
        sp.simplify(projector**2 - projector) == sp.zeros(3)
        and sp.simplify(projector * rational_direction) == sp.zeros(3, 1),
    )
    ledger.check(
        "the reusable TT image is symmetric transverse and traceless",
        projected == projected.T
        and sp.trace(projected) == 0
        and sp.simplify(projected * rational_direction) == sp.zeros(3, 1),
    )

    exact_stf = sp.diag(1, -1, 0)
    angular_integrand = frobenius_norm_squared(
        tt_project_symmetric(exact_stf, direction)
    )
    direct_angular_integral = _sphere_integral(angular_integrand, theta, phi)
    ledger.check(
        "direct sphere integration independently gives the eight-pi-over-five TT reduction",
        direct_angular_integral == sp.Rational(16, 5) * sp.pi,
    )
    ledger.check(
        "the importable integrated formula reproduces the direct angular integral",
        integrated_tt_norm_squared(exact_stf) == direct_angular_integral,
    )
    ledger.check(
        "a pure trace is annihilated rather than assigned positive power",
        integrated_tt_norm_squared(7 * sp.eye(3)) == 0,
    )
    ledger.check(
        "adding a trace leaves the integrated TT contraction unchanged",
        integrated_tt_norm_squared(exact_stf + 11 * sp.eye(3))
        == integrated_tt_norm_squared(exact_stf),
    )

    coupling = sp.symbols("G", positive=True)
    normalized_waveform = 2 * coupling
    declared_flux = 1 / (32 * sp.pi * coupling)
    normalized_power = conditional_tt_power(
        exact_stf, normalized_waveform, declared_flux
    )
    normalized_expected = coupling / 5 * frobenius_norm_squared(exact_stf)
    ledger.check(
        "the one-fifth coefficient follows conditionally from both declared prefactors",
        sp.simplify(normalized_power - normalized_expected) == 0,
    )

    def normalized_prefactors_match(candidate: object) -> bool:
        wave, flux = candidate  # type: ignore[misc]
        result = conditional_tt_power(exact_stf, wave, flux)
        return sp.simplify(result - normalized_expected) == 0

    ledger.mutation_sensitive(
        "the conditional coefficient depends on the waveform and flux normalizations",
        normalized_prefactors_match,
        (2 * coupling, declared_flux),
        [
            (coupling, declared_flux),
            (2 * coupling, 1 / (16 * sp.pi * coupling)),
            (4 * coupling, declared_flux),
        ],
    )

    triple_stf = 3 * exact_stf
    triple_waveform = waveform_prefactor_for_quadrupole_convention(
        normalized_waveform, 3
    )
    triple_power = conditional_tt_power(triple_stf, triple_waveform, declared_flux)
    gw2_power_in_its_written_convention = conditional_tt_power(
        triple_stf, normalized_waveform, declared_flux
    )
    ledger.check(
        "Q equals three I-STF only when its waveform coefficient is divided by three",
        triple_waveform == 2 * coupling / 3,
    )
    ledger.check(
        "normalized and triple-normalized quadrupoles then give identical power",
        sp.simplify(triple_power - normalized_power) == 0,
    )
    ledger.check(
        "GW2's written Q and waveform conventions overstate the same power by nine",
        sp.simplify(gw2_power_in_its_written_convention - 9 * normalized_power) == 0,
    )
    ledger.check(
        "the triple-normalized convention carries G over forty-five",
        sp.simplify(
            triple_power - coupling / 45 * frobenius_norm_squared(triple_stf)
        )
        == 0,
    )

    def convention_covariant(candidate: object) -> bool:
        scale, wave = candidate  # type: ignore[misc]
        result = conditional_tt_power(scale * exact_stf, wave, declared_flux)
        return sp.simplify(result - normalized_power) == 0

    ledger.mutation_sensitive(
        "quadrupole convention conversion",
        convention_covariant,
        (3, 2 * coupling / 3),
        [
            (3, 2 * coupling),
            (2, 2 * coupling / 3),
            (3, coupling / 3),
        ],
    )

    time, frequency = sp.symbols("t omega", positive=True, real=True)
    cosine = sp.diag(2, -2, 0)
    sine = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    harmonic = cosine * sp.cos(frequency * time) + sine * sp.sin(frequency * time)
    direct_cycle_average = sp.simplify(
        frequency
        / (2 * sp.pi)
        * sp.integrate(
            frobenius_norm_squared(harmonic.diff(time, 3)),
            (time, 0, 2 * sp.pi / frequency),
        )
    )
    ledger.check(
        "the exact harmonic cycle average is performed rather than left symbolic",
        sp.simplify(
            direct_cycle_average
            - harmonic_stf_third_derivative_average(cosine, sine, frequency)
        )
        == 0,
    )
    ledger.check(
        "GW2's source explicitly leaves its angle-bracket time average symbolic",
        "time/cycle\n                 average (kept symbolic" in source_text,
    )

    mass, radius = sp.symbols("mu a", positive=True, real=True)
    separation = sp.Matrix(
        [radius * sp.cos(frequency * time), radius * sp.sin(frequency * time), 0]
    )
    circular_stf = sp.simplify(
        mass * (separation * separation.T - radius**2 * sp.eye(3) / 3)
    )
    circular_third = sp.simplify(circular_stf.diff(time, 3))
    circular_norm = 32 * mass**2 * radius**4 * frequency**6
    ledger.check(
        "a circular two-body relative coordinate has the exact constant third-derivative norm",
        sp.trigsimp(frobenius_norm_squared(circular_third) - circular_norm) == 0,
    )
    ledger.check(
        "the circular result is invariant under the two quadrupole conventions",
        sp.trigsimp(
            conditional_tt_power(circular_third, normalized_waveform, declared_flux)
            - conditional_tt_power(
                3 * circular_third, triple_waveform, declared_flux
            )
        )
        == 0,
    )

    nonzero_pure_trace = 5 * sp.eye(3)
    ledger.check(
        "zero TT power means zero STF part, not zero raw tensor",
        nonzero_pure_trace != sp.zeros(3)
        and conditional_tt_power(
            nonzero_pure_trace, normalized_waveform, declared_flux
        )
        == 0,
    )
    ledger.check(
        "angular algebra does not derive the imported field, flux, or lowest-multipole premise",
        "IMPORTED -- the retarded TT waveform and the Isaacson flux" in source_text
        and "monopole/dipole forbidden" in source_text,
    )

    count = ledger.finish()
    print(f"P037 GW2 TT-ANGULAR NORMALIZATION AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
