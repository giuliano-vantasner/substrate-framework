#!/usr/bin/env python3
"""Exact source-aware verifier for the SM3 anomaly claim delta."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.chiral_anomalies import (
    ChiralGaugeMultiplet,
    charge_conjugate_chiral_multiplet,
    chiral_anomaly_ledger,
    five_row_chiral_anomaly_ledger,
    five_row_local_anomaly_membership,
    five_row_local_anomaly_solution_variety,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P165-sm3-anomaly-cancellation-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-9/"
    "bridge_SM3_anomaly_cancellation.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
SOURCE_SHA256 = "3ace90aa5377050e4dcab5778996079eea92c9cc56a53c276a60a5508f63b529"
FROZEN_SHA256 = "2ff19c8d29c6d9619eb644118a9bf6d01331b8029ff20535c1faa19c82a86640"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _displayed_charges() -> tuple[sp.Expr, ...]:
    return (
        sp.Rational(1, 6),
        -sp.Rational(2, 3),
        sp.Rational(1, 3),
        -sp.Rational(1, 2),
        sp.Integer(1),
    )


def run() -> int:
    checks = CheckLedger("P165/SM3")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned SM3 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("frozen proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("eight source predicate sites", len(source_checks) == 8)
    checks.check("one source assertion node", len(source_assertions) == 1)
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "SM3 has no NumPy integration compatibility surface",
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
    checks.check("native SM3 exits cleanly", native.returncode == 0)
    checks.check(
        "native SM3 terminal tally is exact",
        native_lines.count("ALL 8 CHECKS PASS") == 1,
    )

    displayed = five_row_chiral_anomaly_ledger(*_displayed_charges())
    checks.check(
        "canonical ledger reproduces all six supplied anomaly zeroes",
        displayed.local_coefficients == (0, 0, 0, 0, 0)
        and displayed.factor_b_fundamental_doublet_count == 4
        and displayed.factor_b_fundamental_doublet_parity_even,
    )
    q, u, d, l, e = sp.symbols("q u d l e", real=True)
    symbolic = five_row_chiral_anomaly_ledger(q, u, d, l, e)
    checks.check(
        "canonical mixed coefficients match source conventions exactly",
        symbolic.mixed_factor_a_squared_abelian == (2 * q + u + d) / 2
        and symbolic.mixed_factor_b_squared_abelian == (3 * q + l) / 2,
    )
    checks.check(
        "canonical Abelian coefficients retain all row multiplicities",
        symbolic.mixed_gravity_squared_abelian
        == 6 * q + 3 * u + 3 * d + 2 * l + e
        and symbolic.abelian_cubed
        == 6 * q**3 + 3 * u**3 + 3 * d**3 + 2 * l**3 + e**3,
    )
    checks.check(
        "fixed carrier makes color cubic and doublet parity charge-independent",
        symbolic.factor_a_cubed == 0
        and symbolic.factor_b_fundamental_doublet_count == 4,
    )

    variety = five_row_local_anomaly_solution_variety()
    checks.check(
        "linear elimination is exact without a nonzero-q assumption",
        variety.linear_solution == ((l, -3 * q), (e, 6 * q), (d, -2 * q - u)),
    )
    checks.check(
        "reduced cubic exposes every load-bearing factor",
        variety.reduced_cubic == 18 * q * (2 * q - u) * (4 * q + u),
    )
    checks.check(
        "solution variety contains exactly the three named affine lines",
        tuple(branch.name for branch in variety.branches)
        == ("displayed_line", "row_exchanged_line", "vectorlike_line")
        and all(
            five_row_local_anomaly_membership(branch.charges).is_solution
            for branch in variety.branches
        ),
    )

    displayed_membership = five_row_local_anomaly_membership(_displayed_charges())
    exchanged_membership = five_row_local_anomaly_membership(
        (
            sp.Rational(1, 6),
            sp.Rational(1, 3),
            -sp.Rational(2, 3),
            -sp.Rational(1, 2),
            1,
        )
    )
    vectorlike_membership = five_row_local_anomaly_membership((0, 1, -1, 0, 0))
    checks.check(
        "displayed point belongs only to the displayed nonzero line",
        displayed_membership.matching_branches == ("displayed_line",),
    )
    checks.check(
        "row-exchanged nonzero line refutes source uniqueness",
        exchanged_membership.is_solution
        and exchanged_membership.matching_branches == ("row_exchanged_line",),
    )
    checks.check(
        "zero-q vectorlike line refutes source one-freedom prose",
        vectorlike_membership.is_solution
        and vectorlike_membership.matching_branches == ("vectorlike_line",),
    )

    lam = sp.symbols("lambda", real=True, nonzero=True)
    scaled = five_row_chiral_anomaly_ledger(
        lam * q,
        lam * u,
        lam * d,
        lam * l,
        lam * e,
    )
    checks.check(
        "common scaling has the correct degrees without selecting a component",
        sp.simplify(
            scaled.mixed_factor_a_squared_abelian
            - lam * symbolic.mixed_factor_a_squared_abelian
        )
        == 0
        and sp.simplify(
            scaled.mixed_factor_b_squared_abelian
            - lam * symbolic.mixed_factor_b_squared_abelian
        )
        == 0
        and sp.simplify(scaled.abelian_cubed - lam**3 * symbolic.abelian_cubed) == 0
        and sp.simplify(
            scaled.mixed_gravity_squared_abelian
            - lam * symbolic.mixed_gravity_squared_abelian
        )
        == 0,
    )
    wrong_electron = five_row_chiral_anomaly_ledger(*(_displayed_charges()[:-1] + (0,)))
    checks.check(
        "source electron mutation remains load-bearing",
        wrong_electron.abelian_cubed == -1
        and wrong_electron.mixed_gravity_squared_abelian == -1,
    )

    half = sp.Rational(1, 2)
    wrong_cubic_rows = (
        ChiralGaugeMultiplet("Q", 3, 2, 0, half, half, 1, True),
        ChiralGaugeMultiplet("u_wrong", 3, 1, 0, half, 0, 1, False),
        ChiralGaugeMultiplet("d", 3, 1, 0, half, 0, -1, False),
    )
    checks.check(
        "wrong conjugate representation sign reopens the cubic color coefficient",
        chiral_anomaly_ledger(wrong_cubic_rows).factor_a_cubed == 2,
    )
    conjugate = charge_conjugate_chiral_multiplet(
        wrong_cubic_rows[0],
        label="Q_bar",
    )
    checks.check(
        "charge conjugation flips both Abelian and cubic orientation signs",
        conjugate.abelian_charge == -wrong_cubic_rows[0].abelian_charge
        and conjugate.factor_a_cubic_index == -1
        and conjugate.factor_a_quadratic_index == half,
    )
    removed_lepton = chiral_anomaly_ledger(wrong_cubic_rows)
    checks.check(
        "removing the lepton doublet makes the supplied doublet count odd",
        removed_lepton.factor_b_fundamental_doublet_count == 3
        and not removed_lepton.factor_b_fundamental_doublet_parity_even,
    )
    neutral = ChiralGaugeMultiplet("neutral", 1, 1, 0, 0, 0, 0, False)
    neutral_ledger = chiral_anomaly_ledger(displayed.multiplets + (neutral,))
    checks.check(
        "neutral singlet leaves coefficients unchanged and defeats completeness",
        neutral_ledger.local_coefficients == displayed.local_coefficients
        and len(neutral_ledger.multiplets) == len(displayed.multiplets) + 1,
    )

    checks.check(
        "source contains no complete ideal or branch classifier",
        "groebner" not in source_text.lower()
        and "linsolve" not in source_text.lower()
        and "row_exchanged" not in source_text
        and "vectorlike_line" not in source_text,
    )
    checks.check(
        "source uniqueness prose exceeds its implemented two-direction guard",
        "UNIQUE (up to overall scale)" in source_text
        and "the one true freedom" in source_text
        and "Y_{e_R^c}: +1 -> 0" in source_text
        and "Y_{Q_L}: 1/6 -> 1/6 + delta" in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P165 ALL {result} CHECKS PASS")
