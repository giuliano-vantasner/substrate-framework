"""Fresh exact P216 review without canonical claim APIs or primary expressions."""

from __future__ import annotations

import ast
from pathlib import Path
import re

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-43/"
    "bridge_MK3_epsilon_pinned.py"
)


def main() -> int:
    checks = CheckLedger("P216-independent")
    f, e, ell, mu = sp.symbols("F e ell mu", positive=True)
    ratio = sp.cancel(1 / (e * (ell * f) * (mu / f**2)))
    checks.check(
        "fresh cancellation gives the scale-over-product quotient",
        ratio == f / (e * ell * mu),
    )
    c = sp.symbols("c", positive=True)
    checks.check(
        "fresh dimensional family retains an arbitrary normalization",
        sp.simplify(c * ratio - ratio) != 0,
    )
    s, p, target = sp.symbols("s p target", positive=True)
    checks.check(
        "fresh inverse reconstruction needs a supplied product",
        sp.simplify((s / p).subs(p, s / target) - target) == 0,
    )
    u = sp.symbols("u", positive=True)
    checks.check(
        "fresh same-product family leaves individual couplings unidentified",
        sp.simplify(ratio.subs({ell: u, mu: p / u}) - f / (e * p)) == 0
        and sp.simplify(ratio.subs({ell: 2 * u, mu: p / (2 * u)}) - f / (e * p))
        == 0,
    )

    lambda_a, lambda_b = sp.symbols("lambda_A lambda_B", positive=True)
    checks.check(
        "fresh density equality solves the BPS convention map",
        sp.solve(sp.Eq(lambda_a**2, sp.pi**4 * lambda_b**2), lambda_a)
        == [sp.pi**2 * lambda_b],
    )
    color, pion = sp.symbols("N m_pi", positive=True)
    source_product = color * pion / 8
    bps_product = source_product / sp.pi**2
    checks.check(
        "fresh product conversion carries inverse pi squared",
        bps_product == color * pion / (8 * sp.pi**2),
    )
    source_eps = sp.simplify(s / source_product)
    bps_eps = sp.simplify(s / bps_product)
    checks.check(
        "fresh accepted quotient is pi squared above the source quotient",
        sp.simplify(bps_eps / source_eps - sp.pi**2) == 0,
    )

    electron = sp.Rational(511, 1000)
    pion_value = sp.Rational(13803, 100)
    skyrme_scale = 16 * sp.pi * electron
    source_value = (source_eps.subs({s: skyrme_scale, color: 3, pion: pion_value}))
    bps_value = bps_eps.subs({s: skyrme_scale, color: 3, pion: pion_value})
    checks.check(
        "fresh exact numerics reverse the source less-than-one guard",
        bool(sp.N(source_value) < 1)
        and bool(sp.N(bps_value) > 1)
        and sp.simplify(bps_value / source_value - sp.pi**2) == 0,
    )

    b1, rest = sp.symbols("B1 E_e", positive=True)
    top_mass = 48 * sp.pi**3 * b1 * rest
    anw_coefficient = 3 * sp.pi**2 * b1
    fresh_scale = sp.solve(sp.Eq(top_mass, anw_coefficient * s), s)
    checks.check(
        "fresh NY1 cancellation retains its supplied electron-energy premise",
        fresh_scale == [16 * sp.pi * rest]
        and sp.diff(fresh_scale[0], rest) != 0,
    )

    t = sp.symbols("t", positive=True)
    checks.check(
        "fresh simultaneous coupling flow changes the local quotient",
        sp.simplify(ratio.subs({ell: t * ell, mu: t * mu}) - ratio / t**2)
        == 0,
    )
    checks.check(
        "fresh fixed-product constraint permits no nontrivial positive flow",
        sp.solve(sp.Eq(t**2 * p, p), t) == [1],
    )

    source_text = SOURCE.read_text()
    tree = ast.parse(source_text)
    assignments = {
        target.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    checks.check(
        "fresh AST review finds the executable comparator assignment",
        "KAPPA_EMP_VALUE" in assignments
        and "KAPPA_EMP_VALUE = 929 / 1000.0" in source_text,
    )
    checks.check(
        "fresh prose review finds the unchecked factor-of-two contradiction",
        "128 pi m_e / (3 m_pi)  =  (64 pi/3)" in source_text
        and "~  0.248" in source_text
        and "~ 0.496" in source_text,
    )

    claims = {
        claim["id"]: claim
        for claim in yaml.safe_load((ROOT / "governance/claims.yaml").read_text())[
            "claims"
        ]
    }
    checks.check(
        "fresh registry read keeps lambda and mu supplied in C-BPS-001",
        "Let lambda and mu be positive" in claims["C-BPS-001"]["statement"]
        and "select a potential or coupling" in claims["C-BPS-001"]["statement"],
    )
    checks.check(
        "fresh registry read finds no KI2-ratio map in C-BPS-003",
        "epsilon a positive dimensionless parameter tending to zero"
        in claims["C-BPS-003"]["statement"]
        and not re.search(
            r"\b(?:lambda|mu|F_pi)\b",
            claims["C-BPS-003"]["statement"],
        ),
    )
    checks.check(
        "fresh registry read keeps physical vector inputs outside C-VEC-002",
        "derive no HLS field content" in claims["C-VEC-002"]["statement"]
        and "N_c" in claims["C-VEC-002"]["statement"],
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())

