"""Independent exact P082 review without importing charge-trace APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _table() -> tuple[tuple[int, sp.Expr, sp.Expr], ...]:
    return (
        (3, sp.Rational(1, 2), sp.Rational(1, 6)),
        (3, -sp.Rational(1, 2), sp.Rational(1, 6)),
        (3, 0, -sp.Rational(2, 3)),
        (3, 0, sp.Rational(1, 3)),
        (1, sp.Rational(1, 2), -sp.Rational(1, 2)),
        (1, -sp.Rational(1, 2), -sp.Rational(1, 2)),
        (1, 0, sp.Integer(1)),
    )


def _weighted(table: tuple[tuple[int, sp.Expr, sp.Expr], ...], fn: object) -> sp.Expr:
    return sp.simplify(sum(mult * fn(t3, y) for mult, t3, y in table))


def main() -> int:
    checks = CheckLedger("P082-INDEPENDENT")
    table = _table()
    s2 = _weighted(table, lambda t3, _y: t3**2)
    sy = _weighted(table, lambda _t3, y: y**2)
    s3 = sp.Rational(1, 2) * (2 + 1 + 1)
    checks.check(
        "fresh supplied-table traces are two two and ten thirds",
        s2 == s3 == 2 and sy == sp.Rational(10, 3),
    )

    c = sp.Symbol("C", positive=True)
    inverse_2 = c * s2
    inverse_y = c * sy
    ratio = sp.simplify(inverse_2 / inverse_y)
    checks.check(
        "fresh common zero-baseline law gives three fifths only conditionally",
        ratio == sp.Rational(3, 5),
    )
    checks.check(
        "fresh conditional coupling angle is three eighths",
        sp.simplify(ratio / (1 + ratio)) == sp.Rational(3, 8),
    )

    rho = sp.Symbol("rho", positive=True)
    sy_rescaled = sp.simplify(rho**2 * sy)
    coupling_ratio_rescaled = sp.simplify(inverse_2 / (c * sy_rescaled))
    checks.check(
        "fresh common law is covariant under every Abelian scale",
        coupling_ratio_rescaled == sp.Rational(3, 5) / rho**2,
    )
    target = sp.Symbol("target", positive=True)
    target_rho = sp.sqrt(sp.Rational(3, 5) / target)
    checks.check(
        "fresh rescaling realizes every positive coupling-coordinate target",
        sp.simplify(coupling_ratio_rescaled.subs(rho, target_rho) - target) == 0,
    )

    gy = sp.Symbol("gY", positive=True)
    charge_products = tuple(
        sp.simplify((gy / rho) * (rho * y) - gy * y)
        for _mult, _t3, y in table
    )
    checks.check(
        "fresh inverse coupling transform preserves every coupled charge",
        charge_products == (0,) * len(table),
    )
    checks.check(
        "fresh coupled trace norm is invariant",
        sp.simplify((gy / rho) ** 2 * sy_rescaled - gy**2 * sy) == 0,
    )

    canonical_rho = sp.sqrt(sp.Rational(3, 5))
    checks.check(
        "fresh canonical scale equalizes coordinates by construction",
        sp.simplify(sy_rescaled.subs(rho, canonical_rho)) == s2
        and sp.simplify(coupling_ratio_rescaled.subs(rho, canonical_rho)) == 1,
    )
    electric_trace_covariant = _weighted(
        table,
        lambda t3, y: (t3 + (1 / rho) * (rho * y)) ** 2,
    )
    checks.check(
        "fresh covariant electric coordinate preserves the original quotient",
        sp.simplify(s2 / electric_trace_covariant - sp.Rational(3, 8)) == 0,
    )

    c2, cy = sp.symbols("C2 CY", positive=True)
    independent = sp.factor(c2 * s2 / (cy * sy))
    checks.check(
        "fresh sector coefficients retain an arbitrary ratio",
        independent == 3 * c2 / (5 * cy),
    )
    k2, ky = sp.symbols("K2 KY", nonnegative=True)
    affine = sp.factor((k2 + c2 * s2) / (ky + cy * sy))
    checks.check(
        "fresh additive baselines retain two further free coordinates",
        {k2, ky, c2, cy} <= affine.free_symbols
        and sp.simplify(affine.subs({k2: 0, ky: 0, c2: c, cy: c}) - ratio) == 0,
    )
    checks.check(
        "fresh single-baseline counterexample breaks three fifths",
        sp.simplify(affine.subs({k2: 1, ky: 0, c2: c, cy: c}) - sp.Rational(3, 5)) != 0,
    )

    s3_mutated = sp.Rational(1, 2) * (2 + 1)
    checks.check(
        "fresh supplied-colour mutation changes the strong trace",
        s3_mutated == sp.Rational(3, 2) and s3_mutated != s2,
    )
    checks.check(
        "finite algebra has no regulator profile action or boundary scale provenance",
        not hasattr(table, "regulator")
        and not hasattr(table, "effective_action")
        and not hasattr(table, "boundary_scale"),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
