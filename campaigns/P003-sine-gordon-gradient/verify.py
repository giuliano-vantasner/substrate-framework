#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed claim C-SG-004."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.sine_gordon import (
    breather_action,
    breather_energy,
    breather_field,
    breather_field_with_width,
    breather_mean_gradient_integral,
    breather_period,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class GradientCandidate:
    coefficient: int
    offset: int
    action_sign: int


def candidate_expression(candidate: GradientCandidate, omega: sp.Symbol) -> sp.Expr:
    return candidate.coefficient * (
        sp.sqrt(1 - omega**2)
        - candidate.action_sign * omega * sp.acos(omega)
    ) + candidate.offset


def satisfies_legendre_definition(candidate: GradientCandidate) -> bool:
    omega = sp.symbols("omega", positive=True)
    expression = candidate_expression(candidate, omega)
    derivative_identity = sp.simplify(sp.diff(expression, omega) + breather_action(omega))
    endpoint = sp.limit(expression, omega, 1, dir="-")
    return derivative_identity == 0 and endpoint == 0


def run() -> int:
    checks = CheckLedger("C-SG-004")
    x, t = sp.symbols("x t", real=True)
    omega = sp.symbols("omega", positive=True)
    eta = sp.symbols("eta", positive=True)

    field = breather_field(x, t, omega)
    period = breather_period(omega)
    periodic_boundary_density = sp.simplify(
        (x * sp.diff(field, x) * sp.diff(field, t)).subs(t, t + period)
        - x * sp.diff(field, x) * sp.diff(field, t)
    )
    checks.check(
        "the time integration-by-parts boundary cancels over one exact period",
        periodic_boundary_density == 0,
    )

    localized_field = breather_field_with_width(x, t, omega, eta)
    spatial_boundary_terms = (
        x * sp.diff(localized_field, t) ** 2,
        x * sp.diff(localized_field, x) ** 2,
        x * (1 - sp.cos(localized_field)),
    )
    for index, term in enumerate(spatial_boundary_terms, start=1):
        checks.check(
            f"localized spatial boundary term {index} vanishes at plus infinity",
            sp.limit(term, x, sp.oo) == 0,
        )
        checks.check(
            f"localized spatial boundary term {index} vanishes at minus infinity",
            sp.limit(term, x, -sp.oo) == 0,
        )

    generic = sp.Function("phi")(x, t)
    time_product_identity = sp.simplify(
        sp.diff(x * sp.diff(generic, x) * sp.diff(generic, t), t)
        - x * sp.diff(generic, x) * sp.diff(generic, t, 2)
        - x * sp.diff(generic, x, t) * sp.diff(generic, t)
    )
    checks.check(
        "time integration-by-parts product rule has the required sign",
        time_product_identity == 0,
    )
    kinetic_spatial_identity = sp.simplify(
        sp.diff(x * sp.diff(generic, t) ** 2 / 2, x)
        - sp.diff(generic, t) ** 2 / 2
        - x * sp.diff(generic, t) * sp.diff(generic, x, t)
    )
    checks.check(
        "the kinetic spatial product rule produces plus Kbar/2",
        kinetic_spatial_identity == 0,
    )
    gradient_spatial_identity = sp.simplify(
        sp.diff(x * sp.diff(generic, x) ** 2 / 2, x)
        - sp.diff(generic, x) ** 2 / 2
        - x * sp.diff(generic, x) * sp.diff(generic, x, 2)
    )
    checks.check(
        "the gradient spatial product rule produces plus Gbar/2",
        gradient_spatial_identity == 0,
    )
    potential_identity = sp.simplify(
        sp.diff(x * (1 - sp.cos(generic)), x)
        - (1 - sp.cos(generic))
        - x * sp.sin(generic) * sp.diff(generic, x)
    )
    checks.check(
        "the potential product rule produces minus Vbar",
        potential_identity == 0,
    )

    kinetic, gradient, potential = sp.symbols("Kbar Gbar Vbar", real=True)
    energy_symbol, action_symbol = sp.symbols("E J", real=True)
    virial_solution = sp.solve(
        (
            sp.Eq(potential, (kinetic + gradient) / 2),
            sp.Eq(
                energy_symbol,
                (kinetic + gradient) / 2 + potential,
            ),
            sp.Eq(kinetic, omega * action_symbol),
        ),
        (kinetic, gradient, potential),
        dict=True,
    )[0]
    checks.check(
        "virial, Hamiltonian, and action equations derive Gbar = E-omega*J",
        sp.simplify(
            virial_solution[gradient]
            - (energy_symbol - omega * action_symbol)
        )
        == 0,
    )

    legendre_result = sp.simplify(
        breather_energy(omega) - omega * breather_action(omega)
    )
    expected = 16 * (
        sp.sqrt(1 - omega**2) - omega * sp.acos(omega)
    )
    checks.check(
        "accepted energy and action give the exact closed form",
        sp.simplify(legendre_result - expected) == 0,
    )
    checks.check(
        "the canonical API equals the independently assembled Legendre result",
        sp.simplify(breather_mean_gradient_integral(omega) - legendre_result) == 0,
    )
    checks.check(
        "dGbar/domega equals minus the accepted canonical action",
        sp.simplify(
            sp.diff(breather_mean_gradient_integral(omega), omega)
            + breather_action(omega)
        )
        == 0,
    )
    checks.check(
        "Gbar is strictly convex with curvature 16/sqrt(1-omega^2)",
        sp.simplify(
            sp.diff(breather_mean_gradient_integral(omega), omega, 2)
            - 16 / sp.sqrt(1 - omega**2)
        )
        == 0,
    )
    checks.mutation_sensitive(
        "gradient normalization, endpoint, sign, and half-factor",
        satisfies_legendre_definition,
        GradientCandidate(coefficient=16, offset=0, action_sign=1),
        [
            GradientCandidate(coefficient=15, offset=0, action_sign=1),
            GradientCandidate(coefficient=16, offset=1, action_sign=1),
            GradientCandidate(coefficient=16, offset=0, action_sign=-1),
            GradientCandidate(coefficient=8, offset=0, action_sign=1),
        ],
    )
    checks.check(
        "the kink-pair endpoint reaches 16",
        sp.limit(breather_mean_gradient_integral(omega), omega, 0, dir="+") == 16,
    )
    checks.check(
        "the harmonic endpoint vanishes",
        sp.limit(breather_mean_gradient_integral(omega), omega, 1, dir="-") == 0,
    )
    endpoint_scale = (1 - omega) ** sp.Rational(3, 2)
    checks.check(
        "the harmonic endpoint has the exact leading coefficient 32*sqrt(2)/3",
        sp.simplify(
            sp.limit(
                breather_mean_gradient_integral(omega) / endpoint_scale,
                omega,
                1,
                dir="-",
            )
            - 32 * sp.sqrt(2) / 3
        )
        == 0,
    )

    total = checks.finish()
    print(f"P003 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
