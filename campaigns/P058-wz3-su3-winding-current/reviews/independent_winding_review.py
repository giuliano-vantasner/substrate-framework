"""Independent exact and numerical review for P058.

This script deliberately does not import canonical WZW or winding-current
helpers.  It rebuilds the quaternion generator and hedgehog trace from Pauli
matrices, expands the graded closure kernel, and uses NumPy's current
``trapezoid`` API only as regression evidence for a separately exact charge.
"""

from __future__ import annotations

import itertools

import numpy as np
import sympy as sp

from substrate_framework.verification import CheckLedger


def permutation_sign(order: tuple[int, ...]) -> int:
    inversions = sum(
        order[first] > order[second]
        for first in range(len(order))
        for second in range(first + 1, len(order))
    )
    return -1 if inversions % 2 else 1


def alternating_trace(matrices: tuple[sp.Matrix, ...]) -> sp.Expr:
    total = sp.Integer(0)
    for order in itertools.permutations(range(len(matrices))):
        product = sp.eye(matrices[0].rows)
        for index in order:
            product *= matrices[index]
        total += permutation_sign(order) * sp.trace(product)
    return sp.simplify(total)


def quaternion_matrix(point: tuple[sp.Expr, ...]) -> sp.Matrix:
    a0, a1, a2, a3 = point
    return sp.Matrix(
        [
            [a0 + sp.I * a3, a2 + sp.I * a1, 0],
            [-a2 + sp.I * a1, a0 - sp.I * a3, 0],
            [0, 0, 1],
        ]
    )


def quaternion_differential(tangent: tuple[int, int, int, int]) -> sp.Matrix:
    v0, v1, v2, v3 = tangent
    return sp.Matrix(
        [
            [v0 + sp.I * v3, v2 + sp.I * v1, 0],
            [-v2 + sp.I * v1, v0 - sp.I * v3, 0],
            [0, 0, 0],
        ]
    )


def boundary_charge(inner: sp.Expr, outer: sp.Expr) -> sp.Expr:
    primitive = lambda value: value - sp.sin(value) * sp.cos(value)
    return sp.simplify((primitive(inner) - primitive(outer)) / sp.pi)


def numeric_profile(radius: np.ndarray, scale: float) -> tuple[np.ndarray, np.ndarray]:
    profile = 2.0 * np.arctan((scale / radius) ** 2)
    derivative = -4.0 * scale**2 * radius / (radius**4 + scale**4)
    return profile, derivative


def numeric_charge(points: int, scale: float) -> tuple[float, float]:
    radius = np.geomspace(1.0e-4, 1.0e2, points)
    profile, derivative = numeric_profile(radius, scale)
    radial_density = -(2.0 / np.pi) * np.sin(profile) ** 2 * derivative
    numerical = float(np.trapezoid(radial_density, radius))
    primitive = lambda value: value - np.sin(value) * np.cos(value)
    exact_truncated = float((primitive(profile[0]) - primitive(profile[-1])) / np.pi)
    return numerical, exact_truncated


def main() -> int:
    ledger = CheckLedger("P058-INDEPENDENT")
    a0, a1, a2, a3 = sp.symbols("a0 a1 a2 a3", real=True)
    norm_squared = a0**2 + a1**2 + a2**2 + a3**2
    quaternion = quaternion_matrix((a0, a1, a2, a3))
    ledger.check(
        "quaternion block has exact SU3 membership on the unit sphere",
        sp.factor(quaternion.det()) == norm_squared
        and sp.simplify(quaternion.H * quaternion)
        == sp.diag(norm_squared, norm_squared, 1),
    )

    first_column = quaternion[:, 0]
    projected = sp.Matrix(
        [
            sp.re(first_column[0]),
            sp.im(first_column[0]),
            sp.re(first_column[1]),
            sp.im(first_column[1]),
        ]
    )
    ledger.check(
        "first-column projection has positive degree one",
        projected.jacobian((a0, a1, a2, a3)).det() == 1,
    )

    north = quaternion_matrix((sp.Integer(1), sp.Integer(0), sp.Integer(0), sp.Integer(0)))
    frame = (
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    )
    left_values = tuple(north.H * quaternion_differential(tangent) for tangent in frame)
    raw_density = alternating_trace(left_values)
    raw_period = sp.simplify(raw_density * 2 * sp.pi**2)
    coefficient = sp.simplify(-1 / raw_period)
    ledger.check(
        "generator density and period derive the winding coefficient",
        raw_density == 12
        and raw_period == 24 * sp.pi**2
        and coefficient == -1 / (24 * sp.pi**2)
        and sp.simplify(coefficient * raw_period) == -1,
    )

    generic_symbols = sp.symbols("m0:16", real=True)
    generic = tuple(
        sp.Matrix(2, 2, generic_symbols[4 * index : 4 * index + 4])
        for index in range(4)
    )
    trace_four = alternating_trace(generic)
    symmetrized_four = sum(
        (
            sp.trace(
                generic[order[0]]
                * generic[order[1]]
                * generic[order[2]]
                * generic[order[3]]
            )
            for order in itertools.permutations(range(4))
        ),
        sp.Integer(0),
    )
    derivative_terms = tuple(
        (-1) ** (position + position * (4 - position)) for position in range(3)
    )
    ledger.check(
        "graded Leibniz and cyclic terms close the actual trace three-form",
        derivative_terms == (1, 1, 1)
        and sum(derivative_terms) == 3
        and trace_four == 0
        and sp.simplify(symmetrized_four) != 0,
    )

    radius, theta, phi = sp.symbols("r theta phi", positive=True)
    profile = sp.Function("F", real=True)(radius)
    sigma1 = sp.Matrix([[0, 1], [1, 0]])
    sigma2 = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma3 = sp.Matrix([[1, 0], [0, -1]])
    radial_pauli = (
        sp.sin(theta) * sp.cos(phi) * sigma1
        + sp.sin(theta) * sp.sin(phi) * sigma2
        + sp.cos(theta) * sigma3
    )
    field = sp.cos(profile) * sp.eye(2) + sp.I * sp.sin(profile) * radial_pauli
    left = tuple(sp.simplify(field.H * sp.diff(field, coordinate)) for coordinate in (radius, theta, phi))
    raw_hedgehog = alternating_trace(left)
    angular_trace = sp.integrate(
        sp.integrate(raw_hedgehog, (phi, 0, 2 * sp.pi)),
        (theta, 0, sp.pi),
    )
    radial_density = sp.simplify(
        (-angular_trace / (24 * sp.pi**2)).rewrite(sp.cos)
    )
    expected_radial = -2 * sp.sin(profile) ** 2 * sp.diff(profile, radius) / sp.pi
    print(f"independent signed radial density: {radial_density}")
    print(
        "independent radial residual: "
        f"{sp.simplify(sp.expand_complex(radial_density - expected_radial))}"
    )
    ledger.check(
        "independent Pauli trace derives the signed hedgehog radial density",
        sp.simplify(sp.expand_complex(radial_density - expected_radial)) == 0,
    )

    variable = sp.symbols("f", real=True)
    primitive = (variable - sp.sin(variable) * sp.cos(variable)) / sp.pi
    ledger.check(
        "the boundary formula is the exact radial antiderivative",
        sp.simplify(sp.diff(primitive, variable) - 2 * sp.sin(variable) ** 2 / sp.pi)
        == 0
        and boundary_charge(sp.pi, 0) == 1
        and boundary_charge(2 * sp.pi, 0) == 2
        and boundary_charge(0, 0) == 0,
    )
    ledger.check(
        "orientation and endpoint mutations change the charge",
        boundary_charge(0, sp.pi) == -1
        and boundary_charge(sp.pi / 2, 0) == sp.Rational(1, 2)
        and sp.simplify(-coefficient * raw_period) == 1,
    )

    point_counts = (501, 1001, 2001, 4001, 8001)
    regressions = [numeric_charge(points, 1.0) for points in point_counts]
    errors = [abs(numerical - exact) for numerical, exact in regressions]
    print(f"trapezoid point counts and errors: {list(zip(point_counts, errors, strict=True))}")
    ledger.check(
        "current NumPy trapezoid regression refines toward the exact truncated charge",
        all(errors[index + 1] < errors[index] for index in range(len(errors) - 1))
        and errors[-1] < 2.0e-6,
    )
    deformations = [numeric_charge(8001, scale) for scale in (0.7, 1.0, 1.4)]
    ledger.check(
        "smooth scale deformations preserve the boundary-controlled charge",
        max(abs(numerical - exact) for numerical, exact in deformations) < 2.0e-6
        and max(abs(exact - 1.0) for _, exact in deformations) < 2.0e-10,
    )

    color_count = sp.symbols("N_c", positive=True)
    consistent_up = (1 + 1 / color_count) / 2
    consistent_down = (1 / color_count - 1) / 2
    consistent_anomaly = sp.simplify(
        color_count * (consistent_up**2 - consistent_down**2)
    )
    fixed_charge_anomaly = sp.simplify(
        color_count * (sp.Rational(2, 3) ** 2 - sp.Rational(-1, 3) ** 2)
    )
    ledger.check(
        "the source anomaly arithmetic does not by itself force color count",
        consistent_anomaly == 1
        and fixed_charge_anomaly == color_count / 3
        and sp.solve(sp.Eq(fixed_charge_anomaly, 1), color_count) == [3],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
