#!/usr/bin/env python3
"""Exact one-loop invariant, coordinate, and EL4 scope verifier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.dimensional_analysis import dimensionless_mass_coordinate
from substrate_framework.renormalization import (
    one_loop_inverse_coupling_squared,
    one_loop_transmutation_scale,
    transmuted_mass_coordinate,
)
from substrate_framework.verification import CheckLedger


EL4_SHA256 = "4ae8185505b11d3cf2beffcbb6ec786e4bfbdd57e00cd42b8fc223a28a17cf2f"


@dataclass(frozen=True)
class InvariantCandidate:
    beta_sign: int
    beta_denominator: int
    exponent_numerator: int


def candidate_is_invariant(candidate: InvariantCandidate) -> bool:
    scale, coupling, coefficient = sp.symbols("mu g b0", positive=True)
    beta = (
        candidate.beta_sign
        * coefficient
        * coupling**3
        / (candidate.beta_denominator * sp.pi**2)
    )
    invariant = scale * sp.exp(
        -candidate.exponent_numerator * sp.pi**2 / (coefficient * coupling**2)
    )
    total_log_derivative = sp.simplify(
        scale * sp.diff(invariant, scale) + beta * sp.diff(invariant, coupling)
    )
    return total_log_derivative == 0


def run(source_file: Path) -> int:
    checks = CheckLedger("C-RGE-001/C-DIM-005")
    checks.check(
        "the audited EL4 source is the hash-pinned candidate unit",
        hashlib.sha256(source_file.read_bytes()).hexdigest() == EL4_SHA256,
    )

    scale, reference, coupling, coefficient = sp.symbols(
        "mu mu0 g0 b0", positive=True
    )
    inverse = one_loop_inverse_coupling_squared(
        scale, reference, coupling, coefficient
    )
    target_inverse = (
        1 / coupling**2
        + coefficient * sp.log(scale / reference) / (8 * sp.pi**2)
    )
    checks.check(
        "the package API gives the exact separated one-loop solution",
        sp.simplify(inverse - target_inverse) == 0,
    )
    checks.check(
        "the running solution recovers its boundary coupling",
        sp.simplify(inverse.subs(scale, reference) - 1 / coupling**2) == 0,
    )
    checks.check(
        "the inverse coupling satisfies the declared flow equation",
        sp.simplify(scale * sp.diff(inverse, scale) - coefficient / (8 * sp.pi**2))
        == 0,
    )

    invariant = one_loop_transmutation_scale(reference, coupling, coefficient)
    target_invariant = reference * sp.exp(
        -8 * sp.pi**2 / (coefficient * coupling**2)
    )
    checks.check(
        "the transmutation API retains the reference coupling and beta coefficient",
        invariant == target_invariant
        and {reference, coupling, coefficient} <= invariant.free_symbols,
    )
    checks.check(
        "the transmuted scale is the exact zero of the inverse coupling",
        sp.simplify(
            one_loop_inverse_coupling_squared(
                invariant, reference, coupling, coefficient
            )
        )
        == 0,
    )

    running_scale, running_coupling = sp.symbols("mu g", positive=True)
    invariant_field = one_loop_transmutation_scale(
        running_scale, running_coupling, coefficient
    )
    beta_flow = -coefficient * running_coupling**3 / (16 * sp.pi**2)
    total_derivative = sp.simplify(
        running_scale * sp.diff(invariant_field, running_scale)
        + beta_flow * sp.diff(invariant_field, running_coupling)
    )
    checks.check(
        "RG invariance is the total derivative along the declared flow",
        total_derivative == 0,
    )
    checks.check(
        "the partial reference-scale derivative at fixed coupling is not zero",
        sp.simplify(sp.diff(invariant, reference) - invariant / reference) == 0
        and sp.diff(invariant, reference) != 0,
    )
    checks.mutation_sensitive(
        "beta sign and one-loop normalization",
        candidate_is_invariant,
        InvariantCandidate(-1, 16, 8),
        [
            InvariantCandidate(1, 16, 8),
            InvariantCandidate(-1, 8, 8),
            InvariantCandidate(-1, 16, 4),
        ],
    )

    ratio = sp.simplify(invariant / reference)
    checks.check(
        "positive asymptotically-free inputs put the invariant below the reference scale",
        sp.limit(ratio, coupling, 0, dir="+") == 0
        and sp.limit(ratio, coupling, sp.oo) == 1
        and sp.diff(ratio, coupling).is_positive is True,
    )
    action, speed, length = sp.symbols("S c0 a", positive=True)
    reference_energy = action * speed / length
    coupling_squared = sp.symbols("beta2", positive=True)
    conditional_scale = one_loop_transmutation_scale(
        reference_energy, sp.sqrt(coupling_squared), coefficient
    )
    transmuted_length = sp.simplify(action * speed / conditional_scale)
    checks.check(
        "the declared action-speed reference gives the exact longer scale",
        transmuted_length
        == length * sp.exp(8 * sp.pi**2 / (coefficient * coupling_squared)),
    )

    ratio_coefficient, mass = sp.symbols("q m", positive=True)
    mass_energy_equation = sp.Eq(mass * speed**2, ratio_coefficient * conditional_scale)
    solved_mass = sp.solve(mass_energy_equation, mass)[0]
    coordinate = transmuted_mass_coordinate(
        coupling_squared, coefficient, ratio_coefficient
    )
    checks.check(
        "the declared mass-energy ratio gives the exact mass coordinate",
        dimensionless_mass_coordinate(
            solved_mass, speed, action, length
        )
        == coordinate,
    )
    checks.check(
        "the mass coordinate retains all three dimensionless inputs",
        sp.diff(coordinate, ratio_coefficient) != 0
        and sp.diff(coordinate, coupling_squared) != 0
        and sp.diff(coordinate, coefficient) != 0,
    )
    alternate_ratio = sp.symbols("q_alt", positive=True)
    checks.check(
        "two admissible mass-energy ratios give different masses at fixed scale and coupling",
        sp.simplify(
            coordinate
            - transmuted_mass_coordinate(
                coupling_squared, coefficient, alternate_ratio
            )
        )
        != 0,
    )
    desired_coordinate = sp.symbols("N", positive=True)
    required_ratio = sp.solve(sp.Eq(coordinate, desired_coordinate), ratio_coefficient)[0]
    checks.check(
        "an unpinned mass-energy ratio can reproduce any positive coordinate",
        required_ratio
        == desired_coordinate
        * sp.exp(8 * sp.pi**2 / (coefficient * coupling_squared)),
    )

    slope = 8 * sp.pi**2 / coefficient
    matrix = sp.Matrix([[-1, -slope], [-1, -slope]])
    hadronic_offset, electron_offset = sp.symbols("r_h r_e")
    augmented = matrix.row_join(sp.Matrix([hadronic_offset, electron_offset]))
    checks.check(
        "duplicate coefficient rows impose consistency only when their offsets are fixed",
        matrix.rank() == 1 and augmented.rank() == 2,
    )
    free_length_matrix = sp.Matrix(
        [
            [2, 0, 0],
            [-4, 0, 0],
            [-1, slope, 0],
            [-2, 2 * slope, 0],
            [0, 0, 1],
        ]
    )
    checks.check(
        "EL4's fabricated free-length matrix remains full-column-rank",
        free_length_matrix.rank() == 3
        and free_length_matrix.cols - free_length_matrix.rank() == 0,
    )
    arbitrary_prefactor = sp.Function("q")(coupling_squared)
    checks.check(
        "frontier-form factorization does not determine a dimensionless prefactor",
        sp.diff(
            arbitrary_prefactor
            * sp.exp(-8 * sp.pi**2 / (coefficient * coupling_squared)),
            arbitrary_prefactor,
        )
        != 0,
    )

    total = checks.finish()
    print(f"P021 EL4 EXACT AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
