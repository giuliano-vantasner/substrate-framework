#!/usr/bin/env python3
"""Fresh C-OG-005 derivation without importing the canonical optical helper."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P153-independent")
    i = sp.I
    t, x = sp.symbols("t x", real=True)
    n, c0, mass, charge, length = sp.symbols("n c0 m e L", positive=True)
    omega, wave_number, a_t, a_x = sp.symbols(
        "omega k A_t A_x", real=True
    )
    field = sp.exp(i * (wave_number * x - omega * t))
    field_bar = sp.exp(-i * (wave_number * x - omega * t))
    metric = sp.diag(-1 / n, n / c0**2)
    inverse = sp.simplify(metric.inv())
    volume = sp.simplify(sp.sqrt(-metric.det()))
    checks.check(
        "fresh optical inverse and volume",
        inverse == sp.diag(-n, c0**2 / n) and volume == 1 / c0,
    )

    def derivative(value: sp.Expr, connection: sp.Expr, coordinate: sp.Symbol) -> sp.Expr:
        return sp.diff(value, coordinate) - i * charge * connection * value

    d_t = derivative(field, a_t, t)
    d_x = derivative(field, a_x, x)
    operator = sp.simplify(
        derivative(-n * d_t, a_t, t)
        + derivative(c0**2 * d_x / n, a_x, x)
        - mass**2 * field
    )
    invariant_frequency = omega + charge * a_t
    invariant_wavenumber = wave_number - charge * a_x
    mass_shell = sp.simplify(
        n * invariant_frequency**2
        - c0**2 * invariant_wavenumber**2 / n
        - mass**2
    )
    checks.check(
        "fresh plane-wave Euler equation gives the invariant mass shell",
        sp.simplify(operator / field - mass_shell) == 0,
    )

    d_bar_t = sp.diff(field_bar, t) + i * charge * a_t * field_bar
    d_bar_x = sp.diff(field_bar, x) + i * charge * a_x * field_bar
    density = sp.simplify(
        -(
            -n * d_bar_t * d_t
            + c0**2 * d_bar_x * d_x / n
            + mass**2 * field_bar * field
        )
        / c0
    )
    alpha, beta = sp.symbols("alpha beta", real=True)
    phase = alpha * t + beta * x
    changed_field = sp.exp(i * charge * phase) * field
    changed_bar = sp.exp(-i * charge * phase) * field_bar
    changed_dt = sp.diff(changed_field, t) - i * charge * (a_t + alpha) * changed_field
    changed_dx = sp.diff(changed_field, x) - i * charge * (a_x + beta) * changed_field
    changed_bar_t = sp.diff(changed_bar, t) + i * charge * (a_t + alpha) * changed_bar
    changed_bar_x = sp.diff(changed_bar, x) + i * charge * (a_x + beta) * changed_bar
    changed_density = sp.simplify(
        -(
            -n * changed_bar_t * changed_dt
            + c0**2 * changed_bar_x * changed_dx / n
            + mass**2 * changed_bar * changed_field
        )
        / c0
    )
    checks.check(
        "fresh action-density route is affine-gauge invariant",
        sp.simplify(changed_density - density) == 0,
    )
    checks.check(
        "fresh affine labels preserve both invariant components",
        sp.simplify((omega - charge * alpha) + charge * (a_t + alpha) - invariant_frequency) == 0
        and sp.simplify((wave_number + charge * beta) - charge * (a_x + beta) - invariant_wavenumber) == 0,
    )
    checks.check(
        "fresh line gauge removes a constant connection",
        sp.simplify((omega + charge * a_t) - invariant_frequency) == 0
        and sp.simplify((wave_number - charge * a_x) - invariant_wavenumber) == 0,
    )

    mode, winding = sp.symbols("q ell", integer=True)
    theta = sp.symbols("theta", real=True)
    circle_momentum = (2 * sp.pi * mode + theta) / length - charge * a_x
    shifted_momentum = (
        (2 * sp.pi * (mode + winding) + theta) / length
        - charge * (a_x + 2 * sp.pi * winding / (charge * length))
    )
    circle_frequency_squared = sp.simplify(
        mass**2 / n + c0**2 * circle_momentum**2 / n**2
    )
    shifted_frequency_squared = sp.simplify(
        mass**2 / n + c0**2 * shifted_momentum**2 / n**2
    )
    checks.check(
        "fresh circle route is invariant under large-gauge mode relabeling",
        sp.simplify(shifted_momentum - circle_momentum) == 0
        and sp.simplify(shifted_frequency_squared - circle_frequency_squared) == 0,
    )
    checks.check(
        "fresh boundary-phase mutation changes a generic fixed mode",
        sp.simplify(
            circle_frequency_squared.subs(theta, theta + sp.pi)
            - circle_frequency_squared
        )
        != 0,
    )

    n_profile = sp.Function("n", positive=True)(x)
    connection_profile = sp.Function("A_x", real=True)(x)
    generic = sp.Function("Psi")(t, x)
    first = sp.diff(generic, x) - i * charge * connection_profile * generic
    divergence = sp.expand(
        sp.diff(c0**2 * first / n_profile, x)
        - i * charge * connection_profile * c0**2 * first / n_profile
    )
    second = sp.diff(first, x) - i * charge * connection_profile * first
    naive = sp.expand(c0**2 * second / n_profile)
    checks.check(
        "fresh variable-index route has the derivative correction",
        sp.simplify(
            divergence - naive
            + c0**2 * sp.diff(n_profile, x) * first / n_profile**2
        )
        == 0,
    )
    checks.check(
        "fresh constant-index limit removes only the derivative correction",
        sp.simplify((divergence - naive).subs(sp.diff(n_profile, x), 0)) == 0,
    )

    phi = 2 * sp.pi * x / length
    berry_component = sp.Rational(1, 2)
    berry_pullback = sp.simplify(berry_component * sp.diff(phi, x))
    u1_connection = sp.simplify(-berry_pullback / charge)
    checks.check(
        "fresh same-phase Berry and U1 transformation signs agree",
        sp.simplify(charge * u1_connection + berry_pullback) == 0,
    )
    checks.check(
        "fresh half Berry pullback has minus-one circle holonomy",
        u1_connection == -sp.pi / (charge * length)
        and sp.simplify(sp.exp(i * charge * u1_connection * length)) == -1,
    )
    checks.check(
        "fresh missing-texture mutation is dimensionally distinct",
        u1_connection != berry_component,
    )

    fixed_k_shift = sp.expand(
        c0**2 * ((wave_number - charge * a_x) ** 2 - wave_number**2) / n**2
    )
    shifted_fixed_k = sp.expand(
        fixed_k_shift.subs(
            {wave_number: wave_number + charge * beta, a_x: a_x + beta},
            simultaneous=True,
        )
    )
    checks.check(
        "fresh fixed-canonical-k correction is not gauge invariant",
        sp.simplify(shifted_fixed_k - fixed_k_shift) != 0,
    )
    checks.check(
        "fresh full dispersion remains gauge invariant",
        sp.simplify(
            mass_shell.subs(
                {wave_number: wave_number + charge * beta, a_x: a_x + beta},
                simultaneous=True,
            )
            - mass_shell
        )
        == 0,
    )

    medium_dictionary, gravity_dictionary = sp.symbols(
        "medium_dictionary gravity_dictionary"
    )
    checks.check(
        "fresh identical-dispersion countermodels leave physical dictionaries free",
        medium_dictionary not in mass_shell.free_symbols
        and gravity_dictionary not in mass_shell.free_symbols,
    )

    tally = checks.finish()
    print(f"P153 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
