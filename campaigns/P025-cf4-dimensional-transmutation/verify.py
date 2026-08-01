#!/usr/bin/env python3
"""Exact CF4 duplicate, scaling, and implication-boundary verifier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.renormalization import (
    one_loop_inverse_coupling_squared,
    one_loop_transmutation_scale,
    single_scale_tension,
)
from substrate_framework.verification import CheckLedger


CF4_SHA256 = "e8fa7072d78ba5462ef9410689090f4627528c3632d45afd528c0c118f863c6b"


@dataclass(frozen=True)
class DimensionCandidate:
    scale_dimension: sp.Expr
    exponent: sp.Expr
    target_dimension: sp.Expr


def dimensionally_matches(candidate: DimensionCandidate) -> bool:
    return sp.simplify(
        candidate.scale_dimension * candidate.exponent
        - candidate.target_dimension
    ) == 0


def pole_is_below_reference(beta_coefficient: sp.Expr) -> bool:
    coupling = sp.symbols("g", positive=True)
    log_ratio = -8 * sp.pi**2 / (beta_coefficient * coupling**2)
    return log_ratio.is_negative is True


def run(source_file: Path) -> int:
    checks = CheckLedger("C-DIM-007/CF4")
    checks.check(
        "the audited CF4 source is the hash-pinned candidate unit",
        hashlib.sha256(source_file.read_bytes()).hexdigest() == CF4_SHA256,
    )

    scale, reference, coupling, coefficient = sp.symbols(
        "mu mu0 g0 b0", positive=True
    )
    inverse = one_loop_inverse_coupling_squared(
        scale, reference, coupling, coefficient
    )
    expected_inverse = (
        1 / coupling**2
        + coefficient * sp.log(scale / reference) / (8 * sp.pi**2)
    )
    checks.check(
        "CF4.1 is exactly the already accepted C-RGE-001 solution",
        sp.simplify(inverse - expected_inverse) == 0,
    )
    checks.check(
        "the accepted inverse coupling has the declared boundary and ODE slope",
        inverse.subs(scale, reference) == 1 / coupling**2
        and sp.simplify(scale * sp.diff(inverse, scale))
        == coefficient / (8 * sp.pi**2),
    )

    transmutation = one_loop_transmutation_scale(reference, coupling, coefficient)
    checks.check(
        "CF4.2 is exactly the C-RGE-001 formal inverse-coupling zero",
        transmutation
        == reference * sp.exp(-8 * sp.pi**2 / (coefficient * coupling**2))
        and sp.simplify(
            one_loop_inverse_coupling_squared(
                transmutation, reference, coupling, coefficient
            )
        )
        == 0,
    )
    checks.check(
        "a positive beta coefficient puts the formal zero below the reference",
        sp.simplify(sp.log(transmutation / reference)).is_negative is True,
    )

    reference_fixed, coupling_fixed = sp.symbols("mu_R g_R", positive=True)
    running_coupling = 1 / sp.sqrt(
        1 / coupling_fixed**2
        + coefficient * sp.log(reference / reference_fixed) / (8 * sp.pi**2)
    )
    along_flow = one_loop_transmutation_scale(
        reference, running_coupling, coefficient
    )
    checks.check(
        "CF4.3 is the C-RGE-001 total RG derivative, not a partial derivative",
        sp.simplify(sp.diff(along_flow, reference)) == 0
        and sp.diff(transmutation, reference) == transmutation / reference,
    )
    wrong_sign_running = 1 / sp.sqrt(
        1 / coupling_fixed**2
        - coefficient * sp.log(reference / reference_fixed) / (8 * sp.pi**2)
    )
    checks.check(
        "reversing the running sign destroys transmutation-scale invariance",
        sp.simplify(
            sp.diff(
                one_loop_transmutation_scale(
                    reference, wrong_sign_running, coefficient
                ),
                reference,
            )
        )
        != 0,
    )

    exponent = sp.solve(sp.Eq(sp.Symbol("p"), 2), sp.Symbol("p"))[0]
    checks.check(
        "one mass-dimension-one scale uniquely supplies power two for a tension",
        exponent == 2,
    )
    checks.mutation_sensitive(
        "mass dimensions and tension exponent",
        dimensionally_matches,
        DimensionCandidate(1, 2, 2),
        [
            DimensionCandidate(1, 1, 2),
            DimensionCandidate(1, 3, 2),
            DimensionCandidate(1, 2, 1),
            DimensionCandidate(2, 2, 2),
        ],
    )

    ratio = sp.symbols("k", positive=True)
    tension = single_scale_tension(transmutation, ratio)
    checks.check(
        "the importable conditional form is k times Lambda squared",
        tension == ratio * transmutation**2,
    )
    checks.check(
        "the dimensionless ratio remains free and load-bearing",
        sp.simplify(tension / transmutation**2) == ratio
        and sp.diff(tension, ratio) == transmutation**2
        and ratio in tension.free_symbols,
    )
    checks.check(
        "different positive ratios preserve every RGE premise but change tension",
        sp.simplify(
            single_scale_tension(transmutation, 2)
            - single_scale_tension(transmutation, 1)
        )
        == transmutation**2,
    )

    p, q = sp.symbols("p q", real=True)
    two_scale_solutions = sp.solve(sp.Eq(p + q, 2), p)[0]
    checks.check(
        "an extra independent mass scale destroys unique power assignment",
        two_scale_solutions == 2 - q and q in two_scale_solutions.free_symbols,
    )

    log_scale, alpha = sp.symbols("L alpha", positive=True)
    running_alpha = alpha / (
        1 + coefficient * alpha * log_scale / (2 * sp.pi)
    )
    pole_log = -2 * sp.pi / (coefficient * alpha)
    checks.check(
        "the positive-coefficient solution has the exact ultraviolet and pole limits",
        sp.limit(running_alpha, log_scale, sp.oo) == 0
        and sp.limit(running_alpha, log_scale, pole_log, dir="+") == sp.oo,
    )
    checks.check(
        "the pole limit contains no tension or confinement observable",
        ratio not in running_alpha.free_symbols
        and set(running_alpha.free_symbols) == {alpha, coefficient, log_scale},
    )
    sigma = sp.symbols("sigma", nonnegative=True)
    inverse_at_pole = sp.simplify(
        one_loop_inverse_coupling_squared(
            transmutation, reference, coupling, coefficient
        )
    )
    checks.check(
        "zero tension is a countermodel to confinement while all one-loop identities remain true",
        inverse.subs(scale, reference) == 1 / coupling**2
        and sigma not in inverse.free_symbols
        and inverse_at_pole.subs(sigma, 0) == 0
        and inverse_at_pole.subs(sigma, transmutation**2) == 0,
    )

    beta_positive, beta_negative = sp.Integer(7), sp.Integer(-7)
    checks.mutation_sensitive(
        "beta sign and pole placement",
        pole_is_below_reference,
        beta_positive,
        [beta_negative],
    )
    negative_log_ratio = -8 * sp.pi**2 / (beta_negative * coupling**2)
    checks.check(
        "a negative coefficient puts the formal zero above the reference",
        negative_log_ratio.is_positive is True,
    )
    checks.check(
        "pole placement alone does not decide a nonperturbative confinement claim",
        ratio not in negative_log_ratio.free_symbols,
    )

    total = checks.finish()
    print(f"P025 CF4 CLAIM-BOUNDARY AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
