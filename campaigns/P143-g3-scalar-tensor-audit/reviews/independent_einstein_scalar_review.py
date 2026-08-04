from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _geometry(
    metric: sp.Matrix,
    coordinates: tuple[sp.Symbol, ...],
) -> tuple[sp.Matrix, list[list[list[sp.Expr]]], sp.Matrix, sp.Expr, sp.Matrix, list[list[list[list[sp.Expr]]]]]:
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
    riemann_mixed = [
        [
            [
                [
                    sp.simplify(
                        sp.diff(christoffel[a][d][b], coordinates[c])
                        - sp.diff(christoffel[a][c][b], coordinates[d])
                        + sum(
                            christoffel[a][c][e] * christoffel[e][d][b]
                            - christoffel[a][d][e] * christoffel[e][c][b]
                            for e in range(dimension)
                        )
                    )
                    for d in range(dimension)
                ]
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
                sum(riemann_mixed[c][a][c][b] for c in range(dimension))
            )
    scalar = sp.simplify(
        sum(inverse[a, b] * ricci[a, b] for a in range(dimension) for b in range(dimension))
    )
    einstein = (ricci - metric * scalar / 2).applyfunc(sp.simplify)
    return inverse, christoffel, ricci, scalar, einstein, riemann_mixed


def _mixed_divergence(
    inverse: sp.Matrix,
    christoffel: list[list[list[sp.Expr]]],
    tensor_covariant: sp.Matrix,
    coordinates: tuple[sp.Symbol, ...],
) -> sp.Matrix:
    dimension = len(coordinates)
    mixed = (inverse * tensor_covariant).applyfunc(sp.simplify)
    result = sp.zeros(dimension, 1)
    for nu in range(dimension):
        result[nu] = sp.simplify(
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
    return result


def _diagonal_kretschmann(
    metric: sp.Matrix,
    inverse: sp.Matrix,
    riemann_mixed: list[list[list[list[sp.Expr]]]],
) -> sp.Expr:
    dimension = metric.rows
    result = 0
    for a in range(dimension):
        for b in range(dimension):
            for c in range(dimension):
                for d in range(dimension):
                    lowered = sp.simplify(metric[a, a] * riemann_mixed[a][b][c][d])
                    if lowered != 0:
                        result += (
                            inverse[a, a]
                            * inverse[b, b]
                            * inverse[c, c]
                            * inverse[d, d]
                            * lowered**2
                        )
    return sp.simplify(result)


def _scalar_stress(metric: sp.Matrix, gradient: sp.Matrix, potential: sp.Expr = sp.Integer(0)) -> sp.Matrix:
    inverse = metric.inv()
    norm = sp.simplify((gradient.T * inverse * gradient)[0])
    return (gradient * gradient.T - metric * (norm / 2 + potential)).applyfunc(sp.simplify)


def main() -> int:
    checks = CheckLedger("P143/C-STG-001 independent")
    time = sp.symbols("time", positive=True)
    x, y, z = sp.symbols("x y z", real=True)
    coordinates = (time, x, y, z)
    scale = sp.Function("a", positive=True)(time)
    metric = sp.diag(-1, scale**2, scale**2, scale**2)
    inverse, christoffel, _, ricci_scalar, einstein, riemann = _geometry(metric, coordinates)
    hubble = sp.diff(scale, time) / scale
    expected = sp.diag(
        3 * hubble**2,
        -scale**2 * (2 * sp.diff(hubble, time) + 3 * hubble**2),
        -scale**2 * (2 * sp.diff(hubble, time) + 3 * hubble**2),
        -scale**2 * (2 * sp.diff(hubble, time) + 3 * hubble**2),
    )
    checks.check(
        "direct four-dimensional curvature gives flat-FLRW Einstein tensor",
        (einstein - expected).applyfunc(sp.simplify) == sp.zeros(4),
    )
    checks.check(
        "contracted Bianchi identity closes before selecting a solution",
        _mixed_divergence(inverse, christoffel, einstein, coordinates) == sp.zeros(4, 1),
    )

    kappa, time_zero, scale_zero = sp.symbols(
        "kappa time_zero scale_zero", positive=True
    )
    scalar_zero = sp.symbols("scalar_zero", real=True)
    scale_solution = scale_zero * (time / time_zero) ** sp.Rational(1, 3)
    scalar_solution = scalar_zero + sp.sqrt(sp.Rational(2, 3) / kappa) * sp.log(
        time / time_zero
    )
    substitutions = {
        scale: scale_solution,
        sp.diff(scale, time): sp.diff(scale_solution, time),
        sp.diff(scale, time, 2): sp.diff(scale_solution, time, 2),
    }
    einstein_solution = einstein.applyfunc(
        lambda entry: sp.simplify(entry.subs(substitutions))
    )
    stress_solution = _scalar_stress(
        metric.subs(scale, scale_solution),
        sp.Matrix([sp.diff(scalar_solution, time), 0, 0, 0]),
    )
    checks.check(
        "independent stress closes every Einstein component",
        (einstein_solution - kappa * stress_solution).applyfunc(sp.simplify) == sp.zeros(4),
    )

    scalar_box = sp.simplify(
        -(
            sp.diff(scalar_solution, time, 2)
            + 3 * sp.diff(scale_solution, time) / scale_solution
            * sp.diff(scalar_solution, time)
        )
    )
    checks.check("independent scalar equation closes", scalar_box == 0)
    density = sp.simplify(stress_solution[0, 0])
    pressure = sp.simplify(stress_solution[1, 1] / scale_solution**2)
    checks.check(
        "independent continuity equation closes",
        density == pressure == 1 / (3 * kappa * time**2)
        and sp.simplify(
            sp.diff(density, time)
            + 3 * sp.diff(scale_solution, time) / scale_solution * (density + pressure)
        ) == 0,
    )

    ricci_solution = sp.simplify(ricci_scalar.subs(substitutions))
    kretschmann = _diagonal_kretschmann(metric, inverse, riemann)
    kretschmann_solution = sp.simplify(kretschmann.subs(substitutions))
    checks.check(
        "direct curvature invariants expose singular and flat limits",
        ricci_solution == -sp.Rational(2, 3) / time**2
        and kretschmann_solution == sp.Rational(20, 27) / time**4
        and sp.limit(kretschmann_solution, time, 0, dir="+") == sp.oo
        and sp.limit(kretschmann_solution, time, sp.oo) == 0,
    )
    stress_trace = sp.simplify(
        sp.trace(metric.subs(scale, scale_solution).inv() * stress_solution)
    )
    checks.check(
        "Einstein trace and scalar trace agree",
        sp.simplify(-ricci_solution - kappa * stress_trace) == 0,
    )

    def exponent_residual(exponent: sp.Expr) -> sp.Expr:
        trial_hubble = exponent / time
        return sp.simplify(3 * trial_hubble**2 - kappa * density)

    checks.mutation_sensitive(
        "expansion exponent is independently load bearing",
        lambda exponent: exponent_residual(exponent) == 0,
        sp.Rational(1, 3),
        [sp.Rational(1, 2), sp.Rational(2, 3), sp.Integer(0)],
    )
    ghost_stress = -stress_solution
    checks.check(
        "ghost mutation fails the direct Einstein equation",
        ghost_stress[0, 0].is_negative is True
        and (einstein_solution - kappa * ghost_stress).applyfunc(sp.simplify) != sp.zeros(4),
    )

    transverse = 1 + sp.exp(-x**2) / 5
    source_metric = sp.diag(-1, 1, transverse, transverse)
    _, _, _, _, source_einstein, _ = _geometry(source_metric, coordinates)
    source_index = 1 + sp.Rational(3, 10) * sp.exp(-x**2)
    source_scalar = sp.log(source_index)
    source_stress = _scalar_stress(
        source_metric, sp.Matrix([0, sp.diff(source_scalar, x), 0, 0])
    )
    fitted = sp.simplify((source_einstein[0, 0] / source_stress[0, 0]).subs(x, 1))
    source_residual = (source_einstein - fitted * source_stress).applyfunc(
        lambda entry: sp.simplify(entry.subs(x, 1))
    )
    source_sqrt_minus_g = sp.sqrt(-source_metric.det())
    source_scalar_residual = sp.simplify(
        sp.diff(source_sqrt_minus_g * sp.diff(source_scalar, x), x)
        / source_sqrt_minus_g
    ).subs(x, 1)
    checks.check(
        "independent reconstruction rejects G3 one-point source match",
        fitted.is_negative is True
        and source_residual[0, 0] == 0
        and source_residual[1, 1] != 0
        and source_residual[2, 2] != 0
        and source_residual[3, 3] != 0
        and sp.simplify(source_scalar_residual) != 0,
    )
    checks.check(
        "homogeneous exact solution is extensive rather than a localized breather",
        density.is_positive is True
        and sp.integrate(scale_solution**3 * density, (x, -sp.oo, sp.oo)) == sp.oo,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
