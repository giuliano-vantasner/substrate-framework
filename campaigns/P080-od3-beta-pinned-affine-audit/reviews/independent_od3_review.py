"""Independent exact P080 review without importing scale-constraint APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(value: object) -> bool:
    return sp.simplify(sp.sympify(value)) == 0


def _consistent(matrix: sp.Matrix, rhs: sp.Matrix) -> bool:
    return matrix.rank() == matrix.row_join(rhs).rank()


def _coordinate_identifiable(matrix: sp.Matrix, index: int) -> bool:
    target = sp.zeros(1, matrix.cols)
    target[0, index] = 1
    return matrix.col_join(target).rank() == matrix.rank()


def main() -> int:
    checks = CheckLedger("P080-INDEPENDENT")
    x, x_star = sp.symbols("x x_star", real=True)
    k, y_pin = sp.symbols("k y_pin", positive=True)
    g, m, h, s = sp.symbols("g m h s", real=True)
    original = sp.Matrix([[2, 0], [-4, 0], [-1, k], [-2, 2 * k]])
    raw_rhs = sp.Matrix([g, m, h, s])
    free = original[:, 0]
    pinned = original[:, 1]
    transformed_rhs = raw_rhs - pinned * y_pin

    checks.check(
        "fresh affine elimination reconstructs the original equations",
        free * x + pinned * y_pin == original * sp.Matrix([x, y_pin])
        and transformed_rhs + pinned * y_pin == raw_rhs,
    )
    checks.check(
        "fresh row reduction finds one coefficient direction",
        free.rank() == 1
        and free.rref()[1] == (0,)
        and free.cols - free.rank() == 0,
    )
    left_vectors = (
        sp.Matrix([2, 1, 0, 0]),
        sp.Matrix([sp.Rational(1, 2), 0, 1, 0]),
        sp.Matrix([1, 0, 0, 1]),
    )
    checks.check(
        "three explicit vectors form the complete left-null basis",
        all(free.T * vector == sp.zeros(1, 1) for vector in left_vectors)
        and sp.Matrix.hstack(*left_vectors).rank() == 3
        and len(free.T.nullspace()) == 3,
    )
    residuals = tuple(sp.simplify((vector.T * transformed_rhs)[0]) for vector in left_vectors)
    checks.check(
        "fresh elimination yields all three compatibility equations",
        residuals
        == (2 * g + m, g / 2 + h - k * y_pin, g + s - 2 * k * y_pin),
    )
    checks.check(
        "independent augmented-rank calculation rejects generic symbolic data",
        free.row_join(transformed_rhs).rank() == 2
        and not _consistent(free, transformed_rhs),
    )

    compatible_raw = original * sp.Matrix([x_star, y_pin])
    compatible_transformed = sp.simplify(compatible_raw - pinned * y_pin)
    solution = sp.solve(
        list(free * sp.Matrix([x]) - compatible_transformed), x, dict=True
    )
    checks.check(
        "fresh solve is unique only on the compatible supplied branch",
        compatible_transformed == free * x_star
        and _consistent(free, compatible_transformed)
        and solution == [{x: x_star}],
    )
    checks.mutation_sensitive(
        "fresh compatibility oracle rejects every single-row mutation",
        lambda values: _consistent(
            free, sp.Matrix(values) - pinned * y_pin
        ),
        compatible_raw,
        [compatible_raw + sp.eye(4)[:, index] for index in range(4)],
    )

    original_left_one = sp.Matrix([2, 1, 0, 0])
    original_left_two = sp.Matrix([0, 0, -2, 1])
    checks.check(
        "unpinned system has only the two prior AS4 compatibility relations",
        original.T * original_left_one == sp.zeros(2, 1)
        and original.T * original_left_two == sp.zeros(2, 1)
        and (original_left_one.T * raw_rhs)[0] == 2 * g + m
        and (original_left_two.T * raw_rhs)[0] == -2 * h + s,
    )
    unpinned_solution = sp.solve(
        [2 * x - g, -x + k * sp.Symbol("y", real=True) - h],
        [x, sp.Symbol("y", real=True)],
        dict=True,
    )
    checks.check(
        "the extra pinned condition selects an already inferred coupling coordinate",
        len(unpinned_solution) == 1
        and _zero(unpinned_solution[0][x] - g / 2)
        and _zero(
            unpinned_solution[0][sp.Symbol("y", real=True)]
            - (g / 2 + h) / k
        )
        and _zero((g / 2 + h) / k - y_pin)
        is False,
    )
    checks.check(
        "changing the pin leaves rank intact but changes compatibility",
        free.rank() == 1
        and not _consistent(
            free, compatible_raw - pinned * (y_pin + 1)
        ),
    )

    delta = sp.Symbol("delta", real=True)
    shifted_rhs = transformed_rhs - free * delta
    shifted_residuals = tuple(
        sp.simplify((vector.T * shifted_rhs)[0]) for vector in left_vectors
    )
    checks.check(
        "fresh reference-shift derivation preserves left-null residuals",
        shifted_residuals == residuals,
    )
    checks.check(
        "compatible coordinate shifts while equations represent the same branch",
        sp.solve(
            list(free * sp.Matrix([x]) - (compatible_transformed - free * delta)),
            x,
            dict=True,
        )
        == [{x: x_star - delta}],
    )

    nuisance = free.row_join(sp.eye(4))
    checks.check(
        "fresh nuisance restoration reopens the scale coordinate",
        nuisance.rank() == 4
        and nuisance.cols - nuisance.rank() == 1
        and not _coordinate_identifiable(nuisance, 0)
        and len(nuisance.nullspace()) == 1,
    )
    baseline, induced = sp.symbols("B S_ind", positive=True)
    gravity_total = 1 / (baseline + induced * sp.exp(-2 * x))
    gravity_slope = sp.factor(sp.diff(sp.log(gravity_total), x))
    checks.check(
        "fresh differentiation makes the gravity exponent constant only at zero baseline",
        _zero(gravity_slope.subs(baseline, 0) - 2)
        and not _zero(gravity_slope - 2),
    )

    b0 = sp.Symbol("b0", positive=True)
    checks.check(
        "fresh source-product reduction retains b0",
        sp.simplify((8 * sp.pi**2 / b0) / (4 * sp.pi))
        == 2 * sp.pi / b0
        and sp.diff(2 * sp.pi / b0, b0) != 0,
    )
    rho = sp.Symbol("rho", positive=True)
    checks.check(
        "fresh reciprocal-map conjugation moves the numeric fixed coordinate",
        sp.sqrt(rho**2 * 16 * sp.pi**2) == 4 * sp.pi * rho
        and rho * 4 * sp.pi != 4 * sp.pi,
    )
    checks.check(
        "rank-one algebra contains no row provenance or physical selection data",
        free.free_symbols == set()
        and raw_rhs.free_symbols == {g, m, h, s}
        and y_pin not in free.free_symbols,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
