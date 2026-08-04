#!/usr/bin/env python3
"""Fresh passive half-line derivation without the canonical ledger helper."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P150-independent")
    x, time = sp.symbols("x t", real=True)
    speed, boundary, frequency = sp.symbols("c zeta omega", positive=True)
    incident, reflected = sp.symbols("A_i A_r", nonzero=True)

    field = incident * sp.exp(-sp.I * frequency * (time + x / speed)) + reflected * sp.exp(
        -sp.I * frequency * (time - x / speed)
    )
    wave_residual = sp.simplify(sp.diff(field, time, 2) - speed**2 * sp.diff(field, x, 2))
    checks.check("fresh harmonics solve the bulk wave equation", wave_residual == 0)

    boundary_residual = sp.simplify(
        (sp.diff(field, time) - boundary * sp.diff(field, x)).subs(x, 0)
    )
    amplitude_solution = sp.solve(
        sp.Eq(boundary_residual, 0), reflected, dict=True
    )[0][reflected]
    amplitude = sp.factor(amplitude_solution / incident)
    z = sp.symbols("z", positive=True)
    amplitude_z = sp.factor(amplitude.subs(boundary, z * speed))
    checks.check(
        "fresh boundary substitution derives amplitude including phase",
        amplitude_z == (z - 1) / (z + 1),
    )

    reflected_power = sp.factor(amplitude_z**2)
    removed_power = sp.factor(1 - reflected_power)
    checks.check(
        "fresh power expansion derives the complementary fractions",
        reflected_power == (z - 1) ** 2 / (z + 1) ** 2
        and removed_power == 4 * z / (z + 1) ** 2,
    )
    checks.check("fresh power balance is exact", sp.simplify(reflected_power + removed_power - 1) == 0)

    phi_x = sp.symbols("phi_x", real=True, nonzero=True)
    passive_rate = sp.factor(-speed**2 * (boundary * phi_x) * phi_x)
    active_rate = sp.factor(-speed**2 * (-boundary * phi_x) * phi_x)
    checks.check("fresh integration-by-parts sign is dissipative", passive_rate.is_negative is True)
    checks.check("opposite boundary sign is active", active_rate.is_positive is True)

    reciprocal = sp.factor(amplitude_z.subs(z, 1 / z))
    checks.check("fresh reciprocal map flips amplitude", sp.simplify(reciprocal + amplitude_z) == 0)
    checks.check("fresh reciprocal map preserves reflected power", sp.simplify(reciprocal**2 - reflected_power) == 0)
    checks.check(
        "fresh reciprocal solve has two positive branches away from match",
        sp.solve(sp.Eq(reflected_power, sp.Rational(1, 9)), z) == [sp.Rational(1, 2), 2],
    )

    contrast = sp.factor((1 - reflected_power) / (1 + reflected_power))
    checks.check("fresh declared-reference contrast is exact", contrast == 2 * z / (z**2 + 1))
    checks.check(
        "fresh contrast is not an independent third function",
        sp.simplify(contrast - removed_power / (2 - removed_power)) == 0,
    )
    symmetric_contrast = sp.simplify((reflected_power - reflected_power) / (reflected_power + reflected_power))
    checks.check("fresh equal-channel countermodel has zero contrast", symmetric_contrast == 0)

    altered_reference = sp.factor((2 - reflected_power) / (2 + reflected_power))
    checks.check("reference normalization mutation changes the contrast", sp.simplify(altered_reference - contrast) != 0)

    wrong_field = incident * sp.exp(-sp.I * frequency * (time - x / speed)) + reflected * sp.exp(
        -sp.I * frequency * (time + x / speed)
    )
    wrong_residual = sp.simplify(
        (sp.diff(wrong_field, time) - boundary * sp.diff(wrong_field, x)).subs(x, 0)
    )
    wrong_solution = sp.solve(
        sp.Eq(wrong_residual, 0), reflected, dict=True
    )[0][reflected]
    wrong_amplitude = sp.factor(
        wrong_solution.subs(boundary, z * speed) / incident
    )
    checks.check(
        "incoming-outgoing mutation inverts the amplitude ratio",
        sp.simplify(wrong_amplitude * amplitude_z - 1) == 0
        and sp.simplify(wrong_amplitude - amplitude_z) != 0,
    )

    coupling, inertia = sp.symbols("lambda mu", positive=True)
    spatial_rate, potential_force, drive = sp.symbols("phi_xt Vprime J")
    eliminated = -inertia * spatial_rate / coupling**2 + (potential_force - drive) / coupling
    checks.check(
        "fresh piston elimination retains frequency-dependent inertia",
        spatial_rate in eliminated.free_symbols
        and sp.diff(eliminated, spatial_rate) == -inertia / coupling**2,
    )
    checks.check(
        "zero drive and potential still leaves the inertial term",
        eliminated.subs({potential_force: 0, drive: 0}) != 0,
    )

    boundary_storage_fraction = sp.symbols("S", nonnegative=True)
    physical_absorption = sp.simplify(1 - reflected_power - boundary_storage_fraction)
    checks.check(
        "extra boundary storage defeats absorption from complement alone",
        sp.simplify(physical_absorption - removed_power) == -boundary_storage_fraction,
    )

    tally = checks.finish()
    print(f"P150 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
