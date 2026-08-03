"""Independent rederivation for C-LAT-002 and C-MED-004.

This review deliberately imports neither canonical claim module.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-27/"
    "bridge_MC3_per_medium_omega0.py"
)
SOURCE_SHA256 = "74fbddc086781a0d61d5dd22effabf48d7ff37f47c6d97ebde0b2fb6186464a5"


def main() -> int:
    checks = CheckLedger("P097-INDEPENDENT")
    source_text = SOURCE.read_text(encoding="utf-8")
    checks.check(
        "reviewed source is the pinned MC3 object",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )

    review_tree = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    imported_modules = {
        node.module
        for node in ast.walk(review_tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    checks.check(
        "review imports no canonical lattice or mixed-coordinate module",
        "substrate_framework.lattice_scalar" not in imported_modules
        and "substrate_framework.mixed_sine_gordon" not in imported_modules,
    )

    inertia, coupling, onsite, spacing = sp.symbols("I K V0 a", positive=True)
    q = sp.symbols("q0:4", real=True)
    speed = sp.symbols("v0:4", real=True)
    acceleration = sp.symbols("b0:4", real=True)
    lagrangian = sp.Add(
        *(
            inertia * speed[index] ** 2 / 2
            - coupling * (q[(index + 1) % 4] - value) ** 2 / 2
            - onsite * (1 - sp.cos(value))
            for index, value in enumerate(q)
        )
    )
    residuals = tuple(
        sp.simplify(
            inertia * acceleration[index]
            - coupling * (q[(index + 1) % 4] - 2 * value + q[index - 1])
            + onsite * sp.sin(value)
        )
        for index, value in enumerate(q)
    )
    checks.check(
        "fresh site variation derives all four periodic equations",
        all(
            sp.simplify(
                inertia * acceleration[index]
                - sp.diff(lagrangian, q[index])
                - residuals[index]
            )
            == 0
            for index in range(4)
        ),
    )

    k, angular, site = sp.symbols("k Omega j", real=True)
    mode = lambda offset: sp.exp(sp.I * (k * (site + offset) * spacing))
    stencil_ratio = sp.simplify(
        (mode(1) - 2 * mode(0) + mode(-1)) / mode(0)
    )
    stencil_ratio = sp.trigsimp(sp.expand_complex(stencil_ratio))
    expected_stencil = -4 * sp.sin(k * spacing / 2) ** 2
    checks.check(
        "fresh shift substitution derives the exact stencil symbol",
        sp.trigsimp(stencil_ratio - expected_stencil) == 0,
    )
    characteristic = -inertia * angular**2 - coupling * stencil_ratio + onsite
    solved = sp.solve(sp.Eq(characteristic, 0), angular**2)[0]
    expected_dispersion = (
        onsite + 4 * coupling * sp.sin(k * spacing / 2) ** 2
    ) / inertia
    checks.check(
        "fresh characteristic derives the physical dispersion",
        sp.trigsimp(solved - expected_dispersion) == 0,
    )
    checks.check(
        "independent long-wave series retains the lattice correction",
        sp.series(expected_dispersion, k, 0, 6).removeO().expand()
        == onsite / inertia
        + coupling * spacing**2 * k**2 / inertia
        - coupling * spacing**4 * k**4 / (12 * inertia),
    )
    checks.check(
        "independent gap and band edge come from the same branch",
        expected_dispersion.subs(k, 0) == onsite / inertia
        and sp.trigsimp(
            expected_dispersion.subs(k, sp.pi / spacing)
            - (onsite + 4 * coupling) / inertia
        )
        == 0,
    )

    energy_dimension = sp.Matrix([1, 2, -2])
    mass_dimension = sp.Matrix([1, 0, 0])
    length_dimension = sp.Matrix([0, 1, 0])
    checks.check(
        "sqrt energy over mass has speed rather than frequency dimensions",
        (energy_dimension - mass_dimension) / 2 == sp.Matrix([0, 1, -1]),
    )
    checks.check(
        "m times b squared has the required phase-inertia dimensions",
        mass_dimension + 2 * length_dimension == sp.Matrix([1, 2, 0])
        and (
            energy_dimension
            - (mass_dimension + 2 * length_dimension)
        )
        / 2
        == sp.Matrix([0, 0, -1]),
    )

    mass_h, mass_d = sp.symbols("m_H m_D", positive=True)
    scale_h, scale_d = sp.symbols("b_H b_D", positive=True)
    onsite_h, onsite_d = sp.symbols("V_H V_D", positive=True)
    ratio = sp.sqrt(
        onsite_h * mass_d * scale_d**2
        / (onsite_d * mass_h * scale_h**2)
    )
    common = {onsite_d: onsite_h, scale_d: scale_h, mass_d: 2 * mass_h}
    checks.check(
        "fresh host ratio reduces to sqrt two under three exact premises",
        sp.simplify(ratio.subs(common) - sp.sqrt(2)) == 0,
    )
    checks.check(
        "curvature counterfamily removes the nominal isotope shift",
        sp.simplify(ratio.subs({**common, onsite_d: 2 * onsite_h}) - 1) == 0,
    )
    checks.check(
        "coordinate-scale counterfamily removes the nominal isotope shift",
        sp.simplify(
            ratio.subs({**common, scale_d: scale_h / sp.sqrt(2)}) - 1
        )
        == 0,
    )
    checks.check(
        "gap closure is a coefficient limit rather than an existence theorem",
        sp.limit(sp.sqrt(onsite / inertia), onsite, 0, dir="+") == 0
        and "hosts_breather_lattice" in source_text,
    )

    z, tau, g = sp.symbols("z tau g", positive=True)
    plane = sp.exp(sp.I * (k * z - angular * tau))
    mixed_characteristic = sp.simplify(
        (sp.diff(plane, z, tau) - g * plane) / plane
    )
    checks.check(
        "fresh mixed plane wave gives k times Omega minus g",
        mixed_characteristic == k * angular - g,
    )
    checks.mutation_sensitive(
        "independent characteristic rejects Klein-Gordon substitutions",
        lambda candidate: sp.simplify(candidate - mixed_characteristic) == 0,
        k * angular - g,
        (angular**2 - g, angular**2 - k**2 - g, k * angular + g),
    )
    positive_k = sp.symbols("k_pos", positive=True)
    mixed_angular = g / positive_k
    checks.check(
        "fresh mixed branch has no finite frequency floor",
        sp.limit(mixed_angular, positive_k, sp.oo) == 0
        and sp.limit(mixed_angular, positive_k, 0, dir="+") == sp.oo,
    )

    mixed_dimension = sp.Matrix([-1, -1])
    absorption_dimension = sp.Matrix([-1, 0])
    frequency_squared_dimension = sp.Matrix([0, -2])
    checks.check(
        "independent units reject alpha as g or omega squared",
        mixed_dimension != absorption_dimension
        and absorption_dimension != frequency_squared_dimension,
    )
    checks.check(
        "multiplying absorption by a rate completes g dimensions",
        absorption_dimension + sp.Matrix([0, -1]) == mixed_dimension,
    )

    length, time = sp.symbols("L T", positive=True)
    checks.check(
        "normalization constraint has a reciprocal scale symmetry",
        sp.Matrix([[1, 1]]).rank() == 1
        and sp.Matrix([[1, 1]]).nullspace() == [sp.Matrix([-1, 1])]
        and sp.simplify(
            g * (2 * length) * (time / 2) - g * length * time
        )
        == 0,
    )
    normalized_time = 1 / (g * length)
    checks.check(
        "fixed g permits distinct inferred inverse-time scales",
        1 / normalized_time == g * length
        and 1 / (1 / (g * 2 * length)) == 2 * g * length,
    )

    x, clock = sp.symbols("X S", real=True)
    mapped_x = z / length + tau / time
    mapped_clock = z / length - tau / time
    trial = x**2 + 3 * clock**2 + x * clock
    pulled = trial.subs({x: mapped_x, clock: mapped_clock})
    mixed_residual = sp.diff(pulled, z, tau) - sp.sin(pulled) / (length * time)
    hyperbolic = (
        sp.diff(trial, clock, 2) - sp.diff(trial, x, 2) + sp.sin(trial)
    ).subs({x: mapped_x, clock: mapped_clock})
    checks.check(
        "fresh chain rule fixes the light-cone sign and factor",
        sp.trigsimp(mixed_residual + hyperbolic / (length * time)) == 0,
    )
    checks.check(
        "fresh inverse coordinate map recovers z and tau",
        sp.simplify(length * (mapped_x + mapped_clock) / 2 - z) == 0
        and sp.simplify(time * (mapped_x - mapped_clock) / 2 - tau) == 0,
    )

    kink = 4 * sp.atan(sp.exp(x))
    kink_residual = -sp.diff(kink, x, 2) + sp.sin(kink)
    checks.check(
        "fresh exact algebra verifies the normalized static kink",
        sp.simplify(sp.expand_trig(kink_residual)) == 0,
    )
    checks.check(
        "MC3 kink predicate never tests the declared cross derivative",
        "theta_zz = sp.diff(theta_kink, zz, 2)" in source_text
        and "sp.diff(theta_kink, x, t)" not in source_text,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
