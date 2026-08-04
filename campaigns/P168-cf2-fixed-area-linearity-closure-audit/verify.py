#!/usr/bin/env python3
"""Exact accepted-composition and source qualification audit for CF2."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import sympy as sp
import yaml

from substrate_framework.flux_tube import (
    charge_for_slope_equality,
    endpoint_force_slope,
    endpoint_potential,
    spherical_field,
    tube_energy_slope,
    tube_field_energy,
    uniform_tube_field,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-10/"
    "bridge_CF2_linear_potential.py"
)
DOSSIER = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-10/dossiers/CF2-dossier.md"
)

PINNED_HASHES = {
    SOURCE: "e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a",
    DOSSIER: "b88a66e7b4bba4a886ea87d5a88ff6dcaac20ec99b1e9c556198b4c7dc2e79e1",
    ROOT / "src/substrate_framework/flux_tube.py":
        "372c4bebc93231de8bbc99dea1f8494bc2b730e4983a12158d661f48b862d034",
    ROOT / "tests/test_flux_tube.py":
        "d20a455d8721b55c4cbf733e421c60b8fcdac48948d72ded5a460a495a3189b4",
    ROOT / "campaigns/P027-fixed-flux-tube-linearity/verify.py":
        "2eb02b262e92b59214f083cf6f38268362ef9572a677f0e75071231dbf852e12",
    ROOT / "campaigns/P027-fixed-flux-tube-linearity/reviews/independent_work_energy_review.py":
        "1413ddd12667c4dad93113610dfcf621a9634c310dc2407479a2fc8f8566dc70",
    ROOT / "campaigns/P027-fixed-flux-tube-linearity/attempts/0001/result.yaml":
        "994e99f891edcf1004dfc6c4fce0278a30afae78020a0b43fe4587ee88c7bb48",
}


@dataclass(frozen=True)
class EnergyConvention:
    density_coefficient: sp.Expr
    area_power: int


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _native_source() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SOURCE)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def main() -> int:
    checks = CheckLedger("P168-CF2-FIXED-AREA-CLOSURE")

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
        re.match(r"(CF2\.[iv]+-[a-z])", ast.literal_eval(node.args[0])).group(1)
        for node in check_calls
    ]
    checks.check(
        "CF2 has exactly its fifteen advertised lexical predicates in order",
        labels
        == [
            "CF2.i-a", "CF2.i-b", "CF2.ii-a", "CF2.ii-b", "CF2.ii-c",
            "CF2.iii-a", "CF2.iii-b", "CF2.iii-c", "CF2.iv-a",
            "CF2.iv-b", "CF2.iv-c", "CF2.v-a", "CF2.v-b", "CF2.v-c",
            "CF2.v-d",
        ],
    )
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "CF2 has one ledger assertion and imports only SymPy",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1
        and imports == {"sympy"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "CF2 has no executable NumPy trapezoidal integration surface",
        compatibility.numpy_aliases == ()
        and compatibility.legacy_references == 0
        and compatibility.current_references == 0,
    )

    native = _native_source()
    checks.check(
        "hash-pinned CF2 exits cleanly without a compatibility alias",
        native.returncode == 0 and native.stderr == "",
    )
    checks.check(
        "native CF2 executes exactly fifteen predicates and its terminal tally",
        native.stdout.count("  PASS\n") == 15
        and "ALL 15 CHECKS PASS" in native.stdout,
    )

    flux, area, charge, length = sp.symbols("Phi A q L", positive=True)
    field = uniform_tube_field(flux, area)
    energy_slope = tube_energy_slope(flux, area)
    energy = tube_field_energy(length, flux, area)
    force_slope = endpoint_force_slope(charge, flux, area)
    work = endpoint_potential(length, charge, flux, area)
    checks.check(
        "accepted fixed-area Gauss data give a constant uniform field",
        field == flux / area
        and sp.simplify(field * area - flux) == 0
        and sp.diff(field, length) == 0,
    )
    checks.check(
        "accepted field energy is linear with slope Phi squared over two A",
        energy_slope == flux**2 / (2 * area)
        and energy == energy_slope * length
        and sp.diff(energy, length) == energy_slope
        and sp.diff(energy, length, 2) == 0,
    )

    def energy_convention_matches(candidate: object) -> bool:
        assert isinstance(candidate, EnergyConvention)
        candidate_field = flux / area**candidate.area_power
        return (
            sp.simplify(candidate_field * area - flux) == 0
            and sp.simplify(
                candidate.density_coefficient * candidate_field**2 * area
                - flux**2 / (2 * area)
            )
            == 0
        )

    checks.mutation_sensitive(
        "one-half coefficient and Gauss area power",
        energy_convention_matches,
        EnergyConvention(sp.Rational(1, 2), 1),
        [
            EnergyConvention(sp.Integer(1), 1),
            EnergyConvention(sp.Rational(1, 4), 1),
            EnergyConvention(sp.Rational(1, 2), 2),
        ],
    )
    checks.check(
        "endpoint work is separately linear with slope q Phi over A",
        force_slope == charge * flux / area
        and work == force_slope * length
        and sp.diff(work, length) == force_slope
        and sp.diff(work, length, 2) == 0,
    )
    checks.check(
        "energy and endpoint slopes agree if and only if q equals Phi over two",
        sp.solve(sp.Eq(energy_slope, force_slope), charge) == [flux / 2]
        and charge_for_slope_equality(flux) == flux / 2,
    )
    checks.check(
        "q equals Phi is an exact factor-two counterexample",
        endpoint_force_slope(flux, flux, area) == 2 * energy_slope,
    )
    checks.mutation_sensitive(
        "charge-flux equality premise",
        lambda candidate: sp.simplify(
            endpoint_force_slope(candidate, flux, area) - energy_slope
        )
        == 0,
        flux / 2,
        [flux, flux / 4],
    )

    energy_assignments = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "V_tube" for target in node.targets)
    ]
    checks.check(
        "CF2's executable tube-energy path never consumes endpoint charge q",
        energy_assignments
        and all(
            not any(isinstance(descendant, ast.Name) and descendant.id == "q" for descendant in ast.walk(node.value))
            for node in energy_assignments
        )
        and charge not in energy.free_symbols,
    )

    area0, length0, coordinate = sp.symbols("A0 L0 x", positive=True)
    expanding_area = area0 * (1 + coordinate / length0)
    expanding_energy = sp.integrate(
        flux**2 / (2 * expanding_area), (coordinate, 0, length)
    )
    checks.check(
        "an expanding area gives logarithmic rather than linear field energy",
        sp.simplify(
            expanding_energy
            - flux**2 * length0 * sp.log(1 + length / length0) / (2 * area0)
        )
        == 0
        and sp.diff(expanding_energy, length, 2) != 0,
    )

    def energy_is_linear(candidate_area: object) -> bool:
        candidate = sp.sympify(candidate_area)
        candidate_energy = sp.integrate(
            flux**2 / (2 * candidate), (coordinate, 0, length)
        )
        return sp.simplify(sp.diff(candidate_energy, length, 2)) == 0

    checks.mutation_sensitive(
        "fixed cross-section premise",
        energy_is_linear,
        area0,
        [area0 * (1 + coordinate / length0), area0 * sp.exp(coordinate / length0)],
    )

    radius = sp.symbols("r", positive=True)
    radial_field = spherical_field(flux, radius)
    coulomb = charge * flux / (4 * sp.pi * radius)
    checks.check(
        "spherical spreading gives the exact nonconstant inverse-square guard",
        radial_field == flux / (4 * sp.pi * radius**2)
        and sp.diff(radial_field, radius) != 0,
    )
    checks.check(
        "the separate Coulomb potential is curved and vanishes at infinity",
        sp.diff(coulomb, radius, 2) != 0
        and sp.limit(coulomb, radius, sp.oo) == 0,
    )

    supplied_tension = sp.symbols("sigma", positive=True)
    effective_area = flux**2 / (2 * supplied_tension)
    checks.check(
        "effective-area inversion reconstructs rather than predicts supplied tension",
        sp.simplify(tube_energy_slope(flux, effective_area) - supplied_tension) == 0
        and sp.diff(effective_area, supplied_tension) != 0,
    )
    checks.check(
        "the Riesz row in CF2 is exponent arithmetic rather than an imported mechanism",
        2 * 1 - 1 == 1
        and 2 * 1 - 1 - 1 == 0
        and all(
            token not in source_text
            for token in ("import bridge_EM7", "from bridge_EM7", "import bridge_EM3", "from bridge_EM3")
        ),
    )
    checks.check(
        "CF2 imports no CF1 CF5 or QCD implementation",
        all(
            token not in source_text
            for token in (
                "import bridge_CF1", "from bridge_CF1", "import bridge_CF5",
                "from bridge_CF5", "import bridge_QCD3", "from bridge_QCD3",
            )
        ),
    )

    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    accepted = next(claim for claim in registry["claims"] if claim["id"] == "C-FLX-001")
    checks.check(
        "C-FLX-001 is the dependency-free accepted claim for the surviving algebra",
        accepted["verification"] == "symbolic_verified"
        and accepted["review"] == "accepted"
        and accepted["dependencies"] == [],
    )
    checks.check(
        "the accepted statement explicitly separates slopes and excludes physical overreach",
        "q=Phi/2" in accepted["statement"]
        and "endpoint work" in accepted["statement"]
        and "field energy" in accepted["statement"]
        and "no physical charge" in accepted["statement"]
        and "QCD" in accepted["statement"]
        and "confinement" in accepted["statement"],
    )

    total = checks.finish()
    print(f"P168 CF2 FIXED-AREA CLOSURE ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
