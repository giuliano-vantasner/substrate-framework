from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P144-INDEPENDENT-C-RR-001")
    power, u, w = sp.symbols("P u w", positive=True)
    gx, gy = sp.symbols("g_x g_y", positive=True)
    velocity = sp.Matrix([u, w])
    metric = sp.diag(gx, gy)
    denominator = sp.simplify((velocity.T * metric * velocity)[0])
    particular = sp.simplify(-power * metric * velocity / denominator)

    checks.check(
        "fresh Lagrange-multiplier solution closes work balance",
        sp.simplify((particular.T * velocity)[0] + power) == 0,
    )

    alpha = sp.symbols("alpha", real=True)
    null_force = sp.Matrix([alpha * w, -alpha * u])
    checks.check(
        "fresh null-work covector is orthogonal to velocity",
        sp.simplify((null_force.T * velocity)[0]) == 0,
    )
    checks.check(
        "fresh affine family has the same scalar power",
        sp.simplify(((particular + null_force).T * velocity)[0] + power) == 0,
    )
    checks.check(
        "two distinct forces share one power when alpha is nonzero",
        sp.simplify((particular + null_force).subs(alpha, 1) - particular)
        != sp.zeros(2, 1),
    )

    inverse_metric = metric.inv()
    norm_gap = sp.simplify(
        ((particular + null_force).T * inverse_metric * (particular + null_force))[0]
        - (particular.T * inverse_metric * particular)[0]
    )
    checks.check(
        "fresh completion of squares proves the metric minimum",
        sp.simplify(norm_gap - (null_force.T * inverse_metric * null_force)[0]) == 0,
    )

    alternative_metric = sp.diag(2 * gx, gy)
    alternative_denominator = sp.simplify(
        (velocity.T * alternative_metric * velocity)[0]
    )
    alternative_particular = sp.simplify(
        -power * alternative_metric * velocity / alternative_denominator
    )
    checks.check(
        "fresh metric mutation changes components but preserves work",
        alternative_particular != particular
        and sp.simplify((alternative_particular.T * velocity)[0] + power) == 0,
    )

    scalar_rate = sp.symbols("v", nonzero=True, real=True)
    scalar_force = sp.solve(sp.Eq(sp.Symbol("F") * scalar_rate, -power), sp.Symbol("F"))[0]
    checks.check("fresh scalar solution is minus power over rate", scalar_force == -power / scalar_rate)
    arbitrary = sp.symbols("Q", real=True)
    checks.check(
        "fresh zero-rate positive-power counterexample is inconsistent",
        sp.simplify(arbitrary * 0 + power) == power,
    )
    checks.check(
        "fresh zero-rate zero-power equation leaves force arbitrary",
        sp.simplify(arbitrary * 0 + 0) == 0 and arbitrary.free_symbols == {arbitrary},
    )

    d1, d2 = sp.symbols("d_1 d_2", positive=True)
    damping = sp.diag(d1, d2)
    rayleigh = sp.simplify((velocity.T * damping * velocity)[0] / 2)
    force = sp.Matrix([-sp.diff(rayleigh, u), -sp.diff(rayleigh, w)])
    dissipated = sp.simplify(-(force.T * velocity)[0])
    checks.check(
        "fresh Rayleigh differentiation gives minus D times velocity",
        force == sp.Matrix([-d1 * u, -d2 * w]),
    )
    checks.check(
        "fresh Rayleigh work is twice the nonnegative function",
        sp.simplify(dissipated - 2 * rayleigh) == 0
        and dissipated.is_positive is True,
    )

    external_u, external_w = sp.symbols("F_u F_w", real=True)
    energy_rate = sp.simplify(
        external_u * u + external_w * w + (force.T * velocity)[0]
    )
    checks.check(
        "fresh open-system ledger keeps external work",
        sp.simplify(
            energy_rate - (external_u * u + external_w * w - dissipated)
        )
        == 0,
    )

    gamma, kappa, energy, acceleration = sp.symbols(
        "gamma kappa E0 a",
        positive=True,
    )
    g4_power = kappa * energy**2 * gamma**6 * u**2 * acceleration**2 / 8
    g4_quotient = sp.simplify(-g4_power / u)
    checks.check(
        "fresh G4 expression is exactly the assumed-power quotient",
        g4_quotient == -kappa * energy**2 * gamma**6 * u * acceleration**2 / 8,
    )
    checks.check(
        "fresh coefficient mutation remains equally balance-consistent",
        sp.simplify(
            (-kappa * energy**2 * gamma**6 * u * acceleration**2 / 4) * u
            + kappa * energy**2 * gamma**6 * u**2 * acceleration**2 / 4
        )
        == 0,
    )

    omega, time = sp.symbols("omega t", positive=True)
    period = 2 * sp.pi / omega
    checks.check(
        "fresh temporal average erases the twice-frequency harmonic",
        sp.simplify(
            sp.integrate(sp.cos(2 * omega * time), (time, 0, period)) / period
        )
        == 0,
    )

    wrong_damping = sp.diag(d1, -d2)
    wrong_power = sp.simplify((velocity.T * wrong_damping * velocity)[0])
    checks.check(
        "fresh wrong-sign damping has a negative-power counterexample",
        wrong_power.subs({u: 0, w: 1}) == -d2,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
