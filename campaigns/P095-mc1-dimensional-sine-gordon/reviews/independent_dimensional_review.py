"""Independent exact reconstruction of P095's dimensional SG obligations."""

from __future__ import annotations

import ast
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P095-INDEPENDENT")

    lam, tension, mu = sp.symbols("lambda T mu", positive=True, real=True)
    x, time = sp.symbols("x t", real=True)
    field = sp.Function("u")(x, time)
    variation = sp.Function("v")(x, time)
    epsilon = sp.symbols("epsilon", real=True)
    varied_field = field + epsilon * variation
    varied_density = (
        lam * sp.diff(varied_field, time) ** 2 / 2
        - tension * sp.diff(varied_field, x) ** 2 / 2
        - mu * (1 - sp.cos(varied_field))
    )
    first_variation = sp.diff(varied_density, epsilon).subs(epsilon, 0)
    boundary_divergence = sp.diff(
        lam * sp.diff(field, time) * variation,
        time,
    ) - sp.diff(
        tension * sp.diff(field, x) * variation,
        x,
    )
    euler_coefficient = (
        -lam * sp.diff(field, time, 2)
        + tension * sp.diff(field, x, 2)
        - mu * sp.sin(field)
    )
    checks.check(
        "direct first variation separates boundary terms and the field equation",
        sp.simplify(
            first_variation - boundary_divergence - euler_coefficient * variation
        )
        == 0,
    )
    dimensional_residual = -euler_coefficient
    checks.mutation_sensitive(
        "independent variation fixes all three residual signs",
        lambda candidate: sp.simplify(candidate - dimensional_residual) == 0,
        dimensional_residual,
        (
            lam * sp.diff(field, time, 2)
            + tension * sp.diff(field, x, 2)
            + mu * sp.sin(field),
            lam * sp.diff(field, time, 2)
            - tension * sp.diff(field, x, 2)
            - mu * sp.sin(field),
        ),
    )

    coefficient_dimensions = sp.Matrix(
        [
            [1, 1, 1],
            [-1, 1, -1],
            [2, 0, 0],
        ]
    )
    checks.check(
        "density convention independently fixes three full-rank coefficient dimensions",
        coefficient_dimensions.det() == -4
        and coefficient_dimensions.rank() == 3,
    )
    scale_exponents = sp.Matrix(
        [
            [-sp.Rational(1, 2), sp.Rational(1, 2), 0],
            [-sp.Rational(1, 2), 0, sp.Rational(1, 2)],
            [0, sp.Rational(1, 2), -sp.Rational(1, 2)],
            [0, sp.Rational(1, 2), sp.Rational(1, 2)],
            [sp.Rational(1, 2), sp.Rational(1, 2), 0],
        ]
    ).T
    expected_scale_dimensions = sp.Matrix(
        [
            [0, 0, 0, 1, 1],
            [1, 0, 1, 0, 0],
            [-1, -1, 0, 0, 1],
        ]
    )
    checks.check(
        "fresh exponent calculation gives speed gap length energy and action units",
        coefficient_dimensions * scale_exponents == expected_scale_dimensions,
    )

    log_ratios = sp.Matrix(
        [
            [-sp.Rational(1, 2), sp.Rational(1, 2), 0],
            [-sp.Rational(1, 2), 0, sp.Rational(1, 2)],
            [0, sp.Rational(1, 2), -sp.Rational(1, 2)],
        ]
    )
    checks.check(
        "independent log-ratio map has one common-scale kernel",
        log_ratios.rank() == 2
        and log_ratios.nullspace() == [sp.ones(3, 1)],
    )
    inertia_scale, speed, gap = sp.symbols(
        "s c omega_0",
        positive=True,
        real=True,
    )
    inverse_ray = sp.Matrix(
        [inertia_scale, inertia_scale * speed**2, inertia_scale * gap**2]
    )
    recovered_ratios = sp.Matrix(
        [
            sp.sqrt(inverse_ray[1] / inverse_ray[0]),
            sp.sqrt(inverse_ray[2] / inverse_ray[0]),
            sp.sqrt(inverse_ray[1] / inverse_ray[2]),
        ]
    )
    checks.check(
        "inverse reconstruction retains an arbitrary positive coefficient scale",
        recovered_ratios == sp.Matrix([speed, gap, speed / gap])
        and sp.diff(inverse_ray, inertia_scale) != sp.zeros(3, 1),
    )

    alpha = sp.symbols("alpha", positive=True, real=True)
    original_coefficients = sp.Matrix([lam, tension, mu])
    scaled_coefficients = alpha * original_coefficients

    def ratios(coefficients: sp.Matrix) -> sp.Matrix:
        return sp.Matrix(
            [
                sp.sqrt(coefficients[1] / coefficients[0]),
                sp.sqrt(coefficients[2] / coefficients[0]),
                sp.sqrt(coefficients[1] / coefficients[2]),
            ]
        )

    original_energy_scale = sp.sqrt(tension * mu)
    original_action_scale = sp.sqrt(lam * tension)
    checks.check(
        "common scaling preserves kinematics but changes energy and action",
        sp.simplify(ratios(scaled_coefficients) - ratios(original_coefficients))
        == sp.zeros(3, 1)
        and sp.sqrt(scaled_coefficients[1] * scaled_coefficients[2])
        == alpha * original_energy_scale
        and sp.sqrt(scaled_coefficients[0] * scaled_coefficients[1])
        == alpha * original_action_scale,
    )
    checks.mutation_sensitive(
        "independent common-scale test rejects one-coefficient rescalings",
        lambda coefficients: sp.simplify(
            ratios(coefficients) - ratios(original_coefficients)
        )
        == sp.zeros(3, 1),
        scaled_coefficients,
        (
            sp.Matrix([alpha * lam, tension, mu]),
            sp.Matrix([lam, alpha * tension, mu]),
            sp.Matrix([lam, tension, alpha * mu]),
        ),
    )

    length = sp.sqrt(tension / mu)
    omega_zero = sp.sqrt(mu / lam)
    normalized_x, normalized_time = sp.symbols("X tau", real=True)
    normalized_field = sp.Function("U")(normalized_x, normalized_time)
    normalized_operator = (
        sp.diff(normalized_field, normalized_time, 2)
        - sp.diff(normalized_field, normalized_x, 2)
        + sp.sin(normalized_field)
    )
    chain_scaled = (
        lam * omega_zero**2 * sp.diff(normalized_field, normalized_time, 2)
        - tension / length**2 * sp.diff(normalized_field, normalized_x, 2)
        + mu * sp.sin(normalized_field)
    )
    checks.check(
        "independent chain rule yields mu times normalized sine-Gordon",
        sp.simplify(chain_scaled - mu * normalized_operator) == 0,
    )

    frequency = sp.symbols("w", positive=True, real=True)
    eta = sp.sqrt(1 - frequency**2)
    normalized_breather = 4 * sp.atan(
        eta
        * sp.sin(frequency * normalized_time)
        / (frequency * sp.cosh(eta * normalized_x))
    )
    normalized_breather_residual = sp.trigsimp(
        sp.diff(normalized_breather, normalized_time, 2)
        - sp.diff(normalized_breather, normalized_x, 2)
        + sp.sin(normalized_breather)
    )
    checks.check(
        "fresh closed-form differentiation verifies the normalized breather",
        sp.simplify(normalized_breather_residual) == 0,
    )

    initial_velocity = sp.simplify(
        sp.diff(normalized_breather, normalized_time).subs(normalized_time, 0)
    )
    independent_eta, integration_coordinate = sp.symbols(
        "eta z",
        positive=True,
        real=True,
    )
    sech_antiderivative = sp.tanh(integration_coordinate)
    unit_sech_integral = sp.simplify(
        sp.limit(sech_antiderivative, integration_coordinate, sp.oo)
        - sp.limit(sech_antiderivative, integration_coordinate, -sp.oo)
    )
    normalized_initial_energy = sp.simplify(
        8 * independent_eta**2 / independent_eta * unit_sech_integral
    ).subs(independent_eta, eta)
    physical_initial_energy = sp.simplify(
        lam * omega_zero**2 * length * normalized_initial_energy
    )
    checks.check(
        "independent kinetic slice gives physical breather energy",
        initial_velocity == 4 * eta / sp.cosh(eta * normalized_x)
        and sp.simplify(
            sp.diff(sech_antiderivative, integration_coordinate)
            - sp.sech(integration_coordinate) ** 2
        )
        == 0
        and unit_sech_integral == 2
        and sp.simplify(normalized_initial_energy - 16 * eta) == 0
        and sp.simplify(
            physical_initial_energy - original_energy_scale * 16 * eta
        )
        == 0,
    )

    phase_space_jacobian = sp.simplify(lam * omega_zero * length)
    normalized_action = 16 * sp.acos(frequency)
    physical_energy = original_energy_scale * 16 * eta
    physical_action = phase_space_jacobian * normalized_action
    physical_angular_frequency = frequency * omega_zero
    checks.check(
        "canonical phase-space measure gives the independent action scale",
        sp.simplify(phase_space_jacobian - original_action_scale) == 0,
    )
    checks.check(
        "physical action derivative recovers the physical angular frequency",
        sp.simplify(
            sp.diff(physical_energy, frequency)
            / sp.diff(physical_action, frequency)
            - physical_angular_frequency
        )
        == 0,
    )
    checks.mutation_sensitive(
        "energy and action carry distinct load-bearing Jacobians",
        lambda candidate: sp.simplify(
            sp.diff(physical_energy, frequency)
            / sp.diff(candidate, frequency)
            - physical_angular_frequency
        )
        == 0,
        physical_action,
        (
            original_energy_scale * normalized_action,
            normalized_action,
            2 * physical_action,
        ),
    )

    profile_length = length / eta
    one_over_e_length = sp.acosh(sp.E) * profile_length
    checks.check(
        "inverse tail scale is not the core one-over-e envelope distance",
        sp.simplify(
            1 / sp.cosh(eta * one_over_e_length / length) - sp.exp(-1)
        )
        == 0
        and sp.simplify(one_over_e_length - profile_length) != 0,
    )

    checks.check(
        "fixed normalized frequency softens delocalizes and loses energy as mu vanishes",
        sp.limit(frequency * omega_zero, mu, 0, dir="+") == 0
        and sp.limit(length / independent_eta, mu, 0, dir="+") == sp.oo
        and sp.limit(
            original_energy_scale * 16 * independent_eta,
            mu,
            0,
            dir="+",
        )
        == 0,
    )
    physical_frequency = sp.symbols("Omega", positive=True, real=True)
    fixed_physical_ratio = physical_frequency / omega_zero
    checks.check(
        "fixed positive physical frequency exits the normalized breather interval",
        sp.limit(fixed_physical_ratio, mu, 0, dir="+") == sp.oo,
    )

    harmonic = sp.symbols("kappa", nonzero=True, real=True)
    alternative_force = mu * sp.sin(field) + 2 * harmonic * sp.sin(2 * field)
    checks.check(
        "periodicity alone permits forces incompatible with sine-Gordon",
        sp.simplify(
            (alternative_force - mu * sp.sin(field)).subs(field, sp.pi / 4)
        )
        == 2 * harmonic,
    )

    review_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    direct_numpy_integrals = [
        node
        for node in ast.walk(review_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "np"
        and node.func.attr in {"trapz", "trapezoid"}
    ]
    checks.check(
        "independent exact review uses no direct NumPy trapezoidal alias",
        not direct_numpy_integrals,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
