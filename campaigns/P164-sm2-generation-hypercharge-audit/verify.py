#!/usr/bin/env python3
"""Exact source-aware verifier for the SM2 multiplet-charge claim delta."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.gauge_scalar_mass import su2_u1_lower_doublet_mass_evidence
from substrate_framework.multiplet_charges import (
    ChargeMultiplet,
    charge_conjugate_multiplet,
    finite_multiplet_charge_ledger,
    infer_common_abelian_charge,
    multiplet_abelian_normalization_ledger,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P164-sm2-generation-hypercharge-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-9/"
    "bridge_SM2_generation_hypercharge_charges.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
CHECK_ADJUDICATION = CAMPAIGN / "evidence/check-adjudication.yaml"
SOURCE_SHA256 = "cc5532e86128f010f6801dada96ae1ece5a6be845817127d69cf72810b9e33f1"
FROZEN_SHA256 = "e36796fdf7372b0057b94b96e761632f91275d41a3e876d4cad32a2c48f3405d"
REVISION_SHA256 = "d68eaf162bb3388e479836cd5ae4c9449676c3e951d8ac47e72c3965922a1ee0"
REPRODUCTION_SHA256 = "834e523c46669a3ff2eae4c318becfcdfacb2aa8277bd6234d36abed214eb3e4"
SOURCE_AUDIT_SHA256 = "309c8adbffecea387cae900c7e401d8b528df47c3067b079a3f2f7b5aca12fbd"
CHECK_ADJUDICATION_SHA256 = (
    "7c30aa4da0081bbbfa2f2d54bb1cb8f152378f39cc23691f9315f8c4a7a44a6c"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _supplied_table() -> tuple[ChargeMultiplet, ...]:
    half = sp.Rational(1, 2)
    return (
        ChargeMultiplet("Q_L", 3, (half, -half), sp.Rational(1, 6)),
        ChargeMultiplet("u_R", 3, (0,), sp.Rational(2, 3)),
        ChargeMultiplet("d_R", 3, (0,), -sp.Rational(1, 3)),
        ChargeMultiplet("L", 1, (half, -half), -half),
        ChargeMultiplet("e_R", 1, (0,), -1),
    )


def run() -> int:
    checks = CheckLedger("P164/SM2")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned SM2 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("normalized frozen proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
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
    checks.check("seven source predicate sites", len(source_checks) == 7)
    checks.check("one source assertion node", len(source_assertions) == 1)
    checks.check(
        "SM2 has no NumPy integration compatibility surface",
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
    checks.check("native SM2 exits cleanly", native.returncode == 0)
    checks.check(
        "native SM2 terminal tally is exact",
        native_lines.count("ALL 7 CHECKS PASS") == 1,
    )

    table = _supplied_table()
    ledger = finite_multiplet_charge_ledger(table)
    expected_spectra = (
        (sp.Rational(2, 3), -sp.Rational(1, 3)),
        (sp.Rational(2, 3),),
        (-sp.Rational(1, 3),),
        (0, -1),
        (-1,),
    )
    checks.check(
        "canonical ledger derives every supplied multiplet spectrum",
        tuple(spectrum.electric_charges for spectrum in ledger.spectra)
        == expected_spectra,
    )
    checks.check(
        "spectator multiplicities give exactly the supplied fifteen-state count",
        ledger.state_count == ledger.trace_ledger.state_count == 15
        and tuple(spectrum.state_count for spectrum in ledger.spectra)
        == (6, 3, 3, 2, 1),
    )
    trace = ledger.trace_ledger
    checks.check(
        "multiplet expansion composes the accepted charge trace ledger",
        trace.trace_t3_squared == 2
        and trace.trace_abelian_squared == sp.Rational(10, 3)
        and trace.trace_cross == 0
        and trace.trace_electric_squared == sp.Rational(16, 3)
        and trace.trace_ratio == sp.Rational(3, 8)
        and trace.decomposition_residual == 0,
    )

    inversions = tuple(
        infer_common_abelian_charge(
            multiplet.t3_weights,
            spectrum.electric_charges,
        )
        for multiplet, spectrum in zip(table, ledger.spectra, strict=True)
    )
    checks.check(
        "each supplied target spectrum uniquely reconstructs its row value",
        all(inversion.consistent for inversion in inversions)
        and tuple(inversion.candidate_abelian_charge for inversion in inversions)
        == tuple(multiplet.abelian_charge for multiplet in table),
    )
    inconsistent = infer_common_abelian_charge(
        (sp.Rational(1, 2), -sp.Rational(1, 2)),
        (sp.Rational(2, 3), sp.Rational(2, 3)),
    )
    checks.check(
        "inconsistent target separation fails the common-row inversion",
        not inconsistent.consistent and inconsistent.residuals[1] != 0,
    )
    checks.check(
        "SM2 supplies both the targets and the reconstructed row values",
        "# PS weak hypercharges Y_PS (IMPORTED standard SM)" in source_text
        and "# Observed electric charges (the target the reps must reproduce)" in source_text,
    )

    bad_weight = sp.Rational(1, 2)
    bad_up = sp.Rational(1, 2) + bad_weight
    checks.check(
        "source bad-row guard is a load-bearing local inversion counterexample",
        bad_up == 1
        and bad_up != sp.Rational(2, 3)
        and "Y_QL_bad = R(1, 2)" in source_text,
    )
    alternative = infer_common_abelian_charge(
        (sp.Rational(1, 2), -sp.Rational(1, 2)),
        (sp.Rational(3, 2), sp.Rational(1, 2)),
    )
    checks.check(
        "alternative supplied targets select an equally exact alternative row",
        alternative.consistent
        and alternative.candidate_abelian_charge == 1
        and alternative.residuals == (0, 0),
    )
    without_electron = finite_multiplet_charge_ledger(table[:-1])
    with_neutral_singlet = finite_multiplet_charge_ledger(
        table + (ChargeMultiplet("neutral_R", 1, (0,), 0),)
    )
    checks.check(
        "fifteen is a supplied table count rather than completeness",
        without_electron.state_count == 14
        and with_neutral_singlet.state_count == 16
        and with_neutral_singlet.spectra[-1].electric_charges == (0,),
    )

    u_conjugate = charge_conjugate_multiplet(table[1], label="u_R_conj")
    q_conjugate = charge_conjugate_multiplet(table[0], label="Q_L_conj")
    conjugates = finite_multiplet_charge_ledger((u_conjugate, q_conjugate))
    checks.check(
        "charge conjugation negates weights row values and spectra",
        u_conjugate.abelian_charge == -sp.Rational(2, 3)
        and conjugates.spectra[0].electric_charges == (-sp.Rational(2, 3),)
        and conjugates.spectra[1].electric_charges
        == (-sp.Rational(2, 3), sp.Rational(1, 3)),
    )
    checks.check(
        "equal spectator dimension does not type triplet versus antitriplet",
        u_conjugate.spectator_multiplicity == table[1].spectator_multiplicity == 3
        and "(name, SU(3) dim, SU(2) dim" in source_text
        and "antitriplet" not in source_text.lower(),
    )

    y_ql = sp.Rational(1, 6)
    y_h = sp.Rational(1, 2)
    y_ur = sp.Rational(2, 3)
    y_dr = -sp.Rational(1, 3)
    y_l = -sp.Rational(1, 2)
    y_er = sp.Integer(-1)
    correct_yukawa_residuals = (
        sp.simplify(-y_ql - y_h + y_ur),
        sp.simplify(-y_ql + y_h + y_dr),
        sp.simplify(-y_l + y_h + y_er),
    )
    naive_up_sum = sp.simplify(y_ql + y_h + y_ur)
    checks.check(
        "properly conjugated supplied Yukawa rows are neutral",
        correct_yukawa_residuals == (0, 0, 0),
    )
    checks.check(
        "source prose shorthand is not its own Yukawa-neutrality oracle",
        naive_up_sum == sp.Rational(4, 3)
        and "Q_L.H.f_R would not be gauge-invariant" in source_text
        and "correct_yukawa_residuals" not in source_text,
    )

    higgs = su2_u1_lower_doublet_mass_evidence(1, 1, 1)
    checks.check(
        "accepted M1 composition supplies only the conditional neutral lower direction",
        higgs.charge_operator == sp.diag(1, 0)
        and higgs.charge_vacuum_residual == sp.zeros(2, 1),
    )
    alternative_diagonal = sp.diag(
        sp.Rational(1, 2) + 1,
        -sp.Rational(1, 2) + 1,
    )
    checks.check(
        "diagonality alone does not select the supplied electric spectrum",
        alternative_diagonal.is_diagonal()
        and alternative_diagonal != sp.diag(sp.Rational(2, 3), -sp.Rational(1, 3)),
    )

    coupling = sp.Symbol("g_Y", positive=True)
    normalization = multiplet_abelian_normalization_ledger(table, 2, coupling)
    checks.check(
        "factor-two generator and electric-coefficient map preserves every charge",
        normalization.rescaled_electric_coefficient == sp.Rational(1, 2)
        and normalization.rescaled_multiplets[0].abelian_charge == sp.Rational(1, 3)
        and all(
            residual == 0
            for row in normalization.charge_residuals
            for residual in row
        ),
    )
    checks.check(
        "full local normalization map also rescales the Abelian coupling inversely",
        normalization.rescaled_abelian_coupling == coupling / 2
        and normalization.flattened_normalization.coupled_trace_norm_residual == 0
        and all(
            residual == 0
            for residual in normalization.flattened_normalization.charge_product_residuals
        ),
    )
    checks.check(
        "holding the electric coefficient fixed breaks the convention map",
        normalization.fixed_coefficient.spectra[0].electric_charges
        != ledger.spectra[0].electric_charges,
    )
    checks.check(
        "SM2 checks charge coordinates but omits coupling and global normalization",
        "Y_PS = Y_M1 / 2" in source_text
        and "g_Y" not in source_text
        and "period" not in source_text.lower()
        and "charge lattice" not in source_text.lower(),
    )

    loaded_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    checks.check(
        "SM2 constructs no matter dynamics conservation law or anomaly equations",
        "action" not in loaded_names
        and "hamiltonian" not in loaded_names
        and "anomaly" not in loaded_names
        and "current" not in loaded_names,
    )
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in CAMPAIGN.rglob("*.py")
    ]
    checks.check(
        "mutable P164 has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )
    checks.check(
        "mutable P164 has no eager legacy fallback",
        all(item.eager_legacy_default_fallbacks == 0 for item in mutable_compatibility),
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P164 PRIMARY ALL {result} CHECKS PASS")
