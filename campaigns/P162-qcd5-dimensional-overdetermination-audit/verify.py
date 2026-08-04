#!/usr/bin/env python3
"""Exact source-aware verifier for the QCD5 accepted-composition decision."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.linear_systems import diagnose_linear_system
from substrate_framework.momentum_kernels import riesz_radial_force_law
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su3 import fundamental_generators
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P162-qcd5-dimensional-overdetermination-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-8/"
    "bridge_QCD5_d3_overdetermination.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
CHECK_ADJUDICATION = CAMPAIGN / "evidence/check-adjudication.yaml"
SOURCE_SHA256 = "60a2f5b8dbd76f3b4d6b0a48e4fcd5ed9edbc6a4e1d3869cb4a40bf30c87084c"
FROZEN_SHA256 = "58897a865cd86ea174e0f8ec1210fa23aa756e2fd37d7cc8107892760784c539"
REVISION_SHA256 = "e306e5d63dcaa5050365634d27d531f6942e245d32c93cbfb8acd234aa4bdeb3"
REPRODUCTION_SHA256 = "25e8b6e6d6656dcd92dd5f2f4c20faa319c01855ae0f87708f0abcd02d393064"
SOURCE_AUDIT_SHA256 = "6ae713cb620c3f5e3b0c78c506b4f760d85bf2f83c95ce678af5b520df844db9"
CHECK_ADJUDICATION_SHA256 = (
    "f698db4763414be519c7262f17b40c63348c0e37fb4de93b2ab01376cf13b604"
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _radial_exponent(expression: sp.Expr, radius: sp.Symbol) -> sp.Expr:
    return sp.simplify(radius * sp.diff(sp.log(expression), radius))


def run() -> int:
    checks = CheckLedger("P162/QCD5")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned QCD5 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial frozen proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
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
    rank_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in {"rank", "nullspace", "rref"}
    ]
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check("seven source predicates", len(source_checks) == 7)
    checks.check("one source assertion", len(source_assertions) == 1)
    checks.check(
        "QCD5 has no NumPy integration compatibility surface",
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
    checks.check("native QCD5 exits cleanly", native.returncode == 0)
    checks.check(
        "native QCD5 terminal tally is exact",
        native_lines.count("ALL 7 CHECKS PASS") == 1,
    )

    generators = fundamental_generators()
    trace_metric = sp.Matrix(
        8,
        8,
        lambda first, second: sp.trace(generators[first] * generators[second]),
    )
    checks.check(
        "QCD5 zero is the accepted SU3 trace duplicate",
        trace_metric == sp.eye(8) / 2,
    )

    radius = sp.symbols("r", positive=True)
    source_strength, probe_strength = sp.symbols("Q q", nonzero=True, real=True)
    fixed_force = riesz_radial_force_law(
        3, 1, radius, source_strength, probe_strength
    )
    fractional_force = riesz_radial_force_law(
        sp.Rational(5, 2),
        sp.Rational(3, 4),
        radius,
        source_strength,
        probe_strength,
    )
    checks.check(
        "accepted Riesz composition gives the inverse-square family",
        fixed_force.force_radial_power == -2
        and fixed_force.inverse_square_dimension_family == 3
        and fractional_force.force_radial_power == -2
        and fractional_force.inverse_square_dimension_family == sp.Rational(5, 2),
    )
    checks.check(
        "the supplied endpoint selects only a family member",
        fixed_force.inverse_square_residual == 0
        and fractional_force.inverse_square_residual == 0
        and fixed_force.kernel.laplacian_power
        != fractional_force.kernel.laplacian_power,
    )

    fixed_matrix = [[1], [1], [1]]
    fixed_rhs = [3, 3, 3]
    fixed = diagnose_linear_system(fixed_matrix, fixed_rhs)
    single = diagnose_linear_system([[1]], [3])
    checks.check(
        "three fixed-s copies have rank one and two row dependencies",
        fixed.equations == 3
        and fixed.unknowns == 1
        and fixed.coefficient_rank == fixed.augmented_rank == 1
        and fixed.coefficient_row_dependencies == 2,
    )
    checks.check(
        "equation-count overdetermination is not row independence",
        fixed.overdetermined_by_count
        and fixed.consistent
        and fixed.unique
        and single.consistent
        and single.unique
        and single.coefficient_rank == fixed.coefficient_rank,
    )
    d_symbol = sp.symbols("d")
    fixed_solution = sp.linsolve((sp.Matrix(fixed_matrix), sp.Matrix(fixed_rhs)), d_symbol)
    single_solution = sp.linsolve((sp.Matrix([[1]]), sp.Matrix([3])), d_symbol)
    checks.check(
        "removing duplicate sectors leaves the exact same fixed-s solution",
        fixed_solution == single_solution == {(sp.Integer(3),)},
    )

    free_matrix = [[1, -2], [1, -2], [1, -2]]
    free_rhs = [1, 1, 1]
    free = diagnose_linear_system(free_matrix, free_rhs)
    checks.check(
        "free d-s copies have rank one and one solution direction",
        free.equations == 3
        and free.unknowns == 2
        and free.coefficient_rank == free.augmented_rank == 1
        and free.solution_dimension == 1
        and free.underdetermined
        and free.coefficient_row_dependencies == 2,
    )
    checks.check(
        "free family null direction is d equals two s plus one",
        sp.Matrix(free_matrix).nullspace() == [sp.Matrix([2, 1])]
        and sp.linsolve(
            (sp.Matrix(free_matrix), sp.Matrix(free_rhs)),
            sp.symbols("d_free s_free"),
        )
        == {(2 * sp.symbols("s_free") + 1, sp.symbols("s_free"))},
    )

    amplitudes = (sp.Integer(1), sp.Rational(1, 2), sp.Rational(1, 2))
    sectors = ("U1", "SU2", "SU3")
    checks.check(
        "three labels provide only two amplitude values",
        len(sectors) == 3 and len(set(amplitudes)) == 2,
    )
    checks.check(
        "neither labels nor amplitudes enter the constraint rows",
        all([1, -2] == row for row in free_matrix)
        and free_matrix
        == [[1, -2] for _label, _amplitude in zip(sectors, amplitudes)],
    )
    inconsistent = diagnose_linear_system(
        [[1], [1]], [sp.Integer(3), sp.Rational(5, 2)]
    )
    checks.check(
        "different supplied endpoints make repeated shared-d rows inconsistent",
        inconsistent.coefficient_rank == 1
        and inconsistent.augmented_rank == 2
        and not inconsistent.consistent
        and inconsistent.solution_dimension is None,
    )

    dimension, power, alpha = sp.symbols("d s alpha", positive=True)
    kappa_dimension = dimension**2
    dimension_weighted = kappa_dimension * radius ** (2 * power - dimension)
    dimension_weighted_force = -sp.diff(dimension_weighted, radius)
    checks.check(
        "dimension-dependent amplitude leaves the radial exponents unchanged",
        _radial_exponent(dimension_weighted, radius) == 2 * power - dimension
        and _radial_exponent(dimension_weighted_force, radius)
        == 2 * power - dimension - 1,
    )
    radial_weighted = radius**alpha * radius ** (2 * power - dimension)
    checks.check(
        "a genuinely radial mutation changes the displayed constraint",
        _radial_exponent(radial_weighted, radius)
        == alpha + 2 * power - dimension,
    )
    checks.check(
        "QCD5 guard b tests an off-target dimension derivative",
        "dd_logG = sp.simplify(sp.diff(sp.log(G), d_sym))" in source_text
        and "the r-power exponent is STILL 2s-d" in source_text,
    )

    checks.check(
        "QCD5 substitutes count for rank",
        not rank_calls
        and "over_determined = n_constraints > n_unknowns" in source_text
        and "n_constraints = len(system)" in source_text,
    )
    checks.check(
        "QCD5 explicitly constructs all simultaneous equations from one function",
        "system = [sp.Eq(force_exp_shared(k), -2) for _, k in SECTORS]"
        in source_text,
    )
    checks.check(
        "QCD5 conditionality witness is load bearing",
        "d_at_s34 = shared_d_given_s(sp.Rational(3, 4))" in source_text
        and fractional_force.inverse_square_dimension_family == sp.Rational(5, 2),
    )
    checks.check(
        "QCD5 absence verdict is a literal assertion rather than a derivation",
        "no_sg_derivation_of_s = True" in source_text,
    )
    checks.check(
        "QCD5 carries both the original ceiling and a retroactive closure annotation",
        "QCD5 does NOT derive s=1" in source_text
        and "SUBSEQUENTLY RESOLVED by Phase 19 / D3S" in source_text,
    )

    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in CAMPAIGN.rglob("*.py")
    ]
    checks.check(
        "mutable P162 has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )
    checks.check(
        "mutable P162 has no eager legacy fallback",
        all(item.eager_legacy_default_fallbacks == 0 for item in mutable_compatibility),
    )
    return checks.finish()


if __name__ == "__main__":
    result = run()
    print(f"P162 PRIMARY ALL {result} CHECKS PASS")
