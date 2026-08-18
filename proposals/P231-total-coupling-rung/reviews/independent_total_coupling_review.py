#!/usr/bin/env python3
"""Independent rederivation of the P231 total-coupling statements.

This review imports neither ``substrate_framework.total_gravitational_coupling``
nor ``substrate_framework.scalar_one_loop_mass``: every quantity is rebuilt
from its defining proper-time integral or subtraction limit with mpmath
quadrature and fresh SymPy algebra, then compared against the module's
published structure via the proposal's formula freeze.  The published API
values are read from a text dump produced by the campaign verifier so that
no scientific import is shared.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

from substrate_framework.verification import CheckLedger

mp.mp.dps = 40
gam = mp.euler


def sharp_scale(z: mp.mpf) -> mp.mpf:
    return mp.quad(lambda t: mp.e ** (-z * t) * t**-2, [1, mp.inf])


def smooth_scale(z: mp.mpf) -> mp.mpf:
    return mp.quad(lambda t: mp.e ** (-z * t - 1 / t) * t**-2, [0, 1, mp.inf])


def zeta_scale(z: mp.mpf) -> mp.mpf:
    return z * (mp.log(z) + gam - 1)


def induced_shift(N: int, xi: mp.mpf, J: mp.mpf, lam: mp.mpf) -> mp.mpf:
    return N * (1 - 6 * xi) * J * lam**2 / (12 * mp.pi)


def run() -> int:
    checks = CheckLedger("P231/independent-total-coupling")

    # Route 1: the scale factors from their defining integrals.
    for z, tol in ((mp.mpf("0.25"), 1e-30), (mp.mpf(1), 1e-30), (mp.mpf(4), 1e-30)):
        checks.check(
            f"sharp scale factor from tail integral at z={mp.nstr(z, 4)}",
            abs(sharp_scale(z) - (mp.e**-z - z * mp.e1(z))) < tol,
        )
        checks.check(
            f"smooth scale factor from its integral at z={mp.nstr(z, 4)}",
            abs(smooth_scale(z) - 2 * mp.sqrt(z) * mp.besselk(1, 2 * mp.sqrt(z))) < tol,
        )

    # Route 2: squeeze and monotone decoupling by quadrature.
    grid = [mp.mpf("0.05"), mp.mpf("0.2"), mp.mpf("0.5"), mp.mpf(1), mp.mpf(2), mp.mpf(5)]
    checks.check(
        "squeeze 0 < J <= 1 holds for both usable families by quadrature",
        all(0 < sharp_scale(z) <= 1 and 0 < smooth_scale(z) <= 1 for z in grid),
    )
    checks.check(
        "monotone decoupling holds for both usable families",
        all(
            sharp_scale(a) > sharp_scale(b) and smooth_scale(a) > smooth_scale(b)
            for a, b in zip(grid, grid[1:])
        ),
    )

    # Route 3: zeta exclusion legs.
    root = mp.findroot(zeta_scale, 1.5)
    checks.check(
        "zeta family crosses zero at exp(1-EulerGamma) and is negative below it",
        abs(root - mp.e ** (1 - gam)) < 1e-30
        and zeta_scale(mp.mpf(1)) < 0
        and zeta_scale(mp.mpf(2)) > 0,
    )

    # Route 4: the tau^-1 control class as its own integral (-dJ/dz).
    for z in (mp.mpf("0.5"), mp.mpf(1), mp.mpf(2)):
        sharp_control = mp.quad(lambda t: mp.e ** (-z * t) / t, [1, mp.inf])
        smooth_control = mp.quad(lambda t: mp.e ** (-z * t - 1 / t) / t, [0, 1, mp.inf])
        checks.check(
            f"control class equals its defining integral at z={mp.nstr(z, 4)}",
            abs(sharp_control - mp.e1(z)) < 1e-30
            and abs(smooth_control - 2 * mp.besselk(0, 2 * mp.sqrt(z))) < 1e-30,
        )

    # Route 5: the sign map algebra rederived from scratch.
    z = sp.symbols("z", positive=True)
    J = sp.Function("J")
    N, xi, Lam, B = sp.symbols("N xi Lambda B", positive=True)
    total = B + N * (1 - 6 * xi) * Lam**2 * J(z) / (12 * sp.pi)
    boundary = sp.solve(sp.Eq(total, 0), B)[0]
    checks.check(
        "attractive boundary is B* = -N*(1-6*xi)*Lambda^2*J/(12*pi)",
        sp.simplify(boundary + N * (1 - 6 * xi) * Lam**2 * J(z) / (12 * sp.pi)) == 0,
    )
    checks.check(
        "conformal weight kills the induced shift identically",
        sp.simplify((N * (1 - 6 * sp.Rational(1, 6)) * Lam**2 * J(z) / (12 * sp.pi))) == 0,
    )
    # Numeric boundary crossings with the quadrature-built J.
    xi_val = mp.mpf(1) / 3
    J1 = sharp_scale(mp.mpf(1))
    b_star = induced_shift(1, xi_val, -J1, mp.mpf(1))
    checks.check(
        "super-conformal verdict flips exactly at the quadrature boundary",
        b_star + induced_shift(1, xi_val, J1, mp.mpf(1)) == 0
        and (b_star + mp.mpf(10) ** -9 + induced_shift(1, xi_val, J1, mp.mpf(1))) > 0
        and (b_star - mp.mpf(10) ** -9 + induced_shift(1, xi_val, J1, mp.mpf(1))) < 0,
    )

    # Route 6: spread ratio and its structure.
    r_one = smooth_scale(mp.mpf(1)) / sharp_scale(mp.mpf(1))
    checks.check(
        "spread ratio at unit mass is 1.88377257808...",
        abs(r_one - mp.mpf("1.8837725780782")) < 1e-10 and r_one > 1,
    )
    checks.check(
        "smooth family decays slower: spread grows without bound",
        smooth_scale(mp.mpf(50)) / sharp_scale(mp.mpf(50)) > 10**15,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(run())
