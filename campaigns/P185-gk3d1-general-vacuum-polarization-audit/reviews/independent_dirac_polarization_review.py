#!/usr/bin/env python3
"""Independent reconstruction for C-VAC-002; imports no claim module."""

from __future__ import annotations

import ast
from pathlib import Path

import mpmath as mp
import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
CLAIM_MODULE = "substrate_framework.dirac_vacuum_polarization"


def main() -> int:
    checks = CheckLedger("P185-INDEPENDENT-C-VAC-002")
    source = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=__file__)
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    checks.check(
        "independent oracle imports no canonical Dirac polarization module",
        CLAIM_MODULE not in imports
        and "dirac_vacuum_polarization" not in source.split("CLAIM_MODULE", 1)[0],
    )

    a, b, c, d = sp.symbols("a b c d", real=True)
    e0, f, g, h = sp.symbols("e0 f g h", real=True)
    u, v, w0, z = sp.symbols("u v w0 z", real=True)
    left = sp.Matrix([[a, b], [c, d]])
    right = sp.Matrix([[e0, f], [g, h]])
    vertex = sp.Matrix([[u, v], [w0, z]])
    qslash = right.inv() - left.inv()
    contracted = sp.trace(qslash * right * vertex * left)
    shifted = sp.trace(vertex * left) - sp.trace(vertex * right)
    checks.check(
        "generic two-component trace algebra independently gives the Ward difference",
        sp.simplify(contracted - shifted) == 0,
    )
    wrong = sp.trace((right.inv() + left.inv()) * right * vertex * left)
    checks.check(
        "wrong inverse-propagator sign is not the shifted difference",
        sp.simplify(wrong - shifted) != 0,
    )

    x = sp.Symbol("x", real=True)
    charge, momentum2 = sp.symbols("e Q", positive=True)
    d2_prefactor = -4 * charge**2 / (4 * sp.pi)
    d2_integrand = sp.simplify(
        x * (1 - x) / (x * (1 - x) * momentum2)
    )
    d2_form_factor = sp.simplify(
        d2_prefactor * sp.integrate(d2_integrand, (x, 0, 1))
    )
    checks.check(
        "D2 endpoint independently yields form factor and projector coefficient",
        d2_form_factor == -charge**2 / (sp.pi * momentum2)
        and sp.simplify(-momentum2 * d2_form_factor) == charge**2 / sp.pi,
    )
    checks.check(
        "spinor-trace mutation changes the D2 normalization",
        sp.simplify(2 * d2_form_factor - d2_form_factor) != 0,
    )

    epsilon = sp.Symbol("epsilon", positive=True)
    mass2, scale2 = sp.symbols("M2 mu2", positive=True)
    common = charge**2 / (12 * sp.pi**2)
    bare = -common * sp.gamma(epsilon) * (
        4 * sp.pi * scale2 / mass2
    ) ** epsilon
    residue = sp.limit(epsilon * bare, epsilon, 0, dir="+")
    finite_bare = sp.expand(
        sp.expand_log(
            sp.limit(bare - residue / epsilon, epsilon, 0, dir="+"),
            force=True,
        )
    )
    checks.check(
        "D4 Laurent residue and finite bare part reconstruct independently",
        residue == -common
        and sp.simplify(
            finite_bare
            - common
            * (sp.log(mass2 / (4 * sp.pi * scale2)) + sp.EulerGamma)
        )
        == 0,
    )
    finite_counterterm = sp.Symbol("c_fin", real=True)
    counterterm = common * (
        1 / epsilon - sp.EulerGamma + sp.log(4 * sp.pi)
    ) + finite_counterterm
    renormalized = sp.expand(
        sp.expand_log(
            sp.limit(bare + counterterm, epsilon, 0, dir="+"),
            force=True,
        )
    )
    checks.check(
        "MS-bar limit retains one arbitrary finite local counterterm",
        sp.simplify(
            sp.expand_log(
                renormalized
                - common * sp.log(mass2 / scale2)
                - finite_counterterm,
                force=True,
            )
        )
        == 0,
    )
    checks.check(
        "independent logarithmic derivatives have opposite mass and scale signs",
        sp.simplify(mass2 * sp.diff(renormalized, mass2) - common) == 0
        and sp.simplify(scale2 * sp.diff(renormalized, scale2) + common) == 0,
    )

    ratio = sp.Symbol("w", nonnegative=True)
    coefficients = []
    for n in range(1, 7):
        beta_integral = sp.integrate((x * (1 - x)) ** (n + 1), (x, 0, 1))
        closed_beta = sp.factorial(n + 1) ** 2 / sp.factorial(2 * n + 3)
        checks.check(
            f"beta integral coefficient n={n} is exact",
            sp.simplify(beta_integral - closed_beta) == 0,
        )
        coefficients.append(sp.simplify(-common * closed_beta / n))
    checks.check(
        "first three independently generated coefficients match the freeze",
        coefficients[:3]
        == [-common / 30, -common / 280, -common / 1890],
    )

    mp.mp.dps = 80

    def exact_integral(value: mp.mpf) -> mp.mpf:
        return mp.quad(
            lambda parameter: parameter
            * (1 - parameter)
            * mp.log(1 - value * parameter * (1 - parameter)),
            [0, mp.mpf("0.5"), 1],
        )

    for value in (mp.mpf("0.25"), mp.mpf("1.0"), mp.mpf("3.0")):
        exact_value = exact_integral(value)
        partials = []
        for terms in (1, 3, 6):
            partials.append(
                mp.fsum(
                    [
                        -value**n
                        * mp.factorial(n + 1) ** 2
                        / (n * mp.factorial(2 * n + 3))
                        for n in range(1, terms + 1)
                    ]
                )
            )
        errors = [abs(partial - exact_value) for partial in partials]
        checks.check(
            f"high-precision series converges toward independent quadrature at w={value}",
            errors[2] < errors[1] < errors[0],
        )
    checks.check(
        "first omitted term bounds the positive-term magnitude below threshold",
        all(
            abs(
                exact_integral(value)
                - mp.fsum(
                    [
                        -value**n
                        * mp.factorial(n + 1) ** 2
                        / (n * mp.factorial(2 * n + 3))
                        for n in range(1, 7)
                    ]
                )
            )
            < value**7
            * mp.factorial(8) ** 2
            / (7 * mp.factorial(17))
            / (1 - value / 4)
            for value in (mp.mpf("0.25"), mp.mpf("1.0"), mp.mpf("3.0"))
        ),
    )
    checks.check(
        "Feynman-weight maximum independently fixes the first branch point",
        sp.maximum(x * (1 - x), x, sp.Interval(0, 1)) == sp.Rational(1, 4)
        and sp.solve(sp.Eq(1 - ratio / 4, 0), ratio) == [4],
    )
    checks.check(
        "threshold mutation changes the midpoint logarithm argument sign",
        (1 - sp.Rational(39, 10) / 4) > 0
        and (1 - sp.Rational(41, 10) / 4) < 0,
    )

    coupling, trace, rescaling = sp.symbols("g T c", positive=True)
    original_weight = coupling**2 * trace
    paired_weight = (coupling / rescaling) ** 2 * rescaling**2 * trace
    checks.check(
        "representation convention invariance reconstructs independently",
        sp.simplify(paired_weight - original_weight) == 0,
    )
    checks.check(
        "unpaired trace rescaling is not invariant",
        sp.simplify(coupling**2 * rescaling**2 * trace - original_weight) != 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
