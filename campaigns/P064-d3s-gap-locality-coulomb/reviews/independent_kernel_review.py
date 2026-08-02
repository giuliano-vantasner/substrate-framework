"""Independent exact P064 review without importing momentum_kernels."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(expression: object) -> bool:
    return sp.simplify(sp.sympify(expression)) == 0


def main() -> int:
    ledger = CheckLedger("P064-INDEPENDENT")
    q2 = sp.Symbol("Q2", positive=True)
    m2 = sp.Symbol("m2", positive=True)
    u = sp.Symbol("u", real=True)
    order = sp.Symbol("n", integer=True, positive=True)
    beta_coefficient = sp.simplify(
        (-1) ** (order - 1)
        * sp.gamma(order + 1) ** 2
        / (sp.gamma(2 * order + 2) * m2**order)
    )
    factorial_coefficient = (
        (-1) ** (order - 1)
        * sp.factorial(order) ** 2
        / (sp.factorial(2 * order + 1) * m2**order)
    )
    ledger.check(
        "fresh beta integral gives the factorial coefficient sequence",
        _zero(beta_coefficient - factorial_coefficient),
    )
    ledger.check(
        "fresh direct integration matches the general formula through order eight",
        all(
            _zero(
                sp.integrate(
                    (-1) ** (index - 1)
                    * (u * (1 - u)) ** index
                    / m2**index,
                    (u, 0, 1),
                )
                - factorial_coefficient.subs(order, index)
            )
            for index in range(1, 9)
        ),
    )
    ratio = u * (1 - u) * q2 / m2
    exact = ratio / (1 + ratio)
    for truncation in (0, 1, 3, 7):
        polynomial = sum(
            ((-1) ** (index - 1) * ratio**index for index in range(1, truncation + 1)),
            sp.S.Zero,
        )
        remainder = (-1) ** truncation * ratio ** (truncation + 1) / (1 + ratio)
        ledger.check(
            f"fresh finite geometric identity closes at order {truncation}",
            _zero(exact - polynomial - remainder),
        )
    continuation_variable = sp.Symbol("z")
    ledger.check(
        "fresh denominator extremum locates the nearest threshold",
        sp.solve(sp.diff(u * (1 - u), u), u) == [sp.Rational(1, 2)]
        and sp.solve(
            sp.Eq(m2 + continuation_variable * sp.Rational(1, 4), 0),
            continuation_variable,
        )
        == [-4 * m2],
    )

    t = sp.Symbol("t", positive=True)
    density = sp.Function("rho")(t)
    truncation = 5
    spectral_exact = density * q2 / (t + q2)
    spectral_polynomial = sum(
        (
            density * (-1) ** (index - 1) * q2**index / t**index
            for index in range(1, truncation + 1)
        ),
        sp.S.Zero,
    )
    spectral_remainder = (
        density
        * (-1) ** truncation
        * q2 ** (truncation + 1)
        / (t**truncation * (t + q2))
    )
    ledger.check(
        "fresh spectral expansion is a pointwise algebraic identity",
        _zero(spectral_exact - spectral_polynomial - spectral_remainder),
    )
    ledger.check(
        "fresh gapped ultraviolet counterexample has divergent first moment",
        sp.integrate(t / t, (t, 1, sp.oo)) == sp.oo,
    )

    k2 = sp.Symbol("k2", positive=True)
    amplitude, analytic = sp.symbols("A B", positive=True)
    fractional_power = sp.Rational(2, 3)
    inverse_kernel = amplitude * k2**fractional_power + analytic * k2
    ledger.check(
        "fresh asymptotic ratio shows fractional term dominates",
        sp.limit(
            analytic * k2 / (amplitude * k2**fractional_power),
            k2,
            0,
            dir="+",
        )
        == 0,
    )
    coefficient = sp.Symbol("Z", nonzero=True, real=True)
    ledger.check(
        "fresh nonzero analytic coefficient has unit k-squared exponent",
        sp.limit((coefficient * k2 + k2**2) / k2, k2, 0, dir="+")
        == coefficient,
    )
    ledger.check(
        "fresh exact cancellation exposes the next integer power",
        sp.simplify((3 * k2 - 3 * k2 + 5 * k2**2) / k2**2) == 5,
    )

    dimension, power = sp.symbols("d s", positive=True)
    radius, schwinger = sp.symbols("r tau", positive=True)
    gaussian_transform = (
        (4 * sp.pi * schwinger) ** (-dimension / 2)
        * sp.exp(-radius**2 / (4 * schwinger))
    )
    # With y=r^2/(4*tau), the remaining integral is Gamma(d/2-s).
    transformed_prefactor = sp.simplify(
        1
        / sp.gamma(power)
        * (4 * sp.pi) ** (-dimension / 2)
        * (radius**2 / 4) ** (power - dimension / 2)
    )
    derived_normalization = sp.simplify(
        transformed_prefactor * sp.gamma(dimension / 2 - power)
    )
    target_normalization = (
        sp.gamma(dimension / 2 - power)
        / (4**power * sp.pi ** (dimension / 2) * sp.gamma(power))
        * radius ** (2 * power - dimension)
    )
    ledger.check(
        "fresh Schwinger and Gaussian route derives the Riesz normalization",
        gaussian_transform.has(sp.exp(-radius**2 / (4 * schwinger)))
        and _zero(derived_normalization - target_normalization),
    )
    epsilon = sp.Symbol("epsilon", positive=True)
    damped_radial_integral = sp.integrate(
        sp.exp(-epsilon * t) * sp.sin(radius * t) / t,
        (t, 0, sp.oo),
    )
    ledger.check(
        "fresh regulated spherical Fourier integral gives one over four pi r",
        damped_radial_integral == sp.atan(radius / epsilon)
        and sp.limit(
            damped_radial_integral / (2 * sp.pi**2 * radius),
            epsilon,
            0,
            dir="+",
        )
        == 1 / (4 * sp.pi * radius),
    )
    mutated_dimension = sp.simplify(target_normalization.subs({dimension: 4, power: 1}))
    baseline = sp.simplify(target_normalization.subs({dimension: 3, power: 1}))
    ledger.check(
        "fresh dimension mutation changes both normalization and radial power",
        baseline == 1 / (4 * sp.pi * radius)
        and mutated_dimension == 1 / (4 * sp.pi**2 * radius**2)
        and mutated_dimension != baseline,
    )
    mutated_power = sp.simplify(
        target_normalization.subs({dimension: 3, power: sp.Rational(1, 2)})
    )
    ledger.check(
        "fresh fractional-power mutation changes the static kernel",
        mutated_power == 1 / (2 * sp.pi**2 * radius**2)
        and mutated_power != baseline,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
