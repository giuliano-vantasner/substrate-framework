"""Independent exact P081 review without importing charge-trace APIs."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _weighted_sum(table: tuple[tuple[str, int, sp.Expr, sp.Expr], ...], fn: object) -> sp.Expr:
    return sp.simplify(sum(mult * fn(t3, y) for _label, mult, t3, y in table))


def _table() -> tuple[tuple[str, int, sp.Expr, sp.Expr], ...]:
    return (
        ("Q_L_up", 3, sp.Rational(1, 2), sp.Rational(1, 6)),
        ("Q_L_down", 3, -sp.Rational(1, 2), sp.Rational(1, 6)),
        ("u_R_conj", 3, 0, -sp.Rational(2, 3)),
        ("d_R_conj", 3, 0, sp.Rational(1, 3)),
        ("L_neutrino", 1, sp.Rational(1, 2), -sp.Rational(1, 2)),
        ("L_electron", 1, -sp.Rational(1, 2), -sp.Rational(1, 2)),
        ("e_R_conj", 1, 0, sp.Integer(1)),
    )


def main() -> int:
    checks = CheckLedger("P081-INDEPENDENT")
    table = _table()
    trace_t3 = _weighted_sum(table, lambda t3, _y: t3**2)
    trace_y = _weighted_sum(table, lambda _t3, y: y**2)
    trace_cross = _weighted_sum(table, lambda t3, y: t3 * y)
    trace_q = _weighted_sum(table, lambda t3, y: (t3 + y) ** 2)

    checks.check(
        "fresh multiplicity count gives fifteen supplied states",
        sum(mult for _label, mult, _t3, _y in table) == 15,
    )
    checks.check(
        "fresh weighted sums give all four exact traces",
        trace_t3 == 2
        and trace_y == sp.Rational(10, 3)
        and trace_cross == 0
        and trace_q == sp.Rational(16, 3),
    )
    checks.check(
        "fresh expansion retains the cross term before cancellation",
        trace_q == trace_t3 + 2 * trace_cross + trace_y,
    )
    checks.check(
        "fresh finite table quotient is exactly three eighths",
        trace_t3 / trace_q == sp.Rational(3, 8),
    )

    rho, coupling = sp.symbols("rho g_Y", positive=True)
    fixed_q = _weighted_sum(table, lambda t3, y: (t3 + rho * y) ** 2)
    checks.check(
        "fresh fixed-coefficient rescaling produces the full quotient family",
        fixed_q == 2 + sp.Rational(10, 3) * rho**2
        and sp.simplify(trace_t3 / fixed_q - 3 / (3 + 5 * rho**2)) == 0,
    )
    covariant_q = _weighted_sum(
        table,
        lambda t3, y: (t3 + (1 / rho) * (rho * y)) ** 2,
    )
    checks.check(
        "fresh covariant electric-coordinate change preserves Q",
        sp.simplify(covariant_q - trace_q) == 0,
    )
    checks.check(
        "fresh inverse coupling change preserves all generator products",
        all(
            sp.simplify((coupling / rho) * (rho * y) - coupling * y) == 0
            for _label, _mult, _t3, y in table
        ),
    )
    checks.check(
        "fresh coupled trace norm is invariant",
        sp.simplify(
            (coupling / rho) ** 2 * rho**2 * trace_y
            - coupling**2 * trace_y
        )
        == 0,
    )

    first_moment = _weighted_sum(table, lambda _t3, y: y)
    third_moment = _weighted_sum(table, lambda _t3, y: y**3)
    checks.check(
        "fresh homogeneous moments vanish for the supplied table",
        first_moment == third_moment == 0,
    )
    checks.check(
        "fresh rescaling leaves homogeneous zero moments zero",
        sp.simplify(rho * first_moment) == 0
        and sp.simplify(rho**3 * third_moment) == 0,
    )
    mixed_su2 = sp.Rational(1, 2) * (
        3 * sp.Rational(1, 6) - sp.Rational(1, 2)
    )
    mixed_su3 = sp.Rational(1, 2) * (
        2 * sp.Rational(1, 6)
        - sp.Rational(2, 3)
        + sp.Rational(1, 3)
    )
    checks.check(
        "fresh mixed linear sums also leave normalization free",
        mixed_su2 == mixed_su3 == 0
        and rho * mixed_su2 == rho * mixed_su3 == 0,
    )

    g2, gy = sp.symbols("g2 gy", positive=True)
    coupling_angle = gy**2 / (g2**2 + gy**2)
    trace_angle = trace_t3 / (trace_t3 + trace_y)
    residual = sp.factor(coupling_angle - trace_angle)
    checks.check(
        "fresh angle subtraction isolates the extra coupling condition",
        sp.simplify(
            residual
            - (gy**2 * trace_y - g2**2 * trace_t3)
            / ((g2**2 + gy**2) * (trace_t3 + trace_y))
        )
        == 0,
    )
    checks.check(
        "fresh solve requires gY squared over g2 squared equal three fifths",
        sp.solve(sp.Eq(coupling_angle, trace_angle), gy**2, dict=True)
        == [{gy**2: sp.Rational(3, 5) * g2**2}],
    )
    checks.check(
        "equal couplings give one half rather than three eighths",
        coupling_angle.subs(gy, g2) == sp.Rational(1, 2)
        and trace_angle == sp.Rational(3, 8),
    )

    common = sp.Symbol("C", positive=True)
    g2_common_sq = 1 / (common * trace_t3)
    gy_common_sq = 1 / (common * trace_y)
    common_angle = sp.simplify(
        gy_common_sq / (g2_common_sq + gy_common_sq)
    )
    checks.check(
        "fresh common inverse-trace law yields the quotient only conditionally",
        common_angle == trace_angle == sp.Rational(3, 8),
    )
    c2, cy = sp.symbols("C2 CY", positive=True)
    unequal_angle = sp.simplify(
        (1 / (cy * trace_y))
        / (1 / (c2 * trace_t3) + 1 / (cy * trace_y))
    )
    checks.check(
        "fresh unequal kinetic coefficients retain a free ratio",
        sp.simplify(
            unequal_angle
            - c2 * trace_t3 / (c2 * trace_t3 + cy * trace_y)
        )
        == 0
        and sp.simplify(unequal_angle.subs({c2: 2, cy: 7}) - trace_angle) != 0,
    )

    no_colour = tuple(
        (label, 1 if label.startswith(("Q_L", "u_R", "d_R")) else mult, t3, y)
        for label, mult, t3, y in table
    )
    no_colour_ratio = _weighted_sum(no_colour, lambda t3, _y: t3**2) / _weighted_sum(
        no_colour, lambda t3, y: (t3 + y) ** 2
    )
    checks.check(
        "fresh colour mutation reproduces nine twenty-eighths",
        no_colour_ratio == sp.Rational(9, 28),
    )
    dropped = tuple(row for row in table if row[0] != "e_R_conj")
    dropped_ratio = _weighted_sum(dropped, lambda t3, _y: t3**2) / _weighted_sum(
        dropped, lambda t3, y: (t3 + y) ** 2
    )
    checks.check(
        "fresh omitted-singlet mutation reproduces six thirteenths",
        dropped_ratio == sp.Rational(6, 13),
    )
    flipped = tuple(
        (label, mult, t3, -1 if label == "e_R_conj" else y)
        for label, mult, t3, y in table
    )
    flipped_ratio = _weighted_sum(flipped, lambda t3, _y: t3**2) / _weighted_sum(
        flipped, lambda t3, y: (t3 + y) ** 2
    )
    checks.check(
        "fresh nonzero sign flip refutes the source only-at-zero guard",
        flipped_ratio == sp.Rational(3, 8)
        and _weighted_sum(flipped, lambda _t3, y: y) == -2,
    )
    checks.check(
        "finite table arithmetic contains no representation or action derivation",
        all(isinstance(label, str) for label, _mult, _t3, _y in table)
        and not hasattr(table, "gauge_action")
        and not hasattr(table, "kinetic_normalization"),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
