#!/usr/bin/env python3
"""Exact convention and implication audit for EM2 local-U(1) algebra."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.abelian_higgs_vortex import quantized_flux
from substrate_framework.gauge_u1 import (
    finite_energy_winding_flux,
    gauged_scalar_kinetic_density,
    local_u1_transform,
    u1_covariant_commutator,
    u1_covariant_derivative,
    u1_field_strength,
    u1_holonomy,
)
from substrate_framework.u1_charge import u1_current_components
from substrate_framework.verification import CheckLedger


EM2_SHA256 = "9787ae25521e19d926de0f9addafd16353bebc149cea83f3d9dd4c491fef91d6"


@dataclass(frozen=True)
class GaugeConvention:
    derivative_sign: int
    matter_phase_sign: int
    connection_shift_sign: int


def run(source_file: Path) -> int:
    checks = CheckLedger("P030-EM2")
    payload = source_file.read_bytes()
    source_text = payload.decode("utf-8")
    checks.check(
        "the audited EM2 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == EM2_SHA256,
    )

    time, coordinate, coupling = sp.symbols("t x e", real=True, positive=True)
    field = sp.Function("Psi")(time, coordinate)
    conjugate = sp.Function("Psi_conj")(time, coordinate)
    chi = sp.Function("chi")(time, coordinate)
    a0 = sp.Function("A0")(time, coordinate)
    a1 = sp.Function("A1")(time, coordinate)
    transformed, transformed_connections = local_u1_transform(
        field, (a0, a1), chi, (time, coordinate), coupling
    )
    phase = sp.exp(sp.I * coupling * chi)
    checks.check(
        "both connection components transform covariantly for arbitrary chi",
        all(
            sp.simplify(
                u1_covariant_derivative(
                    transformed,
                    transformed_connection,
                    variable,
                    coupling,
                )
                - phase
                * u1_covariant_derivative(
                    field, connection, variable, coupling
                )
            )
            == 0
            for connection, transformed_connection, variable in zip(
                (a0, a1),
                transformed_connections,
                (time, coordinate),
                strict=True,
            )
        ),
    )

    jet_field, jet_derivative, jet_connection, jet_chi = sp.symbols(
        "psi dpsi A dchi"
    )

    def convention_is_covariant(candidate: GaugeConvention) -> bool:
        original = (
            jet_derivative
            + candidate.derivative_sign
            * sp.I
            * coupling
            * jet_connection
            * jet_field
        )
        transformed_derivative = sp.exp(
            candidate.matter_phase_sign * sp.I * coupling * chi
        ) * (
            jet_derivative
            + candidate.matter_phase_sign
            * sp.I
            * coupling
            * jet_chi
            * jet_field
        )
        transformed_connection = (
            jet_connection + candidate.connection_shift_sign * jet_chi
        )
        transformed_covariant = transformed_derivative + (
            candidate.derivative_sign
            * sp.I
            * coupling
            * transformed_connection
            * sp.exp(candidate.matter_phase_sign * sp.I * coupling * chi)
            * jet_field
        )
        expected = (
            sp.exp(candidate.matter_phase_sign * sp.I * coupling * chi)
            * original
        )
        return sp.simplify(transformed_covariant - expected) == 0

    checks.mutation_sensitive(
        "derivative, matter-phase, and connection-shift convention",
        convention_is_covariant,
        GaugeConvention(-1, 1, 1),
        [
            GaugeConvention(1, 1, 1),
            GaugeConvention(-1, -1, 1),
            GaugeConvention(-1, 1, -1),
        ],
    )

    kinetic = gauged_scalar_kinetic_density(
        field, conjugate, (a0, a1), (time, coordinate), coupling
    )
    transformed_kinetic = gauged_scalar_kinetic_density(
        transformed,
        sp.exp(-sp.I * coupling * chi) * conjugate,
        transformed_connections,
        (time, coordinate),
        coupling,
    )
    checks.check(
        "the gauged kinetic density is exactly locally invariant",
        sp.simplify(transformed_kinetic - kinetic) == 0,
    )
    checks.check(
        "a phase-independent potential is separately invariant",
        sp.simplify(
            transformed
            * sp.exp(-sp.I * coupling * chi)
            * conjugate
            - field * conjugate
        )
        == 0,
    )

    bare = gauged_scalar_kinetic_density(
        field, conjugate, (0, 0), (time, coordinate), coupling
    )
    current0, current1 = u1_current_components(
        field, conjugate, coordinate, time
    )
    checks.check(
        "the accepted-current expansion has a plus e A_mu j^mu cross term",
        sp.simplify(
            kinetic
            - bare
            - coupling * (a0 * current0 + a1 * current1)
            - coupling**2 * (a0**2 - a1**2) * field * conjugate
        )
        == 0,
    )

    amplitude, d_amplitude, d_phase, d_chi, connection = sp.symbols(
        "f df dtheta dchi A", real=True
    )
    accepted_polar_current = -2 * amplitude**2 * d_phase
    bare_residual = (
        2 * coupling * amplitude**2 * d_phase * d_chi
        + coupling**2 * amplitude**2 * d_chi**2
    )
    raw_cross_term = -2 * coupling * amplitude**2 * d_phase * connection
    checks.check(
        "polar expansion fixes the source's current-sign mismatch",
        sp.simplify(
            bare_residual
            - (-coupling * accepted_polar_current * d_chi)
            - coupling**2 * amplitude**2 * d_chi**2
        )
        == 0
        and sp.simplify(
            raw_cross_term - coupling * connection * accepted_polar_current
        )
        == 0,
    )
    checks.check(
        "EM2 explicitly assigns the opposite polar current while calling it EM1's",
        "jmu = 2 * f**2 * dtheta" in source_text
        and "-e * jmu * Amu" in source_text,
    )

    curvature = u1_field_strength(a0, a1, time, coordinate)
    transformed_curvature = u1_field_strength(
        *transformed_connections, time, coordinate
    )
    checks.check(
        "the curvature is gauge invariant",
        sp.simplify(transformed_curvature - curvature) == 0,
    )
    checks.check(
        "the covariant-derivative commutator derives minus i e F Psi",
        sp.simplify(
            u1_covariant_commutator(
                field, a0, a1, time, coordinate, coupling
            )
            + sp.I * coupling * curvature * field
        )
        == 0,
    )
    pure_parameter = sp.Function("alpha")(time, coordinate)
    checks.check(
        "a pure-gauge connection has zero curvature",
        u1_field_strength(
            sp.diff(pure_parameter, time),
            sp.diff(pure_parameter, coordinate),
            time,
            coordinate,
        )
        == 0,
    )
    checks.check(
        "local covariance also admits nonzero curvature without selecting dynamics",
        u1_field_strength(0, time, time, coordinate) == 1,
    )
    kinetic_coefficient = sp.symbols("c_F", real=True)
    checks.check(
        "gauge invariance leaves the curvature-action coefficient unconstrained",
        sp.diff(kinetic - kinetic_coefficient * curvature**2, kinetic_coefficient)
        == -curvature**2
        and kinetic_coefficient not in kinetic.free_symbols,
    )

    winding = sp.symbols("N", integer=True, positive=True)
    asymptotic_connection = sp.symbols("a_infinity", real=True)
    angular_coefficient = (winding - asymptotic_connection) ** 2
    forced = sp.solve(sp.Eq(angular_coefficient, 0), asymptotic_connection)
    flux = finite_energy_winding_flux(winding, coupling)
    checks.check(
        "finite angular energy conditionally forces integer winding flux",
        forced == [winding]
        and flux == 2 * sp.pi * winding / coupling
        and sp.simplify(angular_coefficient.subs(asymptotic_connection, 0))
        == winding**2,
    )
    checks.check(
        "the general flux formula agrees with the accepted vortex convention",
        sp.simplify(flux - quantized_flux(winding, coupling)) == 0,
    )
    checks.check(
        "integer winding gives trivial charge-e matter holonomy",
        u1_holonomy(flux.subs(winding, 1), coupling) == 1,
    )
    half_flux = sp.pi / coupling
    half_rejected = False
    try:
        finite_energy_winding_flux(sp.Rational(1, 2), coupling)
    except ValueError:
        half_rejected = True
    checks.check(
        "minus-one holonomy requires a separate fractional-flux premise",
        u1_holonomy(half_flux, coupling) == -1 and half_rejected,
    )
    momentum, arbitrary_phase = sp.symbols("k beta", real=True)
    checks.check(
        "momentum independence is shared by every constant phase",
        sp.diff(sp.exp(sp.I * arbitrary_phase) + 0 * momentum, momentum) == 0,
    )

    total = checks.finish()
    print(f"P030 EM2 LOCAL-U1 AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
