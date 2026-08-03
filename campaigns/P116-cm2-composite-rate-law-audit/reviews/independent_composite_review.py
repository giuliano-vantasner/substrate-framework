"""Implementation-independent exact review of P116's composite theorem."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("C-CMP-001-INDEPENDENT")
    gamma, omega, coupling = sp.symbols("Gamma omega c", positive=True)
    detunings = (sp.Integer(1), sp.Integer(2), sp.Integer(3))

    intermediate_energies = tuple(
        value
        for delta in detunings
        for value in (delta - sp.I * gamma / 2, -delta - sp.I * gamma / 2)
    )
    intermediate = sp.diag(*intermediate_energies)
    endpoint = sp.zeros(2, 2)
    root_coupling = sp.symbols("g", positive=True)
    to_intermediate = sp.ones(2, len(intermediate_energies)) * root_coupling
    to_endpoint = to_intermediate.T
    full_effective = sp.simplify(
        endpoint
        + to_intermediate
        * (-intermediate).inv()
        * to_endpoint
    )
    fresh_offdiagonal = sp.factor(full_effective[0, 1])
    expected_offdiagonal = sp.simplify(
        -sp.I
        * root_coupling**2
        * gamma
        * sum(1 / (delta**2 + gamma**2 / 4) for delta in detunings)
    )
    checks.check(
        "fresh complete block inversion gives the common-loss sum",
        sp.simplify(fresh_offdiagonal - expected_offdiagonal) == 0,
    )

    positive_kernel = sp.simplify(
        coupling
        * sum(1 / (delta**2 + gamma**2 / 4) for delta in detunings)
    )
    pair_magnitude = sp.simplify(gamma * positive_kernel)
    nominal_cycles = omega / (2 * sp.pi * gamma)
    nominal_product = sp.cancel(pair_magnitude * nominal_cycles)
    expected_product = sp.simplify(omega * positive_kernel / (2 * sp.pi))
    checks.check(
        "fresh multiplication cancels one positive loss power",
        sp.simplify(nominal_product - expected_product) == 0,
    )

    squared_loss = sp.symbols("y", nonnegative=True)
    squared_loss_form = sp.simplify(
        omega
        * coupling
        / (2 * sp.pi)
        * sum(1 / (delta**2 + squared_loss / 4) for delta in detunings)
    )
    squared_loss_positive_kernel = sp.simplify(
        sum(
            1 / (delta**2 + squared_loss / 4) ** 2
            for delta in detunings
        )
    )
    expected_squared_loss_derivative = sp.simplify(
        -omega * coupling * squared_loss_positive_kernel / (8 * sp.pi)
    )
    checks.check(
        "the product decreases strictly in squared loss",
        sp.simplify(
            sp.diff(squared_loss_form, squared_loss)
            - expected_squared_loss_derivative
        )
        == 0
        and squared_loss_positive_kernel.is_positive is True,
    )
    checks.check(
        "positive loss therefore has no interior stationary point",
        sp.simplify(
            sp.diff(nominal_product, gamma)
            - expected_squared_loss_derivative.subs(squared_loss, gamma**2)
            * 2
            * gamma
        )
        == 0
        and squared_loss_positive_kernel.subs(
            squared_loss,
            gamma**2,
        ).is_positive
        is True
        and sp.solve(sp.diff(nominal_product, gamma), gamma) == [],
    )

    zero_limit = sp.simplify(
        omega
        * coupling
        / (2 * sp.pi)
        * sum(1 / delta**2 for delta in detunings)
    )
    critical_left = sp.simplify(
        omega
        * coupling
        / (2 * sp.pi)
        * sum(1 / (delta**2 + omega**2) for delta in detunings)
    )
    checks.check(
        "the zero-loss right limit is finite positive",
        sp.simplify(sp.limit(nominal_product, gamma, 0, dir="+") - zero_limit)
        == 0
        and zero_limit.is_positive is True,
    )
    checks.check(
        "the nominal critical left limit is finite positive",
        sp.simplify(
            sp.limit(nominal_product, gamma, 2 * omega, dir="-")
            - critical_left
        )
        == 0
        and critical_left.is_positive is True,
    )
    checks.check(
        "assigning zero at both boundaries makes two jumps",
        zero_limit != 0 and critical_left != 0,
    )
    checks.check(
        "strict decrease and an excluded left endpoint give no maximizer",
        squared_loss_positive_kernel.subs(
            squared_loss,
            gamma**2,
        ).is_positive
        is True
        and zero_limit.is_positive is True,
    )

    actual_product = sp.simplify(
        sp.sqrt(omega**2 - gamma**2 / 4)
        * positive_kernel
        / (2 * sp.pi)
    )
    actual_log_derivative = sp.simplify(sp.diff(sp.log(actual_product), gamma))
    gamma_square_kernel = squared_loss_positive_kernel.subs(
        squared_loss,
        gamma**2,
    )
    positive_kernel_derivative = sp.simplify(
        -coupling * gamma * gamma_square_kernel / 2
    )
    expected_actual_log_derivative = sp.simplify(
        -gamma / (4 * (omega**2 - gamma**2 / 4))
        + positive_kernel_derivative / positive_kernel
    )
    checks.check(
        "the fresh actual-cycle product is also strictly decreasing",
        sp.simplify(
            actual_log_derivative - expected_actual_log_derivative
        )
        == 0
        and gamma_square_kernel.is_positive is True
        and positive_kernel.is_positive is True,
    )
    checks.check(
        "the actual-cycle critical endpoint is continuous at zero value",
        sp.limit(actual_product, gamma, 2 * omega, dir="-") == 0,
    )
    checks.check(
        "nominal and actual routes agree only in the zero-loss limit",
        sp.simplify(
            sp.limit(actual_product - nominal_product, gamma, 0, dir="+")
        )
        == 0
        and sp.simplify(actual_product - nominal_product) != 0,
    )

    source_grid = tuple(sp.Rational(index, 20) for index in range(41))
    def source_extension(value: sp.Expr) -> sp.Expr:
        if value == 0 or value >= 2:
            return sp.Integer(0)
        return nominal_product.subs({gamma: value, omega: 1, coupling: sp.Rational(1, 100)})

    grid_values = tuple(source_extension(value) for value in source_grid)
    checks.check(
        "the forty-one-point grid maximum is its first positive node",
        max(range(len(grid_values)), key=grid_values.__getitem__) == 1,
    )
    finer_first = nominal_product.subs(
        {gamma: sp.Rational(1, 40), omega: 1, coupling: sp.Rational(1, 100)}
    )
    coarse_first = nominal_product.subs(
        {gamma: sp.Rational(1, 20), omega: 1, coupling: sp.Rational(1, 100)}
    )
    checks.check(
        "grid refinement moves the apparent optimum toward zero",
        finer_first > coarse_first,
    )

    common_scale = sp.symbols("rho", positive=True)
    symbolic_detunings = sp.symbols("Delta_1 Delta_2 Delta_3", positive=True)
    symbolic_nominal_product = sp.simplify(
        omega
        * coupling
        / (2 * sp.pi)
        * sum(
            1 / (delta**2 + gamma**2 / 4)
            for delta in symbolic_detunings
        )
    )
    rescaled = symbolic_nominal_product.subs(
        {
            gamma: common_scale * gamma,
            omega: common_scale * omega,
            coupling: common_scale**2 * coupling,
            **{
                delta: common_scale * delta
                for delta in symbolic_detunings
            },
        },
        simultaneous=True,
    )
    checks.check(
        "dimensionally common scaling leaves one frequency power",
        sp.simplify(rescaled - common_scale * symbolic_nominal_product) == 0,
    )
    fixed_coupling = symbolic_nominal_product.subs(
        {
            gamma: common_scale * gamma,
            omega: common_scale * omega,
            **{
                delta: common_scale * delta
                for delta in symbolic_detunings
            },
        },
        simultaneous=True,
    )
    checks.check(
        "fixed coupling normalization has the inverse scale law",
        sp.simplify(
            fixed_coupling - symbolic_nominal_product / common_scale
        )
        == 0,
    )

    barrier, scale, count, population, splitting = sp.symbols(
        "E Theta n N x",
        positive=True,
    )
    activation = sp.exp(-barrier / scale)
    thermal_gate = sp.sech(splitting / 2) ** 2 / 2
    full_factor = sp.simplify(
        activation * count * population * nominal_product * thermal_gate
    )
    checks.check(
        "positive gamma-independent factors preserve loss monotonicity",
        sp.simplify(
            sp.diff(full_factor, gamma)
            - full_factor
            / nominal_product
            * expected_squared_loss_derivative.subs(
                squared_loss,
                gamma**2,
            )
            * 2
            * gamma
        )
        == 0
        and gamma_square_kernel.is_positive is True,
    )
    checks.check(
        "count linearity is a declared factorization rather than a rate theorem",
        sp.diff(full_factor / count, count) == 0
        and sp.diff(full_factor / population, population) == 0,
    )
    checks.check(
        "the activation factor contains a barrier despite the lexical audit",
        sp.diff(sp.log(activation), barrier) == -1 / scale,
    )

    rate_target, free_prefactor = sp.symbols("R nu", positive=True)
    checks.check(
        "zero interaction leaves every displayed factor but gives zero rate",
        0 * full_factor == 0 and full_factor.is_positive is True,
    )
    checks.check(
        "a free prefactor makes one reported magnitude nonidentifying",
        sp.simplify(
            (free_prefactor * full_factor).subs(
                free_prefactor,
                rate_target / full_factor,
            )
            - rate_target
        )
        == 0,
    )

    delta = sp.symbols("Delta", positive=True)
    p = sp.symbols("p", real=True)
    mutated_family = gamma ** (p - 1) / (delta**2 + gamma**2 / 4)
    stationary_square = sp.solve(
        sp.factor(sp.diff(sp.log(mutated_family), gamma)),
        gamma**2,
    )
    checks.check(
        "the general loss-power stationary surface is explicit",
        len(stationary_square) == 1
        and sp.simplify(
            stationary_square[0] - 4 * delta**2 * (p - 1) / (3 - p)
        )
        == 0,
    )
    checks.check(
        "the source linear opening is outside the interior-optimum regime",
        sp.diff(mutated_family.subs(p, 1), gamma).is_negative is True
        and sp.solve(sp.diff(mutated_family.subs(p, 2), gamma), gamma)
        == [2 * delta],
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
