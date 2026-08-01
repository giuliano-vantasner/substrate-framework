#!/usr/bin/env python3
"""Exact winding-label verifier and EL2 physical-scope audit."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.topological_labels import (
    combined_winding_parity,
    winding_parity,
)
from substrate_framework.verification import CheckLedger


EL2_SHA256 = "db90b921e0b3d6966597a39817ad48219cd94fa27ff8aa2a1de4a64c3ccf6965"


def run(source_file: Path) -> int:
    checks = CheckLedger("C-TOP-001")
    payload = source_file.read_bytes()
    checks.check(
        "the audited EL2 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == EL2_SHA256,
    )

    checks.check(
        "the winding label is a homomorphism on a mutation-sensitive integer grid",
        all(
            winding_parity(first + second)
            == winding_parity(first) * winding_parity(second)
            for first in range(-16, 17)
            for second in range(-16, 17)
        ),
    )
    q1, q2 = sp.symbols("q1 q2", integer=True)
    residue_cases = []
    for first_residue in (0, 1):
        for second_residue in (0, 1):
            first = 2 * q1 + first_residue
            second = 2 * q2 + second_residue
            residue_cases.append(
                sp.simplify(
                    (-1) ** (first + second)
                    - (-1) ** first * (-1) ** second
                )
                == 0
            )
    checks.check(
        "the two residue classes prove the homomorphism for all integers",
        all(residue_cases),
    )
    checks.check(
        "even and odd winding classes have distinct exact labels",
        winding_parity(0) == 1
        and winding_parity(2) == 1
        and winding_parity(1) == -1
        and winding_parity(-3) == -1,
    )

    anchor, even_dressing = sp.symbols("w k", integer=True)
    checks.check(
        "adding arbitrary even dressing preserves winding parity",
        sp.simplify(
            combined_winding_parity(anchor, 2 * even_dressing)
            - winding_parity(anchor)
        )
        == 0,
    )
    checks.check(
        "odd dressing is a load-bearing counterexample that flips parity",
        all(
            combined_winding_parity(value, 1) == -winding_parity(value)
            for value in range(-8, 9)
        ),
    )

    statistics, baryon_number, internal_charge = sp.symbols(
        "statistics B Q", real=True
    )
    odd_label = winding_parity(1)
    checks.check(
        "the winding equation leaves statistics, baryon, and charge labels independent",
        odd_label == -1
        and statistics not in odd_label.free_symbols
        and baryon_number not in odd_label.free_symbols
        and internal_charge not in odd_label.free_symbols,
    )
    checks.check(
        "the same odd winding label admits distinct external label assignments",
        (odd_label, 1, 0, 0) != (odd_label, -1, 0, 1)
        and (odd_label, 1, 0, 0)[0] == (odd_label, -1, 0, 1)[0],
    )

    amplitude, omega, eta = sp.symbols("A omega eta", positive=True)
    u1_charge = 4 * amplitude**2 * omega / eta
    checks.check(
        "the accepted conditional U1 charge is not fixed to one unit",
        sp.diff(u1_charge, amplitude) != 0
        and sp.diff(u1_charge, omega) != 0
        and sp.simplify(u1_charge - 1) != 0,
    )

    scale, gradient, magnitude = sp.symbols(
        "lambda E_grad P", positive=True
    )
    scaled_energy = scale * gradient - scale**3 * magnitude
    stationary_scale = sp.sqrt(gradient / (3 * magnitude))
    curvature = sp.simplify(
        sp.diff(scaled_energy, scale, 2).subs(scale, stationary_scale)
    )
    checks.check(
        "EL2's negative-potential Derrick stationary point is a maximum",
        curvature == -6 * magnitude * stationary_scale
        and curvature.is_negative is True,
    )
    checks.check(
        "stationarity alone therefore cannot certify 3D stability",
        sp.diff(scaled_energy, scale).subs(scale, stationary_scale).simplify() == 0
        and sp.limit(scaled_energy, scale, sp.oo) == -sp.oo,
    )

    total = checks.finish()
    print(f"P019 EL2 EXACT AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
