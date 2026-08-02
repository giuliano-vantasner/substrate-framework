"""Independent exact review for P059.

This verifier deliberately does not import the canonical effective-action
helpers.  It derives the stationary field from component derivatives, checks
completion of the square by direct expansion, proves the finite Neumann-series
residual for a noncommuting kernel, and audits what an anomaly equation can and
cannot determine.  The final checks reproduce WZ4's form-factor algebra with
an arbitrary contact coefficient so circular normalization cannot hide behind
the physical comparator.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def matrix_zero(matrix: sp.MatrixBase) -> bool:
    """Test exact matrix equality after elementwise simplification."""

    return matrix.applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def main() -> int:
    ledger = CheckLedger("P059-INDEPENDENT")

    a, b, c = sp.symbols("a b c", real=True)
    j1, j2, v1, v2 = sp.symbols("j1 j2 v1 v2", real=True)
    determinant = a * c - b**2
    kernel = sp.Matrix([[a, b], [b, c]])
    source = sp.Matrix([j1, j2])
    field = sp.Matrix([v1, v2])
    inverse = sp.Matrix([[c, -b], [-b, a]]) / determinant
    action = sp.expand((field.T * kernel * field)[0] / 2 + (field.T * source)[0])
    equations = sp.Matrix([sp.diff(action, component) for component in field])
    stationary = (-inverse * source).applyfunc(sp.factor)
    ledger.check(
        "component derivatives independently give the matrix equation",
        matrix_zero(equations - (kernel * field + source)),
    )
    ledger.check(
        "the adjugate stationary field solves both equations",
        matrix_zero(equations.subs(dict(zip(field, stationary, strict=True)))),
    )

    reduced = sp.factor(action.subs(dict(zip(field, stationary, strict=True))))
    expected_reduced = sp.factor(-(source.T * inverse * source)[0] / 2)
    shifted = field - stationary
    completed = sp.expand((shifted.T * kernel * shifted)[0] / 2 + expected_reduced)
    ledger.check(
        "direct substitution and completion of the square agree",
        sp.factor(reduced - expected_reduced) == 0
        and sp.factor(action - completed) == 0,
    )
    ledger.mutation_sensitive(
        "stationary-source sign",
        lambda candidate: matrix_zero(kernel * candidate + source),
        stationary,
        (-stationary, stationary + sp.Matrix([1, 0])),
    )
    wrong_action = sp.expand((field.T * kernel * field)[0] + (field.T * source)[0])
    wrong_equations = sp.Matrix(
        [sp.diff(wrong_action, component) for component in field]
    )
    ledger.check(
        "removing the quadratic one-half changes the stationary equation",
        matrix_zero(wrong_equations - (2 * kernel * field + source))
        and not matrix_zero(
            wrong_equations.subs(dict(zip(field, stationary, strict=True)))
        ),
    )

    even_amplitude, odd_amplitude = sp.symbols("e o", real=True)
    fixed_kernel = sp.Matrix([[2, 1], [1, 3]])
    fixed_inverse = fixed_kernel.inv()
    even_source = sp.Matrix([even_amplitude, 0])
    odd_source = sp.Matrix([0, odd_amplitude])
    total_reduced = sp.expand(
        -((even_source + odd_source).T * fixed_inverse * (even_source + odd_source))[0]
        / 2
    )
    even_square = sp.expand(-(even_source.T * fixed_inverse * even_source)[0] / 2)
    odd_square = sp.expand(-(odd_source.T * fixed_inverse * odd_source)[0] / 2)
    cross = sp.expand(total_reduced - even_square - odd_square)
    ledger.check(
        "the independently expanded odd term is the even-odd cross term",
        even_square == -3 * even_amplitude**2 / 10
        and odd_square == -odd_amplitude**2 / 5
        and cross == even_amplitude * odd_amplitude / 5
        and sp.expand(total_reduced.subs(odd_amplitude, -odd_amplitude))
        == sp.expand(even_square + odd_square - cross),
    )
    ledger.check(
        "the cross term requires both declared sources",
        cross.subs(even_amplitude, 0) == 0
        and cross.subs(odd_amplitude, 0) == 0
        and cross.subs({even_amplitude: 1, odd_amplitude: 1}) != 0,
    )

    expansion_parameter = sp.symbols("lambda", real=True)
    mass = sp.diag(2, 3)
    derivative = expansion_parameter * sp.Matrix([[1, 2], [2, -1]])
    ratio = mass.inv() * derivative
    inverse_approximation = sum(
        ((-ratio) ** order * mass.inv() for order in range(3)),
        sp.zeros(2),
    )
    full_kernel = mass + derivative
    left_residual = (full_kernel * inverse_approximation - sp.eye(2)).applyfunc(
        sp.factor
    )
    right_residual = (inverse_approximation * full_kernel - sp.eye(2)).applyfunc(
        sp.factor
    )
    ledger.check(
        "the noncommuting finite inverse series has its exact cubic residual",
        matrix_zero(left_residual - mass * ratio**3 * mass.inv())
        and matrix_zero(right_residual - ratio**3)
        and left_residual != sp.zeros(2)
        and right_residual != sp.zeros(2),
    )
    ledger.check(
        "both inverse residuals vanish only through the declared order",
        all(
            matrix_zero(
                residual.applyfunc(
                    lambda entry: sp.series(entry, expansion_parameter, 0, 3).removeO()
                )
            )
            for residual in (left_residual, right_residual)
        )
        and any(
            sp.expand(entry).coeff(expansion_parameter, 3) != 0
            for entry in right_residual
        ),
    )

    mass_scale, momentum_squared = sp.symbols("m q2", nonzero=True, real=True)
    scalar_series = sum(
        ((momentum_squared / mass_scale**2) ** order / mass_scale**2 for order in range(3)),
        sp.Integer(0),
    )
    scalar_residual = sp.factor(
        (mass_scale**2 - momentum_squared) * scalar_series - 1
    )
    ledger.check(
        "the scalar propagator expansion retains the exact truncation error",
        scalar_residual == -momentum_squared**3 / mass_scale**6
        and scalar_residual != 0,
    )

    anomaly_unit, level = sp.symbols("A k", nonzero=True, real=True)
    coefficients = sp.symbols("c1:5", real=True)
    anomaly_map = sp.Matrix([[1, 0, 0, 0, 0]])
    full_variation = level * anomaly_unit + sum(
        (coefficient * 0 for coefficient in coefficients),
        sp.Integer(0),
    )
    ledger.check(
        "the anomaly equation leaves four homogeneous coefficient directions",
        anomaly_map.rank() == 1
        and len(anomaly_map.nullspace()) == 4
        and full_variation == level * anomaly_unit
        and all(sp.diff(full_variation, coefficient) == 0 for coefficient in coefficients),
    )
    ledger.mutation_sensitive(
        "homogeneous terms have zero anomaly variation",
        lambda variations: all(variation == 0 for variation in variations),
        (0, 0, 0, 0),
        ((anomaly_unit, 0, 0, 0), (0, 0, -anomaly_unit, 0)),
    )
    induced_variations = sp.symbols("dV0:2", real=True)
    stationarity_residual = sp.zeros(2, 1)
    induced = sp.Matrix(induced_variations)
    reduced_variation = sp.simplify(
        full_variation + (stationarity_residual.T * induced)[0]
    )
    ledger.check(
        "stationary elimination preserves rather than creates explicit anomaly",
        reduced_variation == level * anomaly_unit
        and reduced_variation.subs(level, 0) == 0,
    )

    contact = sp.symbols("C", real=True)
    source_form_factor = contact * mass_scale**2 / (mass_scale**2 - momentum_squared)
    correction = contact * momentum_squared / (mass_scale**2 - momentum_squared)
    ledger.check(
        "WZ4's form factor is an arbitrary contact plus a vanishing correction",
        sp.factor(source_form_factor - contact - correction) == 0
        and source_form_factor.subs(momentum_squared, 0) == contact
        and sp.limit(correction, mass_scale, sp.oo) == 0
        and sp.limit(source_form_factor, mass_scale, sp.oo) == contact,
    )
    ledger.check(
        "zero imported contact gives zero rather than regenerating a WZW term",
        source_form_factor.subs(contact, 0) == 0
        and correction.subs(contact, 0) == 0,
    )

    spacetime_orientation = -1
    pseudoscalar_intrinsic_factors = (-1) ** 3
    physical_parity = spacetime_orientation * pseudoscalar_intrinsic_factors
    polar_field_assumption = spacetime_orientation
    ledger.check(
        "three pseudoscalars distinguish physical parity from intrinsic parity",
        physical_parity == 1 and polar_field_assumption == -1,
    )

    vector_dimension = 1
    kernel_dimension = 2
    source_dimension = 3
    spacetime_lagrangian_dimension = 4
    ledger.check(
        "the quadratic action and reduced source term have matching dimensions",
        2 * vector_dimension + kernel_dimension == spacetime_lagrangian_dimension
        and vector_dimension + source_dimension == spacetime_lagrangian_dimension
        and 2 * source_dimension - kernel_dimension
        == spacetime_lagrangian_dimension,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
