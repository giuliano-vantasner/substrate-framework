"""Fresh direct-algebra MR4 review without source or canonical HLS APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P222-INDEPENDENT")
    sigma_one = sp.Matrix([[0, 1], [1, 0]])
    sigma_two = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    x, y = sp.symbols("x y", real=True)
    current_x = sp.I * x * sigma_one
    current_y = sp.I * y * sigma_two
    commutator = current_x * current_y - current_y * current_x
    curvature = -commutator / 4
    checks.check(
        "fresh half-connection curvature carries one sixteenth in trace square",
        sp.simplify(sp.trace(curvature * curvature) - sp.trace(commutator * commutator) / 16)
        == 0,
    )
    checks.check(
        "fresh configuration is non-Abelian and nonvacuous",
        sp.trace(commutator * commutator) == -8 * x**2 * y**2,
    )

    g, e_sk, trace_square = sp.symbols("g e T", positive=True)
    induced = trace_square / (32 * g**2)
    skyrme = trace_square / (32 * e_sk**2)
    solutions = sp.solve(sp.Eq(induced, skyrme), e_sk)
    checks.check(
        "fresh positive coefficient matching gives e equals g",
        solutions == [g],
    )
    checks.mutation_sensitive(
        "fresh one-sixteenth trace factor is load bearing",
        lambda factor: sp.solve(
            sp.Eq(trace_square * factor / (2 * g**2), skyrme),
            e_sk,
        )
        == [g],
        sp.Rational(1, 16),
        (sp.Rational(1, 8), sp.Rational(1, 32)),
    )

    mass, decay, parameter, common_unit = sp.symbols("m F a U", positive=True)
    matching = mass / (sp.sqrt(parameter) * decay)
    checks.check(
        "fresh declared vector mass law retains all three inputs",
        sp.simplify(parameter * matching**2 * decay**2 - mass**2) == 0
        and matching.free_symbols == {mass, decay, parameter},
    )
    closure = sp.sqrt(mass) / (
        sp.sqrt(common_unit) * parameter ** sp.Rational(1, 4)
    )
    checks.check(
        "fresh common-unit elimination gives the fourth-root-a closure",
        sp.simplify(closure**2 - mass / (sp.sqrt(parameter) * common_unit)) == 0,
    )
    checks.check(
        "fresh closure retains mass common-unit and KSRF parameter",
        closure.free_symbols == {mass, common_unit, parameter},
    )
    checks.mutation_sensitive(
        "fresh KSRF parameter mutation changes the closure",
        lambda candidate: sp.simplify(candidate - closure.subs(parameter, 2)) == 0,
        closure.subs(parameter, 2),
        (closure.subs(parameter, 1), closure.subs(parameter, 4)),
    )

    electron = sp.symbols("m_e", positive=True)
    specialized = closure.subs(
        {parameter: 2, common_unit: 16 * sp.pi * electron}
    )
    expected = sp.sqrt(mass / (16 * sp.sqrt(2) * sp.pi * electron))
    checks.check(
        "fresh a-two and common-unit specialization matches MR4 algebra",
        sp.simplify(specialized - expected) == 0,
    )
    checks.check(
        "fresh independent mass variations change the dimensionless result",
        sp.diff(expected, mass) != 0 and sp.diff(expected, electron) != 0,
    )
    scale = sp.symbols("rho", positive=True)
    checks.check(
        "fresh common mass scaling exposes ratio rather than absolute prediction",
        sp.simplify(
            expected.subs({mass: scale * mass, electron: scale * electron})
            - expected
        )
        == 0,
    )
    alternative = closure.subs(
        {parameter: sp.Rational(1, 2), common_unit: 16 * sp.pi * electron}
    )
    checks.check(
        "fresh convention coefficient mutation changes e by sqrt two",
        sp.simplify(alternative / expected) == sp.sqrt(2),
    )
    checks.check(
        "fresh dimensional audit rejects e equal to a decay scale over two",
        matching.free_symbols == {mass, decay, parameter}
        and sp.simplify(matching - decay / 2) != 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
