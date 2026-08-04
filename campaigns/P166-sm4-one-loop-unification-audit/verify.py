"""Primary exact composition and source-semantic verifier for P166/SM4."""

from __future__ import annotations

import ast
import hashlib
import math
import os
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.renormalization import (
    diagnose_affine_unification,
    rescale_abelian_inverse_coordinate,
    shift_affine_reference,
)
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P166-sm4-one-loop-unification-audit")
SM4 = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-9/"
    "bridge_SM4_coupling_running_unification.py"
)
DOSSIER = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-9/dossiers/SM4-dossier.md"
)
SM4_SHA = "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac"
DOSSIER_SHA = "8e081707f631dfbe0b7f0c530971457871a7aa51cef6ffc77296af8e2107d9f2"
FREEZE_SHA = "cc945c7eedb8bdf10db50f84f7ebc07004b759b8ed6bfe184683b1203bfabc16"


def _check_calls(tree: ast.AST) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]


def _source_data() -> tuple[sp.Expr, tuple[sp.Expr, ...], tuple[sp.Expr, ...]]:
    reference = sp.Rational(227969, 2500)
    electromagnetic_inverse = sp.Rational(2559, 20)
    weak_coordinate = sp.Rational(11561, 50000)
    strong_coupling = sp.Rational(1181, 10000)
    inverse = (
        sp.Rational(3, 5) * (1 - weak_coordinate) * electromagnetic_inverse,
        weak_coordinate * electromagnetic_inverse,
        1 / strong_coupling,
    )
    beta = (sp.Rational(41, 10), -sp.Rational(19, 6), sp.Integer(-7))
    return reference, inverse, beta


def main() -> int:
    checks = CheckLedger("SM4-ONE-LOOP-UNIFICATION-AUDIT")
    source_bytes = SM4.read_bytes()
    dossier_bytes = DOSSIER.read_bytes()
    checks.check("SM4 source bytes are hash pinned", hashlib.sha256(source_bytes).hexdigest() == SM4_SHA)
    checks.check("SM4 dossier bytes are hash pinned", hashlib.sha256(dossier_bytes).hexdigest() == DOSSIER_SHA)
    checks.check(
        "candidate contract remains byte frozen",
        hashlib.sha256((CAMPAIGN / "proposal.yaml").read_bytes()).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "immutable preregistration remains byte identical",
        hashlib.sha256((CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA,
    )

    text = source_bytes.decode("utf-8")
    tree = ast.parse(text)
    checks.check("SM4 contains eight static check-call sites", len(_check_calls(tree)) == 8)
    checks.check(
        "SM4 contains one assertion node inside its local check helper",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check("SM4's executable import inventory is exact", imports == {"math", "numpy", "sympy"})
    checks.check(
        "SM4 has no direct imported or dynamic source dependency",
        not any(isinstance(node, (ast.ImportFrom,)) for node in ast.walk(tree))
        and all(token not in text for token in ("importlib", "runpy", "exec(", "eval(")),
    )
    checks.check(
        "SM4 has no legacy or current numerical-integration call",
        all(token not in text for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")),
    )
    checks.check(
        "the claimed QCD3 reuse is a local restatement rather than an executable import",
        "b0_qcd3 = c_gauge * C_A - c_matter * T_F * n_f_sym" in text
        and "C_A = 3" in text
        and "T_F = sp.Rational(1, 2)" in text
        and imports == {"math", "numpy", "sympy"},
    )
    checks.check(
        "the U1 and SU2 coefficients and all low-scale coordinates are locally supplied",
        "b1 = sp.Rational(41, 10)" in text
        and "b2 = sp.Rational(-19, 6)" in text
        and "MZ = 91.1876" in text
        and "ALPHA_EM_INV = 127.95" in text
        and "SIN2_THETA_W = 0.23122" in text
        and "ALPHA_S = 0.1181" in text,
    )

    process = subprocess.run(
        [sys.executable, str(SM4)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    checks.check("SM4 executes natively with a clean exit", process.returncode == 0)
    checks.check("SM4 executes exactly eight predicates", process.stdout.count("  PASS\n") == 8)
    checks.check("SM4 emits its terminal tally", "ALL 8 CHECKS PASS" in process.stdout)

    reference, inverse, beta = _source_data()
    checks.check(
        "source decimal strings exactize to three positive inverse couplings",
        inverse
        == (
            sp.Rational(295096203, 5000000),
            sp.Rational(29584599, 1000000),
            sp.Rational(10000, 1181),
        )
        and all(value > 0 for value in inverse),
    )
    checks.check(
        "the accepted coefficient vector matches the source sign convention",
        beta == (sp.Rational(41, 10), -sp.Rational(19, 6), -7)
        and tuple(-value for value in beta) == (-sp.Rational(41, 10), sp.Rational(19, 6), 7),
    )
    checks.check(
        "the conditional SU3 specialization gives b3=-b0=-7",
        sp.Rational(11, 3) * 3 - sp.Rational(4, 3) * sp.Rational(1, 2) * 6 == 7
        and beta[2] == -7,
    )
    checks.check(
        "the exact inverse-coupling derivatives have the stated signs",
        -beta[0] < 0 and -beta[1] > 0 and -beta[2] > 0,
    )

    diagnostics = diagnose_affine_unification(
        inverse,
        beta,
        provenance=("U1", "SU2", "SU3"),
    )
    checks.check(
        "accepted exact diagnostics find rank-two augmented-rank-three inconsistency",
        diagnostics.linear.coefficient_rank == 2
        and diagnostics.linear.augmented_rank == 3
        and not diagnostics.linear.consistent,
    )
    checks.check(
        "the exact left-null compatibility residual is nonzero",
        diagnostics.compatibility_residuals
        == (sp.Rational(-719562920219, 128729000000),),
    )
    crossings = tuple(item.coordinate for item in diagnostics.pairwise_crossings)
    checks.check(
        "all three source pairs have unique exact crossing coordinates",
        all(item.status == "unique" for item in diagnostics.pairwise_crossings)
        and crossings
        == (
            sp.Rational(55189953, 13625000),
            sp.Rational(298508615743, 65545500000),
            sp.Rational(74818234257, 13581500000),
        ),
    )
    checks.check("the exact crossings are strictly ordered and unequal", crossings[0] < crossings[1] < crossings[2])
    log_scales = tuple(
        sp.log(reference) / sp.log(10) + 2 * sp.pi * coordinate / sp.log(10)
        for coordinate in crossings
    )
    expected_logs = (13.0131272486722, 14.3872754728285, 16.9921825412292)
    checks.check(
        "evaluating the exact scales reproduces the source crossing table",
        all(abs(float(sp.N(value, 16)) - expected) < 1.0e-12 for value, expected in zip(log_scales, expected_logs, strict=True)),
    )
    spread = sp.simplify(2 * sp.pi * (crossings[-1] - crossings[0]) / sp.log(10))
    checks.check(
        "the exact supplied-data spread evaluates to 3.979055 decades",
        crossings[-1] - crossings[0] == sp.Rational(2158688760657, 1480383500000)
        and abs(float(sp.N(spread, 16)) - 3.97905529255705) < 1.0e-13,
    )
    checks.check(
        "the source's three-order near-miss threshold is a declared classifier rather than an identity",
        "near_miss = bool(spread > 3.0)" in text and float(sp.N(spread, 16)) > 3.0,
    )
    checks.check(
        "the headline check bundles an unrelated MSSM-window stand-in",
        "near_miss and not_coincident and spread > 3.0 and mssm_in_window" in text
        and "mssm_in_window" not in text[: text.index("mssm_scale_log10")],
    )

    equal = diagnose_affine_unification(
        inverse,
        (sp.Integer(2),) * 3,
        provenance=("U1", "SU2", "SU3"),
    )
    checks.check(
        "all-equal slopes give three parallel-disjoint pairs for unequal inputs",
        equal.linear.coefficient_rank == 1
        and equal.linear.augmented_rank == 2
        and all(item.status == "parallel_disjoint" for item in equal.pairwise_crossings),
    )
    coincident = diagnose_affine_unification(
        (sp.Integer(5),) * 3,
        (sp.Integer(2),) * 3,
        provenance=("one", "two", "three"),
    )
    checks.check(
        "the source's equal-slope guard omits the distinct coincident branch",
        coincident.linear.consistent
        and all(item.status == "coincident" for item in coincident.pairwise_crossings),
    )
    flipped = tuple((*beta[:2], sp.Integer(7)))
    checks.check(
        "flipping b3 exactly reverses the SU3 derivative sign",
        -beta[2] > 0 and -flipped[2] < 0,
    )
    checks.check(
        "the source sign guard leaves its sampled inverse coupling outside the positive domain",
        "a3^-1(UV)={a3_flip_UV:.2f}" in text and float(inverse[2] - 7 * 40 / (2 * sp.pi)) < 0,
    )

    delta = sp.symbols("delta", real=True)
    shifted = shift_affine_reference(inverse, beta, delta)
    shifted_diagnostics = diagnose_affine_unification(
        shifted,
        beta,
        provenance=("U1", "SU2", "SU3"),
    )
    checks.check(
        "a common affine reference shift preserves inconsistency and shifts every crossing together",
        not shifted_diagnostics.linear.consistent
        and all(
            sp.simplify(new.coordinate - old + delta) == 0
            for new, old in zip(shifted_diagnostics.pairwise_crossings, crossings, strict=True)
        ),
    )
    scale_factor = sp.symbols("k", positive=True)
    checks.check(
        "reference-scale rescaling moves every absolute scale but preserves the spread",
        all(
            sp.simplify(
                sp.log(scale_factor * reference * sp.exp(2 * sp.pi * value))
                - sp.log(reference * sp.exp(2 * sp.pi * value))
                - sp.log(scale_factor)
            )
            == 0
            for value in crossings
        ),
    )

    weight = sp.Rational(5, 3)
    new_a1, new_b1, new_weight = rescale_abelian_inverse_coordinate(
        inverse[0], beta[0], weight, 2
    )
    checks.check(
        "paired Abelian rescaling preserves the electromagnetic input row",
        sp.simplify(new_weight * new_a1 + inverse[1] - (weight * inverse[0] + inverse[1])) == 0,
    )
    checks.check(
        "that coordinate change does not preserve an unqualified cross-factor equality",
        new_a1 != inverse[0] and new_b1 != beta[0],
    )

    common, run = sp.symbols("common run", real=True)
    offsets = tuple(sp.simplify(common + run * coefficient - value) for value, coefficient in zip(inverse, beta, strict=True))
    repaired = tuple(sp.simplify(value + offset) for value, offset in zip(inverse, offsets, strict=True))
    repaired_diagnostics = diagnose_affine_unification(
        repaired,
        beta,
        provenance=("U1", "SU2", "SU3"),
    )
    checks.check(
        "independent matching offsets can realize an arbitrary common intersection",
        repaired == tuple(sp.simplify(common + run * coefficient) for coefficient in beta)
        and repaired_diagnostics.linear.consistent
        and repaired_diagnostics.common_inverse_coupling == common
        and repaired_diagnostics.running_coordinate == run,
    )

    weak_symbol = sp.symbols("weak", real=True)
    mutated_inverse = (
        sp.Rational(3, 5) * (1 - weak_symbol) * sp.Rational(2559, 20),
        weak_symbol * sp.Rational(2559, 20),
        inverse[2],
    )
    mutated_residual = diagnose_affine_unification(
        mutated_inverse,
        beta,
        provenance=("U1", "SU2", "SU3"),
    ).compatibility_residuals[0]
    checks.check(
        "the supplied weak coordinate is load bearing for the compatibility verdict",
        weak_symbol in mutated_residual.free_symbols and sp.diff(mutated_residual, weak_symbol) != 0,
    )
    checks.check(
        "the exact composition is the strongest supported positive object",
        not diagnostics.linear.consistent
        and len(crossings) == 3
        and float(sp.N(spread, 16)) > 3
        and repaired_diagnostics.linear.consistent,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
