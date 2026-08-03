"""Independent CM6 review without importing the P120 primary verifier."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import re
import unicodedata

from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate/merged-framework/bridges/phase-31")
CAMPAIGN = Path("campaigns/P120-cm6-honesty-firewall-audit")
CM6_PATH = ROOT / "bridge_CM6_honesty_firewall_guard.py"
CM6_SHA = "60a8d1de7693783c7859d32b5d7b90bd46c6304cbd7c14fd06fb5235acadf3c5"
CM3_PATH = ROOT / "bridge_CM3_crossover.py"
CM3_SHA = "d62d8deadbba30c4d240ed57c204149ffe0d6b2ec49ed0e200206a4b4a8eccdb"
FREEZE_SHA = "c0ab7a4616234878ddad9808ca8e5711b865d934f51b89472f69a5f23e5f326b"
B_NAMES = (
    "bridge_CM2_coherence_rate_law.py",
    "bridge_CM4_discriminating_bar.py",
    "bridge_CM5_excess_electrical.py",
)
A_NAMES = (
    "bridge_CM1_separation_boundary.py",
    "bridge_CM7_gamow_crossover.py",
)
BARRIER_WORDS = (
    "u_e",
    "gamow",
    "screening_enhancement",
    "gamow_energy_kev",
)
EMPIRICAL_WORDS = (
    "excess_heat_watts",
    "cop_measured",
    "transmutation_yield",
)


def fresh_scan(text: str, words: tuple[str, ...]) -> list[tuple[int, str]]:
    """Independent ASCII-equivalent rendering of CM6 line matching."""

    found: list[tuple[int, str]] = []
    for index, line in enumerate(text.splitlines(), 1):
        if re.search(r"\[IMPORT\]", line) is not None:
            continue
        folded = line.casefold()
        found.extend((index, word) for word in words if folded.find(word) >= 0)
    return found


def fresh_clamp_scan(text: str) -> list[int]:
    hits = []
    for index, line in enumerate(text.splitlines(), 1):
        before_hash = line.partition("#")[0]
        lower = before_hash.lower()
        if ("min(" in before_hash and ("cap" in lower or "ceil" in lower)) or (
            "CEILING" in before_hash
        ):
            hits.append(index)
    return hits


def identifiers(text: str) -> set[str]:
    tree = ast.parse(text)
    names = {node.id.casefold() for node in ast.walk(tree) if isinstance(node, ast.Name)}
    names.update(
        node.attr.casefold()
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
    )
    return names


def main() -> int:
    checks = CheckLedger("CM6-INDEPENDENT-REVIEW")
    cm6_bytes = CM6_PATH.read_bytes()
    cm6_text = cm6_bytes.decode("utf-8")
    checks.check(
        "independently read CM6 bytes are hash pinned",
        hashlib.sha256(cm6_bytes).hexdigest() == CM6_SHA,
    )
    checks.check(
        "independently read CM3 counterexample bytes are hash pinned",
        hashlib.sha256(CM3_PATH.read_bytes()).hexdigest() == CM3_SHA,
    )
    checks.check(
        "the preregistration artifact remains byte identical",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    tree = ast.parse(cm6_text)
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "fresh AST count finds twelve static check calls",
        len(calls) == 12,
    )
    checks.check(
        "fresh loop arithmetic expands the calls to twenty runtime verdicts",
        len(B_NAMES) + len(A_NAMES) + 3 + 2 + len(B_NAMES + A_NAMES) + 5 == 20,
    )

    b_text = {name: (ROOT / name).read_text() for name in B_NAMES}
    a_text = {name: (ROOT / name).read_text() for name in A_NAMES}
    checks.check(
        "fresh barrier matcher is empty on the three actually scanned B files",
        all(fresh_scan(text, BARRIER_WORDS) == [] for text in b_text.values()),
    )
    checks.check(
        "fresh raw search finds U_e in both actually scanned A files",
        all("u_e" in text.casefold() for text in a_text.values()),
    )
    checks.check(
        "fresh clamp matcher is empty on the two files CM6 checks",
        fresh_clamp_scan(b_text[B_NAMES[0]]) == []
        and fresh_clamp_scan(b_text[B_NAMES[2]]) == [],
    )
    checks.check(
        "fresh empirical matcher is empty on the five actually scanned files",
        all(
            fresh_scan(text, EMPIRICAL_WORDS) == []
            for text in (*b_text.values(), *a_text.values())
        ),
    )

    phase31_text = {path.name: path.read_text() for path in sorted(ROOT.glob("*.py"))}
    raw_ue_files = {
        name for name, text in phase31_text.items() if "u_e" in text.casefold()
    }
    checks.check(
        "whole-phase raw search refutes literal confinement to only CM1 and CM7",
        raw_ue_files
        == {
            "bridge_CM1_separation_boundary.py",
            "bridge_CM3_crossover.py",
            "bridge_CM6_honesty_firewall_guard.py",
            "bridge_CM7_gamow_crossover.py",
        },
    )
    checks.check(
        "omitted CM3 is labelled B-side by its own pinned source",
        "B-side only" in phase31_text["bridge_CM3_crossover.py"],
    )
    cm3_matches = fresh_scan(
        phase31_text["bridge_CM3_crossover.py"], BARRIER_WORDS
    )
    checks.check(
        "adding the omitted B-side CM3 makes the source literal verdict fail",
        {word for _, word in cm3_matches} >= {"u_e", "gamow"},
    )
    checks.check(
        "CM3's failure is prose-only for U_e under an AST identifier oracle",
        "u_e" not in identifiers(phase31_text["bridge_CM3_crossover.py"]),
    )
    executable_ue_files = {
        name for name, text in phase31_text.items() if "u_e" in identifiers(text)
    }
    checks.check(
        "phase-wide executable U_e identifiers occur in CM1 and CM7 only",
        executable_ue_files
        == {
            "bridge_CM1_separation_boundary.py",
            "bridge_CM7_gamow_crossover.py",
        },
    )
    checks.check(
        "that executable confinement remains only a pinned syntactic statement",
        len(phase31_text) > len(B_NAMES + A_NAMES)
        and all(path.is_file() for path in ROOT.glob("*.py")),
    )

    checks.check(
        "the exact tag rule is case sensitive and line-wide",
        fresh_scan("value = U_e # [IMPORT]", BARRIER_WORDS) == []
        and fresh_scan("value = U_e # [import]", BARRIER_WORDS) == [(1, "u_e")],
    )
    checks.check(
        "tag text inside a string exempts executable syntax",
        fresh_scan('tag = "[IMPORT]"; value = U_e', BARRIER_WORDS) == [],
    )
    checks.check(
        "concatenation and getattr preserve a name while evading the matcher",
        fresh_scan('n="U_"+"e"; value=getattr(obj,n)', BARRIER_WORDS) == []
        and "U_" + "e" == "U_e",
    )
    unicode_name = "U\uff3fe"
    checks.check(
        "lack of Unicode normalization creates a second name evasion",
        fresh_scan(f"value={unicode_name}", BARRIER_WORDS) == []
        and unicodedata.normalize("NFKC", unicode_name) == "U_e",
    )
    checks.check(
        "equivalent shifted-barrier algebra needs no forbidden identifier",
        fresh_scan("f=exp(-sqrt(g/(e+s)))", BARRIER_WORDS) == [],
    )
    checks.check(
        "comments and negated prose produce literal false positives",
        fresh_scan("# U_e is absent", BARRIER_WORDS) == [(1, "u_e")]
        and fresh_scan('"No Gamow machinery"', BARRIER_WORDS) == [(1, "gamow")],
    )
    checks.check(
        "a benign larger identifier collides with the U_e substring",
        fresh_scan("tau_evolution = 1", BARRIER_WORDS) == [(1, "u_e")],
    )
    checks.check(
        "the longer Gamow helper token is redundant with the shorter token",
        fresh_scan("x=gamow_energy_keV(pair)", BARRIER_WORDS)
        == [(1, "gamow"), (1, "gamow_energy_kev")],
    )

    saturation_forms = (
        "y=min (x, limit)",
        "y=np.clip(x,0,limit)",
        "y=x if x<limit else limit",
        "y=x/(1+abs(x))",
        "y=tanh(x)",
        "y=bounded_helper(x)",
    )
    checks.check(
        "fresh clamp matcher misses six saturation spellings",
        all(fresh_clamp_scan(form) == [] for form in saturation_forms),
    )
    checks.check(
        "a capacity variable causes a clamp false positive",
        fresh_clamp_scan("remaining_capacity=min(raw, available)") == [1],
    )
    checks.check(
        "a hash in string data hides a later literal clamp",
        fresh_clamp_scan('label="#"; y=min(x, cap)') == [],
    )
    checks.check(
        "absence of clamp spellings does not prove unbounded output",
        100 / (1 + abs(100)) < 1 and (100 if 100 < 1 else 1) == 1,
    )

    checks.check(
        "a numeric comparator pass condition evades the empirical words",
        fresh_scan('check("fit", abs(output-30.0)<0.01)', EMPIRICAL_WORDS) == [],
    )
    checks.check(
        "an imported comparator also evades the empirical words",
        fresh_scan('target=config["observed"]; check("fit", output==target)', EMPIRICAL_WORDS)
        == [],
    )
    checks.check(
        "an empirical-word comment is a false positive rather than a data-flow proof",
        fresh_scan("# excess_heat_watts is not an input", EMPIRICAL_WORDS)
        == [(1, "excess_heat_watts")],
    )

    modules = set()
    for text in (*b_text.values(), *a_text.values()):
        parsed = ast.parse(text)
        modules.update(
            alias.name
            for node in ast.walk(parsed)
            if isinstance(node, ast.Import)
            for alias in node.names
        )
    checks.check(
        "scanned files import unscanned domain modules",
        {"screening", "barrier_scaling", "medium_omega0", "seeding_kernel"}
        <= modules,
    )
    checks.check(
        "the source carries no transitive file closure or source hashes",
        "sha256" not in cm6_text.casefold()
        and "imported_modules" not in cm6_text
        and "bridge_CM3_crossover.py" not in cm6_text,
    )
    checks.check(
        "disjoint lists remain true after omitting an arbitrary third class",
        {"a"}.isdisjoint({"b"}) and "omitted" not in {"a", "b"},
    )
    checks.check(
        "self-testing selected literals cannot establish semantic completeness",
        fresh_scan("value=U_e", BARRIER_WORDS) != []
        and fresh_scan('n="U_"+"e"', BARRIER_WORDS) == [],
    )
    checks.check(
        "the strongest surviving result is finite lexical and AST evidence only",
        all(fresh_scan(text, BARRIER_WORDS) == [] for text in b_text.values())
        and executable_ue_files
        == {
            "bridge_CM1_separation_boundary.py",
            "bridge_CM7_gamow_crossover.py",
        },
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
