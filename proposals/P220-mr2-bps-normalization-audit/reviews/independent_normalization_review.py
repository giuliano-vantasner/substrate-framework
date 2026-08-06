"""Fresh direct-algebra review of P220 without source or canonical physics APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def coupling_map(lambda_bps: sp.Expr, current_scale: sp.Expr) -> sp.Expr:
    """Solve the positive same-density branch for B_A=current_scale*B_BPS."""

    return sp.simplify(sp.pi**2 * lambda_bps / current_scale)


def main() -> int:
    checks = CheckLedger("P220-INDEPENDENT")
    profile = sp.symbols("f", real=True)
    normalized = sp.simplify(
        4
        * sp.pi
        * sp.integrate(-sp.sin(profile) ** 2 / (2 * sp.pi**2), (profile, sp.pi, 0))
    )
    unnormalized = sp.simplify(
        4 * sp.pi * sp.integrate(-sp.sin(profile) ** 2, (profile, sp.pi, 0))
    )
    checks.check(
        "fresh hedgehog integral detects the target-volume normalization",
        normalized == 1 and unnormalized == 2 * sp.pi**2,
    )

    lambda_a, lambda_bps, current, scale = sp.symbols(
        "lambda_A lambda_BPS B q",
        positive=True,
    )
    solved = sp.solve(
        sp.Eq(lambda_a**2 * (scale * current) ** 2, lambda_bps**2 * sp.pi**4 * current**2),
        lambda_a,
    )
    checks.check(
        "fresh positive-root solve retains the current scale",
        solved == [coupling_map(lambda_bps, scale)],
    )
    checks.mutation_sensitive(
        "fresh current-rescaling mutation changes the coupling map",
        lambda candidate: sp.simplify(
            coupling_map(lambda_bps, candidate) - sp.pi**2 * lambda_bps
        )
        == 0,
        1,
        (2, sp.Rational(1, 2), sp.pi),
    )

    mu, average, degree = sp.symbols("mu W B_degree", positive=True)
    bps_coordinate = 2 * lambda_bps * mu * sp.pi**2 * degree * average
    a_coordinate = 2 * lambda_a * mu * degree * average
    checks.check(
        "fresh bound transformation consumes the pi-squared factor",
        sp.simplify(a_coordinate.subs(lambda_a, sp.pi**2 * lambda_bps) - bps_coordinate)
        == 0,
    )
    angle = sp.symbols("chi", real=True)
    target_average = sp.simplify(
        4
        * sp.pi
        / (2 * sp.pi**2)
        * sp.integrate(
            sp.sin(angle) ** 2 * sp.sqrt(2) * sp.sin(angle / 2),
            (angle, 0, sp.pi),
        )
    )
    checks.check(
        "fresh target integral gives the declared potential average",
        target_average == 32 * sp.sqrt(2) / (15 * sp.pi),
    )

    nc, pion_mass, decay_scale = sp.symbols("N_c m_pi F", positive=True)
    supplied_lambda_a = nc / (4 * decay_scale)
    supplied_mu = pion_mass * decay_scale / 2
    corrected = sp.factor(
        2 * supplied_lambda_a * supplied_mu * degree * target_average
    )
    expected = 8 * sp.sqrt(2) * nc * pion_mass * degree / (15 * sp.pi)
    checks.check(
        "fresh supplied-input elimination gives the corrected expression",
        corrected == expected,
    )
    source_expression = 8 * sp.sqrt(2) * sp.pi * nc * pion_mass * degree / 15
    checks.check(
        "fresh wrong-coordinate mutation isolates exactly pi squared",
        sp.factor(source_expression / corrected) == sp.pi**2,
    )
    checks.check(
        "fresh dependency audit retains N_c pion mass and degree",
        corrected.free_symbols == {nc, pion_mass, degree},
    )
    value = corrected.subs(
        {nc: 3, pion_mass: sp.Rational(13803, 100), degree: 1}
    )
    checks.check(
        "fresh numeric value is fixed only after supplied substitutions",
        abs(float(value) - 99.4165288953323) < 1.0e-12,
    )

    coupling = sp.symbols("e", positive=True)
    c6_a = lambda_a**2 * coupling**4 * decay_scale**2 / (8 * sp.pi**4)
    c6_bps = lambda_bps**2 * coupling**4 * decay_scale**2 / 8
    checks.check(
        "fresh reduced-coefficient coordinates give the same polynomial",
        sp.simplify(c6_a.subs(lambda_a, sp.pi**2 * lambda_bps) - c6_bps) == 0,
    )
    c0 = 32 * mu**2 / (coupling**2 * decay_scale**4)
    angular = 16 * sp.sqrt(2) / 15
    reduced_bound = sp.simplify(
        sp.pi
        * decay_scale
        / coupling
        * 2
        * sp.sqrt(c6_a * c0)
        * angular
    )
    direct_bound = sp.simplify(2 * lambda_a * mu * target_average)
    checks.check(
        "fresh reduced square completion collapses to the direct bound",
        sp.simplify(reduced_bound - direct_bound) == 0,
    )
    checks.check(
        "the alleged second route has the identical free-symbol surface",
        reduced_bound.free_symbols == direct_bound.free_symbols == {lambda_a, mu},
    )

    slack = sp.symbols("s", nonnegative=True)
    sector_energy = direct_bound + slack
    checks.check(
        "a fresh nonnegative slack separates a bound from attained energy",
        sp.simplify(sector_energy - direct_bound) == slack,
    )
    checks.check(
        "positive slack is an explicit nonattainment counterexample",
        sector_energy.subs(slack, 1) > direct_bound,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
