"""Primary exact verifier for the P215 MK2 vector-sextic audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess

import sympy as sp
import yaml

from substrate_framework.effective_actions import low_momentum_inverse_expansion
from substrate_framework.hls_reduction import (
    conditional_hls_ksrf_matching,
    conditional_vector_current_sextic_matching,
    u2_invariant_metric,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-43/"
    "bridge_MK2_lambda_from_medium_omega.py"
)
SOURCE_SHA256 = "351136bca28e413ddd54f1b15bf7084dffe32af565fc87e7220d1437a525eb07"
FORMULA_FREEZE_SHA256 = "64b3732609a582039387d8187df69f501d417c325f05e25f6ea87e48d1657c80"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _claim_map() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load((ROOT / "governance/claims.yaml").read_text())
    return {claim["id"]: claim for claim in registry["claims"]}


def _u2_invariance_solution() -> sp.FiniteSet:
    entries = sp.symbols("g00 g01 g02 g03 g11 g12 g13 g22 g23 g33")
    g00, g01, g02, g03, g11, g12, g13, g22, g23, g33 = entries
    metric = sp.Matrix(
        [
            [g00, g01, g02, g03],
            [g01, g11, g12, g13],
            [g02, g12, g22, g23],
            [g03, g13, g23, g33],
        ]
    )
    equations: list[sp.Expr] = []
    for axis in range(3):
        adjoint = sp.zeros(4)
        for first in range(3):
            for second in range(3):
                adjoint[1 + first, 1 + second] = sp.LeviCivita(
                    axis,
                    first,
                    second,
                )
        equations.extend(adjoint.T * metric + metric * adjoint)
    return sp.linsolve(equations, entries)


def main() -> int:
    checks = CheckLedger("P215")

    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    checks.check(
        "MK2 source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "pre-source formula freeze is immutable",
        _sha256(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )
    literal_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source inventory separates seven predicates from one assertion",
        len(literal_checks) == 7
        and len(assertions) == 1
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "MK2 has no NumPy integration compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = subprocess.run(
        [str(ROOT / ".venv/bin/python"), str(SOURCE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    checks.check(
        "native source executes all seven runtime predicates cleanly",
        native.returncode == 0
        and native.stdout.count("  PASS\n") == 7
        and native.stdout.rstrip().endswith("ALL 7 CHECKS PASS"),
    )

    mass, coupling = sp.symbols("m_omega g_omega", positive=True)
    matching = conditional_vector_current_sextic_matching(mass, coupling)
    checks.check(
        "canonical quadratic elimination derives the stationary vector",
        matching.stationary_field_per_current == -coupling / mass**2
        and matching.stationarity_residual == sp.zeros(1),
    )
    checks.check(
        "canonical elimination derives the source-convention squared-current term",
        matching.effective_current_coefficient == -coupling**2 / (2 * mass**2)
        and matching.source_sextic_coupling
        == coupling / (sp.sqrt(2) * mass),
    )
    checks.check(
        "accepted BPS convention carries the load-bearing pi-squared conversion",
        matching.bps_sextic_coupling
        == coupling / (sp.sqrt(2) * sp.pi**2 * mass)
        and matching.convention_ratio == sp.pi**2,
    )
    checks.check(
        "mass-term and current-normalization mutations change the match",
        sp.simplify(
            conditional_vector_current_sextic_matching(2 * mass, coupling)
            .source_sextic_coupling
            - matching.source_sextic_coupling / 2
        )
        == 0
        and sp.simplify(
            conditional_vector_current_sextic_matching(mass, 3 * coupling)
            .source_sextic_coupling
            - 3 * matching.source_sextic_coupling
        )
        == 0,
    )

    momentum_squared = sp.symbols("q2", nonzero=True, real=True)
    expansion = low_momentum_inverse_expansion(
        sp.Matrix([[mass**2]]),
        sp.Matrix([[-momentum_squared]]),
        max_order=0,
    )
    checks.check(
        "the local inverse is only the zeroth-order kinetic-vector approximation",
        expansion.approximation == sp.Matrix([[mass**-2]])
        and expansion.left_residual == sp.Matrix([[-momentum_squared / mass**2]])
        and expansion.left_residual != sp.zeros(1),
    )
    exact_inverse = sp.simplify(1 / (mass**2 - momentum_squared))
    checks.check(
        "a nonzero derivative kernel separates the full inverse from the local term",
        sp.simplify(exact_inverse - mass**-2) != 0
        and sp.series(exact_inverse, momentum_squared, 0, 3).removeO()
        == mass**-2 + momentum_squared / mass**4 + momentum_squared**2 / mass**6,
    )

    alpha, beta = sp.symbols("alpha beta", positive=True)
    metric = u2_invariant_metric(alpha, beta)
    checks.check(
        "Pauli-half u2 generators have the displayed fundamental trace Gram",
        metric.fundamental_trace_gram == sp.eye(4) / 2,
    )
    general_solution = _u2_invariance_solution()
    g00, g33 = sp.symbols("g00 g33")
    checks.check(
        "adjoint invariance leaves independent singlet and triplet coefficients",
        general_solution
        == sp.FiniteSet((g00, 0, 0, 0, g33, 0, 0, g33, 0, g33)),
    )
    checks.check(
        "canonical u2 metric reconstructs the full single-plus-double-trace family",
        metric.invariant_gram == sp.diag(beta, alpha, alpha, alpha)
        and metric.single_trace_coefficient == 2 * alpha
        and metric.double_trace_coefficient == beta - alpha,
    )
    equal_metric = u2_invariant_metric(alpha, alpha)
    unequal_metric = u2_invariant_metric(sp.Integer(2), sp.Integer(5))
    checks.check(
        "single-trace degeneracy is a specialization rather than a group theorem",
        equal_metric.singlet_triplet_degenerate
        and equal_metric.double_trace_coefficient == 0
        and not unequal_metric.singlet_triplet_degenerate
        and unequal_metric.invariant_gram == sp.diag(5, 2, 2, 2),
    )
    checks.check(
        "the unequal u2-invariant metric is a positive exact countermodel",
        all(value.is_positive for value in unequal_metric.invariant_gram.eigenvals())
        and unequal_metric.double_trace_coefficient == 3,
    )

    mass_scale = sp.symbols("M", positive=True)
    first_family = conditional_vector_current_sextic_matching(
        mass_scale,
        sp.sqrt(2) * alpha * mass_scale,
    )
    second_family = conditional_vector_current_sextic_matching(
        7 * mass_scale,
        7 * sp.sqrt(2) * alpha * mass_scale,
    )
    checks.check(
        "one matched sextic ratio leaves vector mass and coupling separately free",
        first_family.source_sextic_coupling == alpha
        and second_family.source_sextic_coupling == alpha
        and first_family.vector_mass != second_family.vector_mass
        and first_family.current_coupling != second_family.current_coupling,
    )
    checks.check(
        "fixed accepted SU2 data permits distinct singlet sextic ratios",
        conditional_vector_current_sextic_matching(3, 2).source_sextic_coupling
        != conditional_vector_current_sextic_matching(6, 2).source_sextic_coupling,
    )

    color, decay, hls_parameter = sp.symbols("N_c F_pi a", positive=True)
    vector_mass = sp.symbols("m_V", positive=True)
    hls = conditional_hls_ksrf_matching(
        vector_mass,
        decay,
        hls_parameter=hls_parameter,
    )
    conditional_source_lambda = sp.simplify(
        (color * hls.gauge_coupling / 2)
        / (sp.sqrt(2) * vector_mass)
    )
    checks.check(
        "the source cancellation is exact only under all displayed premises",
        conditional_source_lambda
        == color / (2 * sp.sqrt(2 * hls_parameter) * decay)
        and sp.simplify(
            conditional_source_lambda.subs(hls_parameter, 2)
            - color / (4 * decay)
        )
        == 0,
    )
    checks.check(
        "the HLS parameter and singlet coupling normalization are load bearing",
        sp.simplify(
            conditional_source_lambda.subs(hls_parameter, 1)
            - conditional_source_lambda.subs(hls_parameter, 2)
        )
        != 0
        and sp.simplify(
            2 * conditional_source_lambda.subs(hls_parameter, 2)
            - color / (2 * decay)
        )
        == 0,
    )
    conditional_bps_lambda = sp.simplify(conditional_source_lambda / sp.pi**2)
    checks.check(
        "conditional physical composition must retain the accepted BPS convention",
        sp.simplify(
            conditional_bps_lambda.subs(hls_parameter, 2)
            - color / (4 * sp.pi**2 * decay)
        )
        == 0,
    )

    pion_mass = sp.symbols("m_pi", positive=True)
    conditional_mu = pion_mass * decay / 2
    source_product = sp.simplify(
        conditional_source_lambda.subs(hls_parameter, 2) * conditional_mu
    )
    accepted_product = sp.simplify(
        conditional_bps_lambda.subs(hls_parameter, 2) * conditional_mu
    )
    checks.check(
        "MK2.7 is conditional algebra and uses the source rather than accepted lambda convention",
        source_product == color * pion_mass / 8
        and accepted_product == color * pion_mass / (8 * sp.pi**2)
        and sp.simplify(source_product / accepted_product - sp.pi**2) == 0,
    )

    claims = _claim_map()
    checks.check(
        "accepted elimination theorem supplies no HLS mass coupling or current",
        "fixes no field content, source, kernel, mass, coupling" in claims["C-EFT-001"]["statement"]
        and "no HLS field content" in claims["C-EFT-001"]["statement"],
    )
    checks.check(
        "accepted vector theorem keeps KSRF and physical omega outside closure",
        "does not derive HLS field content" in claims["C-VEC-001"]["statement"]
        and "physical rho or pion" in claims["C-VEC-001"]["statement"],
    )
    checks.check(
        "accepted winding current is not a physical baryon or Nc theorem",
        "not by itself" in claims["C-TOP-002"]["statement"]
        and "physical baryon current" in claims["C-TOP-002"]["statement"]
        and "identification with N_c" in claims["C-TOP-002"]["statement"],
    )
    checks.check(
        "accepted WZW level does not identify the integer with Nc",
        "does not" in claims["C-WZW-002"]["statement"]
        and "identify k with N_c" in claims["C-WZW-002"]["statement"],
    )
    checks.check(
        "accepted BPS theorem supplies its coupling and fixes the pi-four convention",
        "sextic density lambda^2*pi^4*B0^2" in claims["C-BPS-001"]["assumptions"][3]
        and "select a potential or coupling" in claims["C-BPS-001"]["statement"],
    )

    post_delta = yaml.safe_load(
        (CAMPAIGN / "evidence/post-source-claim-delta.yaml").read_text()
    )
    checks.check(
        "post-source nonduplication selects only the novel u2 metric surface",
        post_delta["claim_decision"]["promoted_new_claims"] == ["C-VEC-002"]
        and post_delta["claim_decision"]["generic_elimination_owner"] == "C-EFT-001",
    )
    checks.check(
        "source audit preserves conditional algebra and rejects dependency overreach",
        "lambda_A=abs(g_omega)/(sqrt(2)*m_omega)" in (
            CAMPAIGN / "evidence/source-audit.yaml"
        ).read_text()
        and "accepted_N_c_equals_3" in (
            CAMPAIGN / "evidence/check-adjudication.yaml"
        ).read_text(),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
