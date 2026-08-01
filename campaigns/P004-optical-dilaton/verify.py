#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for C-OG-001 and C-OG-002."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.optical_geometry import (
    index_from_potential,
    optical_box_static_1d,
    optical_dilaton,
    optical_metric_1d,
    optical_ricci_scalar_1d,
    slow_geodesic_acceleration_from_potential,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class DilatonCandidate:
    log_scale: int
    linear_scale: int


@dataclass(frozen=True)
class PotentialMapCandidate:
    index_coefficient: int
    geodesic_denominator: int


def dilaton_candidate_is_general_solution(candidate: DilatonCandidate) -> bool:
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    n = sp.Function("n", positive=True)(x)
    scalar = candidate.log_scale * sp.log(n) + candidate.linear_scale * n
    residual = sp.simplify(
        optical_box_static_1d(scalar, n, x, c0)
        - optical_ricci_scalar_1d(n, x, c0)
    )
    return residual == 0


def potential_map_has_required_limit(candidate: PotentialMapCandidate) -> bool:
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    lam = sp.symbols("lambda", positive=True)
    potential = sp.Function("U")(x)
    scaled = lam * potential
    index = 1 / (1 + candidate.index_coefficient * scaled / c0**2)
    dilaton_coefficient = sp.simplify(
        sp.limit(sp.log(index) / lam, lam, 0, dir="+")
    )
    acceleration = sp.simplify(
        c0**2
        * sp.diff(index, x)
        / (candidate.geodesic_denominator * index**3)
    )
    acceleration_coefficient = sp.simplify(
        sp.limit(acceleration / lam, lam, 0, dir="+")
    )
    return (
        sp.simplify(dilaton_coefficient + 2 * potential / c0**2) == 0
        and sp.simplify(acceleration_coefficient + sp.diff(potential, x)) == 0
    )


def run() -> int:
    geometry_checks = CheckLedger("C-OG-001")
    potential_checks = CheckLedger("C-OG-002")
    x = sp.symbols("x", real=True)
    c0 = sp.symbols("c0", positive=True)
    n = sp.Function("n", positive=True)(x)

    metric = optical_metric_1d(n, c0)
    geometry_checks.check(
        "the declared optical metric has constant determinant -1/c0^2",
        sp.simplify(metric.det() + 1 / c0**2) == 0,
    )
    box_dilaton = optical_box_static_1d(optical_dilaton(n), n, x, c0)
    curvature = optical_ricci_scalar_1d(n, x, c0)
    geometry_checks.check(
        "the static volume-form wave operator yields the canonical closed form",
        sp.simplify(
            box_dilaton
            - c0**2
            * (n * sp.diff(n, x, 2) - 2 * sp.diff(n, x) ** 2)
            / n**3
        )
        == 0,
    )
    geometry_checks.check(
        "Box_g(log(n)) equals the optical Ricci scalar for arbitrary n(x)",
        sp.simplify(box_dilaton - curvature) == 0,
    )

    index_symbol = sp.symbols("N", positive=True)
    first_derivative, second_derivative = sp.symbols("f1 f2", real=True)
    box_npp_coefficient = c0**2 * first_derivative / index_symbol
    box_np2_coefficient = c0**2 * (
        second_derivative / index_symbol
        - first_derivative / index_symbol**2
    )
    curvature_npp_coefficient = c0**2 / index_symbol**2
    curvature_np2_coefficient = -2 * c0**2 / index_symbol**3
    solution = sp.solve(
        (
            sp.Eq(box_npp_coefficient, curvature_npp_coefficient),
            sp.Eq(box_np2_coefficient, curvature_np2_coefficient),
        ),
        (first_derivative, second_derivative),
        dict=True,
    )[0]
    geometry_checks.check(
        "arbitrary-profile n-double-prime matching forces f'(n)=1/n",
        sp.simplify(solution[first_derivative] - 1 / index_symbol) == 0,
    )
    geometry_checks.check(
        "n-prime-squared matching consistently forces f''(n)=-1/n^2",
        sp.simplify(solution[second_derivative] + 1 / index_symbol**2) == 0,
    )
    integrated = sp.integrate(solution[first_derivative], index_symbol)
    geometry_checks.check(
        "integrating the forced derivative gives log(n) up to a constant",
        sp.simplify(integrated - sp.log(index_symbol)) == 0,
    )
    geometry_checks.check(
        "an arbitrary additive dilaton constant leaves the identity invariant",
        sp.simplify(
            optical_box_static_1d(sp.log(n) + sp.symbols("C"), n, x, c0)
            - curvature
        )
        == 0,
    )
    geometry_checks.mutation_sensitive(
        "general-composition scale and nonlogarithmic contamination",
        dilaton_candidate_is_general_solution,
        DilatonCandidate(log_scale=1, linear_scale=0),
        [
            DilatonCandidate(log_scale=2, linear_scale=0),
            DilatonCandidate(log_scale=-1, linear_scale=0),
            DilatonCandidate(log_scale=1, linear_scale=1),
        ],
    )

    potential = sp.Function("Phi")(x)
    tf_index = index_from_potential(potential, c0)
    conditional_dilaton = sp.simplify(optical_dilaton(tf_index))
    potential_checks.check(
        "the conditional dilaton is exactly log(1/(1+2*Phi/c0^2))",
        conditional_dilaton == sp.log(1 / (1 + 2 * potential / c0**2)),
    )
    lam = sp.symbols("lambda", positive=True)
    profile = sp.Function("U")(x)
    scaled_dilaton = optical_dilaton(index_from_potential(lam * profile, c0))
    potential_checks.check(
        "the weak-field dilaton coefficient is exactly -2*U/c0^2",
        sp.simplify(
            sp.limit(scaled_dilaton / lam, lam, 0, dir="+")
            + 2 * profile / c0**2
        )
        == 0,
    )
    exact_acceleration = slow_geodesic_acceleration_from_potential(
        potential, x, c0
    )
    potential_checks.check(
        "the exact conditional drift is -(1+2*Phi/c0^2)*Phi_x",
        sp.simplify(
            exact_acceleration
            + (1 + 2 * potential / c0**2) * sp.diff(potential, x)
        )
        == 0,
    )
    scaled_acceleration = slow_geodesic_acceleration_from_potential(
        lam * profile, x, c0
    )
    potential_checks.check(
        "the scaled weak-field acceleration tends to -U_x",
        sp.simplify(
            sp.limit(scaled_acceleration / lam, lam, 0, dir="+")
            + sp.diff(profile, x)
        )
        == 0,
    )
    potential_checks.mutation_sensitive(
        "TF coefficient, sign, and geodesic normalization",
        potential_map_has_required_limit,
        PotentialMapCandidate(index_coefficient=2, geodesic_denominator=2),
        [
            PotentialMapCandidate(index_coefficient=1, geodesic_denominator=2),
            PotentialMapCandidate(index_coefficient=-2, geodesic_denominator=2),
            PotentialMapCandidate(index_coefficient=2, geodesic_denominator=1),
        ],
    )

    geometry_total = geometry_checks.finish()
    potential_total = potential_checks.finish()
    print(f"P004 ALL {geometry_total + potential_total} CHECKS PASS")
    return geometry_total + potential_total


if __name__ == "__main__":
    run()
