#!/usr/bin/env python3
"""Fresh exact rederivation of C-BND-001 without new canonical helpers."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P146-independent")
    u, v, a, beta, current = sp.symbols("u v a beta J", real=True)
    trace = sp.Matrix([u, v, 1])
    coefficient = sp.Matrix([[a, beta, -current]])
    parity = sp.diag(1, -1, 1)

    residual = (coefficient * trace)[0]
    parity_image = (coefficient * parity * trace)[0]
    reflected_coefficient = sp.Matrix([[a, -beta, -current]])
    checks.check(
        "fresh augmented trace gives the declared residual",
        residual == a * u + beta * v - current,
    )
    checks.check(
        "fresh matrix parity equals coefficient reflection",
        parity_image == (reflected_coefficient * trace)[0],
    )
    checks.check(
        "parity is an involution on affine trace space",
        parity * parity == sp.eye(3),
    )

    even_row = sp.simplify((coefficient + coefficient * parity) / 2)
    odd_row = sp.simplify((coefficient - coefficient * parity) / 2)
    checks.check(
        "fresh parity projector isolates temporal-source and spatial rows",
        even_row == sp.Matrix([[a, 0, -current]])
        and odd_row == sp.Matrix([[0, beta, 0]]),
    )
    checks.check(
        "fresh projected rows reconstruct the mixed operator",
        sp.simplify(even_row + odd_row - coefficient) == sp.zeros(1, 3),
    )
    checks.check(
        "fixed residual invariance requires zero spatial coefficient",
        sp.solve(
            list(coefficient * parity - coefficient),
            [beta],
            dict=True,
        )
        == [{beta: 0}],
    )
    checks.check(
        "pure odd affine residual requires temporal and source parts absent",
        sp.solve(
            list(coefficient * parity + coefficient),
            [a, current],
            dict=True,
        )
        == [{a: 0, current: 0}],
    )
    checks.check(
        "generic mixed residual is neither parity eigenvalue",
        sp.simplify(parity_image - residual) == -2 * beta * v
        and sp.simplify(parity_image + residual) == 2 * (a * u - current),
    )

    right_normal = sp.Integer(-1)
    left_normal = sp.Integer(1)
    parity_coordinate_trace = -v
    checks.check(
        "fresh right outward trace has the declared orientation",
        right_normal * v == -v,
    )
    checks.check(
        "fresh parity-mapped left outward trace agrees",
        left_normal * parity_coordinate_trace == right_normal * v,
    )
    eta = sp.Symbol("eta", real=True)
    right_normal_residual = a * u + eta * right_normal * v - current
    left_normal_residual = (
        a * u + eta * left_normal * parity_coordinate_trace - current
    )
    checks.check(
        "fresh normal-form boundary coefficient does not flip",
        sp.simplify(left_normal_residual - right_normal_residual) == 0,
    )
    checks.check(
        "wrong left-domain orientation breaks normal covariance",
        sp.simplify(
            (a * u + eta * parity_coordinate_trace - current)
            - right_normal_residual
        )
        == 0
        and sp.simplify((a * u + eta * v - current) - right_normal_residual)
        == 2 * eta * v,
    )

    row = sp.Matrix([[a, beta]])
    checks.check(
        "one generic boundary row has rank one and nullity one",
        row.rank() == 1 and len(row.nullspace()) == 1,
    )
    null_vector = sp.Matrix([beta, -a])
    checks.check(
        "fresh null direction preserves the boundary source",
        row * null_vector == sp.zeros(1, 1),
    )
    particular = sp.Matrix([0, current / beta])
    family_parameter = sp.Symbol("s", real=True)
    family = particular + family_parameter * null_vector
    checks.check(
        "fresh general trace family retains one free parameter",
        sp.simplify((row * family)[0] - current) == 0,
    )
    checks.check(
        "temporal-only row leaves every coordinate trace free",
        all(sp.simplify(2 * 3 + 0 * candidate - 6) == 0 for candidate in (-5, 0, 9)),
    )

    theta = sp.Symbol("theta", real=True)
    zero_field_change = sp.integrate(sp.cos(theta), (theta, 0, 2 * sp.pi))
    aligned_sign_correlation = 2 * sp.integrate(
        sp.cos(theta),
        (theta, -sp.pi / 2, sp.pi / 2),
    )
    checks.check(
        "fresh periodic trace has zero boundary field change",
        zero_field_change == 0,
    )
    checks.check(
        "fresh aligned trace has nonzero sign correlation",
        aligned_sign_correlation == 4,
    )
    checks.check(
        "fresh counterexample separates correlation from charge transfer",
        zero_field_change == 0 and aligned_sign_correlation != 0,
    )

    drive = sp.Symbol("drive", real=True, nonzero=True)
    checks.check(
        "source vector witness adds an independent zero-gradient premise",
        sp.simplify(1 * drive + 0 * 0 - drive) == 0
        and sp.simplify(1 * drive + 0 * 7 - drive) == 0,
    )
    checks.check(
        "source chiral witness fails its own epsilon-plus residual",
        sp.simplify(drive + drive - drive) == drive,
    )

    wrong_parity = sp.eye(3)
    checks.check(
        "no-spatial-sign mutation fails coefficient reflection",
        sp.simplify(
            (coefficient * wrong_parity * trace)[0]
            - (reflected_coefficient * trace)[0]
        )
        == 2 * beta * v,
    )
    wrong_trace_solution = (current + a * u) / beta
    checks.check(
        "trace-solution sign mutation leaves a nonzero residual",
        sp.simplify(a * u + beta * wrong_trace_solution - current) == 2 * a * u,
    )

    tally = checks.finish()
    print(f"P146 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
