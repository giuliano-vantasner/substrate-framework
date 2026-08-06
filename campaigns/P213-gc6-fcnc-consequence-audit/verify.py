#!/usr/bin/env python3
"""Primary exact and numeric verifier for the GC6 consequence audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
from scipy.linalg import eigh_tridiagonal
import sympy as sp
import yaml

from substrate_framework.multi_scalar_flavor import (
    multi_scalar_mass_basis_ledger,
    off_diagonal_part,
    takagi_multi_scalar_mass_basis_ledger,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / "merged-framework/bridges/phase-42/bridge_GC6_consequence_and_verdict.py"
SOURCE_SHA256 = "e09822946b9b44ade21632c7db42d2061e493b112a13fab9a44e74a6a6d18b17"
BASE_RELEASE_SHA256 = "85d66810ecf5472f4bb7e0d9d6c3d90f811362c76fd94882631db39f72db1f7c"
FORMULA_FREEZE_SHA256 = "71f866af076d2bdcfe1bdd200db3b88da8ba0b7234b54e2463aec1d51a4fab4e"
CLAIM_DELTA_SHA256 = "5a65a3c5fc8631e760fe7fe2d026e9f2163ab995c1c1794957e8650cb9d5706c"
CLAIM_REVISION_SHA256 = "e5b805faf2c68bc2f8e7aec50247f68f8ee836ae851f8afa277fe3d6f1b1f50b"
TRANSITIVE = {
    "WM7": (
        SOURCE_ROOT / "merged-framework/bridges/phase-39/bridge_WM7_induction_trace_field_content.py",
        "a124346ed81c93b36f181f7e0fb1cd2d07387d3578ece17a6fe6c6a0f379a361",
    ),
    "WM1": (
        SOURCE_ROOT / "merged-framework/bridges/phase-23/bridge_WM1_sin2thetaw_trace_ratio.py",
        "75dc34e168c39cd0af0a21cd4c7d039088ac74baefb6615ece98f5069f5b8953",
    ),
    "SM2": (
        SOURCE_ROOT / "merged-framework/bridges/phase-9/bridge_SM2_generation_hypercharge_charges.py",
        "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1",
    ),
    "SM4": (
        SOURCE_ROOT / "merged-framework/bridges/phase-9/bridge_SM4_coupling_running_unification.py",
        "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac",
    ),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"expected mapping in {path}")
    return data


def zero_matrix(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(sp.expand_complex(entry)) == 0 for entry in matrix)


def finite_box_coupling_evidence(
    spacing: float,
    sample_count: int,
) -> tuple[float, float, float]:
    """Recompute GC6's finite-box matrices with both basis conventions."""

    omega = 0.45
    kappa = float(np.sqrt(0.5 - omega**2))
    amplitude = 2.0 * np.sqrt(6.0) * kappa
    phases = (0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0)
    anchors = (0.0, spacing, 2.0 * spacing)
    grid = np.linspace(-8.0, 2.0 * spacing + 8.0, sample_count)
    step = float(grid[1] - grid[0])
    modes: list[np.ndarray] = []
    for center in anchors:
        potential = -12.0 / np.cosh((grid - center) / 0.7) ** 2
        _, vectors = eigh_tridiagonal(
            2.0 / step**2 + potential[1:-1],
            -np.ones(sample_count - 3) / step**2,
            select="i",
            select_range=(0, 0),
        )
        mode = vectors[:, 0]
        modes.append(mode / np.sqrt(np.sum(mode**2) * step))
    interior = grid[1:-1]
    couplings: list[np.ndarray] = []
    for profile_center in (-1.0, 0.0, 1.0):
        profile = amplitude / np.cosh(kappa * (interior - profile_center))
        couplings.append(
            np.asarray(
                [
                    [
                        float(np.sum(modes[a] * modes[b] * profile) * step)
                        for b in range(3)
                    ]
                    for a in range(3)
                ]
            )
        )
    mass = sum(
        np.exp(1j * phase) * coupling
        for phase, coupling in zip(phases, couplings, strict=True)
    )
    left, singular_values, right_adjoint = np.linalg.svd(mass)
    right = right_adjoint.conj().T

    def worst(use_right_basis: bool) -> float:
        ratios = []
        for coupling in couplings:
            transformed = left.conj().T @ coupling @ (
                right if use_right_basis else left
            )
            off_diagonal = max(
                abs(transformed[a, b])
                for a in range(3)
                for b in range(3)
                if a != b
            )
            diagonal = max(abs(transformed[a, a]) for a in range(3))
            ratios.append(float(off_diagonal / diagonal))
        return max(ratios)

    return (
        float(singular_values[0] / singular_values[-1]),
        worst(False),
        worst(True),
    )


def main() -> int:
    checks = CheckLedger("P213-GC6-FCNC-CONSEQUENCE-AUDIT")
    checks.check("source hash remains pinned", digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        digest(ROOT / "governance/releases/v0.154.0.yaml") == BASE_RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        digest(CAMPAIGN / "evidence/formula-freeze.yaml") == FORMULA_FREEZE_SHA256,
    )
    checks.check(
        "post-source claim delta remains pinned",
        digest(CAMPAIGN / "evidence/post-source-claim-delta.yaml")
        == CLAIM_DELTA_SHA256,
    )
    checks.check(
        "alignment edge-condition revision remains pinned",
        digest(CAMPAIGN / "evidence/claim-delta-revision-0003.yaml")
        == CLAIM_REVISION_SHA256,
    )
    proposal = load(CAMPAIGN / "proposal.yaml")
    checks.check(
        "proposal reserves only the novel biunitary surface",
        proposal["claims_proposed"] == ["C-MIX-004"]
        and proposal["revision"] == 3,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "source inventory remains six checks and one assertion",
        len(source_checks) == 6
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    checks.check(
        "source literal and dynamic call split remains exact",
        sum(
            bool(node.args)
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
            for node in source_checks
        )
        == 2,
    )
    checks.check(
        "source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references
        == compatibility.current_references
        == compatibility.eager_legacy_default_fallbacks
        == 0,
    )
    for label, (path, expected_hash) in TRANSITIVE.items():
        audit = audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        checks.check(f"{label} transitive hash remains pinned", digest(path) == expected_hash)
        checks.check(
            f"{label} transitive compatibility surface remains empty",
            audit.legacy_references
            == audit.current_references
            == audit.eager_legacy_default_fallbacks
            == 0,
        )

    a = sp.symbols("a", nonzero=True)
    first = sp.Matrix([[1, a], [a, 2]])
    second = sp.Matrix([[0, -a], [-a, 1]])
    cancellation = multi_scalar_mass_basis_ledger(
        (first, second), (1, 1), sp.eye(2), sp.eye(2)
    )
    checks.check(
        "individual off-diagonal couplings can cancel in a diagonal mass sum",
        cancellation.diagonal_mass_matrix == sp.diag(1, 3)
        and not cancellation.all_couplings_diagonal
        and zero_matrix(
            cancellation.off_diagonal_couplings[0]
            + cancellation.off_diagonal_couplings[1]
        ),
    )
    checks.check(
        "mass-basis reconstruction is an exact derived identity",
        cancellation.reconstructed_diagonal_mass_matrix
        == cancellation.diagonal_mass_matrix
        and zero_matrix(cancellation.reconstruction_residual),
    )

    def cancellation_predicate(weights: object) -> bool:
        try:
            result = multi_scalar_mass_basis_ledger(
                (first, second), weights, sp.eye(2), sp.eye(2)  # type: ignore[arg-type]
            )
        except ValueError:
            return False
        return result.diagonal_mass_matrix == sp.diag(1, 3)

    checks.mutation_sensitive(
        "off-diagonal cancellation weights are load bearing",
        cancellation_predicate,
        (1, 1),
        ((1, 2), (2, 1), (1, -1)),
    )

    reference = sp.diag(2, 5, 11)
    aligned = multi_scalar_mass_basis_ledger(
        (reference, -3 * reference, 7 * reference),
        (2, 1, -1),
        sp.eye(3),
        sp.eye(3),
    )
    checks.check(
        "common matrix alignment is sufficient for diagonal couplings",
        aligned.all_couplings_diagonal and aligned.mass_matrix == -8 * reference,
    )
    zero_alignment_reference = sp.Matrix([[0, 1], [1, 0]])
    zero_alignment = multi_scalar_mass_basis_ledger(
        (zero_alignment_reference, -zero_alignment_reference),
        (1, 1),
        sp.eye(2),
        sp.eye(2),
    )
    checks.check(
        "zero combined alignment coefficient does not force diagonality",
        zero_alignment.mass_matrix == sp.zeros(2)
        and not zero_alignment.all_couplings_diagonal,
    )
    misaligned = multi_scalar_mass_basis_ledger(
        (sp.diag(1, 3), sp.Matrix([[0, 1], [1, 0]])),
        (1, 0),
        sp.eye(2),
        sp.eye(2),
    )
    checks.check(
        "an inert weight can hide a flavor-changing individual coupling",
        misaligned.diagonal_mass_matrix == sp.diag(1, 3)
        and not misaligned.all_couplings_diagonal,
    )

    unitary = sp.Matrix([[1, sp.I], [sp.I, 1]]) / sp.sqrt(2)
    takagi_sources = (
        sp.diag(-sp.Rational(1, 2), sp.Rational(1, 2)),
        sp.Matrix([[0, sp.Rational(3, 2)], [sp.Rational(3, 2), 0]]),
    )
    takagi = takagi_multi_scalar_mass_basis_ledger(
        takagi_sources, (1, sp.I), unitary
    )
    wrong_couplings = tuple(
        sp.simplify(unitary.adjoint() * matrix * unitary)
        for matrix in takagi_sources
    )
    checks.check(
        "Takagi right basis is the conjugate basis",
        takagi.right_basis == unitary.conjugate()
        and takagi.diagonal_mass_matrix == sp.diag(1, 2),
    )
    checks.check(
        "source-style reuse of the left basis manufactures off-diagonal entries",
        takagi.all_couplings_diagonal
        and any(not zero_matrix(off_diagonal_part(matrix)) for matrix in wrong_couplings),
    )

    projectors = (sp.diag(1, 0), sp.diag(0, 1))
    identity_basis = multi_scalar_mass_basis_ledger(
        projectors, (1, 1), sp.eye(2), sp.eye(2)
    )
    rotation = sp.Matrix([[1, 1], [-1, 1]]) / sp.sqrt(2)
    rotated_basis = multi_scalar_mass_basis_ledger(
        projectors, (1, 1), rotation, rotation
    )
    checks.check(
        "degenerate mass blocks retain load-bearing basis freedom",
        identity_basis.diagonal_mass_matrix == rotated_basis.diagonal_mass_matrix
        == sp.eye(2)
        and identity_basis.all_couplings_diagonal
        and not rotated_basis.all_couplings_diagonal,
    )

    n_gen, n_h = sp.symbols("n_gen n_h", positive=True, integer=True)
    s1 = 4 * n_gen / 3 + n_h / 10
    s2 = 4 * n_gen / 3 + n_h / 6
    boundary = sp.factor(s2 / (s2 + sp.Rational(5, 3) * s1))
    expected_boundary = 3 * (8 * n_gen + n_h) / (2 * (32 * n_gen + 3 * n_h))
    checks.check(
        "WM7 supplied-table boundary family is exact",
        sp.simplify(boundary - expected_boundary) == 0,
    )
    checks.check(
        "source count specializations reproduce conditionally",
        boundary.subs({n_gen: 3, n_h: 0}) == sp.Rational(3, 8)
        and boundary.subs({n_gen: 3, n_h: 1}) == sp.Rational(25, 66)
        and boundary.subs({n_gen: 3, n_h: 3}) == sp.Rational(27, 70),
    )
    checks.check(
        "boundary monotonicity is a conditional algebraic property",
        sp.factor(sp.diff(boundary, n_h))
        == 12 * n_gen / (32 * n_gen + 3 * n_h) ** 2,
    )

    selected = [finite_box_coupling_evidence(d, 16000) for d in (3.0, 4.0, 5.0, 6.0)]
    expected_source = (
        0.01228574836029285,
        0.0018281380978665298,
        0.0010061654214178855,
        0.00001660336961380689,
    )
    checks.check(
        "finite-box route reproduces every source left-basis ratio",
        max(abs(row[1] - expected) for row, expected in zip(selected, expected_source))
        < 2e-10,
    )
    checks.check(
        "correct biunitary route differs from the source transform",
        all(abs(row[2] - row[1]) > 1e-8 * max(row[2], row[1]) for row in selected),
    )
    refined = finite_box_coupling_evidence(6.0, 32000)
    checks.check(
        "correct d-six ratio is grid-refined",
        abs(refined[2] - selected[-1][2]) / refined[2] < 5e-6,
    )
    dense_witness = [
        finite_box_coupling_evidence(d, 6000)[2] for d in (4.75, 5.0, 5.25)
    ]
    checks.check(
        "denser spacing witness refutes monotone FCNC decrease",
        dense_witness[0] < dense_witness[1] < dense_witness[2],
    )
    checks.check(
        "source thresholds remain declared rather than derived",
        proposal["opened_source_parameters"]["convergence_relative_threshold"] == 0.5
        and proposal["opened_source_parameters"]["hierarchy_threshold"] == 10.0
        and proposal["opened_source_parameters"]["final_ratio_threshold"] == 0.0001,
    )

    registry = load(ROOT / "governance/claims.yaml")
    statements = {claim["id"]: claim["statement"] for claim in registry["claims"]}
    checks.check(
        "accepted overlap authority keeps geometry and physical maps conditional",
        "d is a free input" in statements["C-OVL-002"]
        and "physical mass or hierarchy" in statements["C-OVL-005"],
    )
    checks.check(
        "accepted gauge authority preserves Yukawa and field-content omissions",
        "same-order Yukawa contribution" in statements["C-RGE-005"]
        and "field-content or anomaly derivation" in statements["C-RGE-005"],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
