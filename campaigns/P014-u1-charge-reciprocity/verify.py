#!/usr/bin/env python3
"""Exact, mutation-sensitive verifier for proposed C-U1-001/C-U1-002."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.sine_gordon import (
    boosted_breather_energy_momentum,
    boosted_breather_phase_components,
)
from substrate_framework.u1_charge import (
    breather_charge_energy_product,
    breather_charge_secant_product,
    breather_parameterized_u1_charge,
    charge_scale_exponent_matrix,
    minkowski_dalembertian,
    sech_profile_u1_charge,
    stationary_phase_field,
    stationary_u1_charge_density,
    u1_current_components,
    u1_current_divergence,
)
from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class CurrentCandidate:
    time_coefficient: int
    space_coefficient: int


def current_candidate_is_exact(candidate: CurrentCandidate) -> bool:
    x, t = sp.symbols("x t", real=True)
    real = sp.Function("R", real=True)(x, t)
    imaginary = sp.Function("I", real=True)(x, t)
    field = real + sp.I * imaginary
    conjugate = real - sp.I * imaginary
    density = candidate.time_coefficient * sp.I * (
        conjugate * sp.diff(field, t) - field * sp.diff(conjugate, t)
    )
    flux = candidate.space_coefficient * sp.I * (
        conjugate * sp.diff(field, x) - field * sp.diff(conjugate, x)
    )
    divergence = sp.expand(sp.diff(density, t) + sp.diff(flux, x))
    reduced = sp.expand(
        sp.I
        * (
            conjugate * minkowski_dalembertian(field, x, t)
            - field * minkowski_dalembertian(conjugate, x, t)
        )
    )
    omega = sp.symbols("omega", positive=True)
    profile = sp.Function("f", real=True)(x)
    stationary = profile * sp.exp(-sp.I * omega * t)
    stationary_conjugate = profile * sp.exp(sp.I * omega * t)
    stationary_density = sp.simplify(
        candidate.time_coefficient
        * sp.I
        * (
            stationary_conjugate * sp.diff(stationary, t)
            - stationary * sp.diff(stationary_conjugate, t)
        )
    )
    return (
        sp.simplify(divergence - reduced) == 0
        and sp.simplify(stationary_density - 2 * omega * profile**2) == 0
    )


@dataclass(frozen=True)
class ProfileCandidate:
    coefficient: int
    amplitude_power: int
    width_power: int


def profile_candidate_is_exact(candidate: ProfileCandidate) -> bool:
    omega, eta, amplitude = sp.symbols("omega eta A", positive=True)
    charge = (
        candidate.coefficient
        * amplitude**candidate.amplitude_power
        * omega
        / eta**candidate.width_power
    )
    expected = sech_profile_u1_charge(omega, eta, amplitude)
    energy = 16 * eta
    secant = energy / omega
    return (
        sp.simplify(charge - expected) == 0
        and sp.simplify(charge * energy - 64 * amplitude**2 * omega) == 0
        and sp.simplify(charge * secant - 64 * amplitude**2) == 0
    )


@dataclass(frozen=True)
class CompositionCandidate:
    charge_coefficient: int
    energy_coefficient: int
    secant_frequency_power: int


def composition_candidate_is_exact(candidate: CompositionCandidate) -> bool:
    omega, eta, amplitude = sp.symbols("omega eta A", positive=True)
    charge = candidate.charge_coefficient * amplitude**2 * omega / eta
    energy = candidate.energy_coefficient * eta
    secant = energy / omega**candidate.secant_frequency_power
    return (
        sp.simplify(charge * energy - 64 * amplitude**2 * omega) == 0
        and sp.simplify(charge * secant - 64 * amplitude**2) == 0
    )


def run() -> int:
    current_checks = CheckLedger("C-U1-001")
    profile_checks = CheckLedger("C-U1-002")
    x, t = sp.symbols("x t", real=True)
    real = sp.Function("R", real=True)(x, t)
    imaginary = sp.Function("I", real=True)(x, t)
    field = real + sp.I * imaginary
    conjugate = real - sp.I * imaginary

    density, flux = u1_current_components(field, conjugate, x, t)
    divergence = u1_current_divergence(field, conjugate, x, t)
    reduced = sp.I * (
        conjugate * minkowski_dalembertian(field, x, t)
        - field * minkowski_dalembertian(conjugate, x, t)
    )
    current_checks.check(
        "the arbitrary-field current divergence reduces to the d'Alembertian identity",
        sp.simplify(divergence - reduced) == 0,
    )
    current_checks.check(
        "the raised spatial component carries the signature minus sign",
        sp.simplify(
            flux
            + sp.I
            * (
                conjugate * sp.diff(field, x)
                - field * sp.diff(conjugate, x)
            )
        )
        == 0,
    )

    restoring = sp.Function("F", real=True)(real**2 + imaginary**2)
    on_shell = sp.simplify(
        sp.I
        * (
            conjugate * restoring * field
            - field * restoring * conjugate
        )
    )
    current_checks.check(
        "a real phase-independent restoring coefficient conserves the current on shell",
        on_shell == 0,
    )
    complex_coefficient = sp.I
    complex_divergence = sp.simplify(
        sp.I
        * (
            conjugate * complex_coefficient * field
            - field * sp.conjugate(complex_coefficient) * conjugate
        )
    )
    current_checks.check(
        "a complex restoring coefficient fails the real-coefficient cancellation",
        complex_divergence != 0,
    )

    real_field = sp.Function("rho", real=True)(x, t)
    real_density, real_flux = u1_current_components(
        real_field, real_field, x, t
    )
    current_checks.check(
        "a genuinely real field has identically zero U1 current",
        real_density == 0 and real_flux == 0,
    )

    omega = sp.symbols("omega", positive=True)
    profile = sp.Function("f", real=True)(x)
    stationary = stationary_phase_field(profile, t, omega)
    stationary_conjugate = profile * sp.exp(sp.I * omega * t)
    stationary_density, stationary_flux = u1_current_components(
        stationary, stationary_conjugate, x, t
    )
    current_checks.check(
        "the stationary phase ansatz has density 2*omega*f^2 and zero flux",
        sp.simplify(
            stationary_density - stationary_u1_charge_density(profile, omega)
        )
        == 0
        and stationary_flux == 0,
    )
    current_checks.check(
        "stationary continuity is kinematic and does not substitute for the general theorem",
        sp.simplify(
            sp.diff(stationary_density, t) + sp.diff(stationary_flux, x)
        )
        == 0
        and divergence != 0,
    )

    coupling = sp.symbols("lambda", real=True, nonzero=True)
    broken_divergence = sp.simplify(
        sp.I
        * (
            stationary_conjugate
            * (restoring * stationary + coupling * stationary_conjugate)
            - stationary
            * (restoring * stationary_conjugate + coupling * stationary)
        )
    )
    expected_broken = -2 * coupling * profile**2 * sp.sin(2 * omega * t)
    current_checks.check(
        "a phase-breaking conjugate-field term produces the exact nonzero leakage",
        sp.simplify(broken_divergence - expected_broken) == 0
        and sp.simplify(expected_broken.subs(coupling, 0)) == 0
        and sp.simplify(expected_broken.subs(coupling, 1)) != 0,
    )
    current_checks.mutation_sensitive(
        "current normalization and raised spatial sign",
        current_candidate_is_exact,
        CurrentCandidate(1, -1),
        [
            CurrentCandidate(-1, -1),
            CurrentCandidate(2, -1),
            CurrentCandidate(1, 1),
            CurrentCandidate(-1, 1),
        ],
    )

    amplitude, eta = sp.symbols("A eta", positive=True)
    integral = sp.integrate(
        amplitude**2 / sp.cosh(eta * x) ** 2,
        (x, -sp.oo, sp.oo),
    )
    profile_checks.check(
        "the declared sech-squared profile has exact norm 2*A^2/eta",
        sp.simplify(integral - 2 * amplitude**2 / eta) == 0,
    )
    integrated_charge = sp.simplify(2 * omega * integral)
    profile_checks.check(
        "integrating the canonical density yields 4*A^2*omega/eta",
        sp.simplify(
            integrated_charge - sech_profile_u1_charge(omega, eta, amplitude)
        )
        == 0,
    )

    breather_eta = sp.sqrt(1 - omega**2)
    charge = breather_parameterized_u1_charge(omega, amplitude)
    profile_checks.check(
        "the shared breather parameterization retains the declared amplitude",
        sp.simplify(charge - 4 * amplitude**2 * omega / breather_eta) == 0,
    )
    profile_checks.check(
        "the charge is strictly increasing by an exact positive derivative on the open domain",
        sp.simplify(
            sp.diff(charge, omega)
            - 4 * amplitude**2 / (1 - omega**2) ** sp.Rational(3, 2)
        )
        == 0,
    )
    profile_checks.check(
        "the one-sided charge limits are zero and infinite in magnitude",
        sp.limit(charge, omega, 0, "+") == 0
        and sp.limit(sp.Abs(charge), omega, 1, "-") == sp.oo,
    )
    profile_checks.check(
        "composition with accepted breather energy gives Q*E=64*A^2*omega",
        sp.simplify(
            breather_charge_energy_product(omega, amplitude)
            - 64 * amplitude**2 * omega
        )
        == 0,
    )
    product = breather_charge_secant_product(omega, amplitude)
    profile_checks.check(
        "composition with the accepted secant scale gives Q*H=64*A^2",
        sp.simplify(product - 64 * amplitude**2) == 0
        and sp.diff(product, omega) == 0,
    )
    profile_checks.check(
        "the logarithmic charge and secant drifts cancel exactly",
        sp.simplify(
            sp.diff(sp.log(charge), omega)
            + sp.diff(
                sp.log(16 * breather_eta / omega),
                omega,
            )
        )
        == 0,
    )

    velocity = sp.symbols("v", real=True)
    phase = boosted_breather_phase_components(omega, velocity)
    energy_momentum = boosted_breather_energy_momentum(omega, velocity)
    profile_checks.check(
        "conditional boosted vector composition is division-free in every frame",
        all(
            sp.simplify(charge * component - 64 * amplitude**2 * phase_component)
            == 0
            for component, phase_component in zip(energy_momentum, phase)
        ),
    )
    rest_phase = boosted_breather_phase_components(omega, 0)
    rest_energy_momentum = boosted_breather_energy_momentum(omega, 0)
    profile_checks.check(
        "the charge-weighted vector relation remains regular at rest",
        all(
            sp.simplify(charge * component - 64 * amplitude**2 * phase_component)
            == 0
            for component, phase_component in zip(
                rest_energy_momentum, rest_phase
            )
        ),
    )

    exponent_matrix = charge_scale_exponent_matrix()
    generator_charge_secant = sp.Matrix([1, 1, 0, 0])
    generator_charge_energy = sp.Matrix([1, 0, 1, -1])
    frequency_power, width_power = sp.symbols("p q", integer=True)
    logarithmic_derivative_numerator = sp.Poly(
        frequency_power - (frequency_power + width_power) * omega**2,
        omega,
    )
    coefficient_solution = sp.solve(
        logarithmic_derivative_numerator.all_coeffs(),
        [frequency_power, width_power],
        dict=True,
    )
    profile_checks.check(
        "a power omega^p*eta^q is constant on the whole family only when p=q=0",
        coefficient_solution
        == [{frequency_power: 0, width_power: 0}],
    )
    profile_checks.check(
        "the frequency-width exponent matrix has rank two and a rank-two kernel",
        exponent_matrix.rank() == 2
        and len(exponent_matrix.nullspace()) == 2,
    )
    profile_checks.check(
        "Q*H and Q*E/omega are independent generators of the exponent kernel",
        exponent_matrix * generator_charge_secant == sp.zeros(2, 1)
        and exponent_matrix * generator_charge_energy == sp.zeros(2, 1)
        and sp.Matrix.hstack(
            generator_charge_secant, generator_charge_energy
        ).rank()
        == 2,
    )
    a, b = sp.symbols("a b", integer=True)
    general_kernel_member = sp.Matrix([a, b, a - b, b - a])
    recombination = (
        b * generator_charge_secant
        + (a - b) * generator_charge_energy
    )
    profile_checks.check(
        "the closed-form integer solution proves the monomial classification exhaustive",
        exponent_matrix * general_kernel_member == sp.zeros(2, 1)
        and sp.simplify(general_kernel_member - recombination)
        == sp.zeros(4, 1),
    )
    profile_checks.check(
        "the two named generators differ only by the defining identity H=E/omega",
        generator_charge_energy - generator_charge_secant
        == sp.Matrix([0, -1, 1, -1]),
    )
    profile_checks.mutation_sensitive(
        "profile coefficient, amplitude power, and width power",
        profile_candidate_is_exact,
        ProfileCandidate(4, 2, 1),
        [
            ProfileCandidate(2, 2, 1),
            ProfileCandidate(4, 1, 1),
            ProfileCandidate(4, 2, 2),
        ],
    )
    profile_checks.mutation_sensitive(
        "charge, energy, and secant normalizations",
        composition_candidate_is_exact,
        CompositionCandidate(4, 16, 1),
        [
            CompositionCandidate(2, 16, 1),
            CompositionCandidate(4, 8, 1),
            CompositionCandidate(4, 16, 2),
        ],
    )

    current_total = current_checks.finish()
    profile_total = profile_checks.finish()
    print(f"P014 ALL {current_total + profile_total} CHECKS PASS")
    return current_total + profile_total


if __name__ == "__main__":
    run()
