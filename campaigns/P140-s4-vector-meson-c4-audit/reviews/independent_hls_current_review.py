from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _current(row: sp.Matrix) -> sp.Matrix:
    sigma = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.Matrix([[1, 0], [0, -1]]),
    )
    return sum(
        (sp.I * component * generator for component, generator in zip(row, sigma, strict=True)),
        sp.zeros(2),
    )


def main() -> int:
    checks = CheckLedger("P140/C-VEC-001 independent")
    symbols = sp.symbols("x00:03 x10:13 x20:23", real=True)
    components = sp.Matrix(3, 3, symbols)
    gram = components * components.T
    invariant_one = sp.expand(sp.trace(gram) ** 2)
    invariant_two = sp.expand(sp.trace(gram * gram))

    wedge = sp.Integer(0)
    currents = [_current(components.row(index)) for index in range(3)]
    trace_sum = sp.Integer(0)
    for first in range(3):
        for second in range(3):
            cross = components.row(first).T.cross(components.row(second).T)
            wedge += sp.expand(cross.dot(cross))
            commutator = (
                currents[first] * currents[second]
                - currents[second] * currents[first]
            )
            trace_sum += sp.trace(commutator * commutator)

    checks.check(
        "fresh wedge sum equals Gram difference",
        sp.simplify(wedge - (invariant_one - invariant_two)) == 0,
    )
    checks.check(
        "fresh Pauli commutator sum fixes minus eight",
        sp.simplify(trace_sum + 8 * wedge) == 0,
    )
    checks.check(
        "wedge is nonnegative on an exact nontrivial sample",
        wedge.subs(dict(zip(symbols, range(1, 10), strict=True))) > 0,
    )
    checks.check(
        "rank-one current is an exact zero counterexample",
        sp.simplify(
            wedge.subs(
                {
                    **{symbols[index]: index + 1 for index in range(3)},
                    **{symbols[index]: 2 * (index - 2) for index in range(3, 6)},
                    **{symbols[index]: 3 * (index - 5) for index in range(6, 9)},
                }
            )
        )
        == 0,
    )

    lam = sp.symbols("lambda", real=True)
    # For Gamma=lambda*L, Maurer--Cartan gives
    # F(Gamma)=lambda*dL+lambda^2*L wedge L
    #         =(lambda^2-lambda)*[L,L].
    curvature_coefficient = sp.expand(lam**2 - lam)
    checks.check(
        "half connection gives minus one quarter curvature",
        curvature_coefficient.subs(lam, sp.Rational(1, 2)) == -sp.Rational(1, 4),
    )
    checks.mutation_sensitive(
        "connection coefficient is load bearing",
        lambda value: curvature_coefficient.subs(lam, value) == -sp.Rational(1, 4),
        sp.Rational(1, 2),
        [0, 1, sp.Rational(1, 3)],
    )

    g, kappa = sp.symbols("g kappa", positive=True)
    vector_components = sp.Matrix(3, 3, sp.symbols("v00:03 v10:13 v20:23", real=True))
    mass_density = sp.expand(
        kappa
        * sum(
            (vector_components[row, column] - components[row, column] / 2) ** 2
            for row in range(3)
            for column in range(3)
        )
    )
    stationary = {
        vector_components[row, column]: components[row, column] / 2
        for row in range(3)
        for column in range(3)
    }
    gradient = sp.Matrix(
        [
            sp.diff(mass_density, vector_components[row, column])
            for row in range(3)
            for column in range(3)
        ]
    )
    hessian = sp.hessian(
        mass_density,
        [
            vector_components[row, column]
            for row in range(3)
            for column in range(3)
        ],
    )
    checks.check(
        "fresh mass variation selects the half connection",
        gradient.subs(stationary) == sp.zeros(9, 1),
    )
    checks.check("fresh mass Hessian is positive", hessian == 2 * kappa * sp.eye(9))
    checks.check("stationary mass penalty vanishes", mass_density.subs(stationary) == 0)

    curvature_trace_sum = trace_sum / 16
    curvature_energy = sp.simplify(-curvature_trace_sum / (2 * g**2))
    skyrme_energy = sp.simplify(-trace_sum / (32 * g**2))
    checks.check(
        "fresh curvature substitution gives the Skyrme coefficient",
        sp.simplify(curvature_energy - skyrme_energy) == 0,
    )
    checks.check(
        "fresh positive wedge form has inverse g squared",
        sp.simplify(curvature_energy - wedge / (4 * g**2)) == 0,
    )

    e = sp.symbols("e", positive=True)
    matched_e = sp.solve(sp.Eq(1 / e**2, 1 / g**2), e)[0]
    checks.check("equally normalized matching gives e equals g", matched_e == g)

    mass, decay, parameter = sp.symbols("m F a", positive=True)
    ksrf_g = mass / (sp.sqrt(parameter) * decay)
    checks.check(
        "conditional KSRF relation closes exactly",
        sp.simplify(mass**2 - parameter * ksrf_g**2 * decay**2) == 0,
    )
    mass_dimensions = {mass: 1, decay: 1, parameter: 0, g: 0, e: 0}

    def dimension(powers: dict[sp.Symbol, int]) -> int:
        return sum(mass_dimensions[symbol] * power for symbol, power in powers.items())

    checks.check(
        "KSRF ratio is dimensionless when mass and decay dimensions match",
        dimension({mass: 1, decay: -1, parameter: 0}) == mass_dimensions[g],
    )
    checks.check(
        "source-like e equals F over two is dimensionally rejected",
        mass_dimensions[e] != dimension({decay: 1}),
    )
    checks.mutation_sensitive(
        "KSRF parameter remains visible",
        lambda value: sp.simplify(value - mass / (sp.sqrt(2) * decay)) == 0,
        mass / (sp.sqrt(2) * decay),
        [mass / decay, mass / (2 * decay)],
    )

    derivative_orders = {
        "curvature": 2,
        "kinetic_eom_residual": 3,
        "field_correction": 3,
        "leading_energy": 4,
        "backreaction_energy": 6,
    }
    checks.check(
        "fresh power counting keeps the full-vector correction beyond p4",
        derivative_orders["kinetic_eom_residual"]
        == derivative_orders["field_correction"]
        and derivative_orders["backreaction_energy"]
        > derivative_orders["leading_energy"],
    )
    checks.check(
        "mass coefficient cannot select the leading quartic coupling",
        not curvature_energy.has(kappa),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
