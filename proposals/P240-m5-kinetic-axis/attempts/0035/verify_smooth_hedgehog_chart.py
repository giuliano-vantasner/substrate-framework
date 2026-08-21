"""Exact regularity audit for the spectral-Cartan hedgehog clock chart."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent


def frobenius_squared(matrix: sp.MatrixBase) -> sp.Expr:
    return sp.expand(sp.trace(matrix.T * matrix))


def main() -> int:
    ledger = CheckLedger("P240/attempt-0035/smooth-hedgehog-chart")
    theta = sp.symbols("theta", real=True)
    sine, cosine = sp.sin(theta), sp.cos(theta)
    director = sp.Matrix([sine, 0, cosine])
    polar = sp.Matrix([cosine, 0, -sine])
    azimuthal = sp.Matrix([0, 1, 0])
    lambda_n, lambda_t, split = sp.symbols("lambda_n lambda_t Delta", real=True)
    rotation_z = sp.Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]])

    uncorrected = (
        lambda_n * director * director.T
        + (lambda_t + split) * polar * polar.T
        + (lambda_t - split) * azimuthal * azimuthal.T
    )
    phi_derivative = rotation_z * uncorrected + uncorrected * rotation_z.T
    physical_phi_norm = sp.trigsimp(frobenius_squared(phi_derivative) / sine**2)
    pole_coefficient = sp.simplify(
        sp.limit(sine**2 * physical_phi_norm, theta, 0, dir="+")
    )
    ledger.check("constant tangential split has a nonzero exact pole coefficient", pole_coefficient == 8 * split**2)

    radial_split = sp.symbols("d", real=True)
    corrected = uncorrected.subs(split, radial_split * sine**2)
    corrected_phi = rotation_z * corrected + corrected * rotation_z.T
    corrected_physical_norm = sp.trigsimp(
        frobenius_squared(corrected_phi) / sine**2
    )
    corrected_pole = sp.simplify(
        sp.limit(corrected_physical_norm, theta, 0, dir="+")
    )
    ledger.check(
        "sin(theta)^2 split factor removes the pole",
        sp.simplify(corrected_pole - 2 * (lambda_n - lambda_t) ** 2) == 0,
    )
    ledger.check("axis repair does not delete the off-axis split", sp.simplify(corrected.subs(theta, sp.pi / 2).diff(radial_split)) != sp.zeros(3))

    x, y, z, radius = sp.symbols("x y z r", real=True, nonzero=True)
    n = sp.Matrix([x, y, z]) / radius
    axis = sp.Matrix([0, 0, 1])
    cross = axis.cross(n)
    cos_theta = z / radius
    polar_numerator = cos_theta * n - axis
    split_tensor = sp.simplify(
        polar_numerator * polar_numerator.T - cross * cross.T
    )
    ledger.check(
        "axis-repaired split has no residual symmetry-axis denominator",
        all(
            not sp.denom(sp.cancel(value)).has(x, y)
            for value in split_tensor
        ),
    )
    scaled_split = sp.simplify(radius**4 * split_tensor)
    scaled_split_on_shell = scaled_split.applyfunc(
        lambda value: sp.cancel(value.subs(radius**2, x**2 + y**2 + z**2))
    )
    ledger.check(
        "r^4 times the repaired split has polynomial Cartesian components",
        all(sp.denom(value) == 1 for value in scaled_split_on_shell),
    )
    scaled_director = (radius**2 * n * n.T).applyfunc(sp.cancel)
    ledger.check("r^2 times n*n^T has polynomial Cartesian components", all(sp.denom(value) == 1 for value in scaled_director))

    normalized_radius = sp.symbols("t", nonnegative=True)
    q_mode, tangent_mode, split_mode = sp.symbols("Q B D", real=True)
    q_profile = normalized_radius**2 + normalized_radius**2 * (1 - normalized_radius**2) * q_mode
    tangent_profile = (1 - normalized_radius**2) * tangent_mode
    split_profile = normalized_radius**4 * (1 - normalized_radius**2) * split_mode
    ledger.check("director anisotropy is O(r^2) at the core and one at the boundary", q_profile.subs(normalized_radius, 0) == 0 and q_profile.subs(normalized_radius, 1) == 1)
    ledger.check("common tangent profile has an even core and zero outer value", sp.diff(tangent_profile, normalized_radius).subs(normalized_radius, 0) == 0 and tangent_profile.subs(normalized_radius, 1) == 0)
    ledger.check("split profile is O(r^4) at the core and zero at the boundary", all(sp.diff(split_profile, normalized_radius, order).subs(normalized_radius, 0) == 0 for order in range(4)) and split_profile.subs(normalized_radius, 1) == 0)

    clock_generator = sp.Matrix(
        [
            [0, -director[2], director[1]],
            [director[2], 0, -director[0]],
            [-director[1], director[0], 0],
        ]
    )
    clock_response = sp.simplify(
        clock_generator * corrected + corrected * clock_generator.T
    )
    clock_norm = sp.trigsimp(frobenius_squared(clock_response))
    ledger.check("clock response is the exact tangential eigenvalue-gap square", sp.simplify(clock_norm - 8 * radial_split**2 * sine**4) == 0)
    ledger.check("clock response vanishes on the repaired axis", clock_response.subs(theta, 0) == sp.zeros(3))
    ledger.check("clock response remains nonzero off axis when the split is nonzero", clock_response.subs({theta: sp.pi / 2, radial_split: 1}) != sp.zeros(3))

    result = {
        "campaign": "P240",
        "attempt": "0035",
        "candidate": "D_fixed_j_two_clock_smooth_hedgehog_chart",
        "uncorrected_pole": "8*Delta^2/sin(theta)^2",
        "axis_repair": "Delta(r,theta)=d(r)*sin(theta)^2",
        "repaired_pole_limit": "2*(lambda_n-lambda_t)^2",
        "core_factors": {
            "director_anisotropy": "O(r^2)",
            "common_tangent": "even in r",
            "tangential_split": "O(r^4)",
        },
        "clock_response_norm": "8*d(r)^2*sin(theta)^4",
        "verdict": "smooth_parameter_free_galerkin_chart_open",
        "scope": "Exact representation regularity only; no stationary field or interaction is established.",
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
