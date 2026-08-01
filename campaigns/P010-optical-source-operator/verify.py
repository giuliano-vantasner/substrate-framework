#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed C-OG-003."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.optical_geometry import (
    index_from_potential,
    optical_box_static_1d,
    optical_dilaton,
    optical_dilaton_source_operator_1d,
    optical_ricci_scalar_1d,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class PullbackCandidate:
    source_sign: int
    tf_coefficient: int
    tf_power: int


def pullback_candidate_is_exact(candidate: PullbackCandidate) -> bool:
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    potential = sp.Function("Phi")(x)
    index = (
        1 + candidate.tf_coefficient * potential / c0**2
    ) ** (-candidate.tf_power)
    candidate_source = sp.simplify(
        candidate.source_sign
        * optical_box_static_1d(sp.log(index), index, x, c0)
    )
    return sp.simplify(candidate_source - 2 * sp.diff(potential, x, 2)) == 0


def run() -> int:
    checks = CheckLedger("C-OG-003")
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    potential = sp.Function("Phi")(x)
    density = sp.Function("rho")(x)
    kappa = sp.symbols("kappa", real=True)

    index = index_from_potential(potential, c0)
    dilaton = optical_dilaton(index)
    source_side = optical_dilaton_source_operator_1d(potential, x, c0)
    expected = 2 * sp.diff(potential, x, 2)

    checks.check(
        "the full curved source-side operator is exactly twice the potential Laplacian",
        sp.simplify(source_side - expected) == 0,
    )
    checks.check(
        "the result is the negative accepted optical curvature under the TF map",
        sp.simplify(
            source_side + optical_ricci_scalar_1d(index, x, c0)
        )
        == 0,
    )
    checks.check(
        "the signal-speed factors cancel without a weak-field limit",
        c0 not in sp.simplify(source_side).free_symbols,
    )
    checks.check(
        "the conditional source equation and Poisson-form equation have identical residuals up to two",
        sp.simplify(
            source_side
            - kappa * density
            - 2
            * (sp.diff(potential, x, 2) - kappa * density / 2)
        )
        == 0,
    )

    scale = sp.symbols("lambda", positive=True)
    profile = sp.Function("U")(x)
    scaled_source = optical_dilaton_source_operator_1d(
        scale * profile, x, c0
    )
    checks.check(
        "the exact scaled family is linear in the potential amplitude",
        sp.simplify(scaled_source - 2 * scale * sp.diff(profile, x, 2))
        == 0,
    )
    checks.check(
        "the weak-field quotient is a corollary of the exact identity",
        sp.simplify(sp.limit(scaled_source / scale, scale, 0, dir="+")
                    - 2 * sp.diff(profile, x, 2))
        == 0,
    )
    checks.mutation_sensitive(
        "operator sign, TF coefficient, and TF exponent",
        pullback_candidate_is_exact,
        PullbackCandidate(-1, 2, 1),
        [
            PullbackCandidate(1, 2, 1),
            PullbackCandidate(-1, 1, 1),
            PullbackCandidate(-1, 2, 2),
        ],
    )

    total = checks.finish()
    print(f"P010 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
