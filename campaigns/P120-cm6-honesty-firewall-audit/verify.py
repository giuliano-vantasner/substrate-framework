"""Primary finite-scanner and semantic-ceiling verifier for P120/CM6."""

from __future__ import annotations

import ast
import hashlib
import io
from pathlib import Path
import tokenize
import unicodedata

from substrate_framework.verification import CheckLedger


SOURCE_ROOT = Path("/home/dan/substrate/merged-framework/bridges/phase-31")
CAMPAIGN = Path("campaigns/P120-cm6-honesty-firewall-audit")
CM6 = "bridge_CM6_honesty_firewall_guard.py"
SOURCE_FILES = {
    "CM1": "bridge_CM1_separation_boundary.py",
    "CM2": "bridge_CM2_coherence_rate_law.py",
    "CM4": "bridge_CM4_discriminating_bar.py",
    "CM5": "bridge_CM5_excess_electrical.py",
    "CM6": CM6,
    "CM7": "bridge_CM7_gamow_crossover.py",
}
SOURCE_HASHES = {
    "CM1": "0f6881d96469274664ed1b762ff56a88b94ecdca599c22f8bb181052bd7f3ccc",
    "CM2": "c75fee880740765d3ef3e32634bf05360fd9789e46bd579fd07af60d29a79fa2",
    "CM4": "984b5a1495c0d17095b127cc79eceb9625592051b0e5ab099bc66683b418c019",
    "CM5": "8af42e5229ba59b31dfb30dbf94e904a2670c4f2f2b57373f9dd25ab169c2841",
    "CM6": "60a8d1de7693783c7859d32b5d7b90bd46c6304cbd7c14fd06fb5235acadf3c5",
    "CM7": "10344b842a47b24651c891dfa55a030dd193e3e48e0b128b93bf74f29af6cee2",
}
CM3_HASH = "d62d8deadbba30c4d240ed57c204149ffe0d6b2ec49ed0e200206a4b4a8eccdb"
FREEZE_HASH = "c0ab7a4616234878ddad9808ca8e5711b865d934f51b89472f69a5f23e5f326b"
IMPORT_MARK = "[IMPORT]"
FORBIDDEN = ("u_e", "gamow", "screening_enhancement", "gamow_energy_kev")
FORBIDDEN_EMPIRICAL = (
    "excess_heat_watts",
    "cop_measured",
    "transmutation_yield",
)
B_SIDE = (SOURCE_FILES["CM2"], SOURCE_FILES["CM4"], SOURCE_FILES["CM5"])
A_SIDE = (SOURCE_FILES["CM1"], SOURCE_FILES["CM7"])


def literal_scan(
    text: str,
    forbidden: tuple[str, ...] = FORBIDDEN,
) -> list[tuple[int, str]]:
    """Reproduce CM6's case-insensitive substring and line-exemption rules."""

    violations: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if IMPORT_MARK in line:
            continue
        lowered = line.lower()
        for literal in forbidden:
            if literal in lowered:
                violations.append((line_number, literal))
    return violations


def clamp_scan(text: str) -> list[str]:
    """Reproduce CM6's two-pattern clamp detector exactly."""

    matches = []
    for line in text.splitlines():
        code = line.split("#", 1)[0]
        if (
            "min(" in code
            and ("cap" in code.lower() or "ceil" in code.lower())
        ) or "CEILING" in code:
            matches.append(line)
    return matches


def _constant_expression(node: ast.AST, known: dict[str, object]) -> object:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name) and node.id in known:
        return known[node.id]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _constant_expression(node.left, known)
        right = _constant_expression(node.right, known)
        return left + right  # type: ignore[operator]
    if isinstance(node, (ast.List, ast.Tuple)):
        return tuple(_constant_expression(item, known) for item in node.elts)
    raise ValueError(f"unsupported constant expression: {ast.dump(node)}")


def _assignments(tree: ast.Module) -> dict[str, object]:
    values: dict[str, object] = {}
    for node in tree.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            try:
                values[node.targets[0].id] = _constant_expression(node.value, values)
            except (TypeError, ValueError):
                pass
    return values


def executable_identifiers(text: str) -> set[str]:
    """Return lower-case identifiers and attribute names from executable AST."""

    tree = ast.parse(text)
    identifiers = {
        node.id.lower() for node in ast.walk(tree) if isinstance(node, ast.Name)
    }
    identifiers.update(
        node.attr.lower()
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    )
    return identifiers


def comments(text: str) -> tuple[str, ...]:
    tokens = tokenize.generate_tokens(io.StringIO(text).readline)
    return tuple(token.string for token in tokens if token.type == tokenize.COMMENT)


def imported_modules(text: str) -> set[str]:
    tree = ast.parse(text)
    direct = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    direct.update(
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    )
    return direct


def main() -> int:
    checks = CheckLedger("CM6-FINITE-SCANNER-AUDIT")
    source_bytes = {
        unit: (SOURCE_ROOT / filename).read_bytes()
        for unit, filename in SOURCE_FILES.items()
    }
    source_text = {
        unit: payload.decode("utf-8") for unit, payload in source_bytes.items()
    }

    for unit, expected in SOURCE_HASHES.items():
        checks.check(
            f"{unit} source bytes are hash pinned",
            hashlib.sha256(source_bytes[unit]).hexdigest() == expected,
        )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_HASH,
    )
    checks.check(
        "pre-source contract is immutable",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_HASH,
    )

    cm6_tree = ast.parse(source_text["CM6"])
    assignments = _assignments(cm6_tree)
    checks.check(
        "source token lists and case-sensitive exemption are recovered exactly",
        assignments["IMPORT_MARK"] == IMPORT_MARK
        and assignments["FORBIDDEN"] == FORBIDDEN
        and assignments["FORBIDDEN_EMPIRICAL"] == FORBIDDEN_EMPIRICAL,
    )
    checks.check(
        "source A-side and B-side lists are recovered exactly",
        assignments["B_SIDE"] == B_SIDE and assignments["A_SIDE"] == A_SIDE,
    )
    source_check_calls = [
        node
        for node in ast.walk(cm6_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    expected_runtime = len(B_SIDE) + len(A_SIDE) + 3 + 2 + len(B_SIDE + A_SIDE) + 5
    checks.check(
        "twelve static calls expand to the declared twenty runtime predicates",
        len(source_check_calls) == 12
        and expected_runtime == 20
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text["CM6"],
    )
    checks.check(
        "CM6 requires no numerical-integration compatibility path",
        all(
            token not in source_text["CM6"]
            for token in (
                "np.trapz",
                "np.trapezoid",
                "trapezoid_integral",
                "scipy.integrate",
            )
        ),
    )

    b_text = {filename: (SOURCE_ROOT / filename).read_text() for filename in B_SIDE}
    a_text = {filename: (SOURCE_ROOT / filename).read_text() for filename in A_SIDE}
    checks.check(
        "the exact barrier token scan is empty on the three declared B-side files",
        all(literal_scan(text) == [] for text in b_text.values()),
    )
    checks.check(
        "raw U_e substring absence independently holds on the declared B-side",
        all("u_e" not in text.lower() for text in b_text.values()),
    )
    checks.check(
        "raw U_e substring presence holds on both declared A-side files",
        all("u_e" in text.lower() for text in a_text.values()),
    )
    checks.check(
        "the two hard-coded filename lists are disjoint and place CM7 only in A",
        set(A_SIDE).isdisjoint(B_SIDE)
        and SOURCE_FILES["CM7"] in A_SIDE
        and SOURCE_FILES["CM7"] not in B_SIDE,
    )
    checks.check(
        "the exact two-pattern clamp scan is empty on CM2 and CM5",
        clamp_scan(source_text["CM2"]) == []
        and clamp_scan(source_text["CM5"]) == [],
    )
    checks.check(
        "the exact three-token empirical scan is empty on all five declared files",
        all(
            literal_scan(text, FORBIDDEN_EMPIRICAL) == []
            for text in (*b_text.values(), *a_text.values())
        ),
    )

    fake_ue = "screened_rate = U_e * 30.0"
    fake_gamow = "coherent_yield = gamow_factor(E)"
    fake_import = "screened_rate = U_e * 30.0  # [IMPORT] citation"
    fake_empirical = "target = excess_heat_watts"
    checks.check(
        "source-style self-tests detect each literal and report its identity",
        literal_scan(fake_ue) == [(1, "u_e")]
        and literal_scan(fake_gamow) == [(1, "gamow")]
        and literal_scan(fake_empirical, FORBIDDEN_EMPIRICAL)
        == [(1, "excess_heat_watts")],
    )
    checks.check(
        "the source-style uppercase import marker exempts the entire line",
        literal_scan(fake_import) == [],
    )
    checks.check(
        "case folding applies to forbidden text but not to the exemption marker",
        literal_scan("value = U_E") == [(1, "u_e")]
        and literal_scan("value = U_e  # [import]") == [(1, "u_e")],
    )
    checks.check(
        "an import marker in executable string data smuggles a forbidden token",
        literal_scan('payload = "[IMPORT]"; value = U_e') == [],
    )
    checks.check(
        "the tagged-scan and raw-B-side rules disagree on tagged U_e",
        literal_scan("value = U_e  # [IMPORT]") == []
        and "u_e" in "value = U_e  # [IMPORT]".lower(),
    )

    constructed = 'name = "U_" + "e"; value = getattr(model, name)'
    constructed_screen = 'name = "screening_" + "enhancement"'
    fullwidth = "value = U\uff3fe"
    checks.check(
        "constructed forbidden names evade the literal scanner",
        literal_scan(constructed) == []
        and "U_" + "e" == "U_e"
        and literal_scan(constructed_screen) == []
        and "screening_" + "enhancement" == "screening_enhancement",
    )
    checks.check(
        "Unicode-equivalent punctuation evades because normalization is absent",
        literal_scan(fullwidth) == []
        and "u_e" in unicodedata.normalize("NFKC", fullwidth).lower(),
    )
    checks.check(
        "an algebraically equivalent barrier formula needs no listed name",
        literal_scan("rate = exp(-sqrt(scale / (energy + shift)))") == [],
    )
    checks.check(
        "comments, docstrings, negation, and benign substrings are false positives",
        literal_scan("# never use U_e here") == [(1, "u_e")]
        and literal_scan('"""No Gamow factor is present."""') == [(1, "gamow")]
        and literal_scan("tau_evolution = 0") == [(1, "u_e")],
    )
    checks.check(
        "AST identifiers separate executable U_e from comment-only occurrences",
        "u_e" in executable_identifiers("value = U_e\n# Gamow")
        and "u_e" not in executable_identifiers("value = 1\n# U_e")
        and any("U_e" in comment for comment in comments("value = 1\n# U_e")),
    )
    checks.check(
        "the declared B-side also has no exact forbidden executable identifiers",
        all(
            not (set(FORBIDDEN) & executable_identifiers(text))
            for text in b_text.values()
        ),
    )
    checks.check(
        "both declared A-side files contain executable U_e identifiers",
        all("u_e" in executable_identifiers(text) for text in a_text.values()),
    )

    clamp_evasions = (
        "reported = min (raw, limit)",
        "reported = np.clip(raw, 0, limit)",
        "reported = raw if raw < limit else limit",
        "reported = saturate(raw)",
        "reported = raw / (1 + abs(raw))",
        "reported = math.tanh(raw)",
        "reported = table[min(index, len(table)-1)]",
    )
    checks.check(
        "seven ordinary saturation spellings evade the two-pattern clamp scan",
        all(clamp_scan(snippet) == [] for snippet in clamp_evasions),
    )
    checks.check(
        "the evasion examples include actually bounded maps",
        min(10, 1) == 1
        and 10 / (1 + abs(10)) < 1
        and (10 if 10 < 1 else 1) == 1,
    )
    checks.check(
        "a benign capacity identifier creates a clamp false positive",
        clamp_scan("remaining_capacity = min(raw, available)")
        == ["remaining_capacity = min(raw, available)"],
    )
    checks.check(
        "hash characters inside strings are misclassified as comments",
        clamp_scan('label = "#"; reported = min(raw, cap)') == [],
    )

    empirical_fit = 'check("fit", abs(model - 30.0) < 0.01)'
    imported_fit = 'target = config["heat"]; check("fit", model == target)'
    checks.check(
        "hard-coded and imported comparator pass conditions evade three identifier tokens",
        literal_scan(empirical_fit, FORBIDDEN_EMPIRICAL) == []
        and literal_scan(imported_fit, FORBIDDEN_EMPIRICAL) == [],
    )
    checks.check(
        "an empirical-token comment is flagged without being a pass condition",
        literal_scan("# excess_heat_watts is intentionally not used", FORBIDDEN_EMPIRICAL)
        == [(1, "excess_heat_watts")],
    )
    checks.check(
        "the import exemption can hide an executable empirical identifier",
        literal_scan(
            "target = excess_heat_watts  # [IMPORT]", FORBIDDEN_EMPIRICAL
        )
        == [],
    )

    scanned_names = set(B_SIDE + A_SIDE)
    imports = set().union(
        *(imported_modules(text) for text in (*b_text.values(), *a_text.values()))
    )
    checks.check(
        "the fixed scan omits nonstandard imported support modules",
        {"screening", "barrier_scaling", "medium_omega0", "seeding_kernel"}
        <= imports
        and scanned_names.isdisjoint(imports),
    )
    checks.check(
        "the source's own named B-side CM3 is outside its B_SIDE list",
        (SOURCE_ROOT / "bridge_CM3_crossover.py").exists()
        and "bridge_CM3_crossover.py" not in scanned_names,
    )
    cm3_bytes = (SOURCE_ROOT / "bridge_CM3_crossover.py").read_bytes()
    cm3_text = cm3_bytes.decode("utf-8")
    checks.check(
        "the omitted CM3 counterexample is itself hash pinned",
        hashlib.sha256(cm3_bytes).hexdigest() == CM3_HASH,
    )
    checks.check(
        "including named B-side CM3 breaks the literal rule on prose but not executable U_e",
        {literal for _, literal in literal_scan(cm3_text)} >= {"u_e", "gamow"}
        and "u_e" not in executable_identifiers(cm3_text),
    )
    checks.check(
        "disjoint hard-coded lists do not establish a complete partition",
        set(("A.py",)).isdisjoint(("B.py",))
        and "omitted.py" not in {"A.py", "B.py"},
    )
    read_src = next(
        node
        for node in cm6_tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "read_src"
    )
    checks.check(
        "source reads are unhashed, default-decoded, and have no local error policy",
        not any(isinstance(node, ast.Try) for node in ast.walk(read_src))
        and "encoding" not in ast.dump(read_src)
        and "sha256" not in source_text["CM6"].lower(),
    )
    checks.check(
        "U_e presence alone can be satisfied by a comment rather than machinery",
        "u_e" in "# U_e is merely discussed".lower()
        and "u_e" not in executable_identifiers("value = 1\n# U_e is merely discussed"),
    )
    checks.check(
        "CM6 is outside its own scan and would self-flag if included",
        CM6 not in scanned_names and len(literal_scan(source_text["CM6"])) > 0,
    )

    checks.check(
        "the exact positive result is finite lexical evidence, not semantic closure",
        all(literal_scan(text) == [] for text in b_text.values())
        and literal_scan(constructed) == []
        and literal_scan("# never use U_e") != [],
    )
    checks.check(
        "no literal result supplies a barrier-free physical model or magnitude oracle",
        "field equation" not in assignments
        and "coupling" not in assignments
        and "observable" not in assignments
        and "input provenance" not in assignments,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
