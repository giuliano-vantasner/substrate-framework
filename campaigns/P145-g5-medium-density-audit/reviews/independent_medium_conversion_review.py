#!/usr/bin/env python3
"""Fresh exact SI-dimension and conversion review for proposed C-MED-005."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P145-independent")

    epsilon_dim = sp.Matrix([-1, -3, 4, 2])
    mu_dim = sp.Matrix([1, 1, -2, -2])
    inverse_mu_dim = -mu_dim
    density_dim = sp.Matrix([1, -3, 0, 0])
    stiffness_dim = sp.Matrix([1, -1, -2, 0])
    speed_dim = sp.Matrix([0, 1, -1, 0])
    newton_dim = sp.Matrix([-1, 3, -2, 0])

    conversion_from_density = density_dim - epsilon_dim
    conversion_from_stiffness = stiffness_dim - inverse_mu_dim
    checks.check(
        "independent unit elimination gives one shared conversion dimension",
        conversion_from_density
        == conversion_from_stiffness
        == sp.Matrix([2, 0, -4, -2]),
    )
    checks.check(
        "unconverted SI coefficients have neither mechanical dimension",
        epsilon_dim != density_dim and inverse_mu_dim != stiffness_dim,
    )
    checks.check(
        "the electromagnetic coefficient ratio is speed squared",
        inverse_mu_dim - epsilon_dim == 2 * speed_dim,
    )

    epsilon, inverse_mu, a, b, xi, scale = sp.symbols(
        "epsilon mu_inv a b xi scale",
        positive=True,
    )
    rho = a * epsilon
    stiffness = b * inverse_mu
    mechanical_speed_squared = sp.cancel(stiffness / rho)
    electromagnetic_speed_squared = sp.cancel(inverse_mu / epsilon)
    checks.check(
        "direct elimination retains b over a in mechanical speed",
        mechanical_speed_squared
        == b * inverse_mu / (a * epsilon),
    )
    checks.check(
        "independent solve selects b equals a",
        sp.solve(
            sp.Eq(mechanical_speed_squared, electromagnetic_speed_squared),
            b,
        )
        == [a],
    )
    checks.check(
        "equal conversion leaves an arbitrary common scale",
        sp.simplify(
            mechanical_speed_squared.subs(b, a)
            - mechanical_speed_squared.subs({a: scale * a, b: scale * a})
        )
        == 0,
    )
    checks.check(
        "density and stiffness scale on that null orbit",
        (scale * a * epsilon) / rho == scale
        and (scale * a * inverse_mu) / stiffness.subs(b, a) == scale,
    )

    strain_energy = sp.simplify(stiffness * xi**2 / 2)
    mass_equivalent = sp.simplify(strain_energy / mechanical_speed_squared)
    checks.check(
        "fresh energy route retains calibration and strain amplitude",
        strain_energy == b * inverse_mu * xi**2 / 2
        and mass_equivalent == a * epsilon * xi**2 / 2,
    )
    checks.check(
        "unit strain energy mass is half the inertia coefficient",
        mass_equivalent.subs(xi, 1) == rho / 2,
    )
    checks.check(
        "amplitude mutation changes energy quadratically",
        sp.simplify(
            strain_energy.subs(xi, 3) / strain_energy.subs(xi, 1)
        )
        == 9,
    )

    source_rows = sp.Matrix(
        [
            [-1, -1, 0],
            [1, 0, 0],
            [0, -1, 0],
            [1, 1, 1],
        ]
    )
    checks.check(
        "fresh log design gives rank two for L1 through L3",
        source_rows[:3, :].rank() == 2,
    )
    checks.check(
        "fresh left relation proves L3 is algebraically dependent",
        sp.Matrix([-1, -1, 1]).T * source_rows[:3, :]
        == sp.zeros(1, 3),
    )
    checks.check(
        "free-kappa L4 consumes the third input direction",
        source_rows.rank() == 3,
    )
    checks.check(
        "the full source ledger has exactly one tautological left relation",
        len(source_rows.T.nullspace()) == 1
        and source_rows.T.nullspace()[0]
        == sp.Matrix([-1, -1, 1, 0]),
    )

    operator_dim = sp.Matrix([0, -2, 0, 0])
    energy_source_dim = sp.Matrix([1, -1, -2, 0])
    mass_source_dim = sp.Matrix([1, -3, 0, 0])
    checks.check(
        "energy-source Einstein coupling has G over c fourth dimension",
        operator_dim - energy_source_dim
        == newton_dim - 4 * speed_dim,
    )
    checks.check(
        "mass-source Einstein coupling has G over c squared dimension",
        operator_dim - mass_source_dim
        == newton_dim - 2 * speed_dim,
    )
    checks.check(
        "bare Newton dimension matches neither typed source coupling",
        newton_dim != operator_dim - energy_source_dim
        and newton_dim != operator_dim - mass_source_dim,
    )
    checks.check(
        "conditional G times epsilon mu has G over c squared dimension",
        newton_dim + epsilon_dim + mu_dim
        == newton_dim - 2 * speed_dim,
    )

    wrong_conversion = sp.Matrix([2, 0, -4, -1])
    checks.check(
        "electric-current exponent mutation breaks both mechanical maps",
        epsilon_dim + wrong_conversion != density_dim
        and inverse_mu_dim + wrong_conversion != stiffness_dim,
    )
    checks.check(
        "unequal-factor mutation doubles speed squared",
        mechanical_speed_squared.subs(b, 2 * a)
        == 2 * electromagnetic_speed_squared,
    )

    total = checks.finish()
    print(f"P145 INDEPENDENT ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(run())
