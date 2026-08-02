"""Independent exact NY1 review without importing canonical Skyrme APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P084-INDEPENDENT")
    coefficient, rest_energy, ratio = sp.symbols("B E R", positive=True)
    top = 48 * sp.pi**3 * coefficient * rest_energy
    classical = 3 * sp.pi**2 * coefficient * ratio
    solution = sp.solve(sp.Eq(classical, top), ratio)[0]
    checks.check(
        "fresh coefficient division gives the exact conditional ratio",
        solution == 16 * sp.pi * rest_energy,
    )
    checks.check(
        "fresh substitution proves the reverse implication",
        sp.simplify(top - classical.subs(ratio, solution)) == 0,
    )
    checks.check(
        "fresh dependence audit retains the dimensionful electron input",
        solution.free_symbols == {rest_energy}
        and sp.diff(solution, rest_energy) == 16 * sp.pi,
    )

    a, c = sp.symbols("a c", positive=True)
    p, q = sp.symbols("p q", integer=True)
    generic = sp.simplify(
        a * sp.pi**3 * coefficient**p * rest_energy
        / (c * sp.pi**2 * coefficient**q)
    )
    checks.check(
        "fresh monomial elimination exposes all coefficient freedoms",
        generic == sp.pi * a * coefficient ** (p - q) * rest_energy / c,
    )
    checks.check(
        "fresh equal-power specialization cancels only the shared coefficient",
        sp.simplify(generic.subs(p, q) - sp.pi * a * rest_energy / c) == 0
        and {a, c, rest_energy} <= generic.subs(p, q).free_symbols,
    )
    checks.check(
        "fresh unequal-power counterexample retains the hedgehog coefficient",
        coefficient in generic.subs({p: 2, q: 1}).free_symbols
        and coefficient in generic.subs({p: 1, q: 2}).free_symbols,
    )

    target, correction = sp.symbols("T kappa", positive=True)
    inverse = sp.solve(sp.Eq(correction * solution, target), correction)[0]
    checks.check(
        "fresh correction inverse realizes every positive target",
        inverse == target / (16 * sp.pi * rest_energy)
        and sp.simplify((correction * solution).subs(correction, inverse) - target)
        == 0,
    )
    electron_mev = sp.Rational(10219979, 20000000)
    evaluated = sp.simplify(solution.subs(rest_energy, electron_mev))
    checks.check(
        "fresh numerical value remains proportional to the supplied measurement",
        evaluated == sp.Rational(10219979, 1250000) * sp.pi
        and sp.diff(solution, rest_energy) != 0,
    )
    proton = sp.simplify(3 * sp.pi**2 * coefficient * solution)
    checks.check(
        "fresh proton closure is the original equality by construction",
        proton == top and proton.free_symbols == {coefficient, rest_energy},
    )
    checks.check(
        "fresh derivation needs neither numerical solver nor quadrature",
        not any(expression.has(sp.Integral) for expression in (solution, generic, inverse)),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
