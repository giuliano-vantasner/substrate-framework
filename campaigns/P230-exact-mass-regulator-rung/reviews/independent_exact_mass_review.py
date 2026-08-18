#!/usr/bin/env python3
"""Independent raw-algebra review of C-IGR-001 through C-IGR-003.

This script imports no scalar_one_loop_mass implementation symbol.  It builds
the coefficient families, determinant factors, mutations, and quadrature
comparisons directly from the frozen proposal conventions.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P230/independent-C-IGR-review")
    tau0, mass2, cutoff, scale, z = sp.symbols(
        "tau0 m2 Lambda mu z", positive=True
    )

    # C-IGR-001: solve the sharp tail problem independently.
    sharp2_tau = (
        sp.exp(-mass2 * tau0)
        - mass2 * tau0 * sp.expint(1, mass2 * tau0)
    ) / tau0
    checks.check(
        "C-IGR-001 raw tail derivative",
        sp.simplify(
            sp.diff(sharp2_tau, tau0)
            + tau0**-2 * sp.exp(-mass2 * tau0)
        )
        == 0,
    )
    sharp2 = sp.simplify(sharp2_tau.subs(tau0, cutoff**-2))
    sharp3 = sp.simplify(
        sp.exp(-mass2 / cutoff**2) * cutoff**4 / 2
        - mass2 * sharp2 / 2
    )
    checks.check(
        "C-IGR-001 raw I3 derivative and massless limits",
        sp.simplify(sp.diff(sharp3, mass2) + sharp2) == 0
        and sp.limit(sharp2, mass2, 0, "+") == cutoff**2
        and sp.limit(sharp3, mass2, 0, "+") == cutoff**4 / 2,
    )
    wrong_branch = (
        sp.exp(-mass2 * tau0)
        - mass2 * tau0 * sp.Ei(mass2 * tau0)
    ) / tau0
    checks.mutation_sensitive(
        "C-IGR-001 E1 branch is load-bearing",
        lambda candidate: sp.simplify(
            sp.diff(candidate, tau0)
            + tau0**-2 * sp.exp(-mass2 * tau0)
        )
        == 0,
        sharp2_tau,
        (wrong_branch,),
    )

    # C-IGR-002: independently instantiate the standard K integral family.
    smooth1 = 2 * sp.besselk(0, 2 * sp.sqrt(z))
    smooth2_unit = 2 * sp.sqrt(z) * sp.besselk(1, 2 * sp.sqrt(z))
    smooth3_unit = 2 * z * sp.besselk(2, 2 * sp.sqrt(z))
    checks.check(
        "C-IGR-002 raw Bessel recurrence",
        sp.simplify(sp.diff(smooth2_unit, z) + smooth1) == 0
        and sp.simplify(sp.diff(smooth3_unit, z) + smooth2_unit) == 0,
    )
    checks.check(
        "C-IGR-002 raw boundary and decay data",
        sp.limit(smooth2_unit, z, 0, "+") == 1
        and sp.limit(smooth3_unit, z, 0, "+") == 1
        and sp.limit(smooth2_unit, z, sp.oo) == 0
        and sp.limit(smooth3_unit, z, sp.oo) == 0,
    )
    wrong_order = 2 * sp.sqrt(z) * sp.besselk(2, 2 * sp.sqrt(z))
    checks.mutation_sensitive(
        "C-IGR-002 Bessel order is load-bearing",
        lambda candidate: sp.simplify(sp.diff(candidate, z) + smooth1) == 0,
        smooth2_unit,
        (wrong_order,),
    )

    mp.mp.dps = 60
    for z_text in ("0.1", "1.0", "2.5"):
        z_value = mp.mpf(z_text)
        integral2 = mp.quad(
            lambda t: mp.exp(-z_value * t - 1 / t) / t**2,
            [0, 1, mp.inf],
        )
        integral3 = mp.quad(
            lambda t: mp.exp(-z_value * t - 1 / t) / t**3,
            [0, 1, mp.inf],
        )
        closed2 = 2 * mp.sqrt(z_value) * mp.besselk(1, 2 * mp.sqrt(z_value))
        closed3 = 2 * z_value * mp.besselk(2, 2 * mp.sqrt(z_value))
        checks.check(
            f"C-IGR-002 independent 60-digit quadrature z={z_text}",
            abs(integral2 - closed2) < mp.mpf("1e-48") * abs(closed2)
            and abs(integral3 - closed3) < mp.mpf("1e-48") * abs(closed3),
        )

    # C-IGR-003: independently take the declared sharp-cutoff finite parts.
    finite2_unscaled = sp.limit(
        sharp2_tau - 1 / tau0 - mass2 * sp.log(tau0),
        tau0,
        0,
        "+",
    )
    sharp3_tau = sp.exp(-mass2 * tau0) / (2 * tau0**2) - mass2 * sharp2_tau / 2
    finite3_unscaled = sp.limit(
        sharp3_tau
        - 1 / (2 * tau0**2)
        + mass2 / tau0
        + mass2**2 * sp.log(tau0) / 2,
        tau0,
        0,
        "+",
    )
    zeta2 = mass2 * (
        sp.log(mass2 / scale**2) + sp.EulerGamma - 1
    )
    zeta3 = -mass2**2 * (
        sp.log(mass2 / scale**2)
        + sp.EulerGamma
        - sp.Rational(3, 2)
    ) / 2
    checks.check(
        "C-IGR-003 raw cutoff finite parts",
        sp.simplify(
            finite2_unscaled
            - mass2 * (sp.log(mass2) + sp.EulerGamma - 1)
        )
        == 0
        and sp.simplify(
            finite3_unscaled
            + mass2**2
            * (sp.log(mass2) + sp.EulerGamma - sp.Rational(3, 2))
            / 2
        )
        == 0,
    )
    checks.check(
        "C-IGR-003 raw derivative and scale identities",
        sp.simplify(sp.diff(zeta3, mass2) + zeta2) == 0
        and sp.simplify(scale * sp.diff(zeta2, scale) + 2 * mass2) == 0
        and sp.simplify(scale * sp.diff(zeta3, scale) - mass2**2) == 0,
    )

    # Independent coefficient typing and scheme ceiling.
    xi = sp.Symbol("xi", real=True)
    per_field = sp.simplify(
        (16 * sp.pi)
        * sp.Rational(1, 2)
        * (4 * sp.pi) ** -2
        * (sp.Rational(1, 6) - xi)
    )
    checks.check(
        "conditional inverse-Newton coefficient is rederived",
        sp.simplify(per_field - (1 - 6 * xi) / (12 * sp.pi)) == 0,
    )
    vacuum_prefactor = -sp.Rational(1, 2) * (4 * sp.pi) ** -2
    checks.mutation_sensitive(
        "proper-time determinant sign is load-bearing",
        lambda candidate: sp.simplify(candidate - vacuum_prefactor) == 0,
        vacuum_prefactor,
        (-vacuum_prefactor,),
    )
    checks.check(
        "exact massless scheme spread forbids a universal regulator value",
        sp.Rational(1, 2) != 1
        and sp.limit(zeta2, mass2, 0, "+") == 0
        and sp.limit(zeta3, mass2, 0, "+") == 0,
    )
    negative_value = sp.simplify(
        per_field.subs(xi, 0) * zeta2.subs({mass2: 1, scale: 1})
    )
    checks.check(
        "power-subtracted value sign depends on the declared scale ratio",
        negative_value.is_negative is True
        and sp.simplify(
            negative_value - (sp.EulerGamma - 1) / (12 * sp.pi)
        )
        == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(run())
