#!/usr/bin/env python3
"""Exact accepted-composition and source qualification audit for CF3."""

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

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su3 import (
    center_conjugation,
    center_element,
    center_elements,
    fundamental_commutant_basis,
    fundamental_generators,
    triality_phase,
)
from substrate_framework.verification import CheckLedger
from substrate_framework.wilson_loops import (
    rectangular_area_law,
    rectangular_perimeter_law,
    static_potential_from_loop,
)


ROOT = Path("/home/dan/substrate-framework")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-10/"
    "bridge_CF3_wilson_area_law.py"
)
DOSSIER = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-10/dossiers/CF3-dossier.md"
)

PINNED_HASHES = {
    SOURCE: "8655579ef3173730c315d60aa821f7085cc131920ae49cb93c60b075d884889d",
    DOSSIER: "bc60b4f1fe46a8a38646839c398ad4c31b203518907ff7853a99fb1f22db3cae",
    ROOT / "src/substrate_framework/su3.py":
        "fb2b2b595875ae61202788418ba4d7f6da5372e97e799e43919ad6d97bc4f169",
    ROOT / "src/substrate_framework/wilson_loops.py":
        "11d23ce301a9dac97079c5128bef285a6f79791cdbb2190e36ffbc3ef9d7f484",
    ROOT / "tests/test_su3.py":
        "eeb1edaf734737c60867d8a7bffe9a6e0bcdd596b820bf7bc0cb3157d8168eae",
    ROOT / "tests/test_wilson_loops.py":
        "6789abd327e16013d206c9679cf1cafb411b371029bb62685d9ef924a69248a1",
    ROOT / "campaigns/P028-su3-center-wilson/verify.py":
        "d6d3434da47816d12a9747b2630b448caa66f00429e73128f867407d3251c85b",
    ROOT / "campaigns/P028-su3-center-wilson/reviews/independent_center_wilson_review.py":
        "1d30dfb5682951c37807b0990b22384c84e8ea057d8c6e510cad33de435cc4f1",
    ROOT / "campaigns/P028-su3-center-wilson/attempts/0001/result.yaml":
        "c65dc64a0911268930464798b7feeb99eafe003cde2aaf166d35a0ec6eb1f770",
}


@dataclass(frozen=True)
class CenterCandidate:
    phase: sp.Expr
    order: int


@dataclass(frozen=True)
class RepresentationCandidate:
    fundamental_phase: sp.Expr
    adjoint_phase: sp.Expr


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
    checks = CheckLedger("P169-CF3-CENTER-WILSON-CLOSURE")
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
        re.match(r"(CF3\.[1-6])", ast.literal_eval(node.args[0])).group(1)
        for node in check_calls
    ]
    checks.check(
        "CF3 has exactly its six advertised lexical predicates in order",
        labels == ["CF3.1", "CF3.2", "CF3.3", "CF3.4", "CF3.5", "CF3.6"],
    )
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "CF3 has one ledger assertion and imports only SymPy",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1
        and imports == {"sympy"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "CF3 has no executable NumPy trapezoidal integration surface",
        compatibility.numpy_aliases == ()
        and compatibility.legacy_references == 0
        and compatibility.current_references == 0,
    )
    native = _native_source()
    checks.check(
        "hash-pinned CF3 exits cleanly without a compatibility alias",
        native.returncode == 0 and native.stderr == "",
    )
    checks.check(
        "native CF3 executes exactly six predicates and its terminal tally",
        native.stdout.count("  PASS\n") == 6
        and "ALL 6 CHECKS PASS" in native.stdout,
    )

    generators = fundamental_generators()
    gram = sp.Matrix(
        8, 8, lambda a, b: sp.trace(generators[a] * generators[b])
    )
    checks.check(
        "the accepted fundamental generator convention is exact",
        gram == sp.eye(8) / 2
        and all(sp.trace(generator) == 0 for generator in generators),
    )
    commutant = fundamental_commutant_basis()
    checks.check(
        "the full complex fundamental commutant is one-dimensional and scalar",
        commutant == (sp.eye(3),),
    )
    elements = center_elements()
    checks.check(
        "unitarity and determinant one leave exactly three distinct center elements",
        len(elements) == 3
        and len({sp.srepr(element) for element in elements}) == 3
        and all(
            sp.simplify(element.H * element) == sp.eye(3)
            and sp.simplify(element.det()) == 1
            for element in elements
        ),
    )
    checks.check(
        "every center element commutes and multiplication closes modulo three",
        all(
            element * generator == generator * element
            for element in elements
            for generator in generators
        )
        and all(
            sp.simplify(
                center_element(a) * center_element(b) - center_element(a + b)
            )
            == sp.zeros(3)
            for a in range(3)
            for b in range(3)
        ),
    )

    omega = center_element(1)[0, 0]

    def is_nontrivial_center(candidate: object) -> bool:
        assert isinstance(candidate, CenterCandidate)
        matrix = sp.simplify(candidate.phase) * sp.eye(3)
        return bool(
            candidate.order == 3
            and matrix != sp.eye(3)
            and sp.simplify(matrix.H * matrix) == sp.eye(3)
            and sp.simplify(matrix.det()) == 1
            and sp.simplify(matrix**candidate.order) == sp.eye(3)
        )

    checks.mutation_sensitive(
        "center phase determinant and exact order",
        is_nontrivial_center,
        CenterCandidate(omega, 3),
        [
            CenterCandidate(-1, 3),
            CenterCandidate(sp.I, 3),
            CenterCandidate(omega, 2),
        ],
    )
    scalar = sp.symbols("z")
    determinant_roots = sp.solve(
        sp.Eq((scalar * sp.eye(3)).det(), 1), scalar
    )
    checks.check(
        "the scalar commutant and determinant constraint prove center completeness",
        len(determinant_roots) == 3
        and all(sp.simplify(root**3 - 1) == 0 for root in determinant_roots)
        and all(sp.simplify(sp.conjugate(root) * root) == 1 for root in determinant_roots),
    )

    vector = sp.Matrix(sp.symbols("v0:3"))
    generic_matrix = sp.Matrix(3, 3, sp.symbols("x0:9"))
    checks.check(
        "fundamental action has phase omega while center conjugation is trivial",
        center_element() * vector == omega * vector
        and triality_phase(1) == omega
        and center_conjugation(generic_matrix) == generic_matrix
        and triality_phase(0) == 1,
    )
    checks.check(
        "abstract triality characters compose modulo three",
        all(
            sp.simplify(triality_phase(a) * triality_phase(b))
            == triality_phase(a + b)
            for a in range(3)
            for b in range(3)
        ),
    )

    def representation_matches(candidate: object) -> bool:
        assert isinstance(candidate, RepresentationCandidate)
        return bool(
            sp.simplify(candidate.fundamental_phase - omega) == 0
            and sp.simplify(candidate.adjoint_phase - 1) == 0
            and sp.simplify(candidate.fundamental_phase - candidate.adjoint_phase)
            != 0
        )

    checks.mutation_sensitive(
        "abstract fundamental and adjoint center characters",
        representation_matches,
        RepresentationCandidate(omega, sp.Integer(1)),
        [
            RepresentationCandidate(sp.Integer(1), sp.Integer(1)),
            RepresentationCandidate(omega, omega),
        ],
    )

    separation, duration, tension, perimeter = sp.symbols(
        "R T sigma rho", positive=True
    )
    area_loop = rectangular_area_law(separation, duration, tension)
    area_potential = static_potential_from_loop(area_loop, duration)
    checks.check(
        "the separately declared area law conditionally extracts a linear potential",
        area_loop == sp.exp(-tension * separation * duration)
        and area_potential == tension * separation
        and sp.diff(area_potential, separation) == tension
        and sp.diff(area_potential, separation, 2) == 0,
    )

    def extracts_declared_area(candidate: object) -> bool:
        expression = sp.sympify(candidate)
        potential = static_potential_from_loop(expression, duration)
        return bool(
            sp.simplify(potential - tension * separation) == 0
            and sp.diff(potential, separation) == tension
        )

    checks.mutation_sensitive(
        "area-law sign product and separation dependence",
        extracts_declared_area,
        area_loop,
        [
            sp.exp(tension * separation * duration),
            sp.exp(-tension * (separation + duration)),
            sp.exp(-tension * duration),
        ],
    )
    perimeter_loop = rectangular_perimeter_law(
        separation, duration, perimeter
    )
    perimeter_potential = static_potential_from_loop(perimeter_loop, duration)
    checks.check(
        "the separately declared perimeter law conditionally extracts a bounded potential",
        perimeter_loop == sp.exp(-2 * perimeter * (separation + duration))
        and perimeter_potential == 2 * perimeter
        and sp.diff(perimeter_potential, separation) == 0,
    )
    checks.check(
        "the same center algebra is compatible with both distinct loop premises",
        commutant == (sp.eye(3),)
        and area_potential != perimeter_potential
        and sp.diff(area_potential, separation)
        != sp.diff(perimeter_potential, separation),
    )
    checks.check(
        "the center derivation contains no loop-law parameter",
        not set().union(*(entry.free_symbols for element in elements for entry in element)).intersection(
            {separation, duration, tension, perimeter}
        ),
    )
    checks.check(
        "CF3 declares rather than derives both loop expectations",
        "DECLARED" in source_text
        and "the area-law model is <W>=exp(-sigma R T)" in source_text
        and "the perimeter-law model <W>=exp(-rho 2(R+T))" in source_text,
    )
    checks.check(
        "CF3 imports none of its narrative neighbors or sibling tension constructions",
        all(
            token not in source_text
            for label in ("CF1", "CF2", "CF4", "EM7", "NA1", "QCD1", "SM3")
            for token in (f"import bridge_{label}", f"from bridge_{label}")
        ),
    )
    checks.check(
        "CF3 sigma remains a free premise with no accepted CF1 or CF2 identity",
        tension in area_potential.free_symbols
        and not any(symbol in area_potential.free_symbols for symbol in sp.symbols("Phi A q")),
    )

    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    accepted = {claim["id"]: claim for claim in registry["claims"]}
    center_claim = accepted["C-LIE-002"]
    loop_claim = accepted["C-WIL-001"]
    checks.check(
        "C-LIE-002 has exactly the accepted representation dependency and scope",
        center_claim["dependencies"] == ["C-LIE-001"]
        and center_claim["verification"] == "symbolic_verified"
        and center_claim["review"] == "accepted"
        and "no substrate field assignment" in center_claim["statement"],
    )
    checks.check(
        "C-WIL-001 is dependency-free premise-explicit accepted algebra",
        loop_claim["dependencies"] == []
        and loop_claim["verification"] == "symbolic_verified"
        and loop_claim["review"] == "accepted"
        and "conditional on the separately declared" in loop_claim["statement"]
        and "derive neither" in loop_claim["statement"],
    )

    total = checks.finish()
    print(f"P169 CF3 CENTER/WILSON CLOSURE ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
