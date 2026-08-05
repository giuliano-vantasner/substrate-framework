#!/usr/bin/env python3
"""Fresh exact information audit of CF5 without canonical physics imports."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class TubeConvention:
    area_coefficient: sp.Expr
    slope_coefficient: sp.Expr


def main() -> int:
    checks = CheckLedger("P170-INDEPENDENT-CF5-INFORMATION")
    flux, tension, area = sp.symbols("Phi sigma A", positive=True)
    solved_area = sp.solve(sp.Eq(tension, flux**2 / (2 * area)), area)
    checks.check(
        "solving the ideal-tube equation produces one tension-dependent area",
        solved_area == [flux**2 / (2 * tension)],
    )
    inverted_area = solved_area[0]
    checks.check(
        "direct back-substitution is an identity for every positive tension",
        sp.simplify(flux**2 / (2 * inverted_area) - tension) == 0,
    )
    checks.check(
        "the inverted area remains load-bearing on the supplied tension",
        sp.diff(inverted_area, tension) == -flux**2 / (2 * tension**2),
    )
    alternative = sp.symbols("sigma_alt", positive=True)
    alternative_area = inverted_area.subs(tension, alternative)
    checks.check(
        "a distinct positive tension constructs a distinct area and closes identically",
        sp.simplify(alternative_area - inverted_area) != 0
        and sp.simplify(flux**2 / (2 * alternative_area) - alternative) == 0,
    )

    def closes(candidate: object) -> bool:
        assert isinstance(candidate, TubeConvention)
        candidate_area = candidate.area_coefficient * flux**2 / tension
        return sp.simplify(
            candidate.slope_coefficient * flux**2 / candidate_area - tension
        ) == 0

    checks.mutation_sensitive(
        "independent inversion coefficient pairing",
        closes,
        TubeConvention(sp.Rational(1, 2), sp.Rational(1, 2)),
        [
            TubeConvention(1, sp.Rational(1, 2)),
            TubeConvention(sp.Rational(1, 2), 1),
            TubeConvention(sp.Rational(1, 4), sp.Rational(1, 2)),
        ],
    )

    winding, gauge, vacuum, self_coupling = sp.symbols(
        "n g v lambda", positive=True
    )
    quantized_flux = 2 * sp.pi * winding / gauge
    vector_length = 1 / (gauge * vacuum)
    scalar_length = 1 / (vacuum * sp.sqrt(2 * self_coupling))
    penetration_ratio = sp.simplify(
        inverted_area.subs(flux, quantized_flux) / vector_length**2
    )
    checks.check(
        "independent elimination cancels the gauge coupling from the ratio",
        penetration_ratio == 2 * sp.pi**2 * winding**2 * vacuum**2 / tension
        and gauge not in penetration_ratio.free_symbols,
    )
    ratio_symbol = sp.symbols("r", positive=True)
    checks.check(
        "an independent ratio value would merely invert to a corresponding tension",
        sp.solve(sp.Eq(penetration_ratio, ratio_symbol), tension)
        == [2 * sp.pi**2 * vacuum**2 * winding**2 / ratio_symbol],
    )

    lower, upper = sp.Rational(1, 10), sp.Integer(100)
    mapped_interval = (
        sp.simplify(2 * sp.pi**2 / upper),
        sp.simplify(2 * sp.pi**2 / lower),
    )
    checks.check(
        "the declared ratio window maps to a factor-one-thousand tension interval",
        sp.simplify(mapped_interval[1] / mapped_interval[0]) == 1000,
    )
    demo = sp.Rational(4211567, 1_000_000)

    def in_window(candidate: sp.Expr) -> bool:
        value = sp.N(
            penetration_ratio.subs(
                {winding: 1, vacuum: 1, tension: candidate}
            ),
            30,
        )
        return bool(lower < value < upper)

    checks.check(
        "the reported demo tension is inside the declared window",
        in_window(demo),
    )
    checks.check(
        "one-tenth tenfold and fortyfold independent mutations remain accepted",
        in_window(demo / 10) and in_window(10 * demo) and in_window(40 * demo),
    )
    checks.check(
        "the source's thousand-scale example is rejected only at the lower boundary",
        not in_window(sp.Integer(1000))
        and sp.N(penetration_ratio.subs(
            {winding: 1, vacuum: 1, tension: 1000}
        )) < lower,
    )
    checks.check(
        "vector and scalar inverse lengths give inequivalent area ratios",
        sp.simplify(
            (inverted_area / scalar_length**2)
            / (inverted_area / vector_length**2)
        )
        == 2 * self_coupling / gauge**2,
    )
    convention_factor = sp.symbols("c_area", positive=True)
    checks.check(
        "a free core-area convention changes the alleged match continuously",
        sp.diff(penetration_ratio / convention_factor, convention_factor) != 0,
    )

    profile_norm, profile_second_moment = sp.symbols("M0 M2", positive=True)
    profile_area = sp.pi * profile_second_moment / profile_norm
    checks.check(
        "a profile-derived geometric area requires independent moment observables",
        profile_area.has(profile_norm, profile_second_moment)
        and not profile_area.has(tension, flux),
    )
    checks.check(
        "equating profile geometry to the inverted area is an additional premise",
        sp.solve(sp.Eq(profile_area, inverted_area), profile_second_moment)
        == [flux**2 * profile_norm / (2 * sp.pi * tension)],
    )
    checks.check(
        "the inverted area itself contains no independent profile moment",
        not inverted_area.has(profile_norm, profile_second_moment),
    )

    total = checks.finish()
    print(f"P170 INDEPENDENT CF5 INFORMATION REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
