"""Exact regular-chart gates frozen for P240 attempt 0007."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P240/regular-axis-chart")
    rho, z, core = sp.symbols("rho z core", positive=True)
    anisotropy, common, split, angle_control, radial_boost = sp.symbols(
        "anisotropy common split angle_control radial_boost", finite=True
    )
    wrong_split, wrong_angle = sp.symbols(
        "wrong_split wrong_angle", positive=True
    )
    radius_squared = rho**2 + z**2
    q_radius = radius_squared / (radius_squared + core**2)
    q_axis = rho**2 / (rho**2 + core**2)
    q_vector = rho / sp.sqrt(rho**2 + core**2)
    director = common + q_radius * anisotropy
    tangent = common + q_axis * split
    azimuthal = common - q_axis * split

    ledger.check(
        "origin isotropy",
        all(
            sp.limit(value, rho, 0).subs(z, 0) == common
            for value in (director, tangent, azimuthal)
        ),
    )
    ledger.check(
        "axis transverse degeneracy",
        sp.simplify(sp.limit(tangent - azimuthal, rho, 0)) == 0,
    )
    ledger.check(
        "quadratic transverse split",
        sp.limit((tangent - azimuthal) / rho**2, rho, 0)
        == 2 * split / core**2,
    )
    ledger.check(
        "quadratic origin anisotropy",
        sp.limit((director - common).subs(z, 0) / rho**2, rho, 0)
        == anisotropy / core**2,
    )
    ledger.check(
        "axis director alignment",
        sp.limit(q_vector * angle_control, rho, 0) == 0,
    )
    ledger.check(
        "axis radial boost",
        sp.limit(q_vector * radial_boost, rho, 0) == 0,
    )
    boundary_anisotropy = 1 / q_radius
    boundary_values = (
        sp.simplify((common + q_radius * boundary_anisotropy).subs(common, 0)),
        sp.simplify(tangent.subs({common: 0, split: 0})),
        sp.simplify(azimuthal.subs({common: 0, split: 0})),
    )
    ledger.check("vacuum boundary decoding", boundary_values == (1, 0, 0))
    ledger.check(
        "wrong split chart mutation",
        sp.limit(2 * wrong_split / rho**2, rho, 0) == sp.oo,
    )
    ledger.check(
        "wrong vector chart mutation",
        sp.limit(wrong_angle / rho, rho, 0) == sp.oo,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
