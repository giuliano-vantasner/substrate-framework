#!/usr/bin/env python3
"""Exact premise, range, and oracle audit of hash-pinned predecessor KI3."""

from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import sympy as sp
import yaml

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


FRAMEWORK_ROOT = Path("/home/dan/substrate-framework")
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / (
    "merged-framework/bridges/phase-34/bridge_KI3_bracket_is_sharp.py"
)
DOSSIER = SOURCE_ROOT / (
    "merged-framework/bridges/phase-34/dossiers/Phase34-KI-dossier.md"
)
LEAN = SOURCE_ROOT / (
    "merged-framework/bridges/phase-34/lean/Phase34KIKernel.lean"
)

PINNED_HASHES = {
    SOURCE: "10e92457cbd213782e5778f5b739660a6d07ea229c44746e24fe0132844fcbd3",
    DOSSIER: "e01fbee40d81ebae1fc6f9452c321e2914cb185cdf257ae226d849ea6392702b",
    LEAN: "269c2b6b023fb1bfacb7dede2e708f09d3e08cad00bcc933e5149357ef5870f5",
    FRAMEWORK_ROOT / "governance/releases/current.yaml":
        "d530afe41d0e88e3236c0f048a1352394028006f9217ed8019b6fdd30f4f7cb6",
    FRAMEWORK_ROOT / "governance/claims.yaml":
        "b2d68ae4e293301d402de4a0292445805ff42e26871b058fc74427aac37b7a0f",
    FRAMEWORK_ROOT / "src/substrate_framework/crossovers.py":
        "0522233fecbcae6b76cb41373fe904d8558da2cd8ab9f13f35fe41b0a5189493",
    FRAMEWORK_ROOT / "tests/test_crossovers.py":
        "1768b63100fc5d69ce0676eb624d35d3e97eece41e1474788f90a3c48ce8d05e",
    FRAMEWORK_ROOT / "campaigns/P107-e4-bps-zero-binding-audit/adjudication.yaml":
        "06947b443bb6fb41fec59a199aab6051f5804a1c89bdcd00c3d5814a57fa7cd2",
    FRAMEWORK_ROOT / (
        "campaigns/P107-e4-bps-zero-binding-audit/evidence/"
        "check-adjudication.yaml"
    ): "0ae7a054976dba93d07b8e397f0e7461406ddab0123ebc3bbc405847eadff0d8",
    FRAMEWORK_ROOT / (
        "campaigns/P172-ki2-epsilon-underdetermination-audit/adjudication.yaml"
    ): "a15b42bd20a9dda1b498ce6b230fdded0c2ef5690ba2b7dbf718fc71dc13b746",
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_source() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SOURCE)],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _claims_by_id() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(
        (FRAMEWORK_ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    )
    return {claim["id"]: claim for claim in registry["claims"]}


def _spread_exceeds_source_threshold(ratio: object) -> bool:
    r = sp.sympify(ratio)
    inverses = (
        r / (1 - r),
        -sp.log(1 - r),
        sp.atanh(r),
        r / sp.sqrt(1 - r**2),
    )
    values = [float(sp.N(value, 40)) for value in inverses]
    return max(values) / min(values) > 1.05


def main() -> int:
    checks = CheckLedger("P173-KI3-BRACKET-SHARPNESS-AUDIT")
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
        re.match(r"(KI3\.[1-5])", ast.literal_eval(node.args[0])).group(1)
        for node in check_calls
    ]
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "KI3 has exactly its five advertised predicates in order",
        labels == [f"KI3.{index}" for index in range(1, 6)],
    )
    checks.check(
        "KI3 has one assertion and imports only SymPy",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1
        and imports == {"sympy"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "KI3 has no NumPy integration-name compatibility surface",
        compatibility.numpy_aliases == ()
        and compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    replay = _run_source()
    checks.check(
        "native KI3 executes all five predicates with its exact terminal tally",
        replay.returncode == 0
        and replay.stderr == ""
        and replay.stdout.count("  PASS\n") == 5
        and "ALL 5 CHECKS PASS" in replay.stdout,
        replay.stderr[-500:],
    )

    epsilon, kappa = sp.symbols("epsilon kappa", positive=True)
    normalized = (
        epsilon / (1 + epsilon),
        1 - sp.exp(-epsilon),
        sp.tanh(epsilon),
        epsilon / sp.sqrt(1 + epsilon**2),
    )
    expected_derivatives = (
        1 / (1 + epsilon) ** 2,
        sp.exp(-epsilon),
        1 / sp.cosh(epsilon) ** 2,
        1 / (1 + epsilon**2) ** sp.Rational(3, 2),
    )
    checks.check(
        "each selected representative has the two exact limiting values",
        all(
            sp.limit(function, epsilon, 0, "+") == 0
            and sp.limit(function, epsilon, sp.oo) == 1
            for function in normalized
        ),
    )
    checks.check(
        "each selected representative is strictly increasing on its positive domain",
        all(
            sp.simplify(sp.diff(function, epsilon) - expected) == 0
            and expected.is_positive is True
            for function, expected in zip(normalized, expected_derivatives, strict=True)
        ),
    )

    r = sp.symbols("r", positive=True)
    inverse_candidates = (
        r / (1 - r),
        -sp.log(1 - r),
        sp.atanh(r),
        r / sp.sqrt(1 - r**2),
    )
    half_inverses = tuple(
        sp.simplify(candidate.subs(r, sp.Rational(1, 2)))
        for candidate in inverse_candidates
    )
    direct_inverse_residuals = tuple(
        sp.simplify(function.subs(epsilon, inverse) - r)
        for function, inverse in zip(
            normalized[:3], inverse_candidates[:3], strict=True
        )
    )
    algebraic_inverse = inverse_candidates[3]
    checks.check(
        "the four exact inverses solve a generic level conditional on zero < r < 1",
        direct_inverse_residuals == (0, 0, 0)
        # Squaring the last positive-positive equation is reversible on (0, 1).
        and sp.simplify(
            algebraic_inverse**2 / (1 + algebraic_inverse**2) - r**2
        ) == 0,
    )
    checks.check(
        "a comparator-free half-level gives four distinct inverse parameters",
        all(
            sp.simplify(left - right) != 0
            for index, left in enumerate(half_inverses)
            for right in half_inverses[:index]
        ),
    )
    checks.check(
        "the selected positive-domain representatives attain neither limiting endpoint",
        all(
            sp.solve(sp.Eq(function, 0), epsilon) == []
            and sp.solve(sp.Eq(function, 1), epsilon) == []
            for function in normalized
        ),
    )
    checks.check(
        "KI3's own representatives therefore support open rather than closed ranges",
        "eps = sp.symbols(\"epsilon\", positive=True)" in source_text
        and "range is exactly the open interval (0, kappa_cl)" in source_text
        and "[0, kappa_cl]" in source_text,
    )

    base = epsilon / (1 + epsilon)
    bump = epsilon / (1 + epsilon) ** 2
    overshooting = sp.factor(base + 4 * bump)
    undershooting = sp.factor(base - 4 * bump)
    checks.check(
        "continuous endpoint-compatible functions can overshoot and undershoot",
        sp.limit(overshooting, epsilon, 0, "+") == 0
        and sp.limit(overshooting, epsilon, sp.oo) == 1
        and overshooting.subs(epsilon, 1) == sp.Rational(3, 2)
        and sp.limit(undershooting, epsilon, 0, "+") == 0
        and sp.limit(undershooting, epsilon, sp.oo) == 1
        and undershooting.subs(epsilon, 1) == -sp.Rational(1, 2),
    )
    repeated_roots = sp.solve(
        sp.Eq(overshooting, sp.Rational(6, 5)), epsilon
    )
    checks.check(
        "one endpoint-compatible map has two positive preimages above the alleged ceiling",
        repeated_roots
        == [
            sp.Rational(13, 2) - sp.sqrt(145) / 2,
            sp.Rational(13, 2) + sp.sqrt(145) / 2,
        ]
        and all(root.is_positive is True for root in repeated_roots),
    )
    overshoot_derivative = sp.factor(sp.diff(overshooting, epsilon))
    checks.check(
        "KI3's one-point derivative probe accepts a globally nonmonotone counterexample",
        sp.simplify(
            overshoot_derivative + (3 * epsilon - 5) / (epsilon + 1) ** 3
        ) == 0
        and overshoot_derivative.subs(epsilon, sp.Rational(1, 2)) > 0
        and overshoot_derivative.subs(epsilon, 2) < 0,
    )
    checks.check(
        "the source assumes the excluding codomain before declaring bracket equality",
        "continuous kappa:(0,inf)->(0,kappa_cl)" in source_text,
    )

    b2_source = sp.Rational(24154, 10000)
    b4_source = sp.Rational(45452, 10000)
    source_anchor = 3 * sp.pi**2 * (2 * b2_source - b4_source)
    claims = _claims_by_id()
    accepted_anchor = sp.Float("8.482417318795285", 30)
    checks.check(
        "KI3 recomputes a stale classical coordinate rather than accepted C-RDIFF-002",
        abs(sp.N(source_anchor, 30) - accepted_anchor) > sp.Rational(1, 50)
        and "8.482417318795285" in claims["C-RDIFF-002"]["statement"],
    )
    checks.check(
        "accepted C-RDIFF-002 explicitly denies a variational or BPS ceiling",
        "not a variational bound" in claims["C-RDIFF-002"]["statement"]
        and "BPS limit" in claims["C-RDIFF-002"]["statement"],
    )
    checks.check(
        "accepted C-BPS-003 explicitly supplies no global interpolation",
        "provide a global interpolation" in claims["C-BPS-003"]["statement"]
        and "may be positive, zero, or negative" in claims["C-BPS-003"]["statement"],
    )
    checks.check(
        "accepted C-BPS-002 conditions zero difference on actual sector attainment",
        "attains the C-BPS-001 equality" in claims["C-BPS-002"]["statement"]
        and "conditional attainment theorem" in claims["C-BPS-002"]["statement"],
    )
    p107_checks = yaml.safe_load(
        (
            FRAMEWORK_ROOT
            / "campaigns/P107-e4-bps-zero-binding-audit/evidence/check-adjudication.yaml"
        ).read_text(encoding="utf-8")
    )
    checks.check(
        "E4 review rejected strict nonzero first order and uncontrolled physical smallness",
        p107_checks["checks"]["E4.5"]["verdict"]
        == "algebra_qualified_as_C-BPS-003_broader_inference_rejected"
        and "positive, zero, or negative" in p107_checks["checks"]["E4.5"]["reason"],
    )
    p172 = yaml.safe_load(
        (
            FRAMEWORK_ROOT
            / "campaigns/P172-ki2-epsilon-underdetermination-audit/adjudication.yaml"
        ).read_text(encoding="utf-8")
    )
    checks.check(
        "KI2 authority is a qualified parameter-family result with no epsilon identification",
        p172["source_disposition"] == {"KI2": "qualified"}
        and p172["accepted_mappings"] == ["C-BPS-001", "C-SK-001"]
        and any(
            item["id"] == "identification_with_C-BPS-003_epsilon"
            for item in p172["unpromoted_claims"]
        ),
    )
    checks.check(
        "C-XOV-001 already makes continuity monotonicity and actual range load bearing",
        "real continuous strictly increasing function" in claims["C-XOV-001"]["statement"]
        and "actual range are independently load bearing" in claims["C-XOV-001"]["statement"]
        and "nonmonotone response can give multiple crossings"
        in claims["C-XOV-001"]["statement"],
    )

    ki34_condition = ast.unparse(check_calls[3].args[1])
    checks.check(
        "the empirical comparator feeds KI3.4's thresholded pass condition",
        ki34_condition == "len(backsolved) == len(interpolants) and spread > 1.05"
        and "ratio = KAPPA_EMP / KAPPA_CL" in source_text
        and "spread = max(backsolved.values()) / min(backsolved.values())"
        in source_text,
    )
    source_ratio = sp.Rational(929, 1000) / source_anchor
    checks.mutation_sensitive(
        "KI3.4's verdict changes when only its comparator level changes",
        _spread_exceeds_source_threshold,
        source_ratio,
        [sp.Rational(1, 10000)],
    )

    lean_text = LEAN.read_text(encoding="utf-8")
    checks.check(
        "the formal theorem proves surjectivity for one explicitly defined Pade map only",
        "noncomputable def kappa (K e : ℝ) : ℝ := K * e / (1 + e)"
        in lean_text
        and "theorem kappa_surjective (K y : ℝ)" in lean_text
        and "∃ e : ℝ, 0 < e ∧ kappa K e = y" in lean_text,
    )
    checks.check(
        "the formal statement does not quantify over an arbitrary interpolation function",
        "theorem kappa_surjective (K y : ℝ)" in lean_text
        and "theorem kappa_surjective (f" not in lean_text
        and "Continuous" not in lean_text[lean_text.index("theorem kappa_surjective"):
                                           lean_text.index("theorem backsolve_is_identity")],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
