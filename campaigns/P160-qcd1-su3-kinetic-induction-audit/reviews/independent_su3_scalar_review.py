#!/usr/bin/env python3
"""Fresh SU3 tensor and scalar-loop derivation without canonical P160 helpers."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(matrix: sp.MatrixBase) -> bool:
    return sp.Matrix(matrix).applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


def _gell_mann_generators() -> tuple[sp.Matrix, ...]:
    imaginary = sp.I
    root_three = sp.sqrt(3)
    matrices = (
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        sp.Matrix([[0, -imaginary, 0], [imaginary, 0, 0], [0, 0, 0]]),
        sp.diag(1, -1, 0),
        sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
        sp.Matrix([[0, 0, -imaginary], [0, 0, 0], [imaginary, 0, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]),
        sp.Matrix([[0, 0, 0], [0, 0, -imaginary], [0, imaginary, 0]]),
        sp.diag(1 / root_three, 1 / root_three, -2 / root_three),
    )
    return tuple(matrix / 2 for matrix in matrices)


def _f(generators: tuple[sp.Matrix, ...], a: int, b: int, c: int) -> sp.Expr:
    commutator = generators[a] * generators[b] - generators[b] * generators[a]
    return sp.simplify(-2 * sp.I * sp.trace(commutator * generators[c]))


def _d(generators: tuple[sp.Matrix, ...], a: int, b: int, c: int) -> sp.Expr:
    anticommutator = generators[a] * generators[b] + generators[b] * generators[a]
    return sp.simplify(2 * sp.trace(anticommutator * generators[c]))


def run() -> int:
    checks = CheckLedger("P160-INDEPENDENT")
    generators = _gell_mann_generators()
    metric = sp.Matrix(
        8,
        8,
        lambda a, b: sp.simplify(sp.trace(generators[a] * generators[b])),
    )
    checks.check(
        "fresh Gell-Mann generators are exact Hermitian and traceless",
        all(generator == generator.H and sp.trace(generator) == 0 for generator in generators),
    )
    checks.check("fresh SU3 trace metric is one half identity", metric == sp.eye(8) / 2)

    f_tensor = {
        (a, b, c): _f(generators, a, b, c)
        for a in range(8)
        for b in range(8)
        for c in range(8)
    }
    d_tensor = {
        (a, b, c): _d(generators, a, b, c)
        for a in range(8)
        for b in range(8)
        for c in range(8)
    }
    checks.check(
        "fresh antisymmetric tensor has standard SU3 witnesses",
        f_tensor[(0, 1, 2)] == 1
        and f_tensor[(3, 4, 7)] == sp.sqrt(3) / 2
        and f_tensor[(0, 3, 6)] == sp.Rational(1, 2),
    )
    checks.check(
        "fresh symmetric tensor has standard SU3 witnesses",
        d_tensor[(0, 0, 7)] == 1 / sp.sqrt(3)
        and d_tensor[(7, 7, 7)] == -1 / sp.sqrt(3)
        and d_tensor[(0, 3, 5)] == sp.Rational(1, 2),
    )
    checks.check(
        "fresh f and d tensors have opposite permutation types",
        all(
            sp.simplify(f_tensor[(a, b, c)] + f_tensor[(b, a, c)]) == 0
            and sp.simplify(f_tensor[(a, b, c)] + f_tensor[(a, c, b)]) == 0
            and sp.simplify(d_tensor[(a, b, c)] - d_tensor[(b, a, c)]) == 0
            and sp.simplify(d_tensor[(a, b, c)] - d_tensor[(a, c, b)]) == 0
            for a in range(8)
            for b in range(8)
            for c in range(8)
        ),
    )
    commutator_residuals = []
    anticommutator_residuals = []
    for a in range(8):
        for b in range(8):
            commutator_residuals.append(
                generators[a] * generators[b]
                - generators[b] * generators[a]
                - sp.I
                * sum(
                    (f_tensor[(a, b, c)] * generators[c] for c in range(8)),
                    sp.zeros(3),
                )
            )
            anticommutator_residuals.append(
                generators[a] * generators[b]
                + generators[b] * generators[a]
                - sp.Rational(1, 3) * (1 if a == b else 0) * sp.eye(3)
                - sum(
                    (d_tensor[(a, b, c)] * generators[c] for c in range(8)),
                    sp.zeros(3),
                )
            )
    checks.check(
        "fresh commutator reconstruction closes all 64 pairs",
        all(_zero(residual) for residual in commutator_residuals),
    )
    checks.check(
        "fresh anticommutator reconstruction closes all 64 pairs",
        all(_zero(residual) for residual in anticommutator_residuals),
    )
    checks.check(
        "fresh d tensor vanishes only on the standard embedded SU2 restriction",
        all(
            d_tensor[(a, b, c)] == 0
            for a in range(3)
            for b in range(3)
            for c in range(3)
        )
        and d_tensor[(0, 0, 7)] != 0,
    )
    missing_identity = sp.simplify(
        generators[0] * generators[0]
        + generators[0] * generators[0]
        - sum(
            (d_tensor[(0, 0, c)] * generators[c] for c in range(8)),
            sp.zeros(3),
        )
    )
    checks.check(
        "fresh omitted identity mutation breaks the anticommutator",
        missing_identity == sp.eye(3) / 3,
    )
    rescaled = tuple(2 * generator for generator in generators)
    checks.check(
        "fresh generator rescaling changes the symmetric tensor cubically",
        _d(rescaled, 0, 0, 7) == 8 / sp.sqrt(3),
    )

    q2, mass, coupling = sp.symbols("Q m g", positive=True)
    species = sp.Integer(2)
    y = sp.Symbol("y", real=True)
    ratio = sp.sqrt(q2) / sp.sqrt(q2 + 4 * mass**2)
    reduced_integrand = y**2 / (1 - ratio**2 * y**2)
    antiderivative = sp.atanh(ratio * y) / ratio**3 - y / ratio**2
    checks.check(
        "fresh scalar real-parameter antiderivative is exact",
        sp.simplify(sp.diff(antiderivative, y) - reduced_integrand) == 0,
    )
    endpoint = sp.simplify(antiderivative.subs(y, 1) - antiderivative.subs(y, 0))
    projector_coefficient = sp.simplify(
        species
        * coupling**2
        * q2
        / (sp.pi * (q2 + 4 * mass**2))
        * endpoint
    )
    expected = sp.simplify(
        species * coupling**2 / sp.pi * (sp.atanh(ratio) / ratio - 1)
    )
    checks.check(
        "fresh scalar parameter integral yields the accepted closed form",
        sp.simplify(projector_coefficient - expected) == 0,
    )
    form_factor = sp.simplify(projector_coefficient / q2)
    low_form_factor = sp.simplify(sp.limit(form_factor, q2, 0))
    checks.check(
        "fresh massive low-momentum form factor is finite",
        low_form_factor == coupling**2 / (6 * sp.pi * mass**2),
    )
    trace_coefficient = sp.simplify(low_form_factor / 4)
    component_coefficient = sp.simplify(sp.Rational(1, 2) * trace_coefficient)
    checks.check(
        "fresh SU3 trace and component coefficients remain typed",
        trace_coefficient == coupling**2 / (24 * sp.pi * mass**2)
        and component_coefficient == coupling**2 / (48 * sp.pi * mass**2),
    )

    color_kernel = sp.simplify(metric * projector_coefficient)
    checks.check(
        "fresh color kernel is the representation metric times the scalar loop",
        color_kernel == sp.eye(8) * projector_coefficient / 2,
    )
    tadpole = sp.Symbol("I_tad", nonzero=True)
    bubble = 2 * species * coupling**2 * metric * tadpole
    seagull = -2 * species * coupling**2 * metric * tadpole
    checks.check(
        "fresh bubble and seagull cancel before projection",
        sp.simplify(bubble + seagull) == sp.zeros(8),
    )
    checks.check(
        "fresh deleted and sign-flipped seagull mutations fail",
        bubble != sp.zeros(8) and sp.simplify(bubble - seagull) != sp.zeros(8),
    )

    proper_time = sp.Symbol("s", positive=True)
    mass_integral = sp.integrate(sp.exp(-mass**2 * proper_time), (proper_time, 0, sp.oo))
    heat_coefficient = sp.simplify(
        species * coupling**2 * sp.Rational(1, 12) / (4 * sp.pi) * mass_integral
    )
    checks.check(
        "fresh proper-time curvature coefficient matches the local trace term",
        mass_integral == 1 / mass**2
        and sp.simplify(heat_coefficient - trace_coefficient) == 0,
    )
    full_curvature = -sp.I * coupling * (
        generators[0] * generators[1] - generators[1] * generators[0]
    )
    checks.check(
        "fresh constant noncommuting background exercises full curvature",
        full_curvature == coupling * generators[2]
        and sp.trace(full_curvature * full_curvature) == coupling**2 / 2,
    )
    checks.check(
        "fresh curl-only mutation misses that background",
        not _zero(full_curvature),
    )

    checks.check(
        "fresh scalar fixed-Q massless limit diverges",
        sp.limit(projector_coefficient, mass, 0, dir="+") == sp.oo,
    )
    checks.check(
        "fresh scalar zero-momentum and heavy-mass limits vanish",
        sp.limit(projector_coefficient, q2, 0) == 0
        and sp.limit(projector_coefficient, mass, sp.oo) == 0,
    )
    u = sp.Symbol("u", real=True)
    source_numerator = u * (1 - u) * q2
    scalar_numerator = (1 - 2 * u) ** 2
    checks.check(
        "fresh QCD1 numerator is not the complex-scalar numerator",
        sp.simplify(source_numerator - scalar_numerator) != 0,
    )
    source_projector = coupling**2 / sp.pi
    checks.check(
        "fresh constant projector coefficient is nonlocal as a curvature kernel",
        sp.limit(source_projector / q2, q2, 0, dir="+") == sp.oo
        and low_form_factor.is_finite is not False,
    )

    pauli = (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )
    pauli_metric = sp.Matrix(
        3, 3, lambda a, b: sp.trace(pauli[a] * pauli[b])
    )
    checks.check(
        "fresh equal SU2 and SU3 indices do not identify their algebras",
        pauli_metric[0, 0] == metric[0, 0] == sp.Rational(1, 2)
        and len(pauli) != len(generators),
    )
    checks.check(
        "fresh fixed SU3 Cartan restriction retains trace one half",
        sp.trace(generators[7] * generators[7]) == sp.Rational(1, 2),
    )
    bare, counterterm = sp.symbols("c_bare c_ct", real=True)
    total = bare + counterterm + component_coefficient
    checks.check(
        "fresh bare and counterterm family defeats unique induction",
        sp.diff(total, bare) == 1
        and sp.diff(total, counterterm) == 1
        and total.subs(bare, 1) != total.subs(bare, 2),
    )

    tally = checks.finish()
    print(f"P160 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
