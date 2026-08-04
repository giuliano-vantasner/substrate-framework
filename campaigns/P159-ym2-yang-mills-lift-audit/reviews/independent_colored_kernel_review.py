#!/usr/bin/env python3
"""Fresh exact review of color-kernel inversion and the YM2 lift boundary."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P159-INDEPENDENT")
    imaginary = sp.I
    generators = (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -imaginary], [imaginary, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )
    trace_metric = sp.Matrix(
        3,
        3,
        lambda first, second: sp.trace(
            generators[first] * generators[second]
        ),
    )
    checks.check("fresh Pauli-half trace metric", trace_metric == sp.eye(3) / 2)

    radius, momentum2, coefficient, tau = sp.symbols(
        "r k2 A T_R", positive=True
    )
    scalar_coulomb = 1 / (4 * sp.pi * coefficient * radius)
    checks.check(
        "fresh d3 radial flux fixes the scalar normalization",
        sp.simplify(
            4
            * sp.pi
            * radius**2
            * (-sp.diff(scalar_coulomb, radius))
            - 1 / coefficient
        )
        == 0,
    )
    kinetic_matrix = coefficient * tau * momentum2 * sp.eye(3)
    inverse_matrix = kinetic_matrix.inv()
    checks.check(
        "fresh matrix inversion gives reciprocal trace index",
        inverse_matrix == sp.eye(3) / (coefficient * tau * momentum2),
    )
    direct_weight = tau * sp.eye(3) / (coefficient * momentum2)
    checks.check(
        "fresh direct trace weighting is not that inverse",
        sp.simplify((inverse_matrix - direct_weight)[0, 0])
        == (1 - tau**2) / (coefficient * momentum2 * tau),
    )
    checks.check(
        "fresh fundamental specialization separates the two normalizations",
        inverse_matrix[0, 0].subs(tau, sp.Rational(1, 2))
        == 2 / (coefficient * momentum2)
        and direct_weight[0, 0].subs(tau, sp.Rational(1, 2))
        == 1 / (2 * coefficient * momentum2),
    )
    checks.check(
        "fresh adjoint-index mutation reverses the scaling",
        inverse_matrix[0, 0].subs(tau, 2)
        == 1 / (2 * coefficient * momentum2)
        and direct_weight[0, 0].subs(tau, 2)
        == 2 / (coefficient * momentum2),
    )

    source = sp.Matrix(sp.symbols("J1:4", real=True))
    exchange = sp.simplify((source.T * inverse_matrix * source)[0])
    checks.check(
        "fresh exchange amplitude requires a source vector",
        exchange
        == sum(component**2 for component in source)
        / (coefficient * tau * momentum2),
    )
    checks.check(
        "fresh zero source removes exchange",
        exchange.subs({component: 0 for component in source}) == 0,
    )

    structure_switch = sp.symbols("epsilon", real=True)
    checks.check(
        "fresh structure switch cannot change a fixed trace metric",
        sp.diff(trace_metric[2, 2], structure_switch) == 0
        and trace_metric[2, 2] == sp.Rational(1, 2),
    )
    checks.check(
        "fresh unit U1 factor is a new normalization",
        sp.trace(generators[2] ** 2) != 1,
    )

    dimension, power = sp.symbols("d s", positive=True)
    potential_power = 2 * power - dimension
    force_power = potential_power - 1
    checks.check(
        "fresh inverse-square solve gives a family",
        sp.solve(sp.Eq(force_power, -2), dimension) == [2 * power + 1],
    )
    checks.check(
        "fresh noninteger pair is an exact inverse-square counterexample",
        force_power.subs(
            {dimension: sp.Rational(14, 5), power: sp.Rational(9, 10)}
        )
        == -2,
    )
    checks.check(
        "fresh fixed-d wrong-power guard cannot select the dimension",
        potential_power.subs({dimension: 3, power: sp.Rational(9, 10)})
        == sp.Rational(-6, 5)
        and potential_power.subs({dimension: 4, power: sp.Rational(3, 2)}) == -1,
    )

    frequency, spatial_k2 = sp.symbols("omega k_spatial2", real=True)
    lorentzian_symbol = spatial_k2 - frequency**2
    checks.check(
        "fresh static slice agrees only at zero frequency",
        lorentzian_symbol.subs(frequency, 0) == spatial_k2
        and lorentzian_symbol.subs(frequency, 2) != spatial_k2,
    )
    gauge_parameter, normalization = sp.symbols("xi kappa", positive=True)
    transverse = normalization * momentum2
    longitudinal = normalization * momentum2 / gauge_parameter
    checks.check(
        "fresh gauge parameter changes a missing longitudinal sector",
        sp.diff(transverse, gauge_parameter) == 0
        and sp.diff(longitudinal, gauge_parameter) != 0,
    )

    bare, loop = sp.symbols("B L", positive=True)
    total_inverse = (bare + loop) * momentum2
    checks.check(
        "fresh bare-plus-loop family changes the propagator",
        sp.simplify(1 / total_inverse.subs(bare, 1) - 1 / total_inverse.subs(bare, 2))
        != 0,
    )
    field_scale = sp.symbols("lambda", positive=True)
    checks.check(
        "fresh field rescaling changes the displayed quadratic coefficient",
        sp.diff(field_scale**2 * total_inverse, field_scale) != 0,
    )

    source_strength, probe_strength = sp.symbols("Q q", real=True)
    kernel = scalar_coulomb.subs(coefficient, coefficient * tau)
    energy = sp.simplify(source_strength * probe_strength * kernel)
    force = sp.simplify(-sp.diff(energy, radius))
    checks.check(
        "fresh force ledger contains both source strengths",
        force
        == source_strength
        * probe_strength
        / (4 * sp.pi * coefficient * tau * radius**2),
    )
    checks.check(
        "fresh probe-sign mutation reverses the force",
        sp.simplify(force.subs(probe_strength, -probe_strength) + force) == 0,
    )
    checks.check(
        "fresh dimensionless color factor cannot define a dimension map",
        sp.diff(tau, dimension) == 0
        and potential_power.subs(dimension, 3)
        != potential_power.subs(dimension, 4),
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P159 INDEPENDENT ALL {result} CHECKS PASS")
