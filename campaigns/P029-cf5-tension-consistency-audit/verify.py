#!/usr/bin/env python3
"""Exact information and sensitivity audit for CF5's effective-area bridge."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.abelian_higgs_vortex import (
    asymptotic_masses,
    quantized_flux,
)
from substrate_framework.flux_tube import tube_energy_slope
from substrate_framework.verification import CheckLedger


CF5_SHA256 = "0a449f8b95bc0a83fb0316992fb0d1776a6157e1445029623b4608246dc256f7"


@dataclass(frozen=True)
class InversionConvention:
    area_coefficient: sp.Expr
    energy_coefficient: sp.Expr


def run(source_file: Path) -> int:
    checks = CheckLedger("P029-CF5")
    payload = source_file.read_bytes()
    source_text = payload.decode("utf-8")
    checks.check(
        "the audited CF5 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == CF5_SHA256,
    )
    checks.check(
        "the pinned source repeats the removed NumPy trapezoid API",
        "np.trapz(" in source_text,
    )

    winding = sp.symbols("n", integer=True, positive=True)
    gauge, vacuum, coupling, tension = sp.symbols(
        "g v lambda sigma", positive=True
    )
    flux = quantized_flux(winding, gauge)
    vector_mass, scalar_mass = asymptotic_masses(vacuum, coupling, gauge)
    penetration_length = sp.simplify(1 / vector_mass)
    effective_area = sp.simplify(flux**2 / (2 * tension))

    checks.check(
        "accepted flux and supplied tension define the effective area exactly",
        flux == 2 * sp.pi * winding / gauge
        and effective_area
        == 2 * sp.pi**2 * winding**2 / (gauge**2 * tension),
    )
    checks.check(
        "substitution into the tube slope reconstructs the supplied tension",
        sp.simplify(tube_energy_slope(flux, effective_area) - tension) == 0,
    )
    checks.check(
        "the reconstructed area remains load-bearing on its tension input",
        sp.diff(effective_area, tension) != 0
        and sp.simplify(tension * effective_area - flux**2 / 2) == 0,
    )

    def inversion_closes(candidate: InversionConvention) -> bool:
        area = sp.simplify(
            candidate.area_coefficient * flux**2 / tension
        )
        slope = sp.simplify(candidate.energy_coefficient * flux**2 / area)
        return sp.simplify(slope - tension) == 0

    checks.mutation_sensitive(
        "matching coefficients in the algebraic inversion",
        inversion_closes,
        InversionConvention(sp.Rational(1, 2), sp.Rational(1, 2)),
        [
            InversionConvention(1, sp.Rational(1, 2)),
            InversionConvention(sp.Rational(1, 2), 1),
            InversionConvention(sp.Rational(1, 4), sp.Rational(1, 2)),
        ],
    )
    alternative_tension = sp.symbols("sigma_alt", positive=True)
    alternative_area = sp.simplify(flux**2 / (2 * alternative_tension))
    checks.check(
        "every positive alternative tension passes the same round trip",
        sp.simplify(tube_energy_slope(flux, alternative_area) - alternative_tension)
        == 0
        and sp.simplify(alternative_area - effective_area) != 0,
    )

    penetration_ratio = sp.simplify(
        effective_area / penetration_length**2
    )
    checks.check(
        "the penetration-area ratio is only a transformed supplied tension",
        penetration_ratio
        == 2 * sp.pi**2 * winding**2 * vacuum**2 / tension
        and gauge not in penetration_ratio.free_symbols,
    )
    ratio_symbol = sp.symbols("r_core", positive=True)
    recovered_tension = sp.solve(
        sp.Eq(penetration_ratio, ratio_symbol), tension
    )
    checks.check(
        "without an independent area ratio the transform constrains no tension",
        recovered_tension
        == [2 * sp.pi**2 * vacuum**2 * winding**2 / ratio_symbol],
    )

    lower, upper = sp.Rational(1, 10), sp.Integer(100)
    lower_tension = sp.simplify(
        2 * sp.pi**2 * winding**2 * vacuum**2 / upper
    )
    upper_tension = sp.simplify(
        2 * sp.pi**2 * winding**2 * vacuum**2 / lower
    )
    checks.check(
        "CF5's ratio window accepts a three-decade tension interval",
        sp.simplify(upper_tension / lower_tension) == 1000,
    )

    accepted_demo_tension = sp.Rational(421160, 100000)

    def in_source_window(candidate_tension: sp.Expr) -> bool:
        candidate_ratio = sp.N(
            penetration_ratio.subs(
                {
                    winding: 1,
                    vacuum: 1,
                    tension: candidate_tension,
                }
            ),
            30,
        )
        return bool(lower < candidate_ratio < upper)

    checks.check(
        "the accepted demo tension reproduces CF5's reported ratio",
        abs(
            float(
                penetration_ratio.subs(
                    {winding: 1, vacuum: 1, tension: accepted_demo_tension}
                )
            )
            - 4.686
        )
        < 0.002,
    )
    checks.check(
        "tenfold and fortyfold tension mutations still pass CF5's window",
        in_source_window(accepted_demo_tension / 10)
        and in_source_window(accepted_demo_tension * 10)
        and in_source_window(accepted_demo_tension * 40),
    )
    checks.check(
        "CF5's selected thousand-scale mutation fails only the broad window",
        not in_source_window(sp.Integer(1000)),
    )

    scalar_length = sp.simplify(1 / scalar_mass)
    checks.check(
        "the declared vortex has distinct vector and scalar inverse lengths",
        penetration_length == 1 / (gauge * vacuum)
        and scalar_length == 1 / (vacuum * sp.sqrt(2 * coupling))
        and sp.simplify(
            (effective_area / scalar_length**2)
            / (effective_area / penetration_length**2)
        )
        == 2 * coupling / gauge**2,
    )
    core_area_factor = sp.symbols("c_area", positive=True)
    checks.check(
        "an unfixed core-area convention rescales the comparison freely",
        sp.simplify(
            effective_area / (core_area_factor * penetration_length**2)
            - penetration_ratio / core_area_factor
        )
        == 0,
    )
    profile = sp.Function("profile")
    checks.check(
        "no smooth-profile observable enters CF5's effective-area definition",
        not effective_area.has(profile)
        and coupling not in effective_area.free_symbols,
    )

    total = checks.finish()
    print(f"P029 CF5 INFORMATION AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
