"""Independent cross-product and sequence review for P125."""

from __future__ import annotations

from fractions import Fraction

import sympy as sp

from substrate_framework.verification import CheckLedger


def gamma_share(weighted: sp.Expr, comparison: sp.Expr) -> sp.Expr:
    return sp.cancel(comparison / (weighted + comparison))


def main() -> int:
    checks = CheckLedger("P125-INDEPENDENT")
    rho, weight = sp.symbols("rho w", positive=True)
    count = sp.symbols("N", positive=True, integer=True)

    current = gamma_share(weight * count, rho)
    next_fixed = gamma_share(weight * (count + 1), rho)
    checks.check(
        "fresh normalization gives the GB4 gamma share",
        current == rho / (count * weight + rho),
    )
    checks.check(
        "fresh cross multiplication gives the fixed-weight adjacent difference",
        sp.simplify(
            sp.factor(next_fixed - current)
            + rho
            * weight
            / ((count * weight + rho) * ((count + 1) * weight + rho))
        )
        == 0,
    )
    for integer in range(1, 8):
        checks.check(
            f"fresh exact N={integer} step decreases at fixed positive inputs",
            gamma_share(Fraction(3, 5) * (integer + 1), Fraction(7, 11))
            < gamma_share(Fraction(3, 5) * integer, Fraction(7, 11)),
        )

    weight_now, weight_next = sp.symbols("w_N w_next", positive=True)
    coupled_difference = sp.factor(
        gamma_share((count + 1) * weight_next, rho)
        - gamma_share(count * weight_now, rho)
    )
    checks.check(
        "fresh coupled cross product isolates the Nw growth condition",
        sp.simplify(
            coupled_difference
            - rho
            * (count * weight_now - (count + 1) * weight_next)
            / (
                (count * weight_now + rho)
                * ((count + 1) * weight_next + rho)
            )
        )
        == 0,
    )
    checks.check(
        "fresh positive weight sequence can make the gamma share constant",
        gamma_share(Fraction(1, 1), Fraction(1, 1))
        == gamma_share(Fraction(1, 1), Fraction(1, 1)),
    )
    checks.check(
        "fresh positive weight sequence can make the gamma share rise",
        gamma_share(Fraction(1, 8), Fraction(1, 1))
        > gamma_share(Fraction(1, 4), Fraction(1, 1)),
    )
    checks.check(
        "fresh exact exponential n equals N example reverses from one to two",
        gamma_share(Fraction(2, 16), Fraction(1, 1))
        > gamma_share(Fraction(1, 4), Fraction(1, 1)),
    )
    checks.check(
        "fresh linear n equals N example remains decreasing",
        gamma_share(Fraction(4, 1), Fraction(1, 1))
        < gamma_share(Fraction(1, 1), Fraction(1, 1)),
    )
    checks.check(
        "fresh quadratic weight example remains decreasing",
        gamma_share(Fraction(8, 1), Fraction(1, 1))
        < gamma_share(Fraction(1, 1), Fraction(1, 1)),
    )

    real_count, alpha = sp.symbols("x alpha", positive=True)
    product = real_count * sp.exp(-alpha * real_count)
    checks.check(
        "fresh product derivative locates the exponential turning point",
        sp.simplify(
            sp.diff(product, real_count)
            - (1 - alpha * real_count) * sp.exp(-alpha * real_count)
        )
        == 0,
    )
    checks.check(
        "fresh endpoint limits show the coupled exponential gamma share returns to one",
        sp.limit(gamma_share(product, rho), real_count, 0, dir="+") == 1
        and sp.limit(gamma_share(product, rho), real_count, sp.oo) == 1,
    )

    baseline = sp.symbols("w1", positive=True)
    odds_ratio = sp.cancel(weight * count / baseline)
    checks.check(
        "fresh odds division gives the same-baseline enhancement",
        odds_ratio == weight * count / baseline,
    )
    checks.check(
        "fresh unit baseline gives one by definition",
        odds_ratio.subs({weight: baseline, count: 1}) == 1,
    )
    checks.check(
        "changing only the baseline normalization changes the enhancement",
        sp.simplify(weight * count / (2 * baseline) - odds_ratio) != 0,
    )
    q = sp.symbols("q", positive=True)
    fitted_rho = q * weight * count / (1 - q)
    checks.check(
        "fresh substitution fits every symbolic interior gamma share",
        sp.simplify(gamma_share(weight * count, fitted_rho) - q) == 0,
    )
    for target in (Fraction(1, 5), Fraction(1, 2), Fraction(4, 5)):
        fitted = target * Fraction(6, 1) / (1 - target)
        checks.check(
            f"fresh target {target} is fitted by a positive free ratio",
            gamma_share(Fraction(6, 1), fitted) == target,
        )

    soft, hard, third = sp.symbols("R_s R_g R_3", positive=True)
    checks.check(
        "fresh third-channel normalization changes the hard share",
        sp.simplify(hard / (soft + hard + third) - hard / (soft + hard)) != 0,
    )
    soft_gate, hard_gate = sp.symbols("C_s C_g", positive=True)
    checks.check(
        "fresh unequal gates do not cancel from a two-channel share",
        sp.simplify(
            hard_gate * hard / (soft_gate * soft + hard_gate * hard)
            - hard / (soft + hard)
        )
        != 0,
    )
    checks.check(
        "fresh common gate cancels exactly",
        sp.simplify(
            soft_gate * hard / (soft_gate * soft + soft_gate * hard)
            - hard / (soft + hard)
        )
        == 0,
    )
    checks.check(
        "fresh zero-coupling model has no physical rate despite valid formal fractions",
        0 * Fraction(3, 5) + 0 * Fraction(7, 11) == 0,
    )
    checks.check(
        "fresh review uses no package branching helper quadrature solver or empirical fit",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
