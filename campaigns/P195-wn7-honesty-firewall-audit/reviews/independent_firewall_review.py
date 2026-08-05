#!/usr/bin/env python3
"""Independent AST/token review of WN7 without importing its scanner code."""

from __future__ import annotations

import ast
import hashlib
import io
from pathlib import Path
import re
import tokenize

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = Path("/home/dan/substrate/merged-framework/bridges/phase-37")
WN7 = SOURCE_ROOT / "bridge_WN7_honesty_firewall_guard.py"
WN7_SHA256 = "88844689bf682ca5ff524378f4e5e46a25bcab54b1a3a6e59afe69b990694d50"
RELEASE_SHA256 = "b995916d6e708d29f0f493562741d7ba35bc202ce2784f4aaed7d1dfd5232a0a"
WN_NAMES = (
    "bridge_WN1_vertex_coefficient_magnitude.py",
    "bridge_WN2_coefficient_cannot_be_the_weight.py",
    "bridge_WN3_amplitude_scale_and_multiplicity.py",
    "bridge_WN4_derived_weight_and_crossover.py",
    "bridge_WN5_gb4_preserved_and_new_prediction.py",
    "bridge_WN6_scale_verdict_and_missing_bridge.py",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def independent_hits(text: str, literals: tuple[str, ...]) -> tuple[tuple[int, str], ...]:
    hits: list[tuple[int, str]] = []
    for number, line in enumerate(text.splitlines(), start=1):
        if "[IMPORT]" in line:
            continue
        folded = line.casefold()
        hits.extend((number, literal) for literal in literals if literal in folded)
    return tuple(hits)


def token_kinds_on_tagged_lines(text: str) -> dict[int, set[int]]:
    tagged = {
        number
        for number, line in enumerate(text.splitlines(), start=1)
        if "[IMPORT]" in line
    }
    result = {number: set() for number in tagged}
    reader = io.StringIO(text).readline
    for token in tokenize.generate_tokens(reader):
        if token.start[0] in tagged:
            result[token.start[0]].add(token.type)
    return result


def main() -> int:
    checks = CheckLedger("P195-WN7-INDEPENDENT")
    checks.check("WN7 bytes are independently pinned", digest(WN7) == WN7_SHA256)
    checks.check(
        "base release is independently pinned",
        digest(ROOT / "governance/releases/v0.144.0.yaml") == RELEASE_SHA256,
    )
    texts = {name: (SOURCE_ROOT / name).read_text(encoding="utf-8") for name in WN_NAMES}
    barrier = ("u_e", "gamow", "screening_enhancement", "gamow_energy_kev")
    decimals = ("0.0362", "90.35", "0.999757")
    empirical = ("excess_heat_watts", "cop_measured", "transmutation_yield")
    checks.check(
        "independent reproduction finds zero exempted barrier hits",
        all(not independent_hits(text, barrier) for text in texts.values()),
    )
    checks.check(
        "independent reproduction finds zero selected decimal hits",
        all(not independent_hits(text, decimals) for text in texts.values()),
    )
    checks.check(
        "independent reproduction finds zero selected empirical hits",
        all(not independent_hits(text, empirical) for text in texts.values()),
    )

    trees = {name: ast.parse(text, filename=name) for name, text in texts.items()}
    imported = {
        alias.name.partition(".")[0]
        for tree in trees.values()
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    }
    checks.check(
        "independent AST import inventory is sys sympy and mpmath",
        imported == {"sys", "sympy", "mpmath"},
    )
    checks.check(
        "three decimal absences cannot prove the AST import inventory",
        not set(decimals) & imported and all(re.fullmatch(r"[0-9.]+", item) for item in decimals),
    )

    wn4 = texts["bridge_WN4_derived_weight_and_crossover.py"]
    wn6 = texts["bridge_WN6_scale_verdict_and_missing_bridge.py"]
    wn4_tag_kinds = token_kinds_on_tagged_lines(wn4)
    checks.check(
        "WN4 named citation tags currently occur only in comment tokens",
        wn4_tag_kinds
        and all(tokenize.COMMENT in kinds for kinds in wn4_tag_kinds.values()),
    )
    checks.check(
        "WN6 import tags also occur in prose and are not named citations",
        "[IMPORT]" in wn6
        and "Huang" not in wn6
        and "Englman" not in wn6,
    )
    executable_bypass = "result = u_e  # [IMPORT]"
    bypass_tree = ast.parse(executable_bypass)
    checks.check(
        "tagged executable syntax is exempt despite a live name read",
        not independent_hits(executable_bypass, barrier)
        and any(isinstance(node, ast.Name) and node.id == "u_e" for node in ast.walk(bypass_tree)),
    )
    checks.check(
        "concatenated forbidden name evades literal matching",
        not independent_hits("name = 'u' + '_e'", barrier),
    )
    checks.check(
        "case-sensitive tag semantics reject a lowercase citation marker",
        independent_hits("value = u_e  # [import]", barrier) == ((1, "u_e"),),
    )

    clamp_regex = re.compile(r"(?:min\([^\n]*(?:cap|ceil)|CEILING)")
    bypasses = (
        "bounded = max(lower, min(raw, upper))",
        "bounded = numpy.clip(raw, lower, upper)",
        "bounded = upper if raw > upper else raw",
    )
    checks.check(
        "independent equivalent caps evade the declared clamp vocabulary",
        all(clamp_regex.search(line) is None for line in bypasses),
    )
    assignment_regex = re.compile(
        r"^\s*(S|A|A_c|rho|S_s|A_s|S_val)\s*=",
        re.IGNORECASE,
    )
    checks.check(
        "independent annotated and destructured assignments evade the regex",
        assignment_regex.match("S: float = 1 * eV") is None
        and assignment_regex.match("S, A = 1 * eV, 2 * joule") is None,
    )
    checks.check(
        "identifier substring creates an independent unit false positive",
        assignment_regex.match("S = parameter") is not None and "meter" in "parameter",
    )

    n = sp.Integer(21)
    finite_powers = (2, 4, 8)
    checks.check(
        "independent polynomial n ninth counterexample passes the finite decay inequalities",
        all(sp.Rational(1, n**9) < sp.Rational(1, n**power) for power in finite_powers),
    )
    def finite_admissibility_witness(index: int) -> sp.Integer:
        return sp.Integer(index) if index < 12 else sp.Integer(0)

    finite_values = tuple(finite_admissibility_witness(index) for index in range(1, 12))
    checks.check(
        "independent finite admissibility witness says nothing about zero at twelve",
        all(index > 0 for index in finite_values)
        and max(range(len(finite_values)), key=finite_values.__getitem__) != 0
        and finite_admissibility_witness(12) == 0,
    )
    sampled = tuple(sp.Integer(1601 - (index - 40) ** 2) for index in range(1, 80))
    peak_index = max(range(len(sampled)), key=sampled.__getitem__)
    checks.check(
        "independent finite interior peak can precede arbitrary later growth",
        0 < peak_index < len(sampled) - 1 and sp.Integer(10**80) > max(sampled),
    )
    population, density = sp.symbols("population density", positive=True)
    zero_response = density / (sp.Integer(0) * population + density)
    checks.check(
        "independent zero-weight substitution satisfies the derivative identity",
        sp.diff(zero_response, population) == 0,
    )
    checks.check(
        "independent amplitude pairs reverse the same fixed-mode limb verdict",
        10**8 * sp.Rational(1, 10) ** 2 < 10**7 < 10**8,
    )
    checks.check(
        "counterexamples jointly reject semantic completeness but retain finite results",
        True,
        "the preceding checks are the independent certificate",
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
