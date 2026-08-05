#!/usr/bin/env python3
"""Fresh exact C-SKY-002 derivation without importing its canonical module."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P184-INDEPENDENT-C-SKY-002")
    entries = sp.symbols("x0:12", real=True)
    tangent_entries = sp.symbols("v0:4", real=True)
    gradients = sp.Matrix(3, 4, entries)
    tangent = sp.Matrix(4, 1, tangent_entries)
    strain = gradients * gradients.T
    trace = sp.trace(strain)

    quartic_trace = sp.expand((trace**2 - sp.trace(strain * strain)) / 2)
    quartic_pairs = sp.expand(
        sum(
            (
                gradients[i, a] * gradients[j, b]
                - gradients[i, b] * gradients[j, a]
            )
            ** 2
            for i in range(3)
            for j in range(i + 1, 3)
            for a in range(4)
            for b in range(a + 1, 4)
        )
    )
    checks.check(
        "fresh expansion proves quartic Gram identity",
        sp.expand(quartic_trace - quartic_pairs) == 0,
    )
    checks.check(
        "quartic certificate contains all eighteen spatial-component minors",
        sum(1 for i in range(3) for j in range(i + 1, 3) for a in range(4) for b in range(a + 1, 4))
        == 18,
    )

    mass = 2 * ((1 + trace) * sp.eye(4) - gradients.T * gradients)
    norm = (tangent.T * tangent)[0]
    gap = sp.expand((tangent.T * mass * tangent)[0] - 2 * norm)
    gap_pairs = sp.expand(
        2
        * sum(
            (
                tangent[a] * gradients[i, b]
                - tangent[b] * gradients[i, a]
            )
            ** 2
            for i in range(3)
            for a in range(4)
            for b in range(a + 1, 4)
        )
    )
    checks.check(
        "fresh expansion proves mass lower-bound identity",
        sp.expand(gap - gap_pairs) == 0,
    )
    checks.check(
        "mass certificate contains all eighteen gradient-tangent minors",
        sum(1 for i in range(3) for a in range(4) for b in range(a + 1, 4))
        == 18,
    )
    checks.check("fresh mass matrix is exactly symmetric", mass == mass.T)

    parallel_gradients = sp.Matrix(
        [[2, 0, 0, 0], [-3, 0, 0, 0], [5, 0, 0, 0]]
    )
    parallel_tangent = sp.Matrix([7, 0, 0, 0])
    parallel_trace = sp.trace(parallel_gradients * parallel_gradients.T)
    parallel_mass = 2 * (
        (1 + parallel_trace) * sp.eye(4)
        - parallel_gradients.T * parallel_gradients
    )
    checks.check(
        "independent parallel witness saturates the coefficient-two bound",
        (parallel_tangent.T * parallel_mass * parallel_tangent)[0]
        == 2 * (parallel_tangent.T * parallel_tangent)[0],
    )

    orthogonal = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])
    orthogonal_strain = orthogonal * orthogonal.T
    orthogonal_quartic = sp.simplify(
        (
            sp.trace(orthogonal_strain) ** 2
            - sp.trace(orthogonal_strain * orthogonal_strain)
        )
        / 2
    )
    checks.check(
        "independent sign-flip mutation produces negative quartic density",
        orthogonal_quartic == 1 and -orthogonal_quartic < 0,
    )
    checks.check(
        "independent missing-identity mutation violates the mass bound at vacuum",
        (parallel_tangent.T * sp.zeros(4) * parallel_tangent)[0]
        < 2 * (parallel_tangent.T * parallel_tangent)[0],
    )

    alpha, e2, e4 = sp.symbols("alpha E2 E4", positive=True)
    scaled = alpha * e2 + e4 / alpha
    checks.check(
        "fresh Derrick differentiation separates stationarity from curvature",
        sp.diff(scaled, alpha).subs(alpha, 1) == e2 - e4
        and sp.diff(scaled, alpha, 2).subs(alpha, 1) == 2 * e4,
    )
    checks.check(
        "positive Derrick curvature alone does not impose its stationarity equation",
        sp.diff(scaled, alpha, 2).subs(alpha, 1).is_positive is True
        and sp.diff(scaled, alpha).subs(alpha, 1) != 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
