"""Independent P104 derivation and cubature without the canonical map API."""

from __future__ import annotations

import ast
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
import sympy as sp

from substrate_framework.verification import CheckLedger


def _pad_descending(coefficients: np.ndarray, size: int) -> np.ndarray:
    return np.pad(coefficients, (size - coefficients.size, 0))


def _adaptive_sphere_integrals(
    numerator_coefficients: list[complex],
    denominator_coefficients: list[complex],
    *,
    tolerance: float,
) -> tuple[float, float, float, float, int]:
    """Use direct and reciprocal charts with nested adaptive quadrature."""

    numerator = np.asarray(numerator_coefficients, dtype=np.complex128)
    denominator = np.asarray(denominator_coefficients, dtype=np.complex128)
    size = max(numerator.size, denominator.size)
    numerator = _pad_descending(numerator, size)
    denominator = _pad_descending(denominator, size)
    reciprocal_numerator = numerator[::-1]
    reciprocal_denominator = denominator[::-1]
    evaluations = 0

    def jacobian(u: float, phi: float) -> float:
        nonlocal evaluations
        evaluations += 1
        if u >= 0.0:
            p = numerator
            q = denominator
            radius = math.sqrt((1.0 - u) / (1.0 + u)) if u < 1.0 else 0.0
            coordinate = radius * complex(math.cos(phi), math.sin(phi))
        else:
            p = reciprocal_numerator
            q = reciprocal_denominator
            radius = math.sqrt((1.0 + u) / (1.0 - u)) if u > -1.0 else 0.0
            coordinate = radius * complex(math.cos(phi), -math.sin(phi))
        p_value = np.polyval(p, coordinate)
        q_value = np.polyval(q, coordinate)
        p_prime = np.polyval(np.polyder(p), coordinate)
        q_prime = np.polyval(np.polyder(q), coordinate)
        wronskian = p_prime * q_value - p_value * q_prime
        homogeneous_norm = abs(p_value) ** 2 + abs(q_value) ** 2
        return float(
            (1.0 + abs(coordinate) ** 2) ** 2
            * abs(wronskian) ** 2
            / homogeneous_norm**2
        )

    def integrate_power(power: int) -> tuple[float, float]:
        def polar_integral(u: float) -> float:
            value, _error = quad(
                lambda phi: jacobian(u, phi) ** power,
                0.0,
                2.0 * math.pi,
                epsabs=tolerance,
                epsrel=tolerance,
                limit=200,
            )
            return float(value)

        value, error = quad(
            polar_integral,
            -1.0,
            1.0,
            points=[0.0],
            epsabs=tolerance,
            epsrel=tolerance,
            limit=200,
        )
        return float(value / (4.0 * math.pi)), float(error / (4.0 * math.pi))

    area, area_error = integrate_power(1)
    angular, angular_error = integrate_power(2)
    return area, angular, area_error, angular_error, evaluations


def main() -> int:
    checks = CheckLedger("C-RMAP-001/002-INDEPENDENT")
    coordinate, radius = sp.symbols("z r", positive=True)
    coefficient = 2 * sp.I * sp.sqrt(3)
    cubic_numerator = sp.Poly(coordinate**4 + coefficient * coordinate**2 + 1, coordinate, extension=True)
    cubic_denominator = sp.Poly(coordinate**4 - coefficient * coordinate**2 + 1, coordinate, extension=True)
    cubic_gcd = sp.gcd(cubic_numerator, cubic_denominator)
    checks.check(
        "fresh polynomial route makes the cubic map coprime and degree four",
        cubic_gcd.degree() == 0
        and max(cubic_numerator.degree(), cubic_denominator.degree()) == 4,
    )
    shared_numerator = sp.Poly(coordinate * (coordinate + 1), coordinate)
    shared_denominator = sp.Poly(coordinate + 1, coordinate)
    shared_gcd = sp.gcd(shared_numerator, shared_denominator)
    checks.check(
        "fresh cancellation route distinguishes apparent and rational degree",
        shared_numerator.degree() == 2
        and shared_gcd.degree() == 1
        and sp.exquo(shared_numerator, shared_gcd).degree() == 1,
    )

    degree_two_jacobian = (
        4 * radius**2 * (1 + radius**2) ** 2 / (1 + radius**4) ** 2
    )
    degree_two_area = sp.integrate(
        2 * degree_two_jacobian * radius / (1 + radius**2) ** 2,
        (radius, 0, sp.oo),
    )
    degree_two_angular = sp.integrate(
        2 * degree_two_jacobian**2 * radius / (1 + radius**2) ** 2,
        (radius, 0, sp.oo),
    )
    checks.check(
        "fresh direct degree-two area integral equals two",
        degree_two_area == 2,
    )
    checks.check(
        "fresh direct degree-two angular integral is pi plus eight thirds",
        sp.simplify(degree_two_angular - sp.pi - sp.Rational(8, 3)) == 0,
    )
    checks.check(
        "fresh degree-two result lies strictly above the Cauchy degree bound",
        sp.simplify(degree_two_angular - 4).is_positive is True,
    )
    generic_degree = sp.Symbol("B", positive=True)
    inverse_degree = 1 / generic_degree
    beta_route = generic_degree**3 * (
        sp.beta(2 - inverse_degree, 2 + inverse_degree)
        + 2 * sp.beta(2, 2)
        + sp.beta(2 + inverse_degree, 2 - inverse_degree)
    )
    generic_formula = generic_degree**3 * (
        1
        + sp.gamma(2 - inverse_degree) * sp.gamma(2 + inverse_degree)
    ) / 3
    checks.check(
        "fresh Euler-beta route derives the generic axial formula and controls",
        sp.simplify(sp.expand_func(beta_route) - generic_formula) == 0
        and sp.simplify(generic_formula.subs(generic_degree, 1) - 1) == 0
        and sp.simplify(generic_formula.subs(generic_degree, 2) - degree_two_angular)
        == 0,
    )

    identity = _adaptive_sphere_integrals([1.0, 0.0], [1.0], tolerance=1.0e-10)
    checks.check(
        "fresh adaptive identity integral reaches exact area and I",
        abs(identity[0] - 1.0) < 2.0e-12
        and abs(identity[1] - 1.0) < 2.0e-12,
    )
    axial_two = _adaptive_sphere_integrals([1.0, 0.0, 0.0], [1.0], tolerance=1.0e-10)
    checks.check(
        "fresh adaptive degree-two route agrees with the exact direct integral",
        abs(axial_two[0] - 2.0) < 2.0e-11
        and abs(axial_two[1] - float(degree_two_angular)) / float(degree_two_angular)
        < 2.0e-11,
    )

    cubic_numeric_coefficient = 2j * math.sqrt(3.0)
    numerator = [1.0, 0.0, cubic_numeric_coefficient, 0.0, 1.0]
    denominator = [1.0, 0.0, -cubic_numeric_coefficient, 0.0, 1.0]
    tolerances = (1.0e-7, 1.0e-9, 1.0e-11)
    cubic = [
        _adaptive_sphere_integrals(
            numerator,
            denominator,
            tolerance=tolerance,
        )
        for tolerance in tolerances
    ]
    checks.check(
        "fresh adaptive cubic solves remain finite and report evaluations",
        all(
            all(math.isfinite(value) for value in result[:4]) and result[4] > 0
            for result in cubic
        ),
    )
    checks.check(
        "fresh reciprocal-chart cubic area converges to degree four",
        abs(cubic[-1][0] - 4.0) < 2.0e-12
        and cubic[-1][2] < 2.0e-11,
    )
    checks.check(
        "fresh adaptive cubic angular value is tolerance stable",
        max(result[1] for result in cubic) - min(result[1] for result in cubic)
        < 5.0e-11
        and cubic[-1][3] < 1.0e-9,
    )
    reference = 20.6496264884189
    checks.check(
        "fresh adaptive cubic route agrees with the separately refined tensor value",
        abs(cubic[-1][1] - reference) / reference < 2.0e-12,
    )

    phase = 0.41
    powers = np.arange(4, -1, -1)
    rotated_numerator = (
        np.asarray(numerator) * np.exp(1j * phase * powers) * np.exp(-0.33j)
    ).tolist()
    rotated_denominator = (
        np.asarray(denominator) * np.exp(1j * phase * powers)
    ).tolist()
    rotated = _adaptive_sphere_integrals(
        rotated_numerator,
        rotated_denominator,
        tolerance=1.0e-9,
    )
    checks.check(
        "fresh domain and target axis rotations preserve the cubic integrals",
        abs(rotated[0] - cubic[-1][0]) < 2.0e-11
        and abs(rotated[1] - cubic[-1][1]) / cubic[-1][1] < 2.0e-11,
    )
    mutated = _adaptive_sphere_integrals(
        [1.0, 0.0, 3.2j, 0.0, 1.0],
        [1.0, 0.0, -3.2j, 0.0, 1.0],
        tolerance=1.0e-8,
    )
    checks.check(
        "fresh coefficient mutation preserves degree area but changes I",
        abs(mutated[0] - 4.0) < 2.0e-9
        and mutated[1] > cubic[-1][1] + 0.1,
    )
    shifted = _adaptive_sphere_integrals(
        [1.0, 0.0, 0.6],
        [1.0],
        tolerance=1.0e-9,
    )
    checks.check(
        "fresh shifted map is only a higher same-degree comparator",
        abs(shifted[0] - 2.0) < 2.0e-10
        and shifted[1] > float(degree_two_angular),
    )

    source_identity = 0.99792
    source_degree_two = 5.79616
    source_degree_four = 20.62952
    checks.check(
        "fresh exact controls reject source endpoint-loss decimals as final values",
        abs(source_identity - 1.0) > 1.0e-3
        and abs(source_degree_two - float(degree_two_angular)) / float(degree_two_angular)
        > 1.0e-3
        and abs(source_degree_four - cubic[-1][1]) / cubic[-1][1] > 5.0e-4,
    )
    checks.check(
        "one higher deformation and invariant rotations cannot prove global minimization",
        shifted[1] > float(degree_two_angular)
        and abs(rotated[1] - cubic[-1][1]) < 1.0e-9,
    )
    review_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    checks.check(
        "independent review imports no canonical rational-map implementation",
        all(
            not isinstance(node, ast.ImportFrom)
            or node.module != "substrate_framework.rational_maps"
            for node in ast.walk(review_tree)
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
