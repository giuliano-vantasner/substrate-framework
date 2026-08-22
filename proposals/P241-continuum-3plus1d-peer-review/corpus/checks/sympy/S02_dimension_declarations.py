"""P241 audit oracle — Section 2 unit bullets are internally inconsistent; consistent table supplied.

Standalone module: python3 S02_dimension_declarations.py
"""

from __future__ import annotations

import json

import sympy as sp

from _util import _check


def check_dimension_declarations() -> dict[str, object]:
    """Section 2 unit bullets are internally inconsistent; consistent table given.

    With u dimensionless, the gradient pair ([Theta]=N, [du]=1/m) is
    self-consistent, but then c0^2=Theta0/rho0 carries dimension m^4/s^2,
    not speed^2; also rho*(Dt u)^2 ~ kg m^-3 s^-2 is not an energy density.
    The consistent table takes u as a length-dimension displacement and
    [Theta] = Pa = J/m^3, after which c0 and Z0 carry the printed units.
    """
    M, L, T = 0, 1, 2
    vec = lambda *c: sp.Matrix(c)
    rho_dim = vec(1, -3, 0)          # kg/m^3
    energy_density = vec(1, -1, -2)  # J/m^3 = Pa
    newton = vec(1, 1, -2)           # N
    speed_sq = vec(0, 2, -2)
    kinetic_uless = rho_dim + vec(0, 0, -2)          # rho*(Dt u)^2, u dimensionless
    c0sq_thetaN = newton - rho_dim                   # Theta0/rho0 with Theta=N
    theta_pa = energy_density                        # required [Theta] under u~L
    c0sq_thetaPa = theta_pa - rho_dim                # Theta0/rho0 with Theta=Pa
    z0_dim = (theta_pa + rho_dim) / 2                # sqrt(Theta0*rho0)
    z_claimed = vec(1, -2, -1)                       # kg m^-2 s^-1 (printed)
    inconsistent = (kinetic_uless != energy_density) or (c0sq_thetaN != speed_sq)
    repair_ok = (c0sq_thetaPa == speed_sq) and (z0_dim == z_claimed)
    return _check(
        "dimension_declarations_audit",
        "P241-S02 Section-2 bullets, (3)",
        bool(inconsistent and repair_ok),
        (
            "u dimensionless: rho*(Dt u)^2 dim {} != energy density {}; "
            "[Theta]=N gives c0^2 dim {} != {} (speed^2). "
            "Consistent table: u length-dimension, [Theta]={} (Pa): "
            "c0^2 -> {} (speed^2), [sqrt(Theta0*rho0)]={} == printed kg m^-2 s^-1."
        ).format(
            list(kinetic_uless), list(energy_density),
            list(c0sq_thetaN), list(speed_sq),
            list(theta_pa), list(c0sq_thetaPa), list(z0_dim),
        ),
    )

if __name__ == "__main__":
    result = check_dimension_declarations()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)
