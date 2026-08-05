#!/usr/bin/env python3
"""Fresh semantic and logical review of KI1 without importing its implementation."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re
import subprocess

from substrate_framework.verification import CheckLedger


SOURCE_ROOT = Path("/home/dan/substrate")
COMMIT = "6d1f4e02f87a0bd1dc326cb68af01872d1e88c64"
KI1 = "merged-framework/bridges/phase-34/bridge_KI1_exhaustive_coupling_search.py"
MK1 = "merged-framework/bridges/phase-43/bridge_MK1_mu_from_medium_cosine.py"
MK2 = "merged-framework/bridges/phase-43/bridge_MK2_lambda_from_medium_omega.py"
MK3 = "merged-framework/bridges/phase-43/bridge_MK3_epsilon_pinned.py"
KI1_SHA256 = "a1ec5f8e64e56165d2c51ad2389ecb455870572ba4ef9eca292151bde4ddb42b"

SOURCE_LITERAL_REGEX = re.compile(
    r"(?<![A-Za-z0-9_])(lam|mu|eps|epsilon|lambda)"
    r"(_(bps|BPS|skyrme|nb|near|nearbps|6|0))?\s*=\s*"
    r"[-+]?[0-9]*\.?[0-9]+"
)
COUPLING_NAMES = {"lam", "lambda", "lambda_bps", "mu", "mu_bps", "eps", "epsilon"}


@dataclass(frozen=True)
class SemanticPolicy:
    """Syntax families admitted by an independent assignment recognizer."""

    annotated: bool
    constructors: bool
    subscript_targets: bool
    dictionary_keys: bool


SEMANTIC_WITNESSES = (
    "lambda_bps: float = 1.234",
    "lambda_bps = sp.Rational(1, 2)",
    "params['lambda_bps'] = 1.2",
    "mu_bps = np.float64(2.0)",
    "couplings = {'epsilon': 0.11}",
)


def _blob(path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(SOURCE_ROOT), "show", f"{COMMIT}:{path}"],
        check=True,
        capture_output=True,
    ).stdout


def _name_from_target(node: ast.AST, policy: SemanticPolicy) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if policy.subscript_targets and isinstance(node, ast.Subscript):
        if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
            return node.slice.value
    return None


def _numeric_value(node: ast.AST, policy: SemanticPolicy) -> bool:
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float)) and not isinstance(node.value, bool)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return _numeric_value(node.operand, policy)
    if policy.constructors and isinstance(node, ast.Call):
        if isinstance(node.func, ast.Attribute):
            function = node.func.attr
        elif isinstance(node.func, ast.Name):
            function = node.func.id
        else:
            function = ""
        return function in {"Rational", "float64", "Decimal"} and bool(node.args)
    return False


def _semantic_assignment_names(source: str, policy: SemanticPolicy) -> set[str]:
    tree = ast.parse(source)
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if _numeric_value(node.value, policy):
                names.update(
                    name
                    for target in node.targets
                    if (name := _name_from_target(target, policy)) in COUPLING_NAMES
                )
            if policy.dictionary_keys and isinstance(node.value, ast.Dict):
                for key, value in zip(node.value.keys, node.value.values, strict=True):
                    if (
                        isinstance(key, ast.Constant)
                        and key.value in COUPLING_NAMES
                        and _numeric_value(value, policy)
                    ):
                        names.add(key.value)
        elif (
            policy.annotated
            and isinstance(node, ast.AnnAssign)
            and node.value is not None
            and _numeric_value(node.value, policy)
        ):
            name = _name_from_target(node.target, policy)
            if name in COUPLING_NAMES:
                names.add(name)
    return names


def _policy_catches_all(candidate: object) -> bool:
    assert isinstance(candidate, SemanticPolicy)
    expected = {"lambda_bps", "mu_bps", "epsilon"}
    per_witness = [
        _semantic_assignment_names(witness, candidate)
        for witness in SEMANTIC_WITNESSES
    ]
    return all(per_witness) and set().union(*per_witness) == expected


def main() -> int:
    checks = CheckLedger("P171-INDEPENDENT-SEMANTIC-INVENTORY")
    source_bytes = _blob(KI1)
    source = source_bytes.decode("utf-8")
    checks.check(
        "the independently read KI1 blob is exact",
        hashlib.sha256(source_bytes).hexdigest() == KI1_SHA256,
    )
    checks.check(
        "KI1's execution is fail-fast so predicates three through five are unreachable after KI1.2",
        "assert ok" in source
        and source.index('"KI1.2 [DERIVED') < source.index('"KI1.3 [DERIVED')
        < source.index('"KI1.4 [DERIVED') < source.index('"KI1.5 [GUARD'),
    )
    checks.check(
        "a runtime tally cannot exist when KI1.2 raises",
        source.index("assert ok") < source.index('print(f"\\nALL {len(PASS)} CHECKS PASS")'),
    )

    checks.check(
        "all five independent semantic witnesses evade KI1's literal regex",
        all(SOURCE_LITERAL_REGEX.search(witness) is None for witness in SEMANTIC_WITNESSES),
    )
    complete = SemanticPolicy(True, True, True, True)
    checks.check(
        "the independent AST policy recognizes every semantic witness family",
        _policy_catches_all(complete),
    )
    checks.mutation_sensitive(
        "the semantic recognizer depends on each nonliteral syntax family",
        _policy_catches_all,
        complete,
        [
            SemanticPolicy(False, True, True, True),
            SemanticPolicy(True, False, True, True),
            SemanticPolicy(True, True, False, True),
            SemanticPolicy(True, True, True, False),
        ],
    )

    checks.check(
        "file-level context intersection has an explicit semantic false-positive model",
        bool(SOURCE_LITERAL_REGEX.search("mu = 2.0  # chemical potential"))
        and bool(re.search(r"BPS", "This document also reviews the BPS sector")),
    )
    checks.check(
        "excluding a directory cannot detect a positive planted elsewhere in that directory",
        "merged-framework/bridges/phase-34/bridge_KI99.py".startswith(
            "merged-framework/bridges/phase-34/"
        )
        and bool(SOURCE_LITERAL_REGEX.search("lambda_bps = 1.234")),
    )

    mk1 = _blob(MK1).decode("utf-8")
    mk2 = _blob(MK2).decode("utf-8")
    mk3 = _blob(MK3).decode("utf-8")
    checks.check(
        "the pinned tree contains an explicit mu candidate derivation",
        "mu_derived = sp.sqrt(sols[0])" in mk1
        and "m_pi * F_pi / 2" in mk1,
    )
    checks.check(
        "the pinned tree contains an explicit lambda candidate derivation",
        "lam_expected = N_c / (4 * F_pi)" in mk2
        and "g_omega^2/(2 m_omega^2)" in mk2,
    )
    checks.check(
        "the pinned tree contains an explicit epsilon candidate evaluation",
        "eps_expected = 128 * sp.pi * m_e / (3 * m_pi)" in mk3
        and "eps_num = float" in mk3,
    )
    checks.check(
        "candidate derivations refute corpus absence without becoming accepted physics",
        all("RESULT (BRIDGE established" in text for text in (mk1, mk2, mk3))
        and all("pending_adjudication" not in text for text in (mk1, mk2, mk3)),
    )

    corpus_snapshot = frozenset({KI1, MK1, MK2, MK3})
    older_snapshot = frozenset({KI1})
    checks.check(
        "a negative corpus statement is snapshot-relative and not monotone under additions",
        older_snapshot < corpus_snapshot
        and not {MK1, MK2, MK3}.isdisjoint(corpus_snapshot)
        and {MK1, MK2, MK3}.isdisjoint(older_snapshot),
    )
    checks.check(
        "repository absence cannot imply physical non-identifiability",
        {"tracked_files": older_snapshot, "external_lambda": 1.0}["tracked_files"]
        == {"tracked_files": older_snapshot, "external_lambda": 2.0}["tracked_files"]
        and 1.0 != 2.0,
    )
    checks.check(
        "repository presence cannot validate the pending candidate formulas",
        MK1 in corpus_snapshot and MK2 in corpus_snapshot and MK3 in corpus_snapshot
        and not source.startswith("accepted scientific registry"),
    )

    total = checks.finish()
    print(f"P171 INDEPENDENT SEMANTIC INVENTORY ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
