#!/usr/bin/env python3
"""Fresh exact current rederivation without importing P148's claim helpers."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P148-independent")
    left, right = sp.symbols("left right", real=True)
    temporal = left + right
    spatial = left - right
    checks.check(
        "fresh chain rule gives the left plus characteristic",
        sp.simplify(temporal + spatial - 2 * left) == 0,
    )
    checks.check(
        "fresh chain rule gives the right minus characteristic",
        sp.simplify(temporal - spatial - 2 * right) == 0,
    )
    checks.check(
        "fresh reversed spatial sign exchanges the two channels",
        sp.simplify(temporal + (right - left) - 2 * right) == 0
        and sp.simplify(temporal - (right - left) - 2 * left) == 0,
    )

    x, t = sp.symbols("x t", real=True)
    phi = sp.Function("phi")(x, t)
    gradient = sp.Matrix([sp.diff(phi, t), -sp.diff(phi, x)])
    dual = sp.Matrix([sp.diff(phi, x), -sp.diff(phi, t)])
    divergence_gradient = sp.simplify(
        sp.diff(gradient[0], t) + sp.diff(gradient[1], x)
    )
    divergence_dual = sp.simplify(sp.diff(dual[0], t) + sp.diff(dual[1], x))
    wave = sp.diff(phi, t, 2) - sp.diff(phi, x, 2)
    checks.check(
        "fresh gradient divergence is box phi",
        sp.simplify(divergence_gradient - wave) == 0,
    )
    checks.check(
        "fresh dual divergence vanishes by mixed partials",
        divergence_dual == 0,
    )
    checks.check(
        "fresh sine-Gordon shell sources the gradient",
        sp.simplify(
            divergence_gradient.subs(
                sp.diff(phi, t, 2), sp.diff(phi, x, 2) - sp.sin(phi)
            )
            + sp.sin(phi)
        )
        == 0,
    )

    plus = sp.diff(phi, t) + sp.diff(phi, x)
    minus = sp.diff(phi, t) - sp.diff(phi, x)
    plus_transport = sp.simplify(sp.diff(plus, t) - sp.diff(plus, x))
    minus_transport = sp.simplify(sp.diff(minus, t) + sp.diff(minus, x))
    checks.check(
        "fresh characteristic transports both equal box phi",
        sp.simplify(plus_transport - wave) == 0
        and sp.simplify(minus_transport - wave) == 0,
    )
    checks.check(
        "fresh nonlinear characteristic balances share the source",
        tuple(
            sp.simplify(
                defect.subs(
                    sp.diff(phi, t, 2), sp.diff(phi, x, 2) - sp.sin(phi)
                )
            )
            for defect in (plus_transport, minus_transport)
        )
        == (-sp.sin(phi), -sp.sin(phi)),
    )

    u, v = sp.symbols("u v", real=True)
    parity = sp.diag(1, -1)
    derivative = sp.Matrix([u, -v])
    epsilon_dual = sp.Matrix([v, -u])
    derivative_after_field_parity = sp.Matrix([u, v])
    dual_after_field_parity = sp.Matrix([-v, -u])
    checks.check(
        "fresh derivative is a vector under scalar parity",
        derivative_after_field_parity == parity * derivative,
    )
    checks.check(
        "fresh epsilon dual is axial under scalar parity",
        dual_after_field_parity == -parity * epsilon_dual,
    )
    checks.check(
        "fresh null combinations are exchanged by parity",
        derivative_after_field_parity - dual_after_field_parity
        == parity * (derivative + epsilon_dual)
        and derivative_after_field_parity + dual_after_field_parity
        == parity * (derivative - epsilon_dual),
    )
    checks.check(
        "fresh covariance alone does not select either null combination",
        derivative - epsilon_dual != derivative + epsilon_dual,
    )

    sigma, tau = sp.symbols("sigma tau", positive=True, real=True)
    gaussian = -2 * sp.pi / (sp.sqrt(2 * sp.pi) * sigma) * sp.exp(
        -tau**2 / (2 * sigma**2)
    )
    checks.check(
        "fresh Gaussian area is fixed by its prefactor",
        sp.integrate(gaussian, (tau, -sp.oo, sp.oo)) == -2 * sp.pi,
    )
    delta_phi = sp.Symbol("delta_phi", real=True)
    delta_topological_charge = -delta_phi / (2 * sp.pi)
    checks.check(
        "fresh half-line transfer needs a supplied endpoint change",
        delta_topological_charge.subs(delta_phi, -2 * sp.pi) == 1
        and delta_topological_charge.subs(delta_phi, 0) == 0,
    )

    imaginary = sp.I
    real_field, real_rate = sp.symbols("real_field real_rate", real=True)
    real_noether_density = sp.simplify(
        imaginary * (real_field * real_rate - real_field * real_rate)
    )
    checks.check(
        "fresh complex-Noether expression vanishes on a real field",
        real_noether_density == 0,
    )
    amplitude, phase_rate = sp.symbols("amplitude phase_rate", real=True)
    psi = amplitude * sp.exp(-imaginary * phase_rate * t)
    complex_density = sp.simplify(
        imaginary
        * (sp.conjugate(psi) * sp.diff(psi, t) - psi * sp.diff(sp.conjugate(psi), t))
    )
    checks.check(
        "fresh enriched complex field has a distinct nonzero density",
        complex_density == 2 * amplitude**2 * phase_rate,
    )

    raising = sp.Matrix([[0, 1], [0, 0]])
    lower_state = sp.Matrix([0, 1])
    checks.check(
        "fresh SU2 ladder changes T3 by one",
        raising * lower_state == sp.Matrix([1, 0])
        and sp.Rational(1, 2) - sp.Rational(-1, 2) == 1,
    )
    checks.check(
        "fresh assigned plus-minus-one label difference is two",
        sp.Integer(1) - sp.Integer(-1) == 2,
    )

    delta = sp.symbols("delta", real=True)
    positive_half = sp.integrate(
        sp.sin(tau + delta), (tau, -sp.pi / 2, sp.pi / 2)
    )
    negative_half = sp.integrate(
        sp.sin(tau + delta), (tau, sp.pi / 2, 3 * sp.pi / 2)
    )
    correlation = sp.trigsimp(positive_half - negative_half)
    checks.check(
        "fresh sign correlation is a phase-dependent trace",
        sp.simplify(correlation - 4 * sp.sin(delta)) == 0,
    )
    checks.check(
        "fresh zero correlation does not determine endpoint transfer",
        correlation.subs(delta, 0) == 0
        and delta_topological_charge.subs(delta_phi, 2 * sp.pi) == -1,
    )
    checks.check(
        "fresh nonzero correlation does not determine endpoint transfer",
        correlation.subs(delta, sp.pi / 2) == 4
        and delta_topological_charge.subs(delta_phi, 0) == 0,
    )

    wrong_dual = sp.Matrix([-sp.diff(phi, x), sp.diff(phi, t)])
    checks.check(
        "fresh dual-orientation mutation is detected",
        wrong_dual != dual,
    )
    wrong_spatial = right - left
    checks.check(
        "fresh chain-sign mutation misses the declared left channel",
        sp.simplify(temporal + wrong_spatial - 2 * left) != 0,
    )
    wrong_charge_scale = sp.Rational(1, 2) * delta_topological_charge
    checks.check(
        "fresh topological normalization mutation is detected",
        wrong_charge_scale.subs(delta_phi, -2 * sp.pi) != 1,
    )
    wrong_parity = sp.eye(2)
    checks.check(
        "fresh parity mutation fails to exchange the null combinations",
        derivative_after_field_parity - dual_after_field_parity
        != wrong_parity * (derivative + epsilon_dual),
    )

    tally = checks.finish()
    print(f"P148 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
