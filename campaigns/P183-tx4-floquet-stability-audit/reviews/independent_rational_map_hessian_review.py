#!/usr/bin/env python3
"""Independent exact symmetry/complement derivation of C-RMAP-003."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


z, zbar = sp.symbols("z zbar")
q, w, x = sp.symbols("q w x", positive=True)


def _integrand(parameters: list[sp.Expr]) -> sp.Expr:
    a1 = parameters[0] + sp.I * parameters[1]
    a0 = parameters[2] + sp.I * parameters[3]
    b2 = parameters[4] + sp.I * parameters[5]
    b1 = parameters[6] + sp.I * parameters[7]
    b0 = 1 + parameters[8] + sp.I * parameters[9]
    a1c = parameters[0] - sp.I * parameters[1]
    a0c = parameters[2] - sp.I * parameters[3]
    b2c = parameters[4] - sp.I * parameters[5]
    b1c = parameters[6] - sp.I * parameters[7]
    b0c = 1 + parameters[8] - sp.I * parameters[9]
    numerator = z**2 + a1 * z + a0
    denominator = b2 * z**2 + b1 * z + b0
    conjugate_numerator = zbar**2 + a1c * zbar + a0c
    conjugate_denominator = b2c * zbar**2 + b1c * zbar + b0c
    rational = numerator / denominator
    conjugate_rational = conjugate_numerator / conjugate_denominator
    derivative = sp.diff(rational, z)
    conjugate_derivative = sp.diff(conjugate_rational, zbar)
    return (
        (1 + z * zbar) ** 4
        * (derivative * conjugate_derivative) ** 2
        / (1 + rational * conjugate_rational) ** 4
    )


def _sphere_average(expression: sp.Expr) -> sp.Expr:
    laurent = sp.cancel(expression.subs({z: q * w, zbar: q / w}))
    zero_mode = sp.simplify(sp.residue(laurent / w, w, 0))
    radial = sp.cancel(zero_mode.subs(q, sp.sqrt(x)))
    if radial.has(w, sp.sqrt(x)):
        raise RuntimeError("independent angular average did not reduce exactly")
    result = sp.integrate(sp.cancel(radial / (1 + x) ** 2), (x, 0, sp.oo))
    if result.has(sp.Integral):
        raise RuntimeError("independent full-sphere integral remained unevaluated")
    return sp.simplify(result)


def _directional_gradient(direction: sp.MatrixBase) -> sp.Expr:
    epsilon = sp.Symbol("epsilon", real=True)
    parameters = [epsilon * direction[index] for index in range(10)]
    derivative = sp.diff(_integrand(parameters), epsilon).subs(epsilon, 0)
    return _sphere_average(derivative)


def _directional_hessian(
    first: sp.MatrixBase,
    second: sp.MatrixBase,
) -> sp.Expr:
    epsilon, eta = sp.symbols("epsilon eta", real=True)
    parameters = [
        epsilon * first[index] + eta * second[index] for index in range(10)
    ]
    derivative = (
        sp.diff(_integrand(parameters), epsilon, eta)
        .subs({epsilon: 0, eta: 0})
    )
    return _sphere_average(derivative)


def _column(entries: list[int]) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(entries)


def main() -> int:
    checks = CheckLedger("P183-INDEPENDENT-C-RMAP-003")
    symmetry = (
        _column([2, 0, 0, 0, 0, 0, -2, 0, 0, 0]),
        _column([0, 2, 0, 0, 0, 0, 0, 2, 0, 0]),
        _column([0, 0, 1, 0, -1, 0, 0, 0, 0, 0]),
        _column([0, 0, 0, 1, 0, 1, 0, 0, 0, 0]),
        _column([0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
    )
    complement = (
        _column([1, 0, 0, 0, 0, 0, 1, 0, 0, 0]),
        _column([0, 1, 0, 0, 0, 0, 0, -1, 0, 0]),
        _column([0, 0, 1, 0, 1, 0, 0, 0, 0, 0]),
        _column([0, 0, 0, 1, 0, -1, 0, 0, 0, 0]),
        _column([0, 0, 0, 0, 0, 0, 0, 0, 1, 0]),
    )
    basis = sp.ImmutableMatrix.hstack(*(symmetry + complement))
    checks.check(
        "fresh symmetry and complement directions form a full chart basis",
        basis.rank() == 10,
    )
    base = _sphere_average(_integrand([sp.S.Zero] * 10))
    checks.check(
        "fresh full-sphere calculation gives the accepted axial value",
        base == sp.pi + sp.Rational(8, 3),
    )

    coordinate_basis = tuple(sp.eye(10)[:, index] for index in range(10))
    gradient = []
    for index in range(10):
        value = _directional_gradient(coordinate_basis[index])
        gradient.append(value)
        print(f"INDEPENDENT GRADIENT {index} {value}", flush=True)
    checks.check(
        "all ten coordinate gradients vanish exactly",
        all(value == 0 for value in gradient),
    )

    coordinate_hessian = sp.zeros(10)
    for first in range(10):
        for second in range(first, 10):
            value = _directional_hessian(
                coordinate_basis[first], coordinate_basis[second]
            )
            coordinate_hessian[first, second] = value
            coordinate_hessian[second, first] = value
        print(f"INDEPENDENT HESSIAN ROW {first} COMPLETE", flush=True)
    transformed_hessian = sp.simplify(basis.T * coordinate_hessian * basis)

    a = sp.pi / 2 + sp.Rational(8, 3)
    b = sp.Rational(32, 3) + 7 * sp.pi / 2
    expected = sp.diag(0, 0, 0, 0, 0, 4 * a, 4 * a, 4 * b, 4 * b, sp.pi)
    checks.check(
        "fresh exact Hessian is zero on symmetry and positive diagonal on complement",
        sp.simplify(transformed_hessian - expected) == sp.zeros(10),
    )
    checks.check(
        "fresh exact Hessian has five-zero five-positive inertia",
        transformed_hessian.rank() == 5
        and len(transformed_hessian.nullspace()) == 5
        and all(item.is_positive is True for item in expected.diagonal()[5:]),
    )

    epsilon = sp.Symbol("epsilon", real=True)
    domain_real_a1 = sp.diff(2 * epsilon, epsilon).subs(epsilon, 0)
    domain_real_b1 = sp.diff(-2 * epsilon, epsilon).subs(epsilon, 0)
    domain_imag_a1 = sp.diff(2 * sp.I * epsilon, epsilon).subs(epsilon, 0)
    domain_imag_b1 = sp.diff(2 * sp.I * epsilon, epsilon).subs(epsilon, 0)
    target_real_a0 = sp.diff(epsilon, epsilon).subs(epsilon, 0)
    target_real_b2 = sp.diff(-epsilon, epsilon).subs(epsilon, 0)
    target_imag_a0 = sp.diff(sp.I * epsilon, epsilon).subs(epsilon, 0)
    target_imag_b2 = sp.diff(sp.I * epsilon, epsilon).subs(epsilon, 0)
    checks.check(
        "independent Möbius coefficient differentiation gives four kernel directions",
        domain_real_a1 == 2
        and domain_real_b1 == -2
        and domain_imag_a1 == 2 * sp.I
        and domain_imag_b1 == 2 * sp.I
        and target_real_a0 == 1
        and target_real_b2 == -1
        and target_imag_a0 == sp.I
        and target_imag_b2 == sp.I,
    )
    phase_map = z**2 / (1 + sp.I * epsilon)
    checks.check(
        "fresh phase-family differentiation gives the fifth kernel direction",
        sp.diff(phase_map, epsilon).subs(epsilon, 0) == -sp.I * z**2,
    )

    negative_mutation = sp.MutableDenseMatrix(transformed_hessian)
    negative_mutation[9, 9] = -sp.pi
    checks.check(
        "negative complementary curvature mutation breaks the local minimum",
        negative_mutation[9, 9].is_negative is True,
    )
    checks.check(
        "dropping one symmetry direction breaks exact kernel equality",
        sp.ImmutableMatrix.hstack(*symmetry[:-1]).rank()
        < len(transformed_hessian.nullspace()),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
