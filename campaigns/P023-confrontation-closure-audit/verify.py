#!/usr/bin/env python3
"""Exact EL6 comparator-closure and duplicate-content audit."""

from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.renormalization import transmuted_mass_coordinate
from substrate_framework.verification import CheckLedger


EL6_SHA256 = "f6ea408d674d2fcc88a9bb0d6564b56b21dfde124161f3786724dd1179259f5e"


def source_scanner_detects_assignment(source: str) -> bool:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in (
                    "a",
                    "a_len",
                    "A_GRANULARITY",
                ):
                    if isinstance(node.value, ast.Constant) and isinstance(
                        node.value.value, (int, float)
                    ):
                        return True
    return False


def run(source_file: Path) -> int:
    checks = CheckLedger("EL6-QUALIFICATION")
    checks.check(
        "the audited EL6 source is the hash-pinned candidate unit",
        hashlib.sha256(source_file.read_bytes()).hexdigest() == EL6_SHA256,
    )
    action_speed, length, coefficient, coupling_squared, shape, offset = sp.symbols(
        "Sc a b0 beta2 b kappa_h", positive=True
    )
    prefactor = offset / (48 * sp.pi**3 * shape)
    coordinate = transmuted_mass_coordinate(
        coupling_squared, coefficient, prefactor
    )
    energy = sp.simplify(coordinate * action_speed / length)
    source_energy = (
        offset
        * action_speed
        * sp.exp(-8 * sp.pi**2 / (coefficient * coupling_squared))
        / (48 * sp.pi**3 * shape * length)
    )
    checks.check(
        "EL6's derived-side expression is exactly C-DIM-005 with a renamed prefactor",
        sp.simplify(energy - source_energy) == 0,
    )
    checks.check(
        "all six source quantities remain load-bearing",
        all(
            sp.diff(energy, symbol) != 0
            for symbol in (
                action_speed,
                length,
                coefficient,
                coupling_squared,
                shape,
                offset,
            )
        ),
    )
    target_energy = sp.symbols("E_target", positive=True)
    required_offset = sp.solve(sp.Eq(energy, target_energy), offset)[0]
    checks.check(
        "the required hadronic offset explicitly depends on the target comparator",
        target_energy in required_offset.free_symbols
        and sp.diff(required_offset, target_energy) != 0,
    )
    checks.check(
        "substituting the comparator-derived offset reproduces the target tautologically",
        sp.simplify(energy.subs(offset, required_offset) - target_energy) == 0,
    )
    required_length = sp.solve(sp.Eq(energy, target_energy), length)[0]
    checks.check(
        "the alternative required length also depends on the target comparator",
        target_energy in required_length.free_symbols
        and sp.diff(required_length, target_energy) != 0,
    )
    alternate_offset = sp.symbols("kappa_alt", positive=True)
    checks.check(
        "two admissible offsets give different energies with every other input fixed",
        sp.simplify(energy - energy.subs(offset, alternate_offset)) != 0,
    )

    mass_ratio = 48 * sp.pi**3 * shape
    checks.check(
        "the source mass-ratio form remains conditional on the shape input",
        sp.diff(mass_ratio, shape) == 48 * sp.pi**3,
    )
    observed_ratio = sp.symbols("R_obs", positive=True)
    required_shape = sp.solve(sp.Eq(mass_ratio, observed_ratio), shape)[0]
    checks.check(
        "a measured ratio can calibrate rather than predict the shape input",
        required_shape == observed_ratio / (48 * sp.pi**3),
    )

    checks.check(
        "EL6's assignment scanner detects only its narrow literal syntax",
        source_scanner_detects_assignment("a = 1.0\n")
        and not source_scanner_detects_assignment("a = float('1.0')\n")
        and not source_scanner_detects_assignment("a: float = 1.0\n"),
    )
    checks.check(
        "absence of a mass symbol does not reduce the number of free physical inputs",
        energy.free_symbols
        == {
            action_speed,
            length,
            coefficient,
            coupling_squared,
            shape,
            offset,
        },
    )
    checks.check(
        "pre-existing unresolved inputs remain debt even when no new symbol is added",
        {length, shape, offset} <= energy.free_symbols,
    )

    total = checks.finish()
    print(f"P023 EL6 CLOSURE AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
