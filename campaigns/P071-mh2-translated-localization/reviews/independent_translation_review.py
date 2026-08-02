"""Independent derivation of P071 without importing its canonical API."""

from __future__ import annotations

import numpy as np
import sympy as sp
from scipy.integrate import quad

from substrate_framework.verification import CheckLedger


def stable_sech(value: float) -> float:
    tail = np.exp(-abs(value))
    return float(2.0 * tail / (1.0 + tail * tail))


def beta_substitution_convolution(alpha: sp.Expr, beta: sp.Expr, offset: sp.Expr) -> sp.Expr:
    """Fresh ``t=exp(2z)`` derivation of the translated convolution."""

    a = sp.Abs(offset)
    half_sum = (alpha + beta) / 2
    if a.is_zero is True:
        return sp.sqrt(sp.pi) * sp.gamma(half_sum) / sp.gamma(
            half_sum + sp.Rational(1, 2)
        )
    return (
        2 ** (alpha + beta - 1)
        * sp.exp(-alpha * a)
        * sp.beta(half_sum, half_sum)
        * sp.hyper(
            (alpha, half_sum),
            (2 * half_sum,),
            1 - sp.exp(-2 * a),
        )
    )


def exact_poschl_parameters(depth: sp.Expr, width: sp.Expr) -> tuple[sp.Expr, ...]:
    index = (sp.sqrt(1 + 4 * depth * width**2) - 1) / 2
    eigenvalue = -index**2 / width**2
    normalization = sp.sqrt(
        sp.gamma(index + sp.Rational(1, 2))
        / (width * sp.sqrt(sp.pi) * sp.gamma(index))
    )
    return index, eigenvalue, normalization, 2 * index / width


def source_exact_overlaps() -> np.ndarray:
    kappa = float(np.sqrt(0.5 - 0.45**2))
    amplitude = 2.0 * np.sqrt(6.0) * kappa
    index, _eigenvalue, normalization, _tail = exact_poschl_parameters(
        sp.Integer(12), sp.Rational(7, 10)
    )
    exponent = float(index)
    norm = float(normalization)

    def one(center: float) -> float:
        value, error = quad(
            lambda x: norm**2
            * stable_sech((x - center) / 0.7) ** (2.0 * exponent)
            * amplitude
            * stable_sech(kappa * x),
            -60.0,
            60.0,
            epsabs=1.0e-13,
            epsrel=1.0e-12,
            limit=300,
        )
        if error > 1.0e-10:
            raise RuntimeError(f"independent overlap error {error}")
        return float(value)

    return np.asarray([one(4.0 * rung) for rung in range(6)])


def main() -> int:
    ledger = CheckLedger("P071-INDEPENDENT")

    t, a = sp.symbols("t a", positive=True)
    z = sp.log(t) / 2
    transformed = sp.simplify(
        (
            sp.sech(z - a) ** 2
            * sp.sech(z)
            / (2 * t)
        ).rewrite(sp.exp)
    )
    expected_transform = 4 * sp.exp(-2 * a) * sp.sqrt(t) / (
        (1 + t) * (1 + sp.exp(-2 * a) * t) ** 2
    )
    ledger.check(
        "independent exponential substitution integrand",
        sp.simplify(transformed - expected_transform) == 0,
    )

    for alpha, beta, offset in ((2, 1, 1), (1, 2, 2), (2, 2, 3)):
        derived = float(
            sp.N(
                beta_substitution_convolution(
                    sp.Integer(alpha), sp.Integer(beta), sp.Integer(offset)
                ),
                30,
            )
        )
        direct, error = quad(
            lambda value: stable_sech(value - offset) ** alpha
            * stable_sech(value) ** beta,
            -50.0,
            50.0,
            epsabs=1.0e-13,
            epsrel=1.0e-12,
            limit=300,
        )
        ledger.check(f"independent convolution {alpha},{beta} status", error < 1.0e-10)
        ledger.check(
            f"independent convolution {alpha},{beta} value",
            abs(direct - derived) < 2.0e-11,
        )

    zero = beta_substitution_convolution(sp.Integer(4), sp.Integer(1), sp.Integer(0))
    ledger.check("zero-shift gamma endpoint", sp.simplify(zero - 3 * sp.pi / 8) == 0)
    ledger.check(
        "independent reflection",
        beta_substitution_convolution(sp.Integer(3), sp.Integer(2), sp.Integer(-2))
        == beta_substitution_convolution(sp.Integer(3), sp.Integer(2), sp.Integer(2)),
    )

    profile_slow_scaled = []
    for offset in (8, 12):
        raw = beta_substitution_convolution(sp.Integer(2), sp.Integer(1), sp.Integer(offset))
        normalized = raw / 2
        profile_slow_scaled.append(float(sp.N(normalized * sp.exp(offset), 30)))
    ledger.check(
        "profile-slow coefficient approaches pi",
        abs(profile_slow_scaled[1] - float(sp.pi))
        < abs(profile_slow_scaled[0] - float(sp.pi)),
    )

    mode_slow_scaled = []
    for offset in (8, 12):
        raw = beta_substitution_convolution(sp.Integer(1), sp.Integer(2), sp.Integer(offset))
        normalized = raw / sp.pi
        mode_slow_scaled.append(float(sp.N(normalized * sp.exp(offset), 30)))
    ledger.check(
        "mode-slow coefficient approaches two",
        abs(mode_slow_scaled[1] - 2.0) < abs(mode_slow_scaled[0] - 2.0),
    )

    offset = sp.symbols("u", positive=True)
    equal_closed = 4 * (offset * sp.coth(offset) - 1) * sp.csch(offset) ** 2
    equal_direct, equal_error = quad(
        lambda value: stable_sech(value - 3.0) ** 2 * stable_sech(value) ** 2,
        -50.0,
        50.0,
        epsabs=1.0e-13,
        epsrel=1.0e-12,
    )
    ledger.check("equal-tail closed integral status", equal_error < 1.0e-10)
    ledger.check(
        "equal-tail closed integral",
        abs(equal_direct - float(equal_closed.subs(offset, 3))) < 2.0e-11,
    )
    equal_scaled = [
        float(sp.N((equal_closed / 2 * sp.exp(2 * offset) / offset).subs(offset, value), 30))
        for value in (12, 24)
    ]
    ledger.check(
        "equal-tail linear prefactor independently required",
        0.0 < 8.0 - equal_scaled[1] < 8.0 - equal_scaled[0],
    )

    x, center = sp.symbols("x center", real=True)
    index, eigenvalue, normalization, density_rate = exact_poschl_parameters(
        sp.Integer(2), sp.Integer(1)
    )
    mode = normalization * sp.sech(x - center) ** index
    operator = -sp.diff(mode, x, 2) - 2 * sp.sech(x - center) ** 2 * mode
    ledger.check("independent Poschl index", index == 1)
    ledger.check("independent Poschl eigenvalue", eigenvalue == -1)
    ledger.check("independent Poschl density rate", density_rate == 2)
    ledger.check(
        "independent translated operator residual",
        sp.simplify((operator - eigenvalue * mode).rewrite(sp.exp)) == 0,
    )
    ledger.check(
        "independent translated normalization",
        sp.simplify(normalization**2 * 2 - 1) == 0,
    )

    source_index, _source_eigenvalue, source_norm, source_mode_rate = exact_poschl_parameters(
        sp.Integer(12), sp.Rational(7, 10)
    )
    source_kappa = sp.sqrt(sp.Rational(1, 2) - sp.Rational(45, 100) ** 2)
    ledger.check("source mode tail faster", float(source_mode_rate) > float(source_kappa))
    overlaps = source_exact_overlaps()
    source_log_ratios = np.diff(np.log(overlaps))
    derived_slope = -4.0 * float(source_kappa)
    ledger.check("independent source overlaps decrease", bool(np.all(source_log_ratios < 0.0)))
    ledger.check(
        "independent source tail reaches slower core slope",
        abs(source_log_ratios[-1] - derived_slope) < 5.0e-8,
    )
    source_amplitude = 2 * sp.sqrt(6) * source_kappa
    source_q = source_kappa * sp.Rational(7, 10)
    source_tail_coefficient = sp.simplify(
        source_amplitude
        * source_norm**2
        * sp.Rational(7, 10)
        * 2 ** (2 * source_index)
        * sp.beta(source_index - source_q / 2, source_index + source_q / 2)
    )
    ledger.check(
        "independent source tail coefficient",
        abs(
            overlaps[-1] * np.exp(float(source_kappa) * 20.0)
            - float(source_tail_coefficient)
        )
        < 3.0e-8,
    )
    ledger.check("independent source span", overlaps[0] / overlaps[-1] > 1.0e3)
    ledger.check("source well index remains supplied", source_index.is_number is True)

    rate, spacing, rho = sp.symbols("rate spacing rho", positive=True)
    ledger.check(
        "independent rate-spacing null direction",
        sp.simplify((rho * rate) * (spacing / rho) - rate * spacing) == 0,
    )

    gaussian_a, gaussian_b, displacement = sp.symbols(
        "gaussian_a gaussian_b displacement", positive=True
    )
    gaussian_log = (
        sp.log(sp.sqrt(gaussian_a / (gaussian_a + gaussian_b)))
        - gaussian_a * gaussian_b * displacement**2 / (gaussian_a + gaussian_b)
    )
    ledger.check(
        "independent Gaussian log curvature nonzero",
        sp.simplify(sp.diff(gaussian_log, displacement, 2))
        == -2 * gaussian_a * gaussian_b / (gaussian_a + gaussian_b),
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
