#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-HOL-001 and NA1."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.nonabelian_holonomy import (
    endpoint_gauge_holonomy_evidence,
    ordered_segment_holonomy,
    su2_holonomy_evidence,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P156-na1-nonabelian-holonomy-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-7/"
    "bridge_NA1_su2L_wilson_loop.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
SOURCE_SHA256 = "c36b2eeace179a95b44400ea42b74f6263671fd4b4a8441fc682c480bc9372c8"
FROZEN_SHA256 = "73dc2c3f3a191dd4819cc896f52b74d09a54f9950fd6b405a92be42771ab5e20"
REVISION_SHA256 = "0f341a4c23fd74e22009e694481d322a3f22524d41249d90ec6c5b6aad815217"
REPRODUCTION_SHA256 = "b8afd6f59b5969b456cf2bf0980af655a9e4b839093ba17fc5c229d3f0293eca"
SOURCE_AUDIT_SHA256 = "1e49a137af832bca71409297eb9e68bf4725aad05ed6afd114dc79ca8a169bf7"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    checks = CheckLedger("P156/C-HOL-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned NA1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check("source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256)
    checks.check("source audit hash", _sha256(SOURCE_AUDIT) == SOURCE_AUDIT_SHA256)
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("five source predicates", len(source_checks) == 5)
    checks.check(
        "one source assertion",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "NA1 has no numerical integration compatibility surface",
        compatibility.numpy_aliases == ()
        and compatibility.legacy_references == 0
        and compatibility.current_references == 0,
    )
    checks.check(
        "source cross-object verdict uses assigned scalar values",
        "wilson_eig = sp.Integer(-1)" in source_text
        and "chi_F_g = sp.Integer(-1)" in source_text
        and "len({wilson_eig, pulson, lean_kink, chi_F_g}) == 1" in source_text,
    )

    sigma_1 = sp.ImmutableMatrix([[0, 1], [1, 0]])
    sigma_2 = sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]])
    sigma_3 = sp.ImmutableMatrix([[1, 0], [0, -1]])
    t_1, t_2, t_3 = sigma_1 / 2, sigma_2 / 2, sigma_3 / 2
    forward = ordered_segment_holonomy((sp.pi * t_1, sp.pi * t_2))
    swapped = ordered_segment_holonomy((sp.pi * t_2, sp.pi * t_1))
    checks.check(
        "chronological transport places the later segment on the left",
        forward.transporter == sp.I * sigma_3
        and swapped.transporter == -sp.I * sigma_3,
    )
    checks.check(
        "ordered transport is unitary with the determinant trace formula",
        forward.unitary_certified
        and forward.determinant == 1
        and forward.determinant_certified,
    )
    checks.check(
        "path reversal and concatenation close exactly",
        forward.reverse_certified and forward.composition_certified,
    )
    checks.check(
        "cyclic basepoint move conjugates rather than fixing the matrix",
        forward.cyclic_basepoint_certified
        and forward.cyclic_shifted_transporter == swapped.transporter
        and forward.cyclic_shifted_transporter != forward.transporter,
    )
    checks.check(
        "trace alone is insensitive to this noncommuting order swap",
        forward.trace == swapped.trace == 0
        and forward.transporter != swapped.transporter,
    )

    alpha, beta = sp.symbols("alpha beta", real=True)
    commuting = ordered_segment_holonomy((alpha * t_3, beta * t_3))
    checks.check(
        "pairwise commuting segments collapse to the exponential of the sum",
        commuting.pairwise_commuting
        and commuting.commuting_collapse_residual == sp.zeros(2),
    )

    open_gauges = (sp.I * sigma_3, sp.I * sigma_1, sp.I * sigma_2)
    open_covariance = endpoint_gauge_holonomy_evidence(
        forward.segment_transporters,
        open_gauges,
    )
    checks.check(
        "open transport transforms by both endpoint factors",
        open_covariance.endpoint_covariance_certified
        and open_covariance.transformed_transporter
        == open_gauges[-1] * forward.transporter * open_gauges[0].H,
    )
    wrong_open_prediction = sp.simplify(
        open_gauges[-1] * forward.transporter
    )
    checks.check(
        "dropping the initial endpoint factor breaks open covariance",
        open_covariance.transformed_transporter != wrong_open_prediction,
    )

    closed_gauges = (sp.I * sigma_1, sp.I * sigma_3, sp.I * sigma_1)
    closed_covariance = endpoint_gauge_holonomy_evidence(
        forward.segment_transporters,
        closed_gauges,
        closed_path=True,
    )
    checks.check(
        "closed transport changes by conjugation while class data remain fixed",
        closed_covariance.endpoint_covariance_certified
        and closed_covariance.closed_conjugacy_certified
        and closed_covariance.transformed_transporter != forward.transporter,
    )

    su2 = su2_holonomy_evidence()
    checks.check(
        "source fundamental center controls are exact",
        su2.fundamental_2pi == -sp.eye(2)
        and su2.fundamental_4pi == sp.eye(2),
    )
    checks.check(
        "noncommuting guard has the exact quadratic BCH coefficient",
        su2.ordered_minus_naive != sp.zeros(2)
        and su2.bch_coefficient_certified
        and su2.commuting_residual == sp.zeros(2),
    )
    checks.check(
        "the same SU2 center element is representation dependent",
        su2.adjoint_2pi == sp.eye(3)
        and su2.fundamental_2pi_normalized_trace == -1
        and su2.adjoint_2pi_normalized_trace == 1
        and su2.fundamental_2pi_trace == -2
        and su2.adjoint_2pi_trace == 3,
    )

    source_su2_z_pi = sp.diag(sp.exp(-sp.I * sp.pi / 2), sp.exp(sp.I * sp.pi / 2))
    positive_sign_pi = sp.ImmutableMatrix((sp.I * sp.pi * t_3).exp())
    checks.check(
        "noncentral angle detects the source orientation mismatch",
        positive_sign_pi == -source_su2_z_pi
        and positive_sign_pi != source_su2_z_pi,
    )
    dictionaries = {
        "declared_weak": forward.transporter,
        "synthetic_internal": ordered_segment_holonomy((sp.pi * t_1, sp.pi * t_2)).transporter,
        "abstract_carrier": sp.I * sigma_3,
    }
    checks.check(
        "identical transport matrices leave physical dictionaries free",
        len(set(dictionaries)) == 3
        and all(matrix == forward.transporter for matrix in dictionaries.values()),
    )
    checks.check(
        "mutable P156 and canonical code has no executable legacy integration access",
        all(
            audit_numpy_trapezoid_compatibility(
                path.read_text(encoding="utf-8"),
                filename=str(path),
            ).legacy_references
            == 0
            for path in (
                Path(__file__),
                ROOT / "src/substrate_framework/nonabelian_holonomy.py",
                ROOT / "tests/test_nonabelian_holonomy.py",
            )
        ),
    )

    return checks.finish()


if __name__ == "__main__":
    tally = run()
    print(f"P156 PRIMARY ALL {tally} CHECKS PASS")
