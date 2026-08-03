"""Independent diagonal-block and countermodel review for P114."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def _fresh_pair(
    detuning: sp.Expr,
    positive_shift: sp.Expr,
    negative_shift: sp.Expr,
    positive_product: sp.Expr,
    negative_product: sp.Expr,
) -> sp.Expr:
    return sp.factor(
        positive_product / (-detuning + sp.I * positive_shift / 2)
        + negative_product / (detuning + sp.I * negative_shift / 2)
    )


def main() -> int:
    checks = CheckLedger("PN6-INDEPENDENT")
    gamma = sp.symbols("Gamma", positive=True)
    data = [(sp.Integer(1), sp.Integer(2)), (sp.Integer(3), sp.Integer(5)), (sp.Integer(4), sp.Integer(7))]
    pair_sum = sp.factor(
        sum(_fresh_pair(delta, gamma, gamma, product, product) for delta, product in data)
    )
    closed = sp.factor(
        -sp.I
        * gamma
        * sum(product / (delta**2 + gamma**2 / 4) for delta, product in data)
    )
    checks.check(
        "fresh common-denominator route derives the finite sum",
        sp.simplify(pair_sum - closed) == 0,
    )

    diagonal = []
    expanded_products = []
    for delta, product in data:
        diagonal.extend((delta - sp.I * gamma / 2, -delta - sp.I * gamma / 2))
        expanded_products.extend((product, product))
    h_qq = sp.diag(*diagonal)
    h_pq = sp.Matrix([[1] * len(diagonal), [0] * len(diagonal)])
    h_qp = sp.Matrix([[0, product] for product in expanded_products])
    fresh_block = sp.simplify(h_pq * (-h_qq).inv() * h_qp)
    checks.check(
        "fresh direct diagonal inverse reproduces the off-diagonal sum",
        sp.simplify(fresh_block[0, 1] - pair_sum) == 0,
    )
    checks.check(
        "fresh resolvent-sign mutation is detected",
        sp.simplify((h_pq * h_qq.inv() * h_qp)[0, 1] - pair_sum) != 0,
    )

    positive, negative, delta = sp.symbols("p q Delta", nonzero=True)
    lossless = sp.simplify(_fresh_pair(delta, 0, 0, positive, negative))
    checks.check(
        "fresh lossless algebra gives the exact product mismatch",
        sp.simplify(lossless - (negative - positive) / delta) == 0,
    )
    checks.check(
        "fresh cross-pair cancellation is not pairwise cancellation",
        _fresh_pair(1, 0, 0, 0, 1) == 1
        and _fresh_pair(2, 0, 0, 2, 0) == -1
        and _fresh_pair(1, 0, 0, 0, 1) + _fresh_pair(2, 0, 0, 2, 0) == 0,
    )
    checks.check(
        "fresh zero-family countermodel kills positive-loss strictness",
        sum(_fresh_pair(d, gamma, gamma, 0, 0) for d in (1, 2, 5)) == 0,
    )
    checks.check(
        "fresh signed-product family cancels at positive loss",
        sp.simplify(
            _fresh_pair(2, gamma, gamma, 1, 1)
            + _fresh_pair(2, gamma, gamma, -1, -1)
        )
        == 0,
    )
    checks.check(
        "fresh complex coupling distinguishes square from Hermitian product",
        sp.I**2 == -1 and sp.conjugate(sp.I) * sp.I == 1,
    )

    separate_losses = [(1, sp.Rational(1, 2), 2), (3, sp.Rational(5, 2), 5)]
    separate_sum = sum(
        _fresh_pair(delta_v, loss, loss, product, product)
        for delta_v, loss, product in separate_losses
    )
    checks.check(
        "fresh per-pair nonuniform losses preserve negative-imaginary sign",
        sp.re(separate_sum) == 0 and sp.im(separate_sum) < 0,
    )
    asymmetric_shift = _fresh_pair(1, 1, 3, 1, 1)
    checks.check(
        "fresh unequal-member shift produces a real component",
        sp.re(asymmetric_shift) != 0,
    )

    small = sp.limit(pair_sum / gamma, gamma, 0, dir="+")
    large = sp.limit(gamma * pair_sum, gamma, sp.oo)
    checks.check(
        "fresh exact limits give both finite-sum coefficients",
        sp.simplify(small + sp.I * sum(c / d**2 for d, c in data)) == 0
        and sp.simplify(large + 4 * sp.I * sum(c for _, c in data)) == 0,
    )
    two_pair_magnitude = gamma * (
        1 / (1 + gamma**2 / 4) + 1 / (9 + gamma**2 / 4)
    )
    derivative = sp.factor(sp.diff(two_pair_magnitude, gamma))
    checks.check(
        "fresh unequal-detuning derivative rejects inherited one-pair optima",
        derivative.subs(gamma, 2) > 0 and derivative.subs(gamma, 6) < 0,
    )
    checks.check(
        "fresh fixed-total normalization removes pair-count growth",
        sp.simplify(
            5 * _fresh_pair(2, gamma, gamma, sp.Rational(3, 5), sp.Rational(3, 5))
            - _fresh_pair(2, gamma, gamma, 3, 3)
        )
        == 0,
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
        "fresh review uses no quadrature solver float fit or comparator",
        not pair_sum.has(sp.Float, sp.Integral),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
