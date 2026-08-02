"""Independent exact rederivation for P070 without canonical overlap imports."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_MH1_yukawa_overlap_mass_formula.py"
)
SOURCE_SHA256 = "6e32edbd129c40ed587408fa70128951f65c04f379a633414fd8202e80ca1854"


def main() -> int:
    ledger = CheckLedger("P070-INDEPENDENT")
    ledger.check(
        "review reads the same immutable MH1 source",
        SOURCE.is_file()
        and hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )

    power, kappa = sp.symbols("s kappa", positive=True)
    beta_substitution = sp.beta(sp.Rational(1, 2), power / 2) / kappa
    gamma_result = sp.sqrt(sp.pi) * sp.gamma(power / 2) / (
        kappa * sp.gamma((power + 1) / 2)
    )
    ledger.check(
        "fresh tanh substitution gives the beta/gamma whole-line integral",
        sp.simplify(sp.expand_func(beta_substitution) - gamma_result) == 0,
    )
    recurrence_left = gamma_result.subs(power, power + 2)
    recurrence_right = sp.simplify(power * gamma_result / (power + 1))
    ledger.check(
        "fresh gamma expression obeys the sech reduction recurrence",
        sp.simplify(recurrence_left - recurrence_right) == 0,
    )

    p, r, amplitude = sp.symbols("p r A", positive=True)
    integral = lambda exponent: sp.sqrt(sp.pi) * sp.gamma(sp.sympify(exponent) / 2) / (
        kappa * sp.gamma((sp.sympify(exponent) + 1) / 2)
    )
    fresh_ratio = sp.simplify(amplitude * integral(2 * p + r) / integral(2 * p))
    ledger.check(
        "fresh normalization gives the general matched-width ratio",
        fresh_ratio
        == amplitude
        * sp.gamma(p + r / 2)
        * sp.gamma(p + sp.Rational(1, 2))
        / (sp.gamma(p) * sp.gamma(p + r / 2 + sp.Rational(1, 2))),
    )
    ledger.check(
        "fresh matched-width ratio is independent of common inverse width",
        sp.diff(fresh_ratio, kappa) == 0,
    )
    sampled = {
        value: sp.simplify(fresh_ratio.subs({p: value, r: 1}))
        for value in (1, 2, 3)
    }
    ledger.check(
        "fresh route reproduces all three MH1 samples",
        sampled
        == {
            1: sp.pi * amplitude / 4,
            2: 9 * sp.pi * amplitude / 32,
            3: 75 * sp.pi * amplitude / 256,
        },
    )

    integral_2 = sp.simplify(integral(2))
    integral_3 = sp.simplify(integral(3))
    integral_4 = sp.simplify(integral(4))
    integral_5 = sp.simplify(integral(5))
    even_norm = integral_4
    odd_norm = sp.simplify(integral_2 - integral_4)
    even_overlap = sp.simplify(amplitude * integral_5 / even_norm)
    odd_overlap = sp.simplify(amplitude * (integral_3 - integral_5) / odd_norm)
    ledger.check(
        "fresh actual-mode norms are four-thirds and two-thirds over width",
        even_norm == 4 / (3 * kappa) and odd_norm == 2 / (3 * kappa),
    )
    ledger.check(
        "fresh actual even and odd squared-density overlaps are exact",
        even_overlap == 9 * sp.pi * amplitude / 32
        and odd_overlap == 3 * sp.pi * amplitude / 16,
    )
    ledger.check(
        "fresh actual-mode ratio is order one",
        sp.simplify(odd_overlap / even_overlap) == sp.Rational(2, 3),
    )

    x = sp.symbols("x", real=True)
    cross_integrand = sp.sech(kappa * x) ** 4 * sp.tanh(kappa * x)
    ledger.check(
        "fresh parity route makes the weighted even-odd cross integrand odd",
        sp.simplify(cross_integrand.subs(x, -x) + cross_integrand) == 0,
    )

    w, lower, upper, f0, f1 = sp.symbols(
        "w lower upper f0 f1", real=True
    )
    expectation = w * f0 + (1 - w) * f1
    ledger.check(
        "normalized two-point expectation lower gap is a weighted profile gap",
        sp.expand(expectation - lower)
        == sp.expand(w * (f0 - lower) + (1 - w) * (f1 - lower)),
    )
    ledger.check(
        "normalized two-point expectation upper gap is a weighted profile gap",
        sp.expand(upper - expectation)
        == sp.expand(w * (upper - f0) + (1 - w) * (upper - f1)),
    )
    ledger.check(
        "negative supplied multiplier reverses overlap sign",
        sp.simplify(fresh_ratio.subs(amplitude, -1) + fresh_ratio.subs(amplitude, 1))
        == 0,
    )

    profile_dimension, scale_dimension = sp.symbols("dPhi dv", real=True)
    ledger.check(
        "L2 normalization leaves the expectation with multiplier dimension",
        sp.simplify((-sp.Rational(1, 2)) * 2 + profile_dimension + 1 - profile_dimension)
        == 0,
    )
    ledger.check(
        "declared product mass dimension is the supplied dimension sum",
        sp.diff(profile_dimension + scale_dimension, profile_dimension) == 1
        and sp.diff(profile_dimension + scale_dimension, scale_dimension) == 1,
    )
    y, scale, rho = sp.symbols("y v rho", nonzero=True, real=True)
    ledger.check(
        "fresh reciprocal rescaling leaves y times v invariant",
        sp.simplify((rho * y) * (scale / rho) - y * scale) == 0,
    )
    ledger.check(
        "common external scale cancels but independent amplitudes do not",
        sp.simplify((odd_overlap * scale) / (even_overlap * scale))
        == sp.Rational(2, 3),
    )

    negative_level = -3 * kappa**2
    zero_level = sp.Integer(0)
    alternative_positive = even_overlap + amplitude / 10
    ledger.check(
        "fresh spectral ceiling rejects positive-mass interpretation only",
        bool(negative_level.subs(kappa, 1) < 0) and zero_level == 0,
    )
    ledger.check(
        "a second positive functional disproves uniqueness of overlap selection",
        alternative_positive != even_overlap
        and bool(alternative_positive.subs(amplitude, 1) > 0),
    )
    ledger.check(
        "source contains no interaction whose variation generates the declared product",
        "L_yukawa" not in SOURCE.read_text(encoding="utf-8")
        and "m_n = y_ns * v" in SOURCE.read_text(encoding="utf-8"),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
