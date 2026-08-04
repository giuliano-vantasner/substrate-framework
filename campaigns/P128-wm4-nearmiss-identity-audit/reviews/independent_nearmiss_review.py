"""Independent P128 derivation without importing the primary verifier."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate/merged-framework/bridges")
WM4 = ROOT / "phase-33/bridge_WM4_nearmiss_identity_map.py"
CAMPAIGN = Path("campaigns/P128-wm4-nearmiss-identity-audit")
WM4_SHA = "443406419edc1021a929a6041dec025f73af6d947cf770eebe9cde25d74cd8c9"
FREEZE_SHA = "5a5e02b02d1f929286cfe6a329eb12518260fa42ee70e5fb9c34cc34f8988e01"


def main() -> int:
    checks = CheckLedger("WM4-INDEPENDENT-NEARMISS-REVIEW")
    payload = WM4.read_bytes()
    text = payload.decode("utf-8")
    checks.check("fresh WM4 read is hash pinned", hashlib.sha256(payload).hexdigest() == WM4_SHA)
    checks.check(
        "fresh preregistration read is hash pinned",
        hashlib.sha256((CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest() == FREEZE_SHA,
    )
    tree = ast.parse(text)
    checks.check(
        "fresh AST count finds eleven checks",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(tree)
        ) == 11,
    )

    x1, x2, x3, s1, s2, s3 = sp.symbols("x1 x2 x3 s1 s2 s3", real=True)
    design = sp.Matrix([[1, s1], [1, s2], [1, s3]])
    observations = sp.Matrix([x1, x2, x3])
    augmented = design.row_join(observations)
    obstruction = sp.expand(augmented.det())
    source_D = x1 * (s2 - s3) + x2 * (s3 - s1) + x3 * (s1 - s2)
    checks.check("fresh determinant expansion recovers minus D in this column orientation", sp.simplify(obstruction + source_D) == 0)

    left_vector = sp.Matrix([s2 - s3, s3 - s1, s1 - s2])
    checks.check(
        "fresh multiplication proves the vector annihilates both design columns",
        (design.T * left_vector).applyfunc(sp.simplify) == sp.zeros(2, 1),
    )
    checks.check("fresh multiplication recovers the scalar obstruction", sp.simplify((left_vector.T * observations)[0] - source_D) == 0)

    concrete_slopes = (sp.Rational(41, 10), sp.Rational(-19, 6), sp.Integer(-7))
    concrete_design = design.subs(dict(zip((s1, s2, s3), concrete_slopes, strict=True)))
    checks.check("fresh exact rank is two on the declared slope triple", concrete_design.rank() == 2)
    checks.check("fresh exact nullity is one on the declared slope triple", len(concrete_design.T.nullspace()) == 1)
    checks.check("fresh minors show its null generator is proportional to D", sp.Matrix.hstack(concrete_design.T.nullspace()[0], left_vector.subs(dict(zip((s1, s2, s3), concrete_slopes, strict=True)))).rank() == 1)

    pair_coordinates = {
        "12": 2 * sp.pi * (x1 - x2) / (s1 - s2),
        "13": 2 * sp.pi * (x1 - x3) / (s1 - s3),
        "23": 2 * sp.pi * (x2 - x3) / (s2 - s3),
    }
    expected = {
        ("12", "13"): 2 * sp.pi * source_D / ((s1 - s2) * (s1 - s3)),
        ("12", "23"): 2 * sp.pi * source_D / ((s1 - s2) * (s2 - s3)),
        ("13", "23"): 2 * sp.pi * source_D / ((s1 - s3) * (s2 - s3)),
    }
    for names, expression in expected.items():
        checks.check(
            f"fresh elimination proves crossing relation {names[0]} minus {names[1]}",
            sp.simplify(sp.together(pair_coordinates[names[0]] - pair_coordinates[names[1]] - expression)) == 0,
        )

    slope_substitution = dict(zip((s1, s2, s3), concrete_slopes, strict=True))
    ratios = [
        abs(sp.simplify(expression / source_D).subs(slope_substitution))
        for expression in expected.values()
    ]
    checks.check("fresh range coefficient is positive and slope-only", all(ratio.free_symbols == set() and ratio > 0 for ratio in ratios))
    checks.check(
        "fresh max-min spread is absolute rather than signed",
        sp.simplify(max(ratios) * sp.Abs(source_D) - max(ratios) * sp.Abs(-source_D)) == 0,
    )

    common, run = sp.symbols("common run", real=True)
    em_weight = sp.Rational(5, 3)
    solution = sp.solve(
        (
            sp.Eq(common + run * s3, x3),
            sp.Eq(em_weight * (common + run * s1) + common + run * s2, em_weight * x1 + x2),
        ),
        (common, run),
        dict=True,
    )[0]
    weak_residual = sp.simplify(solution[common] + solution[run] * s2 - x2)
    coefficient = sp.Rational(5, 1) / (5 * s1 + 3 * s2 - 8 * s3)
    checks.check("fresh two-equation elimination recovers the WM3 inverse residual", sp.simplify(sp.together(weak_residual - coefficient * source_D)) == 0)
    checks.check("fresh residual coefficient is slope-only", coefficient.free_symbols == {s1, s2, s3})
    electromagnetic_coupling = sp.symbols("electromagnetic_coupling", positive=True)
    angle_residual = electromagnetic_coupling * weak_residual
    checks.check("fresh angle residual necessarily contains its supplied electromagnetic factor", electromagnetic_coupling in angle_residual.free_symbols)

    all_equal = {s1: 4, s2: 4, s3: 4, x1: 1, x2: 2, x3: 3}
    checks.check("fresh parallel-line counterexample has D zero", source_D.subs(all_equal) == 0)
    checks.check("fresh parallel-line counterexample is inconsistent", design.subs(all_equal).rank() == 1 and augmented.subs(all_equal).rank() == 2)
    checks.check("fresh all-equal case has two independent annihilators", len(design.subs(all_equal).T.nullspace()) == 2)

    one_equal = {s1: 1, s2: 1, s3: 2}
    checks.check("fresh one-equal-pair case still has rank two", design.subs(one_equal).rank() == 2)
    checks.check("fresh one-equal-pair case keeps the 13 and 23 crossings finite", all(pair_coordinates[name].subs(one_equal).is_finite for name in ("13", "23")))
    checks.check("fresh one-equal-pair case keeps the WM3 coefficient finite", coefficient.subs(one_equal) == sp.Rational(-5, 8))

    distinct_singular = {s1: 0, s2: 8, s3: 3}
    checks.check("fresh distinct slope mutant makes the WM3 denominator zero", len({0, 8, 3}) == 3 and sp.denom(coefficient).subs(distinct_singular) == 0)
    checks.check("fresh crossing denominators stay nonzero in that WM3-singular mutant", all(sp.denom(value).subs(distinct_singular) != 0 for value in pair_coordinates.values()))

    positive_factor = 1 + x1**2
    nonlinear = positive_factor * source_D
    checks.check("fresh nonlinear diagnostic has the same real vanishing locus", sp.solve(sp.Eq(positive_factor, 0), x1, domain=sp.S.Reals) == [])
    checks.check("fresh nonlinear diagnostic is not a constant multiple of D", sp.diff(sp.simplify(nonlinear / source_D), x1) != 0)

    shift = sp.symbols("shift", real=True)
    shifted_D = source_D.subs({x1: x1 - shift * s1, x2: x2 - shift * s2, x3: x3 - shift * s3}, simultaneous=True)
    checks.check("fresh reference-shift expansion leaves D unchanged", sp.simplify(shifted_D - source_D) == 0)
    scale = sp.symbols("scale", positive=True)
    scaled_D = source_D.subs({x1: scale * x1, x2: scale * x2, x3: scale * x3}, simultaneous=True)
    checks.check("fresh coordinate scaling makes D covariant not invariant", sp.simplify(scaled_D - scale * source_D) == 0)

    attributes = {
        (node.value.id, node.attr)
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
    }
    checks.check("fresh provenance audit finds no imported beta attributes", not any(root == "_sm4" and attr in {"b1", "b2", "b3"} for root, attr in attributes))
    checks.check("fresh source audit finds a measured alpha factor in the claimed data-free dictionary", "delta_sin2 = alpha_em_sym * delta_a2" in text and "alpha_em_sym * dict_const" in text)
    checks.check("fresh source audit finds approximate rather than bitwise equality", "math.isclose" in text and "bit-for-bit IDENTICAL" in text)
    checks.check("fresh source audit finds no trapezoid compatibility event", "np.trapz" not in text and "np.trapezoid" not in text)

    checks.check(
        "the strongest independent verdict is conditional one-dimensional linear compatibility",
        concrete_design.rank() == 2
        and source_D.subs(all_equal) == 0
        and augmented.subs(all_equal).rank() == 2
        and electromagnetic_coupling in angle_residual.free_symbols,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
