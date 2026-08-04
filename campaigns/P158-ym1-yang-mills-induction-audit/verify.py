#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-NVP-001 and YM1."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.nonabelian_vacuum_polarization import (
    su2_scalar_qed2_vacuum_polarization,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P158-ym1-yang-mills-induction-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-7/"
    "bridge_YM1_yang_mills_induction.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
SOURCE_SHA256 = "bb8046bcf3a57d23bd50f9ac5ca6953cab8ffaaa2a2f852074495b48b6e83cf6"
FROZEN_SHA256 = "50be0d545a11c3a01f6a1a58f7691449d0d6717e3426090b38f8938f3c54e614"
REVISION_SHA256 = "4b82802d14ef94c283ac6f80b95786c8ff8f09884d086f34cb8ffc3c643481de"
REPRODUCTION_SHA256 = "835f487fe15a551fbf3d565bd254d901f06db833f052d30cf0d5f1850c9c2965"
SOURCE_AUDIT_SHA256 = "cf3d75ce5553f768ad6d1982aa35db8104c379b6d41ab86c6b23ef53aca36fa1"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _zero(matrix: sp.MatrixBase) -> bool:
    simplified = sp.Matrix(matrix).applyfunc(sp.simplify)
    return simplified == sp.zeros(*simplified.shape)


def _fundamental_generators() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )


def _adjoint_generators() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        sp.Matrix([[0, 0, 0], [0, 0, -sp.I], [0, sp.I, 0]]),
        sp.Matrix([[0, 0, sp.I], [0, 0, 0], [-sp.I, 0, 0]]),
        sp.Matrix([[0, -sp.I, 0], [sp.I, 0, 0], [0, 0, 0]]),
    )


def run() -> int:
    checks = CheckLedger("P158/C-NVP-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned YM1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check(
        "source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256
    )
    checks.check("source audit hash", _sha256(SOURCE_AUDIT) == SOURCE_AUDIT_SHA256)
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("nine source predicates", len(source_checks) == 9)
    checks.check("one source assertion", len(source_assertions) == 1)
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "YM1 has no NumPy integration compatibility shape",
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
    checks.check("native YM1 exits cleanly", native.returncode == 0)
    native_lines = [line.strip() for line in native.stdout.splitlines() if line.strip()]
    checks.check(
        "native YM1 terminal tally is exact",
        native_lines.count("ALL 9 CHECKS PASS") == 1,
    )

    q2, mass, coupling = sp.symbols("Q m g", positive=True)
    fundamental = su2_scalar_qed2_vacuum_polarization(
        _fundamental_generators(), q2, mass, coupling, species_count=2
    )
    checks.check(
        "fundamental generators close and have index one half",
        fundamental.dynkin_index == sp.Rational(1, 2)
        and fundamental.trace_metric == sp.eye(3) / 2
        and all(_zero(value) for value in fundamental.commutator_residuals),
    )
    checks.check(
        "color kernel is the representation index times the scalar kernel",
        fundamental.color_projector_coefficient
        == sp.eye(3) * fundamental.abelian_ledger.projector_coefficient / 2,
    )
    checks.check(
        "bubble and seagull cancel in every color before projection",
        fundamental.ward_tadpole_residual == sp.zeros(3)
        and fundamental.bubble_ward_tadpole_coefficient != sp.zeros(3)
        and fundamental.seagull_ward_tadpole_coefficient != sp.zeros(3),
    )
    checks.check(
        "deleting the seagull breaks the Ward contraction",
        fundamental.bubble_ward_tadpole_coefficient != sp.zeros(3),
    )
    checks.check(
        "sign-flipping the seagull breaks the Ward contraction",
        fundamental.bubble_ward_tadpole_coefficient
        - fundamental.seagull_ward_tadpole_coefficient
        != sp.zeros(3),
    )
    checks.check(
        "scalar parameter numerator differs from YM1",
        sp.factor(fundamental.abelian_ledger.projector_parameter_integrand).has(
            (2 * fundamental.abelian_ledger.parameter - 1) ** 2
        )
        and "u * (1 - u) * q2s" in source_text,
    )
    checks.check(
        "fixed-positive-momentum scalar massless limit diverges",
        fundamental.abelian_ledger.massless_projector_limit == sp.oo
        and fundamental.color_projector_coefficient
        != sp.eye(3) * coupling**2 / (2 * sp.pi),
    )
    checks.check(
        "zero-momentum and heavy-mass projector coefficients vanish",
        fundamental.abelian_ledger.zero_momentum_projector_limit == 0
        and fundamental.abelian_ledger.heavy_mass_projector_limit == 0,
    )
    checks.check(
        "local component coefficient contains the Dynkin index",
        fundamental.local_component_fmunu_squared_coefficient
        == coupling**2 / (48 * sp.pi * mass**2),
    )
    checks.check(
        "local trace coefficient keeps the representation trace explicit",
        fundamental.local_trace_fmunu_squared_coefficient
        == coupling**2 / (24 * sp.pi * mass**2)
        and sp.simplify(
            fundamental.local_component_fmunu_squared_coefficient
            - fundamental.dynkin_index
            * fundamental.local_trace_fmunu_squared_coefficient
        )
        == 0,
    )
    checks.check(
        "background-field coefficient independently matches the local trace term",
        fundamental.heat_kernel_curvature_weight == sp.Rational(1, 12)
        and fundamental.heat_kernel_free_factor == 1 / (4 * sp.pi)
        and fundamental.proper_time_mass_integral == 1 / mass**2
        and fundamental.covariant_completion_residual == 0,
    )
    checks.check(
        "real-scalar one-half mutation breaks the complex-scalar completion",
        sp.simplify(
            fundamental.heat_kernel_trace_fmunu_squared_coefficient / 2
            - fundamental.local_trace_fmunu_squared_coefficient
        )
        != 0,
    )

    adjoint = su2_scalar_qed2_vacuum_polarization(
        _adjoint_generators(), q2, mass, coupling, species_count=2
    )
    checks.check(
        "adjoint representation has index two",
        adjoint.dynkin_index == 2 and adjoint.trace_metric == 2 * sp.eye(3),
    )
    checks.check(
        "adjoint-to-fundamental component ratio is four",
        sp.simplify(
            adjoint.local_component_fmunu_squared_coefficient
            / fundamental.local_component_fmunu_squared_coefficient
        )
        == 4,
    )
    checks.check(
        "trace-density coefficient is representation-coordinate independent",
        adjoint.local_trace_fmunu_squared_coefficient
        == fundamental.local_trace_fmunu_squared_coefficient,
    )
    rescaled = tuple(2 * value for value in _fundamental_generators())
    try:
        su2_scalar_qed2_vacuum_polarization(rescaled, q2, mass, coupling)
    except ValueError as error:
        rejected_rescaling = "commutators" in str(error)
    else:
        rejected_rescaling = False
    checks.check(
        "fixed-structure-constant generator rescaling is rejected",
        rejected_rescaling,
    )
    checks.check(
        "omitting the Dynkin index mutates the fundamental kernel",
        fundamental.color_projector_coefficient
        != sp.eye(3) * fundamental.abelian_ledger.projector_coefficient,
    )

    bare, counterterm = sp.symbols("c_bare c_ct", real=True)
    loop = fundamental.local_component_fmunu_squared_coefficient
    total = bare + counterterm + loop
    checks.check(
        "loop contribution is additive rather than a unique total coefficient",
        sp.diff(total, bare) == 1
        and sp.diff(total, counterterm) == 1
        and total.subs({bare: 0, counterterm: 0}) == loop,
    )
    checks.check(
        "source declares g_eff instead of deriving bare and counterterm data",
        "g_eff2 = (2 * sp.pi) / g**2" in source_text
        and "counterterm" not in source_text.lower(),
    )
    checks.check(
        "source has no determinant regulator bubble or seagull construction",
        not {
            "determinant",
            "regularization",
            "loop_momentum",
            "bubble_integral",
            "seagull_integral",
        }.intersection(
            {
                node.id
                for node in ast.walk(tree)
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
            }
        ),
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/nonabelian_vacuum_polarization.py",
        ROOT / "tests/test_nonabelian_vacuum_polarization.py",
    ]
    reports = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P158 and canonical code has no legacy integration access",
        all(report.legacy_references == 0 for report in reports),
    )
    checks.check(
        "mutable P158 has no eager legacy default fallback",
        all(report.eager_legacy_default_fallbacks == 0 for report in reports),
    )

    tally = checks.finish()
    print(f"P158 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
