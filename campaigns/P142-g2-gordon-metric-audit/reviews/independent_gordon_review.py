from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _curvature(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]):
    """Direct Christoffel, Ricci, scalar, and covariant Einstein reconstruction."""

    dimension = len(coordinates)
    inverse = metric.inv()
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
        sum(inverse[a, b] * ricci[a, b] for a in range(dimension) for b in range(dimension))
    )
    einstein = (ricci - metric * scalar / 2).applyfunc(sp.simplify)
    return inverse, christoffel, ricci, scalar, einstein


def _mixed_divergence(
    metric_inverse: sp.Matrix,
    christoffel: list[list[list[sp.Expr]]],
    einstein_covariant: sp.Matrix,
    coordinates: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    """Return the contracted Bianchi expression nabla_mu G^mu_nu."""

    dimension = len(coordinates)
    mixed = (metric_inverse * einstein_covariant).applyfunc(sp.simplify)
    divergence = sp.zeros(dimension, 1)
    for nu in range(dimension):
        divergence[nu] = sp.simplify(
            sum(
                sp.diff(mixed[mu, nu], coordinates[mu])
                + sum(
                    christoffel[mu][mu][lam] * mixed[lam, nu]
                    - christoffel[lam][mu][nu] * mixed[mu, lam]
                    for lam in range(dimension)
                )
                for mu in range(dimension)
            )
        )
    return divergence


def main() -> int:
    checks = CheckLedger("P142/C-GOR-001 independent")
    t, x, y, z = sp.symbols("t x y z", real=True)
    coordinates = (t, x, y, z)
    n = sp.Function("n", positive=True)(x)
    eta = sp.diag(-1, 1, 1, 1)
    velocity = sp.Rational(1, 2)
    gamma = 2 / sp.sqrt(3)
    u_up = sp.Matrix([gamma, 0, 0, gamma * velocity])
    u_down = eta * u_up

    contravariant = (eta + (1 - n**2) * u_up * u_up.T).applyfunc(sp.simplify)
    covariant_closed = (
        eta + (1 - n**-2) * u_down * u_down.T
    ).applyfunc(sp.simplify)
    checks.check("four velocity has mostly-plus norm minus one", (u_up.T * eta * u_up)[0] == -1)
    checks.check(
        "closed covariant form independently inverts inverse metric",
        (contravariant * covariant_closed).applyfunc(sp.simplify) == sp.eye(4),
    )
    checks.check("independent determinant is minus n squared", sp.simplify(contravariant.det()) == -n**2)

    inverse, christoffel, _, scalar, einstein = _curvature(
        covariant_closed, coordinates
    )
    kernel = sp.simplify((n * sp.diff(n, x, 2) - 2 * sp.diff(n, x) ** 2) / n**2)
    expected = sp.zeros(4)
    expected[0, 0] = -kernel / 3
    expected[0, 3] = 2 * kernel / 3
    expected[3, 0] = expected[0, 3]
    expected[2, 2] = -kernel
    expected[3, 3] = -4 * kernel / 3
    checks.check(
        "direct Christoffel curvature matches boost-derived tensor",
        (einstein - expected).applyfunc(sp.simplify) == sp.zeros(4),
    )
    checks.check("direct Ricci scalar is two times kernel", sp.simplify(scalar - 2 * kernel) == 0)
    checks.check(
        "contracted Bianchi identity closes componentwise",
        _mixed_divergence(inverse, christoffel, einstein, coordinates) == sp.zeros(4, 1),
    )

    witness = {n: 2, sp.diff(n, x): 1, sp.diff(n, x, 2): 0}
    evaluated = einstein.applyfunc(lambda entry: sp.simplify(entry.subs(witness)))
    checks.check("direct profile witness is one sixth", evaluated[0, 0] == sp.Rational(1, 6))
    checks.check(
        "direct profile has the conditional half-boost ratios",
        evaluated[0, 3] == -2 * evaluated[0, 0]
        and evaluated[2, 2] == 3 * evaluated[0, 0]
        and evaluated[3, 3] == 4 * evaluated[0, 0]
        and evaluated[1, 1] == 0,
    )

    wrong_contravariant = eta + (n**2 - 1) * u_up * u_up.T
    checks.check(
        "copied-sign determinant exposes the spurious pole",
        sp.simplify(wrong_contravariant.det() - (n**2 - 2)) == 0,
    )
    wrong_witness = wrong_contravariant.subs(n, 2)
    checks.check(
        "copied-sign n equals two witness is positive definite",
        all(value.is_positive is True for value in wrong_witness.eigenvals()),
    )
    checks.mutation_sensitive(
        "Gordon coefficient sign is load bearing",
        lambda coefficient: sp.simplify((eta + coefficient * u_up * u_up.T).det() + n**2) == 0,
        1 - n**2,
        [n**2 - 1, 1 + n**2, sp.Integer(0)],
    )

    coupling, density = sp.symbols("kappa rho", positive=True)
    from_tt = sp.solve(sp.Eq(evaluated[0, 0], coupling * density), coupling)[0]
    checks.check(
        "z-independent scalar source is incompatible with nonzero geometry tz",
        from_tt > 0 and evaluated[0, 3] != from_tt * 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
