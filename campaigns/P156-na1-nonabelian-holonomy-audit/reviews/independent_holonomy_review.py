#!/usr/bin/env python3
"""Fresh continuous and segmented derivation for proposed C-HOL-001."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _matrix_zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(sp.expand_complex(entry)) == 0 for entry in matrix)


def run() -> int:
    checks = CheckLedger("P156-independent")
    sigma_1 = sp.ImmutableMatrix([[0, 1], [1, 0]])
    sigma_2 = sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]])
    sigma_3 = sp.ImmutableMatrix([[1, 0], [0, -1]])
    identity = sp.ImmutableMatrix(sp.eye(2))
    t_1, t_2, t_3 = sigma_1 / 2, sigma_2 / 2, sigma_3 / 2

    s = sp.Symbol("s", real=True)
    gauge = sp.ImmutableMatrix(
        sp.cos(s / 2) * identity + sp.I * sp.sin(s / 2) * sigma_1
    )
    connection = t_2
    original_transport = sp.ImmutableMatrix(
        sp.cos(s / 2) * identity + sp.I * sp.sin(s / 2) * sigma_2
    )
    transformed_connection = sp.ImmutableMatrix(
        (
            gauge * connection * gauge.H
            - sp.I * sp.diff(gauge, s) * gauge.H
        ).applyfunc(sp.simplify)
    )
    transformed_transport = sp.ImmutableMatrix(
        (gauge * original_transport).applyfunc(sp.simplify)
    )
    differential_residual = sp.ImmutableMatrix(
        (
            sp.diff(transformed_transport, s)
            - sp.I * transformed_connection * transformed_transport
        ).applyfunc(sp.simplify)
    )
    checks.check(
        "fresh continuous noncommuting gauge transform satisfies the path equation",
        _matrix_zero(differential_residual),
    )
    checks.check(
        "fresh endpoint prediction has the correct initial condition",
        transformed_transport.subs(s, 0) == identity,
    )
    wrong_connection = sp.ImmutableMatrix(
        (
            gauge * connection * gauge.H
            + sp.I * sp.diff(gauge, s) * gauge.H
        ).applyfunc(sp.simplify)
    )
    wrong_residual = sp.ImmutableMatrix(
        (
            sp.diff(transformed_transport, s)
            - sp.I * wrong_connection * transformed_transport
        ).applyfunc(sp.simplify)
    )
    checks.check(
        "fresh wrong inhomogeneous sign breaks the transport equation",
        not _matrix_zero(wrong_residual),
    )

    first = sp.I * sigma_1
    second = sp.I * sigma_2
    chronological = sp.ImmutableMatrix(second * first)
    swapped = sp.ImmutableMatrix(first * second)
    checks.check(
        "fresh Pauli products derive later-left order sensitivity",
        chronological == sp.I * sigma_3
        and swapped == -sp.I * sigma_3
        and chronological != swapped,
    )
    checks.check(
        "fresh trace counterexample cannot detect the order swap",
        sp.trace(chronological) == sp.trace(swapped) == 0,
    )
    reversed_path = sp.ImmutableMatrix(first.H * second.H)
    checks.check(
        "fresh reversed chronological path is the inverse transporter",
        reversed_path == chronological.H
        and reversed_path * chronological == identity,
    )

    u_0 = sp.I * sigma_3
    u_1 = sp.I * sigma_1
    u_2 = sp.I * sigma_2
    transformed_first = sp.ImmutableMatrix(u_1 * first * u_0.H)
    transformed_second = sp.ImmutableMatrix(u_2 * second * u_1.H)
    transformed_product = sp.ImmutableMatrix(transformed_second * transformed_first)
    checks.check(
        "fresh endpoint factors telescope in the segmented construction",
        transformed_product == u_2 * chronological * u_0.H,
    )
    checks.check(
        "fresh omitted initial endpoint factor is a counterexample",
        transformed_product != u_2 * chronological,
    )

    alpha, beta = sp.symbols("alpha beta", real=True)
    commuting_product = sp.diag(
        sp.exp(sp.I * beta / 2),
        sp.exp(-sp.I * beta / 2),
    ) * sp.diag(
        sp.exp(sp.I * alpha / 2),
        sp.exp(-sp.I * alpha / 2),
    )
    commuting_sum = sp.diag(
        sp.exp(sp.I * (alpha + beta) / 2),
        sp.exp(-sp.I * (alpha + beta) / 2),
    )
    checks.check(
        "fresh diagonal route proves the commuting collapse",
        _matrix_zero(sp.ImmutableMatrix(commuting_product - commuting_sum)),
    )

    angle = sp.Symbol("a", real=True)
    factor_1 = sp.cos(angle / 2) * identity + sp.I * sp.sin(angle / 2) * sigma_1
    factor_2 = sp.cos(angle / 2) * identity + sp.I * sp.sin(angle / 2) * sigma_2
    ordered = sp.ImmutableMatrix((factor_2 * factor_1).applyfunc(sp.simplify))
    naive = sp.ImmutableMatrix(
        (
            sp.cos(angle / sp.sqrt(2)) * identity
            + sp.I * sp.sin(angle / sp.sqrt(2)) * (sigma_1 + sigma_2) / sp.sqrt(2)
        ).applyfunc(sp.simplify)
    )
    coefficient = sp.ImmutableMatrix(
        (ordered - naive).applyfunc(
            lambda entry: sp.simplify(sp.diff(entry, angle, 2).subs(angle, 0) / 2)
        )
    )
    checks.check(
        "fresh series route derives the noncommuting quadratic coefficient",
        coefficient == sp.I * t_3 / 2,
    )

    fundamental = sp.ImmutableMatrix((sp.I * 2 * sp.pi * t_3).exp())
    adjoint = sp.ImmutableMatrix(
        (sp.I * 2 * sp.pi * sp.diag(1, 0, -1)).exp()
    )
    checks.check(
        "fresh representation route separates fundamental and adjoint center images",
        fundamental == -identity
        and adjoint == sp.eye(3)
        and sp.trace(fundamental) / 2 == -1
        and sp.trace(adjoint) / 3 == 1,
    )
    checks.check(
        "fresh raw traces retain carrier dimension",
        sp.trace(fundamental) == -2 and sp.trace(adjoint) == 3,
    )

    source_orient_pi = sp.diag(-sp.I, sp.I)
    positive_transport_pi = sp.ImmutableMatrix((sp.I * sp.pi * t_3).exp())
    checks.check(
        "fresh noncentral probe distinguishes opposite orientation conventions",
        positive_transport_pi == -source_orient_pi,
    )
    checks.check(
        "fresh same-matrix countermodels leave interpretation independent",
        all(
            value == chronological
            for value in {
                "abstract": chronological,
                "declared_internal": sp.I * sigma_3,
                "synthetic": second * first,
            }.values()
        ),
    )

    return checks.finish()


if __name__ == "__main__":
    tally = run()
    print(f"P156 INDEPENDENT ALL {tally} CHECKS PASS")
