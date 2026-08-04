"""Primary exact identity and semantic-ceiling verifier for P128/WM4."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.renormalization import (
    diagnose_affine_unification,
    pairwise_affine_crossing,
    reconstruct_electroweak_unification,
    rescale_abelian_inverse_coordinate,
    shift_affine_reference,
)
from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P128-wm4-nearmiss-identity-audit")
WM4 = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-33/"
    "bridge_WM4_nearmiss_identity_map.py"
)
SM4 = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-9/"
    "bridge_SM4_coupling_running_unification.py"
)
WM3 = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-23/"
    "bridge_WM3_sin2thetaw_rg_running.py"
)
HASHES = {
    WM4: "443406419edc1021a929a6041dec025f73af6d947cf770eebe9cde25d74cd8c9",
    SM4: "c0cc7ed32343afc65cf582d81b2455fdba96d2550e64e3e595e4c995ee53e3ac",
    WM3: "2328ae4d6e66e1caa14a39042c362e57258406383f14ecaa5f5f6c468105e298",
}
FREEZE_HASH = "5a5e02b02d1f929286cfe6a329eb12518260fa42ee70e5fb9c34cc34f8988e01"


def source_attributes(tree: ast.AST, root: str) -> set[str]:
    """Return attributes read directly from a named imported source module."""

    return {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == root
    }


def source_check_calls(tree: ast.AST) -> list[ast.Call]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]


def exact_source_point() -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    electromagnetic_inverse = sp.Rational(2559, 20)
    weak = sp.Rational(11561, 50000)
    strong = sp.Rational(1181, 10000)
    return (
        sp.Rational(3, 5) * (1 - weak) * electromagnetic_inverse,
        weak * electromagnetic_inverse,
        1 / strong,
    )


def main() -> int:
    checks = CheckLedger("WM4-NEARMISS-IDENTITY-AUDIT")
    payloads = {path: path.read_bytes() for path in HASHES}
    for path, expected in HASHES.items():
        checks.check(
            f"{path.stem} source bytes are hash pinned",
            hashlib.sha256(payloads[path]).hexdigest() == expected,
        )

    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_HASH,
    )
    checks.check(
        "immutable preregistration remains byte identical",
        hashlib.sha256((CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_HASH,
    )

    text = payloads[WM4].decode("utf-8")
    tree = ast.parse(text)
    checks.check("WM4 contains eleven static source checks", len(source_check_calls(tree)) == 11)
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "WM4's executable import inventory is recovered exactly",
        imports == {"contextlib", "importlib.util", "io", "math", "os", "numpy", "sympy"},
    )
    checks.check(
        "WM4 dynamically executes the pending SM4 and WM3 scripts",
        text.count("_load(") == 3
        and "bridge_SM4_coupling_running_unification.py" in text
        and "bridge_WM3_sin2thetaw_rg_running.py" in text,
    )
    checks.check(
        "WM4 reads only input scalars from its executed dependency modules",
        source_attributes(tree, "_sm4") == {"ALPHA_EM_INV", "SIN2_THETA_W", "ALPHA_S"}
        and source_attributes(tree, "_wm3") == {"ALPHA_EM_INV", "SIN2_MEASURED", "ALPHA_S"},
    )
    checks.check(
        "the claimed beta reuse is absent and the three values are re-hard-coded",
        not ({"b1", "b2", "b3"} & source_attributes(tree, "_sm4"))
        and "B1, B2, B3 = sp.Rational(41, 10), sp.Rational(-19, 6), sp.Integer(-7)" in text,
    )
    checks.check(
        "WM4 requires no numerical-integration compatibility path",
        all(
            token not in text
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral", "scipy.integrate")
        ),
    )

    a1, a2, a3, b1, b2, b3 = sp.symbols("a1 a2 a3 b1 b2 b3", real=True)
    inverse = sp.Matrix([a1, a2, a3])
    coefficients = sp.Matrix([b1, b2, b3])
    obstruction = sp.expand(
        a1 * (b2 - b3) + a2 * (b3 - b1) + a3 * (b1 - b2)
    )
    determinant = sp.Matrix(
        [[b1, 1, -a1], [b2, 1, -a2], [b3, 1, -a3]]
    ).det()
    checks.check(
        "the source determinant is exactly minus the left-null functional",
        sp.simplify(determinant + obstruction) == 0,
    )
    A, B = sp.symbols("A B", real=True)
    checks.check(
        "the obstruction vanishes identically on the affine-unification plane",
        sp.simplify(
            obstruction.subs(
                {a1: A + B * b1, a2: A + B * b2, a3: A + B * b3}
            )
        )
        == 0,
    )

    L12 = 2 * sp.pi * (a1 - a2) / (b1 - b2)
    L13 = 2 * sp.pi * (a1 - a3) / (b1 - b3)
    L23 = 2 * sp.pi * (a2 - a3) / (b2 - b3)
    crossing_relations = (
        (L12 - L13, 2 * sp.pi * obstruction / ((b1 - b2) * (b1 - b3))),
        (L12 - L23, 2 * sp.pi * obstruction / ((b1 - b2) * (b2 - b3))),
        (L13 - L23, 2 * sp.pi * obstruction / ((b1 - b3) * (b2 - b3))),
    )
    for index, (left, right) in enumerate(crossing_relations, 1):
        checks.check(
            f"conditional crossing-difference identity {index} is exact",
            sp.simplify(sp.together(left - right)) == 0,
        )

    beta = (sp.Rational(41, 10), sp.Rational(-19, 6), sp.Integer(-7))
    source_inverse = exact_source_point()
    diagnostics = diagnose_affine_unification(
        source_inverse, beta, provenance=("U1", "SU2", "SU3")
    )
    checks.check(
        "the accepted affine diagnostic finds a rank-two inconsistent source point",
        diagnostics.linear.coefficient_rank == 2
        and diagnostics.linear.augmented_rank == 3
        and not diagnostics.linear.consistent
        and len(diagnostics.left_nullspace) == 1,
    )
    checks.check(
        "the accepted pairwise oracle finds three unique source crossings",
        all(crossing.status == "unique" for crossing in diagnostics.pairwise_crossings),
    )
    source_substitution = dict(zip((*coefficients, *inverse), (*beta, *source_inverse), strict=True))
    source_D = sp.simplify(obstruction.subs(source_substitution))
    residual = diagnostics.compatibility_residuals[0]
    checks.check(
        "the canonical compatibility residual is a nonzero normalization of D",
        residual != 0 and sp.simplify(residual / source_D).free_symbols == set(),
    )

    exact_crossings = [
        sp.simplify(expression.subs(source_substitution))
        for expression in (L12, L13, L23)
    ]
    exact_range = max(exact_crossings) - min(exact_crossings)
    difference_coefficients = [
        sp.simplify(abs((left - right).subs(source_substitution) / source_D))
        for left, right in ((L12, L13), (L12, L23), (L13, L23))
    ]
    exact_range_from_D = abs(source_D) * max(difference_coefficients)
    checks.check(
        "the source crossing range is exactly absolute D times a beta-only factor",
        sp.simplify(exact_range - exact_range_from_D) == 0,
    )
    checks.check(
        "the range is even under D sign reversal and is not a signed linear functional",
        sp.simplify(sp.Abs(obstruction) - sp.Abs(-obstruction)) == 0
        and sp.simplify(obstruction - (-obstruction)) != 0
        and exact_range_from_D > 0,
    )
    decades = sp.N(exact_range / sp.log(10), 16)
    checks.check(
        "exact rational inputs reproduce the approximate 3.979-decade source headline",
        abs(float(decades) - 3.979) < 0.002,
    )

    weight = sp.Rational(5, 3)
    denominator = sp.expand(5 * b1 + 3 * b2 - 8 * b3)
    reconstruction = reconstruct_electroweak_unification(
        sp.Rational(2559, 20), source_inverse[2], *beta, weight
    )
    predicted_a2 = reconstruction.inverse_couplings[1]
    delta_a2_source = sp.simplify(predicted_a2 - source_inverse[1])
    c_source = sp.simplify(sp.Rational(5, 1) / denominator.subs(dict(zip(coefficients, beta))))
    checks.check(
        "the accepted WM3 reconstruction gives the exact beta-only inverse-coordinate residual",
        sp.simplify(delta_a2_source - c_source * source_D) == 0,
    )
    predicted_sin2 = sp.simplify(predicted_a2 / sp.Rational(2559, 20))
    checks.check(
        "the exact reconstruction reproduces WM4's SM4-input weak coordinate",
        abs(float(predicted_sin2) - 0.20753) < 0.00001,
    )
    alpha_em = sp.symbols("alpha_em", positive=True)
    dictionary_constant = (
        alpha_em
        * sp.Rational(5, 1)
        / denominator
        * (b1 - b2)
        * (b1 - b3)
        / (2 * sp.pi)
    )
    checks.check(
        "the angle dictionary contains the supplied electromagnetic input",
        alpha_em in dictionary_constant.free_symbols
        and dictionary_constant.free_symbols == {alpha_em, b1, b2, b3},
    )
    checks.check(
        "changing alpha_em changes the angle dictionary while preserving the inverse residual",
        sp.simplify(dictionary_constant.subs(alpha_em, 2) - dictionary_constant.subs(alpha_em, 1))
        != 0,
    )

    source_design = sp.Matrix([[1, value] for value in beta])
    source_annihilator = source_design.T.nullspace()
    checks.check(
        "the source beta plane has rank two and a one-dimensional linear annihilator",
        source_design.rank() == 2 and len(source_annihilator) == 1,
    )
    d_vector = sp.Matrix([beta[1] - beta[2], beta[2] - beta[0], beta[0] - beta[1]])
    checks.check(
        "D's coefficient vector spans that source linear annihilator",
        source_design.T * d_vector == sp.zeros(2, 1)
        and sp.Matrix.hstack(source_annihilator[0], d_vector).rank() == 1,
    )

    nonlinear = (1 + a1**2) * obstruction
    checks.check(
        "a nonlinear independent-form diagnostic can share D's real zero set",
        sp.simplify(nonlinear / obstruction) == 1 + a1**2
        and sp.solve(sp.Eq(1 + a1**2, 0), a1, domain=sp.S.Reals) == [],
    )
    checks.check(
        "a shared zero set therefore does not prove constant proportionality",
        sp.diff(sp.simplify(nonlinear / obstruction), a1) != 0,
    )

    equal_beta = (sp.Integer(2), sp.Integer(2), sp.Integer(2))
    equal_diag = diagnose_affine_unification(
        (sp.Integer(1), sp.Integer(2), sp.Integer(3)),
        equal_beta,
        provenance=("one", "two", "three"),
    )
    checks.check(
        "all-equal slopes refute determinant-zero iff finite concurrency",
        sp.simplify(obstruction.subs({b1: 2, b2: 2, b3: 2, a1: 1, a2: 2, a3: 3})) == 0
        and equal_diag.linear.coefficient_rank == 1
        and equal_diag.linear.augmented_rank == 2
        and not equal_diag.linear.consistent,
    )
    checks.check(
        "all-equal slopes enlarge the linear annihilator to dimension two",
        len(sp.Matrix([[1, 2], [1, 2], [1, 2]]).T.nullspace()) == 2,
    )

    one_pair = (sp.Integer(1), sp.Integer(1), sp.Integer(2))
    one_pair_design = sp.Matrix([[1, value] for value in one_pair])
    cross_13 = pairwise_affine_crossing(1, 1, 4, 2, left="1", right="3")
    cross_23 = pairwise_affine_crossing(3, 1, 4, 2, left="2", right="3")
    cross_12 = pairwise_affine_crossing(1, 1, 3, 1, left="1", right="2")
    checks.check(
        "one equal slope pair retains rank two and a one-dimensional annihilator",
        one_pair_design.rank() == 2 and len(one_pair_design.T.nullspace()) == 1,
    )
    checks.check(
        "one pair is parallel while two finite crossings and their difference survive",
        cross_12.status == "parallel_disjoint"
        and cross_13.status == "unique"
        and cross_23.status == "unique"
        and cross_13.coordinate != cross_23.coordinate,
    )
    checks.check(
        "WM3's residual coefficient remains finite when only b1 equals b2",
        denominator.subs({b1: 1, b2: 1, b3: 2}) == -8,
    )

    distinct_singular = {b1: 0, b2: 8, b3: 3}
    checks.check(
        "distinct slopes do not guarantee a finite WM3 reconstruction denominator",
        len(set(distinct_singular.values())) == 3
        and denominator.subs(distinct_singular) == 0,
    )
    singular_raised = False
    try:
        reconstruct_electroweak_unification(10, 2, 0, 8, 3, weight)
    except ValueError as error:
        singular_raised = "denominator" in str(error)
    checks.check("the accepted reconstruction rejects that distinct-slope singularity", singular_raised)

    exact_a2_star = sp.solve(
        sp.Eq(obstruction.subs({b1: beta[0], b2: beta[1], b3: beta[2], a1: source_inverse[0], a3: source_inverse[2]}), 0),
        a2,
    )
    star_substitution = {
        b1: beta[0], b2: beta[1], b3: beta[2],
        a1: source_inverse[0], a2: exact_a2_star[0], a3: source_inverse[2],
    }
    checks.check(
        "an exact rational mutation forces D and every finite crossing difference to zero",
        sp.simplify(obstruction.subs(star_substitution)) == 0
        and all(sp.simplify((left - right).subs(star_substitution)) == 0 for left, right in ((L12, L13), (L12, L23), (L13, L23))),
    )

    delta = sp.symbols("delta", real=True)
    shifted = shift_affine_reference(inverse, coefficients, delta)
    shifted_D = obstruction.subs(dict(zip(inverse, shifted, strict=True)))
    checks.check("D is exactly invariant under a common affine reference shift", sp.simplify(shifted_D - obstruction) == 0)
    checks.check(
        "all pairwise crossing coordinates shift together under the same reference change",
        all(
            sp.simplify(
                pairwise_affine_crossing(
                    shifted[i], coefficients[i], shifted[j], coefficients[j]
                ).coordinate
                - pairwise_affine_crossing(inverse[i], coefficients[i], inverse[j], coefficients[j]).coordinate
                + delta
            ) == 0
            for i, j in ((0, 1), (0, 2), (1, 2))
        ),
    )

    q = sp.Integer(2)
    concurrent = tuple(sp.Integer(10) + coefficient for coefficient in beta)
    new_a1, new_b1, new_weight = rescale_abelian_inverse_coordinate(
        concurrent[0], beta[0], weight, q
    )
    original_D = obstruction.subs(dict(zip((*coefficients, *inverse), (*beta, *concurrent), strict=True)))
    rescaled_D = obstruction.subs(
        {b1: new_b1, b2: beta[1], b3: beta[2], a1: new_a1, a2: concurrent[1], a3: concurrent[2]}
    )
    checks.check(
        "paired Abelian rescaling preserves the EM combination but not coupling equality",
        sp.simplify(new_weight * new_a1 + concurrent[1] - (weight * concurrent[0] + concurrent[1])) == 0
        and original_D == 0
        and rescaled_D != 0,
    )

    scale = sp.symbols("lambda", positive=True)
    scaled_D = obstruction.subs({a1: scale * a1, a2: scale * a2, a3: scale * a3})
    checks.check("D is normalization-covariant rather than invariant", sp.simplify(scaled_D - scale * obstruction) == 0)
    measured = sp.Rational(11561, 50000)
    checks.check(
        "percentage miss changes with its declared denominator",
        sp.simplify(abs(predicted_sin2 - measured) / measured - abs(predicted_sin2 - measured) / predicted_sin2) != 0,
    )

    checks.check(
        "the strongest primary verdict is the accepted conditional linear theorem",
        diagnostics.linear.coefficient_rank == 2
        and not diagnostics.linear.consistent
        and source_D != 0
        and alpha_em in dictionary_constant.free_symbols
        and equal_diag.linear.coefficient_rank == 1,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
