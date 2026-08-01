#!/usr/bin/env python3
"""Independent Noether and coordinate-Jacobian review of P049."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def matrix_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> int:
    ledger = CheckLedger("P049-INDEPENDENT")

    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    potential_function = sp.Function("U")
    potential = potential_function(field)
    field_t = sp.diff(field, t)
    field_x = sp.diff(field, x)
    lagrangian = (field_t**2 - field_x**2) / 2 - potential
    metric = sp.diag(1, -1)
    gradient = sp.Matrix([field_t, field_x])
    covariant = gradient * gradient.T - metric * lagrangian
    contravariant = metric * covariant * metric
    equation = (
        sp.diff(field, t, 2)
        - sp.diff(field, x, 2)
        + sp.diff(potential_function(field), field)
    )
    divergence = sp.Matrix(
        [
            sp.diff(contravariant[0, nu], t)
            + sp.diff(contravariant[1, nu], x)
            for nu in range(2)
        ]
    )
    ledger.check(
        "a general-potential Noether derivation factorizes the Cartesian divergence",
        matrix_zero(divergence - sp.Matrix([field_t * equation, -field_x * equation])),
    )

    cartesian_from_null = sp.Matrix(
        [
            [sp.Rational(1, 2), sp.Rational(1, 2)],
            [sp.Rational(1, 2), -sp.Rational(1, 2)],
        ]
    )
    null_tensor = sp.simplify(cartesian_from_null.T * covariant * cartesian_from_null)
    ledger.check(
        "an independent tensor-coordinate transform fixes the null components",
        sp.simplify(null_tensor[0, 0] - (field_t + field_x) ** 2 / 4) == 0
        and sp.simplify(null_tensor[1, 1] - (field_t - field_x) ** 2 / 4) == 0
        and sp.simplify(null_tensor[0, 1] - potential / 2) == 0,
    )

    def d_plus(expression: sp.Expr) -> sp.Expr:
        return (sp.diff(expression, t) + sp.diff(expression, x)) / 2

    def d_minus(expression: sp.Expr) -> sp.Expr:
        return (sp.diff(expression, t) - sp.diff(expression, x)) / 2

    balance_plus = sp.simplify(d_minus(null_tensor[0, 0]) + d_plus(null_tensor[0, 1]))
    balance_minus = sp.simplify(d_plus(null_tensor[1, 1]) + d_minus(null_tensor[0, 1]))
    ledger.check(
        "the general-potential null balances factorize independently",
        sp.simplify(balance_plus - (field_t + field_x) * equation / 4) == 0
        and sp.simplify(balance_minus - (field_t - field_x) * equation / 4) == 0,
    )

    sine_potential = 1 - sp.cos(field)
    sine_null = null_tensor.subs(potential, sine_potential)
    source_plus = ((field_t + field_x) / 2) ** 2 / 2
    source_minus = ((field_t - field_x) / 2) ** 2 / 2
    source_theta = (sp.cos(field) - 1) / 4
    ledger.check(
        "the NC2 auxiliary definitions are a uniform half-rescaling of canonical balance",
        sp.simplify(source_plus - sine_null[0, 0] / 2) == 0
        and sp.simplify(source_minus - sine_null[1, 1] / 2) == 0
        and sp.simplify(source_theta + sine_null[0, 1] / 2) == 0,
    )
    ledger.check(
        "the source's printed energy bridge is not the canonical energy density",
        sp.simplify(
            source_plus
            + source_minus
            + sine_potential
            - ((field_t**2 + field_x**2) / 2 + sine_potential)
        )
        != 0,
    )

    parity_field_t = field_t.subs(x, -x)
    parity_field_x = -field_x.subs(x, -x)
    parity_plus = (parity_field_t + parity_field_x) ** 2 / 4
    parity_minus = (parity_field_t - parity_field_x) ** 2 / 4
    ledger.check(
        "direct parity substitution exchanges null stresses without selecting one",
        sp.simplify(parity_plus - null_tensor[1, 1].subs(x, -x)) == 0
        and sp.simplify(parity_minus - null_tensor[0, 0].subs(x, -x)) == 0,
    )

    u, v = sp.symbols("u v", real=True)
    massless = sp.Function("psi")(u, v)
    ledger.check(
        "potential deletion, not small amplitude, yields separately conserved null stresses",
        sp.diff(sp.diff(massless, u) ** 2, v).subs(sp.diff(massless, u, v), 0)
        == 0
        and sp.diff(sp.diff(massless, v) ** 2, u).subs(
            sp.diff(massless, u, v),
            0,
        )
        == 0,
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
