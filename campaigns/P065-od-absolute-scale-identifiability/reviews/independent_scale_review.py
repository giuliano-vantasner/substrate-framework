"""Independent exact P065 review without importing scale_constraints."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(value: object) -> bool:
    return sp.simplify(sp.sympify(value)) == 0


def _coordinate_identifiable(matrix: sp.Matrix, index: int) -> bool:
    """Fresh row-space criterion: e_j belongs to row(A)."""

    target = sp.zeros(1, matrix.cols)
    target[0, index] = 1
    return matrix.col_join(target).rank() == matrix.rank()


def main() -> int:
    ledger = CheckLedger("P065-INDEPENDENT")
    od = sp.Matrix(
        [
            [1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
        ]
    )
    ledger.check(
        "fresh row-space test finds no identifiable OD coordinate",
        all(not _coordinate_identifiable(od, index) for index in range(od.cols)),
    )
    null = od.nullspace()
    ledger.check(
        "fresh nullspace derivation gives the mixed OD affine direction",
        null == [sp.Matrix([-1, 1, 1, 1, 1])]
        and od * null[0] == sp.zeros(4, 1),
    )
    partial = sp.Matrix([[1, 0, 0], [0, 1, 0]])
    ledger.check(
        "fresh row-space test identifies two coordinates in a nonunique square-count system",
        [_coordinate_identifiable(partial, index) for index in range(3)]
        == [True, True, False]
        and partial.rows < partial.cols,
    )

    k = sp.Symbol("k", nonzero=True)
    as4 = sp.Matrix([[2, 0], [-4, 0], [-1, k], [-2, 2 * k]])
    left = as4.T.nullspace()
    ledger.check(
        "fresh AS4 row reduction yields two not four coefficient directions",
        as4.rank() == 2 and len(left) == 2,
    )
    g, r, h, s = sp.symbols("g r h s")
    rhs = sp.Matrix([g, r, h, s])
    residuals = {sp.simplify((vector.T * rhs)[0]) for vector in left}
    ledger.check(
        "fresh left-null derivation yields both AS4 compatibility relations",
        residuals == {2 * g + r, -2 * h + s},
    )
    ledger.mutation_sensitive(
        "fresh compatibility oracle rejects either changed redundant datum",
        lambda values: all(_zero((vector.T * sp.Matrix(values))[0]) for vector in left),
        [g, -2 * g, h, 2 * h],
        [
            [g, -2 * g + 1, h, 2 * h],
            [g, -2 * g, h, 2 * h + 1],
        ],
    )

    source_guard = sp.Matrix(
        [[2, 0, 0], [-4, 0, 0], [-1, k, 1], [-2, 2 * k, 1]]
    )
    reopened = source_guard.copy()
    reopened[3, 2] = 2
    ledger.check(
        "fresh rank calculation refutes AS4 free-length guard prose",
        source_guard.rank() == 3
        and source_guard.cols - source_guard.rank() == 0
        and reopened.rank() == 2
        and reopened.cols - reopened.rank() == 1,
    )

    design = sp.Matrix([[1], [1]])
    observations = sp.Matrix([1, 3])
    covariance = sp.eye(2)
    precision = covariance.inv()
    variable = sp.Symbol("x", real=True)
    objective = ((observations - design * variable).T * precision * (observations - design * variable))[0]
    stationary = sp.solve(sp.Eq(sp.diff(objective, variable), 0), variable)
    ledger.check(
        "fresh derivative of the GLS quadratic gives the exact estimator",
        stationary == [2] and sp.diff(objective, variable, 2) == 4,
    )
    estimate = stationary[0]
    residual = observations - design * estimate
    ledger.check(
        "fresh GLS residual is precision-orthogonal with one residual degree",
        design.T * precision * residual == sp.zeros(1, 1)
        and (residual.T * precision * residual)[0] == 2
        and design.rows - design.rank() == 1,
    )
    rho = sp.Symbol("rho", real=True)
    shared_covariance = sp.Matrix([[1, rho], [rho, 1]])
    shared_precision = shared_covariance.inv()
    shared_chi = sp.factor((residual.T * shared_precision * residual)[0])
    ledger.check(
        "fresh covariance inversion exposes anti-common-mode residual weight",
        _zero(shared_chi - 2 / (1 - rho))
        and shared_chi.subs(rho, sp.Rational(1, 2)) == 4,
    )
    ledger.check(
        "fresh covariance determinant separates SPD interior from singular boundary",
        shared_covariance.det() == 1 - rho**2
        and shared_covariance.subs(rho, 1).det() == 0,
    )

    intervals = [(sp.Rational(0), sp.Rational(3)), (sp.Rational(1), sp.Rational(4)), (sp.Rational(1, 2), sp.Rational(2))]
    lower = max(item[0] for item in intervals)
    upper = min(item[1] for item in intervals)
    ledger.check(
        "fresh order-statistic derivation gives the exact interval intersection",
        (lower, upper) == (1, 2) and lower < upper,
    )
    ledger.check(
        "fresh interval boundary and separation distinguish point from contradiction",
        max(0, 1) == min(1, 2)
        and max(0, 2) > min(1, 3),
    )

    matrix = sp.Matrix([[1], [2]])
    values = sp.Matrix([3, 6])
    delta = sp.Rational(5, 2)
    shifted_values = values - matrix * delta
    left_vector = matrix.T.nullspace()[0]
    ledger.check(
        "fresh reference transformation leaves the left-null residual invariant",
        shifted_values == sp.Matrix([sp.Rational(1, 2), 1])
        and _zero((left_vector.T * values)[0] - (left_vector.T * shifted_values)[0]),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
