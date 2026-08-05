#!/usr/bin/env python3
"""Primary exact verifier for TX5 source adjudication and C-SKY-002."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

import substrate_framework.skyrme_o4 as skyrme_o4_module
from substrate_framework.radial_modes import derrick_scaling_evidence
from substrate_framework.skyrme_o4 import o4_skyrme_pointwise_evidence
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-40/"
    "bridge_TX5_full_field_stability.py"
)
SOURCE_SHA256 = "ea12c1fee0dab254c4d8cdc984ee694622199e7cb5380674d689cf1fe6f0e31a"
RELEASE_SHA256 = "001e589256cf33518612e5f24e8714bed14b1ff59cf78343448e90f29c949ecf"
DESCENT_ORACLE = (
    ROOT
    / "campaigns/P184-tx5-full-field-stability-audit/attempts/0004/"
    "diagnose_declared_resolution_descent.py"
)
DESCENT_ORACLE_SHA256 = "8d21eb9d9e3c9795d416a9c594c6c822cad060da7fb8dc5673dda180e7a966ef"
DESCENT_RESULT = DESCENT_ORACLE.with_name("result.yaml")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P184-TX5-C-SKY-002")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.135.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "declared-resolution descent oracle remains pinned",
        _digest(DESCENT_ORACLE) == DESCENT_ORACLE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    lexical_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source lexical and assertion inventory is exact",
        len(lexical_checks) == 8 and len(assertions) == 2,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "TX5 has no NumPy trapezoidal compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source declares the same conditional pointwise mass matrix",
        "M = 2 * ((1 + np.trace(D)) * np.eye(4) - G.T @ G)" in source_text,
    )
    checks.check(
        "strict full-field minimum headline is not one source predicate",
        "STRICT LOCAL MINIMUM" in source_text
        and not any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            and any(
                isinstance(argument, ast.Constant)
                and isinstance(argument.value, str)
                and "STRICT LOCAL MINIMUM" in argument.value
                for argument in node.args
            )
            for node in ast.walk(tree)
        ),
    )

    descent = yaml.safe_load(DESCENT_RESULT.read_text(encoding="utf-8"))
    measured = descent["measured"]
    checks.check(
        "pinned declared-resolution oracle found a stable first-order descent",
        descent["status"] == "passed"
        and descent["configuration"] == {
            "N": 91,
            "L": 6.0,
            "dx": 0.13333333333333333,
            "relaxation_steps": 600,
        }
        and all(slope < 0 for slope in measured["slopes"]),
    )
    checks.check(
        "positive symmetric curvature coexists with lower energy and nonstationarity",
        all(value > 0 for value in measured["curve_second_differences"])
        and measured["one_more_step_energy"] < measured["base_energy"]
        and measured["source_gradient_norm"] > 0,
    )

    gradient_entries = sp.symbols("g0:12", real=True)
    tangent_entries = sp.symbols("w0:4", real=True)
    evidence = o4_skyrme_pointwise_evidence(
        [gradient_entries[0:4], gradient_entries[4:8], gradient_entries[8:12]],
        tangent_entries,
    )
    checks.check(
        "quartic trace form equals the complete spatial-component minor square sum",
        evidence.quartic_identity_residual == 0
        and evidence.quartic_has_sos_certificate,
    )
    checks.check(
        "declared static density is quadratic norm plus quartic square sum",
        evidence.static_density
        == sp.expand(evidence.quadratic_density + evidence.quartic_minor_sos),
    )
    checks.check(
        "mass operator is exactly symmetric",
        evidence.mass_operator == evidence.mass_operator.T,
    )
    checks.check(
        "mass quadratic form minus twice tangent norm is a complete square sum",
        evidence.mass_identity_residual == 0
        and evidence.mass_has_sharp_lower_bound_certificate,
    )
    sharp = o4_skyrme_pointwise_evidence(
        [[2, 0, 0, 0], [-3, 0, 0, 0], [5, 0, 0, 0]],
        [7, 0, 0, 0],
    )
    checks.check(
        "the exact two-identity mass lower bound is sharp",
        sharp.mass_lower_bound_gap == 0
        and sharp.mass_quadratic_form == 2 * sharp.tangent_norm_squared,
    )
    orthogonal = o4_skyrme_pointwise_evidence(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]],
        [1, 0, 0, 0],
    )
    checks.check(
        "quartic-sign mutation makes an exact declared example negative",
        orthogonal.quartic_trace_form == 1
        and -orthogonal.quartic_trace_form == -1,
    )
    zero_gradient = o4_skyrme_pointwise_evidence(
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        [1, 0, 0, 0],
    )
    mutated_mass = zero_gradient.mass_operator - 2 * sp.eye(4)
    checks.check(
        "identity-term mutation breaks the exact mass lower bound",
        zero_gradient.mass_operator == 2 * sp.eye(4)
        and (zero_gradient.tangent.T * mutated_mass * zero_gradient.tangent)[0]
        < 2 * zero_gradient.tangent_norm_squared,
    )

    e2, e4 = sp.symbols("E2 E4", positive=True)
    scale, alpha = sp.symbols("s alpha", real=True, positive=True)
    derrick = derrick_scaling_evidence(e2, e4, scale)
    checks.check(
        "existing logarithmic Derrick API gives the full-space alpha family exactly",
        sp.simplify(
            derrick.scaled_energy.subs(scale, -sp.log(alpha))
            - (alpha * e2 + e4 / alpha)
        )
        == 0,
    )
    checks.check(
        "Derrick stationarity and positive scaling curvature remain distinct obligations",
        derrick.stationary_condition == -e2 + e4
        and derrick.slope_at_origin == -e2 + e4
        and derrick.curvature_at_origin == e2 + e4,
    )
    checks.check(
        "canonical theorem explicitly excludes source headline consequences",
        "does not" in (skyrme_o4_module.__doc__ or "").lower()
        and all(
            phrase in (skyrme_o4_module.__doc__ or "").lower()
            for phrase in ("stationary", "local", "rotating", "dynamic")
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
