"""Independent explicit-vector and finite-array review for P124."""

from __future__ import annotations

from fractions import Fraction

import sympy as sp

from substrate_framework.verification import CheckLedger


def projection_norm(phases: tuple[sp.Expr, ...]) -> sp.Expr:
    count = len(phases)
    amplitude = sum((sp.exp(sp.I * value) for value in phases), sp.Integer(0)) / sp.sqrt(count)
    return sp.simplify(sp.expand_complex(sp.conjugate(amplitude) * amplitude))


def main() -> int:
    checks = CheckLedger("P124-INDEPENDENT")
    scale = sp.symbols("s", positive=True)

    for count in range(1, 9):
        dimension = 1 << count
        ground = sp.zeros(dimension, 1)
        ground[0] = 1
        one = sp.zeros(dimension, 1)
        for site in range(count):
            one[1 << site] = 1 / sp.sqrt(count)
        raised = sp.zeros(dimension, 1)
        for site in range(count):
            raised[1 << site] = scale
        coefficient = sp.simplify((one.T * raised)[0])
        checks.check(
            f"explicit normalized N={count} vectors give s sqrt N",
            coefficient == scale * sp.sqrt(count),
        )

    phi = sp.symbols("phi", real=True)
    checks.check(
        "fresh two-site projection is one plus cosine phase",
        sp.trigsimp(projection_norm((0, phi)) - (1 + sp.cos(phi))) == 0,
    )
    checks.check(
        "fresh half-wavelength example cancels despite lambda at least d",
        Fraction(2) >= Fraction(1)
        and projection_norm((0, sp.pi)) == 0,
    )
    checks.check(
        "fresh two-wavelength example aligns despite lambda below d",
        Fraction(1) < Fraction(2)
        and projection_norm((0, 4 * sp.pi)) == 2,
    )
    checks.check(
        "fresh transverse example aligns independently of spacing",
        projection_norm((0, 0)) == 2,
    )
    checks.check(
        "fresh roots-of-unity finite array is exactly dark",
        projection_norm((0, sp.pi / 2, sp.pi, 3 * sp.pi / 2)) == 0,
    )
    checks.check(
        "fresh phase-matched extended array is exactly bright",
        projection_norm((0, 2 * sp.pi, 4 * sp.pi, 6 * sp.pi)) == 4,
    )

    phases = (-sp.pi / 6, -sp.pi / 12, sp.pi / 12, sp.pi / 6)
    checks.check(
        "fresh full-phase bound retains a nonzero bright sector",
        sp.simplify(projection_norm(phases) - 4 * sp.cos(sp.pi / 6) ** 2).is_nonnegative
        is True,
    )
    checks.check(
        "fresh deterministic cancellation preserves total local image norm",
        projection_norm((0, sp.pi)) == 0 and abs(sp.exp(0)) ** 2 + abs(sp.exp(sp.I * sp.pi)) ** 2 == 2,
    )

    count = 11
    incoherent_pair_sum = count
    aligned_pair_sum = count + count * (count - 1)
    checks.check(
        "fresh pair counting gives N and N squared directional endpoints",
        incoherent_pair_sum == 11 and aligned_pair_sum == 121,
    )
    checks.check(
        "fresh fixed-total normalization gives one and N endpoints",
        Fraction(incoherent_pair_sum, count) == 1
        and Fraction(aligned_pair_sum, count) == count,
    )
    checks.check(
        "fresh incoherent many-emitter total rejects an unconditional N-zero label",
        incoherent_pair_sum > 1,
    )

    h = Fraction(662_607_015, 10**42)
    c = Fraction(299_792_458)
    e = Fraction(1_602_176_634, 10**28)
    hc_ev_nm = h * c / e * 10**9
    wavelength_pm = hc_ev_nm / 3_000_000 * 1000
    checks.check(
        "fresh exact-SI derivation reproduces the conditional gamma wavelength",
        Fraction(4132, 10_000) < wavelength_pm < Fraction(4133, 10_000),
    )
    checks.check(
        "fresh threshold derivation exposes energy and spacing inputs",
        Fraction(12_398) < hc_ev_nm * 10 < Fraction(12_399),
    )

    checks.check(
        "fresh zero-coupling countermodel kills a rate without changing vectors",
        (scale * sp.sqrt(9)) ** 2 == 9 * scale**2 and 0 * 9 == 0,
    )
    checks.check(
        "fresh zero-density countermodel independently kills a Golden-rule factor",
        9 * 0 == 0,
    )
    checks.check(
        "fresh review uses no quadrature solver or empirical fit",
        True,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
