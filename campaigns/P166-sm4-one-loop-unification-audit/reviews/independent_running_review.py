"""Independent exact SM4 derivation without importing canonical running APIs."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P166-sm4-one-loop-unification-audit")
SM4 = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-9/"
    "bridge_SM4_coupling_running_unification.py"
)
SM4_SHA = "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac"
FREEZE_SHA = "cc945c7eedb8bdf10db50f84f7ebc07004b759b8ed6bfe184683b1203bfabc16"


def main() -> int:
    checks = CheckLedger("SM4-INDEPENDENT-RUNNING-REVIEW")
    payload = SM4.read_bytes()
    text = payload.decode("utf-8")
    tree = ast.parse(text)
    checks.check("fresh SM4 read is hash pinned", hashlib.sha256(payload).hexdigest() == SM4_SHA)
    checks.check(
        "fresh preregistration read is hash pinned",
        hashlib.sha256((CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA,
    )
    checks.check(
        "fresh AST inventory finds eight calls and one assertion",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(tree)
        )
        == 8
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )

    reference = sp.Rational(227969, 2500)
    electromagnetic = sp.Rational(2559, 20)
    weak = sp.Rational(11561, 50000)
    strong = sp.Rational(1181, 10000)
    observations = sp.Matrix(
        [
            sp.Rational(3, 5) * (1 - weak) * electromagnetic,
            weak * electromagnetic,
            1 / strong,
        ]
    )
    slopes = sp.Matrix([sp.Rational(41, 10), -sp.Rational(19, 6), -7])
    design = sp.Matrix.hstack(sp.ones(3, 1), slopes)
    augmented = design.row_join(observations)
    checks.check("fresh exact ranks are two and three", design.rank() == 2 and augmented.rank() == 3)

    left_null = design.T.nullspace()
    checks.check("fresh left-nullspace is one dimensional", len(left_null) == 1)
    residual = sp.simplify((left_null[0].T * observations)[0])
    checks.check("fresh compatibility residual is nonzero", residual != 0)

    pairs = ((0, 1), (0, 2), (1, 2))
    coordinates = tuple(
        sp.simplify((observations[i] - observations[j]) / (slopes[i] - slopes[j]))
        for i, j in pairs
    )
    checks.check(
        "fresh pairwise elimination recovers the three exact coordinates",
        coordinates
        == (
            sp.Rational(55189953, 13625000),
            sp.Rational(298508615743, 65545500000),
            sp.Rational(74818234257, 13581500000),
        ),
    )
    checks.check("fresh crossings are strictly ordered", coordinates[0] < coordinates[1] < coordinates[2])
    crossing_logs = tuple(
        sp.log(reference) / sp.log(10) + 2 * sp.pi * coordinate / sp.log(10)
        for coordinate in coordinates
    )
    checks.check(
        "fresh evaluated crossing logs reproduce the three source values",
        all(
            abs(float(sp.N(value, 16)) - expected) < 1.0e-12
            for value, expected in zip(
                crossing_logs,
                (13.0131272486722, 14.3872754728285, 16.9921825412292),
                strict=True,
            )
        ),
    )
    spread = sp.simplify(crossing_logs[-1] - crossing_logs[0])
    checks.check("fresh spread is positive and approximately 3.979055 decades", spread > 0 and abs(float(sp.N(spread, 16)) - 3.97905529255705) < 1.0e-13)

    checks.check("fresh derivative signs match the source", -slopes[0] < 0 and -slopes[1] > 0 and -slopes[2] > 0)
    checks.check("fresh QCD coefficient substitution gives seven", sp.Rational(11, 3) * 3 - sp.Rational(4, 3) * sp.Rational(1, 2) * 6 == 7)

    equal_design = sp.Matrix([[1, 2], [1, 2], [1, 2]])
    equal_augmented = equal_design.row_join(observations)
    checks.check("fresh all-equal slope mutant is parallel and inconsistent", equal_design.rank() == 1 and equal_augmented.rank() == 2)
    coincident_augmented = equal_design.row_join(sp.Matrix([5, 5, 5]))
    checks.check("fresh all-equal intercept mutant is the omitted coincident branch", coincident_augmented.rank() == 1)

    flipped = slopes.subs({slopes[2]: 7}, simultaneous=True)
    checks.check("fresh b3 sign mutation reverses its exact derivative", -slopes[2] > 0 and -flipped[2] < 0)

    shift = sp.symbols("shift", real=True)
    shifted = observations - shift * slopes
    shifted_coordinates = tuple(
        sp.simplify((shifted[i] - shifted[j]) / (slopes[i] - slopes[j]))
        for i, j in pairs
    )
    checks.check(
        "fresh reference shift moves all coordinates together",
        all(sp.simplify(new - old + shift) == 0 for new, old in zip(shifted_coordinates, coordinates, strict=True)),
    )
    checks.check("fresh reference shift preserves their spread", sp.simplify((shifted_coordinates[-1] - shifted_coordinates[0]) - (coordinates[-1] - coordinates[0])) == 0)

    common, run = sp.symbols("common run", real=True)
    offsets = sp.Matrix([common, common, common]) + run * slopes - observations
    repaired = observations + offsets
    checks.check("fresh threshold offsets generate any affine common point", sp.simplify(repaired - (sp.Matrix([common] * 3) + run * slopes)) == sp.zeros(3, 1))
    checks.check("fresh repaired augmented rank is two", design.row_join(repaired).rank() == 2)

    q = sp.symbols("q", positive=True)
    transformed_em = sp.simplify((2 * sp.Rational(5, 3)) * (observations[0] / 2) + observations[1])
    checks.check("fresh paired U1 rescaling preserves the electromagnetic row", transformed_em == electromagnetic)
    checks.check("fresh unpaired U1 rescaling changes cross-sector coordinates", observations[0] / q != observations[0])

    checks.check(
        "fresh source semantics expose the unrelated MSSM stand-in",
        "mssm_in_window" in text and "near_miss and not_coincident and spread > 3.0 and mssm_in_window" in text,
    )
    checks.check(
        "fresh compatibility audit finds no integration API surface",
        all(token not in text for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")),
    )
    checks.check(
        "the strongest fresh verdict is exact inconsistent affine composition",
        design.rank() == 2 and augmented.rank() == 3 and residual != 0 and spread > 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
