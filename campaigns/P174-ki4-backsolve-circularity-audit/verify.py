#!/usr/bin/env python3
"""Exact inverse-domain, conditioning, graph, and comparator audit of KI4."""

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


ROOT = Path("/home/dan/substrate-framework")
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / "merged-framework/bridges/phase-34/bridge_KI4_backsolve_circularity.py"
DOSSIER = SOURCE_ROOT / "merged-framework/bridges/phase-34/dossiers/Phase34-KI-dossier.md"
LEAN = SOURCE_ROOT / "merged-framework/bridges/phase-34/lean/Phase34KIKernel.lean"
PINNED_HASHES = {
    SOURCE: "138f204c2bf7e7278a1a4aadad4bed1680e11b6b6de7189a02640a81652f00cd",
    DOSSIER: "e01fbee40d81ebae1fc6f9452c321e2914cb185cdf257ae226d849ea6392702b",
    LEAN: "269c2b6b023fb1bfacb7dede2e708f09d3e08cad00bcc933e5149357ef5870f5",
    ROOT / "governance/releases/current.yaml": "d530afe41d0e88e3236c0f048a1352394028006f9217ed8019b6fdd30f4f7cb6",
    ROOT / "governance/claims.yaml": "b2d68ae4e293301d402de4a0292445805ff42e26871b058fc74427aac37b7a0f",
    ROOT / "src/substrate_framework/crossovers.py": "0522233fecbcae6b76cb41373fe904d8558da2cd8ab9f13f35fe41b0a5189493",
    ROOT / "src/substrate_framework/gravity_scale_confrontation.py": "0b6018a5195759a2d4dbd3fc9775f86f3449ebf182855261a640759e6f70317c",
    ROOT / "src/substrate_framework/linear_systems.py": "c22a768b0f82acfc0774e3fbeac2e59b1e3536b674a9bb1bf8f2248816687311",
    ROOT / "campaigns/P173-ki3-bracket-sharpness-audit/adjudication.yaml": "8832c2e5af974d8ef1d2d3bf58a742ef1559c7cc133af31e1341389f269c894b",
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_source() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SOURCE)], check=False, capture_output=True, text=True,
        timeout=120, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _toposort(graph: dict[str, tuple[str, ...]]) -> bool:
    nodes = set(graph) | {target for targets in graph.values() for target in targets}
    indegree = {node: 0 for node in nodes}
    for targets in graph.values():
        for target in targets:
            indegree[target] += 1
    queue = [node for node, degree in indegree.items() if degree == 0]
    visited = 0
    while queue:
        node = queue.pop()
        visited += 1
        for target in graph.get(node, ()):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return visited == len(nodes)


def _source_disagreement_passes(comparator: object) -> bool:
    b2, b4 = sp.Rational(24154, 10000), sp.Rational(45452, 10000)
    source_point = 3 * sp.pi**2 * (2 * b2 - b4)
    return bool(float(source_point / sp.sympify(comparator)) > 5.0)


def main() -> int:
    checks = CheckLedger("P174-KI4-INVERSE-CONDITIONING-GRAPH-AUDIT")
    for path, expected in PINNED_HASHES.items():
        checks.check(f"pinned artifact {path.name} retains its audited bytes", _digest(path) == expected)

    text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(SOURCE))
    calls = sorted(
        (node for node in ast.walk(tree) if isinstance(node, ast.Call)
         and isinstance(node.func, ast.Name) and node.func.id == "check"),
        key=lambda node: node.lineno,
    )
    labels = [re.match(r"(KI4\.[1-5])", ast.literal_eval(node.args[0])).group(1) for node in calls]
    imports = {alias.name for node in tree.body if isinstance(node, ast.Import) for alias in node.names}
    checks.check("KI4 has exactly five advertised predicates in order", labels == [f"KI4.{i}" for i in range(1, 6)])
    checks.check(
        "KI4 has one assertion and imports only SymPy",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1 and imports == {"sympy"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(text, filename=str(SOURCE))
    checks.check(
        "KI4 has no NumPy integration-name compatibility surface",
        compatibility.numpy_aliases == () and compatibility.legacy_references == 0
        and compatibility.current_references == 0 and compatibility.eager_legacy_default_fallbacks == 0,
    )
    replay = _run_source()
    checks.check(
        "native KI4 executes all five predicates with its exact terminal tally",
        replay.returncode == 0 and replay.stderr == "" and replay.stdout.count("  PASS\n") == 5
        and "ALL 5 CHECKS PASS" in replay.stdout,
        replay.stderr[-500:],
    )

    e, r = sp.symbols("e r", positive=True)
    maps = (e / (1 + e), 1 - sp.exp(-e), sp.tanh(e))
    inverses = (r / (1 - r), -sp.log(1 - r), sp.atanh(r))
    checks.check(
        "the three inverse compositions are exact conditional on zero < r < 1",
        all(sp.simplify(function.subs(e, inverse) - r) == 0 for function, inverse in zip(maps, inverses, strict=True)),
    )
    half = sp.Rational(1, 2)
    half_inverse = tuple(sp.simplify(inverse.subs(r, half)) for inverse in inverses)
    checks.check(
        "an in-range target gives three positive exact reconstructions",
        half_inverse == (1, sp.log(2), sp.atanh(sp.Rational(1, 2)))
        and all(value.is_positive is True for value in half_inverse),
    )
    outside_inverse = tuple(sp.simplify(inverse.subs(r, 2)) for inverse in inverses)
    checks.check(
        "a positive but out-of-range target invalidates the source's arbitrary-y reading",
        outside_inverse[0] == -2
        and outside_inverse[1].is_real is False
        and outside_inverse[2].is_real is False,
    )
    checks.check(
        "the source declares y positive but carries no y less than K premise",
        "eps, y = sp.symbols(\"epsilon y\", positive=True)" in text
        and "y < K" not in text and "K - y" in text,
    )

    parameter_prior = sp.Interval.open(0, sp.oo)
    parameter_after_half = sp.FiniteSet(1)
    output_support = sp.Interval.open(0, 1)
    checks.check(
        "an exact observation through a fixed injective map reduces parameter uncertainty",
        parameter_after_half.is_subset(parameter_prior)
        and parameter_after_half != parameter_prior,
    )
    checks.check(
        "the union over all hypothetical targets equals output support but is not an observed-target posterior",
        output_support == sp.Interval.open(0, 1)
        and parameter_after_half != output_support,
    )
    posterior_assignments = [
        node for node in ast.walk(tree) if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "posterior" for target in node.targets)
    ]
    checks.check(
        "KI4.2 assigns posterior equal to prior after only eleven sampled positivity tests",
        len(posterior_assignments) == 1
        and isinstance(posterior_assignments[0].value, ast.IfExp)
        and ast.unparse(posterior_assignments[0].value) == "prior if all_admissible else None"
        and "range(1, 12)" in text,
    )

    noninjective = 4 * e / (1 + e) ** 2
    roots = sp.solve(sp.Eq(noninjective, half), e)
    checks.check(
        "an endpoint-compatible noninjective map has a multivalued back-solve",
        sp.limit(noninjective, e, 0, "+") == 0
        and sp.limit(noninjective, e, sp.oo) == 0
        and roots == [3 - 2 * sp.sqrt(2), 2 * sp.sqrt(2) + 3]
        and all(root.is_positive is True for root in roots),
    )
    checks.check(
        "a constant admissible-shape candidate cannot reconstruct an arbitrary target",
        sp.solve(sp.Eq(sp.Rational(1, 2), sp.Rational(1, 3)), e) == [],
    )

    fit_graph = {
        "observed_y": ("fitted_epsilon", "residual"),
        "fitted_epsilon": ("predicted_y",),
        "predicted_y": ("residual",),
    }
    fabricated_cycle_graph = {**fit_graph, "predicted_y": ("residual", "observed_y")}
    checks.check(
        "ordinary same-datum reconstruction has an acyclic computational graph",
        _toposort(fit_graph) and not _toposort(fabricated_cycle_graph),
    )
    checks.check(
        "KI4 manufactures its graph cycle by adding a result-to-observed-input edge",
        'backsolved["kappa_predicted"] = ["kappa_emp (comparator)"]' in text,
    )

    theta = sp.symbols("theta", real=True)
    observed_y, held_out_z = sp.Integer(2), sp.Integer(6)
    fitted_theta = observed_y
    predicted_z = fitted_theta**2 + 1
    checks.check(
        "calibration can make a distinct held-out observable falsifiable",
        sp.simplify(theta.subs(theta, fitted_theta) - observed_y) == 0
        and predicted_z == 5 and sp.simplify(predicted_z - held_out_z) == -1,
    )

    condition4 = ast.unparse(calls[3].args[1])
    checks.check(
        "the empirical comparator feeds KI4.4's pass condition",
        condition4 == "collapses_to_point and disagreement > 5.0"
        and "disagreement = float(derived_point / KAPPA_EMP)" in text,
    )
    source_comparator = sp.Rational(929, 1000)
    b2, b4 = sp.Rational(24154, 10000), sp.Rational(45452, 10000)
    source_point = 3 * sp.pi**2 * (2 * b2 - b4)
    checks.mutation_sensitive(
        "KI4.4's verdict changes when only the comparator changes",
        _source_disagreement_passes, source_comparator, [source_point],
    )
    checks.check(
        "KI4.5's derivation verdict is a hard-coded boolean rather than a derived predicate",
        "backsolve_is_a_derivation = False" in text
        and "and (not backsolve_is_a_derivation)" in ast.unparse(calls[4].args[1]),
    )
    claims_data = yaml.safe_load((ROOT / "governance/claims.yaml").read_text(encoding="utf-8"))
    claims = {claim["id"]: claim for claim in claims_data["claims"]}
    checks.check(
        "C-IDN-002 already classifies same-row zero residual as inverse reconstruction",
        "zero residual by construction" in claims["C-IDN-002"]["statement"]
        and "inverse reconstruction" in claims["C-IDN-002"]["statement"]
        and "not an independent over-determination test" in claims["C-IDN-002"]["statement"],
    )
    checks.check(
        "C-XOV-001 makes map range and monotonicity load-bearing inverse premises",
        "continuous strictly increasing function" in claims["C-XOV-001"]["statement"]
        and "actual range are independently load bearing" in claims["C-XOV-001"]["statement"],
    )
    p173 = yaml.safe_load((ROOT / "campaigns/P173-ki3-bracket-sharpness-audit/adjudication.yaml").read_text())
    checks.check(
        "P173 supplies examples but rejects KI4's framework-wide bracket premise",
        p173["source_disposition"] == {"KI3": "qualified"}
        and any(item["id"] == "framework_wide_exact_bracket" for item in p173["unpromoted_claims"]),
    )
    accepted_point = sp.Float("8.482417318795285", 30)
    checks.check(
        "KI4 uses the stale source coordinate rather than accepted C-RDIFF-002",
        abs(sp.N(source_point, 30) - accepted_point) > sp.Rational(1, 50)
        and "8.482417318795285" in claims["C-RDIFF-002"]["statement"],
    )

    lean = LEAN.read_text(encoding="utf-8")
    checks.check(
        "Lean proves same-datum reconstruction for one explicitly defined Pade map",
        "noncomputable def kappa (K e : ℝ) : ℝ := K * e / (1 + e)" in lean
        and "theorem backsolve_is_identity (K y : ℝ)" in lean,
    )
    checks.check(
        "Lean's alleged posterior set explicitly intersects the prior before proving equality",
        "{y ∈ Set.Ioo (0:ℝ) K | ∃ e : ℝ, 0 < e ∧ kappa K e = y} = Set.Ioo (0:ℝ) K" in lean,
    )
    checks.check(
        "Lean encodes no observed target conditioned parameter posterior or information measure",
        all(token not in lean for token in ("posteriorEpsilon", "Observed", "entropy", "mutualInformation")),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
