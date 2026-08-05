"""Derive the full degree-two rational-map Hessian exactly.

The script differentiates the actual chart integrand for each real coefficient
pair, extracts the azimuthal Fourier zero mode as a Laurent coefficient, and
integrates the resulting rational function over the full sphere.  No matrix
entry or eigenvalue is inserted from TX4 or attempt 0004.
"""

from __future__ import annotations

import sympy as sp


z, zbar = sp.symbols("z zbar")
q, w, x = sp.symbols("q w x", positive=True)


def chart_integrand(parameters: list[sp.Expr]) -> sp.Expr:
    a1 = parameters[0] + sp.I * parameters[1]
    a0 = parameters[2] + sp.I * parameters[3]
    b2 = parameters[4] + sp.I * parameters[5]
    b1 = parameters[6] + sp.I * parameters[7]
    b0 = 1 + parameters[8] + sp.I * parameters[9]
    a1_bar = parameters[0] - sp.I * parameters[1]
    a0_bar = parameters[2] - sp.I * parameters[3]
    b2_bar = parameters[4] - sp.I * parameters[5]
    b1_bar = parameters[6] - sp.I * parameters[7]
    b0_bar = 1 + parameters[8] - sp.I * parameters[9]

    numerator = z**2 + a1 * z + a0
    denominator = b2 * z**2 + b1 * z + b0
    numerator_bar = zbar**2 + a1_bar * zbar + a0_bar
    denominator_bar = b2_bar * zbar**2 + b1_bar * zbar + b0_bar
    rational_map = numerator / denominator
    rational_map_bar = numerator_bar / denominator_bar
    derivative = sp.diff(rational_map, z)
    derivative_bar = sp.diff(rational_map_bar, zbar)
    return (
        (1 + z * zbar) ** 4
        * (derivative * derivative_bar) ** 2
        / (1 + rational_map * rational_map_bar) ** 4
    )


def angular_zero_mode(expression: sp.Expr) -> sp.Expr:
    laurent = sp.cancel(expression.subs({z: q * w, zbar: q / w}))
    zero_mode = sp.simplify(sp.residue(laurent / w, w, 0))
    if zero_mode.has(w):
        raise RuntimeError("azimuthal zero mode still contains w")
    radial = sp.cancel(zero_mode.subs(q, sp.sqrt(x)))
    if radial.has(sp.sqrt(x)):
        radial = sp.powsimp(radial, force=True)
    if radial.has(sp.sqrt(x)):
        raise RuntimeError("azimuthal average is not rational in r squared")
    return radial


def sphere_average(expression: sp.Expr) -> sp.Expr:
    radial = angular_zero_mode(expression)
    result = sp.integrate(sp.cancel(radial / (1 + x) ** 2), (x, 0, sp.oo))
    if result.has(sp.Integral):
        raise RuntimeError(f"unevaluated exact sphere integral: {result}")
    return sp.simplify(result)


def directional_parameters(
    first: int,
    second: int | None,
    epsilon: sp.Symbol,
    eta: sp.Symbol,
) -> list[sp.Expr]:
    parameters: list[sp.Expr] = []
    for index in range(10):
        value: sp.Expr = sp.S.Zero
        if index == first:
            value += epsilon
        if second is not None and index == second:
            value += eta
        parameters.append(value)
    return parameters


def exact_gradient_entry(index: int) -> sp.Expr:
    epsilon, eta = sp.symbols("epsilon eta", real=True)
    integrand = chart_integrand(
        directional_parameters(index, None, epsilon, eta)
    )
    derivative = sp.diff(integrand, epsilon).subs(epsilon, 0)
    return sphere_average(sp.cancel(derivative))


def exact_hessian_entry(first: int, second: int) -> sp.Expr:
    epsilon, eta = sp.symbols("epsilon eta", real=True)
    if first == second:
        integrand = chart_integrand(
            directional_parameters(first, None, epsilon, eta)
        )
        derivative = sp.diff(integrand, epsilon, 2).subs(epsilon, 0)
    else:
        integrand = chart_integrand(
            directional_parameters(first, second, epsilon, eta)
        )
        derivative = (
            sp.diff(integrand, epsilon, eta)
            .subs({epsilon: 0, eta: 0})
        )
    return sphere_average(sp.cancel(derivative))


def main() -> None:
    base = sphere_average(chart_integrand([sp.S.Zero] * 10))
    print("BASE", base, flush=True)
    gradient_entries = []
    for index in range(10):
        entry = exact_gradient_entry(index)
        gradient_entries.append(entry)
        print("GRADIENT", index, entry, flush=True)

    hessian = sp.zeros(10)
    for first in range(10):
        for second in range(first, 10):
            entry = exact_hessian_entry(first, second)
            hessian[first, second] = entry
            hessian[second, first] = entry
            print("HESSIAN", first, second, entry, flush=True)

    print("GRADIENT_MATRIX")
    sp.print_latex(sp.Matrix(gradient_entries))
    print("HESSIAN_MATRIX")
    print(hessian)
    print("RANK", hessian.rank())
    print("NULLITY", 10 - hessian.rank())
    print("EIGENVALUES", hessian.eigenvals())


if __name__ == "__main__":
    main()
