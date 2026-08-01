#!/usr/bin/env python3
"""Exact and mutation-sensitive verifier for P001 claims C-SG-001/002."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import sympy as sp
from scipy.integrate import quad

from substrate_framework.sine_gordon import (
    breather_energy,
    breather_field,
    breather_field_with_width,
    breather_inverse_width,
    breather_peak_amplitude,
    breather_period,
    hamiltonian_density,
    sine_gordon_residual,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class FieldCandidate:
    coefficient: int
    width_sign: int
    potential_sign: int


def candidate_probe_is_on_shell(candidate: FieldCandidate) -> bool:
    """Test a scientifically meaningful exact point for mutation sensitivity."""

    x, t, omega = sp.symbols("x t omega", real=True)
    eta = sp.sqrt(1 - candidate.width_sign * omega**2)
    field = candidate.coefficient * sp.atan(
        eta * sp.sin(omega * t) / (omega * sp.cosh(eta * x))
    )
    residual = (
        sp.diff(field, t, 2)
        - sp.diff(field, x, 2)
        + candidate.potential_sign * sp.sin(field)
    )
    probe = residual.subs(
        {omega: sp.Rational(3, 5), x: 0, t: 5 * sp.pi / 6}
    )
    return sp.simplify(probe) == 0


def numerical_energy(
    density: object,
    x: sp.Symbol,
    t: sp.Symbol,
    omega: sp.Symbol,
    frequency: float,
    phase_fraction: float,
    domain_widths: float,
) -> tuple[float, float]:
    """Integrate the full Hamiltonian density on a finite refined domain."""

    density_fn = sp.lambdify((x, t, omega), density, modules="numpy")
    eta = float(np.sqrt(1.0 - frequency**2))
    period = 2.0 * np.pi / frequency
    time = phase_fraction * period
    bound = domain_widths / eta
    value, error = quad(
        lambda coordinate: float(density_fn(coordinate, time, frequency)),
        -bound,
        bound,
        epsabs=1.0e-11,
        epsrel=1.0e-11,
        limit=300,
    )
    return float(value), float(error)


def run() -> int:
    solution_checks = CheckLedger("C-SG-001")
    energy_checks = CheckLedger("C-SG-002")

    x, t = sp.symbols("x t", real=True)
    omega = sp.symbols("omega", positive=True)
    eta = sp.symbols("eta", positive=True)

    field = breather_field(x, t, omega)
    residual = sp.simplify(sine_gordon_residual(field, x, t))
    solution_checks.check(
        "direct breather has identically zero sine-Gordon residual",
        residual == 0,
        "the full symbolic residual did not vanish",
    )

    explicit_width_field = breather_field_with_width(x, t, omega, eta)
    solution_checks.check(
        "explicit-width profile localizes at positive spatial infinity",
        sp.limit(explicit_width_field, x, sp.oo) == 0,
    )
    solution_checks.check(
        "explicit-width profile localizes at negative spatial infinity",
        sp.limit(explicit_width_field, x, -sp.oo) == 0,
    )
    periodic_shift = explicit_width_field.subs(t, t + 2 * sp.pi / omega)
    solution_checks.check(
        "profile is exactly periodic with period 2*pi/omega",
        sp.trigsimp(periodic_shift - explicit_width_field) == 0,
    )
    solution_checks.check(
        "canonical period agrees with the field shift",
        breather_period(sp.Rational(3, 5)) == 10 * sp.pi / 3,
    )
    solution_checks.check(
        "peak field is attained at x=0 and quarter period",
        sp.simplify(
            field.subs(t, sp.pi / (2 * omega)).subs(x, 0)
            - breather_peak_amplitude(omega)
        )
        == 0,
    )
    solution_checks.mutation_sensitive(
        "field equation normalization",
        candidate_probe_is_on_shell,
        FieldCandidate(coefficient=4, width_sign=1, potential_sign=1),
        [
            FieldCandidate(coefficient=3, width_sign=1, potential_sign=1),
            FieldCandidate(coefficient=4, width_sign=-1, potential_sign=1),
            FieldCandidate(coefficient=4, width_sign=1, potential_sign=-1),
        ],
    )

    density_explicit = sp.simplify(
        hamiltonian_density(explicit_width_field, x, t).subs(t, 0)
    )
    target_density = 8 * eta**2 / sp.cosh(eta * x) ** 2
    energy_checks.check(
        "clean time slice derives purely kinetic density 8*eta^2*sech^2",
        sp.simplify(density_explicit - target_density) == 0,
    )
    sech_integral = sp.integrate(
        1 / sp.cosh(eta * x) ** 2, (x, -sp.oo, sp.oo)
    )
    energy_checks.check(
        "positive-width sech-squared line integral is 2/eta",
        sp.simplify(sech_integral - 2 / eta) == 0,
    )
    derived_energy_eta = sp.simplify(8 * eta**2 * sech_integral)
    derived_energy = derived_energy_eta.subs(
        eta, breather_inverse_width(omega)
    )
    energy_checks.check(
        "Hamiltonian integral independently derives the canonical energy",
        sp.simplify(derived_energy - breather_energy(omega)) == 0,
    )
    energy_checks.mutation_sensitive(
        "energy normalization",
        lambda coefficient: sp.simplify(
            coefficient * breather_inverse_width(omega) - derived_energy
        )
        == 0,
        16,
        [15, 32],
    )
    energy_checks.check(
        "omega to zero reaches the kink-antikink threshold 16",
        sp.limit(breather_energy(omega), omega, 0, dir="+") == 16,
    )
    energy_checks.check(
        "omega to one has vanishing breather energy",
        sp.limit(breather_energy(omega), omega, 1, dir="-") == 0,
    )

    full_density = hamiltonian_density(field, x, t)
    numeric_cases = (
        (0.5, 0.17),
        (0.6, 0.31),
        (0.8, 0.43),
    )
    for frequency, phase_fraction in numeric_cases:
        numeric, reported_error = numerical_energy(
            full_density,
            x,
            t,
            omega,
            frequency,
            phase_fraction,
            domain_widths=16.0,
        )
        exact = float(breather_energy(sp.Float(frequency)))
        energy_checks.check(
            f"full-density quadrature conserves energy at omega={frequency}",
            abs(numeric - exact) < 2.0e-10 and reported_error < 2.0e-10,
            f"numeric={numeric:.16g}, exact={exact:.16g}, quad_error={reported_error:.3g}",
        )

    refinement_errors: list[float] = []
    exact_refinement = float(breather_energy(sp.Rational(3, 5)))
    for widths in (6.0, 10.0, 14.0):
        numeric, _ = numerical_energy(
            full_density,
            x,
            t,
            omega,
            frequency=0.6,
            phase_fraction=0.37,
            domain_widths=widths,
        )
        refinement_errors.append(abs(numeric - exact_refinement))
    energy_checks.check(
        "quadrature domain refinement reduces truncation error",
        all(
            fine < coarse
            for coarse, fine in zip(refinement_errors, refinement_errors[1:])
        ),
        f"errors={refinement_errors}",
    )
    energy_checks.check(
        "refined full-density quadrature reaches the exact energy",
        refinement_errors[-1] < 2.0e-10,
        f"errors={refinement_errors}",
    )

    solution_total = solution_checks.finish()
    energy_total = energy_checks.finish()
    print(f"P001 ALL {solution_total + energy_total} CHECKS PASS")
    return solution_total + energy_total


if __name__ == "__main__":
    run()
