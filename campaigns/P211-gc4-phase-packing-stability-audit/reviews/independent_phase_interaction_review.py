#!/usr/bin/env python3
"""Independent rederivation for P211 without importing its canonical module."""

from __future__ import annotations

import ast
import hashlib
import itertools
from pathlib import Path

import sympy as sp

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC4_stability_forces_three.py"
)
SOURCE_SHA256 = "3292400544911dca74009a019b24b44f105f8aeb5c68a6172220903950f465bb"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P211-GC4-INDEPENDENT-REVIEW")
    checks.check("source hash remains independently pinned", digest(SOURCE) == SOURCE_SHA256)
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    audit = audit_numpy_trapezoid_compatibility(source, filename=str(SOURCE))
    checks.check(
        "independent source inventory remains eight checks and one assertion",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(tree)
        )
        == 8
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    checks.check(
        "independent compatibility audit finds no quadrature name",
        audit.legacy_references == audit.current_references == 0,
    )

    f, g, c = sp.symbols("f g c", real=True)
    rho2 = f**2 + g**2 + 2 * c * f * g
    cross = sp.Poly(sp.expand(rho2**2 - f**4 - g**4), c)
    checks.check("quartic cross has phase degree two", cross.degree() == 2)
    checks.check(
        "quartic cross has a nonzero phase-independent coefficient",
        cross.coeff_monomial(1) == 2 * f**2 * g**2,
    )
    checks.check(
        "quartic cross has the exact linear phase coefficient",
        sp.expand(
            cross.coeff_monomial(c) - 4 * f * g * (f**2 + g**2)
        )
        == 0,
    )
    checks.check(
        "quartic cross has the exact quadratic phase coefficient",
        cross.coeff_monomial(c**2) == 4 * f**2 * g**2,
    )

    t, q = sp.symbols("t q", real=True, positive=True)
    rational_31 = sp.integrate((1 - t**2) / (1 - q * t), (t, -1, 1))
    rational_22 = sp.integrate((1 - t**2) / (1 - q * t) ** 2, (t, -1, 1))
    q_value = sp.Rational(4, 5)
    s_value = sp.log(3)
    fresh_31 = sp.simplify(rational_31.subs(q, q_value) / sp.cosh(s_value))
    fresh_22 = sp.simplify(rational_22.subs(q, q_value) / sp.cosh(s_value) ** 2)
    expected_31 = sp.simplify(
        2
        * (sp.sinh(s_value) * sp.cosh(s_value) - s_value)
        / sp.sinh(s_value) ** 3
    )
    expected_22 = sp.simplify(
        4
        * (s_value * sp.cosh(s_value) - sp.sinh(s_value))
        / sp.sinh(s_value) ** 3
    )
    checks.check(
        "fresh rational substitution derives the mixed cubic overlap",
        sp.simplify(fresh_31 - expected_31) == 0,
    )
    checks.check(
        "fresh rational substitution derives the density overlap",
        sp.simplify(fresh_22 - expected_22) == 0,
    )

    i31, i22 = sp.symbols("I31 I22", positive=True)
    exact_energy = -c * i31 / 6 - (1 + 2 * c**2) * i22 / 12
    checks.check(
        "perpendicular phase remains exactly attractive in the trial ledger",
        exact_energy.subs(c, 0) == -i22 / 12,
    )
    checks.check(
        "opposite phases are not the negative of equal phases at finite separation",
        sp.simplify(exact_energy.subs(c, 1) + exact_energy.subs(c, -1))
        == -i22 / 2,
    )

    s = sp.symbols("s", positive=True)
    j31 = 2 * (sp.sinh(s) * sp.cosh(s) - s) / sp.sinh(s) ** 3
    j22 = 4 * (s * sp.cosh(s) - sp.sinh(s)) / sp.sinh(s) ** 3
    checks.check("fresh mixed tail rate is one", sp.limit(sp.exp(s) * j31, s, sp.oo) == 4)
    checks.check(
        "fresh density tail rate is two with a linear factor",
        sp.limit(j22 / (16 * (s - 1) * sp.exp(-2 * s)), s, sp.oo) == 1,
    )

    def energy(distance: sp.Expr, cosine: sp.Expr) -> sp.Expr:
        return sp.simplify(
            -cosine * j31.subs(s, distance) / 6
            - (1 + 2 * cosine**2) * j22.subs(s, distance) / 12
        )

    d = sp.symbols("d", positive=True)
    anti_force = -sp.diff(energy(d, -1), d)
    checks.check(
        "fresh anti-phase force changes sign",
        float(anti_force.subs(d, 1)) < 0 and float(anti_force.subs(d, 6)) > 0,
    )
    z3_force = -sp.diff(energy(d, -sp.Rational(1, 2)), d)
    checks.check(
        "fresh Z3 pair force changes sign",
        float(z3_force.subs(d, 1)) < 0 and float(z3_force.subs(d, 6)) > 0,
    )

    optimum = {n: sp.simplify(sp.cos(2 * sp.pi / n)) for n in range(2, 7)}
    checks.check(
        "nearest-gap optimum is negative only through count three",
        [bool(optimum[n] < 0) for n in range(2, 7)]
        == [True, True, False, False, False],
    )
    checks.check(
        "nearest-gap optimum is nonpositive through count four",
        [bool(optimum[n] <= 0) for n in range(2, 7)]
        == [True, True, True, False, False],
    )
    for n in range(2, 7):
        phases = [2 * sp.pi * index / n for index in range(n)]
        worst = max(
            sp.simplify(sp.cos(a - b))
            for a, b in itertools.combinations(phases, 2)
        )
        checks.check(
            f"regular {n}-gon attains its nearest-gap lower bound",
            sp.simplify(worst - optimum[n]) == 0,
        )

    checks.check(
        "strict capacity is not exact occupancy",
        bool(optimum[2] < 0) and bool(optimum[3] < 0),
    )
    sparse_phases = (0, sp.pi, 0, sp.pi)
    cycle = ((0, 1), (1, 2), (2, 3), (3, 0))
    checks.check(
        "fresh sparse graph countermodel has four negative edges",
        all(
            sp.cos(sparse_phases[i] - sparse_phases[j]) == -1
            for i, j in cycle
        ),
    )
    tetrahedron = (
        (1, 1, 1),
        (1, -1, -1),
        (-1, 1, -1),
        (-1, -1, 1),
    )
    checks.check(
        "fresh tetrahedral countermodel has four pairwise negative orientations",
        all(
            sum(a * b for a, b in zip(tetrahedron[i], tetrahedron[j])) == -1
            for i, j in itertools.combinations(range(4), 2)
        ),
    )
    checks.check(
        "source triple section never constructs a three-profile field",
        "pair_ints[(i, j)] = E_int(10.0, dth)" in source,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
