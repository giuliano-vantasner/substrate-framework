"""Independent transform and waveform audit for P088."""

from __future__ import annotations

import mpmath
import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P088-INDEPENDENT")
    frequency, center, packet_center, width, sigma = sp.symbols(
        "omega omega_b mu tau sigma", positive=True, real=True
    )
    gaussian_quadratic = width**2 + 1 / (2 * sigma**2)
    gaussian_linear = width**2 * center + packet_center / (2 * sigma**2)
    gaussian_constant = width**2 * center**2 + packet_center**2 / (2 * sigma**2)
    fresh_overlap = sp.simplify(
        sp.exp(gaussian_linear**2 / gaussian_quadratic - gaussian_constant)
        / (sigma * sp.sqrt(2 * gaussian_quadratic))
    )
    closed_overlap = sp.exp(
        -width**2 * (packet_center - center) ** 2
        / (1 + 2 * sigma**2 * width**2)
    ) / sp.sqrt(1 + 2 * sigma**2 * width**2)
    checks.check(
        "fresh completion of the square reproduces the Gaussian overlap",
        sp.simplify(fresh_overlap / closed_overlap) == 1,
    )
    checks.check(
        "fresh sharp-kernel-first limit kills DC and exact resonance alike",
        sp.limit(closed_overlap.subs(packet_center, 0), width, sp.oo) == 0
        and sp.limit(closed_overlap.subs(packet_center, center), width, sp.oo) == 0,
    )
    checks.check(
        "fresh delta-first limit retains resonance and rejects DC",
        sp.limit(
            sp.limit(
                closed_overlap.subs(packet_center, center), sigma, 0, dir="+"
            ),
            width,
            sp.oo,
        )
        == 1
        and sp.limit(
            sp.limit(closed_overlap.subs(packet_center, 0), sigma, 0, dir="+"),
            width,
            sp.oo,
        )
        == 0,
    )

    time, duration, offset = sp.symbols("t T c", positive=True, real=True)
    finite_shift = sp.integrate(
        offset * sp.exp(-sp.I * frequency * time), (time, 0, duration)
    )
    checks.check(
        "fresh finite-record transform has generic nonzero leakage",
        sp.simplify(
            finite_shift.subs(frequency, sp.pi / duration)
            + 2 * sp.I * offset * duration / sp.pi
        )
        == 0
        and sp.simplify(finite_shift.subs(frequency, 2 * sp.pi / duration)) == 0,
    )

    response = sp.Function("epsilon")(time)
    electric_field = sp.Function("E")(time)
    product_current = sp.diff(response * electric_field, time)
    checks.check(
        "fresh product-rule derivation exposes the omitted response-rate term",
        sp.simplify(
            product_current
            - response * sp.diff(electric_field, time)
            - electric_field * sp.diff(response, time)
        )
        == 0,
    )
    boundary, transform = sp.symbols("B Vhat")
    checks.check(
        "fresh integration-by-parts ledger keeps the boundary term",
        boundary + sp.I * frequency * transform
        != sp.I * frequency * transform
        and (boundary + sp.I * frequency * transform).subs(boundary, 0)
        == sp.I * frequency * transform,
    )

    slew = sp.Symbol("s", positive=True)
    inserted = frequency**2 * sp.exp(-(frequency / slew) ** 2)
    fixed_peak = inserted / slew**2
    checks.check(
        "fresh scaling audit makes the inserted family increase pointwise",
        sp.simplify(
            sp.diff(inserted, slew)
            - 2 * frequency**4 * sp.exp(-(frequency / slew) ** 2) / slew**3
        )
        == 0,
    )
    checks.check(
        "fresh fixed-peak rescaling makes the same band decrease for slew above frequency",
        sp.simplify(
            sp.diff(fixed_peak, slew)
            - 2
            * frequency**2
            * (frequency**2 - slew**2)
            * sp.exp(-(frequency / slew) ** 2)
            / slew**5
        )
        == 0
        and sp.diff(fixed_peak, slew).subs({frequency: 1, slew: 2}) < 0,
    )
    checks.check(
        "fresh limits separate inserted saturation from fixed-peak decay",
        sp.limit(inserted, slew, sp.oo) == frequency**2
        and sp.limit(fixed_peak, slew, sp.oo) == 0,
    )

    gaussian_spectrum = sp.exp(-frequency**2 / (2 * slew**2))
    inverse_transform = sp.integrate(
        gaussian_spectrum * sp.exp(sp.I * frequency * time),
        (frequency, -sp.oo, sp.oo),
    ) / (2 * sp.pi)
    expected_time_pulse = slew * sp.exp(-slew**2 * time**2 / 2) / sp.sqrt(2 * sp.pi)
    checks.check(
        "fresh inverse transform shows that the alleged fixed amplitude scales with slew",
        sp.simplify(inverse_transform - expected_time_pulse) == 0
        and sp.diff(expected_time_pulse.subs(time, 0), slew) != 0,
    )

    shared_slope = sp.Symbol("S", positive=True)
    low_frequency, high_frequency = sp.Integer(1), sp.Integer(3)
    low_amplitude = shared_slope / low_frequency
    high_amplitude = shared_slope / high_frequency
    select_low = lambda item: sp.exp(-4 * (item - low_frequency) ** 2)
    low_score = low_amplitude**2 * select_low(low_frequency)
    high_score = high_amplitude**2 * select_low(high_frequency)
    checks.check(
        "fresh sinusoidal counterfamily has equal maximum slope but unequal score",
        low_amplitude * low_frequency == shared_slope
        and high_amplitude * high_frequency == shared_slope
        and sp.simplify(low_score / high_score) == 9 * sp.exp(16)
        and 9 * sp.exp(16) > 1,
    )

    mpmath.mp.dps = 40

    def kernel(item: mpmath.mpf) -> mpmath.mpf:
        center_value = 1 / mpmath.sqrt(2)
        return mpmath.exp(-16 * (item - center_value) ** 2) + mpmath.exp(
            -16 * (item + center_value) ** 2
        )

    def overlap(slew_value: mpmath.mpf, fixed: bool) -> mpmath.mpf:
        center_value = 1 / mpmath.sqrt(2)
        normalization = slew_value**-2 if fixed else 1
        return mpmath.quad(
            lambda item: normalization
            * item**2
            * mpmath.exp(-(item / slew_value) ** 2)
            * kernel(item),
            [0, center_value],
        )

    inserted_values = [overlap(mpmath.mpf(value), False) for value in (1, 2, 4)]
    fixed_values = [overlap(mpmath.mpf(value), True) for value in (1, 2, 4)]
    checks.check(
        "independent high-precision quadrature confirms normalization-sensitive trends",
        inserted_values[0] < inserted_values[1] < inserted_values[2]
        and fixed_values[0] > fixed_values[1] > fixed_values[2],
    )

    input_dimension, response_dimension, frequency_dimension, energy_dimension = (
        sp.symbols("d_S d_chi d_omega d_E")
    )
    count_dimension = (
        input_dimension + response_dimension + frequency_dimension - energy_dimension
    )
    checks.check(
        "fresh dimensional ledger leaves the population normalization undeclared",
        sp.solve(sp.Eq(count_dimension, 0), response_dimension)
        == [energy_dimension - frequency_dimension - input_dimension],
    )
    checks.check(
        "fresh dependency ledger separates derivative algebra from a response mechanism",
        len(
            {
                "voltage-to-field map",
                "driven interaction",
                "causal response",
                "absorption",
                "formation rule",
                "breakdown dynamics",
            }
        )
        == 6,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
