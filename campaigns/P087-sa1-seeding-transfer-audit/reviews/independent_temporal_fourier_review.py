"""Independent P087 derivation without canonical sine-Gordon imports."""

from __future__ import annotations

import mpmath
import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P087-INDEPENDENT")
    phase, amplitude = sp.symbols("y a", real=True, positive=True)
    trace = 4 * sp.atan(amplitude * sp.sin(phase))
    checks.check(
        "fresh trace has exact odd parity",
        sp.simplify(trace.subs(phase, -phase) + trace) == 0,
    )
    checks.check(
        "fresh trace has exact half-wave antisymmetry",
        sp.simplify(trace.subs(phase, phase + sp.pi) + trace) == 0,
    )

    index = sp.Symbol("n", integer=True, positive=True)
    cosine_integrand = trace * sp.cos(index * phase)
    even_sine_integrand = trace * sp.sin(2 * index * phase)
    checks.check(
        "fresh paired integrands remove cosine and even-sine modes",
        sp.simplify(
            cosine_integrand.subs(phase, -phase) + cosine_integrand
        )
        == 0
        and sp.simplify(
            even_sine_integrand.subs(phase, phase + sp.pi)
            + even_sine_integrand
        )
        == 0,
    )

    tangent = sp.Symbol("u", nonnegative=True)
    quarter = sp.integrate(
        1 / (1 + (1 + amplitude**2) * tangent**2),
        (tangent, 0, sp.oo),
    )
    reciprocal_integral = 4 * quarter
    checks.check(
        "fresh tangent substitution gives the full reciprocal integral",
        quarter == sp.pi / (2 * sp.sqrt(1 + amplitude**2))
        and reciprocal_integral == 2 * sp.pi / sp.sqrt(1 + amplitude**2),
    )

    cosine_squared_integral = sp.simplify(
        ((1 + amplitude**2) * reciprocal_integral - 2 * sp.pi)
        / amplitude**2
    )
    by_parts = sp.simplify(
        4 * amplitude * cosine_squared_integral / sp.pi
    )
    rationalized = 8 * amplitude / (sp.sqrt(1 + amplitude**2) + 1)
    checks.check(
        "fresh integration by parts derives the nonlinear coefficient",
        sp.simplify(
            by_parts - 8 * (sp.sqrt(1 + amplitude**2) - 1) / amplitude
        )
        == 0
        and sp.simplify(by_parts - rationalized) == 0,
    )

    derivative_route = 8 / amplitude**2 * (
        1 - 1 / sp.sqrt(1 + amplitude**2)
    )
    checks.check(
        "fresh parameter derivative agrees with the by-parts result",
        sp.simplify(sp.diff(by_parts, amplitude) - derivative_route) == 0
        and sp.limit(by_parts, amplitude, 0, dir="+") == 0,
    )

    mpmath.mp.dps = 50
    numeric_cases = (mpmath.mpf("0.25"), mpmath.mpf("1"), mpmath.mpf("2"))
    numeric_errors = []
    for value in numeric_cases:
        integral = mpmath.quad(
            lambda y: 4 * mpmath.atan(value * mpmath.sin(y)) * mpmath.sin(y),
            [0, 2 * mpmath.pi],
        ) / mpmath.pi
        closed = 8 * value / (mpmath.sqrt(1 + value**2) + 1)
        numeric_errors.append(abs(integral - closed))
    checks.check(
        "independent high-precision quadrature matches three amplitudes",
        max(numeric_errors) < mpmath.mpf("1e-45"),
    )

    omega = sp.Symbol("omega", positive=True)
    eta = sp.sqrt(1 - omega**2)
    core = sp.simplify(rationalized.subs(amplitude, eta / omega))
    checks.check(
        "fresh on-shell core substitution gives 8*eta/(1+omega)",
        sp.simplify(core - 8 * eta / (1 + omega)) == 0,
    )
    leading = 4 * eta / omega
    checks.check(
        "fresh comparison confines the source coefficient to the small-amplitude limit",
        sp.simplify(core.subs(omega, sp.Rational(3, 5)) - 4) == 0
        and sp.simplify(leading.subs(omega, sp.Rational(3, 5)) - sp.Rational(16, 3))
        == 0
        and sp.limit(core / leading, omega, 1, dir="-") == 1,
    )

    observed, center, width, scale = sp.symbols(
        "Omega omega_b tau A", positive=True
    )
    gaussian_pair = scale * (
        sp.exp(-(observed - center) ** 2 * width**2)
        + sp.exp(-(observed + center) ** 2 * width**2)
    )
    checks.check(
        "fresh finite-width evaluation refutes an exact Gaussian DC null",
        gaussian_pair.subs(observed, 0)
        == 2 * scale * sp.exp(-center**2 * width**2)
        and gaussian_pair.subs(observed, 0).is_positive,
    )
    checks.check(
        "fresh third-harmonic probe distinguishes a pair from an odd comb",
        sp.limit(gaussian_pair.subs(observed, center), width, sp.oo) == scale
        and sp.limit(gaussian_pair.subs(observed, 3 * center), width, sp.oo) == 0,
    )

    spectrum_scale, overlap, energy = sp.symbols("c O E", positive=True)
    normalized_coordinate = sp.simplify(
        spectrum_scale * scale * overlap / energy / spectrum_scale
    )
    checks.check(
        "fresh scaling audit exposes nonidentifiable population normalization",
        spectrum_scale not in normalized_coordinate.free_symbols
        and sp.diff(normalized_coordinate, scale) == overlap / energy,
    )

    drive, cutoff = sp.symbols("w Omega_0", positive=True)
    alternatives = (
        sp.I * drive,
        drive**2 / (cutoff**2 + drive**2),
        1 - sp.exp(-drive**2 / cutoff**2),
    )
    checks.check(
        "fresh counterfamily proves zero DC is weaker than differentiation",
        all(candidate.subs(drive, 0) == 0 for candidate in alternatives)
        and len({sp.srepr(candidate) for candidate in alternatives}) == 3,
    )
    checks.check(
        "fresh phase-origin shift rotates sine into cosine",
        sp.expand_trig(sp.sin(phase - sp.pi / 2)) == -sp.cos(phase),
    )

    input_dimension, response_dimension, frequency_dimension, energy_dimension = (
        sp.symbols("d_S d_chi d_omega d_E")
    )
    count_dimension = sp.simplify(
        input_dimension
        + response_dimension
        + frequency_dimension
        - energy_dimension
    )
    checks.check(
        "fresh dimensional ledger requires an undeclared closure equation",
        count_dimension != 0
        and sp.solve(sp.Eq(count_dimension, 0), response_dimension)
        == [energy_dimension - frequency_dimension - input_dimension],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
