#!/usr/bin/env python3
"""Primary exact verifier for the P231 total-coupling rung (C-IGR-004, C-GRV-002 candidates)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import sympy as sp

from substrate_framework import total_gravitational_coupling as implementation
from substrate_framework.total_gravitational_coupling import baseline_provenance
from substrate_framework.scalar_induced_newton import SHARP_PROPER_TIME_REGULATOR
from substrate_framework.scalar_one_loop_mass import (
    SMOOTH_PROPER_TIME_REGULATOR,
    ZETA_POWER_SUBTRACTED_REGULATOR,
    curvature_proper_time_integral,
    exact_mass_inverse_newton_shift,
)
from substrate_framework.verification import CheckLedger

ROOT = Path(__file__).resolve().parents[2]


def run() -> int:
    checks = CheckLedger("P231/total-coupling")
    z, t = sp.symbols("z t", positive=True)
    lam, m2 = sp.symbols("Lambda m2", positive=True)
    m2n = sp.symbols("m2n", nonnegative=True)
    gam = sp.EulerGamma
    J_sharp = sp.exp(-z) - z * sp.expint(1, z)
    J_smooth = 2 * sp.sqrt(z) * sp.besselk(1, 2 * sp.sqrt(z))
    J_zeta = z * (sp.log(z) + gam - 1)

    checks.check(
        "L1 sharp J is the positive tail integral of a positive integrand",
        sp.simplify(sp.diff(J_sharp, z) + sp.expint(1, z)) == 0
        and sp.limit(J_sharp, z, 0, "+") == 1
        and sp.integrate(t**-2, (t, 1, sp.oo)) == 1,
    )
    checks.check(
        "L1/L2 smooth J has exact Bessel recurrence and unit endpoint",
        sp.simplify(sp.diff(J_smooth, z) + 2 * sp.besselk(0, 2 * sp.sqrt(z))) == 0
        and sp.limit(J_smooth, z, 0, "+") == 1,
    )
    squeeze_grid = [sp.Rational(1, 100), sp.Rational(1, 10), sp.Rational(1, 2), sp.Integer(1), sp.Integer(2), sp.Integer(10)]
    checks.check(
        "L1+L2 squeeze 0 < J(z) <= 1 on grid for both usable schemes",
        all(
            0 < factor.subs(z, q).evalf(30) <= 1
            for q in squeeze_grid
            for factor in (J_sharp, J_smooth)
        ),
    )
    root = sp.exp(1 - gam)
    checks.check(
        "L1 zeta J changes sign at the exact root exp(1-EulerGamma)",
        sp.simplify(J_zeta.subs(z, root)) == 0
        and J_zeta.subs(z, sp.Integer(1)).evalf(20) < 0
        and J_zeta.subs(z, sp.Integer(2)).evalf(20) > 0,
    )
    checks.check(
        "L2 zeta derivative changes sign at exp(-EulerGamma)",
        sp.diff(J_zeta, z).subs(z, sp.exp(-gam)).evalf(20) == 0
        and sp.diff(J_zeta, z).subs(z, sp.exp(-gam) * sp.Rational(1, 2)).evalf(20) < 0
        and sp.diff(J_zeta, z).subs(z, sp.exp(-gam) * sp.Integer(2)).evalf(20) > 0,
    )
    ledger = implementation.scheme_selection_ledger(cutoff=sp.Integer(1), mass_squared=sp.Integer(1))
    checks.check(
        "selection ledger outputs {sharp, smooth} usable and zeta excluded",
        ledger.usable_schemes == (SHARP_PROPER_TIME_REGULATOR, SMOOTH_PROPER_TIME_REGULATOR)
        and ledger.excluded_schemes == (ZETA_POWER_SUBTRACTED_REGULATOR,)
        and len(ledger.entries[-1].exclusion_reasons) == 3,
    )
    checks.check(
        "scale factors match accepted C-IGR-001..003 families exactly",
        all(
            sp.simplify(
                implementation.curvature_scale_factor(reg, cutoff=lam, mass_squared=m2n)
                - sp.simplify(
                    curvature_proper_time_integral(reg, cutoff=lam, mass_squared=m2n) / lam**2
                ).subs(z, m2n / lam**2)
            )
            == 0
            for reg in (SHARP_PROPER_TIME_REGULATOR, SMOOTH_PROPER_TIME_REGULATOR)
        ),
    )
    spread = implementation.scheme_spread_ratio(cutoff=sp.Integer(1), mass_squared=sp.Integer(1))
    unit_expected = sp.simplify(J_smooth.subs(z, 1) / J_sharp.subs(z, 1))
    series = sp.series(J_smooth - J_sharp, z, 0, 2).removeO()
    checks.check(
        "spread structure: R(1) exact, leading difference EulerGamma*z, R unbounded",
        sp.simplify(spread.unit_mass_ratio - unit_expected) == 0
        and sp.simplify(series - gam * z) == 0
        and (J_smooth / J_sharp).subs(z, 100).evalf(30) > 10**30,
    )
    for reg in (SHARP_PROPER_TIME_REGULATOR, SMOOTH_PROPER_TIME_REGULATOR):
        result = implementation.total_inverse_gravity_coupling(
            sp.Rational(1, 4), 2, sp.Rational(0), regulator=reg, cutoff=1, mass_squared=1
        )
        accepted = exact_mass_inverse_newton_shift(
            2, sp.Rational(0), regulator=reg, cutoff=1, mass_squared=1
        )
        checks.check(
            f"total equals baseline plus accepted induced shift [{reg}]",
            sp.simplify(result.induced_shift - accepted.value) == 0
            and sp.simplify(result.total_inverse_coupling - (sp.Rational(1, 4) + accepted.value)) == 0,
        )
    mapping = implementation.attractive_sign_map(
        1, sp.Rational(1, 3), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0
    )
    boundary = mapping.baseline_boundary
    above = implementation.total_inverse_gravity_coupling(
        boundary + sp.Rational(1, 1000), 1, sp.Rational(1, 3),
        regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0,
    )
    below = implementation.total_inverse_gravity_coupling(
        boundary - sp.Rational(1, 1000), 1, sp.Rational(1, 3),
        regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0,
    )
    checks.check(
        "super-conformal boundary is necessary and sufficient",
        sp.simplify(boundary - 1 / (12 * sp.pi)) == 0
        and above.attractive_newtonian is True
        and below.attractive_newtonian is False
        and sp.simplify(mapping.all_mass_threshold - 1 / (12 * sp.pi)) == 0,
    )
    sub = implementation.attractive_sign_map(
        2, sp.Rational(0), regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 4)
    )
    neg_small = implementation.total_inverse_gravity_coupling(
        sp.Rational(-1, 1000), 2, sp.Rational(0),
        regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 4),
    )
    neg_large = implementation.total_inverse_gravity_coupling(
        sp.Rational(-1, 1000), 2, sp.Rational(0),
        regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Integer(100),
    )
    checks.check(
        "sub-conformal: B=0 attractive for all masses; negative B flips at large mass",
        sub.all_mass_threshold == 0
        and implementation.total_inverse_gravity_coupling(
            sp.Rational(0), 2, sp.Rational(0), regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Integer(100)
        ).attractive_newtonian
        is True
        and neg_small.attractive_newtonian is True
        and neg_large.attractive_newtonian is False,
    )
    conformal = [
        implementation.total_inverse_gravity_coupling(
            sp.Rational(0), count, sp.Rational(1, 6), regulator=reg, cutoff=1, mass_squared=sp.Rational(1, 3)
        )
        for count in (1, 3)
        for reg in (SHARP_PROPER_TIME_REGULATOR, SMOOTH_PROPER_TIME_REGULATOR)
    ]
    checks.check(
        "conformal point: purely-induced total is exactly zero (marginal)",
        all(r.total_sign == 0 and r.total_inverse_coupling == 0 for r in conformal)
        and all(
            implementation.purely_induced_attractive_verdict(xi) is expected
            for xi, expected in (
                (sp.Rational(0), True),
                (sp.Rational(1, 12), True),
                (sp.Rational(1, 6), False),
                (sp.Rational(1, 5), False),
            )
        ),
    )
    control = implementation.higher_curvature_control_ledger(1, cutoff=sp.Integer(1), mass_squared=sp.Integer(1))
    by_scheme = {entry.regulator: entry for entry in control.entries}
    checks.check(
        "tau^-1 control class equals -dJ/dz exactly in all three schemes",
        sp.simplify(sp.diff(J_sharp, z) + sp.expint(1, z)) == 0
        and sp.simplify(sp.diff(J_smooth, z) + 2 * sp.besselk(0, 2 * sp.sqrt(z))) == 0
        and sp.simplify(sp.diff(J_zeta, z) - (sp.log(z) + gam)) == 0
        and sp.simplify(by_scheme[SHARP_PROPER_TIME_REGULATOR].tau_minus_one_value - sp.expint(1, 1)) == 0
        and sp.simplify(by_scheme[SMOOTH_PROPER_TIME_REGULATOR].tau_minus_one_value - 2 * sp.besselk(0, 2)) == 0
        and sp.simplify(by_scheme[ZETA_POWER_SUBTRACTED_REGULATOR].tau_minus_one_value - gam) == 0,
    )
    checks.check(
        "control ledger carries the predeclared domain and nonlocal bound",
        "z_min" in control.predeclared_domain
        and "Lambda**-2" in control.nonlocal_remainder_bound
        and control.vacuum_sector_value is not None,
    )
    accepted_value = exact_mass_inverse_newton_shift(
        1, sp.Rational(0), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=1
    ).value
    wrong_prefactor = sp.simplify(accepted_value * 2)
    flipped = exact_mass_inverse_newton_shift(
        1, sp.Rational(1, 5), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=1
    ).value
    wrong_bessel = sp.simplify(
        sp.diff(2 * sp.sqrt(z) * sp.besselk(0, 2 * sp.sqrt(z)), z) + 2 * sp.besselk(0, 2 * sp.sqrt(z))
    )
    wrong_branch = sp.simplify(
        sp.diff(J_sharp.subs(sp.expint(1, z), sp.expint(1, -z)), z) + sp.expint(1, z)
    )
    checks.check(
        "mutations break load-bearing checks: prefactor, xi sign, Bessel order, E1 branch",
        sp.simplify(wrong_prefactor - accepted_value) != 0
        and (sp.simplify(flipped + accepted_value) != 0 or accepted_value == 0)
        and wrong_bessel != 0
        and wrong_branch != 0,
    )
    baseline_flip = implementation.total_inverse_gravity_coupling(
        sp.Rational(-1, 4), 2, sp.Rational(0),
        regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=1,
    )
    positive_case = implementation.total_inverse_gravity_coupling(
        sp.Rational(1, 4), 2, sp.Rational(0),
        regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=1,
    )
    checks.check(
        "baseline sign mutation flips the attractive verdict",
        baseline_flip.attractive_newtonian is False and positive_case.attractive_newtonian is True,
    )
    try:
        implementation.total_inverse_gravity_coupling(
            sp.Rational(1), 1, sp.Rational(0),
            regulator=ZETA_POWER_SUBTRACTED_REGULATOR, cutoff=1, mass_squared=1,
        )
        zeta_rejected = False
    except ValueError:
        zeta_rejected = True
    checks.check("excluded scheme cannot normalize a total coupling", zeta_rejected)

    module_source = (ROOT / "src/substrate_framework/total_gravitational_coupling.py").read_text()
    test_body = "\n".join(
        line for line in (ROOT / "tests/test_total_gravitational_coupling.py").read_text().splitlines()
        if "forbidden" not in line
    )
    checks.check(
        "no empirical gravity comparator in module or tests",
        all(
            token not in module_source + test_body
            for token in ("6.674", "Planck", "planck", "M_pl", "M_Pl", "CODATA", "G_obs")
        ),
    )

    # --- exact monotone-decoupling proof: the tau^-1 class is itself an
    # integral of a strictly positive integrand (E1 via its definition and
    # the standard K_0 representation), so J' = -L < 0 exactly, and the
    # control class is literally the tau^-1 proper-time integral. ---
    u = sp.symbols("u", positive=True)
    # E1(z) = integral_1^infinity exp(-z*u)/u du: positivity is the positive
    # integrand, decay to zero is the exact squeeze u >= 1 giving
    # E1(z) <= integral_1^infinity exp(-z*u) du = exp(-z)/z.
    checks.check(
        "tau^-1 class is the positive-integrand proper-time integral (exact squeeze)",
        sp.simplify(sp.diff(sp.expint(1, z), z) + sp.exp(-z) / z) == 0
        and sp.simplify(
            (sp.integrate(sp.exp(-z * u) / u, (u, 1, sp.oo)) - sp.expint(1, z)).rewrite(sp.Ei)
        )
        == 0
        and all(
            sp.expint(1, q).evalf(30) > 0
            and sp.expint(1, q).evalf(30) <= (sp.exp(-q) / q).evalf(30)
            for q in (sp.Rational(1, 10), sp.Integer(1), sp.Integer(10))
        ),
    )
    checks.check(
        "smooth tau^-1 class matches the K_0 representation derivative",
        sp.simplify(
            sp.diff(2 * sp.besselk(0, 2 * sp.sqrt(z)), z) + 2 / sp.sqrt(z) * sp.besselk(1, 2 * sp.sqrt(z))
        )
        == 0,
    )
    # --- massless boundary: the accepted continuous extension ---
    checks.check(
        "massless boundary returns the accepted continuous extension, never NaN",
        implementation.curvature_scale_factor(SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0) == 1
        and implementation.curvature_scale_factor(SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0) == 1
        and implementation.curvature_scale_factor(ZETA_POWER_SUBTRACTED_REGULATOR, cutoff=1, mass_squared=0) == 0
        and implementation.scheme_spread_ratio(cutoff=1, mass_squared=0).ratio == 1,
    )
    try:
        implementation.higher_curvature_control_ledger(1, cutoff=1, mass_squared=0)
        control_divergence_declared = False
    except ValueError as exc:
        control_divergence_declared = "z_min" in str(exc)
    checks.check(
        "log divergence of the tau^-1 class at m^2=0 is declared, not silent",
        control_divergence_declared,
    )
    # --- baseline provenance (issue #88 obligation: explicit provenance and ceiling) ---
    provenance = baseline_provenance(
        1, sp.Rational(0), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=1
    )
    checks.check(
        "baseline provenance: B=0 premise, attractive verdict, exact G_total, quoted ceiling",
        provenance.is_purely_induced is True
        and provenance.purely_induced_attractive is True
        and sp.simplify(
            1 / provenance.purely_induced_newton_constant
            - provenance.purely_induced_total_inverse_coupling
        )
        == 0
        and "scheme-bracketed" in provenance.downstream_ceiling
        and provenance.status.startswith("declared_premise_per_C-GRV-001"),
    )
    conformal_provenance = baseline_provenance(
        3, sp.Rational(1, 6), regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 3)
    )
    checks.check(
        "conformal baseline provenance lands on the marginal locus exactly",
        conformal_provenance.purely_induced_total_inverse_coupling == 0
        and conformal_provenance.purely_induced_attractive is False
        and conformal_provenance.purely_induced_newton_constant is None,
    )

    # --- renormalization condition (issue #88: physical_regulator_or_renormalization_condition) ---
    condition = implementation.renormalization_condition(cutoff=sp.Integer(1), mass_squared=sp.Rational(1, 4))
    checks.check(
        "renormalization condition: usable set, finite parts, and reference member derived",
        condition.usable_schemes == (SHARP_PROPER_TIME_REGULATOR, SMOOTH_PROPER_TIME_REGULATOR)
        and condition.excluded_schemes == (ZETA_POWER_SUBTRACTED_REGULATOR,)
        and sp.simplify(condition.finite_parts[SHARP_PROPER_TIME_REGULATOR] - (sp.exp(-sp.Rational(1, 4)) - sp.Rational(1, 4) * sp.expint(1, sp.Rational(1, 4)))) == 0
        and sp.simplify(condition.finite_parts[SMOOTH_PROPER_TIME_REGULATOR] - sp.besselk(1, 1)) == 0
        and condition.reference_scheme == SHARP_PROPER_TIME_REGULATOR,
    )
    checks.check(
        "condition massless limit reproduces the accepted C-GRV-001 shift s*Lambda^2",
        implementation.renormalization_condition(cutoff=sp.Integer(1), mass_squared=0).finite_parts[SHARP_PROPER_TIME_REGULATOR] == 1
        and sp.simplify(exact_mass_inverse_newton_shift(3, sp.Rational(0), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0).value - sp.Rational(1, 4) / sp.pi) == 0
        and "E_cut = hbar*c/a" in condition.reference_justification,
    )
    checks.check(
        "condition provenance names accepted claims and approved imports; unpromoted modules are non-authority",
        "C-GRV-001" in " ".join(condition.provenance)
        and "C-IGR-001" in " ".join(condition.provenance)
        and "Vassilevich" in " ".join(condition.provenance)
        and "Visser" in " ".join(condition.provenance)
        and "scalar_induced_newton" in " ".join(condition.non_authority)
        and "covariant_sine_gordon_action" in " ".join(condition.non_authority),
    )

    # --- total Newton constant (issue #88: total_Newton_constant) ---
    newton = implementation.total_newton_constant(sp.Integer(0), 3, sp.Rational(0), cutoff=1, mass_squared=sp.Rational(1, 4))
    newton_by_scheme = {e.regulator: e for e in newton.entries}
    checks.check(
        "total Newton constant: reciprocal identity and attractive sign on the usable set",
        all(
            sp.simplify(e.total_newton_constant * e.total_inverse_coupling - 1) == 0
            and e.total_sign == 1
            and e.attractive_newtonian is True
            for e in newton.entries
        ),
    )
    checks.check(
        "purely-induced bracket endpoints are 12*pi/(N*J(z)) and G ratio is the spread R(z)",
        sp.simplify(newton.purely_induced_bracket[0] - 12 * sp.pi / (3 * sp.besselk(1, 1))) == 0
        and sp.simplify(
            newton_by_scheme[SHARP_PROPER_TIME_REGULATOR].total_newton_constant
            / newton_by_scheme[SMOOTH_PROPER_TIME_REGULATOR].total_newton_constant
            - sp.besselk(1, 1) / (sp.exp(-sp.Rational(1, 4)) - sp.Rational(1, 4) * sp.expint(1, sp.Rational(1, 4)))
        )
        == 0,
    )
    conformal_newton = implementation.total_newton_constant(sp.Integer(0), 3, sp.Rational(1, 6), cutoff=1, mass_squared=sp.Rational(1, 3))
    repulsive_newton = implementation.total_newton_constant(sp.Integer(-1), 1, sp.Rational(1, 3), cutoff=1, mass_squared=1)
    checks.check(
        "Newton constant honesty: conformal marginal is None (never zoo); repulsive is negative",
        all(
            e.total_newton_constant is None and e.acceptance == "marginal_zero_total_no_newton_constant"
            for e in conformal_newton.entries
        )
        and conformal_newton.purely_induced_bracket is None
        and all(
            e.total_sign == -1 and e.attractive_newtonian is False
            and sp.Float(sp.N(e.total_newton_constant, 50), 50) < 0
            for e in repulsive_newton.entries
        ),
    )

    import os

    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_scalar_one_loop_mass.py", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    checks.check(
        "accepted P230 consumer suite still passes",
        proc.returncode == 0 and "passed" in proc.stdout,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(run())
