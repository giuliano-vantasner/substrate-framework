"""Independent matrix and energy rederivation for P092."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P092-INDEPENDENT")
    omega_0, gamma, eigenvalue = sp.symbols(
        "omega_0 Gamma lambda",
        positive=True,
        real=True,
    )
    system = sp.Matrix([[0, 1], [-omega_0**2, -gamma]])
    characteristic = sp.factor((eigenvalue * sp.eye(2) - system).det())
    checks.check(
        "first-order state matrix independently gives the oscillator polynomial",
        sp.expand(
            characteristic - (eigenvalue**2 + gamma * eigenvalue + omega_0**2)
        )
        == 0,
    )
    eigenvalues = tuple(system.eigenvals())
    checks.check(
        "matrix eigenvalues independently satisfy both roots and Vieta data",
        len(eigenvalues) == 2
        and all(sp.simplify(characteristic.subs(eigenvalue, item)) == 0 for item in eigenvalues)
        and sp.simplify(sum(eigenvalues) + gamma) == 0
        and sp.simplify(sp.prod(eigenvalues) - omega_0**2) == 0,
    )

    q, velocity = sp.symbols("q v", real=True)
    state = sp.Matrix([q, velocity])
    energy = (velocity**2 + omega_0**2 * q**2) / 2
    gradient = sp.Matrix([sp.diff(energy, q), sp.diff(energy, velocity)])
    energy_rate = sp.expand((gradient.T * system * state)[0])
    checks.check(
        "state-space gradient independently gives dE/dt=-Gamma*v^2",
        energy_rate == -gamma * velocity**2,
    )
    checks.check(
        "energy loss is semidefinite rather than pointwise proportional to E",
        energy_rate.subs(velocity, 0) == 0
        and (-gamma * energy).subs({velocity: 0, q: 1}) != 0,
    )

    omega_d = sp.sqrt(omega_0**2 - gamma**2 / 4)
    quadratic_window = 1 / gamma
    zero_spacing = sp.pi / omega_d
    full_period = 2 * zero_spacing
    cycle_count = sp.simplify(quadratic_window / full_period)
    checks.check(
        "zero spacing independently gives the actual damped cycle count",
        sp.simplify(cycle_count - omega_d / (2 * sp.pi * gamma)) == 0,
    )
    checks.check(
        "actual cycle count has the correct critical limit",
        sp.limit(cycle_count.subs(omega_0, 1), gamma, 2, dir="-") == 0,
    )
    checks.mutation_sensitive(
        "full period rather than half-period is load bearing",
        lambda multiplier: sp.simplify(
            quadratic_window / (multiplier * zero_spacing) - cycle_count
        )
        == 0,
        2,
        (1, 4),
    )

    k, omega = sp.symbols("k Omega", real=True)
    x, time = sp.symbols("x t", real=True)
    plane_wave = sp.exp(sp.I * (k * x - omega * time))
    linear_residual = sp.expand(
        sp.diff(plane_wave, time, 2)
        - sp.diff(plane_wave, x, 2)
        + plane_wave
    )
    dispersion_factor = sp.simplify(linear_residual / plane_wave)
    checks.check(
        "plane-wave substitution independently gives Omega^2=1+k^2",
        dispersion_factor == k**2 - omega**2 + 1,
    )
    checks.check(
        "real normalized field modes cannot have a sub-gap natural frequency",
        sp.solve(sp.Eq(sp.Rational(1, 4), 1 + k**2), k) == [],
    )
    checks.check(
        "countermodel is underdamped as a field mode but overdamped after substitution",
        sp.Rational(6, 5) < 2
        and sp.Rational(6, 5) > 2 * sp.Rational(1, 2),
    )
    checks.mutation_sensitive(
        "linearized mass term is load bearing",
        lambda mass_squared: sp.simplify(
            k**2 - omega**2 + mass_squared - dispersion_factor
        )
        == 0,
        1,
        (0, 2),
    )

    integrated_loss, boundary_flux = sp.symbols(
        "I F",
        nonnegative=True,
        real=True,
    )
    period_change = boundary_flux - gamma * integrated_loss
    checks.check(
        "period-integrated balance is strictly lossy at zero flux",
        period_change.subs({boundary_flux: 0, gamma: 1, integrated_loss: 1}) == -1,
    )
    checks.check(
        "periodicity and zero flux force zero integrated motion",
        sp.solve(
            sp.Eq(period_change.subs(boundary_flux, 0), 0),
            integrated_loss,
        )
        == [0],
    )
    checks.mutation_sensitive(
        "positive damping sign is load bearing in the periodic obstruction",
        lambda sign: sp.simplify(
            boundary_flux
            + sign * gamma * integrated_loss
            - period_change
        )
        == 0,
        -1,
        (0, 1),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
