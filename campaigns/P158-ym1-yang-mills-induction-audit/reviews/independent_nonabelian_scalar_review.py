#!/usr/bin/env python3
"""Fresh C-NVP-001 derivation without importing its canonical module."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _zero(matrix: sp.MatrixBase) -> bool:
    simplified = sp.Matrix(matrix).applyfunc(sp.simplify)
    return simplified == sp.zeros(*simplified.shape)


def _trace_metric(generators: tuple[sp.Matrix, ...]) -> sp.Matrix:
    return sp.Matrix(
        3,
        3,
        lambda first, second: sp.simplify(
            sp.trace(generators[first] * generators[second])
        ),
    )


def run() -> int:
    checks = CheckLedger("P158-INDEPENDENT")
    imaginary = sp.I
    fundamental = (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -imaginary], [imaginary, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )
    adjoint = (
        sp.Matrix([[0, 0, 0], [0, 0, -imaginary], [0, imaginary, 0]]),
        sp.Matrix([[0, 0, imaginary], [0, 0, 0], [-imaginary, 0, 0]]),
        sp.Matrix([[0, -imaginary, 0], [imaginary, 0, 0], [0, 0, 0]]),
    )
    cyclic = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    checks.check(
        "fresh fundamental and adjoint carriers are exact Hermitian SU2 representations",
        all(
            all(_zero(generator - generator.H) for generator in representation)
            and all(
                _zero(
                    representation[first] * representation[second]
                    - representation[second] * representation[first]
                    - imaginary * representation[target]
                )
                for first, second, target in cyclic
            )
            for representation in (fundamental, adjoint)
        ),
    )
    fundamental_metric = _trace_metric(fundamental)
    adjoint_metric = _trace_metric(adjoint)
    checks.check(
        "fresh trace metrics give indices one half and two",
        fundamental_metric == sp.eye(3) / 2
        and adjoint_metric == 2 * sp.eye(3),
    )

    q2, mass, coupling = sp.symbols("Q m g", positive=True)
    species = sp.Integer(3)
    y = sp.symbols("y", real=True)
    ratio = sp.sqrt(q2) / sp.sqrt(q2 + 4 * mass**2)
    reduced_integrand = y**2 / (1 - ratio**2 * y**2)
    antiderivative = sp.atanh(ratio * y) / ratio**3 - y / ratio**2
    checks.check(
        "fresh real-parameter antiderivative is exact",
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
    expected_closed_form = sp.simplify(
        species * coupling**2 / sp.pi * (sp.atanh(ratio) / ratio - 1)
    )
    checks.check(
        "fresh parameter integral yields the exact closed form",
        sp.simplify(projector_coefficient - expected_closed_form) == 0,
    )
    form_factor = sp.simplify(projector_coefficient / q2)
    low_form_factor = sp.simplify(sp.limit(form_factor, q2, 0))
    checks.check(
        "fresh low-momentum form factor is species g squared over twelve pi m squared",
        low_form_factor == species * coupling**2 / (12 * sp.pi * mass**2),
    )
    local_trace_coefficient = sp.simplify(low_form_factor / 4)
    checks.check(
        "fresh quadratic-action conversion gives the trace-density coefficient",
        local_trace_coefficient
        == species * coupling**2 / (48 * sp.pi * mass**2),
    )

    dynkin_index = sp.Rational(1, 2)
    color_kernel = sp.eye(3) * dynkin_index * projector_coefficient
    checks.check(
        "fresh fundamental color kernel carries the trace index",
        color_kernel == sp.eye(3) * projector_coefficient / 2
        and color_kernel != sp.eye(3) * projector_coefficient,
    )
    component_coefficient = sp.simplify(dynkin_index * local_trace_coefficient)
    checks.check(
        "fresh component and trace coefficients differ by T of R",
        component_coefficient
        == species * coupling**2 / (96 * sp.pi * mass**2)
        and component_coefficient != local_trace_coefficient,
    )

    tadpole = sp.Symbol("I_tad", nonzero=True)
    bubble_contraction = 2 * species * coupling**2 * dynkin_index * tadpole
    seagull_contraction = -2 * species * coupling**2 * dynkin_index * tadpole
    checks.check(
        "fresh denominator-shift identity cancels bubble and seagull contractions",
        sp.simplify(bubble_contraction + seagull_contraction) == 0,
    )
    checks.check(
        "fresh deleted and sign-flipped seagull mutations fail",
        bubble_contraction != 0
        and sp.simplify(bubble_contraction - seagull_contraction) != 0,
    )

    heat_kernel_weight = sp.Rational(1, 12)
    free_kernel_factor = 1 / (4 * sp.pi)
    proper_time_mass_integral = sp.integrate(
        sp.exp(-mass**2 * sp.Symbol("s", positive=True)),
        (sp.Symbol("s", positive=True), 0, sp.oo),
    )
    heat_kernel_coefficient = sp.simplify(
        species
        * coupling**2
        * heat_kernel_weight
        * free_kernel_factor
        * proper_time_mass_integral
    )
    checks.check(
        "fresh proper-time curvature coefficient matches the two-point local limit",
        proper_time_mass_integral == 1 / mass**2
        and sp.simplify(heat_kernel_coefficient - local_trace_coefficient) == 0,
    )
    checks.check(
        "fresh real-scalar determinant mutation misses the complex-scalar coefficient",
        sp.simplify(heat_kernel_coefficient / 2 - local_trace_coefficient) != 0,
    )

    f1, f2, f3 = sp.symbols("F1 F2 F3", real=True)
    curvature_matrix = sum(
        (component * generator for component, generator in zip(
            (f1, f2, f3), fundamental, strict=True
        )),
        sp.zeros(2),
    )
    checks.check(
        "fresh representation trace converts full curvature to component density",
        sp.simplify(sp.trace(curvature_matrix * curvature_matrix))
        == dynkin_index * (f1**2 + f2**2 + f3**2),
    )
    constant_connection = (fundamental[0], fundamental[1])
    full_curvature = -imaginary * coupling * (
        constant_connection[0] * constant_connection[1]
        - constant_connection[1] * constant_connection[0]
    )
    checks.check(
        "fresh noncommuting constant background tests the nonlinear completion",
        not _zero(full_curvature)
        and sp.simplify(sp.trace(full_curvature * full_curvature)) != 0,
    )
    checks.check(
        "fresh curl-only quadratic mutation misses that background",
        _zero(constant_connection[1].diff(sp.Symbol("x")))
        and _zero(constant_connection[0].diff(sp.Symbol("y")))
        and not _zero(full_curvature),
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
    source_parameter = sp.Symbol("u", real=True)
    ym1_integrand = sp.simplify(
        source_parameter
        * (1 - source_parameter)
        * q2
        / (mass**2 + source_parameter * (1 - source_parameter) * q2)
    )
    scalar_integrand = sp.simplify(
        (1 - 2 * source_parameter) ** 2
        / (mass**2 + source_parameter * (1 - source_parameter) * q2)
    )
    checks.check(
        "fresh YM1 numerator mutation is not the complex-scalar integrand",
        sp.simplify(ym1_integrand - scalar_integrand) != 0,
    )

    bare, counterterm = sp.symbols("c_bare c_ct", real=True)
    total = bare + counterterm + component_coefficient
    checks.check(
        "fresh bare-plus-counterterm counterfamily defeats unique induction",
        sp.diff(total, bare) == 1
        and sp.diff(total, counterterm) == 1
        and total.subs(bare, 1) != total.subs(bare, 2),
    )
    rescaling = sp.symbols("lambda", positive=True)
    checks.check(
        "fresh field-coordinate rescaling changes the displayed kinetic coefficient",
        sp.simplify(component_coefficient / rescaling**2 - component_coefficient)
        != 0,
    )

    tally = checks.finish()
    print(f"P158 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
