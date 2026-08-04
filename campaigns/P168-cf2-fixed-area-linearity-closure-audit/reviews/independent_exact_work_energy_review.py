#!/usr/bin/env python3
"""Fresh exact derivation of CF2's two conditional linear constructions."""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp

from substrate_framework.verification import CheckLedger


@dataclass(frozen=True)
class LocalModel:
    density_coefficient: sp.Expr
    area_exponent: int


def main() -> int:
    checks = CheckLedger("P168-INDEPENDENT-WORK-ENERGY")
    flux, area, charge, length, coordinate = sp.symbols(
        "Phi A q L x", positive=True
    )
    field_symbol = sp.symbols("E", positive=True)

    field_solutions = sp.solve(sp.Eq(field_symbol * area, flux), field_symbol)
    checks.check(
        "independent solution of the uniform-cap equation gives E equals Phi over A",
        field_solutions == [flux / area],
    )
    field = field_solutions[0]
    checks.check(
        "fixed area makes the independently solved field length-independent",
        length not in field.free_symbols and sp.diff(field, length) == 0,
    )

    volume_energy = sp.integrate(
        sp.Rational(1, 2) * field**2 * area,
        (coordinate, 0, length),
    )
    endpoint_work = sp.integrate(
        charge * field,
        (coordinate, 0, length),
    )
    checks.check(
        "independent volume integration gives Phi squared L over two A",
        volume_energy == flux**2 * length / (2 * area),
    )
    checks.check(
        "independent endpoint-force integration gives q Phi L over A",
        endpoint_work == charge * flux * length / area,
    )
    energy_slope = sp.diff(volume_energy, length)
    force_slope = sp.diff(endpoint_work, length)
    checks.check(
        "both constructions are linear while retaining distinct symbolic slopes",
        sp.diff(volume_energy, length, 2) == 0
        and sp.diff(endpoint_work, length, 2) == 0
        and sp.simplify(energy_slope - force_slope) != 0,
    )
    checks.check(
        "independent slope equality solves uniquely to q equals Phi over two",
        sp.solve(sp.Eq(energy_slope, force_slope), charge) == [flux / 2],
    )
    checks.check(
        "q equals Phi doubles endpoint work relative to field energy",
        sp.simplify(endpoint_work.subs(charge, flux) / volume_energy) == 2,
    )

    def local_model_matches(candidate: object) -> bool:
        assert isinstance(candidate, LocalModel)
        proposed_field = flux / area**candidate.area_exponent
        proposed_energy = sp.integrate(
            candidate.density_coefficient * proposed_field**2 * area,
            (coordinate, 0, length),
        )
        return (
            sp.simplify(proposed_field * area - flux) == 0
            and sp.simplify(proposed_energy - volume_energy) == 0
        )

    checks.mutation_sensitive(
        "independent normalization and area-power reconstruction",
        local_model_matches,
        LocalModel(sp.Rational(1, 2), 1),
        [
            LocalModel(sp.Integer(1), 1),
            LocalModel(sp.Rational(1, 4), 1),
            LocalModel(sp.Rational(1, 2), 2),
        ],
    )

    area0, length0 = sp.symbols("A0 L0", positive=True)
    expanding_area = area0 * (1 + coordinate / length0)
    expanding_field = flux / expanding_area
    expanding_energy = sp.integrate(
        sp.Rational(1, 2) * expanding_field**2 * expanding_area,
        (coordinate, 0, length),
    )
    expected_logarithm = (
        flux**2
        * length0
        * sp.log(1 + length / length0)
        / (2 * area0)
    )
    checks.check(
        "independent expanding-area integration gives the logarithmic counterexample",
        sp.simplify(expanding_energy - expected_logarithm) == 0,
    )
    checks.check(
        "the expanding-area field and energy have nonzero length variation",
        sp.diff(expanding_field, coordinate) != 0
        and sp.diff(expanding_energy, length, 2) != 0,
    )
    checks.check(
        "the expanding-area result has the constant-area limit",
        sp.limit(expected_logarithm, length0, sp.oo)
        == flux**2 * length / (2 * area0),
    )

    radius = sp.symbols("r", positive=True)
    sphere_area = 4 * sp.pi * radius**2
    radial_field = sp.solve(
        sp.Eq(field_symbol * sphere_area, flux), field_symbol
    )[0]
    coulomb_work = charge * flux / (4 * sp.pi * radius)
    checks.check(
        "independent spherical Gauss solution is inverse-square",
        radial_field == flux / sphere_area
        and sp.diff(radial_field, radius) != 0,
    )
    checks.check(
        "independent Coulomb guard is curved and decays at infinity",
        sp.diff(coulomb_work, radius, 2) != 0
        and sp.limit(coulomb_work, radius, sp.oo) == 0,
    )
    checks.check(
        "fixed-area energy is unbounded but that algebra alone names no physical phase",
        sp.limit(volume_energy, length, sp.oo) == sp.oo
        and not any(
            symbol.name in {"quark", "QCD", "confinement", "vortex"}
            for symbol in volume_energy.free_symbols
        ),
    )

    tension = sp.symbols("sigma", positive=True)
    effective_area = flux**2 / (2 * tension)
    checks.check(
        "effective-area inversion is exactly dependent on supplied tension",
        sp.simplify(flux**2 / (2 * effective_area) - tension) == 0
        and sp.diff(effective_area, tension) != 0,
    )

    total = checks.finish()
    print(f"P168 INDEPENDENT WORK-ENERGY REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
