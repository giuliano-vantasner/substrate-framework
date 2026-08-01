#!/usr/bin/env python3
"""Independent manual derivative, high-precision Fourier, and TT review."""

from __future__ import annotations

import mpmath as mp
import sympy as sp

from substrate_framework.verification import CheckLedger


def manual_mu_third(theta: mp.mpf) -> mp.mpf:
    """Return mu'''(t) at omega=1/sqrt(2), derived without package APIs."""

    sine = mp.sin(theta)
    cosine = mp.cos(theta)
    denominator = 1 + sine**2
    return 32 * cosine * (
        -3 * sine / denominator**2
        + (2 * sine**2 - 1) * mp.asinh(sine) / denominator ** mp.mpf("2.5")
    )


def direct_mean(subdivisions: int) -> mp.mpf:
    points = [mp.pi * index / subdivisions for index in range(subdivisions + 1)]
    return mp.quad(lambda theta: manual_mu_third(theta) ** 2, points) / mp.pi


def main() -> int:
    ledger = CheckLedger("P042-INDEPENDENT")

    theta = sp.symbols("theta", real=True)
    profile = sp.asinh(sp.sin(theta)) ** 2
    manual_profile_third = 4 * sp.cos(theta) * (
        -3 * sp.sin(theta) / (1 + sp.sin(theta) ** 2) ** 2
        + (2 * sp.sin(theta) ** 2 - 1)
        * sp.asinh(sp.sin(theta))
        / (1 + sp.sin(theta) ** 2) ** sp.Rational(5, 2)
    )
    ledger.check(
        "manual chain-rule differentiation equals the exact third profile derivative",
        sp.trigsimp(sp.diff(profile, theta, 3) - manual_profile_third) == 0,
    )
    ledger.check(
        "manual special-frequency derivatives have exact symmetry zeros and nonzero quarter phase",
        sp.simplify(8 * manual_profile_third.subs(theta, 0)) == 0
        and sp.simplify(8 * manual_profile_third.subs(theta, sp.pi / 2)) == 0
        and sp.simplify(
            8 * manual_profile_third.subs(theta, sp.pi / 4) + sp.Rational(64, 3)
        )
        == 0,
    )

    mp.mp.dps = 60
    means = [direct_mean(subdivisions) for subdivisions in (4, 8, 16, 32)]
    ledger.check(
        "sixty-digit direct period quadrature is subdivision stable",
        max(means) - min(means) < mp.mpf("1e-45"),
    )
    mean = means[-1]
    ledger.check(
        "independent direct quadrature resolves the special mean square",
        abs(mean - mp.mpf("379.46463806874721422926815749206337776021142027526"))
        < mp.mpf("1e-45"),
    )

    def moment_dynamic(value: mp.mpf) -> mp.mpf:
        return 16 * mp.sqrt(2) * mp.asinh(mp.sin(value)) ** 2

    omega = 1 / mp.sqrt(2)
    terms: list[mp.mpf] = []
    for harmonic in range(1, 17):
        coefficient = (
            2
            / mp.pi
            * mp.quad(
                lambda value, k=harmonic: moment_dynamic(value)
                * mp.cos(2 * k * value),
                [0, mp.pi / 2, mp.pi],
            )
        )
        terms.append(
            mp.mpf("0.5") * (2 * harmonic * omega) ** 6 * coefficient**2
        )
    partials = [sum(terms[:count]) for count in (4, 8, 12, 16)]
    errors = [abs(partial - mean) for partial in partials]
    ledger.check(
        "high-precision Fourier-Parseval sums converge independently to direct quadrature",
        all(fine < coarse for coarse, fine in zip(errors, errors[1:]))
        and errors[-1] < mp.mpf("1e-12"),
    )
    fraction = terms[0] / mean
    ledger.check(
        "the first allowed two-omega harmonic is numerically dominant",
        abs(fraction - mp.mpf("0.805369871686086230317821549431"))
        < mp.mpf("1e-28")
        and terms[0] > sum(terms[1:]),
    )

    derivative, inclination = sp.symbols("d i", real=True)
    raw_second = sp.diag(sp.Function("mu")(theta), sp.Symbol("c"), sp.Symbol("c"))
    normalized = sp.simplify(raw_second - sp.eye(3) * sp.trace(raw_second) / 3)
    manual_derivative = normalized.diff(theta).subs(
        sp.diff(sp.Function("mu")(theta), theta),
        derivative,
    )
    ledger.check(
        "direct trace subtraction gives the normalized derivative and contraction",
        manual_derivative == sp.diag(2 * derivative / 3, -derivative / 3, -derivative / 3)
        and sp.simplify(
            sum(manual_derivative[row, column] ** 2 for row in range(3) for column in range(3))
            - 2 * derivative**2 / 3
        )
        == 0,
    )
    direction = sp.Matrix([sp.cos(inclination), 0, sp.sin(inclination)])
    first = sp.Matrix([sp.sin(inclination), 0, -sp.cos(inclination)])
    second = sp.Matrix([0, 1, 0])
    plus_coordinate = sp.simplify(
        (first.dot(manual_derivative * first) - second.dot(manual_derivative * second))
        / sp.sqrt(2)
    )
    cross_coordinate = sp.simplify(
        sp.sqrt(2) * first.dot(manual_derivative * second)
    )
    ledger.check(
        "direct transverse contractions give sine-squared plus and zero cross",
        sp.trigsimp(
            plus_coordinate - derivative * sp.sin(inclination) ** 2 / sp.sqrt(2)
        )
        == 0
        and cross_coordinate == 0
        and sp.simplify(direction.dot(first)) == 0
        and sp.simplify(direction.dot(second)) == 0,
    )

    coupling = sp.symbols("G", positive=True, real=True)
    normalized_power = sp.Rational(1, 5) * coupling * sp.Rational(2, 3) * derivative**2
    triple_power = sp.Rational(1, 45) * coupling * 6 * derivative**2
    ledger.check(
        "independent coefficient accounting makes normalized and triple powers identical",
        sp.simplify(normalized_power - triple_power) == 0
        and sp.simplify(normalized_power - 2 * coupling * derivative**2 / 15) == 0,
    )
    ledger.check(
        "the source's triple tensor with G over five is exactly nine times too large",
        sp.simplify(sp.Rational(1, 5) * coupling * 6 * derivative**2 - 9 * normalized_power)
        == 0,
    )
    corrected_average = mp.mpf(2) * mean / 15
    ledger.check(
        "independent mean-square evidence gives the corrected conditional average coefficient",
        abs(corrected_average - mp.mpf("50.595285075832961897235754332275117034694856036701"))
        < mp.mpf("1e-45"),
    )

    count = ledger.finish()
    print(f"P042 INDEPENDENT TIME-FOURIER REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
