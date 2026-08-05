#!/usr/bin/env python3
"""Current-NumPy compatibility and information-closure audit for CF5."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import numpy as np
import sympy as sp
import yaml

from substrate_framework.abelian_higgs_vortex import (
    VortexParameters,
    asymptotic_masses,
    quantized_flux,
    solve_vortex_bvp,
    vortex_tension,
)
from substrate_framework.flux_tube import tube_energy_slope
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-10/"
    "bridge_CF5_flux_tube_tension_consistency.py"
)
DOSSIER = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-10/dossiers/CF5-dossier.md"
)

PINNED_HASHES = {
    SOURCE: "0a449f8b95bc0a83fb0316992fb0d1776a6157e1445029623b4608246dc256f7",
    DOSSIER: "bd499ab50a04c45d3a80167a5a20b75067b8eecff5bfe11d992270e94ba95305",
    ROOT / "src/substrate_framework/abelian_higgs_vortex.py":
        "d816938fc091ee4641bec7f193e4b9e083131f6d5193c4870b910ee3d1e93d99",
    ROOT / "src/substrate_framework/flux_tube.py":
        "372c4bebc93231de8bbc99dea1f8494bc2b730e4983a12158d661f48b862d034",
    ROOT / "src/substrate_framework/numerics.py":
        "a6271efbb5c5694cf05cfdd5a67b126ad4ebe8eaf432ba90c715c306a125afe1",
    ROOT / "src/substrate_framework/source_audit.py":
        "ee24c7a236dc6b8f70bba3d6cefb42f9b4ca5b206f1643de09438cf61a648cf7",
    ROOT / "tests/test_abelian_higgs_vortex.py":
        "534af58c5e007de4a526027f2d7f3496526645edc82273794e520d070ab2ce46",
    ROOT / "tests/test_flux_tube.py":
        "d20a455d8721b55c4cbf733e421c60b8fcdac48948d72ded5a460a495a3189b4",
    ROOT / "tests/test_numerics.py":
        "1907c3b03bb9d9f6490ace46f0000e3436a0ca9010d1666514cd88a46a2f87d0",
    ROOT / "tests/test_source_audit.py":
        "4d7c6009b2beeac3fa5cc71aeb4434c57494f7157690253bcf9e5e9059b6ef3f",
    ROOT / "campaigns/P026-abelian-higgs-vortex/verify.py":
        "b4d06baaeb3a196185f58c526b1b423a191a8d1f3a8c973feea9357d90291ed1",
    ROOT / "campaigns/P026-abelian-higgs-vortex/reviews/independent_finite_difference_review.py":
        "eea4cebeb7493383369cfcf38f2e338cf1fe1899a7a7444b1d3244801143f359",
    ROOT / "campaigns/P026-abelian-higgs-vortex/attempts/0004/result.yaml":
        "2e823dca1e0adbccb6866ccea21076aeea603a5cffd733314b7fd581d4b7b1af",
    ROOT / "campaigns/P029-cf5-tension-consistency-audit/verify.py":
        "c67d82355a523b598fa78b363154f0c27801f5452f26093b464a7b97d0398e80",
    ROOT / "campaigns/P029-cf5-tension-consistency-audit/reviews/independent_information_review.py":
        "0b14766fff63bccf50df9ea71a47963fed282faa883fbccfcc1c7c0e21f787cf",
}


@dataclass(frozen=True)
class InversionConvention:
    area_coefficient: sp.Expr
    energy_coefficient: sp.Expr


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_source(*, alias: bool) -> subprocess.CompletedProcess[str]:
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    if alias:
        code = (
            "import runpy; import numpy as np; "
            "setattr(np, 'trapz', np.trapezoid); "
            f"runpy.run_path({str(SOURCE)!r}, run_name='__main__')"
        )
        command = [sys.executable, "-c", code]
    else:
        command = [sys.executable, str(SOURCE)]
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
        timeout=120,
    )


def main() -> int:
    checks = CheckLedger("P170-CF5-CURRENT-NUMPY-INFORMATION-CLOSURE")
    for path, expected in PINNED_HASHES.items():
        checks.check(
            f"pinned artifact {path.name} retains its audited bytes",
            _digest(path) == expected,
        )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    check_calls = sorted(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    labels = [
        re.match(r"(CF5\.[1-6])", ast.literal_eval(node.args[0])).group(1)
        for node in check_calls
    ]
    checks.check(
        "CF5 has exactly its six advertised lexical predicates in order",
        labels == ["CF5.1", "CF5.2", "CF5.3", "CF5.4", "CF5.5", "CF5.6"],
    )
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from = {
        (node.module, alias.name)
        for node in tree.body
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    checks.check(
        "CF5 has two assertions and its exact direct import surface",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 2
        and imports == {"numpy", "sympy"}
        and imported_from == {("scipy.integrate", "solve_bvp")},
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "CF5 has one executable legacy integration call and no eager fallback",
        compatibility.numpy_aliases == ("np",)
        and compatibility.legacy_references == 1
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = _run_source(alias=False)
    if hasattr(np, "trapz"):
        native_shape_ok = (
            native.returncode == 0
            and native.stderr == ""
            and native.stdout.count("  PASS\n") == 6
            and "ALL 6 CHECKS PASS" in native.stdout
        )
    else:
        native_shape_ok = (
            native.returncode != 0
            and native.stdout.count("  PASS\n") == 0
            and "AttributeError" in native.stderr
            and "has no attribute 'trapz'" in native.stderr
        )
    checks.check(
        "native CF5 outcome is exactly predicted by the installed NumPy name surface",
        native_shape_ok,
    )
    replay = _run_source(alias=True)
    checks.check(
        "an isolated legacy alias backed only by np.trapezoid restores clean execution",
        callable(np.trapezoid)
        and replay.returncode == 0
        and replay.stderr == ""
        and replay.stdout.count("  PASS\n") == 6
        and "ALL 6 CHECKS PASS" in replay.stdout,
        replay.stderr[-500:],
    )
    checks.check(
        "the compatibility replay retains the source numerical diagnostics",
        "sigma_CF1 N=400: 4.211567" in replay.stdout
        and "N=800: 4.211567" in replay.stdout
        and "A_eff/lambda_pen^2 = 4.686904" in replay.stdout,
    )

    winding = sp.symbols("n", integer=True, positive=True)
    gauge, vacuum, coupling, tension = sp.symbols(
        "g v lambda sigma", positive=True
    )
    flux = quantized_flux(winding, gauge)
    vector_mass, scalar_mass = asymptotic_masses(vacuum, coupling, gauge)
    penetration_length = sp.simplify(1 / vector_mass)
    scalar_length = sp.simplify(1 / scalar_mass)
    effective_area = sp.simplify(flux**2 / (2 * tension))
    checks.check(
        "accepted flux and supplied tension define the inverted area exactly",
        flux == 2 * sp.pi * winding / gauge
        and effective_area
        == 2 * sp.pi**2 * winding**2 / (gauge**2 * tension),
    )
    checks.check(
        "back-substitution reconstructs the supplied tension for all positive inputs",
        sp.simplify(tube_energy_slope(flux, effective_area) - tension) == 0
        and sp.diff(effective_area, tension) != 0,
    )

    def inversion_closes(candidate: object) -> bool:
        assert isinstance(candidate, InversionConvention)
        area = sp.simplify(candidate.area_coefficient * flux**2 / tension)
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
        "every positive alternative tension passes the same inversion round trip",
        sp.simplify(tube_energy_slope(flux, alternative_area) - alternative_tension)
        == 0
        and sp.simplify(alternative_area - effective_area) != 0,
    )

    penetration_ratio = sp.simplify(effective_area / penetration_length**2)
    checks.check(
        "the penetration-area ratio is only a transform of the supplied tension",
        penetration_ratio
        == 2 * sp.pi**2 * winding**2 * vacuum**2 / tension
        and gauge not in penetration_ratio.free_symbols,
    )
    ratio_symbol = sp.symbols("r_core", positive=True)
    checks.check(
        "without an independent area ratio the transform constrains no tension",
        sp.solve(sp.Eq(penetration_ratio, ratio_symbol), tension)
        == [2 * sp.pi**2 * vacuum**2 * winding**2 / ratio_symbol],
    )
    lower, upper = sp.Rational(1, 10), sp.Integer(100)
    lower_tension = sp.simplify(2 * sp.pi**2 * winding**2 * vacuum**2 / upper)
    upper_tension = sp.simplify(2 * sp.pi**2 * winding**2 * vacuum**2 / lower)
    checks.check(
        "CF5's declared ratio window accepts a factor-one-thousand tension interval",
        sp.simplify(upper_tension / lower_tension) == 1000,
    )
    accepted_demo_tension = sp.Rational(4211567, 1_000_000)

    def in_source_window(candidate_tension: sp.Expr) -> bool:
        candidate_ratio = sp.N(
            penetration_ratio.subs(
                {winding: 1, vacuum: 1, tension: candidate_tension}
            ),
            30,
        )
        return bool(lower < candidate_ratio < upper)

    checks.check(
        "the replayed demo tension reproduces CF5's reported transformed ratio",
        abs(
            float(
                penetration_ratio.subs(
                    {winding: 1, vacuum: 1, tension: accepted_demo_tension}
                )
            )
            - 4.686904
        )
        < 1.0e-6,
    )
    checks.check(
        "one-tenth tenfold and fortyfold tension mutations all pass CF5's window",
        in_source_window(accepted_demo_tension / 10)
        and in_source_window(accepted_demo_tension * 10)
        and in_source_window(accepted_demo_tension * 40),
    )
    checks.check(
        "CF5's selected thousand-scale mutation fails only the broad window",
        not in_source_window(sp.Integer(1000)),
    )
    checks.check(
        "the declared vortex has two inequivalent inverse-length area conventions",
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
        "an unfixed geometric area convention rescales the comparison freely",
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

    parameters = VortexParameters()
    solution = solve_vortex_bvp(
        parameters,
        outer_radius=20.0,
        initial_points=120,
        tolerance=1.0e-8,
    )
    canonical_tension = vortex_tension(solution, quadrature_points=20_001)
    checks.check(
        "the current canonical np.trapezoid-backed path reproduces accepted BVP evidence",
        solution.evidence.max_rms_residual < 1.1e-8
        and abs(canonical_tension - 4.21160) < 5.0e-5,
    )

    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    accepted = {claim["id"]: claim for claim in registry["claims"]}
    vortex_exact = accepted["C-VTX-001"]
    vortex_numeric = accepted["C-VTX-002"]
    tube = accepted["C-FLX-001"]
    checks.check(
        "the accepted vortex claims retain their conditional non-confinement ceiling",
        vortex_exact["dependencies"] == []
        and vortex_numeric["dependencies"] == ["C-VTX-001"]
        and "no substrate, dual" in vortex_exact["statement"]
        and "not a continuum existence or uniqueness theorem" in vortex_numeric["statement"],
    )
    checks.check(
        "the accepted tube claim already adjudicates CF5's inversion as non-predictive",
        tube["dependencies"] == []
        and "Matching a supplied tension by A_eff=Phi^2/(2*sigma) defines" in tube["statement"]
        and "does not predict it" in tube["statement"]
        and "no physical charge, flux tube, vortex-tension identity" in tube["statement"],
    )

    total = checks.finish()
    print(f"P170 CF5 CURRENT-NUMPY INFORMATION CLOSURE ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
