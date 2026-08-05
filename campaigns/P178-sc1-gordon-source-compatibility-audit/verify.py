#!/usr/bin/env python3
"""Exact source-aware verifier for SC1 and proposed C-GOR-002."""

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

from substrate_framework.gordon_metric import (
    MINKOWSKI_MOSTLY_PLUS,
    gordon_metric_mostly_plus,
    transverse_profile_einstein,
)
from substrate_framework.gordon_scalar_compatibility import (
    nonzero_boost_scalar_ray_system,
    reciprocal_index_identity,
    rest_boost_scalar_conditions,
    transverse_gordon_scalar_residual,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P178-sc1-gordon-source-compatibility-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-36/"
    "bridge_SC1_gordon_coupled_overdetermined.py"
)
PINNED_HASHES = {
    SOURCE: "70799bff934f1f6986545a0bde0cb94fe016dd4b468b36614ac3e5d9bb74aec0",
    ROOT / "governance/releases/v0.129.0.yaml": (
        "0b1cb52fc82307b94a489579497524f07c52e5adba69114d199a146aa87a9227"
    ),
    CAMPAIGN / "evidence/proposal-revision-0001.yaml": (
        "6971a8a68ee866844170a917457f0d9b6af510de2820b764de91c1ce882ebfa6"
    ),
}


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_source() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SOURCE)],
        check=False,
        capture_output=True,
        text=True,
        timeout=60,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _correct_gordon_sign(candidate: object) -> bool:
    index = sp.symbols("N", positive=True)
    velocity = sp.Rational(1, 2)
    gamma = 2 / sp.sqrt(3)
    four_velocity = sp.Matrix([gamma, 0, 0, gamma * velocity])
    coefficient = sp.sympify(candidate)
    trial = MINKOWSKI_MOSTLY_PLUS + coefficient * four_velocity * four_velocity.T
    return sp.simplify(trial.det() + index**2) == 0


def main() -> int:
    checks = CheckLedger("P178-SC1-C-GOR-002")
    for path, expected in PINNED_HASHES.items():
        checks.check(
            f"pinned artifact {path.name} retains its audited bytes",
            _digest(path) == expected,
        )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "SC1 has five lexical predicates and one assertion node",
        len(source_checks) == 5
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "SC1 has no NumPy integration compatibility surface",
        compatibility.numpy_aliases == ()
        and compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    native = _run_source()
    checks.check(
        "native SC1 exits zero and executes exactly five predicates",
        native.returncode == 0
        and native.stderr == ""
        and len(re.findall(r"  PASS$", native.stdout, flags=re.MULTILINE)) == 5
        and native.stdout.count("ALL 5 CHECKS PASS") == 1,
        native.stderr[-500:],
    )
    checks.check(
        "native SC1 reproduces its source-defined vacuum solve and old witness",
        "{a: 0, b: 0, c: 0}" in native.stdout
        and "G_tt at n = 2+x, x = 0:  5/6" in native.stdout
        and "{a: 0, b: c/3}" in native.stdout,
    )

    index = sp.symbols("N", positive=True)
    checks.check(
        "SC1 executes the unaccepted copied-sign Gordon coefficient",
        "g_contra = eta_inv + (nx**2 - 1)" in source_text
        and "G_tt_at0 == sp.Rational(5, 6)" in source_text,
    )
    checks.mutation_sensitive(
        "the mostly-plus Gordon coefficient sign is load bearing",
        _correct_gordon_sign,
        1 - index**2,
        [index**2 - 1, 1 + index**2, sp.Integer(0)],
    )
    old_metric = MINKOWSKI_MOSTLY_PLUS + (index**2 - 1) * sp.Matrix(
        [2 / sp.sqrt(3), 0, 0, 1 / sp.sqrt(3)]
    ) * sp.Matrix([2 / sp.sqrt(3), 0, 0, 1 / sp.sqrt(3)]).T
    checks.check(
        "the source-sign determinant has the spurious positive-index pole",
        sp.simplify(old_metric.det() - (index**2 - 2)) == 0
        and all(value.is_positive is True for value in old_metric.subs(index, 2).eigenvals()),
    )

    x = sp.symbols("x", real=True)
    profile = sp.Function("n", positive=True)(x)
    correct_geometry = transverse_profile_einstein(profile, x, sp.Rational(1, 2))
    witness = {
        profile: 2,
        sp.diff(profile, x): 1,
        sp.diff(profile, x, 2): 0,
    }
    correct_witness = correct_geometry.einstein_covariant.applyfunc(
        lambda entry: sp.simplify(entry.subs(witness))
    )
    checks.check(
        "accepted C-GOR-001 gives one sixth while SC1 guards five sixths",
        correct_witness[0, 0] == sp.Rational(1, 6)
        and correct_witness[0, 0] != sp.Rational(5, 6)
        and "matches_G2_value = (G_tt_at0 == sp.Rational(5, 6))" in source_text,
    )

    checks.check(
        "SC1 uses the opposite potential sign from canonical C-STG-001",
        "Brack = sp.Rational(1, 2) * Kin - (1 - sp.cos(U))" in source_text,
    )
    checks.check(
        "SC1 omits the independent tx component equation",
        "cond_tx" not in source_text
        and "T[0, 1]" not in source_text
        and "T[1, 0]" not in source_text,
    )

    rapidity_coordinate = sp.symbols("r", real=True, nonzero=True)
    velocity = rapidity_coordinate / sp.sqrt(1 + rapidity_coordinate**2)
    ray = nonzero_boost_scalar_ray_system(index, velocity)
    expected_minor = 8 * index**2 * rapidity_coordinate**2 * sp.sqrt(
        1 + rapidity_coordinate**2
    )
    checks.check(
        "the accepted nonzero-boost ray system has exact rank three",
        ray.coefficient_matrix.shape == (4, 3)
        and ray.diagnostics.coefficient_rank == 3
        and ray.diagnostics.augmented_rank == 3
        and ray.diagnostics.unique
        and ray.diagnostics.overdetermined_by_count,
    )
    checks.check(
        "the declared rapidity-normalized minor is nonzero",
        sp.simplify(ray.first_three_minor - expected_minor) == 0
        and ray.first_three_minor.is_zero is False,
    )
    nonzero_solution = sp.solve(
        ray.ray_conditions,
        [ray.temporal_square, ray.transverse_square, ray.potential],
        dict=True,
    )
    vacuum = {
        ray.temporal_square: 0,
        ray.transverse_square: 0,
        ray.potential: 0,
    }
    checks.check(
        "all four accepted ray conditions have the unique zero jet solution",
        nonzero_solution == [vacuum]
        and all(sp.simplify(condition.subs(vacuum)) == 0 for condition in ray.ray_conditions),
    )
    relaxed_solution = sp.solve(
        ray.ray_conditions[1:],
        [ray.temporal_square, ray.transverse_square, ray.potential],
        dict=True,
    )
    checks.check(
        "dropping xx reopens only a negative-potential algebraic branch",
        len(relaxed_solution) == 1
        and relaxed_solution[0][ray.temporal_square] == 0
        and sp.simplify(
            relaxed_solution[0][ray.transverse_square] + 2 * ray.potential
        )
        == 0,
    )
    theta = sp.symbols("theta", real=True)
    cosine_potential = 2 * sp.sin(theta / 2) ** 2
    checks.check(
        "the normalized nonnegative cosine potential removes that relaxed branch",
        ray.transverse_square.is_nonnegative is True
        and sp.simplify(1 - sp.cos(theta) - cosine_potential) == 0
        and cosine_potential.is_nonnegative is True
        and (ray.transverse_square + 2 * cosine_potential).is_nonnegative is True,
    )

    rest = rest_boost_scalar_conditions(index)
    checks.check(
        "the rest branch retains both zero tt and zero xx equations",
        rest.tt_zero_condition
        == index**2 * rest.temporal_square + rest.transverse_square + 2 * rest.potential
        and rest.xx_zero_condition
        == index**2 * rest.temporal_square + rest.transverse_square - 2 * rest.potential,
    )
    checks.check(
        "rest equations isolate the potential and a sum of real squares",
        rest.potential_condition == rest.potential
        and rest.square_sum_condition
        == index**2 * rest.temporal_square + rest.transverse_square
        and rest.temporal_square.is_nonnegative is True
        and rest.transverse_square.is_nonnegative is True,
    )
    checks.check(
        "rest sum-of-squares mutations cannot masquerade as vacuum",
        rest.square_sum_condition.subs(
            {rest.temporal_square: 0, rest.transverse_square: 0}
        )
        == 0
        and rest.square_sum_condition.subs(
            {rest.temporal_square: 1, rest.transverse_square: 0}
        )
        != 0
        and rest.square_sum_condition.subs(
            {rest.temporal_square: 0, rest.transverse_square: 1}
        )
        != 0,
    )
    rest_geometry = transverse_gordon_scalar_residual(
        sp.exp(x),
        x,
        0,
        0,
        0,
        0,
        sp.symbols("kappa_rest", positive=True),
    )
    checks.check(
        "rest geometry retains yy and zz kernel equations after scalar vacuum",
        rest_geometry.geometry.curvature_kernel == -1
        and rest_geometry.geometry.einstein_covariant[0, 0] == 0
        and rest_geometry.geometry.einstein_covariant[1, 1] == 0
        and rest_geometry.geometry.einstein_covariant[2, 2] == 1
        and rest_geometry.geometry.einstein_covariant[3, 3] == 1
        and rest_geometry.residual_covariant != sp.zeros(4),
    )

    positive_x = sp.symbols("x_positive", positive=True)
    slope, intercept, coupling = sp.symbols("A B kappa", positive=True)
    reciprocal_affine = 1 / (slope * positive_x + intercept)
    locus = transverse_gordon_scalar_residual(
        reciprocal_affine,
        positive_x,
        sp.Rational(1, 2),
        0,
        0,
        0,
        coupling,
    )
    checks.check(
        "reciprocal-affine positive index is a complete zero-residual witness",
        locus.geometry.curvature_kernel == 0
        and locus.stress.covariant == sp.zeros(4)
        and locus.residual_covariant == sp.zeros(4),
    )
    identity = reciprocal_index_identity(profile, x)
    checks.check(
        "the curvature kernel vanishes exactly with reciprocal second derivative",
        identity.identity_residual == 0
        and sp.simplify(
            identity.reciprocal_second_derivative
            + identity.curvature_kernel / profile
        )
        == 0,
    )
    nonflat = transverse_gordon_scalar_residual(
        sp.exp(x),
        x,
        sp.Rational(1, 2),
        0,
        0,
        0,
        coupling,
    )
    checks.check(
        "a nonzero curvature-kernel mutation fails the zero-stress equation",
        nonflat.geometry.curvature_kernel == -1
        and nonflat.stress.covariant == sp.zeros(4)
        and nonflat.residual_covariant != sp.zeros(4),
    )

    temporal, transverse, potential = sp.symbols("p q V", positive=True)
    loaded = transverse_gordon_scalar_residual(
        sp.exp(x),
        x,
        sp.Rational(1, 2),
        temporal,
        transverse,
        potential,
        coupling,
    )
    checks.check(
        "the omitted tx equation is sensitive to two active derivatives",
        loaded.geometry.einstein_covariant[0, 1] == 0
        and loaded.stress.covariant[0, 1] == temporal * transverse
        and loaded.residual_covariant[0, 1] == -coupling * temporal * transverse,
    )
    zero_gradient = transverse_gordon_scalar_residual(
        sp.exp(x),
        x,
        sp.Rational(1, 2),
        0,
        0,
        potential,
        coupling,
    )
    metric = zero_gradient.geometry.metric.covariant
    checks.check(
        "canonical and SC1 potential signs give opposite zero-gradient stresses",
        (zero_gradient.stress.covariant + metric * potential).applyfunc(sp.simplify)
        == sp.zeros(4)
        and (metric * potential - zero_gradient.stress.covariant).applyfunc(sp.simplify)
        != sp.zeros(4),
    )

    integer = sp.symbols("m", integer=True)
    scalar_value = 2 * sp.pi * integer
    checks.check(
        "the declared cosine-potential locus is an on-shell scalar vacuum",
        sp.simplify(1 - sp.cos(scalar_value)) == 0
        and sp.simplify(sp.sin(scalar_value)) == 0,
    )
    symbolic_result = transverse_profile_einstein(profile, x, velocity)
    checks.check(
        "simplified subluminal margin admits the exact symbolic parametrization",
        symbolic_result.gamma_squared == 1 + rapidity_coordinate**2
        and sp.simplify(1 - symbolic_result.velocity**2)
        == 1 / (1 + rapidity_coordinate**2),
    )

    base = yaml.safe_load(
        (ROOT / "governance/releases/v0.129.0.yaml").read_text(encoding="utf-8")
    )
    checks.check(
        "C-GOR-002 was collision free at the frozen v0.129.0 boundary",
        "C-GOR-002" not in base["accepted_claims"],
    )
    checks.check(
        "SC1 overreaches from its old objects to canonical closure and SC2 authority",
        re.search(r"the G3\s+route, which SC2 solves", native.stdout) is not None
        and "No non-vacuum self-consistent static Gordon configuration exists" in source_text
        and "fully inhomogeneous" in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
