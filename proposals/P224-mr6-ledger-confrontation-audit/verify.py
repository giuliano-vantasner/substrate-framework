"""Primary authority, exact-algebra, and bounded numeric audit for P224 MR6."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.bps_energy import bps_bound_per_absolute_degree
from substrate_framework.generalized_skyrme_radial import (
    solve_generalized_skyrme_radial_profile,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-44/"
    "bridge_MR6_ledger_and_confrontation.py"
)
SOURCE_SHA = "9443373f412cfe86b26bec6c35eb245ee83cd5dd5b65c76a5b3bb1c6d2106d9d"
FREEZE_SHA = "e55d564309810f0262b62df0b2d422351b7cdd30dc2c17eea2499d6127fbc858"
ME = 0.511
MPI = 138.03
MRHO = 775.26
NC = 3.0
UNIT = 16.0 * np.pi * ME
COUPLING = float(np.sqrt(MRHO / (16.0 * np.sqrt(2.0) * np.pi * ME)))
C6 = NC**2 * COUPLING**4 / (128.0 * np.pi**4)
C0 = 8.0 * MPI**2 / (COUPLING**4 * UNIT**2)


def branch(scale: float, *, l0_only: bool = False):
    factor = scale**2
    return solve_generalized_skyrme_radial_profile(
        1,
        1.0,
        0.0 if l0_only else factor * C6,
        C0 if l0_only else factor * C0,
        outer_radius=20.0,
        initial_points=401,
        sample_points=8001,
        continuation_steps=8,
        tolerance=1.0e-6,
        max_nodes=200_000,
    )


def main() -> int:
    checks = CheckLedger("P224")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    checks.check(
        "source and preregistered formula freeze are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA
        and hashlib.sha256(
            (CAMPAIGN / "evidence/formula-freeze.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source inventory separates six predicates from three assertions",
        len(calls) == 6 and len(assertions) == 3,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "MR6 uses current SciPy trapezoid without legacy NumPy access",
        compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0
        and "from scipy.integrate import solve_bvp, trapezoid" in source_text,
    )
    reproduction = yaml.safe_load(
        (CAMPAIGN / "evidence/source-reproduction.yaml").read_text()
    )["native_execution"]
    checks.check(
        "hash-identical native execution reaches all source nodes",
        reproduction["execution_classification"] == "clean_noncanonical"
        and reproduction["runtime_checks"] == 6
        and reproduction["assertions"] == 3
        and reproduction["exit_status"] == 0,
    )

    lambda_bps, lambda_a, mu, average = sp.symbols(
        "lambda_BPS lambda_A mu W", positive=True
    )
    bound = bps_bound_per_absolute_degree(lambda_bps, mu, average)
    checks.check(
        "same-current lambda conversion gives both exact bound coordinates",
        bound == 2 * lambda_bps * mu * sp.pi**2 * average
        and sp.simplify(
            bound.subs(lambda_bps, lambda_a / sp.pi**2)
            - 2 * lambda_a * mu * average
        )
        == 0,
    )
    pion, color = sp.symbols("m_pi N_c", positive=True)
    corrected = 8 * sp.sqrt(2) * color * pion / (15 * sp.pi)
    wrong = 8 * sp.sqrt(2) * sp.pi * color * pion / 15
    checks.check(
        "the source MK6 formula error is exactly pi squared",
        sp.simplify(wrong / corrected - sp.pi**2) == 0
        and sp.simplify(wrong - corrected) != 0,
    )
    corrected_value = float(corrected.subs({color: 3, pion: sp.Rational(13803, 100)}))
    wrong_value = float(wrong.subs({color: 3, pion: sp.Rational(13803, 100)}))
    checks.check(
        "conditional numeric substitution reproduces the governed correction",
        abs(corrected_value - 99.41652889533228) < 1.0e-12
        and abs(wrong_value / corrected_value - np.pi**2) < 1.0e-12,
    )

    ledger = yaml.safe_load(
        (CAMPAIGN / "evidence/authority-ledger.yaml").read_text()
    )
    checks.check(
        "authority ledger separates source changes from accepted claim changes",
        ledger["counts"]["source_claimed_overturns"] == 4
        and ledger["counts"]["executable_overturn_rows_actually_recomputed"] == 3
        and ledger["counts"]["executable_double_counting_predicates_recomputed"] == 0
        and ledger["counts"]["accepted_claims_changed_by_MR6"] == 0,
    )
    checks.check(
        "MK6.3 source proxy is two comparator thresholds not double counting",
        "mk63_before = (abs(M_cl_sector - M_NUCLEON)" in source_text
        and "mk63_after = (abs(M_cl_sector - M_NUCLEON)" in source_text
        and "finite_functional_interaction_ledger" not in source_text,
    )
    claims = {
        claim["id"]: claim
        for claim in yaml.safe_load((ROOT / "governance/claims.yaml").read_text())[
            "claims"
        ]
    }
    checks.check(
        "accepted variational claims contain no physical diagnosis",
        "no action" in claims["C-VAR-002"]["statement"]
        and "double-counting diagnosis" in claims["C-VAR-003"]["statement"]
        and "supplies no physical decomposition" in claims["C-VAR-003"]["statement"],
    )
    p223 = yaml.safe_load(
        (
            ROOT
            / "campaigns/P223-mr5-derived-coupling-solve-audit/evidence/primary-numerical-evidence.yaml"
        ).read_text()
    )
    governed_kappa = p223["domains"]["R20"]["kappa"]
    checks.check(
        "MR6 confrontation kappa is stale and not executable",
        abs(governed_kappa - 11.536444259568) < 1.0e-12
        and "kappa   = 11.49" in source_text
        and "def kappa" not in source_text
        and "KAPPA" not in source_text,
    )

    s, c6, c0 = sp.symbols("s c6 c0", nonnegative=True)
    checks.check(
        "common lambda-mu scaling gives the declared coefficient path exactly",
        sp.diff(s**2 * c6, s) == 2 * s * c6
        and sp.diff(s**2 * c0, s) == 2 * s * c0
        and (s**2 * c6).subs(s, 0) == 0
        and (s**2 * c0).subs(s, 0) == 0,
    )
    profiles = {scale: branch(scale) for scale in (0.0, 0.25, 0.5, 0.75, 1.0)}
    l0_profile = branch(1.0, l0_only=True)
    checks.check(
        "canonical sampled branches pass status residual and boundary gates",
        all(
            item.max_rms_residual < 1.1e-6
            and abs(item.inner_boundary_residual) < 2.0e-11
            and abs(item.outer_boundary_residual) < 2.0e-11
            and np.all(np.isfinite(item.field))
            for item in (*profiles.values(), l0_profile)
        ),
    )
    values = [profiles[scale].energy_coefficient for scale in profiles]
    checks.check(
        "five source-scale points reproduce a monotone stationary-branch sample",
        all(right > left for left, right in zip(values, values[1:]))
        and abs(values[0] - 1.2313219792351653) < 3.0e-8
        and abs(values[-1] - 1.435998787155452) < 3.0e-8,
    )
    check_call_63 = next(call for call in calls if call.lineno == 258)
    checks.check(
        "finite source scan contains no continuous monotonicity oracle",
        len(check_call_63.args) >= 2
        and "monotone" in {node.id for node in ast.walk(check_call_63) if isinstance(node, ast.Name)}
        and "derivative" not in {node.id for node in ast.walk(check_call_63) if isinstance(node, ast.Name)}
        and "scales = [0.0, 0.25, 0.5, 0.75, 1.0]" in source_text,
    )
    checks.check(
        "one common scaling path cannot localize two independent coefficients",
        sp.Matrix([[sp.diff(s**2 * c6, s)], [sp.diff(s**2 * c0, s)]]).rank() == 1,
    )

    base_values = (0, 1)
    added_values = (0, 1)
    joint_values = tuple(a + b for a, b in zip(base_values, added_values))
    checks.check(
        "positivity somewhere does not imply a strict infimum increase",
        min(base_values) == min(joint_values) == 0
        and max(added_values) > 0
        and all(value >= 0 for value in added_values),
    )
    checks.check(
        "accepted variational owner states only the nonstrict order without extra hypotheses",
        "M>=sum_i m_i" in claims["C-VAR-002"]["statement"]
        and "incompatible component minimizers" in claims["C-VAR-002"]["statement"]
        and "strictly raises its minimum" in source_text,
    )

    numeric_literals = {
        float(node.value)
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    }
    checks.check(
        "source guard omits comparators that directly drive pass predicates",
        938.92 in numeric_literals
        and 1836.15 in numeric_literals
        and "mk62_before" in source_text
        and "dev_L0" in source_text
        and "FORBIDDEN = [929 / 1000.0, 28296 / 1000.0]" in source_text,
    )
    checks.check(
        "guard recomputation omits every solved stationary branch",
        "indep = (abs(e2 - E_DER)" in source_text
        and "B_CL" not in source_text[source_text.index("indep = ("):source_text.index("check(\n    \"MR6.6")]
        and "B_FULL" not in source_text[source_text.index("indep = ("):source_text.index("check(\n    \"MR6.6")]
        and "B_L0" not in source_text[source_text.index("indep = ("):source_text.index("check(\n    \"MR6.6")],
    )
    delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "all surviving exact surfaces already have accepted owners",
        delta["reserved_identifiers"] == []
        and set(delta["unchanged_exact_owners"])
        == {"C-BPS-001", "C-VEC-002", "C-VAR-002"}
        and delta["package_change"] == "none"
        and delta["release_change"] == "none",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
