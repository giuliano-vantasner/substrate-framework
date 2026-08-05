#!/usr/bin/env python3
"""Primary exact and adversarial verifier for the P195 WN7 audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import re

import sympy as sp

from substrate_framework.source_audit import (
    audit_numpy_trapezoid_compatibility,
    audit_source_tokens,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = Path("/home/dan/substrate/merged-framework/bridges/phase-37")
SOURCE = SOURCE_ROOT / "bridge_WN7_honesty_firewall_guard.py"
SOURCE_SHA256 = "88844689bf682ca5ff524378f4e5e46a25bcab54b1a3a6e59afe69b990694d50"
RELEASE_SHA256 = "b995916d6e708d29f0f493562741d7ba35bc202ce2784f4aaed7d1dfd5232a0a"
WN_HASHES = {
    "bridge_WN1_vertex_coefficient_magnitude.py":
        "3764b29955c3bd51c10278159e08a52ff616a7041510e56917b091f1a802cdde",
    "bridge_WN2_coefficient_cannot_be_the_weight.py":
        "dc9a7dbd79c908d1ec206392cdd81a34b5a39c08dcba31f2c164c3d92073504c",
    "bridge_WN3_amplitude_scale_and_multiplicity.py":
        "8a13c8b2af4d89297a11b3ef7460cc1f35fe274dc4affb2b9a7d3649bc237e88",
    "bridge_WN4_derived_weight_and_crossover.py":
        "2377bb4ba817cd20c188d4adeeeb9169253e9b1231477ac2069b36cc923fc7e2",
    "bridge_WN5_gb4_preserved_and_new_prediction.py":
        "5618ba007e041512a7d207026dc6369c8277312acba4c250219a1629585a7fbc",
    "bridge_WN6_scale_verdict_and_missing_bridge.py":
        "07f049bac9eb99cb29ef6c3cd333aaecddc17492a73a8fc2aac7eb140ebcab10",
}
IMPORT_MARK = "[IMPORT]"
FORBIDDEN_BARRIER = ("u_e", "gamow", "screening_enhancement", "gamow_energy_kev")
FORBIDDEN_IMPORTS = ("0.0362", "90.35", "0.999757")
FORBIDDEN_EMPIRICAL = (
    "excess_heat_watts",
    "cop_measured",
    "transmutation_yield",
)
UNIT_TOKENS = (
    "ev", "mev", "kev", "joule", "watt", "kelvin", "hertz", "kg",
    "metre", "meter", "second", "angstrom",
)
ASSIGN = re.compile(
    r"^\s*(S|A|A_c|rho|S_s|A_s|S_val)\s*=",
    re.IGNORECASE,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scan_violations(
    text: str,
    forbidden: tuple[str, ...] = FORBIDDEN_BARRIER,
) -> list[tuple[int, str]]:
    """Reproduce WN7's exact case and whole-line exemption semantics."""

    violations: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if IMPORT_MARK in line:
            continue
        lowered = line.lower()
        for literal in forbidden:
            if literal in lowered:
                violations.append((line_number, literal))
    return violations


def clamp_lines(text: str) -> list[str]:
    result: list[str] = []
    for line in text.splitlines():
        code = line.split("#", 1)[0]
        if (
            ("min(" in code and ("cap" in code.lower() or "ceil" in code.lower()))
            or "CEILING" in code
        ):
            result.append(line)
    return result


def unit_assignments(text: str) -> list[str]:
    offenders: list[str] = []
    for line in text.splitlines():
        code = line.split("#", 1)[0]
        if ASSIGN.match(code) and any(token in code.lower() for token in UNIT_TOKENS):
            offenders.append(line)
    return offenders


def decays_superpolynomially(sequence, nmax: int = 21) -> bool:
    return all(sequence(nmax) < sp.Rational(1, nmax**power) for power in (2, 4, 8))


def is_admissible_weight(weight, ns=tuple(range(1, 12))) -> bool:
    values = [weight(index) for index in ns]
    return bool(
        all(value > 0 for value in values)
        and max(range(len(values)), key=lambda index: values[index]) != 0
    )


def has_interior_mode(weight, upper: int = 80) -> bool:
    values = [weight(index) for index in range(1, upper)]
    index = max(range(len(values)), key=lambda offset: values[offset])
    return bool(0 < index < len(values) - 1)


def preserves_general_w(expression) -> bool:
    if expression is None:
        return False
    population, density = sp.symbols("population density", positive=True)
    response = density / (expression * population + density)
    expected = -density * expression / (expression * population + density) ** 2
    return bool(sp.simplify(sp.diff(response, population) - expected) == 0)


def reaches_growth_limb(mode_count, amplitude, threshold) -> bool:
    return bool(sp.Rational(mode_count) * sp.Rational(amplitude) ** 2 > threshold)


def main() -> int:
    checks = CheckLedger("P195-WN7-PRIMARY")
    checks.check("WN7 source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.144.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "all six scanned sources remain pinned",
        all(digest(SOURCE_ROOT / name) == expected for name, expected in WN_HASHES.items()),
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source inventory has 29 check sites and no assertions",
        len(calls) == 29
        and not any(isinstance(node, ast.Assert) for node in ast.walk(source_tree)),
    )
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "WN7 has no NumPy integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    texts = {
        name: (SOURCE_ROOT / name).read_text(encoding="utf-8")
        for name in WN_HASHES
    }
    checks.check(
        "exact barrier scan has zero current hits",
        all(not scan_violations(text) for text in texts.values()),
    )
    checks.check(
        "exact selected-decimal scan has zero current hits",
        all(not scan_violations(text, FORBIDDEN_IMPORTS) for text in texts.values()),
    )
    checks.check(
        "exact selected-identifier scan has zero current hits",
        all(not scan_violations(text, FORBIDDEN_EMPIRICAL) for text in texts.values()),
    )
    checks.check(
        "exact clamp-pattern scan has zero current hits",
        all(not clamp_lines(text) for text in texts.values()),
    )
    checks.check(
        "exact selected unit-assignment scan has zero current hits",
        all(not unit_assignments(text) for text in texts.values()),
    )

    imported_modules = {
        alias.name.split(".", 1)[0]
        for text in texts.values()
        for node in ast.walk(ast.parse(text))
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    checks.check(
        "AST import inventory is sys sympy and mpmath rather than three decimals",
        imported_modules == {"sys", "sympy", "mpmath"},
    )
    navigation = audit_source_tokens(
        SOURCE_ROOT,
        {"import_tag": r"\[IMPORT\]"},
        include_pattern="bridge_WN[1-6]_*.py",
        flags=0,
    )
    checks.check(
        "canonical lexical navigation hashes six files and locates two tagged files",
        navigation.scanned_file_count == 6
        and navigation.paths_for("import_tag")
        == (
            "bridge_WN4_derived_weight_and_crossover.py",
            "bridge_WN6_scale_verdict_and_missing_bridge.py",
        ),
    )

    checks.check(
        "whole-line tag exemption admits executable forbidden syntax",
        not scan_violations("value = u_e  # [IMPORT] citation"),
    )
    checks.check(
        "literal construction evades the finite substring scanner",
        not scan_violations("value = 'u' + '_e'"),
    )
    checks.check(
        "comments and docstrings collide with the finite substring scanner",
        len(scan_violations("# do not use u_e\n'''gamow is forbidden prose'''")) == 2,
    )
    checks.check(
        "selected decimal scan collides with unrelated larger decimals",
        scan_violations("calibration = 90.351", FORBIDDEN_IMPORTS) == [(1, "90.35")],
    )
    checks.check(
        "selected empirical identifier scan collides with comments",
        scan_violations("# no excess_heat_watts input exists", FORBIDDEN_EMPIRICAL)
        == [(1, "excess_heat_watts")],
    )
    checks.check(
        "clamp scanner misses equivalent executable caps",
        not clamp_lines("reported = max(0, min(raw, 10))\nreported = np.clip(raw, 0, cap)"),
    )
    checks.check(
        "naive comment splitting misses code after a hash inside a string",
        not clamp_lines("label = '#'; capped = min(raw, ceiling)"),
    )
    checks.check(
        "assignment scanner misses annotations and aliases",
        not unit_assignments("S: float = 0.031 * eV\nvalues['S'] = 2 * joule"),
    )
    checks.check(
        "assignment scanner collides with unit substrings inside identifiers",
        unit_assignments("S = parameter") == ["S = parameter"],
    )

    checks.check(
        "one over n ninth passes the finite superpolynomial fixture",
        decays_superpolynomially(lambda n: sp.Rational(1, n**9)),
    )
    checks.check(
        "a weight that first vanishes off-grid passes finite admissibility",
        is_admissible_weight(lambda n: sp.Integer(n) if n < 12 else sp.Integer(0)),
    )

    def finite_peak_then_growth(index: int) -> sp.Integer:
        if index < 80:
            return sp.Integer(1601 - (index - 40) ** 2)
        return sp.Integer(10**index)

    checks.check(
        "a post-grid growing weight passes the finite interior-mode fixture",
        has_interior_mode(finite_peak_then_growth)
        and finite_peak_then_growth(80) > finite_peak_then_growth(40),
    )
    checks.check(
        "zero expression passes the purported general-weight guard",
        preserves_general_w(sp.Integer(0)),
    )
    checks.check(
        "fixed mode count changes limb solely through free amplitude",
        not reaches_growth_limb(10**8, sp.Rational(1, 10), 10**7)
        and reaches_growth_limb(10**8, 1, 10**7),
    )
    checks.mutation_sensitive(
        "selected literal set is load bearing only for its finite proposition",
        lambda literal: len(scan_violations(f"x = {literal}")) == 1,
        "u_e",
        ("static_screen", "barrier_factor", "screening_factor"),
    )
    checks.check(
        "finite fixtures do not establish their broader labels",
        all(
            marker in source_text
            for marker in (
                "ZERO NEW IMPORTS",
                "DATA GATE CLOSED",
                "superpolynomial",
                "admissibility",
                "interior-mode",
            )
        ),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
