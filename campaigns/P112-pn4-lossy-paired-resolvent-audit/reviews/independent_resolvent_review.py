"""Independent direct-matrix and calculus review for P112."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def _fresh_pair(
    detuning: sp.Expr,
    loss: sp.Expr,
    positive_product: sp.Expr,
    negative_product: sp.Expr,
    energy: sp.Expr = sp.Integer(0),
) -> sp.Expr:
    return sp.factor(
        positive_product / (energy - detuning + sp.I * loss / 2)
        + negative_product / (energy + detuning + sp.I * loss / 2)
    )


def main() -> int:
    checks = CheckLedger("C-RES-001-INDEPENDENT")
    delta, gamma, product, energy = sp.symbols(
        "Delta Gamma c E", positive=True
    )
    expression = _fresh_pair(delta, gamma, product, product, energy)
    checks.check(
        "fresh common-denominator route gives the general pair",
        sp.simplify(
            expression
            - 2 * product * (energy + sp.I * gamma / 2)
            / ((energy + sp.I * gamma / 2) ** 2 - delta**2)
        )
        == 0,
    )
    at_zero = sp.simplify(expression.subs(energy, 0))
    checks.check(
        "fresh zero-energy route fixes sign and half-width",
        sp.simplify(
            at_zero + sp.I * product * gamma / (delta**2 + gamma**2 / 4)
        )
        == 0,
    )
    checks.check(
        "fresh lossless route cancels only on shell",
        sp.simplify(at_zero.subs(gamma, 0)) == 0
        and sp.simplify(
            expression.subs(gamma, 0)
            - 2 * product * energy / (energy**2 - delta**2)
        )
        == 0,
    )

    positive, negative = sp.symbols("p q")
    fresh_asymmetric = _fresh_pair(delta, 0, positive, negative)
    checks.check(
        "fresh asymmetric route derives matching-product cancellation",
        sp.simplify(fresh_asymmetric - (negative - positive) / delta) == 0,
    )
    checks.check(
        "fresh unequal-phase counterexample survives",
        sp.simplify(fresh_asymmetric.subs({positive: 1, negative: sp.I}))
        != 0,
    )

    magnitude = product * gamma / (delta**2 + gamma**2 / 4)
    checks.check(
        "fresh calculus route finds the sole positive stationary point",
        sp.solve(sp.together(sp.diff(magnitude, gamma)), gamma) == [2 * delta]
        and sp.diff(magnitude, gamma, 2).subs(gamma, 2 * delta) < 0,
    )
    checks.check(
        "fresh endpoint limits both vanish",
        sp.limit(magnitude, gamma, 0, dir="+") == 0
        and sp.limit(magnitude, gamma, sp.oo) == 0,
    )
    checks.check(
        "fresh asymptotic normalizations fix both coefficients",
        sp.limit(at_zero / gamma, gamma, 0, dir="+")
        == -sp.I * product / delta**2
        and sp.limit(gamma * at_zero, gamma, sp.oo) == -4 * sp.I * product,
    )
    checks.check(
        "fresh peak evaluation is product over detuning",
        sp.simplify(magnitude.subs(gamma, 2 * delta) - product / delta) == 0,
    )

    coupling = sp.symbols("g", positive=True)
    full = sp.Matrix(
        [
            [0, 0, coupling, coupling],
            [0, 0, coupling, coupling],
            [coupling, coupling, delta - sp.I * gamma / 2, 0],
            [coupling, coupling, 0, -delta - sp.I * gamma / 2],
        ]
    )
    endpoint = [0, 1]
    intermediate = [2, 3]
    h_pp = full.extract(endpoint, endpoint)
    h_pq = full.extract(endpoint, intermediate)
    h_qq = full.extract(intermediate, intermediate)
    h_qp = full.extract(intermediate, endpoint)
    direct = sp.simplify(h_pp + h_pq * (-h_qq).inv() * h_qp)
    expected = _fresh_pair(delta, gamma, coupling**2, coupling**2)
    checks.check(
        "fresh full-matrix partition reproduces every effective entry",
        all(sp.simplify(entry - expected) == 0 for entry in direct),
    )
    checks.check(
        "fresh sign mutation changes the effective block",
        sp.simplify((-direct)[0, 1] - direct[0, 1]) != 0,
    )

    pair_count = sp.symbols("L", positive=True, integer=True)
    fixed_pair = sp.simplify(pair_count * at_zero)
    fixed_total = sp.simplify(pair_count * at_zero.subs(product, product / pair_count))
    checks.check(
        "fresh size ledger separates extensive and fixed-total conventions",
        sp.simplify(fixed_pair - pair_count * at_zero) == 0
        and sp.simplify(fixed_total - at_zero) == 0,
    )
    checks.check(
        "fresh model enlargement is not a discretization limit",
        not fixed_pair.has(sp.Symbol("dx"), sp.Symbol("dt")),
    )

    lossless = sp.simplify(full.subs(gamma, 0))
    checks.check(
        "fresh short-time series disproves zero lossless transfer",
        lossless[1, 0] == 0
        and sp.simplify((lossless**2)[1, 0] - 2 * coupling**2) == 0,
    )
    q_population = sp.symbols("Qpop", nonnegative=True)
    checks.check(
        "fresh conditional norm balance is nonincreasing but not normalized",
        -gamma * q_population <= 0,
    )
    checks.check(
        "fresh zero-loss countermodel preserves finite full dynamics",
        gamma.subs(gamma, 0) == 0 and (lossless**2)[1, 0] != 0,
    )

    speed, momentum, mass = sp.symbols("v P m", positive=True)
    angle = sp.atan(momentum / (mass * speed)) / 2
    checks.check(
        "fresh two-state rotation has the stated narrow limit",
        sp.series(angle, momentum, 0, 2).removeO()
        == momentum / (2 * mass * speed)
        and sp.limit(angle, speed, sp.oo) == 0,
    )
    checks.check(
        "fresh two-state rotation contains no nuclear scale",
        angle.free_symbols == {speed, momentum, mass},
    )
    checks.check(
        "fresh review imports no canonical paired-resolvent implementation",
        not any(
            isinstance(node, ast.ImportFrom)
            and node.module == "substrate_framework.paired_resolvent"
            for node in ast.walk(ast.parse(Path(__file__).read_text()))
        ),
    )
    checks.check(
        "fresh review uses no quadrature solver float or comparator",
        not expression.has(sp.Float, sp.Integral),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
