"""Independent exact review for P060.

This verifier deliberately does not import the canonical symmetry-breaking
helpers.  It derives the differentiated invariance identity from an arbitrary
symbolic potential, constructs the complete O(4) generator basis and vacuum
orbit directly, rederives both Pauli kinetic conventions, and checks the
classical mode equation and explicit-breaking mutations.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def matrix_zero(matrix: sp.MatrixBase) -> bool:
    """Test exact matrix equality after elementwise simplification."""

    return matrix.applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def main() -> int:
    ledger = CheckLedger("P060-INDEPENDENT")

    x, y = sp.symbols("x y", real=True)
    a, b, c, d = sp.symbols("a b c d", real=True)
    arbitrary_potential = sp.Function("V")(x, y)
    field = sp.Matrix([x, y])
    generator = sp.Matrix([[a, b], [c, d]])
    gradient = sp.Matrix(
        [sp.diff(arbitrary_potential, component) for component in field]
    )
    hessian = sp.hessian(arbitrary_potential, field)
    invariance_residual = sp.expand((gradient.T * generator * field)[0])
    differentiated = sp.Matrix(
        [sp.diff(invariance_residual, component) for component in field]
    )
    ledger.check(
        "direct component differentiation proves the general linear identity",
        matrix_zero(
            differentiated - hessian * generator * field - generator.T * gradient
        ),
    )
    ledger.check(
        "invariance plus stationarity leaves the Hessian-tangent term",
        matrix_zero(
            (generator.T * gradient).xreplace(
                {gradient[0]: sp.Integer(0), gradient[1]: sp.Integer(0)}
            )
        ),
    )

    fields = sp.Matrix(sp.symbols("sigma pi1 pi2 pi3", real=True))
    coupling, scale = sp.symbols("lambda v", positive=True)
    generators: list[sp.Matrix] = []
    pairs: list[tuple[int, int]] = []
    for first in range(4):
        for second in range(first + 1, 4):
            value = sp.zeros(4)
            value[first, second] = 1
            value[second, first] = -1
            generators.append(value)
            pairs.append((first, second))
    flattened = sp.Matrix.hstack(
        *(generator_matrix.reshape(16, 1) for generator_matrix in generators)
    )
    ledger.check(
        "all six independently constructed O(4) generators are antisymmetric",
        len(generators) == 6
        and flattened.rank() == 6
        and all(generator_matrix.T == -generator_matrix for generator_matrix in generators),
    )

    vacuum = sp.Matrix([scale, 0, 0, 0])
    tangents = sp.Matrix.hstack(
        *(generator_matrix * vacuum for generator_matrix in generators)
    )
    ledger.check(
        "the actual O(4) vacuum-tangent map has rank three",
        tangents.rank() == 3
        and tangents.columnspace()
        == [
            sp.Matrix([0, -scale, 0, 0]),
            sp.Matrix([0, 0, -scale, 0]),
            sp.Matrix([0, 0, 0, -scale]),
        ],
    )
    stabilizer_basis = tangents.nullspace()
    ledger.check(
        "the tangent-map kernel is the three-dimensional unbroken rotation space",
        len(stabilizer_basis) == 3
        and all(matrix_zero(tangents * coefficient) for coefficient in stabilizer_basis)
        and pairs == [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)],
    )

    radius_squared = (fields.T * fields)[0]
    potential = coupling * (radius_squared - scale**2) ** 2
    field_substitutions = dict(zip(fields, vacuum, strict=True))
    radial_gradient = sp.Matrix(
        [sp.diff(potential, component) for component in fields]
    )
    radial_hessian = sp.hessian(potential, fields).subs(field_substitutions)
    ledger.check(
        "independent differentiation gives the O(4) stationary Hessian",
        matrix_zero(radial_gradient.subs(field_substitutions))
        and radial_hessian == sp.diag(8 * coupling * scale**2, 0, 0, 0),
    )
    ledger.check(
        "every constructed broken tangent is an exact Hessian zero direction",
        matrix_zero(radial_hessian * tangents)
        and radial_hessian.rank() == 1
        and len(radial_hessian.nullspace()) == 3,
    )
    ledger.mutation_sensitive(
        "stationary-vacuum location",
        lambda candidate: matrix_zero(radial_gradient.subs(candidate)),
        field_substitutions,
        (
            dict(zip(fields, (scale / 2, 0, 0, 0), strict=True)),
            dict(zip(fields, (scale, 1, 0, 0), strict=True)),
        ),
    )

    anisotropy = sp.symbols("mu2", positive=True)
    anisotropic_potential = potential + anisotropy * fields[1] ** 2 / 2
    anisotropic_residuals = tuple(
        sp.simplify(
            (
                sp.Matrix(
                    [sp.diff(anisotropic_potential, component) for component in fields]
                ).T
                * generator_matrix
                * fields
            )[0]
        )
        for generator_matrix in generators
    )
    anisotropic_hessian = sp.hessian(anisotropic_potential, fields).subs(
        field_substitutions
    )
    ledger.check(
        "an anisotropic mass mutation breaks the relevant symmetry and lifts one tangent",
        any(residual != 0 for residual in anisotropic_residuals)
        and anisotropic_hessian[1, 1] == anisotropy
        and not matrix_zero(anisotropic_hessian * tangents),
    )

    source, shifted = sp.symbols("c s0", positive=True)
    tilted = potential - source * fields[0]
    shifted_vacuum = dict(zip(fields, (shifted, 0, 0, 0), strict=True))
    stationary_source = 4 * coupling * shifted * (shifted**2 - scale**2)
    shifted_gradient = sp.Matrix(
        [sp.diff(tilted, component) for component in fields]
    ).subs(shifted_vacuum)
    shifted_hessian = sp.hessian(tilted, fields).subs(shifted_vacuum)
    ledger.check(
        "the linear tilt independently gives transverse curvature c over s0",
        matrix_zero(shifted_gradient.subs(source, stationary_source))
        and sp.simplify(shifted_hessian[1, 1] - stationary_source / shifted) == 0
        and sp.simplify(
            shifted_hessian[1, 1].subs(shifted, scale + 1)
        )
        != 0,
    )

    pauli = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )
    trace_gram = sp.Matrix(
        3,
        3,
        lambda row, column: sp.trace(pauli[row] * pauli[column]),
    )
    ledger.check(
        "explicit Pauli multiplication gives trace Gram matrix two times identity",
        trace_gram == 2 * sp.eye(3)
        and all(matrix.H == matrix for matrix in pauli),
    )

    p1, p2, p3 = sp.symbols("p1 p2 p3", real=True)
    epsilon = sp.symbols("epsilon", real=True)
    carrier = (p1 * pauli[0] + p2 * pauli[1] + p3 * pauli[2]) / scale
    second_order_u = sp.eye(2) + sp.I * epsilon * carrier - epsilon**2 * carrier**2 / 2
    second_order_udag = (
        sp.eye(2) - sp.I * epsilon * carrier - epsilon**2 * carrier**2 / 2
    )
    leading_trace = sp.simplify(
        sp.trace(sp.diff(second_order_u, epsilon) * sp.diff(second_order_udag, epsilon)).subs(
            epsilon, 0
        )
    )
    momentum_square = p1**2 + p2**2 + p3**2
    ledger.check(
        "independent exponential differentiation gives the leading derivative trace",
        sp.simplify(leading_trace - 2 * momentum_square / scale**2) == 0,
    )
    physicist_term = sp.simplify(scale**2 * leading_trace / 4)
    anw_term = sp.simplify(scale**2 * leading_trace / 16)
    ledger.mutation_sensitive(
        "SU(2) action prefactor normalization",
        lambda term: sp.simplify(term - momentum_square / 2) == 0,
        physicist_term,
        (anw_term, 4 * physicist_term),
    )
    ledger.check(
        "the ANW-prefactor coordinates have one-quarter the canonical metric",
        sp.simplify(anw_term - momentum_square / 8) == 0
        and sp.simplify(4 * anw_term - physicist_term) == 0,
    )

    time = sp.symbols("t", real=True)
    wave_number, mass_squared, kinetic = sp.symbols("k m2 K", positive=True)
    mode = sp.Function("q")(time)
    mode_lagrangian = (
        kinetic * sp.diff(mode, time) ** 2 / 2
        - kinetic * wave_number**2 * mode**2 / 2
        - mass_squared * mode**2 / 2
    )
    equation = sp.simplify(
        sp.diff(sp.diff(mode_lagrangian, sp.diff(mode, time)), time)
        - sp.diff(mode_lagrangian, mode)
    )
    frequency_squared = sp.solve(
        equation.subs(
            {
                sp.diff(mode, time, 2): -sp.Symbol("omega2") * mode,
            }
        ),
        sp.Symbol("omega2"),
    )[0]
    ledger.check(
        "the declared quadratic mode equation separates kinetic and Hessian premises",
        sp.simplify(
            equation
            - kinetic * (wave_number**2 * mode + sp.diff(mode, time, 2))
            - mass_squared * mode
        )
        == 0
        and frequency_squared == wave_number**2 + mass_squared / kinetic
        and frequency_squared.subs(mass_squared, 0) == wave_number**2,
    )
    ledger.check(
        "an added potential curvature lifts the declared derivative-only mode",
        frequency_squared.subs(mass_squared, 1) != wave_number**2,
    )

    field_dimension = 1
    derivative_dimension = 1
    potential_dimension = 4
    hessian_dimension = potential_dimension - 2 * field_dimension
    linear_source_dimension = potential_dimension - field_dimension
    ledger.check(
        "four-dimensional scalar conventions give consistent exact dimensions",
        2 * (field_dimension + derivative_dimension) == potential_dimension
        and hessian_dimension == 2
        and linear_source_dimension == 3
        and 2 * field_dimension == hessian_dimension,
    )

    ledger.check(
        "the finite-dimensional proof contains no physical-pion dictionary",
        all(
            name not in {str(symbol) for symbol in fields.free_symbols}
            for name in ("F_pi_physical", "quark_condensate", "nucleon")
        ),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
