#!/usr/bin/env python3
"""Primary exact verifier for C-IGR-001 through C-IGR-003."""

from __future__ import annotations

import inspect

import sympy as sp

from substrate_framework import scalar_one_loop_mass as implementation
from substrate_framework.scalar_one_loop_mass import (
    SMOOTH_PROPER_TIME_REGULATOR,
    ZETA_POWER_SUBTRACTED_REGULATOR,
    curvature_proper_time_integral,
    exact_mass_inverse_newton_shift,
    exact_mass_vacuum_density_shift,
    regulator_scheme_ledger,
    vacuum_proper_time_integral,
)
from substrate_framework.scalar_induced_newton import SHARP_PROPER_TIME_REGULATOR
from substrate_framework.verification import CheckLedger


def run() -> int:
    checks = CheckLedger("P230/C-IGR")
    cutoff, scale, mass2 = sp.symbols("Lambda mu m2", positive=True)
    tau0, z = sp.symbols("tau0 z", positive=True)

    sharp2 = curvature_proper_time_integral(
        SHARP_PROPER_TIME_REGULATOR,
        cutoff=cutoff,
        mass_squared=mass2,
    )
    sharp2_expected = cutoff**2 * (
        sp.exp(-mass2 / cutoff**2)
        - mass2 * sp.expint(1, mass2 / cutoff**2) / cutoff**2
    )
    checks.check(
        "C-IGR-001 sharp I2 closed form",
        sp.simplify(sharp2 - sharp2_expected) == 0,
    )
    sharp_tail = (
        sp.exp(-mass2 * tau0)
        - mass2 * tau0 * sp.expint(1, mass2 * tau0)
    ) / tau0
    checks.check(
        "C-IGR-001 sharp tail derivative fixes the integral",
        sp.simplify(
            sp.diff(sharp_tail, tau0)
            + tau0**-2 * sp.exp(-mass2 * tau0)
        )
        == 0,
    )
    u = sp.Symbol("u", nonnegative=True)
    checks.check(
        "C-IGR-001 large-mass tail is squeezed to zero",
        sp.factor(1 - 1 / (1 + u) ** 2).is_nonnegative is True
        and sp.limit(sp.exp(-z) / z, z, sp.oo) == 0,
    )

    sharp3 = vacuum_proper_time_integral(
        SHARP_PROPER_TIME_REGULATOR,
        cutoff=cutoff,
        mass_squared=mass2,
    )
    checks.check(
        "C-IGR-001 sharp I3 integration-by-parts form",
        sp.simplify(
            sharp3
            - sp.exp(-mass2 / cutoff**2) * cutoff**4 / 2
            + mass2 * sharp2 / 2
        )
        == 0,
    )

    smooth2 = curvature_proper_time_integral(
        SMOOTH_PROPER_TIME_REGULATOR,
        cutoff=cutoff,
        mass_squared=mass2,
    )
    smooth3 = vacuum_proper_time_integral(
        SMOOTH_PROPER_TIME_REGULATOR,
        cutoff=cutoff,
        mass_squared=mass2,
    )
    dimensionless2 = 2 * sp.sqrt(z) * sp.besselk(1, 2 * sp.sqrt(z))
    dimensionless3 = 2 * z * sp.besselk(2, 2 * sp.sqrt(z))
    checks.check(
        "C-IGR-002 smooth Bessel closed forms",
        sp.simplify(smooth2 - cutoff**2 * dimensionless2.subs(z, mass2 / cutoff**2))
        == 0
        and sp.simplify(
            smooth3 - cutoff**4 * dimensionless3.subs(z, mass2 / cutoff**2)
        )
        == 0,
    )
    checks.check(
        "C-IGR-002 smooth recurrence and massless boundaries",
        sp.simplify(
            sp.diff(dimensionless3, z) + dimensionless2
        )
        == 0
        and sp.limit(dimensionless2, z, 0, "+") == 1
        and sp.limit(dimensionless3, z, 0, "+") == 1,
    )
    checks.check(
        "C-IGR-002 smooth large-mass limits",
        sp.limit(dimensionless2, z, sp.oo) == 0
        and sp.limit(dimensionless3, z, sp.oo) == 0,
    )

    zeta2 = curvature_proper_time_integral(
        ZETA_POWER_SUBTRACTED_REGULATOR,
        mass_squared=mass2,
        renormalization_scale=scale,
    )
    zeta3 = vacuum_proper_time_integral(
        ZETA_POWER_SUBTRACTED_REGULATOR,
        mass_squared=mass2,
        renormalization_scale=scale,
    )
    checks.check(
        "C-IGR-003 declared power-subtracted finite parts",
        sp.simplify(
            zeta2
            - mass2
            * (sp.log(mass2 / scale**2) + sp.EulerGamma - 1)
        )
        == 0
        and sp.simplify(
            zeta3
            + mass2**2
            * (
                sp.log(mass2 / scale**2)
                + sp.EulerGamma
                - sp.Rational(3, 2)
            )
            / 2
        )
        == 0,
    )
    checks.check(
        "C-IGR-003 scale derivatives remain explicit",
        sp.simplify(scale * sp.diff(zeta2, scale) + 2 * mass2) == 0
        and sp.simplify(scale * sp.diff(zeta3, scale) - mass2**2) == 0,
    )

    for regulator, kwargs in (
        (
            SHARP_PROPER_TIME_REGULATOR,
            {"cutoff": cutoff, "mass_squared": mass2},
        ),
        (
            SMOOTH_PROPER_TIME_REGULATOR,
            {"cutoff": cutoff, "mass_squared": mass2},
        ),
        (
            ZETA_POWER_SUBTRACTED_REGULATOR,
            {"mass_squared": mass2, "renormalization_scale": scale},
        ),
    ):
        i2 = curvature_proper_time_integral(regulator, **kwargs)
        i3 = vacuum_proper_time_integral(regulator, **kwargs)
        checks.check(
            f"{regulator} exact dI3/dm2 bridge",
            sp.simplify(sp.diff(i3, mass2) + i2) == 0,
        )

    field_count, xi = sp.Integer(3), sp.Rational(1, 12)
    shift = exact_mass_inverse_newton_shift(
        field_count,
        xi,
        regulator=SHARP_PROPER_TIME_REGULATOR,
        cutoff=cutoff,
        mass_squared=0,
    )
    independent_coefficient = sp.simplify(
        field_count
        * (16 * sp.pi)
        * sp.Rational(1, 2)
        * (4 * sp.pi) ** -2
        * (sp.Rational(1, 6) - xi)
    )
    checks.check(
        "conditional inverse-Newton factor is independently typed",
        sp.simplify(shift.value - independent_coefficient * cutoff**2) == 0,
    )

    vacuum = exact_mass_vacuum_density_shift(
        2,
        regulator=SHARP_PROPER_TIME_REGULATOR,
        cutoff=cutoff,
        mass_squared=mass2,
    )
    expected_vacuum = -sp.Rational(2, 2) * (4 * sp.pi) ** -2 * sharp3
    checks.check(
        "mass-resummed vacuum composition uses I3 once",
        sp.simplify(vacuum.value - expected_vacuum) == 0,
    )
    spurious = -sp.Rational(2, 2) * (4 * sp.pi) ** -2 * mass2 * sharp2
    checks.mutation_sensitive(
        "vacuum mass double count is rejected",
        lambda candidate: sp.simplify(candidate - expected_vacuum) == 0,
        vacuum.value,
        (vacuum.value + spurious,),
    )

    wrong_sharp = 2 * sharp_tail
    checks.mutation_sensitive(
        "sharp prefactor is load-bearing",
        lambda candidate: sp.simplify(
            sp.diff(candidate, tau0) + tau0**-2 * sp.exp(-mass2 * tau0)
        )
        == 0,
        sharp_tail,
        (wrong_sharp,),
    )
    wrong_order = 2 * sp.sqrt(z) * sp.besselk(2, 2 * sp.sqrt(z))
    smooth1 = 2 * sp.besselk(0, 2 * sp.sqrt(z))
    checks.mutation_sensitive(
        "smooth Bessel order is load-bearing",
        lambda candidate: sp.simplify(sp.diff(candidate, z) + smooth1) == 0,
        dimensionless2,
        (wrong_order,),
    )

    negative_zeta = exact_mass_inverse_newton_shift(
        1,
        0,
        regulator=ZETA_POWER_SUBTRACTED_REGULATOR,
        mass_squared=1,
        renormalization_scale=1,
    )
    checks.check(
        "zeta full-value sign is not inferred from curvature weight",
        negative_zeta.curvature_weight_sign == 1
        and negative_zeta.value_sign == -1,
    )
    ledger = regulator_scheme_ledger(1, 0, 1)
    checks.check(
        "massless scheme spread is exact and regulator selection stays open",
        ledger.sharp_value == 1
        and ledger.smooth_value == 1
        and ledger.zeta_value == 0
        and vacuum_proper_time_integral(
            SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0
        )
        == sp.Rational(1, 2)
        and vacuum_proper_time_integral(
            SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0
        )
        == 1,
    )

    source = inspect.getsource(implementation)
    signature = inspect.signature(curvature_proper_time_integral)
    checks.check(
        "constant-mass scope and implementation independence are explicit",
        "spacetime-constant nonnegative" in source
        and "varying effective mass" in source
        and "leading_scalar_newton_shift_coefficient" not in source
        and "background" not in signature.parameters,
    )
    checks.check(
        "no empirical comparator or legacy trapezoid access enters",
        all(token not in source for token in ("6.674", "M_pl", "np.trapz", 'getattr(np, "trapz")')),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(run())
