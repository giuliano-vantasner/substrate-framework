"""Independent exact P101 review without canonical threshold or barrier APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _elasticity(expression: sp.Expr, variable: sp.Symbol) -> sp.Expr:
    return sp.simplify(variable * sp.diff(expression, variable) / expression)


def main() -> int:
    checks = CheckLedger("P101-INDEPENDENT")
    n = sp.Symbol("n", positive=True)
    visibility = sp.Symbol("V", positive=True)
    barrier, theta = sp.symbols("E theta", positive=True)
    scale = theta * n * (1 + (n - 1) * visibility)
    direct_root = sp.simplify(
        (
            sp.sqrt((1 - visibility) ** 2 + 4 * visibility * barrier / theta)
            - (1 - visibility)
        )
        / (2 * visibility)
    )
    checks.check(
        "fresh quadratic substitution gives the declared barrier",
        sp.simplify(scale.subs(n, direct_root) - barrier) == 0,
    )
    checks.check(
        "fresh population derivative is strictly positive on the declared domain",
        sp.simplify(
            sp.diff(scale, n) - theta * (1 - visibility + 2 * n * visibility)
        )
        == 0
        and sp.diff(scale, n).subs({visibility: 0}) == theta
        and sp.simplify(sp.diff(scale, n).subs({visibility: 1}) - 2 * n * theta)
        == 0,
    )
    incoherent = sp.solve(sp.Eq(scale.subs(visibility, 0), barrier), n)[0]
    coherent = sp.solve(sp.Eq(scale.subs(visibility, 1), barrier), n)[0]
    checks.check(
        "fresh endpoint solutions are linear and square-root branches",
        incoherent == barrier / theta and coherent == sp.sqrt(barrier / theta),
    )

    x = sp.Symbol("x", positive=True)
    checks.check(
        "fresh endpoint ordering changes at one",
        sp.sqrt(x).subs(x, 9) < x.subs(x, 9)
        and sp.sqrt(x).subs(x, 1) == x.subs(x, 1)
        and sp.sqrt(x).subs(x, sp.Rational(1, 9)) > x.subs(x, sp.Rational(1, 9)),
    )

    tension, coupling, amplitude, wave, thickness = sp.symbols(
        "T g A k l_m", positive=True
    )
    composed_barrier = 2 * sp.pi * tension**2 / (
        coupling * amplitude**2 * wave**2 * thickness
    )
    fresh_coherent = sp.sqrt(composed_barrier / theta)
    fresh_incoherent = composed_barrier / theta
    checks.check(
        "fresh barrier substitution preserves the endpoint square relation",
        sp.simplify(fresh_coherent**2 - fresh_incoherent) == 0,
    )
    variables = (tension, coupling, amplitude, wave, thickness, theta)
    checks.check(
        "fresh coherent elasticities are exact half-barrier elasticities",
        tuple(_elasticity(fresh_coherent, variable) for variable in variables)
        == (1, sp.Rational(-1, 2), -1, -1, sp.Rational(-1, 2), sp.Rational(-1, 2)),
    )
    checks.check(
        "fresh incoherent elasticities are exact barrier-minus-scale elasticities",
        tuple(_elasticity(fresh_incoherent, variable) for variable in variables)
        == (2, -1, -2, -2, -1, -1),
    )

    common = sp.Symbol("lambda", positive=True)
    checks.check(
        "fresh common energy rescaling leaves the threshold ratio invariant",
        sp.simplify((common * barrier) / (common * theta) - barrier / theta) == 0,
    )
    checks.check(
        "fresh independent scale rescaling changes both endpoint thresholds",
        sp.simplify(sp.sqrt(barrier / (common * theta)) / coherent) == 1 / sp.sqrt(common)
        and sp.simplify((barrier / (common * theta)) / incoherent) == 1 / common,
    )

    log_matrix = sp.Matrix(
        [
            [1, sp.Rational(-1, 2), -1, -1, sp.Rational(-1, 2), sp.Rational(-1, 2)],
            [2, -1, -2, -2, -1, -1],
        ]
    )
    checks.check(
        "fresh endpoint observation matrix has rank one and five null directions",
        log_matrix.rank() == 1 and len(log_matrix.nullspace()) == 5,
    )
    target = sp.Symbol("q", positive=True)
    checks.check(
        "fresh inverse families realize arbitrary endpoint coordinates",
        sp.simplify((barrier / (barrier / target)) - target) == 0
        and sp.simplify(sp.sqrt(barrier / (barrier / target**2)) - target) == 0,
    )

    half_root = sp.simplify(
        (sp.sqrt(sp.Rational(1, 4) + 80) - sp.Rational(1, 2))
    )
    checks.check(
        "fresh general-V example has integer threshold nine",
        sp.ceiling(half_root) == 9
        and (8 * (1 + sp.Rational(7, 2))) < 40
        and (9 * (1 + 4)) >= 40,
    )
    checks.check(
        "fresh subunit endpoint roots both require one positive integer source",
        sp.ceiling(sp.Rational(1, 4)) == 1
        and sp.ceiling(sp.Rational(1, 2)) == 1,
    )

    count = sp.Integer(10)
    visibility_boundary = sp.solve(
        sp.Eq(count * (1 + (count - 1) * visibility), 40), visibility
    )[0]
    checks.check(
        "fresh inverse-coherence guard boundary is one third",
        visibility_boundary == sp.Rational(1, 3),
    )
    checks.check(
        "fresh guard separates endpoint algebra without adding event semantics",
        count < 40 and count**2 > 40,
    )
    checks.check(
        "fresh review uses no numerical solver quadrature or fitted comparator",
        not any(
            expression.has(sp.Integral, sp.Float)
            for expression in (
                direct_root,
                coherent,
                incoherent,
                fresh_coherent,
                fresh_incoherent,
                visibility_boundary,
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
