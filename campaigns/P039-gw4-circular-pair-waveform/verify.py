#!/usr/bin/env python3
"""Verify P039's circular-pair theorem and audit GW4's source claims."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

import sympy as sp

from substrate_framework.circular_pair import (
    conditional_equal_mass_circular_power,
    conditional_equal_mass_circular_waveform,
    equal_mass_circular_pair_moments,
)
from substrate_framework.sine_gordon import breather_energy
from substrate_framework.tt_angular import (
    conditional_tt_power,
    frobenius_norm_squared,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "0e2637aa188c77a2b976b87e8efffc104eb64c25b759b739d0467d01790c4a15"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P039-GW4")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    source_words = " ".join(source_text.split())
    ledger.check(
        "the audited GW4 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    reproduction = subprocess.run(
        [sys.executable, str(args.source_file)],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    ledger.check(
        "GW4's current NumPy reproduction fails at removed trapz",
        reproduction.returncode != 0
        and "module 'numpy' has no attribute 'trapz'" in reproduction.stderr,
    )
    ledger.check(
        "GW4 reaches only its four pre-power checks",
        reproduction.stdout.count("  PASS") == 4,
    )
    ledger.check(
        "GW4 never reaches a terminal pass tally",
        "ALL " not in reproduction.stdout,
    )

    time, mass, radius, frequency = sp.symbols(
        "t m a Omega", positive=True, real=True
    )
    ledger.check(
        "the imported special breather energy agrees with the accepted exact energy",
        sp.simplify(
            breather_energy(1 / sp.sqrt(2)) - 8 * sp.sqrt(2)
        )
        == 0,
    )
    ledger.check(
        "GW4 declares rather than derives the point-lump orbit model",
        "DECLARED:      point-lump orbit model" in source_text
        and "masses on a circular orbit of radius a" in source_text,
    )
    ledger.check(
        "GW4 explicitly imports the retarded TT waveform",
        "retarded TT quadrupole waveform" in source_text
        and "standard linearized" in source_text,
    )

    moments = equal_mass_circular_pair_moments(mass, radius, frequency, time)
    normalized = moments.trace_free_second_moment
    triple = moments.triple_normalized_quadrupole
    normalized_second = sp.simplify(normalized.diff(time, 2))
    normalized_third = sp.simplify(normalized.diff(time, 3))
    ledger.check(
        "the declared equal pair has constant monopole and zero center-of-mass dipole",
        moments.monopole == 2 * mass and moments.dipole == sp.zeros(3, 1),
    )
    ledger.check(
        "the two source quadrupole conventions differ by exactly three",
        sp.simplify(triple - 3 * normalized) == sp.zeros(3),
    )
    ledger.check(
        "the normalized second-derivative norm has coefficient thirty-two",
        sp.trigsimp(
            frobenius_norm_squared(normalized_second)
            - 32 * mass**2 * radius**4 * frequency**4
        )
        == 0,
    )
    ledger.check(
        "the normalized third-derivative norm has coefficient one hundred twenty-eight",
        sp.trigsimp(
            frobenius_norm_squared(normalized_third)
            - 128 * mass**2 * radius**4 * frequency**6
        )
        == 0,
    )
    ledger.check(
        "the triple-normalized third-derivative norm has coefficient eleven hundred fifty-two",
        sp.trigsimp(
            frobenius_norm_squared(3 * normalized_third)
            - 1152 * mass**2 * radius**4 * frequency**6
        )
        == 0,
    )
    ledger.check(
        "GW4's headline thirty-two and executable eleven-hundred-fifty-two power factors disagree",
        "32 G m^2 a^4 Om^6 / 5" in source_text
        and "1152 m^2 a^4 Om^6" in source_text,
    )

    coupling = sp.symbols("G", positive=True)
    flux = 1 / (32 * sp.pi * coupling)
    corrected_power = conditional_equal_mass_circular_power(
        mass,
        radius,
        frequency,
        2 * coupling,
        flux,
    )
    corrected_expected = (
        sp.Rational(128, 5)
        * coupling
        * mass**2
        * radius**4
        * frequency**6
    )
    source_power = conditional_tt_power(
        3 * normalized_third,
        2 * coupling,
        flux,
    )
    ledger.check(
        "the accepted conditional inputs give corrected circular-pair power 128 G over five",
        sp.trigsimp(corrected_power - corrected_expected) == 0,
    )
    ledger.check(
        "GW4's written triple-Q convention overstates that same conditional power by nine",
        sp.trigsimp(source_power - 9 * corrected_power) == 0,
    )

    def convention_covariant(candidate: object) -> bool:
        scale, waveform = candidate  # type: ignore[misc]
        candidate_power = conditional_tt_power(
            scale * normalized_third,
            waveform,
            flux,
        )
        return sp.trigsimp(candidate_power - corrected_power) == 0

    ledger.mutation_sensitive(
        "circular-pair quadrupole convention conversion",
        convention_covariant,
        (3, 2 * coupling / 3),
        [
            (3, 2 * coupling),
            (2, 2 * coupling / 3),
            (3, coupling / 3),
        ],
    )

    def third_derivative_order(candidate: object) -> bool:
        order = int(candidate)
        derivative = sp.simplify(normalized.diff(time, order))
        return sp.trigsimp(
            frobenius_norm_squared(derivative)
            - 128 * mass**2 * radius**4 * frequency**6
        ) == 0

    ledger.mutation_sensitive(
        "load-bearing third derivative order",
        third_derivative_order,
        3,
        [1, 2, 4],
    )

    inclination, wave, distance = sp.symbols(
        "i A R", positive=True, real=True
    )
    waveform = conditional_equal_mass_circular_waveform(
        mass,
        radius,
        frequency,
        time,
        inclination,
        wave,
        distance,
    )
    phase = 2 * frequency * time
    plus_expected = (
        -2
        * wave
        * mass
        * radius**2
        * frequency**2
        * (1 + sp.cos(inclination) ** 2)
        * sp.cos(phase)
        / distance
    )
    cross_expected = (
        -4
        * wave
        * mass
        * radius**2
        * frequency**2
        * sp.cos(inclination)
        * sp.sin(phase)
        / distance
    )
    ledger.check(
        "the arbitrary-inclination conventional plus coefficient is exact",
        sp.trigsimp(waveform.conventional_plus - plus_expected) == 0,
    )
    ledger.check(
        "the arbitrary-inclination conventional cross coefficient is exact",
        sp.trigsimp(waveform.conventional_cross - cross_expected) == 0,
    )
    ledger.check(
        "normalized basis coordinates retain their square-root-two conversion",
        sp.simplify(
            waveform.normalized_plus_coordinate
            - sp.sqrt(2) * waveform.conventional_plus
        )
        == 0
        and sp.simplify(
            waveform.normalized_cross_coordinate
            - sp.sqrt(2) * waveform.conventional_cross
        )
        == 0,
    )

    face = conditional_equal_mass_circular_waveform(
        mass, radius, frequency, time, 0, wave, distance
    )
    edge = conditional_equal_mass_circular_waveform(
        mass, radius, frequency, time, sp.pi / 2, wave, distance
    )
    ledger.check(
        "face-on plus and cross have equal amplitudes in quadrature at twice orbital frequency",
        sp.trigsimp(
            face.conventional_plus
            + 4
            * wave
            * mass
            * radius**2
            * frequency**2
            * sp.cos(phase)
            / distance
        )
        == 0
        and sp.trigsimp(
            face.conventional_cross
            + 4
            * wave
            * mass
            * radius**2
            * frequency**2
            * sp.sin(phase)
            / distance
        )
        == 0,
    )
    ledger.check(
        "edge-on cross vanishes while plus retains half the face-on amplitude",
        edge.conventional_cross == 0
        and sp.trigsimp(2 * edge.conventional_plus - face.conventional_plus) == 0,
    )

    static = equal_mass_circular_pair_moments(mass, radius, 0, time)
    ledger.check(
        "a static pair has exactly zero third moment derivative",
        static.trace_free_second_moment.diff(time, 3) == sp.zeros(3),
    )
    drift = sp.Matrix([sp.symbols("v", real=True) * time, 0, 0])
    shifted_positions = [
        sp.Matrix([radius, 0, 0]) + drift,
        sp.Matrix([-radius, 0, 0]) + drift,
    ]
    from substrate_framework.conserved_moments import discrete_mass_moments

    translating = discrete_mass_moments([mass, mass], shifted_positions)
    ledger.check(
        "a uniformly translating pair has exactly zero third moment derivative",
        translating.trace_free_second_moment.diff(time, 3) == sp.zeros(3),
    )

    offset = sp.Matrix(sp.symbols("b_x b_y b_z", real=True))
    orbit_position = sp.Matrix(
        [radius * sp.cos(frequency * time), radius * sp.sin(frequency * time), 0]
    )
    translated_orbit = discrete_mass_moments(
        [mass, mass],
        [orbit_position + offset, -orbit_position + offset],
    )
    ledger.check(
        "constant origin translation leaves the third quadrupole derivative unchanged",
        sp.simplify(
            translated_orbit.trace_free_second_moment.diff(time, 3)
            - normalized_third
        )
        == sp.zeros(3),
    )
    ledger.check(
        "the circular paths require nonzero acceleration not supplied by point kinematics",
        sp.simplify(orbit_position.diff(time, 2)) != sp.zeros(3, 1),
    )
    ledger.check(
        "GW4's later FS2 and P3D3 annotations do not derive their premises in this source",
        "SUBSEQUENTLY RESOLVED" in source_text
        and "Phase 13's FS" in source_text
        and "Phase 14's P3D3" in source_text,
    )
    ledger.check(
        "the exact conditional waveform is not a physical breather-binary verdict",
        "finite SIZE of the breather is not resolved here" in source_words
        and "slow-orbit / Newtonian-source" in source_words,
    )

    count = ledger.finish()
    print(f"P039 GW4 CIRCULAR-PAIR WAVEFORM AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
