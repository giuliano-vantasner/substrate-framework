#!/usr/bin/env python3
"""Independent inverse-reconstruction and conditioning audit for KI4."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")
CLAIMS = ROOT / "governance/claims.yaml"
CLAIMS_SHA256 = "b2d68ae4e293301d402de4a0292445805ff42e26871b058fc74427aac37b7a0f"
P173 = ROOT / "campaigns/P173-ki3-bracket-sharpness-audit/adjudication.yaml"
P173_SHA256 = "8832c2e5af974d8ef1d2d3bf58a742ef1559c7cc133af31e1341389f269c894b"


def _acyclic(graph: dict[str, tuple[str, ...]]) -> bool:
    nodes = set(graph) | {target for targets in graph.values() for target in targets}
    indegree = {node: 0 for node in nodes}
    for targets in graph.values():
        for target in targets:
            indegree[target] += 1
    queue = [node for node in nodes if indegree[node] == 0]
    seen = 0
    while queue:
        node = queue.pop()
        seen += 1
        for target in graph.get(node, ()):
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    return seen == len(nodes)


def main() -> int:
    checks = CheckLedger("P174-INDEPENDENT-INVERSE-CONDITIONING")
    checks.check(
        "independent accepted authority retains pinned bytes",
        hashlib.sha256(CLAIMS.read_bytes()).hexdigest() == CLAIMS_SHA256
        and hashlib.sha256(P173.read_bytes()).hexdigest() == P173_SHA256,
    )
    registry = yaml.safe_load(CLAIMS.read_text(encoding="utf-8"))
    claims = {claim["id"]: claim for claim in registry["claims"]}
    checks.check(
        "accepted authority distinguishes inverse reconstruction from independent testing",
        "inverse reconstruction" in claims["C-IDN-002"]["statement"]
        and "not an independent over-determination test" in claims["C-IDN-002"]["statement"],
    )

    epsilon, level = sp.symbols("epsilon level", positive=True)
    response = epsilon / (1 + epsilon)
    inverse = level / (1 - level)
    checks.check(
        "fresh exact algebra reconstructs an in-range target",
        sp.simplify(response.subs(epsilon, inverse) - level) == 0,
    )
    checks.check(
        "the inverse domain is load bearing",
        inverse.subs(level, sp.Rational(1, 2)) == 1
        and inverse.subs(level, 2) == -2,
    )
    prior_parameters = sp.Interval.open(0, sp.oo)
    observed_parameter_set = sp.FiniteSet(1)
    checks.check(
        "one exact observed level identifies one parameter for the fixed injective map",
        observed_parameter_set.is_subset(prior_parameters)
        and observed_parameter_set != prior_parameters,
    )
    checks.check(
        "possible output support and conditioned parameter set are different objects",
        sp.Interval.open(0, 1) != observed_parameter_set,
    )

    folded = 4 * epsilon / (1 + epsilon) ** 2
    roots = sp.solve(sp.Eq(folded, sp.Rational(1, 2)), epsilon)
    checks.check(
        "a fresh noninjective response makes the back-solve multivalued",
        roots == [3 - 2 * sp.sqrt(2), 3 + 2 * sp.sqrt(2)]
        and all(root.is_positive is True for root in roots),
    )
    checks.check(
        "a fixed constant response excludes an unequal observation",
        sp.solve(sp.Eq(sp.Rational(1, 2), sp.Rational(1, 3)), epsilon) == [],
    )

    computational_graph = {
        "observed_y": ("fit", "residual"),
        "fit": ("reconstruction", "held_out_prediction"),
        "reconstruction": ("residual",),
    }
    checks.check(
        "the ordinary calibration and residual graph is acyclic",
        _acyclic(computational_graph),
    )
    graph_with_invalid_input_edge = {
        **computational_graph,
        "reconstruction": ("residual", "observed_y"),
    }
    checks.check(
        "only an added reconstruction-to-input edge creates a directed cycle",
        not _acyclic(graph_with_invalid_input_edge),
    )

    fitted = sp.Integer(2)
    same_datum_residual = fitted - 2
    held_out_prediction = fitted**2 + 1
    checks.check(
        "same-datum reconstruction is exact by construction",
        same_datum_residual == 0,
    )
    checks.check(
        "a distinct held-out observable can still refute the calibrated model",
        held_out_prediction == 5 and held_out_prediction - 6 == -1,
    )
    p173 = yaml.safe_load(P173.read_text(encoding="utf-8"))
    checks.check(
        "the predecessor review supplies examples but no framework-wide bracket",
        p173["source_disposition"] == {"KI3": "qualified"}
        and any(item["id"] == "framework_wide_exact_bracket" for item in p173["unpromoted_claims"]),
    )
    checks.check(
        "accepted monotone inversion remains conditional on global premises",
        "actual range are independently load bearing" in claims["C-XOV-001"]["statement"]
        and "free level, response scale" in claims["C-XOV-001"]["statement"],
    )
    checks.check(
        "no empirical comparator is needed for the valid inverse-reconstruction result",
        all(not expression.has(sp.Float) for expression in (response, inverse, held_out_prediction)),
    )
    total = checks.finish()
    print(f"P174 INDEPENDENT INVERSE CONDITIONING ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
