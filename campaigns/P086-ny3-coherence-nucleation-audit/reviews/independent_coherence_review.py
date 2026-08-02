"""Independent exact rederivation for P086 without canonical gate imports."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P086-INDEPENDENT")
    count = sp.Symbol("N", integer=True, positive=True)
    intensity, coherence = sp.symbols("I V", positive=True)

    diagonal_terms = count
    ordered_distinct_pairs = count * (count - 1)
    expected = sp.expand(
        intensity * (diagonal_terms + ordered_distinct_pairs * coherence)
    )
    checks.check(
        "fresh diagonal and ordered-pair count gives the iid expectation",
        sp.expand(
            expected
            - intensity * (count**2 * coherence - count * coherence + count)
        )
        == 0,
    )
    checks.check(
        "fresh endpoint evaluation separates random expectation and alignment",
        expected.subs(coherence, 0) == count * intensity
        and expected.subs(coherence, 1) == count**2 * intensity,
    )

    phase, variance = sp.symbols("phi sigma_squared", real=True, positive=True)
    gaussian_density = sp.exp(-phase**2 / (2 * variance)) / sp.sqrt(
        2 * sp.pi * variance
    )
    mean_phasor = sp.integrate(
        sp.exp(sp.I * phase) * gaussian_density,
        (phase, -sp.oo, sp.oo),
    )
    checks.check(
        "fresh Gaussian characteristic integral fixes the pair coherence",
        sp.simplify(mean_phasor - sp.exp(-variance / 2)) == 0
        and sp.simplify(mean_phasor * sp.conjugate(mean_phasor) - sp.exp(-variance))
        == 0,
    )
    checks.check(
        "a fixed-total normalization changes the fully aligned scaling",
        sp.simplify(expected.subs(intensity, intensity / count).subs(coherence, 1))
        == count * intensity,
    )
    checks.check(
        "a deterministic antiphase pair lies outside the iid nonnegative-pair family",
        sp.simplify((1 + sp.exp(sp.I * sp.pi)) * (1 + sp.exp(-sp.I * sp.pi)))
        == 0,
    )

    population = sp.Symbol("n", positive=True)
    unit, barrier = sp.symbols("theta E", positive=True)
    visibility = sp.Symbol("V_positive", positive=True)
    scale = sp.expand(unit * population * (1 + (population - 1) * visibility))
    roots = sp.solve(sp.Eq(scale, barrier), population)
    positive_root = (
        sp.sqrt(unit) * (visibility - 1)
        + sp.sqrt(4 * barrier * visibility + unit * (visibility - 1) ** 2)
    ) / (2 * visibility * sp.sqrt(unit))
    checks.check(
        "fresh quadratic solution contains the advertised positive root",
        any(sp.simplify(root - positive_root) == 0 for root in roots),
    )
    checks.check(
        "fresh substitution proves the root rather than copying its form",
        sp.simplify(scale.subs(population, positive_root) - barrier) == 0,
    )
    ratio = barrier / unit
    checks.check(
        "endpoint comparison changes sign at a unit barrier ratio",
        sp.sqrt(4) < 4
        and sp.sqrt(sp.Rational(1, 4)) > sp.Rational(1, 4)
        and sp.sqrt(1) == 1
        and sp.simplify(
            sp.sqrt(ratio)
            - ratio
            - sp.sqrt(ratio) * (1 - sp.sqrt(ratio))
        )
        == 0,
    )
    derivative = sp.factor(sp.diff(scale, visibility))
    checks.check(
        "fresh coherence derivative vanishes for one source",
        derivative == unit * population * (population - 1)
        and derivative.subs(population, 1) == 0,
    )

    response = sp.exp(-barrier / scale)
    checks.check(
        "fresh activated-factor derivatives keep barrier and scale roles separate",
        sp.diff(response, barrier).subs(population, 2).is_negative
        and sp.simplify(sp.diff(response, visibility).subs(population, 1)) == 0
        and sp.diff(response, visibility).subs(population, 2).is_positive,
    )
    rate_prefactor = sp.Symbol("omega", positive=True)
    rate = rate_prefactor * response
    checks.check(
        "a separate prefactor is required to turn the factor into a rate",
        rate_prefactor not in response.free_symbols
        and rate_prefactor in rate.free_symbols
        and sp.simplify(rate / rate_prefactor - response) == 0,
    )

    radius, tension, pressure, core = sp.symbols("R T P C", positive=True)
    landscape = 2 * sp.pi * radius * tension - sp.pi * radius**2 * pressure + core
    stationary = sp.solve(sp.Eq(sp.diff(landscape, radius), 0), radius)[0]
    height = sp.simplify(landscape.subs(radius, stationary) - landscape.subs(radius, 0))
    checks.check(
        "fresh capillary derivation fixes only a conditional relative barrier",
        stationary == tension / pressure
        and height == sp.pi * tension**2 / pressure
        and core not in height.free_symbols,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
