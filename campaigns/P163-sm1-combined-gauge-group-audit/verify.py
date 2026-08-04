#!/usr/bin/env python3
"""Exact source-aware verifier for the SM1 product-gauge claim delta."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.product_gauge import (
    product_gauge_connection_component,
    standard_product_gauge_algebra,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P163-sm1-combined-gauge-group-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-9/"
    "bridge_SM1_combined_gauge_group.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
CHECK_ADJUDICATION = CAMPAIGN / "evidence/check-adjudication.yaml"
SOURCE_SHA256 = "bb7b70bc2ac0dd703f95ccbbaf843d40e78279f357795b9be74d6eee484749f2"
FROZEN_SHA256 = "b5d363206208eafb93e4ab145fa6a8c14ac0537e9a25fb8c2e1d5b2b5ae45f1b"
REVISION_SHA256 = "9e447100cf057ac7e3bfff7aea081857ac128311b812c7d2819551f9390d5a6a"
REPRODUCTION_SHA256 = "035d93f344bdde88166a9684197677c0d93238762690a258f1d002ab43469c0d"
SOURCE_AUDIT_SHA256 = "a42ce033dd2f9f890c84c3603ae26e4da6a02e5d0ebeb3a8dcfa38350c530e8a"
CHECK_ADJUDICATION_SHA256 = (
    "0148260e5cb03d0ddc98f361e0ed2fe7a87acd18a07f3bc2f4c9de9af4e3b5ae"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    checks = CheckLedger("P163/SM1")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned SM1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial frozen proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("source-aware revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check("source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256)
    checks.check("source audit hash", _sha256(SOURCE_AUDIT) == SOURCE_AUDIT_SHA256)
    checks.check(
        "predicate adjudication hash",
        _sha256(CHECK_ADJUDICATION) == CHECK_ADJUDICATION_SHA256,
    )

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check("six source predicates", len(source_checks) == 6)
    checks.check("one source assertion", len(source_assertions) == 1)
    checks.check(
        "SM1 has no NumPy integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = subprocess.run(
        [sys.executable, str(SOURCE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    native_lines = [line.strip() for line in native.stdout.splitlines() if line.strip()]
    checks.check("native SM1 exits cleanly", native.returncode == 0)
    checks.check(
        "native SM1 terminal tally is exact",
        native_lines.count("ALL 6 CHECKS PASS") == 1,
    )

    algebra = standard_product_gauge_algebra(sp.Integer(1))
    checks.check(
        "canonical product theorem checks every factor bracket",
        len(algebra.color_commutator_residuals) == 64
        and len(algebra.isospin_commutator_residuals) == 9
        and all(
            residual == sp.zeros(6)
            for residual in algebra.color_commutator_residuals
            + algebra.isospin_commutator_residuals
        ),
    )
    checks.check(
        "all thirty-five cross brackets vanish",
        len(algebra.cross_commutator_residuals) == 35
        and all(
            residual == sp.zeros(6)
            for residual in algebra.cross_commutator_residuals
        ),
    )
    checks.check(
        "non-Abelian factors remain noncommutative",
        algebra.color_embeddings[0] * algebra.color_embeddings[1]
        - algebra.color_embeddings[1] * algebra.color_embeddings[0]
        != sp.zeros(6)
        and algebra.isospin_embeddings[0] * algebra.isospin_embeddings[1]
        - algebra.isospin_embeddings[1] * algebra.isospin_embeddings[0]
        != sp.zeros(6),
    )
    checks.check(
        "nonzero Abelian weight gives a faithful twelve-generator local representation",
        len(algebra.generators) == 12
        and algebra.flattened_generator_matrix.shape == (36, 12)
        and algebra.generator_rank == 12,
    )
    scaled = standard_product_gauge_algebra(sp.Rational(7, 3))
    checks.check(
        "nonzero weight rescaling changes normalization but not local rank",
        scaled.abelian_generator == sp.Rational(7, 3) * sp.eye(6)
        and scaled.generator_rank == algebra.generator_rank == 12,
    )
    try:
        standard_product_gauge_algebra(sp.Integer(0))
    except ValueError as failure:
        zero_rejected = "nonzero" in str(failure)
    else:
        zero_rejected = False
    checks.check("zero Abelian weight is rejected as nonfaithful", zero_rejected)
    checks.check(
        "SM1 hides the nonzero premise inside its rank specialization",
        'Y = sp.Symbol("Y", real=True)' in source_text
        and "gens = Ta6 + Wi6 + [YB6.subs(Y, 1)]" in source_text,
    )

    checks.check(
        "canonical joint commutant is exactly the scalar span",
        algebra.joint_commutant_basis == (sp.ImmutableMatrix(sp.eye(6)),),
    )
    mixed = sp.kronecker_product(
        algebra.color_generators[0], algebra.isospin_generators[0]
    )
    checks.check(
        "mixed tensor mutation leaves the joint commutant",
        any(
            residual != sp.zeros(6)
            for residual in algebra.factor_commutator_residuals(mixed)
        ),
    )
    checks.check(
        "SM1's one rejected example does not itself prove uniqueness",
        "Y_bad = kron(Tc[0], tau[0])" in source_text
        and "joint_commutant" not in source_text
        and "nullspace" not in source_text,
    )

    half_weight = standard_product_gauge_algebra(sp.Rational(1, 2))
    checks.check(
        "compact U1 full-turn periodicity is independent of local rank",
        algebra.compact_u1_single_valued
        and algebra.compact_u1_full_turn_residual == sp.zeros(6)
        and not half_weight.compact_u1_single_valued
        and half_weight.compact_u1_full_turn == -sp.eye(6)
        and half_weight.generator_rank == 12,
    )
    checks.check(
        "SM1 supplies no compact period quotient or center kernel",
        "quotient" not in source_text.lower()
        and "kernel" not in source_text.lower()
        and "2 * sp.pi" not in source_text,
    )

    color_components = sp.symbols("G0:8", real=True)
    isospin_components = sp.symbols("W0:3", real=True)
    abelian_component = sp.symbols("B", real=True)
    couplings = sp.symbols("g_s g g_Y", positive=True)
    connection = product_gauge_connection_component(
        algebra,
        color_components,
        isospin_components,
        abelian_component,
        couplings,
    )
    expected_color_direction = sum(
        (
            component * generator
            for component, generator in zip(
                color_components, algebra.color_embeddings, strict=True
            )
        ),
        sp.zeros(6),
    )
    expected_isospin_direction = sum(
        (
            component * generator
            for component, generator in zip(
                isospin_components, algebra.isospin_embeddings, strict=True
            )
        ),
        sp.zeros(6),
    )
    expected_abelian_direction = abelian_component * algebra.abelian_generator
    checks.check(
        "canonical algebra-valued component is an exact three-term sum",
        sp.simplify(
            connection.total
            - connection.color_term
            - connection.isospin_term
            - connection.abelian_term
        )
        == sp.zeros(6),
    )
    checks.check(
        "independent coupling mutations affect their supplied blocks",
        sp.simplify(
            sp.diff(connection.color_term, couplings[0]) - expected_color_direction
        )
        == sp.zeros(6)
        and sp.simplify(
            sp.diff(connection.isospin_term, couplings[1])
            - expected_isospin_direction
        )
        == sp.zeros(6)
        and sp.simplify(
            sp.diff(connection.abelian_term, couplings[2])
            - expected_abelian_direction
        )
        == sp.zeros(6),
    )

    coordinate = sp.symbols("x", real=True)
    local_parameter = sp.Function("alpha")(coordinate)
    field = sp.Function("psi")(coordinate)
    phase = sp.exp(sp.I * local_parameter)
    bare_derivative_residual = sp.simplify(
        sp.diff(phase * field, coordinate) - phase * sp.diff(field, coordinate)
    )
    checks.check(
        "constant norm invariance is not local derivative covariance",
        bare_derivative_residual
        == sp.I * phase * field * sp.diff(local_parameter, coordinate)
        and bare_derivative_residual != 0,
    )
    checks.check(
        "SM1 phase probe is global and contains no connection transformation",
        'alpha = sp.Symbol("alpha", real=True)' in source_text
        and "sp.diff(alpha" not in source_text
        and "transformed_connection" not in source_text,
    )
    checks.check(
        "SM1 constructs no physical gauge dynamics",
        "action" not in {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
        }
        and "lagrangian" not in source_text.lower()
        and "field_equation" not in source_text,
    )
    checks.check(
        "SM1 imports physical labels from already-qualified predecessors",
        "each with a GENERATED kinetic term" in source_text
        and "left-quark-doublet space" in source_text,
    )

    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in CAMPAIGN.rglob("*.py")
    ]
    checks.check(
        "mutable P163 has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )
    checks.check(
        "mutable P163 has no eager legacy fallback",
        all(item.eager_legacy_default_fallbacks == 0 for item in mutable_compatibility),
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P163 PRIMARY ALL {result} CHECKS PASS")
