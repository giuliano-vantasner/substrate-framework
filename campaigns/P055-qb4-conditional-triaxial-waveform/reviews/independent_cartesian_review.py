"""Independent Cartesian and direct-sphere review for P055."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def frobenius(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    return sp.simplify(
        sum(
            left[row, column] * right[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


def direct_tt(tensor: sp.Matrix, direction: sp.Matrix, trace_factor=sp.Rational(1, 2)) -> sp.Matrix:
    projector = sp.simplify(sp.eye(3) - direction * direction.T)
    transverse = sp.simplify(projector * tensor * projector)
    return sp.simplify(transverse - trace_factor * projector * sp.trace(transverse))


def exact_sphere_inner(left: sp.Matrix, right: sp.Matrix, trace_factor=sp.Rational(1, 2)) -> sp.Expr:
    mu, phi = sp.symbols("mu phi", real=True)
    direction = sp.Matrix(
        [
            sp.sqrt(1 - mu**2) * sp.cos(phi),
            sp.sqrt(1 - mu**2) * sp.sin(phi),
            mu,
        ]
    )
    integrand = sp.expand_trig(
        frobenius(
            direct_tt(left, direction, trace_factor),
            direct_tt(right, direction, trace_factor),
        )
    )
    value = sp.simplify(
        sp.integrate(sp.integrate(integrand, (phi, 0, 2 * sp.pi)), (mu, -1, 1))
    )
    if value.has(sp.Integral, sp.Sum, sp.Product, sp.Limit):
        raise AssertionError("independent exact sphere oracle remained unevaluated")
    return value


def main() -> int:
    ledger = CheckLedger("P055-INDEPENDENT")
    cosine_tensor = sp.diag(1, -1, 0)
    sine_tensor = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    cosine_integral = exact_sphere_inner(cosine_tensor, cosine_tensor)
    sine_integral = exact_sphere_inner(sine_tensor, sine_tensor)
    mixed_integral = exact_sphere_inner(cosine_tensor, sine_tensor)
    ledger.check(
        "direct sphere integration gives sixteen-pi-over-five for both real-m2 tensors",
        cosine_integral == sp.Rational(16, 5) * sp.pi
        and sine_integral == sp.Rational(16, 5) * sp.pi,
    )
    ledger.check(
        "direct sphere integration makes the cosine and sine real-m2 tensors orthogonal",
        mixed_integral == 0,
    )
    ledger.mutation_sensitive(
        "two-dimensional TT trace removal requires one half",
        lambda candidate: exact_sphere_inner(
            cosine_tensor, cosine_tensor, candidate
        )
        == sp.Rational(16, 5) * sp.pi,
        sp.Rational(1, 2),
        [sp.Rational(1, 3), 0],
    )

    coupling, distance, cosine3, sine3 = sp.symbols(
        "G R q_c3 q_s3", nonzero=True, real=True
    )
    wave_prefactor = 2 * coupling / 3
    flux_prefactor = 1 / (32 * sp.pi * coupling)
    direct_power = sp.simplify(
        flux_prefactor
        * wave_prefactor**2
        * (
            cosine3**2 * cosine_integral
            + sine3**2 * sine_integral
            + 2 * cosine3 * sine3 * mixed_integral
        )
    )
    ledger.check(
        "direct angular flux reduction gives two-G-over-forty-five real-m2 power",
        direct_power
        == 2 * coupling * (cosine3**2 + sine3**2) / 45,
    )
    ledger.mutation_sensitive(
        "triple convention requires the two-G-over-three waveform coefficient",
        lambda candidate: sp.simplify(
            flux_prefactor
            * candidate**2
            * cosine_integral
            - 2 * coupling / 45
        )
        == 0,
        2 * coupling / 3,
        [2 * coupling, coupling / 3],
    )

    x_axis = sp.Matrix([1, 0, 0])
    y_axis = sp.Matrix([0, 1, 0])
    z_axis = sp.Matrix([0, 0, 1])
    plus_basis = (x_axis * x_axis.T - y_axis * y_axis.T) / sp.sqrt(2)
    cross_basis = (x_axis * y_axis.T + y_axis * x_axis.T) / sp.sqrt(2)
    q_cosine2, q_sine2 = sp.symbols("q_c2 q_s2", real=True)
    second_tensor = q_cosine2 * cosine_tensor + q_sine2 * sine_tensor
    projected = direct_tt(second_tensor, z_axis)
    conventional_plus = sp.simplify(frobenius(projected, plus_basis) / sp.sqrt(2))
    conventional_cross = sp.simplify(frobenius(projected, cross_basis) / sp.sqrt(2))
    ledger.check(
        "direct natural-axis projection separates conventional real-m2 plus and cross readouts",
        conventional_plus == q_cosine2 and conventional_cross == q_sine2,
    )
    ledger.check(
        "declared scale-three waveform gives the exact natural-axis coefficients",
        sp.simplify(
            2 * coupling * conventional_plus / (3 * distance)
            - 2 * coupling * q_cosine2 / (3 * distance)
        )
        == 0
        and sp.simplify(
            2 * coupling * conventional_cross / (3 * distance)
            - 2 * coupling * q_sine2 / (3 * distance)
        )
        == 0,
    )

    # Direct generic frame: reference z projected transverse to n=(1,1,1).
    direction = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    first_raw = z_axis - direction * direction.dot(z_axis)
    first = sp.simplify(first_raw / sp.sqrt(first_raw.dot(first_raw)))
    second = sp.simplify(direction.cross(first))
    generic_plus_basis = (first * first.T - second * second.T) / sp.sqrt(2)
    generic_cross_basis = (first * second.T + second * first.T) / sp.sqrt(2)
    fixed_tensor = sp.diag(2, -1, -1)
    generic_projected = direct_tt(fixed_tensor, direction)
    fixed_plus = sp.simplify(frobenius(generic_projected, generic_plus_basis) / sp.sqrt(2))
    fixed_cross = sp.simplify(frobenius(generic_projected, generic_cross_basis) / sp.sqrt(2))
    ledger.check(
        "direct generic-frame projection gives two nonzero coordinates for one fixed tensor",
        fixed_plus != 0 and fixed_cross != 0,
    )
    sample_one, sample_two = sp.symbols("f_1 f_2", nonzero=True, real=True)
    fixed_samples = sp.Matrix(
        [[fixed_plus * sample_one, fixed_cross * sample_one],
         [fixed_plus * sample_two, fixed_cross * sample_two]]
    )
    ledger.check(
        "the fixed-tensor two-coordinate sample determinant is exactly zero",
        sp.simplify(fixed_samples.det()) == 0,
    )
    magnitude = sp.sqrt(fixed_plus**2 + fixed_cross**2)
    ledger.check(
        "a direct spin-two coordinate rotation eliminates fixed-tensor cross",
        sp.simplify(
            -(fixed_cross / magnitude) * fixed_plus
            + (fixed_plus / magnitude) * fixed_cross
        )
        == 0,
    )

    independent_samples = sp.Matrix([[1, 0], [0, 1]])
    proportional_samples = sp.Matrix([[1, -2], [2, -4]])
    ledger.mutation_sensitive(
        "two temporal traces require a nonzero coefficient determinant",
        lambda candidate: sp.simplify(candidate.det()) != 0,
        independent_samples,
        [proportional_samples, sp.zeros(2)],
    )
    phase = sp.symbols("tau", real=True)
    circular = sp.Matrix([sp.cos(phase), sp.sin(phase)])
    ledger.check(
        "direct quadrature coefficients trace a unit circle while one trace is linear",
        sp.trigsimp(circular.dot(circular)) == 1
        and sp.Matrix([sp.cos(phase), 0]).dot(
            sp.Matrix([sp.cos(phase), 0])
        )
        == sp.cos(phase) ** 2,
    )

    # Compare the independently frozen formulas with the primary public API.
    from substrate_framework.conditional_triaxial_radiation import (
        conditional_real_m2_natural_axis_waveform,
        conditional_real_m2_power,
    )

    primary_wave = conditional_real_m2_natural_axis_waveform(
        q_cosine2, q_sine2, coupling, distance
    )
    ledger.check(
        "primary waveform agrees with the independently frozen natural-axis result",
        primary_wave.conventional_plus
        == 2 * coupling * conventional_plus / (3 * distance)
        and primary_wave.conventional_cross
        == 2 * coupling * conventional_cross / (3 * distance),
    )
    ledger.check(
        "primary power agrees with the independently frozen sphere integral",
        conditional_real_m2_power(cosine3, sine3, coupling) == direct_power,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
