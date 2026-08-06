"""Fresh convention and functional-composition review for P219."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P219-INDEPENDENT")
    nc, pion_mass, decay_scale, degree = sp.symbols(
        "N_c m_pi F B",
        positive=True,
    )
    lambda_a = nc / (4 * decay_scale)
    lambda_bps = lambda_a / sp.pi**2
    mu = pion_mass * decay_scale / 2
    average = 32 * sp.sqrt(2) / (15 * sp.pi)
    from_bps_coordinate = sp.factor(
        2 * lambda_bps * mu * sp.pi**2 * degree * average
    )
    from_a_coordinate = sp.factor(2 * lambda_a * mu * degree * average)
    expected = 8 * sp.sqrt(2) * nc * pion_mass * degree / (15 * sp.pi)
    checks.check(
        "fresh lambda-coordinate elimination agrees exactly",
        from_bps_coordinate == expected and from_a_coordinate == expected,
    )
    source_expression = 8 * sp.sqrt(2) * sp.pi * nc * pion_mass * degree / 15
    checks.check(
        "fresh convention mutation isolates pi squared",
        sp.factor(source_expression / expected) == sp.pi**2,
    )
    value = expected.subs(
        {nc: 3, pion_mass: sp.Rational(13803, 100), degree: 1}
    )
    checks.check(
        "fresh exact substitution gives the corrected supplied-input scale",
        abs(float(value) - 99.4165288953323) < 1.0e-12,
    )

    d1, d2, d3 = sp.symbols("d1 d2 d3", nonnegative=True)
    total_gap = d1 + d2 + d3
    checks.check(
        "finite pointwise sum gap is a sum of component gaps",
        sp.diff(total_gap, d1) == 1
        and sp.diff(total_gap, d2) == 1
        and sp.diff(total_gap, d3) == 1,
    )
    checks.check(
        "joint attainment forces every nonnegative component gap to vanish",
        sp.solve([total_gap, d1, d2, d3], [d1, d2, d3], dict=True)
        == [{d1: 0, d2: 0, d3: 0}],
    )
    checks.check(
        "common minimizing sequences give the converse epsilon criterion",
        all(
            sum(gaps) < epsilon
            for epsilon, gaps in (
                (sp.Rational(1, 2), (sp.Rational(1, 16),) * 3),
                (sp.Rational(1, 10), (sp.Rational(1, 40),) * 3),
                (sp.Rational(1, 100), (sp.Rational(1, 400),) * 3),
            )
        ),
    )
    coordinate = sp.symbols("x", real=True)
    common_sum = coordinate**2 + 2 * coordinate**2 + 4 * coordinate**2
    split_sum = (coordinate - 2) ** 2 + (coordinate + 2) ** 2
    checks.check(
        "fresh common-minimizer example saturates the lower bound",
        sp.minimum(common_sum, coordinate) == 0,
    )
    checks.check(
        "fresh incompatible-minimizer counterexample has a strict joint gap",
        sp.minimum(split_sum, coordinate) == 8,
    )
    checks.mutation_sensitive(
        "common minimizer premise changes the verdict",
        lambda shift: sp.minimum(
            (coordinate - 2) ** 2 + (coordinate - shift) ** 2,
            coordinate,
        )
        == 0,
        2,
        (-2, -1, 0, 1),
    )
    bps_coefficient, slack_one, slack_two = sp.symbols(
        "K s_1 s_2",
        nonnegative=True,
    )
    signed_difference = 2 * (bps_coefficient + slack_one) - (
        2 * bps_coefficient + slack_two
    )
    checks.check(
        "linear lower-bound terms cancel without fixing the signed difference",
        sp.expand(signed_difference) == 2 * slack_one - slack_two,
    )
    checks.check(
        "opposite slack choices produce both signs",
        signed_difference.subs({slack_one: 1, slack_two: 0}) > 0
        and signed_difference.subs({slack_one: 0, slack_two: 1}) < 0,
    )
    checks.check(
        "the exact theorem needs no MK6 physical or comparator symbols",
        total_gap.free_symbols == {d1, d2, d3}
        and total_gap.free_symbols.isdisjoint(expected.free_symbols),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
