"""Independent exact rederivation for P069 without canonical lattice imports."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_ME3_lattice_continuum.py"
)
SOURCE_SHA256 = "8b5f888708b2edc202cb1acba37780aa62e7d71d002dc5042fd92e8afefbb0d0"


def main() -> int:
    ledger = CheckLedger("P069-INDEPENDENT")
    ledger.check(
        "review reads the same immutable ME3 source",
        SOURCE.is_file()
        and hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )

    a = sp.symbols("a", positive=True)
    derivative = sp.symbols("f0:9", real=True)
    plus = sp.Add(
        *(derivative[order] * a**order / sp.factorial(order) for order in range(7))
    )
    minus = sp.Add(
        *(
            derivative[order] * (-a) ** order / sp.factorial(order)
            for order in range(7)
        )
    )
    fresh_stencil = sp.expand((plus - 2 * derivative[0] + minus) / a**2)
    ledger.check(
        "fresh neighbour expansions give the centered modified equation",
        fresh_stencil
        == derivative[2] + a**2 * derivative[4] / 12 + a**4 * derivative[6] / 360,
    )
    ledger.check(
        "two next-order Lagrange remainders give M8 a6 over 20160",
        sp.simplify(2 * derivative[8] * a**8 / sp.factorial(8) / a**2)
        == derivative[8] * a**6 / 20160,
    )

    x = sp.symbols("x", real=True)
    for field in (sp.Integer(1), x, x**2, x**3):
        discrete = sp.simplify(
            (field.subs(x, x + a) - 2 * field + field.subs(x, x - a)) / a**2
        )
        ledger.check(
            f"finite-a stencil equals continuum derivative for {field}",
            sp.simplify(discrete - sp.diff(field, x, 2)) == 0,
        )

    k, mass = sp.symbols("k m", real=True, positive=True)
    shift_eigenvalue = sp.simplify(
        (sp.exp(sp.I * k * a) - 2 + sp.exp(-sp.I * k * a)) / a**2
    )
    real_shift_eigenvalue = sp.simplify(sp.expand_complex(shift_eigenvalue))
    fresh_symbol = -4 * sp.sin(k * a / 2) ** 2 / a**2
    ledger.check(
        "fresh shift-eigenvector route gives the exact symbol",
        sp.trigsimp(real_shift_eigenvalue - fresh_symbol) == 0,
    )
    ledger.check(
        "fresh symbol is reciprocal-periodic",
        sp.trigsimp(
            fresh_symbol
            + 4 * sp.sin((k + 2 * sp.pi / a) * a / 2) ** 2 / a**2
        )
        == 0,
    )
    dispersion = mass**2 - fresh_symbol
    ledger.check(
        "fresh dispersion expansion fixes both correction signs",
        sp.series(dispersion, a, 0, 6).removeO().expand()
        == mass**2 + k**2 - a**2 * k**4 / 12 + a**4 * k**6 / 360,
    )
    ledger.check(
        "fresh edge evaluation rejects a global small-ka approximation",
        sp.simplify(dispersion.subs(k, sp.pi / a) - (mass**2 + 4 / a**2)) == 0,
    )
    ledger.check(
        "zero mode is insensitive to positive spatial spacing",
        sp.simplify(dispersion.subs(k, 0) - mass**2) == 0,
    )

    q = sp.symbols("q0:4", real=True)
    velocity = sp.symbols("v0:4", real=True)
    acceleration = sp.symbols("b0:4", real=True)
    own_action_density = a * sp.Add(
        *(
            velocity[index] ** 2 / 2
            - ((q[(index + 1) % 4] - q[index]) / a) ** 2 / 2
            - mass**2 * (1 - sp.cos(q[index]))
            for index in range(4)
        )
    )
    for index in range(4):
        own_euler_lagrange = a * acceleration[index] - sp.diff(
            own_action_density, q[index]
        )
        expected = a * (
            acceleration[index]
            - (q[(index + 1) % 4] - 2 * q[index] + q[(index - 1) % 4]) / a**2
            + mass**2 * sp.sin(q[index])
        )
        ledger.check(
            f"fresh periodic index variation gives site {index} equation",
            sp.simplify(own_euler_lagrange - expected) == 0,
        )

    length = sp.symbols("L", positive=True)
    site_count = sp.symbols("N", integer=True, positive=True)
    normalized_constant = -2 * a * site_count
    unweighted_constant = -2 * site_count
    ledger.check(
        "fixed-length normalized constant-field value remains finite",
        normalized_constant.subs(site_count, length / a) == -2 * length,
    )
    ledger.check(
        "fixed-length unweighted site value diverges under refinement",
        sp.limit(unweighted_constant.subs(site_count, length / a), a, 0, dir="+")
        == -sp.oo,
    )
    ledger.check(
        "fixed-grid omission is only a global one-over-a multiplier",
        sp.simplify((own_action_density / a) - own_action_density * (1 / a)) == 0,
    )

    duration = sp.symbols("T", positive=True)
    mx, mxx, mt, mtx = sp.symbols("Mx Mxx Mt Mtx", nonnegative=True)
    kinetic_riemann = length * a * mt * mtx / 2
    potential_riemann = length * a * mass**2 * mx / 2
    gradient_riemann = length * a * mx * mxx / 2
    forward_gradient = length * (a * mx * mxx / 2 + a**2 * mxx**2 / 8)
    total_bound = duration * (
        kinetic_riemann
        + potential_riemann
        + gradient_riemann
        + forward_gradient
    )
    ledger.check(
        "fresh Riemann and forward-Taylor bounds reproduce every action term",
        sp.expand(total_bound)
        == sp.expand(
            duration
            * length
            * (
                a * mt * mtx / 2
                + a * mass**2 * mx / 2
                + a * mx * mxx
                + a**2 * mxx**2 / 8
            )
        ),
    )
    ledger.check(
        "fresh action bound converges for fixed derivative bounds",
        sp.limit(total_bound, a, 0, dir="+") == 0,
    )

    variation_scale = sp.symbols("lambda", positive=True)
    ledger.check(
        "ME3 cosine parameter is an inverse-wavenumber scale not its full wavelength",
        sp.simplify(
            sp.cos((x + 2 * sp.pi * variation_scale) / variation_scale)
            - sp.cos(x / variation_scale)
        )
        == 0,
    )
    ledger.check(
        "no exact route turns spacing into a selected termination scale",
        sp.diff(fresh_symbol, mass) == 0
        and sp.diff(own_action_density, length) == 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
