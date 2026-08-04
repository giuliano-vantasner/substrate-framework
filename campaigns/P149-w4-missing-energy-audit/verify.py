#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-KIN-001 and W4."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.relativistic_thresholds import two_body_threshold_ledger
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P149-w4-missing-energy-audit"
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / "merged-framework/bridges/phase-6/bridge_W4_neutrino_missing_energy.py"
DOSSIER = SOURCE_ROOT / "merged-framework/bridges/phase-6/dossiers/W4_dossier.md"
SOLUTION = SOURCE_ROOT / "sg-breather-ionization/solution.md"
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
SOURCE_SHA256 = "afa341c860ba89889d8d0a9fe6cd62948b5303f243e3884abf7d3acf24a7f602"
DOSSIER_SHA256 = "c72601001ded5c27bd56984609afcffb664e02aacbfca7222e9d583f662f4413"
SOLUTION_SHA256 = "a5a0ced9a097f07daea67e37b9516755307536e4850dfc975da72ee8eb876f86"
FROZEN_SHA256 = "33a12bf08d88a972983b3fe5da82321cf616e918ff3cbc69f6f79801a1324054"
REVISION_SHA256 = "65bbd11e137f54cb6c6c7cda69fb40dd5730964c9203d9f35b461607dc46c06b"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    checks = CheckLedger("P149/C-KIN-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    dossier_text = DOSSIER.read_text(encoding="utf-8")
    solution_text = SOLUTION.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned W4 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("pinned W4 dossier hash", _sha256(DOSSIER) == DOSSIER_SHA256)
    checks.check("pinned imported outcome hash", _sha256(SOLUTION) == SOLUTION_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("eight source predicates", len(source_checks) == 8)
    checks.check("one source assertion", len(source_assertions) == 1)
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "W4 has no NumPy integration compatibility shape",
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
    checks.check("native W4 exits cleanly", native.returncode == 0)
    checks.check(
        "native W4 terminal tally is exact",
        native.stdout.rstrip().endswith("ALL 8 CHECKS PASS"),
    )

    mass1, mass2 = sp.symbols("m1 m2", positive=True)
    rapidity = sp.symbols("theta", real=True)
    ledger = two_body_threshold_ledger(mass1, mass2, rapidity)
    checks.check(
        "observed particle is derived on shell",
        ledger.observed_mass_shell_residual == 0,
    )
    checks.check(
        "threshold four-momentum closes componentwise",
        ledger.four_momentum_closure == sp.zeros(2, 1),
    )
    target_defect = 2 * mass1 * (mass1 + mass2) * (1 - sp.cosh(rapidity))
    checks.check(
        "residual mass-shell defect is exact",
        sp.simplify(ledger.residual_mass_shell_defect - target_defect) == 0,
    )
    zero = two_body_threshold_ledger(mass1, mass2, 0)
    checks.check(
        "zero recoil leaves both target masses on shell",
        zero.observed_four_momentum == sp.ImmutableMatrix((mass1, 0))
        and zero.residual_four_momentum == sp.ImmutableMatrix((mass2, 0))
        and zero.residual_mass_shell_defect == 0,
    )

    w4_point = two_body_threshold_ledger(8, 8, sp.log(2))
    observed = w4_point.observed_four_momentum.applyfunc(
        lambda value: sp.simplify(value.rewrite(sp.exp))
    )
    residual = w4_point.residual_four_momentum.applyfunc(
        lambda value: sp.simplify(value.rewrite(sp.exp))
    )
    defect = sp.simplify(w4_point.residual_mass_shell_defect.rewrite(sp.exp))
    checks.check(
        "W4 velocity point gives exact observed kink vector",
        observed == sp.ImmutableMatrix((10, 6)),
    )
    checks.check(
        "W4 opposite-momentum residual is massless rather than a kink",
        residual == sp.ImmutableMatrix((6, -6))
        and w4_point.residual_target_mass == 8
        and defect == -64,
    )
    checks.check(
        "W4 assigned hidden gamma violates the free-particle domain",
        sp.Rational(2) - sp.Rational(5, 4) == sp.Rational(3, 4)
        and sp.Rational(3, 4) < 1,
    )
    checks.check(
        "above-threshold energy repairs the two-free-particle recoil ledger",
        observed[0] + sp.sqrt(8**2 + observed[1] ** 2) == 20
        and 20 > 16,
    )

    omega = sp.symbols("omega", real=True)
    breather_energy = 16 * sp.sqrt(1 - omega**2)
    threshold_deficit = 16 - breather_energy
    checks.check(
        "W4.1 maps only to the accepted scalar threshold partition",
        sp.simplify(breather_energy + threshold_deficit - 16) == 0,
    )
    gamma = sp.symbols("gamma", real=True)
    missing_expression = 16 - 8 * gamma
    coincidence = sp.solve(
        sp.Eq(missing_expression, threshold_deficit), gamma
    )
    checks.check(
        "W4.2 derives scalar equality but no state identity",
        coincidence == [2 * sp.sqrt(1 - omega**2)]
        and "intact breather" in source_text
        and "state" not in {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)},
    )
    checks.check(
        "W4.3 scalar subtraction closes but hidden free kink fails",
        sp.simplify(8 * gamma + missing_expression - 16) == 0
        and "a consistent free kink" in source_text
        and defect != 0,
    )
    checks.check(
        "W4.4 algebraic residual bounds do not create an on-shell interval",
        sp.diff(missing_expression, gamma) == -8
        and sp.simplify(target_defect.subs({mass1: 8, mass2: 8}))
        == 256 * (1 - sp.cosh(rapidity)),
    )
    checks.check(
        "W4.5 momentum is assigned independently of the energy mass shell",
        "P_absorbed_val = sp.solve" in source_text
        and "P_missing = P_absorbed_val" in source_text
        and residual[0] ** 2 - residual[1] ** 2 == 0,
    )
    checks.check(
        "W4.6 numerical point adds no new exact claim",
        threshold_deficit.subs(omega, sp.Rational(1, 2)) == 16 - 8 * sp.sqrt(3)
        and missing_expression.subs(gamma, 1) == 8,
    )

    checks.check(
        "W4.G1 conditional zero is written into a Piecewise definition",
        "E_missing_ionization_elastic = sp.Piecewise" in source_text
        and "DeltaQ_elastic = 0" in source_text,
    )
    checks.check(
        "imported both-absorbed outcome defeats charge-to-visibility implication",
        "(b) Both absorbed → Q_reflected = 0" in solution_text,
    )
    checks.check(
        "W4.G2 boosted both-reflect ledger becomes negative not zero",
        (16 - 8 * (sp.Rational(5, 4) + sp.Rational(5, 4))) == -4,
    )
    checks.check(
        "dossier admits it never measured the proposed spatial split",
        "does NOT output the absorbed/reflected energy split directly" in dossier_text
        and "optional SciPy numeric as a secondary check" in dossier_text,
    )
    loaded_names = {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    checks.check(
        "W4 executes no field evolution or boundary flux solver",
        not loaded_names.intersection(
            {"solve_ivp", "solve_bvp", "evolve", "boundary_flux", "stress_tensor"}
        ),
    )
    checks.check(
        "W3 physical-current dependency has no accepted authority",
        "W3's V-A vertex" in source_text,
    )

    wrong_total = sp.ImmutableMatrix((mass1 + mass2 + 1, 0))
    wrong_residual = wrong_total - ledger.observed_four_momentum
    wrong_defect = sp.trigsimp(
        wrong_residual[0] ** 2 - wrong_residual[1] ** 2 - mass2**2
    )
    checks.check(
        "threshold-energy mutation changes the load-bearing defect",
        sp.simplify(wrong_defect - ledger.residual_mass_shell_defect) != 0,
    )
    wrong_momentum_residual = sp.ImmutableMatrix(
        (ledger.residual_four_momentum[0], -ledger.residual_four_momentum[1])
    )
    checks.check(
        "momentum sign mutation preserves invariant but breaks vector closure",
        sp.trigsimp(
            wrong_momentum_residual[0] ** 2 - wrong_momentum_residual[1] ** 2
            - ledger.residual_invariant_mass_squared
        )
        == 0
        and sp.simplify(
            ledger.threshold_four_momentum
            - ledger.observed_four_momentum
            - wrong_momentum_residual
        )
        != sp.zeros(2, 1),
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/relativistic_thresholds.py"
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P149 and canonical code has no legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P149 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
