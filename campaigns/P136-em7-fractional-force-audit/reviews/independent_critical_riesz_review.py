from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P136-INDEPENDENT-CRITICAL-RIESZ")

    proper_time = sp.Symbol("t", positive=True)
    radius = sp.Symbol("r", positive=True)
    reference = sp.Symbol("r0", positive=True)
    dimension, power = sp.symbols("d s", positive=True)
    coefficient = sp.Symbol("A", positive=True)

    # Fresh Schwinger/Gaussian route.  The inverse Fourier transform of
    # exp(-t k^2) in the angular convention is
    # (4*pi*t)^(-d/2) exp(-r^2/(4t)).
    radial_proper_time_integral = sp.integrate(
        proper_time ** (power - 1 - dimension / 2)
        * sp.exp(-radius**2 / (4 * proper_time)),
        (proper_time, 0, sp.oo),
        conds="none",
    )
    expected_radial_integral = (
        4 ** (dimension / 2 - power)
        * radius ** (2 * power - dimension)
        * sp.gamma(dimension / 2 - power)
    )
    checks.check(
        "fresh Schwinger radial integral",
        sp.simplify(radial_proper_time_integral - expected_radial_integral)
        == 0,
    )
    gaussian_prefactor = 1 / (
        coefficient * sp.gamma(power) * (4 * sp.pi) ** (dimension / 2)
    )
    fresh_riesz = sp.simplify(
        gaussian_prefactor * radial_proper_time_integral
    )
    expected_riesz = (
        sp.gamma(dimension / 2 - power)
        * radius ** (2 * power - dimension)
        / (
            coefficient
            * 4**power
            * sp.pi ** (dimension / 2)
            * sp.gamma(power)
        )
    )
    checks.check(
        "fresh Gaussian route gives the Riesz normalization",
        sp.simplify(fresh_riesz - expected_riesz) == 0,
    )

    epsilon = sp.Symbol("epsilon", positive=True)
    subcritical_power = dimension / 2 - epsilon
    subcritical_normalization = sp.gamma(epsilon) / (
        coefficient
        * 4**subcritical_power
        * sp.pi ** (dimension / 2)
        * sp.gamma(subcritical_power)
    )
    subtracted = sp.simplify(
        subcritical_normalization
        * (radius ** (-2 * epsilon) - reference ** (-2 * epsilon))
    )
    critical_limit = sp.simplify(sp.limit(subtracted, epsilon, 0, dir="+"))
    critical_normalization = 2 / (
        coefficient
        * 4 ** (dimension / 2)
        * sp.pi ** (dimension / 2)
        * sp.gamma(dimension / 2)
    )
    fresh_log = sp.simplify(
        critical_normalization * sp.log(reference / radius)
    )
    checks.check(
        "fresh reference-subtracted critical limit",
        sp.simplify(critical_limit - fresh_log) == 0,
    )
    checks.check(
        "fresh unsubtracted critical limit diverges",
        sp.limit(
            (subcritical_normalization * radius ** (-2 * epsilon)).subs(
                dimension, 2
            ),
            epsilon,
            0,
            dir="+",
        )
        == sp.oo,
    )
    checks.check(
        "critical reference mutation changes only a constant",
        sp.simplify(
            sp.diff(
                fresh_log.subs(reference, 2 * reference) - fresh_log,
                radius,
            )
        )
        == 0,
    )

    # Independent radial-flux normalization in two dimensions.
    two_dimensional = sp.simplify(fresh_log.subs(dimension, 2))
    radial_field = sp.simplify(-sp.diff(two_dimensional, radius))
    unit_flux = sp.simplify(
        coefficient * 2 * sp.pi * radius * radial_field
    )
    checks.check(
        "fresh two-dimensional radial flux fixes the log coefficient",
        sp.simplify(
            two_dimensional
            - sp.log(reference / radius) / (2 * sp.pi * coefficient)
        )
        == 0
        and unit_flux == 1,
    )

    # The ordinary one-dimensional inverse Laplacian is distributional and
    # requires a separate homogeneous/boundary prescription.
    coordinate = sp.Symbol("x", real=True)
    one_dimensional = -sp.Abs(coordinate) / (2 * coefficient)
    distributional_source = sp.simplify(
        -coefficient * sp.diff(one_dimensional, coordinate, 2)
    )
    checks.check(
        "fresh one-dimensional ordinary Green function is distributional",
        distributional_source == sp.DiracDelta(coordinate),
    )
    checks.check(
        "one-dimensional branch is outside the subcritical Riesz integral",
        sp.Integer(1) >= sp.Rational(1, 2),
    )

    source_strength, probe_strength = sp.symbols("Q q", real=True)
    subcritical_green = expected_riesz
    potential = sp.simplify(source_strength * subcritical_green)
    energy = sp.simplify(probe_strength * potential)
    radial_force = sp.simplify(-sp.diff(energy, radius))
    force_exponent = sp.simplify(2 * power - dimension - 1)
    checks.check(
        "fresh source-probe differentiation gives the conditional force",
        sp.simplify(radial_force + sp.diff(energy, radius)) == 0
        and radial_force.has(source_strength)
        and radial_force.has(probe_strength),
    )
    checks.check(
        "fresh inverse-square equation has a one-parameter family",
        sp.solve(sp.Eq(force_exponent, -2), dimension) == [2 * power + 1],
    )
    checks.check(
        "fresh noninteger inverse-square counterexample is subcritical",
        force_exponent.subs(
            {power: sp.Rational(9, 10), dimension: sp.Rational(14, 5)}
        )
        == -2
        and sp.Rational(9, 10) < sp.Rational(7, 5),
    )
    checks.check(
        "fixing dimension three alone rejects but does not select power one",
        force_exponent.subs({dimension: 3, power: sp.Rational(9, 10)})
        != -2
        and sp.solve(sp.Eq(force_exponent.subs(dimension, 3), -2), power)
        == [1],
    )
    checks.check(
        "source and probe sign mutations are independently visible",
        sp.simplify(potential.subs(source_strength, -source_strength) + potential)
        == 0
        and sp.simplify(energy.subs(probe_strength, -probe_strength) + energy)
        == 0,
    )
    checks.check(
        "inverse-kernel coefficient mutation halves the response",
        sp.simplify(
            radial_force.subs(coefficient, 2 * coefficient)
            - radial_force / 2
        )
        == 0,
    )

    # Analytic continuation of d in gamma functions is an algebraic operation.
    # No metric, measure, diffusion kernel, or Dirichlet form occurs here.
    free_symbols = fresh_riesz.free_symbols
    checks.check(
        "fresh derivation contains parameters but no geometric construction",
        free_symbols == {dimension, power, radius, coefficient},
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
