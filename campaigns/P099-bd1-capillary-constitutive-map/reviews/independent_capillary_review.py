"""Independent variational, dimensional, and rank rederivation for P099."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P099-INDEPENDENT")

    radial, azimuth = sp.symbols("r phi", positive=True)
    stiffness, strength = sp.symbols("K_F s", positive=True)
    core_cutoff, outer_cutoff = sp.symbols("r_c R_o", positive=True)
    director = strength * azimuth
    density = stiffness * (sp.diff(director, azimuth) / radial) ** 2 / 2
    annulus_integral = sp.integrate(
        sp.integrate(
            density * radial,
            (radial, core_cutoff, outer_cutoff),
        ),
        (azimuth, 0, 2 * sp.pi),
    )
    checks.check(
        "annulus integration independently gives the Frank logarithm",
        sp.simplify(
            annulus_integral
            - sp.pi * stiffness * strength**2 * sp.log(outer_cutoff / core_cutoff)
        )
        == 0,
    )

    field = sp.symbols("psi", real=True)
    quartic, bias = sp.symbols("lambda h", positive=True)
    bulk = quartic * (field**2 - 1) ** 2 / 4 - bias * field
    well_difference = sp.simplify(bulk.subs(field, -1) - bulk.subs(field, 1))
    checks.check(
        "declared tilted wells independently give the two-h difference",
        well_difference == 2 * bias,
    )

    amplitude, wave, frequency, position, time = sp.symbols(
        "A k omega x t",
        positive=True,
    )
    standing_profile = amplitude * sp.sin(wave * position) * sp.cos(frequency * time)
    energy_density = (
        sp.diff(standing_profile, time) ** 2
        + sp.diff(standing_profile, position) ** 2
    ) / 2
    wall_average = sp.simplify(
        sp.integrate(
            energy_density.subs(position, 0),
            (time, 0, 2 * sp.pi / frequency),
        )
        / (2 * sp.pi / frequency)
    )
    checks.check(
        "declared standing-profile energy density gives A squared k squared over four",
        wall_average == amplitude**2 * wave**2 / 4,
    )
    checks.check(
        "standing-profile result is an ansatz specialization rather than a dispersion law",
        frequency not in wall_average.free_symbols
        and wave in wall_average.free_symbols,
    )

    radius = sp.symbols("R", real=True)
    tension, drive, offset = sp.symbols("tau p E_0", positive=True)
    energy = 2 * sp.pi * radius * tension - sp.pi * radius**2 * drive + offset
    completed_square = (
        offset
        + sp.pi * tension**2 / drive
        - sp.pi * drive * (radius - tension / drive) ** 2
    )
    checks.check(
        "completion of the square independently proves the global maximum",
        sp.expand(energy - completed_square) == 0
        and completed_square.subs(radius, tension / drive)
        == offset + sp.pi * tension**2 / drive,
    )
    checks.check(
        "subtracting the R-zero state independently removes only the offset",
        sp.simplify(
            completed_square.subs(radius, tension / drive)
            - completed_square.subs(radius, 0)
        )
        == sp.pi * tension**2 / drive,
    )

    core_energy, coupling, thickness = sp.symbols(
        "epsilon_core g l_m",
        positive=True,
    )
    declared_tension = (
        sp.pi * stiffness * strength**2 * sp.log(outer_cutoff / core_cutoff)
        + core_energy
    )
    declared_drive = coupling * amplitude**2 * wave**2 * thickness / 2
    eliminated_radius = sp.solve(sp.Eq(sp.diff(energy, radius), 0), radius)[0]
    substituted_radius = sp.factor(eliminated_radius.subs({tension: declared_tension, drive: declared_drive}))
    substituted_barrier = sp.factor(
        (sp.pi * tension**2 / drive).subs({tension: declared_tension, drive: declared_drive})
    )
    checks.check(
        "independent elimination gives the declared composed radius",
        sp.simplify(
            substituted_radius
            - 2 * declared_tension / (coupling * amplitude**2 * wave**2 * thickness)
        )
        == 0,
    )
    checks.check(
        "independent elimination gives the declared composed relative barrier",
        sp.simplify(
            substituted_barrier
            - 2 * sp.pi * declared_tension**2
            / (coupling * amplitude**2 * wave**2 * thickness)
        )
        == 0,
    )

    alpha, amplitude_power, wavenumber_power = sp.symbols("alpha m n", real=True)
    coupling_length_exponent = wavenumber_power - 3 - amplitude_power * alpha
    bulk_length_exponent = sp.simplify(
        coupling_length_exponent
        + amplitude_power * alpha
        - wavenumber_power
    )
    area_length_exponent = sp.simplify(bulk_length_exponent + 1)
    checks.check(
        "independent exponent balance closes every monomial loading convention",
        bulk_length_exponent == -3 and area_length_exponent == -2,
    )
    checks.check(
        "dimensionless amplitude admits linear and quadratic laws with the same coupling dimension",
        coupling_length_exponent.subs({alpha: 0, amplitude_power: 1, wavenumber_power: 2})
        == coupling_length_exponent.subs({alpha: 0, amplitude_power: 2, wavenumber_power: 2})
        == -1,
    )

    exponent_matrix = sp.Matrix(
        [[1, -1, -2, -2, -1], [2, -1, -2, -2, -1]]
    )
    barrier_row = exponent_matrix[1, :]
    checks.check(
        "independent exact ranks expose the observation ceiling",
        exponent_matrix.rank() == 2
        and len(exponent_matrix.nullspace()) == 3
        and sp.Matrix([list(barrier_row)]).rank() == 1
        and len(sp.Matrix([list(barrier_row)]).nullspace()) == 4,
    )
    checks.check(
        "all two-observable null directions leave line tension fixed",
        all(vector[0] == 0 for vector in exponent_matrix.nullspace()),
    )
    checks.mutation_sensitive(
        "drive amplitude exponent is independently load bearing",
        lambda exponent: sp.simplify(
            coupling * amplitude**exponent * wave**2 * thickness / 2
            - declared_drive
        )
        == 0,
        2,
        (1, 3),
    )

    negative_drive = sp.symbols("q", positive=True)
    wrong_sign_energy = 2 * sp.pi * radius * tension + sp.pi * radius**2 * negative_drive
    wrong_sign_root = sp.solve(
        sp.Eq(sp.diff(wrong_sign_energy, radius), 0),
        radius,
    )
    checks.check(
        "negative area drive independently gives a monotone positive-radius landscape",
        sp.diff(wrong_sign_energy, radius).subs(radius, 1).is_positive is True
        and wrong_sign_root == [-tension / negative_drive]
        and wrong_sign_root[0].is_negative is True,
    )
    checks.check(
        "no-loading limit is a model-internal divergence, not a rate theorem",
        sp.limit(
            2
            * sp.pi
            * tension**2
            / (coupling * amplitude**2 * wave**2 * thickness),
            amplitude,
            0,
            dir="+",
        )
        == sp.oo,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
