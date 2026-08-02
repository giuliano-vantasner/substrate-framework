"""Independent exact P083 review without importing the new running APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P083-INDEPENDENT")
    electromagnetic = sp.Rational(1279, 10)
    strong = sp.Rational(500, 59)
    weight = sp.Rational(5, 3)
    beta_1 = sp.Rational(41, 10)
    beta_2 = -sp.Rational(19, 6)
    beta_3 = sp.Integer(-7)

    denominator = sp.factor(
        beta_2 + weight * beta_1 - (1 + weight) * beta_3
    )
    running = sp.factor(
        (electromagnetic - (1 + weight) * strong) / denominator
    )
    common = sp.factor(strong - beta_3 * running)
    checks.check(
        "fresh elimination derives exact common and running coordinates",
        denominator == sp.Rational(67, 3)
        and running == sp.Rational(186383, 39530)
        and common == sp.Rational(1639681, 39530),
    )

    inverse_1 = sp.factor(common + running * beta_1)
    inverse_2 = sp.factor(common + running * beta_2)
    inverse_3 = sp.factor(common + running * beta_3)
    weak = sp.factor(inverse_2 / electromagnetic)
    checks.check(
        "fresh inverse couplings close both observation equations",
        inverse_3 == strong
        and inverse_2 + weight * inverse_1 == electromagnetic,
    )
    checks.check(
        "fresh weak coordinate matches the exact source reconstruction",
        weak == sp.Rational(6296809, 30335322),
    )

    matrix = sp.Matrix(
        [
            [1, beta_1, electromagnetic / weight],
            [1, beta_2, -electromagnetic],
            [1, beta_3, 0],
        ]
    )
    rhs = sp.Matrix([electromagnetic / weight, 0, strong])
    checks.check(
        "fresh three-coordinate determinant is nonzero",
        matrix.det() != 0 and matrix.rank() == matrix.row_join(rhs).rank() == 3,
    )
    checks.check(
        "fresh three-coordinate solve identifies the alleged output as a fitted coordinate",
        matrix.inv() * rhs == sp.Matrix([common, running, weak]),
    )
    checks.check(
        "fresh equation-removal audit restores one null direction",
        matrix[:2, :].rank() == 2
        and len(matrix[:2, :].nullspace()) == 1
        and matrix[:2, :].nullspace()[0][2] != 0,
    )

    boundary_weight = sp.Symbol("n", positive=True)
    checks.check(
        "fresh common-coupling boundary depends on supplied normalization",
        sp.diff(1 / (1 + boundary_weight), boundary_weight) != 0
        and (1 / (1 + boundary_weight)).subs(boundary_weight, weight)
        == sp.Rational(3, 8),
    )
    q = sp.Symbol("q", positive=True)
    checks.check(
        "fresh paired Abelian coordinate change preserves the electromagnetic row",
        sp.simplify((q * weight) * (inverse_1 / q) - weight * inverse_1) == 0
        and sp.simplify((q * weight) * (beta_1 / q) - weight * beta_1) == 0,
    )
    checks.check(
        "fresh Abelian coordinate change does not preserve cross-sector equality",
        sp.simplify(inverse_1 / q - inverse_2) != sp.simplify(inverse_1 - inverse_2),
    )

    measured = sp.Rational(11561, 50000)
    fixed = sp.Matrix(
        [
            (1 - measured) * electromagnetic / weight,
            measured * electromagnetic,
            strong,
        ]
    )
    design = sp.Matrix([[1, beta_1], [1, beta_2], [1, beta_3]])
    checks.check(
        "fresh fixed-data augmented rank rejects exact three-way unification",
        design.rank() == 2 and design.row_join(fixed).rank() == 3,
    )
    crossings = (
        sp.factor((fixed[0] - fixed[1]) / (beta_1 - beta_2)),
        sp.factor((fixed[0] - fixed[2]) / (beta_1 - beta_3)),
        sp.factor((fixed[1] - fixed[2]) / (beta_2 - beta_3)),
    )
    checks.check(
        "fresh fixed-data pairwise crossings are exactly distinct",
        crossings
        == (
            sp.Rational(27584193, 6812500),
            sp.Rational(7451936137, 1637250000),
            sp.Rational(1867213863, 339250000),
        )
        and len(set(crossings)) == 3,
    )
    checks.check(
        "fresh reconstructed pairwise crossings coincide by construction",
        {
            sp.factor((inverse_1 - inverse_2) / (beta_1 - beta_2)),
            sp.factor((inverse_1 - inverse_3) / (beta_1 - beta_3)),
            sp.factor((inverse_2 - inverse_3) / (beta_2 - beta_3)),
        }
        == {running},
    )

    target = sp.Symbol("target", positive=True)
    target_inverse = sp.Matrix(
        [
            (1 - target) * electromagnetic / weight,
            target * electromagnetic,
            strong,
        ]
    )
    offsets = target_inverse - sp.ones(3, 1) * strong
    checks.check(
        "fresh matching offsets realize every symbolic target",
        target_inverse - offsets == sp.ones(3, 1) * strong
        and target in offsets.free_symbols,
    )
    checks.check(
        "fresh coefficient mutation changes the reconstructed weak coordinate",
        sp.factor(
            (
                strong
                + (beta_2 - beta_3)
                * (electromagnetic - (1 + weight) * strong)
                / (
                    beta_2
                    + weight * (beta_1 + 1)
                    - (1 + weight) * beta_3
                )
            )
            / electromagnetic
            - weak
        )
        != 0,
    )
    residual = sp.factor(abs(weak - measured) / measured)
    checks.check(
        "fresh comparator residual is nonzero and approximately ten percent",
        residual == sp.Rational(17933103821, 175353328821)
        and sp.Rational(1, 10) < residual < sp.Rational(11, 100),
    )
    checks.check(
        "fresh derivation requires no numerical quadrature or solver",
        not any(
            expression.has(sp.Integral)
            for expression in (denominator, running, common, weak, residual)
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
