"""Primary exact coefficient, provenance, and source-semantics verifier for P129."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.gauge_beta import (
    GaugeFactor,
    ProductMultiplet,
    abelian_gauge_rescaling_ledger,
    gauge_only_beta,
    product_gauge_coefficients,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-33/"
    "bridge_WM5_two_loop_coefficients.py"
)
CAMPAIGN = Path("campaigns/P129-wm5-two-loop-coefficient-audit")
SOURCE_SHA = "8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc"
FREEZE_SHA = "37e3001f76cf327861eb5df092adfbb4c46c73a133c635c6ef26db073cc959a2"


def _extract_matrix_assignment(tree: ast.Module, name: str) -> sp.Matrix:
    node = next(
        item
        for item in tree.body
        if isinstance(item, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == name for target in item.targets)
    )
    module = ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[]))
    namespace: dict[str, object] = {"sp": sp, "R": sp.Rational}
    exec(compile(module, str(SOURCE), "exec"), namespace)
    value = namespace[name]
    if not isinstance(value, sp.MatrixBase):
        raise TypeError(f"{name} is not a SymPy matrix")
    return sp.Matrix(value)


def _multiplet(
    label: str,
    kind: str,
    multiplicity: int,
    color_dimension: int,
    isospin_dimension: int,
    hypercharge: sp.Expr,
) -> ProductMultiplet:
    normalized_y2 = sp.Rational(3, 5) * hypercharge**2
    return ProductMultiplet(
        label=label,
        kind=kind,  # type: ignore[arg-type]
        multiplicity=multiplicity,
        dynkin_indices=(
            normalized_y2 * color_dimension * isospin_dimension,
            sp.Rational(1, 2) * color_dimension if isospin_dimension == 2 else 0,
            sp.Rational(1, 2) * isospin_dimension if color_dimension == 3 else 0,
        ),
        quadratic_casimirs=(
            normalized_y2,
            sp.Rational(3, 4) if isospin_dimension == 2 else 0,
            sp.Rational(4, 3) if color_dimension == 3 else 0,
        ),
    )


def _declared_table() -> tuple[ProductMultiplet, ...]:
    return (
        _multiplet("Q_L", "weyl_fermion", 3, 3, 2, sp.Rational(1, 6)),
        _multiplet("u_R_conj", "weyl_fermion", 3, 3, 1, -sp.Rational(2, 3)),
        _multiplet("d_R_conj", "weyl_fermion", 3, 3, 1, sp.Rational(1, 3)),
        _multiplet("L_L", "weyl_fermion", 3, 1, 2, -sp.Rational(1, 2)),
        _multiplet("e_R_conj", "weyl_fermion", 3, 1, 1, 1),
        _multiplet("H", "complex_scalar", 1, 1, 2, sp.Rational(1, 2)),
    )


def main() -> int:
    checks = CheckLedger("WM5-TWO-LOOP-COEFFICIENT-AUDIT")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "WM5 source bytes are hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    normalized_contract = (CAMPAIGN / "proposal.yaml").read_bytes().replace(
        b"status: accepted\n", b"status: draft\n"
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "pre-source contract remains byte immutable",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "eleven source call sites match the terminal source tally",
        len(source_checks) == 11 and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "WM5 has no quadrature compatibility path",
        all(
            token not in source_text
            for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")
        ),
    )

    imported_attributes = {
        (node.value.id, node.attr)
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
    }
    expected_imported_attributes = {
        ("_wm1", "FIELDS"),
        ("_wm1", "Tr"),
        ("_sm2", "Y_H_PS"),
        ("_sm4", "b1"),
        ("_sm4", "b2"),
        ("_sm4", "b3"),
        ("_sm4", "SIN2_THETA_W"),
        ("_sm4", "ALPHA_EM_INV"),
        ("_sm4", "ALPHA_S"),
    }
    checks.check(
        "AST provenance finds only the three executable dependency namespaces",
        {
            name
            for name, _attribute in imported_attributes
            if name.startswith("_")
        }
        == {"_wm1", "_sm2", "_sm4"}
        and expected_imported_attributes <= imported_attributes,
    )
    for token in (
        "N_GEN = 3",
        "KAPPA = R(1, 2)",
        "ETA = R(1)",
        "GUT = R(3, 5)",
        "C2_FUND3 = R(4, 3)",
        "T_FUND3 = R(1, 2)",
        "C2_DOUB2 = R(3, 4)",
        "T_DOUB2 = R(1, 2)",
    ):
        checks.check(f"source hardcodes rather than imports {token}", token in source_text)
    embedded_expected = _extract_matrix_assignment(source_tree, "B_expected")
    embedded_literature = _extract_matrix_assignment(source_tree, "B_LITERATURE")
    checks.check(
        "source embeds the same exact nonzero comparator matrix twice",
        embedded_expected.shape == (3, 3)
        and embedded_expected != sp.zeros(3, 3)
        and embedded_expected == embedded_literature,
    )

    factors = (
        GaugeFactor("U1_GUT", 0, is_abelian=True),
        GaugeFactor("SU2", 2),
        GaugeFactor("SU3", 3),
    )
    table = _declared_table()
    ledger = product_gauge_coefficients(factors, table)
    expected_one = (sp.Rational(41, 10), -sp.Rational(19, 6), -7)
    expected_two = (
        (sp.Rational(199, 50), sp.Rational(27, 10), sp.Rational(44, 5)),
        (sp.Rational(9, 10), sp.Rational(35, 6), 12),
        (sp.Rational(11, 10), sp.Rational(9, 2), -26),
    )
    checks.check(
        "canonical ledger reproduces the exact supplied-table one-loop vector",
        ledger.one_loop == expected_one,
    )
    checks.check(
        "canonical ledger reproduces the exact supplied-table gauge matrix",
        ledger.two_loop_gauge_matrix == expected_two
        and sp.Matrix(expected_two) == embedded_expected,
    )
    checks.check(
        "every coefficient decomposes into explicit gauge fermion and scalar terms",
        all(
            sp.simplify(
                ledger.one_loop[a]
                - ledger.one_loop_gauge[a]
                - ledger.one_loop_weyl_fermions[a]
                - ledger.one_loop_complex_scalars[a]
            )
            == 0
            for a in range(3)
        )
        and all(
            sp.simplify(
                ledger.two_loop_gauge_matrix[a][b]
                - ledger.two_loop_gauge[a][b]
                - ledger.two_loop_weyl_fermions[a][b]
                - ledger.two_loop_complex_scalars[a][b]
            )
            == 0
            for a in range(3)
            for b in range(3)
        ),
    )
    checks.check(
        "gauge-only scope explicitly withholds same-order and physical completions",
        "two-loop Yukawa contribution" in ledger.omitted_terms
        and "multiple-Abelian kinetic mixing" in ledger.omitted_terms
        and "physical field-content derivation" in ledger.omitted_terms[-1],
    )

    rho = sp.symbols("rho", positive=True)
    rescaling = abelian_gauge_rescaling_ledger(ledger, (rho, 1, 1))
    checks.check(
        "Abelian coefficient rescaling laws close with zero exact residual",
        rescaling.one_loop_residuals == (0, 0, 0)
        and rescaling.two_loop_residuals == ((0, 0, 0),) * 3,
    )
    g1, g2, g3 = sp.symbols("g1 g2 g3", real=True)
    base_beta = gauge_only_beta(ledger, (g1, g2, g3))
    rescaled_beta = gauge_only_beta(rescaling.rescaled, (g1 / rho, g2, g3))
    checks.check(
        "inverse coupling rescaling makes the beta vector covariant",
        tuple(
            sp.simplify(rescaled_beta[a] - base_beta[a] / (rho if a == 0 else 1))
            for a in range(3)
        )
        == (0, 0, 0),
    )
    checks.check(
        "matrix orientation is load bearing because the exact matrix is asymmetric",
        tuple(zip(*ledger.two_loop_gauge_matrix, strict=True))
        != ledger.two_loop_gauge_matrix,
    )

    no_higgs = product_gauge_coefficients(factors, table[:-1])
    double_fermions = product_gauge_coefficients(
        factors,
        tuple(
            ProductMultiplet(
                item.label,
                item.kind,
                item.multiplicity * (2 if item.kind == "weyl_fermion" else 1),
                item.dynkin_indices,
                item.quadratic_casimirs,
            )
            for item in table
        ),
    )
    ql = table[0]
    colorless_ql = ProductMultiplet(
        ql.label,
        ql.kind,
        ql.multiplicity,
        (ql.dynkin_indices[0] / 3, ql.dynkin_indices[1] / 3, 0),
        (ql.quadratic_casimirs[0], ql.quadratic_casimirs[1], 0),
    )
    color_mutant = product_gauge_coefficients(factors, (colorless_ql,) + table[1:])
    checks.mutation_sensitive(
        "exact coefficient table",
        lambda candidate: candidate == (expected_one, expected_two),
        (ledger.one_loop, ledger.two_loop_gauge_matrix),
        (
            (no_higgs.one_loop, no_higgs.two_loop_gauge_matrix),
            (double_fermions.one_loop, double_fermions.two_loop_gauge_matrix),
            (color_mutant.one_loop, color_mutant.two_loop_gauge_matrix),
            (ledger.one_loop, tuple(zip(*ledger.two_loop_gauge_matrix, strict=True))),
        ),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
