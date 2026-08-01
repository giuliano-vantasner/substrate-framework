#!/usr/bin/env python3
"""Verify P049's canonical light-cone stress theorem and audit NC2."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.governance import load_yaml
from substrate_framework.sine_gordon import (
    hamiltonian_density,
    light_cone_derivatives,
    naive_chiral_currents,
    sine_gordon_lagrangian_density,
    sine_gordon_light_cone_stress_balances,
    sine_gordon_light_cone_stress_components,
    sine_gordon_potential,
    sine_gordon_residual,
    sine_gordon_stress_divergence,
    sine_gordon_stress_tensor_contravariant,
    sine_gordon_stress_tensor_covariant,
    sine_gordon_stress_trace,
    spatial_parity_transform,
    static_kink_field,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "6854fafe62ef7c8bfcf558573e3c89fec0d2144cb9a39df2e2ecb6d66d960136"
)


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P049-NC2")

    source_bytes = args.source_file.read_bytes()
    reproduction = load_yaml(args.source_reproduction)
    ledger.check(
        "the audited NC2 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    ledger.check(
        "the predecessor executable exits successfully with all seven checks",
        reproduction.get("sha256") == EXPECTED_SOURCE_SHA256
        and reproduction.get("exit_code") == 0
        and reproduction.get("terminal_tally") == "ALL 7 CHECKS PASS",
    )

    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    field_t = sp.diff(field, t)
    field_x = sp.diff(field, x)
    current_plus, current_minus = naive_chiral_currents(field, x, t)
    residual = sine_gordon_residual(field, x, t)
    potential = sine_gordon_potential(field)

    plus, minus = light_cone_derivatives(field, x, t)
    ledger.check(
        "the half-normalized light-cone operators invert to Cartesian derivatives",
        sp.simplify(plus + minus - field_t) == 0
        and sp.simplify(plus - minus - field_x) == 0,
    )
    generic = sp.Function("F")(x, t)
    generic_plus, _generic_minus = light_cone_derivatives(generic, x, t)
    _mixed_plus, mixed_minus = light_cone_derivatives(generic_plus, x, t)
    ledger.check(
        "four partial-plus partial-minus equals the Cartesian wave operator",
        sp.simplify(
            4 * mixed_minus
            - sp.diff(generic, t, 2)
            + sp.diff(generic, x, 2)
        )
        == 0,
    )

    def derivative_scale_predicate(candidate: object) -> bool:
        scale = sp.sympify(candidate)
        candidate_plus = scale * (sp.diff(generic, t) + sp.diff(generic, x))
        candidate_minus = scale * (sp.diff(generic, t) - sp.diff(generic, x))
        return bool(
            sp.simplify(candidate_plus + candidate_minus - sp.diff(generic, t))
            == 0
            and sp.simplify(candidate_plus - candidate_minus - sp.diff(generic, x))
            == 0
        )

    ledger.mutation_sensitive(
        "light-cone derivative Jacobian scale",
        derivative_scale_predicate,
        sp.Rational(1, 2),
        [1, sp.Rational(1, 4)],
    )

    lagrangian = sine_gordon_lagrangian_density(field, x, t)
    covariant = sine_gordon_stress_tensor_covariant(field, x, t)
    contravariant = sine_gordon_stress_tensor_contravariant(field, x, t)
    metric = sp.diag(1, -1)
    gradient = sp.Matrix([field_t, field_x])
    ledger.check(
        "the canonical covariant tensor derives from the scalar Lagrangian and metric",
        matrix_zero(covariant - (gradient * gradient.T - metric * lagrangian)),
    )
    ledger.check(
        "raising both indices flips only the symmetric mixed components",
        matrix_zero(contravariant - metric * covariant * metric)
        and contravariant[0, 1] == -covariant[0, 1]
        and contravariant[1, 0] == -covariant[1, 0],
    )
    ledger.check(
        "the canonical energy density is exactly the accepted Hamiltonian density",
        sp.simplify(covariant[0, 0] - hamiltonian_density(field, x, t)) == 0,
    )

    divergence = sine_gordon_stress_divergence(field, x, t)
    expected_divergence = sp.Matrix([field_t * residual, -field_x * residual])
    ledger.check(
        "the full Cartesian divergence factorizes off shell by the SG residual",
        matrix_zero(divergence - expected_divergence),
    )

    def raised_mixed_sign_predicate(candidate: object) -> bool:
        sign = sp.sympify(candidate)
        energy = hamiltonian_density(field, x, t)
        candidate_flux = sign * field_t * field_x
        divergence_zero = sp.diff(energy, t) + sp.diff(candidate_flux, x)
        return bool(sp.simplify(divergence_zero - field_t * residual) == 0)

    ledger.mutation_sensitive(
        "raised mixed-component sign",
        raised_mixed_sign_predicate,
        -1,
        [0, 1],
    )

    plus_plus, minus_minus, plus_minus = sine_gordon_light_cone_stress_components(
        field,
        x,
        t,
    )
    ledger.check(
        "the Cartesian-to-null Jacobian fixes all three canonical covariant components",
        sp.simplify(plus_plus - current_plus**2 / 4) == 0
        and sp.simplify(minus_minus - current_minus**2 / 4) == 0
        and sp.simplify(plus_minus - potential / 2) == 0,
    )
    balances = sine_gordon_light_cone_stress_balances(field, x, t)
    ledger.check(
        "both null stress balances factorize off shell by the SG residual",
        sp.simplify(balances[0] - current_plus * residual / 4) == 0
        and sp.simplify(balances[1] - current_minus * residual / 4) == 0,
    )

    def mixed_component_coefficient_predicate(candidate: object) -> bool:
        coefficient = sp.sympify(candidate)
        candidate_mixed = coefficient * potential
        _pp_plus, pp_minus = light_cone_derivatives(plus_plus, x, t)
        mixed_plus, _mixed_minus = light_cone_derivatives(candidate_mixed, x, t)
        return bool(
            sp.simplify(pp_minus + mixed_plus - current_plus * residual / 4)
            == 0
        )

    ledger.mutation_sensitive(
        "canonical mixed null-stress coefficient",
        mixed_component_coefficient_predicate,
        sp.Rational(1, 2),
        [0, 1, -sp.Rational(1, 2)],
    )

    def balance_sign_predicate(candidate: object) -> bool:
        sign = sp.sympify(candidate)
        _pp_plus, pp_minus = light_cone_derivatives(plus_plus, x, t)
        mixed_plus, _mixed_minus = light_cone_derivatives(plus_minus, x, t)
        return bool(
            sp.simplify(
                pp_minus + sign * mixed_plus - current_plus * residual / 4
            )
            == 0
        )

    ledger.mutation_sensitive(
        "potential-gradient balance sign",
        balance_sign_predicate,
        1,
        [0, -1],
    )

    ledger.check(
        "the canonical trace and mixed null component encode the same potential",
        sp.simplify(sine_gordon_stress_trace(field, x, t) - 2 * potential) == 0
        and sp.simplify(sine_gordon_stress_trace(field, x, t) - 4 * plus_minus)
        == 0,
    )

    source_plus_plus = plus**2 / 2
    source_minus_minus = minus**2 / 2
    source_theta = (sp.cos(field) - 1) / 4
    ledger.check(
        "NC2's named null stresses and Theta are uniformly half the canonical balance",
        sp.simplify(source_plus_plus - plus_plus / 2) == 0
        and sp.simplify(source_minus_minus - minus_minus / 2) == 0
        and sp.simplify(source_theta + plus_minus / 2) == 0
        and sp.simplify(source_theta + sine_gordon_stress_trace(field, x, t) / 8)
        == 0,
    )

    def source_to_canonical_scale_predicate(candidate: object) -> bool:
        scale = sp.sympify(candidate)
        return bool(
            sp.simplify(scale * source_plus_plus - plus_plus) == 0
            and sp.simplify(-scale * source_theta - plus_minus) == 0
        )

    ledger.mutation_sensitive(
        "NC2 auxiliary-to-canonical normalization",
        source_to_canonical_scale_predicate,
        2,
        [1, 4],
    )

    source_claimed_energy = source_plus_plus + source_minus_minus + potential
    correct_energy_from_source = 2 * (source_plus_plus + source_minus_minus) + potential
    ledger.check(
        "NC2's printed source-component energy bridge misses a kinetic factor two",
        sp.simplify(source_claimed_energy - hamiltonian_density(field, x, t))
        != 0
        and sp.simplify(correct_energy_from_source - hamiltonian_density(field, x, t))
        == 0,
    )

    parity_field = spatial_parity_transform(field, x)
    parity_components = sine_gordon_light_cone_stress_components(parity_field, x, t)
    reflected_components = tuple(
        component.subs(x, -x)
        for component in sine_gordon_light_cone_stress_components(field, x, t)
    )
    ledger.check(
        "spatial parity exchanges the two null stresses and leaves the mixed component even",
        sp.simplify(parity_components[0] - reflected_components[1]) == 0
        and sp.simplify(parity_components[1] - reflected_components[0]) == 0
        and sp.simplify(parity_components[2] - reflected_components[2]) == 0,
    )

    kink = static_kink_field(x)
    kink_tensor = sine_gordon_stress_tensor_covariant(kink, x, t)
    ledger.check(
        "the exact static kink has positive energy and zero longitudinal pressure",
        sp.simplify(kink_tensor[1, 1]) == 0
        and sp.simplify(kink_tensor[0, 0] - 2 * sine_gordon_potential(kink)) == 0,
    )

    u, v = sp.symbols("u v", real=True)
    free_field = sp.Function("free_phi")(u, v)
    free_mixed = sp.diff(free_field, u, v)
    free_plus_stress = sp.diff(free_field, u) ** 2
    free_minus_stress = sp.diff(free_field, v) ** 2
    ledger.check(
        "deleting the potential gives a separate massless model with conserved null stresses",
        sp.simplify(
            sp.diff(free_plus_stress, v).subs(free_mixed, 0)
        )
        == 0
        and sp.simplify(
            sp.diff(free_minus_stress, u).subs(free_mixed, 0)
        )
        == 0,
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
