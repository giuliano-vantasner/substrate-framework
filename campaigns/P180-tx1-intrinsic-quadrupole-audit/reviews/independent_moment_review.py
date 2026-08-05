#!/usr/bin/env python3
"""Independent angular rederivation and cubature for P180."""

from __future__ import annotations

import math

import numpy as np
import sympy as sp

from substrate_framework.verification import CheckLedger


def _sphere_rule(polar_order: int, azimuthal_order: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    u, weights_u = np.polynomial.legendre.leggauss(polar_order)
    phi = (np.arange(azimuthal_order) + 0.5) * 2 * np.pi / azimuthal_order
    weights = weights_u[:, None] * np.full((1, azimuthal_order), 2 * np.pi / azimuthal_order)
    uu = np.broadcast_to(u[:, None], weights.shape)
    pp = np.broadcast_to(phi[None, :], weights.shape)
    directions = np.asarray(
        (
            np.sqrt(1 - uu**2) * np.cos(pp),
            np.sqrt(1 - uu**2) * np.sin(pp),
            uu,
        )
    )
    return uu, pp, weights, directions


def _stf_tensor(field: np.ndarray, weights: np.ndarray, directions: np.ndarray) -> np.ndarray:
    result = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            kernel = directions[i] * directions[j]
            if i == j:
                kernel = kernel - 1 / 3
            result[i, j] = np.sum(field * kernel * weights)
    return result


def _homogeneous_jacobian(
    coordinate: np.ndarray,
    numerator: np.ndarray,
    denominator: np.ndarray,
) -> np.ndarray:
    p = np.polyval(numerator, coordinate)
    q = np.polyval(denominator, coordinate)
    pp = np.polyval(np.polyder(numerator), coordinate)
    qp = np.polyval(np.polyder(denominator), coordinate)
    return (
        (1 + np.abs(coordinate) ** 2) ** 2
        * np.abs(pp * q - p * qp) ** 2
        / (np.abs(p) ** 2 + np.abs(q) ** 2) ** 2
    )


def main() -> int:
    checks = CheckLedger("P180/C-RMOM-001-INDEPENDENT")
    u = sp.symbols("u", real=True)
    stereographic_squared = (1 - u) / (1 + u)
    jacobian_from_map = sp.simplify(
        4
        * stereographic_squared
        * (1 + stereographic_squared) ** 2
        / (1 + stereographic_squared**2) ** 2
    )
    expected = 4 * (1 - u**2) / (1 + u**2) ** 2
    checks.check("stereographic R=z squared Jacobian is independently reduced", sp.simplify(jacobian_from_map - expected) == 0)
    mean = sp.simplify(sp.integrate(expected, (u, -1, 1)) / 2)
    square_mean = sp.simplify(sp.integrate(expected**2, (u, -1, 1)) / 2)
    a1zz = sp.simplify(2 * sp.pi * sp.integrate(expected * (u**2 - sp.Rational(1, 3)), (u, -1, 1)))
    a2zz = sp.simplify(2 * sp.pi * sp.integrate(expected**2 * (u**2 - sp.Rational(1, 3)), (u, -1, 1)))
    checks.check("independent degree and squared mean are exact", mean == 2 and sp.simplify(square_mean - sp.pi - sp.Rational(8, 3)) == 0)
    checks.check("independent axial coefficients have exact values", a1zz == 8 * sp.pi * (3 * sp.pi - 10) / 3 and a2zz == 8 * sp.pi * (3 * sp.pi - 16) / 9)
    checks.check("both independent coefficients force the oblate sign", a1zz.is_negative is True and a2zz.is_negative is True)

    exact_a1 = np.diag([-float(a1zz) / 2, -float(a1zz) / 2, float(a1zz)])
    exact_a2 = np.diag([-float(a2zz) / 2, -float(a2zz) / 2, float(a2zz)])
    errors: list[float] = []
    for polar, azimuthal in ((24, 48), (48, 96), (96, 192)):
        uu, _, weights, directions = _sphere_rule(polar, azimuthal)
        numeric_jacobian = 4 * (1 - uu**2) / (1 + uu**2) ** 2
        a1 = _stf_tensor(numeric_jacobian, weights, directions)
        a2 = _stf_tensor(numeric_jacobian**2, weights, directions)
        errors.append(max(float(np.max(np.abs(a1 - exact_a1))), float(np.max(np.abs(a2 - exact_a2)))))
    checks.check("direct tensor sphere cubature converges to exact B2 tensors", errors[-1] < 2e-12 and errors[-1] <= errors[0])

    s3 = math.sqrt(3)
    numerator = np.asarray((1, 0, 2j * s3, 0, 1), dtype=np.complex128)
    denominator = np.asarray((1, 0, -2j * s3, 0, 1), dtype=np.complex128)
    cubic_norms: list[float] = []
    for polar, azimuthal in ((24, 48), (48, 96), (96, 192)):
        uu, phi, weights, directions = _sphere_rule(polar, azimuthal)
        coordinate = np.sqrt((1 - uu) / (1 + uu)) * np.exp(1j * phi)
        jacobian_four = _homogeneous_jacobian(coordinate, numerator, denominator)
        a1 = _stf_tensor(jacobian_four, weights, directions)
        a2 = _stf_tensor(jacobian_four**2, weights, directions)
        cubic_norms.append(max(float(np.max(np.abs(a1))), float(np.max(np.abs(a2)))))
    checks.check("declared degree-four map has a resolution-bounded rank-two null", cubic_norms[-1] < 2e-10 and cubic_norms[-1] <= cubic_norms[0])
    checks.check("numeric B4 null is not promoted as an exact symmetry theorem", cubic_norms[-1] > 0.0)

    radius, field_at_wall, negative_power = sp.symbols("R f_R p", positive=True)
    correct_monopole_squared_tail = field_at_wall**4 / (radius * (4 * negative_power + 1))
    source_monopole_squared_tail = field_at_wall**4 * radius / (4 * negative_power + 1)
    checks.check("independent tail dimensions expose the source R-squared error", sp.simplify(source_monopole_squared_tail / correct_monopole_squared_tail) == radius**2)
    checks.check("static intrinsic tensors have zero third time derivative", sp.diff(sp.diag(1, 1, -2), sp.Symbol("t"), 3) == sp.zeros(3))
    print(f"B2 cubature errors {errors}")
    print(f"B4 numeric STF norms {cubic_norms}")
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
