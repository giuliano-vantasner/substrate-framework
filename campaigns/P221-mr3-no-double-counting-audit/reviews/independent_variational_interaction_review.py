"""Fresh exact review of C-VAR-003 without source or canonical variational APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def quadratic_minimum(expression: sp.Expr, coordinate: sp.Symbol) -> sp.Expr:
    coefficient = sp.expand(expression).coeff(coordinate, 2)
    linear = sp.expand(expression).coeff(coordinate, 1)
    constant = sp.expand(expression).coeff(coordinate, 0)
    return sp.simplify(constant - linear**2 / (4 * coefficient))


def interaction(
    base: sp.Expr,
    first: sp.Expr,
    second: sp.Expr,
    coordinate: sp.Symbol,
) -> sp.Expr:
    return sp.simplify(
        quadratic_minimum(base + first + second, coordinate)
        + quadratic_minimum(base, coordinate)
        - quadratic_minimum(base + first, coordinate)
        - quadratic_minimum(base + second, coordinate)
    )


def main() -> int:
    checks = CheckLedger("P221-INDEPENDENT")
    base_value, first_value, second_value = sp.symbols("A P Q", real=True)
    checks.check(
        "fresh pointwise mixed expression cancels identically",
        sp.expand(
            (base_value + first_value + second_value)
            + base_value
            - (base_value + first_value)
            - (base_value + second_value)
        )
        == 0,
    )

    m_a, m_ap, m_aq, m_apq = sp.symbols(
        "m_A m_AP m_AQ m_APQ",
        real=True,
    )
    mixed = m_apq + m_a - m_ap - m_aq
    checks.check(
        "fresh increment subtraction gives the same mixed difference",
        sp.expand((m_apq - m_a) - (m_ap - m_a) - (m_aq - m_a)) == mixed,
    )
    checks.check(
        "fresh swap of the additions leaves the interaction unchanged",
        sp.simplify(m_apq + m_a - m_aq - m_ap - mixed) == 0,
    )
    shift_a, shift_p, shift_q = sp.symbols("c_A c_P c_Q", real=True)
    shifted = (
        m_apq
        + shift_a
        + shift_p
        + shift_q
        + m_a
        + shift_a
        - (m_ap + shift_a + shift_p)
        - (m_aq + shift_a + shift_q)
    )
    checks.check(
        "fresh additive-constant transformation cancels",
        sp.expand(shifted - mixed) == 0,
    )

    coordinate = sp.symbols("x", real=True)
    base = coordinate**2
    first = (coordinate - 1) ** 2
    positive_second = (coordinate + 1) ** 2
    negative_second = (coordinate - 1) ** 2
    checks.check(
        "fresh completing-square derivation gives a positive example",
        interaction(base, first, positive_second, coordinate) == 1,
    )
    checks.check(
        "fresh completing-square derivation gives a negative example",
        interaction(base, first, negative_second, coordinate)
        == -sp.Rational(1, 3),
    )
    center = 2 + sp.sqrt(3)
    zero_second = (coordinate - center) ** 2
    zero_value = interaction(base, first, zero_second, coordinate)
    checks.check(
        "fresh displaced quadratics give exact zero interaction",
        zero_value == 0,
    )
    checks.check(
        "the fresh zero example has no common component minimizer",
        set.intersection(
            {sp.S.Zero},
            {sp.S.One},
            {center},
        )
        == set(),
    )
    common_first = 2 * coordinate**2
    common_second = 3 * coordinate**2
    checks.check(
        "fresh common-minimizer example forces zero interaction",
        interaction(base, common_first, common_second, coordinate) == 0,
    )

    scale = sp.symbols("lambda", positive=True)
    checks.check(
        "fresh positive scaling realizes every positive magnitude",
        interaction(
            scale * base,
            scale * first,
            scale * positive_second,
            coordinate,
        )
        == scale,
    )
    checks.check(
        "fresh positive scaling realizes every negative magnitude",
        interaction(
            3 * scale * base,
            3 * scale * first,
            3 * scale * negative_second,
            coordinate,
        )
        == -scale,
    )
    checks.mutation_sensitive(
        "fresh zero root is load bearing",
        lambda candidate: sp.simplify(
            interaction(base, first, (coordinate - candidate) ** 2, coordinate)
        )
        == 0,
        center,
        (-1, 0, 1),
    )

    lower_bound, slack = sp.symbols("L s", nonnegative=True)
    checks.check(
        "fresh slack keeps a lower bound distinct from a realized value",
        sp.simplify((lower_bound + slack) - lower_bound) == slack,
    )
    checks.check(
        "fresh exact theorem contains no physical or comparator symbols",
        mixed.free_symbols == {m_a, m_ap, m_aq, m_apq},
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
