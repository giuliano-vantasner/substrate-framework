#!/usr/bin/env python3
"""Exact error, premise, finite-probe, comparator, and formal audit of KI5."""

from __future__ import annotations

import ast
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import sympy as sp
import yaml

from substrate_framework.energy_differences import normalized_linear_difference
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / "merged-framework/bridges/phase-34/bridge_KI5_kappa_is_not_a_variational_bound.py"
DOSSIER = SOURCE_ROOT / "merged-framework/bridges/phase-34/dossiers/Phase34-KI-dossier.md"
LEAN = SOURCE_ROOT / "merged-framework/bridges/phase-34/lean/Phase34KIKernel.lean"
PINNED_HASHES = {
    SOURCE: "5db475be67e6668f9064096055b0452bb2a762c435132ae324896cce3f9863fe",
    DOSSIER: "e01fbee40d81ebae1fc6f9452c321e2914cb185cdf257ae226d849ea6392702b",
    LEAN: "269c2b6b023fb1bfacb7dede2e708f09d3e08cad00bcc933e5149357ef5870f5",
    ROOT / "governance/releases/current.yaml": "d530afe41d0e88e3236c0f048a1352394028006f9217ed8019b6fdd30f4f7cb6",
    ROOT / "governance/claims.yaml": "b2d68ae4e293301d402de4a0292445805ff42e26871b058fc74427aac37b7a0f",
    ROOT / "src/substrate_framework/energy_differences.py": "ad9f82d978eb95e2c33321ea400de82facd69b7d7fed6260bc56becaae8c1b3c",
    ROOT / "campaigns/P105-e2-rational-map-radial-profiles/adjudication.yaml": "4bf1c967953b78711d1e43b6b809f62dadb8cc424f88292d7635051871e6ceb3",
    ROOT / "campaigns/P106-e3-conditional-energy-difference-audit/adjudication.yaml": "b3cbb2510b98f5520ab547ba8fa7da7ca6ec7bc8574dbfefee3bd953698b5b7c",
    ROOT / "campaigns/P105-e2-rational-map-radial-profiles/attempts/0006/result.yaml": "33e58ec644a0181c9395b20fe171dbd5a612b533b9e24f696f99cb859be375f6",
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_source() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SOURCE)], check=False, capture_output=True, text=True,
        timeout=120, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _source_comparator_predicate(comparator: object) -> bool:
    optimal = sp.Rational(84574, 10000)
    degraded_b4 = sp.Rational(78468, 10000)
    target = sp.sympify(comparator)
    return bool(
        abs(degraded_b4 - target) < abs(optimal - target)
        and degraded_b4 / target > 5
    )


def _identity_for_final_sign(final_sign: object) -> bool:
    n, alpha, true_i, true_f, delta_i, delta_f = sp.symbols(
        "n alpha true_i true_f delta_i delta_f", real=True,
    )
    sign = sp.sympify(final_sign)
    estimate = alpha * (n * (true_i + delta_i) + sign * (true_f + delta_f))
    truth = alpha * (n * true_i + sign * true_f)
    return sp.simplify(estimate - truth - alpha * (n * delta_i - delta_f)) == 0


def main() -> int:
    checks = CheckLedger("P175-KI5-VARIATIONAL-BOUND-AUDIT")
    for path, expected in PINNED_HASHES.items():
        checks.check(f"pinned artifact {path.name} retains its audited bytes", _digest(path) == expected)

    text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(SOURCE))
    calls = sorted(
        (
            node for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    labels = [re.match(r"(KI5\.[1-5])", ast.literal_eval(node.args[0])).group(1) for node in calls]
    checks.check("KI5 has exactly five advertised predicates in order", labels == [f"KI5.{i}" for i in range(1, 6)])
    checks.check(
        "KI5 has one assertion and the advertised NumPy SymPy SciPy imports",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1
        and "import numpy as np" in text and "import sympy as sp" in text
        and "from scipy.integrate import solve_bvp" in text,
    )
    compatibility = audit_numpy_trapezoid_compatibility(text, filename=str(SOURCE))
    checks.check(
        "immutable KI5 uses a lazy current-first integration alias without an eager legacy default",
        compatibility.numpy_aliases == ("np",)
        and compatibility.current_references == 1
        and compatibility.legacy_references == 1
        and compatibility.eager_legacy_default_fallbacks == 0
        and 'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in text,
    )
    replay = _run_source()
    checks.check(
        "native current-NumPy KI5 executes all five predicates and terminal tally",
        replay.returncode == 0 and replay.stderr == ""
        and replay.stdout.count("  PASS\n") == 5
        and "ALL 5 CHECKS PASS" in replay.stdout,
        replay.stderr[-500:],
    )

    n, alpha = sp.symbols("n alpha", positive=True)
    true_i, true_f = sp.symbols("true_i true_f", real=True)
    delta_i, delta_f = sp.symbols("delta_i delta_f", nonnegative=True)
    estimated = alpha * (n * (true_i + delta_i) - (true_f + delta_f))
    truth = alpha * (n * true_i - true_f)
    propagated = sp.simplify(estimated - truth)
    checks.check(
        "the general signed upper-estimate error is exact",
        propagated == alpha * (n * delta_i - delta_f),
    )
    checks.mutation_sensitive(
        "the final subtraction sign is load bearing",
        _identity_for_final_sign,
        -1,
        [1],
    )
    checks.check(
        "the canonical accepted API evaluates the unnormalized slack combination",
        normalized_linear_difference(1.0, 0.1, multiplicity=2) > 0
        and normalized_linear_difference(0.1, 1.0, multiplicity=2) < 0,
    )
    checks.check(
        "independent nonnegative slacks place the estimate on both sides of truth",
        propagated.subs({n: 2, alpha: 1, delta_i: 1, delta_f: 0}) > 0
        and propagated.subs({n: 2, alpha: 1, delta_i: 0, delta_f: 1}) < 0,
    )
    checks.check(
        "a correlated slack relation gives the exact one-sided conditions",
        sp.simplify(propagated.subs(delta_f, n * delta_i)) == 0
        and propagated.subs({n: 2, alpha: 1, delta_i: 1, delta_f: 3}) < 0
        and propagated.subs({n: 2, alpha: 1, delta_i: 2, delta_f: 3}) > 0,
    )
    eps_i, eps_f = sp.symbols("eps_i eps_f", nonnegative=True)
    checks.check(
        "componentwise error budgets imply a two-sided difference interval",
        sp.simplify(alpha * (n * eps_i + eps_f) - alpha * (n * eps_i - eps_f))
        == 2 * alpha * eps_f,
    )
    alternating = [
        (sp.Rational(1, k), sp.Rational(0)) if k % 2 == 0
        else (sp.Rational(0), sp.Rational(1, k))
        for k in range(2, 10)
    ]
    alternating_errors = [2 * first - final for first, final in alternating]
    checks.check(
        "convergent upper estimates can approach the true difference from alternating sides",
        all(first >= 0 and final >= 0 for first, final in alternating)
        and all(abs(error) <= sp.Rational(2, k) for k, error in zip(range(2, 10), alternating_errors, strict=True))
        and any(error > 0 for error in alternating_errors)
        and any(error < 0 for error in alternating_errors),
    )

    scale = sp.symbols("scale", real=True)
    finite_probe_counterexample = (scale - 1) ** 2 * (
        (scale - sp.Rational(41, 40)) ** 2 - sp.Rational(1, 10000)
    )
    sampled_scales = [sp.Rational(9, 10), sp.Rational(19, 20), sp.Rational(21, 20), sp.Rational(11, 10)]
    checks.check(
        "an exact unsampled counterfamily defeats finite width-probe minimization",
        finite_probe_counterexample.subs(scale, 1) == 0
        and all(finite_probe_counterexample.subs(scale, value) > 0 for value in sampled_scales)
        and finite_probe_counterexample.subs(scale, sp.Rational(41, 40)) < 0,
    )
    checks.check(
        "KI5.2 checks only eight selected rescalings before asserting minimization",
        "for B in (2, 4):" in text
        and "for s in (0.90, 0.95, 1.05, 1.10):" in text
        and "solved profile minimises the functional" in text,
    )
    checks.check(
        "KI5 consumes solve_bvp output without a solver-success gate",
        "sol = solve_bvp" in text and "sol.sol(rr)" in text
        and not any(isinstance(node, ast.Attribute) and node.attr == "success" for node in ast.walk(tree)),
    )
    checks.check(
        "KI5 uses finite-wall Dirichlet data rather than accepted asymptotic Robin evidence",
        "ya[0] - np.pi" in text and "yb[0]" in text
        and "rmax=16.0, n0=3000, tol=1e-6" in text,
    )

    claims_data = yaml.safe_load((ROOT / "governance/claims.yaml").read_text(encoding="utf-8"))
    claims = {claim["id"]: claim for claim in claims_data["claims"]}
    checks.check(
        "C-RDIFF-001 already owns the exact separate-upper-bound ceiling",
        "Separate upper bounds" in claims["C-RDIFF-001"]["statement"]
        and "slacks enter with opposite signs" in claims["C-RDIFF-001"]["statement"]
        and "neither an upper nor a lower bound" in " ".join(claims["C-RDIFF-001"]["assumptions"]),
    )
    checks.check(
        "C-RPROF-002 supplies stationary branches but no variational bound",
        "stationary branch" in claims["C-RPROF-002"]["statement"]
        and "variational upper bound" in claims["C-RPROF-002"]["statement"]
        and "local or global minimum" in claims["C-RPROF-002"]["statement"]
        and "minimization outside the tested numerical surface"
        in " ".join(claims["C-RPROF-002"]["assumptions"]),
    )
    checks.check(
        "C-RDIFF-002 owns the corrected coordinate and rejects physical binding",
        "8.482417318795285" in claims["C-RDIFF-002"]["statement"]
        and "not a variational bound" in claims["C-RDIFF-002"]["statement"]
        and "does not establish exothermic physical binding" in " ".join(claims["C-RDIFF-002"]["assumptions"]),
    )
    accepted_numeric = yaml.safe_load(
        (ROOT / "campaigns/P105-e2-rational-map-radial-profiles/attempts/0006/result.yaml").read_text()
    )["corrected_2401_sample_results"]
    accepted_kappa = 3 * sp.pi**2 * (
        2 * sp.Float(str(accepted_numeric["B2"]["energy_coefficient"]), 30)
        - sp.Float(str(accepted_numeric["B4"]["energy_coefficient"]), 30)
    )
    checks.check(
        "KI5 reproduces stale inputs rather than the accepted conditional coordinate",
        "b(2) = 2.4154" in replay.stdout and "b(4) = 4.5452" in replay.stdout
        and abs(accepted_kappa - sp.Float("8.4574")) > sp.Rational(1, 50),
    )

    fourth_condition = ast.unparse(calls[3].args[1])
    checks.check(
        "the empirical comparator enters both KI5.4 pass predicates",
        fourth_condition == "moves_toward_emp and still_far"
        and "abs(kappa_deg4 - KAPPA_EMP) < abs(KAPPA_OPT - KAPPA_EMP)" in text
        and "(kappa_deg4 / KAPPA_EMP) > 5.0" in text,
    )
    checks.mutation_sensitive(
        "KI5.4's verdict changes when only the comparator changes",
        _source_comparator_predicate,
        sp.Rational(929, 1000),
        [sp.Rational(83, 10)],
    )
    checks.check(
        "KI5.5 hard-codes the rejected-bound verdict",
        "eight_four_six_is_a_bound = False" in text
        and "not eight_four_six_is_a_bound" in ast.unparse(calls[4].args[1]),
    )
    checks.check(
        "source convergence does not supply a full-model ansatz-error bound",
        "ansatz error at the few-percent level" in text
        and "E2's convergence checks bound the ansatz error" in text
        and "variational upper bound" in claims["C-RPROF-002"]["statement"]
        and "full three-dimensional solution" in claims["C-RPROF-002"]["statement"],
    )

    lean = LEAN.read_text(encoding="utf-8")
    checks.check(
        "Lean exactly proves positive and negative witnesses for the abstract error",
        "def kappaError (d2 d4 : ℝ) : ℝ := 2 * d2 - d4" in lean
        and "theorem kappa_error_sign_indeterminate" in lean
        and "exact ⟨1, 0" in lean and "exact ⟨0, 1" in lean,
    )
    checks.check(
        "Lean encodes no energy functional minimizer convergence or comparator premise",
        all(token not in lean for token in ("Ehat", "Functional", "minimizer", "convergesTo", "0.929")),
    )
    checks.check(
        "the unchanged Lean execution can be reused at this exact theorem scope",
        _digest(LEAN) == "269c2b6b023fb1bfacb7dede2e708f09d3e08cad00bcc933e5149357ef5870f5"
        and (ROOT / "campaigns/P172-ki2-epsilon-underdetermination-audit/attempts/0009/result.yaml").exists(),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
