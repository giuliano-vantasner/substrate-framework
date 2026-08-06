#!/usr/bin/env python3
"""Fresh GC6 review without importing the C-MIX-004 canonical API."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.special import gamma
import sympy as sp

from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-42/"
    "bridge_GC6_consequence_and_verdict.py"
)
SOURCE_SHA256 = "e09822946b9b44ade21632c7db42d2061e493b112a13fab9a44e74a6a6d18b17"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def zero(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(sp.expand_complex(entry)) == 0 for entry in matrix)


def off_diagonal_zero(matrix: sp.MatrixBase) -> bool:
    return all(
        sp.simplify(matrix[row, column]) == 0
        for row in range(matrix.rows)
        for column in range(matrix.cols)
        if row != column
    )


def analytic_poschl_couplings(
    spacing: float,
    *,
    epsabs: float = 1e-11,
    epsrel: float = 1e-11,
) -> tuple[float, float, float]:
    """Use exact whole-line Pöschl ground shapes and adaptive quadrature."""

    depth = 12.0
    width = 0.7
    index = (np.sqrt(1.0 + 4.0 * depth * width**2) - 1.0) / 2.0
    normalization = np.sqrt(
        gamma(index + 0.5) / (width * np.sqrt(np.pi) * gamma(index))
    )
    kappa = np.sqrt(0.5 - 0.45**2)
    amplitude = 2.0 * np.sqrt(6.0) * kappa
    anchors = (0.0, spacing, 2.0 * spacing)
    phases = np.exp(1j * np.asarray((0.0, 2.0 * np.pi / 3.0, 4.0 * np.pi / 3.0)))

    def sech(value: float) -> float:
        if abs(value) > 700.0:
            return 0.0
        return float(1.0 / np.cosh(value))

    errors: list[float] = []
    couplings: list[np.ndarray] = []
    for profile_center in (-1.0, 0.0, 1.0):
        matrix = np.zeros((3, 3), dtype=np.float64)
        for a, left_center in enumerate(anchors):
            for b, right_center in enumerate(anchors):
                def integrand(coordinate: float) -> float:
                    left = normalization * sech((coordinate - left_center) / width) ** index
                    right = normalization * sech((coordinate - right_center) / width) ** index
                    profile = amplitude * sech(kappa * (coordinate - profile_center))
                    return left * right * profile

                matrix[a, b], error = quad(
                    integrand,
                    -np.inf,
                    np.inf,
                    epsabs=epsabs,
                    epsrel=epsrel,
                    limit=300,
                )
                errors.append(float(error))
        couplings.append(matrix)
    mass = sum(
        phase * matrix for phase, matrix in zip(phases, couplings, strict=True)
    )
    left, singular_values, right_adjoint = np.linalg.svd(mass)
    right = right_adjoint.conj().T
    ratios = []
    for coupling in couplings:
        transformed = left.conj().T @ coupling @ right
        off = max(
            abs(transformed[a, b])
            for a in range(3)
            for b in range(3)
            if a != b
        )
        diagonal = max(abs(transformed[a, a]) for a in range(3))
        ratios.append(float(off / diagonal))
    return (
        float(singular_values[0] / singular_values[-1]),
        max(ratios),
        max(errors),
    )


def main() -> int:
    checks = CheckLedger("P213-GC6-INDEPENDENT-FLAVOR-REVIEW")
    checks.check("source hash remains independently pinned", digest(SOURCE) == SOURCE_SHA256)
    source = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(SOURCE))
    audit = audit_numpy_trapezoid_compatibility(source, filename=str(SOURCE))
    checks.check(
        "independent inventory remains six checks and one assertion",
        sum(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            for node in ast.walk(tree)
        )
        == 6
        and sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    checks.check(
        "independent compatibility audit finds no quadrature name",
        audit.legacy_references
        == audit.current_references
        == audit.eager_legacy_default_fallbacks
        == 0,
    )

    y11, y12, y21, y22 = sp.symbols("y11 y12 y21 y22")
    z11, z12, z21, z22 = sp.symbols("z11 z12 z21 z22")
    first = sp.Matrix([[y11, y12], [y21, y22]])
    second = sp.Matrix([[z11, z12], [z21, z22]])
    v1, v2 = sp.symbols("v1 v2")
    rotation = sp.Matrix([[1, 1], [-1, 1]]) / sp.sqrt(2)
    mass = v1 * first + v2 * second
    transformed_mass = sp.simplify(rotation.T * mass * rotation)
    transformed_sum = sp.simplify(
        v1 * rotation.T * first * rotation + v2 * rotation.T * second * rotation
    )
    checks.check(
        "fresh distributive derivation reconstructs every mass-basis entry",
        zero(transformed_mass - transformed_sum),
    )

    a = sp.symbols("a", nonzero=True)
    cancellation_first = sp.Matrix([[1, a], [a, 2]])
    cancellation_second = sp.Matrix([[0, -a], [-a, 1]])
    checks.check(
        "fresh cancellation countermodel has diagonal sum and nondiagonal parts",
        off_diagonal_zero(cancellation_first + cancellation_second)
        and not off_diagonal_zero(cancellation_first)
        and not off_diagonal_zero(cancellation_second),
    )
    checks.check(
        "fresh weight mutation breaks the cancellation",
        not off_diagonal_zero(cancellation_first + 2 * cancellation_second),
    )
    aligned_reference = sp.Matrix([[0, 1], [1, 0]])
    aligned_pair = (aligned_reference, -aligned_reference)
    aligned_mass = aligned_pair[0] + aligned_pair[1]
    checks.check(
        "fresh zero-coefficient aligned family leaves individual off-diagonal couplings",
        zero(aligned_mass)
        and all(not off_diagonal_zero(matrix) for matrix in aligned_pair),
    )

    unitary = sp.Matrix([[1, sp.I], [sp.I, 1]]) / sp.sqrt(2)
    diagonal = sp.diag(1, 2)
    symmetric_mass = sp.simplify(unitary * diagonal * unitary.T)
    real_source = symmetric_mass.applyfunc(lambda entry: sp.simplify(sp.re(entry)))
    imaginary_source = symmetric_mass.applyfunc(lambda entry: sp.simplify(sp.im(entry)))
    correct = (
        sp.simplify(unitary.adjoint() * real_source * unitary.conjugate()),
        sp.simplify(unitary.adjoint() * imaginary_source * unitary.conjugate()),
    )
    wrong = (
        sp.simplify(unitary.adjoint() * real_source * unitary),
        sp.simplify(unitary.adjoint() * imaginary_source * unitary),
    )
    checks.check(
        "fresh Takagi derivation uses the conjugate right basis",
        zero(unitary.adjoint() * symmetric_mass * unitary.conjugate() - diagonal),
    )
    checks.check(
        "fresh exact countermodel separates correct and source transformations",
        all(off_diagonal_zero(matrix) for matrix in correct)
        and any(not off_diagonal_zero(matrix) for matrix in wrong),
    )

    first_projector = sp.diag(1, 0)
    second_projector = sp.diag(0, 1)
    checks.check(
        "fresh degenerate-basis witness preserves mass and changes individual diagonality",
        rotation.T * (first_projector + second_projector) * rotation == sp.eye(2)
        and not off_diagonal_zero(rotation.T * first_projector * rotation),
    )

    ng, nh = sp.symbols("ng nh", positive=True, integer=True)
    s1 = sp.Rational(4, 3) * ng + sp.Rational(1, 10) * nh
    s2 = sp.Rational(4, 3) * ng + sp.Rational(1, 6) * nh
    boundary = sp.factor(s2 / (s2 + sp.Rational(5, 3) * s1))
    checks.check(
        "fresh trace reduction gives the exact conditional count family",
        sp.simplify(
            boundary - 3 * (8 * ng + nh) / (2 * (32 * ng + 3 * nh))
        )
        == 0,
    )
    checks.check(
        "fresh trace family reproduces all source rational endpoints",
        [boundary.subs({ng: 3, nh: value}) for value in range(4)]
        == [sp.Rational(3, 8), sp.Rational(25, 66), sp.Rational(13, 34), sp.Rational(27, 70)],
    )
    checks.check(
        "fresh trace derivative is positive only conditionally on positive generation count",
        sp.factor(sp.diff(boundary, nh))
        == 12 * ng / (32 * ng + 3 * nh) ** 2,
    )

    selected = [analytic_poschl_couplings(value) for value in (3.0, 4.0, 5.0, 6.0)]
    expected = (
        0.014240123852561425,
        0.0021279861136508523,
        0.0011688866083767273,
        0.000018871146738993443,
    )
    checks.check(
        "analytic whole-line modes reproduce corrected selected-spacing ratios",
        max(abs(result[1] - value) for result, value in zip(selected, expected)) < 2e-12,
    )
    checks.check(
        "adaptive quadrature reports controlled absolute errors",
        max(result[2] for result in selected) < 1.2e-11,
    )
    tighter = analytic_poschl_couplings(6.0, epsabs=2e-12, epsrel=2e-12)
    checks.check(
        "analytic-route tolerance refinement stabilizes the d-six ratio",
        abs(tighter[1] - selected[-1][1]) / selected[-1][1] < 2e-8,
    )
    dense = [analytic_poschl_couplings(value)[1] for value in (4.75, 5.0, 5.25)]
    checks.check(
        "independent whole-line route confirms the nonmonotone spacing witness",
        dense[0] < dense[1] < dense[2],
    )
    checks.check(
        "small corrected ratio remains a conditional numeric output",
        selected[-1][1] < 1e-4
        and selected[-1][0] > 10
        and selected[-1][1] != 0.0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
