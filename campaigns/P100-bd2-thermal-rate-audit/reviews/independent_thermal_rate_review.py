"""Independent exact rederivation of the P100 conditional rate family."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P100-INDEPENDENT")

    x = sp.symbols("x", real=True)
    partition = 1 + sp.exp(-x)
    upper = sp.exp(-x) / partition
    gate = sp.simplify(2 * upper * (1 - upper))
    checks.check(
        "partition moments independently give the normalized symmetric gate",
        sp.simplify((gate - sp.sech(x / 2) ** 2 / 2).rewrite(sp.exp)) == 0,
    )

    quantum, thermal = sp.symbols("q vartheta", positive=True)
    y = quantum / (2 * thermal)
    coordinate = sp.tanh(y)
    scale = quantum / (2 * coordinate)
    checks.check(
        "direct coth-tanh inversion gives both effective-scale limits",
        sp.simplify(
            scale - quantum * sp.coth(quantum / (2 * thermal)) / 2
        )
        == 0
        and sp.limit(scale, thermal, 0, dir="+") == quantum / 2
        and sp.limit(scale / thermal, thermal, sp.oo) == 1,
    )

    tension, drive, radius = sp.symbols("tau p R", positive=True)
    energy = 2 * sp.pi * radius * tension - sp.pi * radius**2 * drive
    critical = sp.solve(sp.Eq(sp.diff(energy, radius), 0), radius)[0]
    barrier = sp.simplify(energy.subs(radius, critical) - energy.subs(radius, 0))
    checks.check(
        "independent capillary elimination gives pi tau squared over p",
        critical == tension / drive
        and barrier == sp.pi * tension**2 / drive,
    )

    frequency = sp.symbols("nu", positive=True)
    source_prefactor = frequency * tension / sp.sqrt(drive * scale)
    eliminated_prefactor = frequency * sp.sqrt(barrier / (sp.pi * scale))
    checks.check(
        "independent positive-domain elimination gives the reduced prefactor",
        sp.simplify(source_prefactor - eliminated_prefactor) == 0,
    )

    reduced_coordinate, ratio = sp.symbols("u b", positive=True)
    reduced_shape = (
        sp.sqrt(reduced_coordinate)
        * (1 - reduced_coordinate**2)
        * sp.exp(-2 * ratio * reduced_coordinate)
    )
    log_derivative = sp.factor(
        sp.diff(reduced_shape, reduced_coordinate) / reduced_shape
    )
    expected_log_derivative = (
        1 / (2 * reduced_coordinate)
        - 2 * reduced_coordinate / (1 - reduced_coordinate**2)
        - 2 * ratio
    )
    checks.check(
        "direct differentiation independently gives the stationary residual",
        sp.simplify(log_derivative - expected_log_derivative) == 0,
    )

    residual_derivative = sp.diff(expected_log_derivative, reduced_coordinate)
    checks.check(
        "independent residual is strictly decreasing on the physical interval",
        sp.simplify(
            residual_derivative
            - (
                -1 / (2 * reduced_coordinate**2)
                - 2 * (1 + reduced_coordinate**2)
                / (1 - reduced_coordinate**2) ** 2
            )
        )
        == 0,
    )
    upper = 1 / sp.sqrt(5)
    checks.check(
        "independent endpoint bracket gives one root below one over sqrt five",
        sp.limit(expected_log_derivative, reduced_coordinate, 0, dir="+")
        == sp.oo
        and sp.simplify(
            expected_log_derivative.subs(reduced_coordinate, upper) + 2 * ratio
        )
        == 0,
    )
    y_bound = sp.atanh(upper)
    checks.check(
        "independent thermal bound excludes the source onset coordinate",
        float(sp.N(y_bound, 40)) < 0.482
        and float(sp.N(1 / (2 * y_bound), 40)) > 1.039
        and float(sp.N(sp.tanh(1) - upper, 40)) > 0,
    )

    constant_shape = (
        (1 - reduced_coordinate**2)
        * sp.exp(-2 * ratio * reduced_coordinate)
    )
    positive_domain_coordinate = sp.symbols("y_domain", positive=True)
    physical_constant_derivative = sp.simplify(
        sp.diff(constant_shape, reduced_coordinate).subs(
            reduced_coordinate,
            sp.tanh(positive_domain_coordinate),
        )
    )
    manifest_negative_derivative = (
        -2
        * sp.exp(-2 * ratio * sp.tanh(positive_domain_coordinate))
        * (
            sp.tanh(positive_domain_coordinate)
            + ratio * sp.sech(positive_domain_coordinate) ** 2
        )
    )
    checks.check(
        "constant-prefactor comparison has no stationary point",
        sp.simplify(physical_constant_derivative - manifest_negative_derivative)
        == 0
        and (
            sp.tanh(positive_domain_coordinate)
            + ratio * sp.sech(positive_domain_coordinate) ** 2
        ).is_positive
        is True
        and sp.limit(constant_shape, reduced_coordinate, 0, dir="+") == 1
        and sp.limit(constant_shape, reduced_coordinate, 1, dir="-") == 0,
    )

    activation_scale, energy_barrier = sp.symbols("Theta E", positive=True)
    barrier_response = sp.sqrt(energy_barrier / activation_scale) * sp.exp(
        -energy_barrier / activation_scale
    )
    log_barrier_response = (
        sp.log(energy_barrier / activation_scale) / 2
        - energy_barrier / activation_scale
    )
    barrier_elasticity = sp.simplify(
        energy_barrier
        * sp.diff(log_barrier_response, energy_barrier)
    )
    checks.check(
        "direct barrier derivative independently proves the half-ratio threshold",
        sp.simplify(
            barrier_elasticity
            - (sp.Rational(1, 2) - energy_barrier / activation_scale)
        )
        == 0,
    )

    amplitude = sp.symbols("A", positive=True)
    constant = sp.symbols("C", positive=True)
    amplitude_barrier = constant / amplitude**2
    amplitude_response = sp.sqrt(amplitude_barrier / activation_scale) * sp.exp(
        -amplitude_barrier / activation_scale
    )
    amplitude_elasticity = sp.simplify(
        amplitude
        * sp.diff(amplitude_response, amplitude)
        / amplitude_response
    )
    checks.check(
        "independent loading derivative changes sign at E over Theta one half",
        sp.simplify(
            amplitude_elasticity
            - (2 * amplitude_barrier / activation_scale - 1)
        )
        == 0,
    )

    sensitivity_coordinate = sp.symbols("y_sensitivity", positive=True)
    gate_y = sp.sech(sensitivity_coordinate) ** 2 / 2
    log_temperature_slope = sp.simplify(
        -sensitivity_coordinate
        * sp.diff(gate_y, sensitivity_coordinate)
    )
    ordinary_temperature_slope_shape = sp.simplify(
        sensitivity_coordinate * log_temperature_slope
    )
    checks.check(
        "independent chain rule separates log and ordinary temperature slopes",
        log_temperature_slope
        == sensitivity_coordinate
        * sp.sech(sensitivity_coordinate) ** 2
        * sp.tanh(sensitivity_coordinate)
        and ordinary_temperature_slope_shape
        == sensitivity_coordinate**2
        * sp.sech(sensitivity_coordinate) ** 2
        * sp.tanh(sensitivity_coordinate),
    )

    rho = sp.symbols("rho", positive=True)
    dimensionless_shape = (
        sp.sqrt(energy_barrier / activation_scale)
        * sp.exp(-energy_barrier / activation_scale)
        * sp.sech(quantum / (2 * thermal)) ** 2
        / 2
    )
    checks.check(
        "independent common-energy orbit preserves the response shape",
        sp.simplify(
            dimensionless_shape.subs(
                {
                    energy_barrier: rho * energy_barrier,
                    activation_scale: rho * activation_scale,
                    quantum: rho * quantum,
                    thermal: rho * thermal,
                },
                simultaneous=True,
            )
            - dimensionless_shape
        )
        == 0,
    )

    checks.mutation_sensitive(
        "independent gate factor is load bearing",
        lambda coefficient: sp.simplify(
            (
                gate
                - coefficient * sp.sech(x / 2) ** 2
            ).rewrite(sp.exp)
        )
        == 0,
        sp.Rational(1, 2),
        (1, sp.Rational(1, 4)),
    )
    checks.mutation_sensitive(
        "independent capillary coefficient is load bearing",
        lambda coefficient: sp.simplify(
            coefficient * tension**2 / drive - barrier
        )
        == 0,
        sp.pi,
        (1, 2 * sp.pi),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
