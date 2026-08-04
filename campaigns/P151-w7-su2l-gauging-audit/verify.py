#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-NAG-001 and W7."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.nonabelian_gauge import (
    local_nonabelian_gauge_ledger,
    nonabelian_covariant_derivative,
    nonabelian_field_strength,
    su2_projected_connection,
    su2_projected_unitary,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su2_doublets import (
    su2_chiral_factor_ledger,
    su2_same_carrier_projector_ledger,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P151-w7-su2l-gauging-audit"
SOURCE = Path("/home/dan/substrate/merged-framework/bridges/phase-6/bridge_W7_su2L_gauging_charged_current.py")
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_SHA256 = "1a1fa278f6b8a0cab74d020fc01db1fa3576f57084d0cd80959867c591bf66c3"
FROZEN_SHA256 = "ffff59b623899eafa418fd165a7e97a1d004457b75a20296ddfe885b05b8fbaa"
REVISION_SHA256 = "75a89e768497a820cf2a26239d694b4a9cc62d18a170522d87e27ced3293590c"
REPRODUCTION_SHA256 = "431b059cc027c1266057738c182658499dab3f65b5da7fd9770754a8dab04875"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _zero(matrix: sp.MatrixBase) -> bool:
    return sp.Matrix(matrix).applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def run() -> int:
    checks = CheckLedger("P151/C-NAG-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned W7 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check("source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256)
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("eleven source predicates", len(source_checks) == 11)
    checks.check("one source assertion", len(source_assertions) == 1)
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "W7 has no NumPy integration compatibility shape",
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
    checks.check("native W7 exits cleanly", native.returncode == 0)
    checks.check(
        "native W7 terminal tally is exact",
        native.stdout.rstrip().endswith("ALL 11 CHECKS PASS"),
    )

    time, coordinate = sp.symbols("t x", real=True)
    coupling = sp.symbols("g", positive=True)
    alpha = sp.Function("alpha", real=True)(time, coordinate)
    unitary = sp.diag(sp.exp(sp.I * alpha / 2), sp.exp(-sp.I * alpha / 2))
    generators = (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )
    components = [
        sp.Function(f"w{mu}{index}", real=True)(time, coordinate)
        for mu in range(2)
        for index in range(3)
    ]
    connections = tuple(
        sum(
            (
                components[3 * mu + index] * generators[index]
                for index in range(3)
            ),
            sp.zeros(2),
        )
        for mu in range(2)
    )
    field = sp.Matrix(
        [
            sp.Function("psi0")(time, coordinate),
            sp.Function("psi1")(time, coordinate),
        ]
    )
    ledger = local_nonabelian_gauge_ledger(
        field,
        connections,
        unitary,
        (time, coordinate),
        coupling,
    )
    checks.check(
        "correct finite connection sign gives derivative covariance",
        all(_zero(residual) for residual in ledger.covariance_residuals),
    )
    checks.check(
        "curvature transforms by conjugation",
        _zero(ledger.curvature_covariance_residual),
    )
    checks.check(
        "covariant commutator derives the curvature",
        _zero(ledger.commutator_curvature_residual),
    )
    checks.check(
        "curvature trace square is invariant",
        ledger.trace_invariance_residual == 0,
    )

    zero_connection = sp.zeros(2)
    correct_shift = ledger.transformed_connections[0].subs(
        {
            component: 0
            for component in components
        }
    )
    checks.check(
        "correct inhomogeneous shift has the positive T3 component",
        _zero(
            correct_shift
            - sp.diff(alpha, time) / coupling * generators[2]
        ),
    )
    wrong_connection = sp.simplify(
        unitary * zero_connection * unitary.H
        + sp.I / coupling * unitary.diff(time) * unitary.H
    )
    wrong_residual = nonabelian_covariant_derivative(
        unitary * field,
        wrong_connection,
        time,
        coupling,
    ) - unitary * nonabelian_covariant_derivative(
        field,
        zero_connection,
        time,
        coupling,
    )
    checks.check(
        "W7 inhomogeneous-sign mutation breaks full covariance",
        not _zero(wrong_residual),
    )
    checks.check(
        "W7 CHECK1 evaluates only the homogeneous connection rotation",
        "We absorb the 1/g by working with the connection" in source_text
        and "The d_mu alpha inhomogeneous shift is the abelian" in source_text,
    )

    projector = sp.diag(1, 0)
    carrier = su2_chiral_factor_ledger(
        projector,
        parity_exchange=sp.Matrix([[0, 1], [1, 0]]),
    )
    projected = su2_projected_connection(
        sp.symbols("W1 W2 W3", real=True),
        projector,
    )
    right_block = sp.kronecker_product(
        sp.eye(2),
        carrier.complementary_projector,
    )
    checks.check(
        "independent-factor left generators are Hermitian and close",
        all(_zero(residual) for residual in carrier.left_hermiticity_residuals)
        and all(_zero(residual) for residual in carrier.left_commutator_residuals),
    )
    checks.check(
        "projected SU2 connection annihilates the right block",
        projected.shape == (4, 4) and _zero(projected * right_block),
    )
    projected_unitary = su2_projected_unitary(unitary, projector)
    checks.check(
        "projected finite transformation is identity on the right block",
        _zero(projected_unitary * right_block - right_block),
    )
    same_carrier = su2_same_carrier_projector_ledger(projector)
    checks.check(
        "W7 same-carrier left generators fail Hermiticity and closure",
        sum(_zero(residual) for residual in same_carrier.hermiticity_residuals) == 1
        and not all(_zero(residual) for residual in same_carrier.commutator_residuals),
    )
    checks.check(
        "parity exchanges left and right rather than making left odd",
        all(_zero(residual) for residual in carrier.parity_left_to_right_residuals or ())
        and any(
            not _zero(left + right)
            for left, right in zip(
                carrier.left_generators,
                carrier.right_generators,
                strict=True,
            )
        ),
    )

    raising = generators[0] + sp.I * generators[1]
    lowering = generators[0] - sp.I * generators[1]
    upper, lower = sp.Matrix([1, 0]), sp.Matrix([0, 1])
    checks.check(
        "charged ladder matrix elements are exact representation data",
        (upper.T * raising * lower)[0] == 1
        and (lower.T * lowering * upper)[0] == 1,
    )
    checks.check(
        "W7 assigned charge labels change by two not one",
        sp.Integer(1) - sp.Integer(-1) == 2
        and sp.Rational(1, 2) - sp.Rational(-1, 2) == 1,
    )
    checks.check(
        "source inserts unit winding separately from its charge labels",
        "dQ_event = sp.Integer(1)" in source_text
        and "kink = sp.Matrix([1, 0])        # Q = +1" in source_text
        and "antikink = sp.Matrix([0, 1])    # Q = -1" in source_text,
    )

    noncommuting_curvature = nonabelian_field_strength(
        (generators[0], generators[1]),
        (time, coordinate),
        coupling,
    )
    checks.check(
        "noncommuting connections have nonzero algebraic curvature",
        not _zero(noncommuting_curvature),
    )
    checks.check(
        "curl-only mutation misses the non-Abelian curvature",
        _zero(generators[1].diff(time) - generators[0].diff(coordinate))
        and not _zero(noncommuting_curvature),
    )

    checks.check(
        "W7 kinetic check expands only one component",
        "a_idx = 0" in source_text
        and "FaFa = sp.expand(Fa * Fa)" in source_text,
    )
    loaded_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    checks.check(
        "W7 contains no action variation source equation or matter-current construction",
        not loaded_names.intersection(
            {"euler_lagrange", "functional_derivative", "matter_current", "psi_bar", "gamma_mu"}
        ),
    )
    checks.check(
        "W7 g-to-impedance relation is declared rather than derived",
        "g_sq_related = k * Z" in source_text
        and "k = sp.Symbol(\"k\", positive=True)" in source_text,
    )
    checks.check(
        "accepted W5 theorem supplies no lambda-mu coupling match",
        "lambda" not in (ROOT / "src/substrate_framework/boundary_scattering.py").read_text(
            encoding="utf-8"
        ),
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/nonabelian_gauge.py"
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P151 and canonical code has no legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P151 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
