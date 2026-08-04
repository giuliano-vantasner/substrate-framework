#!/usr/bin/env python3
"""Exact, source-aware verifier for proposed C-REP-002 and W2."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.boundary_correlations import (
    boundary_sign_correlation_density,
    right_half_line_topological_charge_change,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su2_doublets import (
    su2_chiral_factor_ledger,
    su2_common_charge_ledger,
    su2_fundamental_ledger,
    su2_same_carrier_projector_ledger,
)
from substrate_framework.symmetric_spin import symmetric_spin_rung
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P147-w2-su2-doublet-audit"
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / (
    "merged-framework/bridges/phase-6/bridge_W2_su2L_chiral_doublet.py"
)
DOSSIER = SOURCE_ROOT / "merged-framework/bridges/phase-6/dossiers/W2_dossier.md"
LEAN = SOURCE_ROOT / "sg-breather-ionization/dynamics_lean/ChargeDiscrimination.lean"
SOLUTION = SOURCE_ROOT / "sg-breather-ionization/solution.md"
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
HASHES = {
    SOURCE: "0babbe7b46b058a6e19a25a598a65bc2ae48189ff21a428d09c3ceae3f42ad16",
    DOSSIER: "bd870f2e85b9d7f4d546c8fdd304fd94fc4b9e196c64cb8b7b16c798559064b4",
    LEAN: "c692eb12d9aa81f7547f855fe24ed03f7ba2403ac3fc4710c33c42ff80364056",
    SOLUTION: "a5a0ced9a097f07daea67e37b9516755307536e4850dfc975da72ee8eb876f86",
    FROZEN: "4a0016be9650016d96c6e504ccdc2798889ff95ac54866247aed191e273618b2",
    REVISION: "32dd8556161fabd390066e49291d190e65b3b0a987f5dd3cbeb71cf56445cb58",
    REPRODUCTION: "76563b91e892f57bc4dc50d6c35d0e0c31bddbc55d7fae47fb3e2f93cd3709b8",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _all_zero(matrices: tuple[sp.ImmutableMatrix, ...]) -> bool:
    return all(matrix == sp.zeros(*matrix.shape) for matrix in matrices)


def run() -> int:
    checks = CheckLedger("P147/C-REP-002")
    for path, digest in HASHES.items():
        checks.check(f"pinned {path.name} hash", _sha256(path) == digest)

    source_text = SOURCE.read_text(encoding="utf-8")
    dossier_text = DOSSIER.read_text(encoding="utf-8")
    lean_text = LEAN.read_text(encoding="utf-8")
    solution_text = SOLUTION.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [
        node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)
    ]
    checks.check("nine source predicates", len(source_checks) == 9)
    checks.check("one source assertion", len(source_assertions) == 1)
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "W2 has no NumPy integration compatibility event",
        compatibility.numpy_aliases == ()
        and compatibility.legacy_references == 0
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
    checks.check("native W2 process exits cleanly", native.returncode == 0)
    checks.check(
        "native W2 terminal tally is exact",
        native.stdout.rstrip().endswith("ALL 9 CHECKS PASS"),
    )

    fundamental = su2_fundamental_ledger()
    checks.check(
        "standard generators are Hermitian traceless and nonzero",
        all(generator == generator.H for generator in fundamental.generators)
        and all(sp.trace(generator) == 0 for generator in fundamental.generators)
        and all(generator != sp.zeros(2) for generator in fundamental.generators),
    )
    checks.check(
        "standard Pauli-half generators close su2 exactly",
        _all_zero(fundamental.commutator_residuals),
    )
    checks.check(
        "standard fundamental Casimir is three quarters",
        fundamental.casimir == sp.Rational(3, 4) * sp.eye(2),
    )
    checks.check(
        "full fundamental commutant is scalar",
        fundamental.commutant_basis == (sp.eye(2),),
    )

    bottom = sp.ImmutableMatrix([0, 1])
    top = sp.ImmutableMatrix([1, 0])
    accepted_rung = symmetric_spin_rung(1, 0)
    checks.check(
        "W2 ladder is the accepted C-SPN-002 N-one specialization",
        fundamental.raising_operator * bottom
        == accepted_rung.raising_coefficient * top
        and fundamental.lowering_operator * top
        == accepted_rung.raising_coefficient * bottom,
    )
    checks.check(
        "basis vector names do not enter the matrix construction",
        "kink = sp.Matrix([1, 0])" in source_text
        and "antikink = sp.Matrix([0, 1])" in source_text
        and all("kink" not in str(entry) for matrix in fundamental.generators for entry in matrix),
    )

    declared_label_difference = sp.Integer(1) - sp.Integer(-1)
    checks.check(
        "declared W2 label transition changes topological label by two",
        declared_label_difference == 2
        and "dQ_event = Q_kink - Q_antikink" in source_text,
    )
    checks.check(
        "W2 check three inserts a different per-event unit",
        "dQ_per_event = sp.Integer(1)" in source_text
        and declared_label_difference != 1,
    )
    q = sp.Symbol("q", real=True)
    checks.check(
        "opposite-sign label pairing does not fix its magnitude",
        sp.simplify(q - (-(-q))) == 0
        and sp.solve(sp.Eq(sp.Rational(1, 2), q / 2), q) == [1],
    )
    checks.check(
        "T3 equals Q over two is a supplied label calibration",
        "t3_is_Q_over_2" in source_text
        and "Q_kink = sp.Integer(1)" in source_text
        and "Q_antikink = sp.Integer(-1)" in source_text,
    )

    common_charge = su2_common_charge_ledger(0, assigned_labels=(1, -1))
    checks.check(
        "one common Abelian doublet charge has unit separation",
        common_charge.eigenvalue_separation == 1
        and _all_zero(common_charge.commutator_residuals),
    )
    checks.check(
        "W2 plus-minus-one labels are incompatible with one common charge",
        common_charge.assigned_label_residuals
        == (sp.Rational(1, 2), sp.Rational(-1, 2))
        and common_charge.labels_compatible is False,
    )
    checks.check(
        "W2 source corrects the dossier's zero-hypercharge sentence",
        "Y_kink == Q_kink and Y_antikink == Q_antikink" in source_text
        and "Y = 2(Q − T₃) = 0 for both" in dossier_text,
    )

    projector = sp.diag(1, 0)
    chirality_sign = sp.diag(1, -1)
    same_carrier = su2_same_carrier_projector_ledger(projector)
    checks.check(
        "W2 chirality sign reuses twice T3 on the same carrier",
        chirality_sign - 2 * sp.Matrix(fundamental.generators[2]) == sp.zeros(2)
        and projector == (sp.eye(2) + chirality_sign) / 2
        and "eps_x = sp.Matrix([[1, 0], [0, -1]])" in source_text,
    )
    checks.check(
        "same-carrier rank-one projector is outside the commutant",
        same_carrier.projector_rank == 1
        and not same_carrier.projector_in_fundamental_commutant,
    )
    checks.check(
        "same-carrier W2 generators fail Hermiticity",
        sum(
            residual != sp.zeros(2)
            for residual in same_carrier.hermiticity_residuals
        )
        == 2,
    )
    checks.check(
        "same-carrier W2 generators fail all su2 commutators",
        all(
            residual != sp.zeros(2)
            for residual in same_carrier.commutator_residuals
        ),
    )

    exchange = sp.ImmutableMatrix([[0, 1], [1, 0]])
    factored = su2_chiral_factor_ledger(
        projector,
        parity_exchange=exchange,
    )
    checks.check(
        "independent-factor left generators are Hermitian and close",
        _all_zero(factored.left_hermiticity_residuals)
        and _all_zero(factored.left_commutator_residuals),
    )
    checks.check(
        "independent-factor right generators are Hermitian and close",
        _all_zero(factored.right_hermiticity_residuals)
        and _all_zero(factored.right_commutator_residuals),
    )
    checks.check(
        "left factor annihilates the independent right subspace",
        all(
            generator
            * sp.kronecker_product(sp.eye(2), sp.ImmutableMatrix([0, 1]))
            == sp.zeros(4, 2)
            for generator in factored.left_generators
        ),
    )
    checks.check(
        "declared parity exchanges left and right factors",
        _all_zero(factored.parity_left_to_right_residuals or ()),
    )
    checks.check(
        "vector is parity even and axial is parity odd",
        _all_zero(factored.parity_vector_even_residuals or ())
        and _all_zero(factored.parity_axial_odd_residuals or ()),
    )
    checks.check(
        "left operator alone is exchanged rather than parity odd",
        all(
            right != -left
            for left, right in zip(
                factored.left_generators,
                factored.right_generators,
                strict=True,
            )
        ),
    )

    checks.check(
        "W2 guard preloads its desired Boolean and substitutes its image",
        "guard_fires = True" in source_text
        and "G_left_parity = Ta * PR" in source_text
        and "maps_to_right = is_zero_mat(G_left_parity - Ta * PR)" in source_text,
    )
    checks.check(
        "W2 never evaluates its cited correlation or boundary evolution",
        "boundary_sign_correlation_density" not in source_text
        and "solve_ivp" not in source_text
        and "solve_bvp" not in source_text,
    )
    checks.check(
        "correlation remains independent of topological transfer",
        boundary_sign_correlation_density(1, 3) == 3
        and right_half_line_topological_charge_change(0) == 0,
    )

    checks.check(
        "imported Lean drive selection is a definition by sign",
        "if F₀ < 0 then reflectedCharge_cplus else reflectedCharge_cminus"
        in lean_text,
    )
    checks.check(
        "imported fermion parity is declared integer arithmetic",
        "def fermionParity (Q : ℤ) : ℤ := (-1 : ℤ) ^ Q.natAbs" in lean_text
        and "unfold fermionParity reflectedCharge_cplus reflectedCharge_cminus"
        in lean_text,
    )
    checks.check(
        "solution marks chiral and rectification claims as analysis",
        "| Chiral boundary condition derivation | `theoretical_analysis` |"
        in solution_text
        and "| Topological rectification condition | `theoretical_analysis` |"
        in solution_text,
    )
    checks.check(
        "solution's printed chiral spatial signs contradict its coordinates",
        "φ(x,t) = φ_L(t+x) + φ_R(t−x)" in solution_text
        and "φ_x(0,t) = −φ_L'(t) + φ_R'(t)" in solution_text,
    )

    loaded_names = {
        node.id
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    checks.check(
        "W2 loads no gauge or Lorentz-spinor dynamics",
        not loaded_names.intersection(
            {
                "W_mu",
                "gamma5",
                "lagrangian",
                "action",
                "field_strength",
                "covariant_derivative",
                "current",
            }
        ),
    )
    checks.check(
        "W2 ceiling verdict is a hard-coded negative inventory",
        "gauge_field_built = False" in source_text,
    )

    doubled = tuple(2 * generator for generator in fundamental.generators)
    checks.check(
        "generator-scale mutation breaks the frozen su2 normalization",
        any(
            residual != sp.zeros(2)
            for residual in (
                doubled[0] * doubled[1]
                - doubled[1] * doubled[0]
                - sp.I * doubled[2],
                doubled[1] * doubled[2]
                - doubled[2] * doubled[1]
                - sp.I * doubled[0],
            )
        ),
    )
    wrong_labels = su2_common_charge_ledger(
        0,
        assigned_labels=(sp.Rational(1, 2), sp.Rational(1, 2)),
    )
    checks.check(
        "lower-label sign mutation breaks common-charge compatibility",
        wrong_labels.labels_compatible is False,
    )
    try:
        su2_chiral_factor_ledger(projector, parity_exchange=sp.eye(2))
    except ValueError as error:
        parity_mutation_detected = "exchange the projectors" in str(error)
    else:
        parity_mutation_detected = False
    checks.check(
        "nonexchanging parity mutation is rejected",
        parity_mutation_detected,
    )
    try:
        su2_chiral_factor_ledger(sp.diag(1, sp.Rational(1, 2)))
    except ValueError as error:
        projector_mutation_detected = "idempotent" in str(error)
    else:
        projector_mutation_detected = False
    checks.check(
        "nonprojector mutation is rejected",
        projector_mutation_detected,
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/su2_doublets.py"
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P147 and canonical code has no legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P147 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
