"""Primary exact and governance verifier for the P220 MR2 audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.bps_energy import bps_bound_per_absolute_degree
from substrate_framework.generalized_skyrme_radial import (
    generalized_skyrme_reduced_coefficients,
)
from substrate_framework.hls_reduction import (
    conditional_vector_current_sextic_matching,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path(__file__).resolve().parent
ROOT = CAMPAIGN.parents[1]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-44/"
    "bridge_MR2_bps_normalization_pi_squared.py"
)
SOURCE_SHA = "2e62ce2d6cbee805a988046a27a742e622931291e8e013a9aede6ce16e48e990"
FREEZE_SHA = "a660d26ba399c114cb4057af7d68f287cc47e22a44ac70c6402b7d41e502dafb"


def _lambda_a_for_current_scale(
    lambda_bps: sp.Expr,
    current_scale: sp.Expr,
) -> sp.Expr:
    """Return the positive coupling map for B_A=current_scale*B_BPS."""

    return sp.simplify(sp.pi**2 * lambda_bps / current_scale)


def main() -> int:
    checks = CheckLedger("P220")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source and preregistered formula surface are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA
        and hashlib.sha256(
            (CAMPAIGN / "evidence/formula-freeze.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    executable_names = {
        node.id for node in ast.walk(source_tree) if isinstance(node, ast.Name)
    }
    assignments = {
        target.id: node.value
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name)
    }
    checks.check(
        "source inventory separates eight predicates and one assertion",
        len(calls) == 8 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "MR2 has no NumPy SciPy or trapezoidal compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0
        and "numpy" not in source_text
        and "scipy" not in source_text,
    )
    reproduction = yaml.safe_load(
        (CAMPAIGN / "evidence/source-reproduction.yaml").read_text()
    )
    checks.check(
        "hash-identical P215 execution is durable without a ceremonial rerun",
        reproduction["execution"]["source_hash_identical"] is True
        and reproduction["execution"]["exit_status"] == 0
        and reproduction["inventory"]["runtime_check_executions"] == 8
        and reproduction["execution"]["terminal_tally"] == "ALL_8_CHECKS_PASS",
    )

    profile_value = sp.symbols("F_profile", real=True)
    normalized_radial = -sp.sin(profile_value) ** 2 / (2 * sp.pi**2)
    unit_degree = sp.simplify(
        4 * sp.pi * sp.integrate(normalized_radial, (profile_value, sp.pi, 0))
    )
    unnormalized_degree = sp.simplify(
        4
        * sp.pi
        * sp.integrate(-sp.sin(profile_value) ** 2, (profile_value, sp.pi, 0))
    )
    checks.check(
        "hedgehog density is unit normalized and the omitted factor is detected",
        unit_degree == 1 and unnormalized_degree == 2 * sp.pi**2,
    )

    lambda_a, lambda_bps, current, scale = sp.symbols(
        "lambda_A lambda_BPS B_current q",
        positive=True,
    )
    positive_solution = sp.solve(
        sp.Eq((lambda_a * scale * current) ** 2, (lambda_bps * sp.pi**2 * current) ** 2),
        lambda_a,
    )
    checks.check(
        "positive-root elimination retains the current-normalization scale",
        positive_solution == [_lambda_a_for_current_scale(lambda_bps, scale)],
    )
    checks.mutation_sensitive(
        "same normalized current is load bearing for the pi-squared map",
        lambda candidate_scale: sp.simplify(
            _lambda_a_for_current_scale(lambda_bps, candidate_scale)
            - sp.pi**2 * lambda_bps
        )
        == 0,
        1,
        (2, sp.Rational(1, 2), sp.pi),
    )

    matching = conditional_vector_current_sextic_matching(
        sp.symbols("m", positive=True),
        sp.symbols("g", positive=True),
    )
    checks.check(
        "canonical current elimination already owns the same convention ratio",
        matching.convention_ratio == sp.pi**2
        and sp.simplify(matching.source_sextic_coupling / sp.pi**2 - matching.bps_sextic_coupling)
        == 0,
    )

    mu, coupling, decay_scale, average, degree = sp.symbols(
        "mu e F W B",
        positive=True,
    )
    c6_bps, _ = generalized_skyrme_reduced_coefficients(
        lambda_bps,
        mu,
        coupling,
        decay_scale,
    )
    c6_a = lambda_a**2 * coupling**4 * decay_scale**2 / (8 * sp.pi**4)
    checks.check(
        "canonical reduced coefficients already own both lambda coordinates",
        sp.simplify(c6_a.subs(lambda_a, sp.pi**2 * lambda_bps) - c6_bps) == 0,
    )
    checks.check(
        "omitting the pi-squared conversion changes the reduced coefficient",
        sp.simplify(c6_a.subs(lambda_a, lambda_bps) - c6_bps) != 0,
    )

    bps_bound = bps_bound_per_absolute_degree(lambda_bps, mu, average) * degree
    a_bound = 2 * lambda_a * mu * average * degree
    checks.check(
        "canonical BPS and lambda-A bounds are the same conditional object",
        sp.simplify(a_bound.subs(lambda_a, sp.pi**2 * lambda_bps) - bps_bound) == 0,
    )
    nc, pion_mass = sp.symbols("N_c m_pi", positive=True)
    supplied_lambda_a = nc / (4 * decay_scale)
    supplied_mu = pion_mass * decay_scale / 2
    source_average = 32 * sp.sqrt(2) / (15 * sp.pi)
    corrected = sp.simplify(
        a_bound.subs(
            {
                lambda_a: supplied_lambda_a,
                mu: supplied_mu,
                average: source_average,
            }
        )
    )
    expected = 8 * sp.sqrt(2) * nc * pion_mass * degree / (15 * sp.pi)
    source_mk6 = 8 * sp.sqrt(2) * sp.pi * nc * pion_mass * degree / 15
    checks.check(
        "the corrected supplied-input expression follows exactly",
        sp.simplify(corrected - expected) == 0,
    )
    checks.check(
        "the rejected MK6 expression is exactly pi squared larger",
        sp.simplify(source_mk6 / corrected - sp.pi**2) == 0,
    )
    checks.check(
        "the corrected expression still depends on supplied inputs",
        corrected.free_symbols == {nc, pion_mass, degree},
    )
    corrected_value = corrected.subs(
        {nc: 3, pion_mass: sp.Rational(13803, 100), degree: 1}
    )
    checks.check(
        "99.417 MeV is a reproducible conditional substitution only",
        abs(float(corrected_value) - 99.4165288953323) < 1.0e-12
        and corrected.free_symbols,
    )

    angular_integral = 16 * sp.sqrt(2) / 15
    c0 = 32 * mu**2 / (coupling**2 * decay_scale**4)
    reduced_square_bound = sp.simplify(
        sp.pi
        * decay_scale
        / coupling
        * 2
        * sp.sqrt(c6_a * c0)
        * angular_integral
    )
    direct_a_bound = sp.simplify(2 * lambda_a * mu * source_average)
    checks.check(
        "MR2 reduced route eliminates to the same coefficient identity",
        sp.simplify(reduced_square_bound - direct_a_bound) == 0,
    )
    checks.check(
        "the reduced route has no independent free-symbol surface",
        reduced_square_bound.free_symbols == direct_a_bound.free_symbols
        and reduced_square_bound.free_symbols == {lambda_a, mu},
    )

    slack = sp.symbols("s", nonnegative=True)
    checks.check(
        "a lower bound does not establish the physical sector energy",
        sp.simplify((direct_a_bound + slack) - direct_a_bound) == slack
        and (direct_a_bound + slack).subs(slack, 1) != direct_a_bound,
    )
    checks.check(
        "source guard is selected-token evidence rather than dependency closure",
        isinstance(assignments.get("FORBIDDEN"), ast.List)
        and len(assignments["FORBIDDEN"].elts) == 3
        and all(isinstance(element, ast.BinOp) for element in assignments["FORBIDDEN"].elts)
        and isinstance(assignments.get("derived_clean"), ast.Compare)
        and "m_e" not in executable_names,
    )

    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    claims = {entry["id"]: entry for entry in registry["claims"]}
    checks.check(
        "accepted registry owns every exact MR2 survivor",
        all(
            claims[claim_id]["review"] == "accepted"
            for claim_id in ("C-BPS-001", "C-VEC-002", "C-GSK-001")
        )
        and "lambda_A=pi^2*lambda" in " ".join(claims["C-BPS-001"]["assumptions"])
        and "lambda_BPS=lambda_A/pi^2" in claims["C-VEC-002"]["statement"]
        and "lambda_A=pi^2*lambda_BPS" in claims["C-GSK-001"]["statement"],
    )
    post_delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "claim delta remains empty after exact nonduplication",
        post_delta["provisional_claims"] == []
        and post_delta["decision"] == "retain_no_claim_or_canonical_API"
        and post_delta["expected_disposition"] == "duplicate_evidence",
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
