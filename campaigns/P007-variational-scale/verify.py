#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for P007's three proposed claims."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.collective_dynamics import (
    optical_collective_acceleration,
    optical_collective_lagrangian,
    slow_optical_collective_acceleration,
    virial_scaling_exponents,
)
from substrate_framework.optical_geometry import slow_geodesic_acceleration_1d
from substrate_framework.variational import (
    euler_lagrange_expression,
    solve_euler_lagrange_acceleration,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class MultiplierCandidate:
    coordinate_power: int
    time_power: int


def multiplier_preserves_euler_factor(candidate: MultiplierCandidate) -> bool:
    time = sp.symbols("t", real=True)
    scale = sp.symbols("A", nonzero=True)
    coordinate = sp.Function("q", real=True)(time)
    potential = sp.Function("V")(coordinate)
    base = sp.diff(coordinate, time) ** 2 / 2 - potential
    multiplier = (
        scale
        * coordinate ** candidate.coordinate_power
        * (1 + time) ** candidate.time_power
    )
    return sp.simplify(
        euler_lagrange_expression(multiplier * base, coordinate, time)
        - multiplier * euler_lagrange_expression(base, coordinate, time)
    ) == 0


@dataclass(frozen=True)
class VirialTarget:
    width_slope: sp.Rational
    energy_slope: sp.Rational


def target_selects_option_c(target: VirialTarget) -> bool:
    quadratic, quartic = sp.symbols("a b", real=True)
    width, energy = virial_scaling_exponents(quadratic, quartic)
    solution = sp.solve(
        [
            sp.Eq(width, target.width_slope),
            sp.Eq(energy, target.energy_slope),
        ],
        [quadratic, quartic],
        dict=True,
    )
    return solution == [{quadratic: 0, quartic: 1}]


def run() -> int:
    variational_checks = CheckLedger("C-VAR-001")
    collective_checks = CheckLedger("C-CC-001")
    virial_checks = CheckLedger("C-VIR-001")

    time = sp.symbols("t", real=True)
    coordinate = sp.Function("q", real=True)(time)
    velocity = sp.diff(coordinate, time)
    fixed_scale = sp.symbols("A", nonzero=True)
    generic = sp.Function("ell")(coordinate, velocity, time)
    variational_checks.check(
        "an arbitrary fixed scale factors through the Euler-Lagrange operator",
        sp.simplify(
            euler_lagrange_expression(
                fixed_scale * generic, coordinate, time
            )
            - fixed_scale
            * euler_lagrange_expression(generic, coordinate, time)
        )
        == 0,
    )
    variational_checks.check(
        "a uniform scale squared also cancels, so degree one is not necessary",
        sp.simplify(
            euler_lagrange_expression(
                fixed_scale**2 * generic, coordinate, time
            )
            - fixed_scale**2
            * euler_lagrange_expression(generic, coordinate, time)
        )
        == 0,
    )
    variational_checks.check(
        "the zero multiplier is excluded because it annihilates every equation",
        euler_lagrange_expression(0 * generic, coordinate, time) == 0,
    )
    variational_checks.mutation_sensitive(
        "the multiplier must be path and time independent",
        multiplier_preserves_euler_factor,
        MultiplierCandidate(0, 0),
        [MultiplierCandidate(1, 0), MultiplierCandidate(0, 1)],
    )

    signal_speed, energy_scale = sp.symbols("c0 E0", positive=True)
    index_function = sp.Function("n", positive=True)
    index = index_function(coordinate)
    collective_lagrangian = optical_collective_lagrangian(
        coordinate,
        time,
        index,
        signal_speed,
        energy_scale,
    )
    metric_line_element = (
        1 / index - index * velocity**2 / signal_speed**2
    )
    collective_checks.check(
        "the declared action is the timelike line element of C-OG-001",
        sp.simplify(
            collective_lagrangian**2 / energy_scale**2
            - metric_line_element
        )
        == 0,
    )
    solved_acceleration = solve_euler_lagrange_acceleration(
        collective_lagrangian, coordinate, time
    )
    expected_acceleration = optical_collective_acceleration(
        coordinate, time, index, signal_speed
    )
    collective_checks.check(
        "solving the declared action gives the exact full acceleration",
        sp.simplify(solved_acceleration - expected_acceleration) == 0,
    )
    collective_checks.check(
        "the full acceleration removes only E0 and retains the index profile",
        energy_scale not in solved_acceleration.free_symbols
        and index in solved_acceleration.atoms(sp.Function)
        and sp.Derivative(index, coordinate)
        in solved_acceleration.atoms(sp.Derivative),
    )
    slow_acceleration = sp.simplify(solved_acceleration.subs(velocity, 0))
    collective_checks.check(
        "the exact zero-velocity limit matches the accepted optical drift",
        sp.simplify(
            slow_acceleration
            - slow_optical_collective_acceleration(
                coordinate, index, signal_speed
            )
        )
        == 0
        and sp.simplify(
            slow_acceleration
            - slow_geodesic_acceleration_1d(
                index, coordinate, signal_speed
            )
        )
        == 0,
    )
    collective_checks.check(
        "same initial data have an E0-independent local IVP vector field",
        energy_scale not in expected_acceleration.free_symbols,
    )

    wrong_lagrangian = -energy_scale / sp.sqrt(index) * sp.sqrt(
        1 - index**2 * velocity**2 / (energy_scale * signal_speed**2)
    )
    rescaling = sp.symbols("k", positive=True)
    collective_checks.check(
        "the source mixed-scale counterexample is not uniformly homogeneous",
        sp.simplify(
            wrong_lagrangian.subs(energy_scale, rescaling * energy_scale)
            - rescaling * wrong_lagrangian
        )
        != 0
        and sp.simplify(
            wrong_lagrangian.subs(energy_scale, rescaling * energy_scale)
            - rescaling**2 * wrong_lagrangian
        )
        != 0,
    )
    wrong_acceleration = solve_euler_lagrange_acceleration(
        wrong_lagrangian, coordinate, time
    )
    collective_checks.check(
        "the same EL solve retains E0 for the mixed-scale counterexample",
        energy_scale in wrong_acceleration.free_symbols,
    )
    alpha = sp.symbols("alpha", positive=True)
    wrong_initial = sp.simplify(
        wrong_acceleration
        .subs(sp.Derivative(index, coordinate), alpha)
        .subs(index, 1 + alpha * coordinate)
        .subs(velocity, 0)
        .subs(coordinate, 0)
    )
    collective_checks.check(
        "the mixed-scale model has exact E0-dependent initial acceleration",
        sp.simplify(
            wrong_initial
            - energy_scale * signal_speed**2 * alpha / 2
        )
        == 0
        and sp.simplify(
            wrong_initial.subs(energy_scale, 2)
            - wrong_initial.subs(energy_scale, 1)
        )
        == signal_speed**2 * alpha / 2,
    )
    collective_checks.check(
        "the kinetic-index exponent is load-bearing in the full acceleration",
        sp.simplify(
            solved_acceleration
            - (
                signal_speed**2 - index**2 * velocity**2
            )
            * sp.diff(index, coordinate)
            / (2 * index**3)
        )
        != 0,
    )

    quadratic, quartic = sp.symbols("a b", real=True)
    width_slope, energy_slope = virial_scaling_exponents(
        quadratic, quartic
    )
    virial_checks.check(
        "the simultaneous half-slope equations uniquely select (a,b)=(0,1)",
        sp.solve(
            [
                sp.Eq(width_slope, -sp.Rational(1, 2)),
                sp.Eq(energy_slope, -sp.Rational(1, 2)),
            ],
            [quadratic, quartic],
            dict=True,
        )
        == [{quadratic: 0, quartic: 1}],
    )
    virial_checks.check(
        "Options A and B fail different halves of the declared predicate",
        virial_scaling_exponents(1, 0)
        == (sp.Rational(1, 2), sp.Rational(-1, 2))
        and virial_scaling_exponents(1, 1) == (0, -1),
    )
    virial_checks.mutation_sensitive(
        "both target slopes are load-bearing",
        target_selects_option_c,
        VirialTarget(
            sp.Rational(-1, 2), sp.Rational(-1, 2)
        ),
        [
            VirialTarget(sp.Rational(1, 2), sp.Rational(-1, 2)),
            VirialTarget(sp.Rational(-1, 2), sp.Rational(-1, 1)),
        ],
    )

    variational_total = variational_checks.finish()
    collective_total = collective_checks.finish()
    virial_total = virial_checks.finish()
    total = variational_total + collective_total + virial_total
    print(f"P007 ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
