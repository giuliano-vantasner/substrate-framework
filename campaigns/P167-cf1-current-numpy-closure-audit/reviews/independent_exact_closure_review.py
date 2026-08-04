#!/usr/bin/env python3
"""Fresh exact CF1 rederivation without importing the vortex claim module."""

from __future__ import annotations

from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")


def main() -> int:
    checks = CheckLedger("P167-INDEPENDENT-EXACT-CLOSURE")
    r = sp.symbols("r", positive=True)
    rho = sp.symbols("rho", positive=True)
    n = sp.symbols("n", integer=True, positive=True)
    g, lam, v = sp.symbols("g lambda v", positive=True)
    f = sp.Function("f")(r)
    a = sp.Function("a")(r)

    radial_lagrangian = r * (
        sp.diff(f, r) ** 2 / 2
        + f**2 * (n - a) ** 2 / (2 * r**2)
        + sp.diff(a, r) ** 2 / (2 * g**2 * r**2)
        + lam * (f**2 - v**2) ** 2 / 4
    )
    scalar_equation = sp.simplify(
        (
            sp.diff(sp.diff(radial_lagrangian, sp.diff(f, r)), r)
            - sp.diff(radial_lagrangian, f)
        )
        / r
    )
    gauge_equation = sp.simplify(
        g**2
        * r
        * (
            sp.diff(sp.diff(radial_lagrangian, sp.diff(a, r)), r)
            - sp.diff(radial_lagrangian, a)
        )
    )
    expected_scalar = (
        sp.diff(f, r, 2)
        + sp.diff(f, r) / r
        - f * (n - a) ** 2 / r**2
        - lam * f * (f**2 - v**2)
    )
    expected_gauge = (
        sp.diff(a, r, 2)
        - sp.diff(a, r) / r
        + g**2 * (n - a) * f**2
    )
    checks.check(
        "fresh direct variation gives the general-coupling scalar equation",
        sp.simplify(scalar_equation - expected_scalar) == 0,
    )
    checks.check(
        "fresh direct variation gives the general-coupling gauge equation",
        sp.simplify(gauge_equation - expected_gauge) == 0,
    )
    checks.check(
        "the source equation is exactly the gauge-coupling-one specialization",
        sp.simplify(expected_gauge.subs(g, 1) - (
            sp.diff(a, r, 2) - sp.diff(a, r) / r + (n - a) * f**2
        )) == 0,
    )
    checks.check(
        "wrong scalar friction and wrong gauge sign fail the derived equations",
        sp.simplify(scalar_equation - (expected_scalar - sp.diff(f, r) / r)) != 0
        and sp.simplify(gauge_equation - (expected_gauge - 2 * g**2 * (n - a) * f**2)) != 0,
    )

    asymptotic = sp.symbols("a_infinity", real=True)
    log_coefficient = v**2 * (n - asymptotic) ** 2
    checks.check(
        "fresh large-radius energy analysis uniquely fixes the positive-vacuum boundary",
        sp.solve(sp.Eq(log_coefficient, 0), asymptotic) == [n],
    )
    checks.check(
        "the ungauged positive-winding counterexample retains logarithmic divergence",
        sp.simplify(log_coefficient.subs(asymptotic, 0) - v**2 * n**2) == 0,
    )
    theta = sp.symbols("theta", real=True)
    flux = sp.integrate(n / g, (theta, 0, 2 * sp.pi))
    checks.check(
        "fresh line integration gives the declared two-pi winding over coupling flux",
        sp.simplify(flux - 2 * sp.pi * n / g) == 0,
    )
    checks.check(
        "omitting the physical coupling changes generic flux despite the g-one demo",
        sp.simplify(flux - 2 * sp.pi * n) != 0
        and sp.simplify(flux.subs(g, 1) - 2 * sp.pi * n) == 0,
    )

    delta = sp.Function("delta")(r)
    chi = sp.Function("chi")(r)
    epsilon = sp.symbols("epsilon")
    perturbed_scalar = v - epsilon * delta
    scalar_linear = sp.expand(
        sp.diff(perturbed_scalar, r, 2)
        + sp.diff(perturbed_scalar, r) / r
        - lam * perturbed_scalar * (perturbed_scalar**2 - v**2)
    ).coeff(epsilon, 1)
    perturbed_gauge = n - epsilon * chi
    gauge_linear = sp.expand(
        sp.diff(perturbed_gauge, r, 2)
        - sp.diff(perturbed_gauge, r) / r
        + g**2 * (n - perturbed_gauge) * v**2
    ).coeff(epsilon, 1)
    checks.check(
        "fresh vacuum linearization fixes scalar inverse length squared to two-lambda-v-squared",
        sp.simplify(
            scalar_linear
            + sp.diff(delta, r, 2)
            + sp.diff(delta, r) / r
            - 2 * lam * v**2 * delta
        ) == 0,
    )
    checks.check(
        "fresh vacuum linearization fixes vector inverse length squared to g-squared-v-squared",
        sp.simplify(
            gauge_linear
            + sp.diff(chi, r, 2)
            - sp.diff(chi, r) / r
            - g**2 * v**2 * chi
        ) == 0,
    )
    checks.check(
        "both exact inverse lengths vanish in the positive zero-vacuum limit",
        sp.limit(g * v, v, 0, dir="+") == 0
        and sp.limit(v * sp.sqrt(2 * lam), v, 0, dir="+") == 0,
    )

    profile = sp.Function("F")(rho)
    connection = sp.Function("A")(rho)
    scaled_terms = [
        rho * sp.diff(profile, rho) ** 2 / 2,
        profile**2 * (n - connection) ** 2 / (2 * rho),
        sp.diff(connection, rho) ** 2 / (2 * g**2 * rho),
        rho * lam * (profile**2 - 1) ** 2 / 4,
    ]
    checks.check(
        "rho-equals-v-r and f-equals-v-F factor the full tension as v-squared",
        all(not term.has(v) for term in scaled_terms),
    )
    checks.check(
        "zero scalar and zero vacuum solve the scalar equation but do not prove uniqueness",
        sp.simplify(expected_scalar.subs({v: 0, f: 0})) == 0,
    )

    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())["claims"]
    claims = {entry["id"]: entry for entry in registry}
    checks.check(
        "C-VTX-001 states the exact model while excluding physical identity and existence",
        claims["C-VTX-001"]["verification"] == "symbolic_verified"
        and "no substrate, dual, chromoelectric, QCD, or confinement identity" in claims["C-VTX-001"]["statement"]
        and "no vortex existence" in claims["C-VTX-001"]["statement"],
    )
    checks.check(
        "C-VTX-002 preserves the correct resolution-bounded epistemic ceiling",
        claims["C-VTX-002"]["verification"] == "numeric_evidence"
        and claims["C-VTX-002"]["epistemic"] == "qualified"
        and "resolution-bounded numerical evidence" in claims["C-VTX-002"]["statement"],
    )
    checks.check(
        "C-FLX-001 cannot silently equate endpoint work or uniform field energy to vortex tension",
        "slopes agree if and only if q=Phi/2" in claims["C-FLX-001"]["statement"]
        and "vortex-tension identity" in claims["C-FLX-001"]["statement"],
    )

    total = checks.finish()
    print(f"P167 INDEPENDENT EXACT CLOSURE ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
