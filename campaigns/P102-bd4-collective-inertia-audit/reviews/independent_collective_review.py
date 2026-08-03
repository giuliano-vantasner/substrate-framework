"""Independent exact P102 review without the canonical collective API."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("C-COL-001-INDEPENDENT")
    x, t = sp.symbols("x t", real=True)
    q = sp.Function("q", real=True)(t)
    phi = sp.Function("phi", real=True)(x, q)
    inertia_density = sp.symbols("lambda", positive=True)
    qdot = sp.diff(q, t)
    checks.check(
        "fresh field chain rule pulls velocity through the profile coordinate",
        sp.diff(phi, t) == sp.diff(phi, q) * qdot,
    )
    kinetic_density = inertia_density * sp.diff(phi, t) ** 2 / 2
    expected_density = (
        inertia_density * sp.diff(phi, q) ** 2 * qdot**2 / 2
    )
    checks.check(
        "fresh kinetic-density substitution has the exact one-half factor",
        sp.simplify(kinetic_density - expected_density) == 0,
    )

    coordinate = sp.Function("Q", real=True)(t)
    metric_function = sp.Function("M", positive=True)(coordinate)
    potential_function = sp.Function("U", real=True)(coordinate)
    reduced_lagrangian = (
        metric_function * sp.diff(coordinate, t) ** 2 / 2 - potential_function
    )
    direct_euler_lagrange = sp.simplify(
        sp.diff(sp.diff(reduced_lagrangian, sp.diff(coordinate, t)), t)
        - sp.diff(reduced_lagrangian, coordinate)
    )
    expected_euler_lagrange = sp.simplify(
        metric_function * sp.diff(coordinate, t, 2)
        + sp.diff(metric_function, coordinate) * sp.diff(coordinate, t) ** 2 / 2
        + sp.diff(potential_function, coordinate)
    )
    checks.check(
        "fresh Euler-Lagrange differentiation derives the connection term",
        sp.simplify(direct_euler_lagrange - expected_euler_lagrange) == 0,
    )

    mass, curvature = sp.symbols("M K", positive=True)
    growth = sp.symbols("s")
    characteristic = mass * growth**2 + curvature
    stable_roots = sp.solve(characteristic, growth)
    unstable_roots = sp.solve(characteristic.subs(curvature, -curvature), growth)
    checks.check(
        "fresh positive-curvature roots are imaginary",
        stable_roots == [-sp.I * sp.sqrt(curvature) / sp.sqrt(mass), sp.I * sp.sqrt(curvature) / sp.sqrt(mass)],
    )
    checks.check(
        "fresh negative-curvature roots are real exponentials",
        unstable_roots == [-sp.sqrt(curvature) / sp.sqrt(mass), sp.sqrt(curvature) / sp.sqrt(mass)],
    )
    checks.check(
        "fresh zero-curvature equation is linearly neutral",
        sp.solve(mass * growth**2, growth) == [0],
    )

    radius, tension, pressure = sp.symbols("R T P", positive=True)
    capillary = 2 * sp.pi * radius * tension - sp.pi * radius**2 * pressure
    stationary_radius = sp.solve(sp.Eq(sp.diff(capillary, radius), 0), radius)[0]
    capillary_curvature = sp.diff(capillary, radius, 2).subs(radius, stationary_radius)
    checks.check(
        "fresh capillary differentiation gives a strict maximum",
        stationary_radius == tension / pressure
        and capillary_curvature == -2 * sp.pi * pressure,
    )
    checks.check(
        "fresh capillary characteristic roots have the BD4 magnitude but unstable sign",
        sp.solve(mass * growth**2 + capillary_curvature, growth)
        == [
            -sp.sqrt(2) * sp.sqrt(sp.pi) * sp.sqrt(pressure) / sp.sqrt(mass),
            sp.sqrt(2) * sp.sqrt(sp.pi) * sp.sqrt(pressure) / sp.sqrt(mass),
        ],
    )

    old_coordinate, new_coordinate = sp.symbols("q Q", real=True)
    coordinate_scale = sp.symbols("a", positive=True)
    old_metric = sp.Function("M", positive=True)(old_coordinate)
    old_potential = sp.Function("U", real=True)(old_coordinate)
    inverse_map = new_coordinate / coordinate_scale
    jacobian = sp.diff(inverse_map, new_coordinate)
    transformed_metric = old_metric.subs(old_coordinate, inverse_map) * jacobian**2
    transformed_hessian_at_stationary = (
        sp.diff(old_potential, old_coordinate, 2).subs(old_coordinate, inverse_map)
        * jacobian**2
    )
    checks.check(
        "fresh coordinate rescaling co-transforms metric and stationary Hessian",
        jacobian == 1 / coordinate_scale
        and transformed_metric
        == old_metric.subs(old_coordinate, inverse_map) / coordinate_scale**2
        and transformed_hessian_at_stationary
        == sp.diff(old_potential, old_coordinate, 2).subs(old_coordinate, inverse_map)
        / coordinate_scale**2,
    )
    checks.check(
        "fresh stationary ratio cancels the coordinate Jacobian",
        sp.simplify(
            transformed_hessian_at_stationary / transformed_metric
            - sp.diff(old_potential, old_coordinate, 2).subs(old_coordinate, inverse_map)
            / old_metric.subs(old_coordinate, inverse_map)
        )
        == 0,
    )
    nonlinear_map = new_coordinate**2
    direct_hessian = sp.diff(old_potential.subs(old_coordinate, nonlinear_map), new_coordinate, 2)
    stationary_piece = (
        sp.diff(old_potential, old_coordinate, 2).subs(old_coordinate, nonlinear_map)
        * sp.diff(nonlinear_map, new_coordinate) ** 2
    )
    gradient_piece = (
        sp.diff(old_potential, old_coordinate).subs(old_coordinate, nonlinear_map)
        * sp.diff(nonlinear_map, new_coordinate, 2)
    )
    chain_hessian = stationary_piece + gradient_piece
    checks.check(
        "fresh nonstationary chain rule contains a gradient term",
        sp.simplify(direct_hessian - chain_hessian) == 0
        and sp.simplify(chain_hessian - stationary_piece - gradient_piece) == 0
        and sp.diff(nonlinear_map, new_coordinate, 2) != 0
        and gradient_piece != 0,
    )

    length = sp.symbols("ell", positive=True)
    profile_coordinate = sp.symbols("q0", real=True)
    gaussian = sp.exp(-(x - profile_coordinate) ** 2 / (2 * length**2))
    gaussian_integral = sp.integrate(
        sp.diff(gaussian, profile_coordinate) ** 2,
        (x, -sp.oo, sp.oo),
    )
    zero_integral = sp.integrate(sp.diff(x**2, profile_coordinate) ** 2, (x, -sp.oo, sp.oo))
    divergent_integral = sp.integrate(sp.diff(profile_coordinate * x, profile_coordinate) ** 2, (x, -sp.oo, sp.oo))
    checks.check(
        "fresh concrete profile has a finite positive geometric factor",
        gaussian_integral == sp.sqrt(sp.pi) / (2 * length),
    )
    checks.check(
        "fresh counterprofiles are zero and divergent despite the same formal dimension",
        zero_integral == 0 and divergent_integral is sp.oo,
    )

    dimension_matrix = sp.Matrix(
        [
            [1, 0, 0, 1, 1, 0],
            [-1, -1, 1, -2, -2, 0],
            [2, 0, 0, 2, 0, -2],
        ]
    )
    checks.check(
        "fresh dimension addition closes inertia and spectral ratio",
        dimension_matrix[:, 0] + 2 * dimension_matrix[:, 1] + dimension_matrix[:, 2]
        == dimension_matrix[:, 3]
        and dimension_matrix[:, 4] - dimension_matrix[:, 3]
        == dimension_matrix[:, 5],
    )

    normalization = sp.symbols("rho", positive=True)
    checks.check(
        "fresh common action scaling cancels while inertia-only scaling does not",
        sp.simplify((normalization * curvature) / (normalization * mass) - curvature / mass) == 0
        and sp.simplify(curvature / (normalization * mass) - curvature / mass) != 0,
    )
    observation_matrix = sp.Matrix(
        [[2, -1, 0], [0, sp.Rational(1, 2), sp.Rational(-1, 2)]]
    )
    observation_nullspace = observation_matrix.nullspace()
    checks.check(
        "fresh barrier-plus-rate observations retain one null direction",
        observation_matrix.rank() == 2
        and len(observation_nullspace) == 1
        and observation_matrix * observation_nullspace[0] == sp.zeros(2, 1)
        and observation_nullspace[0] == sp.Matrix([sp.Rational(1, 2), 1, 1]),
    )
    checks.check(
        "fresh exact review introduces no numerical solver fitted comparator or hbar map",
        not any(
            expression.has(sp.Float)
            for expression in (
                direct_euler_lagrange,
                capillary_curvature,
                gaussian_integral,
                transformed_hessian_at_stationary,
            )
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
