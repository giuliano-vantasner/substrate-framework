"""Independent exact P075 review without importing scale-constraint APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(value: object) -> bool:
    return sp.simplify(sp.sympify(value)) == 0


def _coordinate_identifiable(matrix: sp.Matrix, index: int) -> bool:
    target = sp.zeros(1, matrix.cols)
    target[0, index] = 1
    return matrix.col_join(target).rank() == matrix.rank()


def main() -> int:
    ledger = CheckLedger("P075-INDEPENDENT")
    k = sp.Symbol("k", positive=True)
    g, r, h, s = sp.symbols("g r h s", real=True)
    matrix = sp.Matrix([[2, 0], [-4, 0], [-1, k], [-2, 2 * k]])
    rhs = sp.Matrix([g, r, h, s])
    reduced, pivots = matrix.rref()

    ledger.check(
        "fresh row reduction yields two coefficient directions",
        reduced[:2, :] == sp.eye(2)
        and reduced[2:, :] == sp.zeros(2, 2)
        and pivots == (0, 1)
        and matrix.rank() == 2
        and matrix.cols - matrix.rank() == 0,
    )
    left_one = sp.Matrix([2, 1, 0, 0])
    left_two = sp.Matrix([0, 0, -2, 1])
    ledger.check(
        "explicit left-null vectors span the two row dependencies",
        matrix.T * left_one == sp.zeros(2, 1)
        and matrix.T * left_two == sp.zeros(2, 1)
        and sp.Matrix.hstack(left_one, left_two).rank() == 2,
    )
    ledger.check(
        "explicit elimination gives both compatibility conditions",
        (left_one.T * rhs)[0] == 2 * g + r
        and (left_two.T * rhs)[0] == -2 * h + s,
    )
    ledger.check(
        "generic right-hand sides raise augmented rank above coefficient rank",
        matrix.row_join(rhs).rank() == 3 and matrix.rank() == 2,
    )

    compatible_rhs = sp.Matrix([g, -2 * g, h, 2 * h])
    compatible_augmented = matrix.row_join(compatible_rhs)
    solution = sp.solve(
        list(matrix * sp.Matrix(sp.symbols("x y")) - compatible_rhs),
        sp.symbols("x y"),
        dict=True,
    )
    ledger.check(
        "fresh solve is unique only after both right-hand-side relations are imposed",
        compatible_augmented.rank() == 2
        and solution
        == [{sp.Symbol("x"): g / 2, sp.Symbol("y"): (g + 2 * h) / (2 * k)}],
    )
    ledger.mutation_sensitive(
        "fresh left-null oracle rejects each incompatible datum",
        lambda values: _zero((left_one.T * sp.Matrix(values))[0])
        and _zero((left_two.T * sp.Matrix(values))[0]),
        compatible_rhs,
        [
            [g, -2 * g + 1, h, 2 * h],
            [g, -2 * g, h, 2 * h + 1],
        ],
    )

    source_guard = sp.Matrix(
        [[2, 0, 0], [-4, 0, 0], [-1, k, 1], [-2, 2 * k, 1]]
    )
    corrected_guard = source_guard.copy()
    corrected_guard[3, 2] = 2
    ledger.check(
        "fresh rank audit separates the source guard from an actual reopened nullity",
        source_guard.rank() == 3
        and source_guard.cols - source_guard.rank() == 0
        and corrected_guard.rank() == 2
        and corrected_guard.cols - corrected_guard.rank() == 1,
    )

    correct_dimensions = sp.Matrix([[0, 1, 0], [1, 2, -1], [0, 1, -1]])
    source_dimensions = sp.Matrix([[1, 0, 0], [1, 2, -1], [0, 1, -1]])
    ledger.check(
        "fresh dimension construction catches AS4's mislabeled a row without changing rank",
        correct_dimensions[0, :] == sp.Matrix([[0, 1, 0]])
        and source_dimensions[0, :] != correct_dimensions[0, :]
        and correct_dimensions.rank() == source_dimensions.rank() == 3,
    )

    nuisance = sp.Matrix(
        [
            [2, 0, -1, 0, 0],
            [-4, 0, 0, -1, 0],
            [-1, k, 0, 0, 0],
            [-2, 2 * k, 0, 0, -1],
        ]
    )
    nuisance_null = nuisance.nullspace()
    ledger.check(
        "fresh nuisance restoration leaves a mixed scale-coupling direction",
        nuisance.rank() == 4
        and len(nuisance_null) == 1
        and nuisance * nuisance_null[0] == sp.zeros(4, 1)
        and nuisance_null[0][0] != 0
        and nuisance_null[0][1] != 0
        and not _coordinate_identifiable(nuisance, 0)
        and not _coordinate_identifiable(nuisance, 1),
    )

    x = sp.Symbol("x", real=True)
    baseline, induced = sp.symbols("B S", positive=True)
    total_g = 1 / (baseline + induced * sp.exp(-2 * x))
    slope = sp.factor(sp.diff(sp.log(total_g), x))
    ledger.check(
        "fresh differentiation makes the gravity row constant only at zero baseline",
        _zero(slope.subs(baseline, 0) - 2)
        and not _zero(slope - 2),
    )

    observations = sp.Matrix([2, -3, 3, 7])
    identity_precision = sp.eye(4)
    unequal_precision = sp.diag(1, sp.Rational(1, 4), 1, sp.Rational(1, 9))

    def weighted_ledger(precision: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix, sp.Expr]:
        estimate = (matrix.T * precision * matrix).inv() * matrix.T * precision * observations
        residual = observations - matrix * estimate
        return estimate, residual, sp.simplify((residual.T * precision * residual)[0])

    estimate_one, residual_one, chi_one = weighted_ledger(identity_precision)
    estimate_two, residual_two, chi_two = weighted_ledger(unequal_precision)
    ledger.check(
        "fresh weighted normal equations depend on the declared covariance",
        matrix.T * identity_precision * residual_one == sp.zeros(2, 1)
        and matrix.T * unequal_precision * residual_two == sp.zeros(2, 1)
        and chi_one > 0
        and chi_two > 0
        and (estimate_one != estimate_two or chi_one != chi_two),
    )

    wrong_medium = 7 * g + h
    wrong_confine = -3 * g + 5 * h
    ledger.check(
        "fresh counterexample shows symbol occurrence is weaker than coefficient verification",
        wrong_medium.has(g)
        and wrong_confine.has(h)
        and not _zero(wrong_medium + 2 * g)
        and not _zero(wrong_confine - 2 * h),
    )
    ledger.check(
        "the exact matrix carries no physical provenance or covariance object",
        all(not entry.free_symbols - {k} for entry in matrix)
        and matrix.shape == (4, 2)
        and not hasattr(matrix, "covariance_provenance"),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
