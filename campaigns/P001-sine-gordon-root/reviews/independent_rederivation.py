#!/usr/bin/env python3
"""Independent exact review route for C-SG-001 and C-SG-002.

This file intentionally does not import ``substrate_framework.sine_gordon``.
It rebuilds the normalized field equation and evaluates the energy on the
quarter-period static slice, whereas the proposal verifier uses the zero-field
kinetic slice for its exact integral.
"""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P001-INDEPENDENT-REVIEW")
    x, t = sp.symbols("x t", real=True)
    omega = sp.symbols("omega", positive=True)
    eta = sp.sqrt(1 - omega**2)

    argument = eta * sp.sin(omega * t) / (omega * sp.cosh(eta * x))
    phi = 4 * sp.atan(argument)
    residual = sp.diff(phi, t, 2) - sp.diff(phi, x, 2) + sp.sin(phi)
    checks.check(
        "independently reconstructed field is exactly on shell",
        sp.simplify(residual) == 0,
    )
    checks.check(
        "field is localized for positive inverse width",
        sp.limit(
            4
            * sp.atan(
                sp.symbols("a", positive=True)
                * sp.sin(omega * t)
                / (
                    omega
                    * sp.cosh(sp.symbols("a", positive=True) * x)
                )
            ),
            x,
            sp.oo,
        )
        == 0,
    )

    peak_time = sp.pi / (2 * omega)
    peak_field = sp.simplify(phi.subs(t, peak_time))
    peak_density = sp.simplify(
        sp.diff(peak_field, x) ** 2 / 2 + 1 - sp.cos(peak_field)
    )
    peak_argument = eta / (omega * sp.cosh(eta * x))
    factored_peak_density = sp.simplify(
        8
        * peak_argument**2
        * (1 + eta**2 * sp.tanh(eta * x) ** 2)
        / (1 + peak_argument**2) ** 2
    )
    checks.check(
        "quarter-period gradient and potential density factor exactly",
        sp.simplify(peak_density - factored_peak_density) == 0,
    )

    y = sp.symbols("y", real=True)
    transformed_integrand = sp.simplify(
        8
        * eta
        * omega**2
        * (1 + eta**2 * y**2)
        / (1 - eta**2 * y**2) ** 2
    )
    antiderivative = sp.simplify(8 * eta * omega**2 * y / (1 - eta**2 * y**2))
    density_after_change = sp.simplify(
        8
        * (eta**2 * (1 - y**2) / omega**2)
        * (1 + eta**2 * y**2)
        / (1 + eta**2 * (1 - y**2) / omega**2) ** 2
        / (eta * (1 - y**2))
    )
    checks.check(
        "quarter-period density transforms under y=tanh(eta*x)",
        sp.simplify(density_after_change - transformed_integrand) == 0,
    )
    checks.check(
        "transformed energy integrand has the stated exact antiderivative",
        sp.simplify(sp.diff(antiderivative, y) - transformed_integrand) == 0,
    )
    peak_energy = sp.simplify(antiderivative.subs(y, 1) - antiderivative.subs(y, -1))
    checks.check(
        "independent quarter-period integral gives 16*sqrt(1-omega^2)",
        sp.simplify(peak_energy - 16 * eta) == 0,
    )
    checks.check(
        "independent result reaches kink-pair threshold at omega to zero",
        sp.limit(peak_energy, omega, 0, dir="+") == 16,
    )
    checks.check(
        "independent result vanishes at omega to one",
        sp.limit(peak_energy, omega, 1, dir="-") == 0,
    )

    wrong_width = sp.sqrt(1 + omega**2)
    wrong_phi = 4 * sp.atan(
        wrong_width
        * sp.sin(omega * t)
        / (omega * sp.cosh(wrong_width * x))
    )
    wrong_residual = (
        sp.diff(wrong_phi, t, 2)
        - sp.diff(wrong_phi, x, 2)
        + sp.sin(wrong_phi)
    )
    wrong_probe = sp.simplify(
        wrong_residual.subs(
            {omega: sp.Rational(3, 5), x: 0, t: 5 * sp.pi / 6}
        )
    )
    checks.check(
        "independent wrong-width counterexample is off shell",
        wrong_probe != 0,
    )

    total = checks.finish()
    print(f"P001 INDEPENDENT REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
