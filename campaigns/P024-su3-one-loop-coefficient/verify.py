#!/usr/bin/env python3
"""Exact SU(3) invariant and conditional QCD3 coefficient verifier."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.su3 import (
    conditional_one_loop_coefficient,
    fundamental_generators,
    invariants,
    structure_constant,
)
from substrate_framework.verification import CheckLedger


QCD3_SHA256 = "7d7c9a9bc2f04c933fc62484fec3329c0eb7769bb54ba8cd67701da5110af0ca"


@dataclass(frozen=True)
class CoefficientCandidate:
    adjoint_casimir: sp.Expr
    dynkin_index: sp.Expr
    gauge_weight: sp.Expr
    matter_weight: sp.Expr


def candidate_has_qcd3_coefficient(candidate: CoefficientCandidate) -> bool:
    flavors = sp.symbols("n_f")
    value = (
        candidate.gauge_weight * candidate.adjoint_casimir
        - candidate.matter_weight * candidate.dynkin_index * flavors
    )
    return sp.expand(value) == 11 - 2 * flavors / 3


def normalization_matches(scale: sp.Expr) -> bool:
    generators = tuple(scale * generator for generator in fundamental_generators())
    gram = sp.Matrix(
        8, 8, lambda a, b: sp.trace(generators[a] * generators[b])
    )
    commutator = generators[0] * generators[1] - generators[1] * generators[0]
    f123 = sp.simplify(-2 * sp.I * sp.trace(commutator * generators[2]))
    return gram == sp.eye(8) / 2 and f123 == 1


def run(source_file: Path) -> int:
    checks = CheckLedger("C-LIE-001/C-RGE-002")
    checks.check(
        "the audited QCD3 source is the hash-pinned candidate unit",
        hashlib.sha256(source_file.read_bytes()).hexdigest() == QCD3_SHA256,
    )
    generators = fundamental_generators()
    checks.check(
        "the eight fundamental generators are Hermitian and traceless",
        len(generators) == 8
        and all(generator.H == generator for generator in generators)
        and all(sp.trace(generator) == 0 for generator in generators),
    )
    gram = sp.Matrix(
        8, 8, lambda a, b: sp.trace(generators[a] * generators[b])
    )
    checks.check(
        "the declared normalization has exact Dynkin index one-half",
        gram == sp.eye(8) / 2,
    )
    closure = True
    antisymmetry = True
    for a in range(8):
        for b in range(8):
            commutator = generators[a] * generators[b] - generators[b] * generators[a]
            reconstructed = sum(
                (
                    sp.I * structure_constant(a, b, c) * generators[c]
                    for c in range(8)
                ),
                sp.zeros(3),
            )
            closure = closure and sp.simplify(commutator - reconstructed) == sp.zeros(3)
            for c in range(8):
                antisymmetry = antisymmetry and sp.simplify(
                    structure_constant(a, b, c) + structure_constant(b, a, c)
                ) == 0
    checks.check("all generator commutators close exactly", closure)
    checks.check("the computed structure constants are antisymmetric", antisymmetry)
    checks.check(
        "load-bearing standard structure constants have exact values",
        structure_constant(0, 1, 2) == 1
        and structure_constant(3, 4, 7) == sp.sqrt(3) / 2
        and structure_constant(0, 3, 6) == sp.Rational(1, 2),
    )
    values = invariants()
    checks.check(
        "explicit fundamental and adjoint matrices give all three invariants",
        values.dynkin_index == sp.Rational(1, 2)
        and values.fundamental_casimir == sp.Rational(4, 3)
        and values.adjoint_casimir == 3,
    )
    contraction = sp.Matrix(
        8,
        8,
        lambda a, b: sp.simplify(
            sum(
                structure_constant(a, c, d) * structure_constant(b, c, d)
                for c in range(8)
                for d in range(8)
            )
        ),
    )
    checks.check(
        "direct structure-constant contraction independently gives C_A=3",
        contraction == 3 * sp.eye(8),
    )
    checks.check(
        "representation dimensions satisfy the Casimir-index relation",
        values.fundamental_casimir * 3 == values.dynkin_index * 8,
    )
    checks.mutation_sensitive(
        "generator normalization and commutator orientation",
        normalization_matches,
        sp.Integer(1),
        [sp.Integer(2), sp.Integer(-1)],
    )

    flavors, gauge_weight, matter_weight = sp.symbols(
        "n_f c_g c_m", nonnegative=True
    )
    general = conditional_one_loop_coefficient(
        flavors, gauge_weight, matter_weight
    )
    checks.check(
        "the conditional coefficient retains both imported loop weights",
        general == 3 * gauge_weight - matter_weight * flavors / 2
        and {flavors, gauge_weight, matter_weight} <= general.free_symbols,
    )
    standard = conditional_one_loop_coefficient(
        flavors, sp.Rational(11, 3), sp.Rational(4, 3)
    )
    checks.check(
        "declared standard weights specialize to eleven minus two-thirds flavors",
        standard == 11 - 2 * flavors / 3,
    )
    checks.mutation_sensitive(
        "group factors and imported one-loop weights",
        candidate_has_qcd3_coefficient,
        CoefficientCandidate(3, sp.Rational(1, 2), sp.Rational(11, 3), sp.Rational(4, 3)),
        [
            CoefficientCandidate(2, sp.Rational(1, 2), sp.Rational(11, 3), sp.Rational(4, 3)),
            CoefficientCandidate(3, 1, sp.Rational(11, 3), sp.Rational(4, 3)),
            CoefficientCandidate(3, sp.Rational(1, 2), 3, sp.Rational(4, 3)),
            CoefficientCandidate(3, sp.Rational(1, 2), sp.Rational(11, 3), 1),
        ],
    )
    critical = sp.solve(sp.Eq(standard, 0), flavors)[0]
    checks.check(
        "the exact sign crossover is thirty-three halves",
        critical == sp.Rational(33, 2),
    )
    checks.check(
        "integer flavors zero through sixteen give a positive coefficient",
        all(standard.subs(flavors, count) > 0 for count in range(17)),
    )
    checks.check(
        "integer flavors seventeen and above begin with negative coefficient",
        all(standard.subs(flavors, count) < 0 for count in range(17, 20)),
    )
    checks.check(
        "six declared flavors give the conditional coefficient seven",
        standard.subs(flavors, 6) == 7,
    )
    abelian = -sp.Rational(4, 3) * values.dynkin_index * flavors
    checks.check(
        "dropping the declared gauge-loop term leaves a negative matter term",
        abelian == -2 * flavors / 3 and abelian.subs(flavors, 6) == -4,
    )
    log_scale, alpha = sp.symbols("L alpha", positive=True)
    running = alpha / (1 + 7 * alpha * log_scale / (2 * sp.pi))
    checks.check(
        "positive conditional coefficient gives exact decreasing ultraviolet running",
        sp.diff(running, log_scale).is_negative is True
        and sp.limit(running, log_scale, sp.oo) == 0,
    )

    total = checks.finish()
    print(f"P024 QCD3 EXACT AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
