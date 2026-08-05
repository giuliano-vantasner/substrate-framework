#!/usr/bin/env python3
"""Independent direct rederivation of GC1's valid and invalid inferences."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P208-INDEPENDENT-CURVATURE")
    field, kappa = sp.symbols("f kappa", real=True, positive=True)
    scale = sp.symbols("lambda", real=True, nonzero=True)
    potential = kappa**2 * field**2 / 2 - field**4 / 48
    curvature = sp.diff(potential, field, 2)
    deficit = sp.simplify(curvature.subs(field, 0) - curvature)
    coupling = scale * field
    checks.check(
        "direct differentiation gives the conditional linear lock",
        deficit == field**2 / 4
        and sp.simplify(deficit - coupling**2 / (4 * scale**2)) == 0,
    )

    epsilon = sp.symbols("epsilon", nonzero=True, real=True)
    deformed = potential + epsilon * field**6
    deformed_curvature = sp.diff(deformed, field, 2)
    checks.check(
        "potential deformation changes the lock",
        sp.simplify(
            deformed_curvature.subs(field, 0) - deformed_curvature
        )
        == field**2 / 4 - 30 * epsilon * field**4,
    )
    checks.check(
        "nonlinear coupling is an exact countermodel",
        sp.simplify(deficit - (scale * field**2) ** 2 / (4 * scale**2))
        != 0,
    )
    sine_deficit = (1 - sp.cos(field)) / 2
    checks.check(
        "exact-sine deficit is only asymptotically quartic",
        sp.simplify(sine_deficit - deficit) != 0
        and sp.series(sine_deficit - deficit, field, 0, 6)
        == -field**4 / 48 + sp.Order(field**6),
    )

    coordinate, center = sp.symbols("x x_0", real=True)
    profile = sp.sqrt(24) * kappa * sp.sech(kappa * (coordinate - center))
    well = sp.simplify(kappa**2 - profile**2 / 4)
    derivative = sp.diff(well, coordinate)
    checks.check(
        "direct profile substitution has one analytic minimum",
        sp.simplify(
            derivative
            - 12
            * kappa**3
            * sp.sech(kappa * (coordinate - center)) ** 2
            * sp.tanh(kappa * (coordinate - center))
        )
        == 0
        and sp.diff(well, coordinate, 2).subs(coordinate, center)
        == 12 * kappa**4,
    )

    # Recompute both normalized expectations directly from exact sech integrals.
    z = sp.symbols("z", real=True)
    even_density = 1 / sp.cosh(z) ** 4
    odd_density = 1 / sp.cosh(z) ** 2 - 1 / sp.cosh(z) ** 4
    multiplier = sp.sqrt(24) * kappa / sp.cosh(z)
    even_overlap = sp.simplify(
        sp.integrate(even_density * multiplier, (z, -sp.oo, sp.oo))
        / sp.integrate(even_density, (z, -sp.oo, sp.oo))
    )
    odd_overlap = sp.simplify(
        sp.integrate(odd_density * multiplier, (z, -sp.oo, sp.oo))
        / sp.integrate(odd_density, (z, -sp.oo, sp.oo))
    )
    checks.check(
        "direct overlap integrals scale to zero with a fixed ratio",
        even_overlap == 9 * sp.pi * sp.sqrt(24) * kappa / 32
        and odd_overlap == 3 * sp.pi * sp.sqrt(24) * kappa / 16
        and sp.simplify(odd_overlap / even_overlap) == sp.Rational(2, 3),
    )

    # An arbitrarily small positive Pöschl depth has an exact bound state.
    s, width = sp.symbols("s w", positive=True)
    depth = s * (s + 1) / width**2
    mode = sp.sech(coordinate / width) ** s
    h_mode = sp.simplify(
        -sp.diff(mode, coordinate, 2)
        - depth * sp.sech(coordinate / width) ** 2 * mode
    )
    checks.check(
        "arbitrarily shallow Poschl family has a negative exact level",
        sp.simplify(h_mode + s**2 * mode / width**2) == 0
        and sp.limit(depth, s, 0, dir="+") == 0
        and sp.limit(-s**2 / width**2, s, 0, dir="+") == 0,
    )

    probability, a, b = sp.symbols("p a b", real=True)
    mean = probability * a + (1 - probability) * b
    second = probability * a**2 + (1 - probability) * b**2
    checks.check(
        "source moment diagnostic is exactly a variance identity",
        sp.simplify(
            sp.factor(second - mean**2)
            - probability * (1 - probability) * (a - b) ** 2
        )
        == 0,
    )
    displacement = sp.symbols("R", positive=True)
    checks.check(
        "a perfectly relocated point distribution saturates the source ratio",
        sp.sqrt(displacement**2) / displacement == 1,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
