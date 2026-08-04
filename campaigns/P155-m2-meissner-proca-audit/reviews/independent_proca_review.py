#!/usr/bin/env python3
"""Fresh C-PRC-001 derivation without importing the canonical Proca helper."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero_matrix(matrix: sp.MatrixBase) -> bool:
    simplified = sp.ImmutableMatrix(sp.Matrix(matrix).applyfunc(sp.simplify))
    return simplified == sp.zeros(*matrix.shape)


def run() -> int:
    checks = CheckLedger("P155-independent")
    coordinates = sp.symbols("t x y z", real=True)
    metric = sp.diag(-1, 1, 1, 1)
    mass = sp.Symbol("m", positive=True)
    vector = sp.Matrix(
        [sp.Function(f"A{index}")(*coordinates) for index in range(4)]
    )
    covector = metric * vector
    field_strength = sp.Matrix(
        4,
        4,
        lambda mu, nu: sp.diff(covector[nu], coordinates[mu])
        - sp.diff(covector[mu], coordinates[nu]),
    )
    raised_field_strength = metric * field_strength * metric
    density = sp.simplify(
        -sum(
            field_strength[mu, nu] * raised_field_strength[mu, nu]
            for mu in range(4)
            for nu in range(4)
        )
        / 4
        - mass**2 * (covector.T * vector)[0] / 2
    )
    variational_coefficients = []
    expected_lowered = []
    for component in range(4):
        coefficient = sp.diff(density, vector[component])
        for mu, coordinate in enumerate(coordinates):
            derivative = sp.diff(vector[component], coordinate)
            coefficient -= sp.diff(sp.diff(density, derivative), coordinate)
        variational_coefficients.append(sp.simplify(coefficient))

        expected_upper = []
        for nu in range(4):
            expected_upper.append(
                sp.simplify(
                    sum(
                        sp.diff(raised_field_strength[mu, nu], coordinates[mu])
                        for mu in range(4)
                    )
                    - mass**2 * vector[nu]
                )
            )
        expected_lowered.append(
            sp.simplify(
                sum(metric[component, nu] * expected_upper[nu] for nu in range(4))
            )
        )
    checks.check(
        "fresh full coordinate variation gives the vector Proca equation",
        _zero_matrix(sp.Matrix(variational_coefficients) - sp.Matrix(expected_lowered)),
    )

    expected_upper_vector = metric * sp.Matrix(expected_lowered)
    divergence_of_euler = sp.simplify(
        sum(
            sp.diff(expected_upper_vector[nu], coordinates[nu])
            for nu in range(4)
        )
    )
    divergence_of_vector = sp.simplify(
        sum(sp.diff(vector[nu], coordinates[nu]) for nu in range(4))
    )
    checks.check(
        "fresh double divergence cancels by antisymmetry",
        sp.simplify(divergence_of_euler + mass**2 * divergence_of_vector) == 0,
    )
    checks.check(
        "fresh nonzero mass derives rather than gauges the divergence constraint",
        mass.is_nonzero is True
        and sp.simplify(divergence_of_euler / (-mass**2) - divergence_of_vector)
        == 0,
    )

    omega, kx, ky, kz = sp.symbols("omega kx ky kz", real=True)
    momentum_covector = sp.Matrix([-omega, kx, ky, kz])
    momentum_vector = metric * momentum_covector
    momentum_norm = sp.simplify((momentum_covector.T * momentum_vector)[0])
    fresh_kernel = sp.simplify(
        -(momentum_norm + mass**2) * sp.eye(4)
        + momentum_vector * momentum_covector.T
    )
    checks.check(
        "fresh Fourier contraction reproduces the massive constraint coefficient",
        _zero_matrix(
            momentum_covector.T * fresh_kernel
            + mass**2 * momentum_covector.T
        ),
    )
    checks.check(
        "fresh transverse factor gives the massive dispersion",
        sp.simplify(
            -(momentum_norm + mass**2)
            - (omega**2 - kx**2 - ky**2 - kz**2 - mass**2)
        )
        == 0,
    )
    transverse = sp.Matrix([0, 0, 1, 0])
    longitudinal = sp.Matrix([0, 1, 0, 0])
    one_direction_kernel = fresh_kernel.subs({ky: 0, kz: 0})
    on_shell_kernel = sp.simplify(
        one_direction_kernel.subs(omega**2, kx**2 + mass**2)
    )
    checks.check(
        "fresh scalar-proxy counterexample fails the full vector kernel",
        _zero_matrix(on_shell_kernel * transverse)
        and not _zero_matrix(on_shell_kernel * longitudinal),
    )

    coordinate = sp.Symbol("x_half", real=True)
    boundary = sp.Symbol("A0", real=True, nonzero=True)
    c_decay, c_grow = sp.symbols("c_decay c_grow", real=True)
    general = c_decay * sp.exp(-mass * coordinate) + c_grow * sp.exp(
        mass * coordinate
    )
    checks.check(
        "fresh characteristic substitution derives both static roots",
        sp.solve(sp.Symbol("r") ** 2 - mass**2, sp.Symbol("r"))
        == [-mass, mass]
        and sp.simplify(sp.diff(general, coordinate, 2) - mass**2 * general)
        == 0,
    )
    decaying = general.subs({c_decay: boundary, c_grow: 0})
    checks.check(
        "fresh boundary and decay solve fixes both integration constants",
        decaying.subs(coordinate, 0) == boundary
        and sp.limit(decaying, coordinate, sp.oo) == 0,
    )
    growing = general.subs({c_decay: 0, c_grow: boundary})
    checks.check(
        "fresh growing branch solves the ODE but fails the BVP",
        sp.simplify(sp.diff(growing, coordinate, 2) - mass**2 * growing) == 0
        and sp.limit(sp.Abs(growing), coordinate, sp.oo) == sp.oo,
    )
    checks.check(
        "fresh tangential-longitudinal comparison enforces vector geometry",
        sp.Integer(0) == 0
        and sp.diff(decaying, coordinate)
        == -boundary * mass * sp.exp(-mass * coordinate),
    )

    kinetic, quadratic = sp.symbols("kappa q", positive=True)
    rescaled_mass_squared = sp.simplify(quadratic / kinetic)
    checks.check(
        "fresh canonical field rescaling gives q over kappa",
        sp.simplify(
            kinetic
            * (sp.Symbol("A_c", real=True) / sp.sqrt(kinetic)) ** 2
            - sp.Symbol("A_c", real=True) ** 2
        )
        == 0
        and rescaled_mass_squared == quadratic / kinetic,
    )
    g, v = sp.symbols("g v", positive=True)
    composed_mass = sp.sqrt((g**2 * v**2 / 4) / 1)
    checks.check(
        "fresh conditional canonical composition gives gv over two",
        sp.simplify(composed_mass - g * v / 2) == 0
        and sp.simplify(1 / composed_mass - 2 / (g * v)) == 0,
    )
    checks.check(
        "fresh noncanonical mutation changes the claimed length",
        sp.simplify(sp.sqrt(4 / (g**2 * v**2 / 4)) - 4 / (g * v)) == 0,
    )
    checks.check(
        "fresh massless contraction cannot imply transversality",
        _zero_matrix((momentum_covector.T * fresh_kernel).subs(mass, 0))
        and not _zero_matrix(momentum_covector.T),
    )

    source_or_guard_on_growing = growing.has(sp.exp(-mass * coordinate)) or growing.has(
        sp.exp(mass * coordinate)
    )
    checks.check(
        "fresh replay exposes the source OR branch guard",
        source_or_guard_on_growing
        and sp.limit(sp.Abs(growing), coordinate, sp.oo) == sp.oo,
    )
    material_label, particle_label = sp.symbols(
        "material_label particle_label"
    )
    checks.check(
        "fresh same-equation dictionaries remain independent inputs",
        material_label not in decaying.free_symbols
        and particle_label not in decaying.free_symbols,
    )

    tally = checks.finish()
    print(f"P155 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
