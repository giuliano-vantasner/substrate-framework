"""Fresh exact rederivation for proposed C-GOR-002.

This review intentionally does not import ``gordon_scalar_compatibility``.
"""

from __future__ import annotations

from itertools import combinations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _curvature(
    metric: sp.Matrix,
    coordinates: tuple[sp.Symbol, ...],
) -> tuple[sp.Matrix, sp.Expr, sp.Matrix]:
    dimension = len(coordinates)
    inverse = metric.inv().applyfunc(sp.simplify)
    christoffel = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coordinates[b])
                            + sp.diff(metric[d, b], coordinates[c])
                            - sp.diff(metric[b, c], coordinates[d])
                        )
                        / 2
                        for d in range(dimension)
                    )
                )
                for c in range(dimension)
            ]
            for b in range(dimension)
        ]
        for a in range(dimension)
    ]
    ricci = sp.zeros(dimension)
    for a in range(dimension):
        for b in range(dimension):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(christoffel[c][a][b], coordinates[c])
                    - sp.diff(christoffel[c][a][c], coordinates[b])
                    + sum(
                        christoffel[c][c][d] * christoffel[d][a][b]
                        - christoffel[c][b][d] * christoffel[d][a][c]
                        for d in range(dimension)
                    )
                    for c in range(dimension)
                )
            )
    scalar = sp.simplify(
        sum(
            inverse[a, b] * ricci[a, b]
            for a in range(dimension)
            for b in range(dimension)
        )
    )
    einstein = (ricci - metric * scalar / 2).applyfunc(sp.simplify)
    return inverse, scalar, einstein


def _fresh_scalar_stress(
    metric: sp.Matrix,
    gradient: sp.Matrix,
    potential: sp.Expr,
) -> sp.Matrix:
    norm = sp.simplify((gradient.T * metric.inv() * gradient)[0])
    return (gradient * gradient.T - metric * (norm / 2 + potential)).applyfunc(
        sp.simplify
    )


def main() -> int:
    checks = CheckLedger("P178/C-GOR-002 independent")
    t, x, y, z = sp.symbols("t x y z", real=True)
    coordinates = (t, x, y, z)
    n = sp.Function("n", positive=True)(x)
    eta = sp.diag(-1, 1, 1, 1)
    velocity = sp.Rational(1, 2)
    gamma = 2 / sp.sqrt(3)
    u_up = sp.Matrix([gamma, 0, 0, gamma * velocity])
    u_down = eta * u_up
    metric = (eta + (1 - n**-2) * u_down * u_down.T).applyfunc(sp.simplify)
    inverse, scalar, einstein = _curvature(metric, coordinates)
    kernel = sp.factor(
        (n * sp.diff(n, x, 2) - 2 * sp.diff(n, x) ** 2) / n**2
    )
    expected = sp.zeros(4)
    expected[0, 0] = -kernel / 3
    expected[0, 3] = expected[3, 0] = 2 * kernel / 3
    expected[2, 2] = -kernel
    expected[3, 3] = -4 * kernel / 3
    checks.check(
        "fresh Christoffel reconstruction gives the accepted Gordon tensor",
        (einstein - expected).applyfunc(sp.simplify) == sp.zeros(4)
        and sp.simplify(scalar - 2 * kernel) == 0,
    )
    checks.check(
        "fresh inverse and determinant retain the Lorentzian convention",
        (inverse * metric).applyfunc(sp.simplify) == sp.eye(4)
        and sp.simplify(metric.det() + n**-2) == 0,
    )
    witness = {n: 2, sp.diff(n, x): 1, sp.diff(n, x, 2): 0}
    evaluated = einstein.applyfunc(lambda entry: sp.simplify(entry.subs(witness)))
    checks.check(
        "fresh witness is one sixth with the invariant component ratios",
        evaluated[0, 0] == sp.Rational(1, 6)
        and evaluated[0, 3] == -2 * evaluated[0, 0]
        and evaluated[2, 2] == 3 * evaluated[0, 0]
        and evaluated[3, 3] == 4 * evaluated[0, 0]
        and evaluated[1, 1] == 0,
    )

    N, v = sp.symbols("N v", positive=True)
    gamma_squared = 1 / (1 - v**2)
    general_u_down = sp.Matrix(
        [-sp.sqrt(gamma_squared), 0, 0, sp.sqrt(gamma_squared) * v]
    )
    general_metric = (
        eta + (1 - N**-2) * general_u_down * general_u_down.T
    ).applyfunc(sp.simplify)
    temporal, transverse, potential = sp.symbols("p q V", real=True)
    stress = _fresh_scalar_stress(
        general_metric,
        sp.Matrix([temporal, transverse, 0, 0]),
        potential,
    )
    a, b = sp.symbols("a b", nonnegative=True)

    def jetify(expression: sp.Expr) -> sp.Expr:
        return sp.factor(
            sp.expand(expression)
            .subs(temporal**2, a)
            .subs(transverse**2, b)
        )

    stress = stress.applyfunc(jetify)
    conditions = [
        stress[1, 1],
        stress[0, 3] + stress[0, 0] / v,
        stress[2, 2] - (v**-2 - 1) * stress[0, 0],
        stress[3, 3] - v**-2 * stress[0, 0],
    ]
    conditions = [
        sp.factor(sp.together(item).as_numer_denom()[0]) for item in conditions
    ]
    matrix, rhs = sp.linear_eq_to_matrix(conditions, [a, b, potential])
    minors = {
        rows: sp.factor(matrix[list(rows), :].det())
        for rows in combinations(range(4), 3)
    }
    direct_minor = 8 * N**2 * v**2 * (v**2 - 1) ** 5
    checks.check(
        "fresh all-component elimination has a nonzero subluminal minor",
        rhs == sp.zeros(4, 1)
        and sp.simplify(minors[(0, 1, 2)] - direct_minor) == 0,
    )
    solution = sp.solve(conditions, [a, b, potential], dict=True)
    checks.check(
        "fresh general nonzero-boost solve has only the zero scalar jet",
        solution == [{a: 0, b: 0, potential: 0}]
        and matrix.rank() == 3,
    )
    checks.check(
        "fresh tx component exposes the omitted bilinear equation",
        stress[0, 1] == temporal * transverse
        and expected[0, 1] == 0,
    )

    rest_metric = sp.diag(-N**-2, 1, 1, 1)
    rest_stress = _fresh_scalar_stress(
        rest_metric,
        sp.Matrix([temporal, transverse, 0, 0]),
        potential,
    ).applyfunc(jetify)
    rest_tt = sp.factor(2 * N**2 * rest_stress[0, 0])
    rest_xx = sp.factor(2 * rest_stress[1, 1])
    checks.check(
        "fresh rest equations isolate the potential and real-square sum",
        rest_tt == N**2 * a + b + 2 * potential
        and rest_xx == N**2 * a + b - 2 * potential
        and sp.factor((rest_tt + rest_xx) / 2) == N**2 * a + b
        and sp.factor((rest_tt - rest_xx) / 4) == potential,
    )
    checks.check(
        "positive square mutations make the rest vacuum guard sensitive",
        (N**2 * a + b).subs({a: 0, b: 0}) == 0
        and (N**2 * a + b).subs({a: 1, b: 0}) != 0
        and (N**2 * a + b).subs({a: 0, b: 1}) != 0,
    )
    rest_profile_metric = sp.diag(-n**-2, 1, 1, 1)
    _, rest_scalar, rest_einstein = _curvature(rest_profile_metric, coordinates)
    rest_expected = sp.diag(0, 0, -kernel, -kernel)
    checks.check(
        "fresh rest curvature leaves yy and zz to force the kernel to zero",
        (rest_einstein - rest_expected).applyfunc(sp.simplify) == sp.zeros(4)
        and sp.simplify(rest_scalar - 2 * kernel) == 0,
    )

    reciprocal_second = sp.factor(sp.diff(1 / n, x, 2))
    checks.check(
        "fresh reciprocal differentiation classifies the zero-curvature profiles",
        sp.simplify(reciprocal_second + kernel / n) == 0,
    )
    positive_x = sp.symbols("positive_x", positive=True)
    slope, intercept = sp.symbols("A B", positive=True)
    affine_index = 1 / (slope * positive_x + intercept)
    affine_kernel = sp.factor(
        (
            affine_index * sp.diff(affine_index, positive_x, 2)
            - 2 * sp.diff(affine_index, positive_x) ** 2
        )
        / affine_index**2
    )
    checks.check(
        "fresh reciprocal-affine family realizes the complete vacuum geometry locus",
        affine_kernel == 0
        and sp.diff(1 / affine_index, positive_x, 2) == 0,
    )

    wrong_stress = (
        sp.Matrix([temporal, transverse, 0, 0])
        * sp.Matrix([temporal, transverse, 0, 0]).T
        - general_metric
        * (
            (
                sp.Matrix([temporal, transverse, 0, 0]).T
                * general_metric.inv()
                * sp.Matrix([temporal, transverse, 0, 0])
            )[0]
            / 2
            - potential
        )
    ).applyfunc(sp.simplify)
    checks.check(
        "wrong potential sign mutation changes the stress tensor",
        (wrong_stress - _fresh_scalar_stress(
            general_metric,
            sp.Matrix([temporal, transverse, 0, 0]),
            potential,
        ) - 2 * general_metric * potential).applyfunc(sp.simplify)
        == sp.zeros(4),
    )
    relaxed = sp.solve(conditions[1:], [a, b, potential], dict=True)
    checks.check(
        "fresh canonical relaxation differs from SC1 guard A",
        len(relaxed) == 1
        and relaxed[0][a] == 0
        and sp.simplify(relaxed[0][b] + 2 * potential) == 0,
    )
    integer = sp.symbols("m", integer=True)
    checks.check(
        "fresh cosine-potential specialization is on shell at the vacuum locus",
        sp.simplify(1 - sp.cos(2 * sp.pi * integer)) == 0
        and sp.simplify(sp.sin(2 * sp.pi * integer)) == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
