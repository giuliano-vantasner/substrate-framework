#!/usr/bin/env python3
"""Independent volume-energy and endpoint-work review for P027."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P027-INDEPENDENT")
    flux, area, charge, length, coordinate = sp.symbols(
        "Phi A q L x", positive=True
    )
    field = flux / area
    volume_energy = sp.integrate(field**2 * area / 2, (coordinate, 0, length))
    endpoint_work = sp.integrate(charge * field, (coordinate, 0, length))
    checks.check(
        "independent volume integration gives Phi squared L over two A",
        volume_energy == flux**2 * length / (2 * area),
    )
    checks.check(
        "independent endpoint work gives q Phi L over A",
        endpoint_work == charge * flux * length / area,
    )
    checks.check(
        "the two independently derived slopes agree only at q equals Phi over two",
        sp.solve(
            sp.Eq(
                sp.diff(volume_energy, length),
                sp.diff(endpoint_work, length),
            ),
            charge,
        )
        == [flux / 2],
    )
    checks.check(
        "setting q equal to Phi doubles endpoint work relative to field energy",
        sp.simplify(endpoint_work.subs(charge, flux) / volume_energy) == 2,
    )

    area0, length0 = sp.symbols("A0 L0", positive=True)
    expanding_area = area0 * (1 + coordinate / length0)
    expanding_energy = sp.integrate(
        flux**2 / (2 * expanding_area), (coordinate, 0, length)
    )
    checks.check(
        "independent expanding-area integration gives a logarithmic counterexample",
        sp.simplify(
            expanding_energy
            - flux**2
            * length0
            * sp.log(1 + length / length0)
            / (2 * area0)
        )
        == 0
        and sp.diff(expanding_energy, length, 2) != 0,
    )

    tension = sp.symbols("sigma", positive=True)
    effective_area = flux**2 / (2 * tension)
    checks.check(
        "effective area inversion reconstructs its input tension tautologically",
        sp.simplify(flux**2 / (2 * effective_area) - tension) == 0
        and sp.diff(effective_area, tension) != 0,
    )
    total = checks.finish()
    print(f"P027 INDEPENDENT WORK-ENERGY REVIEW ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    run()
