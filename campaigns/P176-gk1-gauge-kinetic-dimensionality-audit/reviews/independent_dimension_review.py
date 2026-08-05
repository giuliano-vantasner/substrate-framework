#!/usr/bin/env python3
"""Independent exponent derivation for proposed C-DIM-009.

This route intentionally imports neither GK1 nor the campaign's primary
verifier nor ``substrate_framework.gauge_dimensions``.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _coupling_mass_completion(candidate: object) -> bool:
    dimension = sp.Symbol("D", positive=True)
    exponent = sp.sympify(candidate)
    return sp.simplify(4 - dimension + exponent - 2) == 0


def _connection_conversion_power(candidate: object) -> bool:
    strength, field_strength = sp.symbols("g F", positive=True)
    power = sp.sympify(candidate)
    return sp.simplify((strength * field_strength) ** 2 / strength**power - field_strength**2) == 0


def main() -> int:
    checks = CheckLedger("P176-INDEPENDENT-C-DIM-009")
    dimension = sp.Symbol("D", positive=True)
    potential_dimension, coupling_dimension = sp.symbols("a gamma", real=True)

    action_equation = sp.Eq(-dimension + 2 * (potential_dimension + 1), 0)
    minimal_coupling_equation = sp.Eq(coupling_dimension + potential_dimension, 1)
    solution = sp.solve(
        (action_equation, minimal_coupling_equation),
        (potential_dimension, coupling_dimension),
        dict=True,
    )
    checks.check(
        "the action and covariant derivative give one canonical solution",
        len(solution) == 1
        and solution[0][potential_dimension] == dimension / 2 - 1
        and solution[0][coupling_dimension] == 2 - dimension / 2,
    )

    canonical_potential = solution[0][potential_dimension]
    canonical_coupling = solution[0][coupling_dimension]
    fourier_potential = sp.simplify(canonical_potential - dimension)
    projector_dimension = sp.solve(
        sp.Eq(
            dimension + 2 * fourier_potential + sp.Symbol("pi_dimension"),
            0,
        ),
        sp.Symbol("pi_dimension"),
    )
    checks.check(
        "the momentum-space quadratic projector coefficient has dimension two",
        projector_dimension == [2],
    )

    coupling_squared_dimension = sp.simplify(2 * canonical_coupling)
    pure_solution = sp.solve(
        sp.Eq(coupling_squared_dimension, projector_dimension[0]), dimension
    )
    checks.check(
        "the scale-free pure-coupling ansatz selects D equals two",
        coupling_squared_dimension == 4 - dimension and pure_solution == [2],
    )
    checks.mutation_sensitive(
        "the supplied mass power D minus two is necessary",
        _coupling_mass_completion,
        dimension - 2,
        [dimension - 4, dimension],
    )
    checks.check(
        "a positive independent mass scale completes the coefficient in every D",
        sp.simplify(coupling_squared_dimension + dimension - 2) == 2,
    )

    connection_potential_dimension = sp.simplify(
        canonical_coupling + canonical_potential
    )
    connection_curvature_dimension = sp.simplify(
        connection_potential_dimension + 1
    )
    connection_coefficient_dimension = sp.simplify(
        dimension - 2 * connection_curvature_dimension
    )
    checks.check(
        "absorbing the coupling gives connection dimensions one and two",
        connection_potential_dimension == 1
        and connection_curvature_dimension == 2
        and connection_coefficient_dimension == dimension - 4,
    )
    checks.mutation_sensitive(
        "density equality requires division by coupling squared",
        _connection_conversion_power,
        2,
        [0, 1, 4],
    )

    strength, canonical_coefficient, curvature = sp.symbols(
        "g kappa F", positive=True
    )
    connection_curvature = strength * curvature
    connection_coefficient = canonical_coefficient / strength**2
    checks.check(
        "the two kinetic densities coincide exactly",
        sp.simplify(
            connection_coefficient * connection_curvature**2 / 4
            - canonical_coefficient * curvature**2 / 4
        )
        == 0,
    )

    q2, mass, scale = sp.symbols("Q M lambda", positive=True)
    form_factors = (
        sp.Integer(1),
        q2 / (q2 + mass**2),
        sp.log(1 + q2 / mass**2),
    )
    scaled = (
        sp.Integer(1),
        scale**2 * q2 / (scale**2 * q2 + scale**2 * mass**2),
        sp.log(1 + scale**2 * q2 / (scale**2 * mass**2)),
    )
    checks.check(
        "three distinct four-dimensional form factors are scale invariant",
        all(
            sp.simplify(after - before) == 0
            for after, before in zip(scaled, form_factors, strict=True)
        )
        and sp.simplify(form_factors[0] - form_factors[1]) != 0
        and sp.simplify(form_factors[1] - form_factors[2]) != 0,
    )
    checks.check(
        "multiplication by Q gives dimension-two projector homogeneity",
        all(
            sp.simplify(scale**2 * q2 * after - scale**2 * q2 * before) == 0
            for after, before in zip(scaled, form_factors, strict=True)
        ),
    )

    trace_index, generator_scale = sp.symbols("T_R rho", positive=True)
    original_weight = strength**2 * trace_index
    transformed_weight = (
        strength / generator_scale
    ) ** 2 * generator_scale**2 * trace_index
    checks.check(
        "generator scaling requires inverse coupling scaling",
        sp.simplify(transformed_weight - original_weight) == 0,
    )
    checks.check(
        "changing only the trace factor changes the physical loop weight",
        sp.simplify(
            strength**2 * generator_scale**2 * trace_index - original_weight
        )
        != 0,
    )

    component_count = dimension * (dimension - 1) / 2
    magnetic_count = (dimension - 1) * (dimension - 2) / 2
    checks.check(
        "the supplied D two and D four component counts are exact",
        component_count.subs(dimension, 2) == 1
        and component_count.subs(dimension, 4) == 6
        and magnetic_count.subs(dimension, 2) == 0
        and magnetic_count.subs(dimension, 4) == 3,
    )

    loop, bare, counterterm = sp.symbols("k_loop k_bare k_ct", real=True)
    total = loop + bare + counterterm
    checks.check(
        "a loop contribution does not identify the total kinetic coefficient",
        sp.diff(total, bare) == 1
        and sp.diff(total, counterterm) == 1
        and sp.simplify(total.subs(bare, 0) - total.subs(bare, 1)) == -1,
    )

    riesz_shape, source_amplitude = sp.symbols("G A_source", nonzero=True)
    checks.check(
        "a normalized Green shape does not determine its independent amplitude",
        sp.diff(source_amplitude * riesz_shape, source_amplitude) == riesz_shape
        and sp.solve(
            sp.Eq(source_amplitude * riesz_shape, sp.Symbol("observed")),
            source_amplitude,
        )
        == [sp.Symbol("observed") / riesz_shape],
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
