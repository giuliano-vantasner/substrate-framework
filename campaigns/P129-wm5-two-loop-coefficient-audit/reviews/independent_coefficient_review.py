"""Independent exact P129 rederivation without the canonical gauge-beta API."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-33/"
    "bridge_WM5_two_loop_coefficients.py"
)
FROZEN = Path(
    "campaigns/P129-wm5-two-loop-coefficient-audit/evidence/frozen-proposal.yaml"
)
SOURCE_SHA = "8c3fbfeecb6f98d7d80c47e8f267fe1216dde724b81cc3f73f2a3bb17caf1bbc"
FREEZE_SHA = "37e3001f76cf327861eb5df092adfbb4c46c73a133c635c6ef26db073cc959a2"


def main() -> int:
    checks = CheckLedger("WM5-INDEPENDENT-COEFFICIENT-REVIEW")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "independently read source bytes retain their pinned hash",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    checks.check(
        "independently read preregistration remains byte identical",
        hashlib.sha256(FROZEN.read_bytes()).hexdigest() == FREEZE_SHA,
    )
    checks.check(
        "fresh AST walk finds eleven source predicates",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(source_tree)
        )
        == 11,
    )

    # Fresh representation enumeration. Each row is
    # label, copies, color dimension, isospin dimension, hypercharge, kind.
    fields = (
        ("Q_L", 3, 3, 2, sp.Rational(1, 6), "F"),
        ("u_R_conj", 3, 3, 1, -sp.Rational(2, 3), "F"),
        ("d_R_conj", 3, 3, 1, sp.Rational(1, 3), "F"),
        ("L_L", 3, 1, 2, -sp.Rational(1, 2), "F"),
        ("e_R_conj", 3, 1, 1, sp.Integer(1), "F"),
        ("H", 1, 1, 2, sp.Rational(1, 2), "S"),
    )
    adjoint = (sp.Integer(0), sp.Integer(2), sp.Integer(3))

    def s2(row: tuple[object, ...], factor: int) -> sp.Expr:
        _label, _copies, color, isospin, hypercharge, _kind = row
        color = int(color)
        isospin = int(isospin)
        hypercharge = sp.sympify(hypercharge)
        if factor == 0:
            return sp.Rational(3, 5) * hypercharge**2 * color * isospin
        if factor == 1:
            return sp.Rational(1, 2) * color if isospin == 2 else sp.Integer(0)
        return sp.Rational(1, 2) * isospin if color == 3 else sp.Integer(0)

    def c2(row: tuple[object, ...], factor: int) -> sp.Expr:
        _label, _copies, color, isospin, hypercharge, _kind = row
        color = int(color)
        isospin = int(isospin)
        hypercharge = sp.sympify(hypercharge)
        if factor == 0:
            return sp.Rational(3, 5) * hypercharge**2
        if factor == 1:
            return sp.Rational(3, 4) if isospin == 2 else sp.Integer(0)
        return sp.Rational(4, 3) if color == 3 else sp.Integer(0)

    fermions = tuple(row for row in fields if row[-1] == "F")
    scalars = tuple(row for row in fields if row[-1] == "S")
    one_loop: list[sp.Expr] = []
    matrix: list[list[sp.Expr]] = []
    for a in range(3):
        b_a = -sp.Rational(11, 3) * adjoint[a]
        b_a += sum(sp.Rational(2, 3) * int(row[1]) * s2(row, a) for row in fermions)
        b_a += sum(sp.Rational(1, 3) * int(row[1]) * s2(row, a) for row in scalars)
        one_loop.append(sp.simplify(b_a))
        matrix.append([])
        for b in range(3):
            delta = sp.Integer(a == b)
            value = -sp.Rational(34, 3) * adjoint[a] ** 2 * delta
            value += sum(
                int(row[1])
                * s2(row, a)
                * (sp.Rational(10, 3) * adjoint[a] * delta + 2 * c2(row, b))
                for row in fermions
            )
            value += sum(
                int(row[1])
                * s2(row, a)
                * (sp.Rational(2, 3) * adjoint[a] * delta + 4 * c2(row, b))
                for row in scalars
            )
            matrix[a].append(sp.simplify(value))

    expected_one = [sp.Rational(41, 10), -sp.Rational(19, 6), -7]
    expected_matrix = [
        [sp.Rational(199, 50), sp.Rational(27, 10), sp.Rational(44, 5)],
        [sp.Rational(9, 10), sp.Rational(35, 6), 12],
        [sp.Rational(11, 10), sp.Rational(9, 2), -26],
    ]
    checks.check(
        "fresh multiplet enumeration gives the exact one-loop vector",
        one_loop == expected_one,
    )
    checks.check(
        "fresh multiplet enumeration gives the exact gauge-only matrix",
        matrix == expected_matrix,
    )
    per_generation_y2 = sum(
        int(row[1]) * s2(row, 0) for row in fermions
    ) / 3
    per_generation_y4 = sum(
        int(row[1]) * s2(row, 0) * c2(row, 0) for row in fermions
    ) / 3
    checks.check(
        "fresh Abelian moments are second moment two and quartic moment nineteen over thirty",
        per_generation_y2 == 2 and per_generation_y4 == sp.Rational(19, 30),
    )
    qcd_closed = -sp.Rational(34, 3) * 3**2 + (
        sp.Rational(10, 3) * 3 + 2 * sp.Rational(4, 3)
    ) * 2 * 6 * sp.Rational(1, 2)
    checks.check(
        "fresh Dirac-pair QCD specialization independently gives minus twenty-six",
        sp.simplify(qcd_closed) == -26 == matrix[2][2],
    )

    rho = sp.symbols("rho", positive=True)
    row_scales = (rho**2, 1, 1)
    rescaled_one = [sp.simplify(row_scales[a] * one_loop[a]) for a in range(3)]
    rescaled_matrix = [
        [sp.simplify(row_scales[a] * row_scales[b] * matrix[a][b]) for b in range(3)]
        for a in range(3)
    ]
    checks.check(
        "fresh homogeneous counting gives the Abelian row and column scaling law",
        rescaled_one[0] == rho**2 * expected_one[0]
        and rescaled_matrix[0][0] == rho**4 * expected_matrix[0][0]
        and rescaled_matrix[0][2] == rho**2 * expected_matrix[0][2]
        and rescaled_matrix[2][0] == rho**2 * expected_matrix[2][0],
    )
    g1, g2, g3, loop = sp.symbols("g1 g2 g3 L", positive=True)
    couplings = (g1, g2, g3)
    transformed_couplings = (g1 / rho, g2, g3)
    base_beta = [
        one_loop[a] * couplings[a] ** 3 / loop
        + couplings[a] ** 3
        * sum(matrix[a][b] * couplings[b] ** 2 for b in range(3))
        / loop**2
        for a in range(3)
    ]
    transformed_beta = [
        rescaled_one[a] * transformed_couplings[a] ** 3 / loop
        + transformed_couplings[a] ** 3
        * sum(
            rescaled_matrix[a][b] * transformed_couplings[b] ** 2
            for b in range(3)
        )
        / loop**2
        for a in range(3)
    ]
    checks.check(
        "fresh beta-polynomial substitution proves inverse-coupling covariance",
        all(
            sp.simplify(
                transformed_beta[a] - base_beta[a] / (rho if a == 0 else 1)
            )
            == 0
            for a in range(3)
        ),
    )

    matrix_tuple = tuple(tuple(row) for row in matrix)
    checks.check(
        "fresh transpose mutant fails because row and column roles differ",
        tuple(zip(*matrix_tuple, strict=True)) != matrix_tuple,
    )
    no_scalar_one = [
        sp.simplify(
            -sp.Rational(11, 3) * adjoint[a]
            + sum(
                sp.Rational(2, 3) * int(row[1]) * s2(row, a)
                for row in fermions
            )
        )
        for a in range(3)
    ]
    dirac_count_one = [
        sp.simplify(
            -sp.Rational(11, 3) * adjoint[a]
            + sum(
                sp.Rational(4, 3) * int(row[1]) * s2(row, a)
                for row in fermions
            )
            + sum(
                sp.Rational(1, 3) * int(row[1]) * s2(row, a)
                for row in scalars
            )
        )
        for a in range(3)
    ]
    checks.check(
        "fresh Higgs omission and Dirac-counting mutants both fail the exact vector",
        no_scalar_one != expected_one
        and no_scalar_one[0] == 4
        and dirac_count_one != expected_one
        and dirac_count_one[2] == -3,
    )
    checks.check(
        "fresh formula has no place for a physical field-content derivation",
        all(row[0] not in {"StandardModel", "anomaly_forced"} for row in fields),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
