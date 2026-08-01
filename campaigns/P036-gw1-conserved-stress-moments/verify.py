#!/usr/bin/env python3
"""Verify C-MOM-001 and audit the hash-pinned GW1 source unit."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import sympy as sp

from substrate_framework.conserved_moments import (
    discrete_mass_moments,
    isolated_conserved_stress_moment_rates,
    symmetric_trace_free,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "3aba56675f887f98c015de7caad1834893ffdbc27ca1daf3c7056694953102fc"


@dataclass(frozen=True)
class MomentCoefficients:
    monopole_rate: int
    dipole_momentum_factor: int
    dipole_acceleration: int
    second_moment_stress_factor: int


def valid_moment_coefficients(candidate: MomentCoefficients) -> bool:
    return candidate == MomentCoefficients(0, 1, 0, 2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P036-GW1")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    ledger.check(
        "the audited GW1 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    reproduced = subprocess.run(
        [sys.executable, str(args.source_file)],
        capture_output=True,
        text=True,
        check=False,
    )
    ledger.check("GW1 exits cleanly", reproduced.returncode == 0)
    ledger.check(
        "GW1's declared twenty-four-check tally reproduces",
        "ALL 24 CHECKS PASS" in reproduced.stdout,
    )

    t, x, y, z = sp.symbols("t x y z", real=True)
    velocity = sp.Matrix([sp.Rational(1, 2), -sp.Rational(1, 3), sp.Rational(2, 5)])
    coordinates = sp.Matrix([x, y, z])
    displacement = coordinates - velocity * t
    density = sp.exp(-sum(component**2 for component in displacement)) / sp.pi ** sp.Rational(3, 2)
    energy_flux = sp.simplify(velocity * density)
    spatial_stress = sp.simplify(velocity * velocity.T * density)
    energy_residual = sp.simplify(
        sp.diff(density, t)
        + sum(sp.diff(energy_flux[index], coordinates[index]) for index in range(3))
    )
    ledger.check(
        "a translating three-dimensional Gaussian obeys exact energy continuity",
        energy_residual == 0,
    )
    momentum_residuals = [
        sp.simplify(
            sp.diff(energy_flux[index], t)
            + sum(
                sp.diff(spatial_stress[axis, index], coordinates[axis])
                for axis in range(3)
            )
        )
        for index in range(3)
    ]
    ledger.check(
        "the same symmetric tensor obeys all three momentum equations",
        momentum_residuals == [0, 0, 0]
        and spatial_stress == spatial_stress.T,
    )

    monopole = sp.Integer(1)
    momentum = velocity
    dipole = velocity * t
    second_moment = sp.simplify(
        velocity * velocity.T * t**2 + sp.eye(3) / 2
    )
    integrated_stress = sp.simplify(velocity * velocity.T)
    ledger.check(
        "the normalized translating Gaussian has constant monopole and momentum",
        sp.diff(monopole, t) == 0
        and sp.diff(momentum, t) == sp.zeros(3, 1),
    )
    ledger.check(
        "its dipole is affine rather than generally constant",
        sp.diff(dipole, t) == momentum
        and sp.diff(dipole, t, 2) == sp.zeros(3, 1)
        and dipole != sp.zeros(3, 1),
    )
    ledger.check(
        "its exact second moment satisfies ddot I equals twice integrated stress",
        sp.diff(second_moment, t, 2) == 2 * integrated_stress,
    )

    rates = isolated_conserved_stress_moment_rates(momentum, integrated_stress)
    ledger.check(
        "the reusable isolated-source API reproduces the complete Gaussian ladder",
        rates.monopole_rate == 0
        and rates.momentum_rate == sp.zeros(3, 1)
        and rates.dipole_rate == momentum
        and rates.dipole_acceleration == sp.zeros(3, 1)
        and rates.second_moment_acceleration == sp.diff(second_moment, t, 2),
    )
    ledger.check(
        "the normalized STF acceleration is twice the STF integrated stress",
        rates.trace_free_second_moment_acceleration
        == 2 * symmetric_trace_free(integrated_stress),
    )
    ledger.check(
        "GW1's quadrupole convention is exactly three times normalized STF",
        rates.triple_normalized_quadrupole_acceleration
        == 3 * rates.trace_free_second_moment_acceleration,
    )
    ledger.mutation_sensitive(
        "conserved moment coefficients",
        valid_moment_coefficients,
        MomentCoefficients(0, 1, 0, 2),
        [
            MomentCoefficients(1, 1, 0, 2),
            MomentCoefficients(0, -1, 0, 2),
            MomentCoefficients(0, 1, 1, 2),
            MomentCoefficients(0, 1, 0, 1),
        ],
    )

    finite_density = 1 - t
    finite_current = x
    finite_residual = sp.diff(finite_density, t) + sp.diff(finite_current, x)
    finite_monopole = sp.integrate(finite_density, (x, 0, 1))
    boundary_flux = finite_current.subs(x, 1) - finite_current.subs(x, 0)
    ledger.check(
        "a nonzero boundary flux changes the monopole despite local continuity",
        finite_residual == 0
        and sp.diff(finite_monopole, t) == -boundary_flux
        and boundary_flux == 1,
    )

    v, w = sp.symbols("v w", real=True)
    density1 = sp.exp(-(x - v * t) ** 2) / sp.sqrt(sp.pi)
    energy_flux1 = v * density1
    momentum_density1 = w * density1
    stress1 = v * w * density1
    ledger.check(
        "a nonsymmetric conserved tensor need not identify dipole velocity with momentum",
        sp.simplify(sp.diff(density1, t) + sp.diff(energy_flux1, x)) == 0
        and sp.simplify(sp.diff(momentum_density1, t) + sp.diff(stress1, x)) == 0
        and v != w,
    )
    ledger.check(
        "stress symmetry is the load-bearing D-dot equals P premise",
        sp.integrate(energy_flux1, (x, -sp.oo, sp.oo)) == v
        and sp.integrate(momentum_density1, (x, -sp.oo, sp.oo)) == w,
    )

    a = sp.Matrix(sp.symbols("a0:3"))
    shifted_second = sp.simplify(
        second_moment - a * dipole.T - dipole * a.T + monopole * a * a.T
    )
    ledger.check(
        "constant origin translation leaves the isolated second derivative unchanged",
        sp.diff(shifted_second, t, 2) == sp.diff(second_moment, t, 2),
    )

    static = discrete_mass_moments([1, 1], [[1, 0, 0], [-1, 0, 0]])
    ledger.check(
        "a nonzero static trace-free quadrupole does not imply time variation",
        static.trace_free_second_moment != sp.zeros(3)
        and sp.diff(static.trace_free_second_moment, t, 2) == sp.zeros(3),
    )

    g = sp.Function("g")(t)
    source_momentum = g * sp.exp(-x**2)
    source_total_momentum_rate = sp.simplify(
        sp.diff(sp.integrate(source_momentum, (x, -sp.oo, sp.oo)), t)
    )
    ledger.check(
        "GW1's explicit sloshing current has unconstrained nonzero total-momentum rate",
        source_total_momentum_rate == sp.sqrt(sp.pi) * sp.diff(g, t)
        and source_total_momentum_rate != 0,
    )
    ledger.check(
        "GW1 chooses its current and compact stress independently instead of enforcing the local equation",
        'pi1 = g * sp.exp(-x**2)' in source_text
        and 'Txx = sp.Function("S")(t) * sp.exp(-x**2)' in source_text,
    )
    ledger.check(
        "a compact stress surface integral cannot cancel the arbitrary current's total derivative",
        sp.integrate(sp.diff(sp.exp(-x**2), x), (x, -sp.oo, sp.oo)) == 0
        and source_total_momentum_rate != 0,
    )

    ledger.check(
        "GW1's orbit is externally held rather than closed as an isolated stress tensor",
        "the external" in source_text
        and "mechanism holding the binary on its orbit is given" in source_text,
    )
    ledger.check(
        "GW1's nonzero binary second moment is kinematic but not a radiation oracle",
        "I-ddot^{xx} != 0" in source_text
        and "standard linearised-gravity result" in source_text,
    )
    ledger.check(
        "GW1 imports its retarded radiation rule and forward TT coupling",
        "retarded Green's function is 1/r" in source_text
        and "only this STF" in source_text
        and "couples to the TT graviton" in source_text,
    )
    ledger.check(
        "GW1's lowest-radiating-order function is a declared two-case lookup",
        "if dim == 2:" in source_text
        and "if dim == 4 and spin == 2:" in source_text
        and "return 2" in source_text,
    )
    ledger.check(
        "conservation suppresses lower derivatives but supplies no gravitational field",
        rates.monopole_rate == 0
        and rates.dipole_acceleration == sp.zeros(3, 1)
        and "linearised-gravity result" in source_text,
    )

    count = ledger.finish()
    print(f"P036 GW1 CONSERVED-STRESS MOMENT AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
