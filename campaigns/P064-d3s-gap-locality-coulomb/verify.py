"""Primary exact verifier for P064 momentum-kernel claims and D3S audit."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.momentum_kernels import (
    leading_power_ledger,
    massive_parameter_kernel,
    riesz_green_kernel,
    spectral_moment_expansion,
)
from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-19/"
    "bridge_D3S_coulomb_from_sg.py"
)
SOURCE_SHA256 = "a5ff9c760cf8776115881d7a2e5e86c562cdf461f61f36784ff95c6381d24d71"


def _zero(expression: object) -> bool:
    return sp.simplify(sp.sympify(expression)) == 0


def main() -> int:
    ledger = CheckLedger("P064")
    ledger.check("hash-pinned D3S source exists", SOURCE.is_file())
    ledger.check(
        "hash-pinned D3S source integrity",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    ledger.check(
        "D3S inserts a bare local inverse kernel before selecting its power",
        "inv_prop = sp.expand(q2 -" in source_text
        and "leading_power = sp.Integer(2)" in source_text,
    )
    ledger.check(
        "D3S declares rather than derives the dimensional lift",
        "DECLARED      -- the polarization argument is 1+1D" in source_text
        and "d=3 is QCD5's, not derived here" in source_text,
    )
    ledger.check(
        "D3S numerical slope regresses an exactly constructed power",
        "G_num = r ** (2 * 1.0 - 3.0)" in source_text
        and "np.polyfit" in source_text,
    )

    q2 = sp.Symbol("Q2", positive=True)
    m2, coefficient = sp.symbols("m2 C", positive=True)
    massive = massive_parameter_kernel(q2, m2, coefficient)
    ledger.check(
        "declared massive kernel has the exact first two coefficients",
        massive.first_coefficient == coefficient / (6 * m2)
        and massive.second_coefficient == -coefficient / (30 * m2**2),
    )
    direct_coefficients = tuple(
        sp.integrate(
            coefficient
            * (-1) ** (order - 1)
            * (massive.parameter * (1 - massive.parameter)) ** order
            / m2**order,
            (massive.parameter, 0, 1),
        )
        for order in range(1, 7)
    )
    ledger.check(
        "beta formula derives six coefficients without copied targets",
        all(
            _zero(massive.coefficient(order) - direct_coefficients[order - 1])
            for order in range(1, 7)
        ),
    )
    continuation_variable = sp.Symbol("z")
    ledger.check(
        "nearest parameter singularity fixes the convergence radius",
        massive.convergence_radius == 4 * m2
        and sp.solve(
            sp.Eq(m2 + continuation_variable * sp.Rational(1, 4), 0),
            continuation_variable,
        )
        == [-4 * m2],
    )
    for truncation in (0, 1, 2, 5):
        pointwise_polynomial = sum(
            (
                coefficient
                * (-1) ** (order - 1)
                * (
                    massive.parameter
                    * (1 - massive.parameter)
                    * q2
                    / m2
                )
                ** order
                for order in range(1, truncation + 1)
            ),
            sp.S.Zero,
        )
        ledger.check(
            f"geometric remainder identity closes at order {truncation}",
            _zero(
                massive.integrand
                - pointwise_polynomial
                - massive.pointwise_remainder_integrand(truncation)
            ),
        )
    ledger.check(
        "massless and zero-transfer limits do not commute",
        massive.zero_transfer_limit == 0
        and massive.massless_at_fixed_positive_transfer == coefficient
        and sp.limit(
            sp.limit(massive.closed_form, q2, 0, dir="+"),
            m2,
            0,
            dir="+",
        )
        == 0
        and sp.limit(
            sp.limit(massive.closed_form, m2, 0, dir="+"),
            q2,
            0,
            dir="+",
        )
        == coefficient,
    )
    u = massive.parameter
    mutated_first = sp.integrate((u * (1 - u)) ** 2 / m2, (u, 0, 1))
    ledger.mutation_sensitive(
        "first coefficient binds the declared numerator",
        lambda value: _zero(value - 1 / (6 * m2)),
        massive.first_coefficient / coefficient,
        [mutated_first, -massive.first_coefficient / coefficient],
    )

    t = sp.Symbol("t", positive=True)
    gap = sp.Symbol("Delta", positive=True)
    density = sp.Function("rho")(t)
    spectral = spectral_moment_expansion(q2, t, density, gap, 4)
    ledger.check(
        "spectral inverse-moment expansion has an exact pointwise remainder",
        spectral.pointwise_identity_residual == 0
        and len(spectral.inverse_moments) == 4,
    )
    divergent = spectral_moment_expansion(q2, t, t, 1, 1)
    zero_density = spectral_moment_expansion(q2, t, 0, 1, 2)
    ledger.check(
        "a gap alone supplies neither ultraviolet convergence nor nonzero moment",
        divergent.inverse_moments[0].doit() == sp.oo
        and all(moment.doit() == 0 for moment in zero_density.inverse_moments),
    )
    positive_density = 1 / t
    positive_spectral = spectral_moment_expansion(q2, t, positive_density, 1, 2)
    ledger.check(
        "positive integrable declared density supplies a positive first moment",
        positive_spectral.inverse_moments[0].doit() == 1,
    )

    k2 = sp.Symbol("k2", positive=True)
    z_unknown = sp.Symbol("Z", real=True)
    refused_unknown = False
    try:
        leading_power_ledger(k2, [(1, z_unknown), (2, 1)])
    except ValueError:
        refused_unknown = True
    ledger.check(
        "leading-power oracle refuses an undecidable symbolic coefficient",
        refused_unknown,
    )
    z_nonzero = sp.Symbol("Z_nz", real=True, nonzero=True)
    generic = leading_power_ledger(k2, [(1, z_nonzero), (2, 1)])
    ledger.check(
        "nonzero local coefficient conditionally gives s one",
        generic.leading_exponent == 1
        and generic.propagator_momentum_exponent == 2,
    )
    e2 = sp.Symbol("e2", positive=True)
    source_z = 1 - e2 / (6 * sp.pi * m2)
    source_q4 = e2 / (30 * sp.pi * m2**2)
    tuned = leading_power_ledger(
        k2,
        [
            (1, source_z.subs(e2, 6 * sp.pi * m2)),
            (2, source_q4.subs(e2, 6 * sp.pi * m2)),
        ],
    )
    ledger.check(
        "D3S allowed exact cancellation changes the leading exponent",
        tuned.leading_exponent == 2
        and tuned.leading_coefficient == 1 / (5 * m2)
        and tuned.propagator_momentum_exponent == 4,
    )
    fractional_amplitude = sp.Symbol("A", positive=True)
    fractional = leading_power_ledger(
        k2,
        [(sp.Rational(1, 2), fractional_amplitude), (1, -2), (2, 3)],
    )
    ledger.check(
        "declared lower fractional bare term survives analytic corrections",
        fractional.leading_exponent == sp.Rational(1, 2)
        and fractional.propagator_momentum_exponent == 1,
    )
    ledger.mutation_sensitive(
        "leading verdict binds coefficient cancellation and fractional premise",
        lambda terms: leading_power_ledger(k2, terms).leading_exponent == 1,
        [(1, 2), (2, 1)],
        [
            [(1, 2), (1, -2), (2, 1)],
            [(sp.Rational(1, 2), 1), (1, 2)],
        ],
    )

    radius = sp.Symbol("r", positive=True)
    dimension, power = sp.symbols("d s", positive=True)
    general_riesz = riesz_green_kernel(dimension, power, radius)
    ledger.check(
        "general Riesz kernel retains dimension power and Fourier normalization",
        general_riesz.fourier_convention == "inverse_angular"
        and general_riesz.normalization
        == sp.gamma(dimension / 2 - power)
        / (4**power * sp.pi ** (dimension / 2) * sp.gamma(power))
        and general_riesz.radial_power == 2 * power - dimension,
    )
    coulomb_specialization = riesz_green_kernel(3, 1, radius)
    ledger.check(
        "three-dimensional s-one specialization is exact but conditional",
        coulomb_specialization.green_kernel == 1 / (4 * sp.pi * radius)
        and coulomb_specialization.radial_derivative
        == -1 / (4 * sp.pi * radius**2),
    )
    ledger.mutation_sensitive(
        "Riesz endpoint binds dimension power and inverse coefficient",
        lambda args: _zero(
            riesz_green_kernel(args[0], args[1], radius, args[2]).green_kernel
            - 1 / (4 * sp.pi * radius)
        ),
        (3, 1, 1),
        [
            (4, 1, 1),
            (3, sp.Rational(1, 2), 1),
            (3, 1, 2),
        ],
    )
    invalid_domain_refused = False
    try:
        riesz_green_kernel(2, 1, radius)
    except ValueError:
        invalid_domain_refused = True
    ledger.check(
        "Riesz endpoint refuses the logarithmic boundary without prescription",
        invalid_domain_refused,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
