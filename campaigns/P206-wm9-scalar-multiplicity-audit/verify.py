#!/usr/bin/env python3
"""Primary exact verifier for WM9's scalar-multiplicity interpretation."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.normalized_overlaps import matched_width_sech_overlap
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-39/"
    "bridge_WM9_scalar_multiplicity_from_condensate.py"
)
SOURCE_SHA256 = "d0d94417f5abd572e2e306c1f33dc264d42cfef94e4281dbc258ea9fa83ffd4d"
RELEASE_SHA256 = "18dffeef5efd516018c918f65b45173c81ac0e1ba99fdd8a96274cc1df5c72db"
FORMULA_FREEZE_SHA256 = "d7e2a1a798471ca78d292990bacbe99c0ca658d7b40438007b64fa9a42be263b"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def free_symbol_count(expressions: list[sp.Expr]) -> int:
    return len(set().union(*(expression.free_symbols for expression in expressions)))


def main() -> int:
    checks = CheckLedger("P206-WM9-SCALAR-MULTIPLICITY")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.150.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml") == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source predicate inventory remains exact",
        len(source_checks) == 8
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references
        == compatibility.current_references
        == compatibility.eager_legacy_default_fallbacks
        == 0,
    )
    checks.check(
        "source scalar count is implemented as free-symbol cardinality",
        "n_condensates = len(amplitude_symbols)" in source_text
        and "amplitude_symbols |= (fs & {A})" in source_text,
    )
    checks.check(
        "source mode count is the length of a literal supplied tuple",
        "MODES = (1, 2, 3)" in source_text and "n_modes = len(MODES)" in source_text,
    )
    checks.check(
        "source three-condensate exclusion declares the symbols it later counts",
        "A1, A2, A3 = sp.symbols" in source_text
        and "three_condensate_amplitudes = {A1, A2, A3}" in source_text,
    )

    amplitude = sp.Symbol("A", real=True)
    kappa = sp.Symbol("kappa", positive=True)
    overlaps = [
        matched_width_sech_overlap(p, 1, amplitude, kappa).normalized_overlap
        for p in (1, 2, 3)
    ]
    checks.check(
        "canonical overlap API reproduces three distinct supplied-p profiles",
        len(set(overlaps)) == 3,
    )
    checks.check(
        "canonical overlaps are linear in one supplied amplitude",
        free_symbol_count(overlaps) == 1
        and all(sp.diff(value / amplitude, amplitude) == 0 for value in overlaps),
    )
    checks.check(
        "shared amplitude is an overlap premise rather than a species theorem",
        all(value.subs(amplitude, 0) == 0 for value in overlaps),
    )

    field_labels = ("H1", "H2", "H3")
    equal_profile_fields = {label: amplitude * sp.sech(kappa) for label in field_labels}
    checks.check(
        "three distinct field labels can share one amplitude symbol",
        len(equal_profile_fields) == 3
        and free_symbol_count(list(equal_profile_fields.values())) == 2,
    )
    equal_amplitude_values = [amplitude * overlaps[index] / amplitude for index in range(3)]
    checks.check(
        "three species with equality-constrained amplitudes reproduce one-symbol overlaps",
        len(field_labels) == 3 and free_symbol_count(equal_amplitude_values) == 1,
    )

    amplitudes = sp.symbols("A_1:4", real=True)
    unconstrained = [
        value.subs(amplitude, amplitudes[index]) for index, value in enumerate(overlaps)
    ]
    constrained = [
        value.subs({candidate: amplitude for candidate in amplitudes})
        for value in unconstrained
    ]
    checks.check(
        "equality substitution changes symbol count without changing field labels",
        free_symbol_count(unconstrained) == 3
        and free_symbol_count(constrained) == 1
        and len(field_labels) == 3,
    )

    couplings = sp.symbols("lambda_1:4", nonzero=True)
    one_field_mode_couplings = [
        couplings[index] * overlaps[index] for index in range(3)
    ]
    checks.check(
        "one field with three mode couplings can expose four free symbols",
        free_symbol_count(one_field_mode_couplings) == 4,
    )
    checks.check(
        "an inert field is a zero-symbol counterexample to symbol-count ontology",
        free_symbol_count([sp.Integer(0)]) == 0,
    )

    # A change of coordinates can expose or eliminate symbols while the number of
    # declared field labels stays fixed.  The physical multiplicity therefore needs
    # a separately typed action/representation ledger.
    common, delta_1, delta_2 = sp.symbols("A_common delta_1 delta_2", real=True)
    reparameterized = [common, common + delta_1, common + delta_2]
    symmetric_slice = [value.subs({delta_1: 0, delta_2: 0}) for value in reparameterized]
    checks.check(
        "a symmetric parameter slice collapses three coordinates to one",
        free_symbol_count(reparameterized) == 3
        and free_symbol_count(symmetric_slice) == 1,
    )

    claims = {
        claim["id"]: claim for claim in load(ROOT / "governance/claims.yaml")["claims"]
    }
    checks.check(
        "accepted Q-ball claim explicitly rejects forced complex ontology and stability",
        "no VK, spectral, orbital, or nonlinear stability, forced complex ontology"
        in claims["C-QBL-001"]["statement"],
    )
    checks.check(
        "accepted scalar Hessian claim rejects generations and flavor towers",
        "not positive particle masses or generations" in claims["C-QBL-003"]["statement"]
        and "flavor tower" in claims["C-QBL-003"]["statement"],
    )
    checks.check(
        "accepted overlap claim rejects Yukawa generation and physical condensate maps",
        all(
            phrase in claims["C-OVL-001"]["statement"]
            for phrase in ("no fermion", "Yukawa interaction", "physical condensate", "generation assignment")
        ),
    )
    checks.check(
        "accepted phase count rejects an observed family-count map",
        "no quark or generation map" in claims["C-MIX-002"]["statement"]
        and "observed family count" in claims["C-MIX-002"]["statement"],
    )
    checks.check(
        "accepted gauge-scalar mass claim retains a supplied vacuum and no condensate ontology",
        "supplied generators" in claims["C-GSM-001"]["statement"]
        and "declared vacuum" in claims["C-GSM-001"]["statement"]
        and "condensate" in claims["C-GSM-001"]["statement"],
    )
    checks.check(
        "accepted beta ledger types scalar multiplicity as supplied field-table data",
        "positive integer multiplicity m_r" in claims["C-RGE-005"]["statement"]
        and "one declared complex scalar doublet" in claims["C-RGE-005"]["statement"]
        and "field-content or anomaly derivation" in claims["C-RGE-005"]["statement"],
    )
    checks.check(
        "accepted finite-representation ledger leaves the table and physical matter supplied",
        "separately supplied nonempty finite table" in claims["C-REP-003"]["statement"]
        and "physical matter" in claims["C-REP-003"]["statement"],
    )
    checks.check(
        "no accepted scalar-multiplicity derivation claim has been smuggled into the registry",
        "C-OVL-004" not in claims and "C-RGE-008" not in claims,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
