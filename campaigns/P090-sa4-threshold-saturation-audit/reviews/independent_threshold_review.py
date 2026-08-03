"""Independent analytic and adaptive-quadrature review for P090."""

from __future__ import annotations

import math

import sympy as sp
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P090-INDEPENDENT")
    omega_b = 1.0 / math.sqrt(2.0)
    tau = 10.0
    energy_unit = 16.0 * math.sqrt(1.0 - omega_b**2)

    def kernel(frequency: float, sharpness: float = tau) -> float:
        return math.exp(-sharpness**2 * (frequency - omega_b) ** 2) + math.exp(
            -sharpness**2 * (frequency + omega_b) ** 2
        )

    def band_value(slew: float, *, fixed_peak: bool = False) -> tuple[float, float]:
        normalization = slew**-2 if fixed_peak else 1.0
        value, error = quad(
            lambda frequency: normalization
            * frequency**2
            * math.exp(-(frequency / slew) ** 2)
            * kernel(frequency),
            0.0,
            2.0,
            epsabs=1.0e-13,
            epsrel=1.0e-13,
            limit=200,
        )
        return value, error

    ceiling, ceiling_error = quad(
        lambda frequency: frequency**2 * kernel(frequency),
        0.0,
        2.0,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
        limit=200,
    )
    analytic_full_line_ceiling = math.sqrt(math.pi) * (
        omega_b**2 / tau + 1.0 / (2.0 * tau**3)
    )
    checks.check(
        "adaptive ceiling agrees with the independently derived Gaussian moment",
        abs(ceiling - analytic_full_line_ceiling) / analytic_full_line_ceiling
        < 1.0e-12
        and ceiling_error < 1.0e-12,
    )

    slews = (0.3, 0.5, 0.8, 1.2, 2.0, 4.0, 8.0, 16.0)
    values_and_errors = [band_value(value) for value in slews]
    values = [item[0] for item in values_and_errors]
    counts = [math.floor(900.0 * value / energy_unit) for value in values]
    checks.check(
        "fresh adaptive integration reproduces the inserted count sequence",
        counts == [0, 0, 3, 4, 6, 6, 7, 7]
        and max(item[1] for item in values_and_errors) < 1.0e-12,
    )

    normalized = [value / ceiling for value in values]

    def michaelis_error(scale: float) -> float:
        return sum(
            (fraction - slew / (slew + scale)) ** 2
            for fraction, slew in zip(normalized, slews, strict=True)
        )

    fit = minimize_scalar(
        michaelis_error,
        bounds=(0.05, 5.0),
        method="bounded",
        options={"xatol": 1.0e-12},
    )
    checks.check(
        "independent optimizer reproduces the loose source fit",
        fit.success
        and abs(fit.x - 0.899) < 0.01
        and abs(fit.fun - 0.1960) < 5.0e-4,
    )
    checks.check(
        "fit residual is material on the normalized eight-point curve",
        math.sqrt(fit.fun / len(slews)) > 0.15,
    )

    sharp_half_scale = omega_b / math.sqrt(math.log(2.0))
    checks.check(
        "sharp-lobe half scale matches the fitted coordinate without bandwidth input",
        abs(sharp_half_scale - 0.8493218) < 1.0e-6
        and abs(math.exp(-(omega_b / sharp_half_scale) ** 2) - 0.5) < 1.0e-14,
    )

    inserted_large = [band_value(value)[0] for value in (4.0, 8.0, 16.0)]
    fixed_large = [band_value(value, fixed_peak=True)[0] for value in (4.0, 8.0, 16.0)]
    checks.check(
        "fresh normalization counterfamily reverses the large-slew ordering",
        inserted_large[0] < inserted_large[1] < inserted_large[2]
        and fixed_large[0] > fixed_large[1] > fixed_large[2],
    )

    weak_value, weak_error = band_value(0.2)
    crossing_gain = energy_unit / weak_value
    checks.check(
        "source sub-threshold example is moved through threshold by free gain",
        weak_error < 1.0e-12
        and math.floor(0.5 * crossing_gain * weak_value / energy_unit) == 0
        and math.floor(crossing_gain * weak_value / energy_unit) == 1
        and crossing_gain > 900.0,
    )

    source_dc = kernel(0.0, 10.0)
    mutated_dc = kernel(0.0, 5.0)
    checks.check(
        "fresh finite-sharpness mutation rejects the alleged exact DC null",
        0.0 < source_dc < 1.0e-9 and mutated_dc > 1.0e-9,
    )

    frequency, slew, scale = sp.symbols("omega s a", positive=True, real=True)
    sharp_response = sp.exp(-(frequency / slew) ** 2)
    michaelis = slew / (slew + scale)
    checks.check(
        "fresh asymptotic rederivation separates Gaussian fill from Michaelis response",
        sp.limit(sharp_response / slew, slew, 0, dir="+") == 0
        and sp.limit(michaelis / slew, slew, 0, dir="+") == 1 / scale
        and sp.limit(slew * (1 - sharp_response), slew, sp.oo) == 0
        and sp.limit(slew * (1 - michaelis), slew, sp.oo) == scale,
    )

    count = sp.Symbol("n", integer=True, nonnegative=True)
    unit, score = sp.symbols("E_b F", positive=True, real=True)
    chosen_gain = (count + sp.Rational(1, 2)) * unit / score
    checks.check(
        "fresh inverse construction realizes arbitrary floor populations",
        sp.floor(chosen_gain * score / unit) == count,
    )
    checks.check(
        "fresh floor and ceiling audit separates completed units from required units",
        sp.floor(sp.Rational(3, 2)) == 1
        and sp.ceiling(sp.Rational(3, 2)) == 2,
    )

    exact_breather_energy = 16 * sp.sqrt(1 - frequency**2)
    checks.check(
        "fresh accepted-family limit rejects a positive universal breather-energy floor",
        sp.limit(exact_breather_energy, frequency, 1, dir="-") == 0,
    )

    common_slew = sp.Symbol("S", positive=True)
    low_frequency, high_frequency = sp.Integer(1), sp.Integer(3)
    low_amplitude = common_slew / low_frequency
    high_amplitude = common_slew / high_frequency
    selector = lambda item: sp.exp(-4 * (item - low_frequency) ** 2)
    low_score = low_amplitude**2 * selector(low_frequency)
    high_score = high_amplitude**2 * selector(high_frequency)
    checks.check(
        "equal maximum slew does not fix spectral overlap",
        low_amplitude * low_frequency == common_slew
        and high_amplitude * high_frequency == common_slew
        and sp.simplify(low_score / high_score) == 9 * sp.exp(16),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
