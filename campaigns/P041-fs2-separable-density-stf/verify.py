#!/usr/bin/env python3
"""Verify P041's separable-density moments and audit FS2."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

import sympy as sp

from substrate_framework.governance import load_yaml
from substrate_framework.separable_moments import axisymmetric_separable_moments
from substrate_framework.sine_gordon import (
    breather_energy,
    breather_energy_second_moment,
)
from substrate_framework.tt_angular import (
    frobenius_inner_product,
    frobenius_norm_squared,
    tt_polarization_basis,
    tt_project_symmetric,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "9e9edbde8810a9040047d13e328eafbea992a218060de4d10a4118080f20cc31"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument(
        "--source-reproduction",
        type=Path,
        help="reuse a hash-matched durable reproduction record",
    )
    args = parser.parse_args()
    ledger = CheckLedger("P041-FS2")

    source_bytes = args.source_file.read_bytes()
    source_text = source_bytes.decode()
    source_words = " ".join(source_text.split())
    ledger.check(
        "the audited FS2 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    if args.source_reproduction is None:
        reproduction = subprocess.run(
            [sys.executable, str(args.source_file)],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        reproduction_exit = reproduction.returncode
        reproduction_tally = reproduction.stdout
    else:
        reproduction_record = load_yaml(args.source_reproduction)
        if reproduction_record.get("sha256") != EXPECTED_SOURCE_SHA256:
            raise ValueError("source reproduction record does not match FS2 hash")
        reproduction_exit = reproduction_record.get("exit_code")
        reproduction_tally = str(reproduction_record.get("terminal_tally", ""))
    ledger.check("FS2 exits cleanly", reproduction_exit == 0)
    ledger.check(
        "FS2's declared five-check tally reproduces",
        "ALL 5 CHECKS PASS" in reproduction_tally,
    )
    ledger.check(
        "FS2 uses the current trapezoid API with an older-version fallback",
        "np.trapezoid if hasattr(np, \"trapezoid\") else np.trapz" in source_text,
    )

    total, longitudinal, variance = sp.symbols(
        "M mu sigma2", positive=True, real=True
    )
    moments = axisymmetric_separable_moments(total, longitudinal, variance)
    transverse = total * variance
    difference = longitudinal - transverse
    normalized_expected = sp.diag(2 * difference / 3, -difference / 3, -difference / 3)
    triple_expected = sp.diag(2 * difference, -difference, -difference)
    ledger.check(
        "Fubini and centered axisymmetry give the exact diagonal second moment",
        moments.second_moment == sp.diag(longitudinal, transverse, transverse),
    )
    ledger.check(
        "the transverse input is per-axis variance rather than radial variance",
        moments.transverse_axis_second_moment == total * variance
        and sp.simplify(2 * moments.transverse_axis_second_moment - 2 * total * variance)
        == 0,
    )
    ledger.check(
        "the normalized STF and triple quadrupole conventions are exact",
        moments.trace_free_second_moment == normalized_expected
        and moments.triple_normalized_quadrupole == triple_expected
        and moments.triple_normalized_quadrupole
        == 3 * moments.trace_free_second_moment,
    )
    ledger.check(
        "both STF conventions are symmetric and traceless",
        moments.trace_free_second_moment == moments.trace_free_second_moment.T
        and sp.trace(moments.trace_free_second_moment) == 0
        and sp.trace(moments.triple_normalized_quadrupole) == 0,
    )

    time = sp.symbols("t", real=True)
    longitudinal_function = sp.Function("mu")(time)
    time_moments = axisymmetric_separable_moments(
        total,
        longitudinal_function,
        variance,
    )
    for order in (1, 2, 3):
        derivative = sp.diff(longitudinal_function, time, order)
        normalized_derivative = time_moments.trace_free_second_moment.diff(
            time,
            order,
        )
        triple_derivative = time_moments.triple_normalized_quadrupole.diff(
            time,
            order,
        )
        ledger.check(
            f"constant transverse width cancels from derivative order {order}",
            normalized_derivative
            == sp.diag(2 * derivative / 3, -derivative / 3, -derivative / 3)
            and triple_derivative
            == sp.diag(2 * derivative, -derivative, -derivative),
        )
    third = sp.diff(longitudinal_function, time, 3)
    normalized_third = time_moments.trace_free_second_moment.diff(time, 3)
    triple_third = time_moments.triple_normalized_quadrupole.diff(time, 3)
    ledger.check(
        "the third-derivative contractions retain the factor-nine convention ratio",
        sp.simplify(frobenius_norm_squared(normalized_third) - 2 * third**2 / 3)
        == 0
        and sp.simplify(frobenius_norm_squared(triple_third) - 6 * third**2)
        == 0,
    )

    special_frequency = 1 / sp.sqrt(2)
    special_moment = breather_energy_second_moment(special_frequency, time)
    special_third = sp.simplify(sp.diff(special_moment, time, 3))
    special_phase = sp.pi / (4 * special_frequency)
    ledger.check(
        "the accepted exact breather moment gives a nonzero special third derivative",
        sp.simplify(special_third.subs(time, special_phase) + sp.Rational(64, 3))
        == 0,
    )
    embedded_special = axisymmetric_separable_moments(
        breather_energy(special_frequency),
        special_moment,
        variance,
    )
    special_triple_third = embedded_special.triple_normalized_quadrupole.diff(
        time,
        3,
    )
    ledger.check(
        "the exact source specialization replaces FS2's same-data spectral reference",
        sp.simplify(
            special_triple_third
            - sp.diag(2 * special_third, -special_third, -special_third)
        )
        == sp.zeros(3)
        and sp.simplify(
            frobenius_norm_squared(special_triple_third).subs(time, special_phase)
            - sp.Rational(8192, 3)
        )
        == 0,
    )

    generic_derivative = sp.symbols("d", real=True)
    generic_tensor = sp.diag(
        2 * generic_derivative / 3,
        -generic_derivative / 3,
        -generic_derivative / 3,
    )
    axial_projection = tt_project_symmetric(generic_tensor, [1, 0, 0])
    perpendicular_projection = tt_project_symmetric(generic_tensor, [0, 0, 1])
    perpendicular_basis = tt_polarization_basis([0, 0, 1], [1, 0, 0])
    ledger.check(
        "viewing along the symmetry axis annihilates the axisymmetric STF derivative",
        axial_projection == sp.zeros(3),
    )
    ledger.check(
        "a perpendicular view leaves the exact linear plus tensor",
        perpendicular_projection
        == sp.diag(generic_derivative / 2, -generic_derivative / 2, 0)
        and sp.simplify(
            frobenius_inner_product(
                perpendicular_projection,
                perpendicular_basis.plus,
            )
            - generic_derivative / sp.sqrt(2)
        )
        == 0
        and frobenius_inner_product(
            perpendicular_projection,
            perpendicular_basis.cross,
        )
        == 0,
    )
    ledger.check(
        "adding arbitrary pure trace leaves every TT projection unchanged",
        sp.simplify(
            tt_project_symmetric(generic_tensor + sp.Function("c")(time) * sp.eye(3), [0, 0, 1])
            - perpendicular_projection
        )
        == sp.zeros(3),
    )

    def convention_predicate(candidate: object) -> bool:
        scale = sp.sympify(candidate)
        candidate_tensor = scale * normalized_third
        return sp.simplify(candidate_tensor - triple_third) == sp.zeros(3)

    ledger.mutation_sensitive(
        "triple-normalized STF scale",
        convention_predicate,
        3,
        [1, 2, 4],
    )

    def transverse_scale_predicate(candidate: object) -> bool:
        scale = sp.sympify(candidate)
        candidate_second = sp.diag(
            longitudinal,
            scale * total * variance,
            scale * total * variance,
        )
        return candidate_second == moments.second_moment

    ledger.mutation_sensitive(
        "per-axis transverse variance scale",
        transverse_scale_predicate,
        1,
        [sp.Rational(1, 2), 2, 3],
    )

    ledger.check(
        "FS2's Gaussian profile and width are declared in the audited source",
        "AXISYMMETRIC 3+1 EMBEDDING (DECLARED)" in source_text
        and "S_PERP = 0.8" in source_text,
    )
    ledger.check(
        "FS2's later P3D3 annotation cannot replace its own incompatible width",
        "sigma_perp^2 = <r^2>/3 = 3.84" in source_words
        and "The value below (0.64) is retained" in source_words,
    )
    ledger.check(
        "FS2's spectral reference reuses a sampled source moment rather than the accepted exact formula",
        "mu_spec = np.array([mu_of_t(tt) for tt in ts_spec])" in source_text
        and "Fmu = np.fft.rfft(mu_spec)" in source_text,
    )
    ledger.check(
        "FS2 supplies density algebra but no conserved 3+1 stress or field dynamics",
        "rho(x,y,z,t) = T_00(x,t) g_perp(y,z)" in source_words
        and "fixed normalized Gaussian g_perp" in source_words
        and "-> FS3 (the radiated power" in source_words
        and "partial_mu T" not in source_text
        and "T0i" not in source_text,
    )

    count = ledger.finish()
    print(f"P041 FS2 SEPARABLE-DENSITY STF AUDIT ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
