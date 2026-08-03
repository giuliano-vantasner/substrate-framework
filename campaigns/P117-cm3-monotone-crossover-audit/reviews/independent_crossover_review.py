"""Implementation-independent exact review of P117's crossover theorem.

This review deliberately does not import ``substrate_framework.crossovers``.
It rebuilds both inverses from fresh symbolic response definitions.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("C-XOV-001-INDEPENDENT")

    energy, scale, odds = sp.symbols("E E0 u", positive=True)
    response = 1 - sp.exp(-energy / scale)
    level = odds / (1 + odds)
    crossing = scale * sp.log(1 + odds)

    checks.check(
        "positive log coordinate parameterizes an interior unit level",
        level.is_positive is True and (1 - level).is_positive is True,
    )
    checks.check(
        "fresh logarithmic inversion gives the exponential crossing",
        sp.simplify(-scale * sp.log(1 - level) - crossing) == 0,
    )
    checks.check(
        "fresh exponential substitution has zero residual",
        sp.simplify(response.subs(energy, crossing) - level) == 0,
    )
    response_derivative = sp.diff(response, energy)
    checks.check(
        "the exponential response is strictly increasing",
        response_derivative.is_positive is True,
    )
    checks.check(
        "the exponential response has range zero inclusive to one exclusive",
        sp.limit(response, energy, 0, dir="+") == 0
        and sp.limit(response, energy, sp.oo) == 1
        and response.subs(energy, crossing) < 1,
    )
    checks.check(
        "strict increase makes the fresh crossing unique",
        response_derivative.is_positive is True
        and sp.solve(sp.Eq(response, level), energy) == [crossing],
    )

    generic_level = sp.symbols("c", positive=True)
    generic_inverse = -scale * sp.log(1 - generic_level)
    level_derivative = sp.diff(generic_inverse, generic_level)
    level_second_derivative = sp.diff(generic_inverse, generic_level, 2)
    checks.check(
        "fresh inverse sensitivities agree on the interior parameterization",
        sp.simplify(
            level_derivative.subs(generic_level, level)
            - scale * (1 + odds)
        )
        == 0
        and sp.simplify(
            level_second_derivative.subs(generic_level, level)
            - scale * (1 + odds) ** 2
        )
        == 0,
    )
    checks.check(
        "level sensitivity and convexity are positive",
        (scale * (1 + odds)).is_positive is True
        and (scale * (1 + odds) ** 2).is_positive is True,
    )
    checks.check(
        "the inverse is covariant under common energy scaling",
        sp.simplify(
            (sp.symbols("rho", positive=True) * scale)
            * sp.log(1 + odds)
        )
        == sp.symbols("rho", positive=True) * crossing,
    )
    checks.check(
        "the half-level specialization is exactly log two",
        sp.simplify(
            generic_inverse.subs({generic_level: sp.Rational(1, 2), scale: 1})
            - sp.log(2)
        )
        == 0,
    )
    checks.check(
        "the lower endpoint is finite and the upper endpoint only a limit",
        generic_inverse.subs(generic_level, 0) == 0
        and sp.limit(crossing, odds, sp.oo) == sp.oo
        and sp.limit(level, odds, sp.oo) == 1,
    )

    barrier, shift, q = sp.symbols("G U q", positive=True)
    shifted_factor = sp.exp(-sp.sqrt(barrier / (energy + shift)))
    shifted_floor = sp.exp(-sp.sqrt(barrier / shift))
    shifted_crossing = barrier / q**2 - shift
    checks.check(
        "fresh shifted factor has the accepted positive zero-energy floor",
        sp.limit(shifted_factor, energy, 0, dir="+") == shifted_floor
        and shifted_floor.is_positive is True,
    )
    checks.check(
        "the fresh shifted factor is strictly increasing",
        sp.diff(shifted_factor, energy).is_positive is True,
    )
    positive_crossing = sp.symbols("X", positive=True)
    parameterized_barrier = (positive_crossing + shift) * q**2
    checks.check(
        "fresh shifted inversion has zero residual on its interior domain",
        sp.simplify(
            shifted_factor.subs(
                {
                    barrier: parameterized_barrier,
                    energy: positive_crossing,
                }
            )
            - sp.exp(-q)
        )
        == 0,
    )
    checks.check(
        "fresh shifted inversion returns the parameterized positive energy",
        sp.simplify(
            shifted_crossing.subs(barrier, parameterized_barrier)
            - positive_crossing
        )
        == 0,
    )
    floor_margin = sp.symbols("r", positive=True)
    floor_parameterized_barrier = shift * (q + floor_margin) ** 2
    level_floor_ratio = sp.simplify(
        sp.exp(-q)
        / shifted_floor.subs(barrier, floor_parameterized_barrier)
    )
    checks.check(
        "positive shifted crossing is equivalent to an above-floor margin",
        sp.simplify(sp.log(level_floor_ratio) - floor_margin) == 0
        and floor_margin.is_positive is True
        and sp.factor(
            shifted_crossing.subs(barrier, floor_parameterized_barrier)
        ).is_positive
        is True,
    )
    shifted_generic_inverse = barrier / sp.log(generic_level) ** 2 - shift
    checks.check(
        "fresh shifted sensitivities have the exact signs",
        sp.simplify(
            sp.diff(shifted_generic_inverse, generic_level).subs(
                generic_level,
                sp.exp(-q),
            )
            - 2 * barrier * sp.exp(q) / q**3
        )
        == 0
        and (2 * barrier * sp.exp(q) / q**3).is_positive is True
        and sp.diff(shifted_generic_inverse, barrier).subs(
            generic_level,
            sp.exp(-q),
        )
        == q**-2
        and sp.diff(shifted_generic_inverse, shift) == -1,
    )
    rho = sp.symbols("rho", positive=True)
    checks.check(
        "the shifted inverse is covariant under common energy scaling",
        sp.simplify(
            (rho * barrier) / q**2
            - rho * shift
            - rho * shifted_crossing
        )
        == 0,
    )
    checks.check(
        "the exponential surrogate and shifted factor disagree at zero",
        response.subs(energy, 0) == 0 and shifted_floor.is_positive is True,
    )

    gamma, omega, coupling, detuning = sp.symbols(
        "Gamma omega a Delta",
        positive=True,
    )
    accepted_cm2_factor = (
        omega
        * coupling
        / (2 * sp.pi * (detuning**2 + gamma**2 / 4))
    )
    checks.check(
        "a fresh C-CMP factor is not a flat level in loss",
        sp.diff(accepted_cm2_factor, gamma).is_negative is True,
    )
    target = sp.symbols("E_target", positive=True)
    checks.check(
        "a free exponential scale fits any positive target",
        sp.simplify(
            crossing.subs(scale, target / sp.log(1 + odds)) - target
        )
        == 0,
    )
    prefactor, target_rate = sp.symbols("nu R", positive=True)
    checks.check(
        "an undeclared physical prefactor makes the level nonidentifying",
        0 * response == 0
        and sp.simplify(
            (prefactor * response).subs(prefactor, target_rate / response)
            - target_rate
        )
        == 0,
    )

    x = sp.symbols("x", real=True)
    plateau = sp.Piecewise((x, x < 1), (1, True))
    skipped = sp.Piecewise((0, x < 0), (1, True))
    checks.check(
        "dropping strictness permits repeated level crossings",
        plateau.subs(x, 1) == 1 and plateau.subs(x, 2) == 1,
    )
    checks.check(
        "dropping continuity permits a skipped interior level",
        skipped.subs(x, -1) == 0
        and skipped.subs(x, 1) == 1
        and sp.solve(sp.Eq(skipped, sp.Rational(1, 2)), x) == [],
    )
    checks.check(
        "dropping monotonicity permits two crossings",
        sp.solve(sp.Eq(x**2, 1), x) == [-1, 1],
    )

    checks.mutation_sensitive(
        "fresh exponential inverse is load bearing",
        lambda candidate: sp.simplify(
            response.subs(energy, candidate) - level
        )
        == 0,
        crossing,
        (-crossing, 2 * crossing, scale / sp.log(1 + odds)),
    )
    checks.mutation_sensitive(
        "fresh shifted inverse signs and logarithmic power are load bearing",
        lambda candidate: sp.simplify(
            candidate - shifted_crossing
        )
        == 0,
        shifted_crossing,
        (
            barrier / q**2 + shift,
            barrier / q - shift,
            barrier * q**2 - shift,
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
