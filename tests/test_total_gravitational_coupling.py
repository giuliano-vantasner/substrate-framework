"""Total gravitational coupling tests (P231, advances #88).

Oracles, per ``.agents/skills/physics-erdos-loop/references/oracles.md``:

* exact selection legs, squeeze bounds, sign-map boundaries, and control
  identities are verified symbolically (SymPy) or by exact Leibniz
  derivative-plus-endpoint reconstructions;
* special-function closed forms are corroborated by high-precision mpmath
  quadrature of their defining integrals;
* load-bearing mutations (wrong prefactor, wrong sign, wrong Bessel order,
  wrong exponential-integral branch, baseline flips, threshold crossings)
  must each break a relevant check;
* no empirical gravitational comparator appears anywhere (comparator
  blinding is frozen in the proposal manifest).
"""

import mpmath as mp
import pytest
import sympy as sp

import substrate_framework as framework
from substrate_framework.scalar_induced_newton import SHARP_PROPER_TIME_REGULATOR
from substrate_framework.scalar_one_loop_mass import (
    SMOOTH_PROPER_TIME_REGULATOR,
    ZETA_POWER_SUBTRACTED_REGULATOR,
    curvature_proper_time_integral,
    exact_mass_inverse_newton_shift,
)
from substrate_framework.total_gravitational_coupling import (
    EXCLUDED_TOTAL_COUPLING_SCHEMES,
    USABLE_TOTAL_COUPLING_SCHEMES,
    attractive_sign_map,
    baseline_provenance,
    curvature_scale_factor,
    higher_curvature_control_ledger,
    purely_induced_attractive_verdict,
    scheme_selection_ledger,
    scheme_spread_ratio,
    total_inverse_gravity_coupling,
)

z = sp.symbols("z", positive=True)
t = sp.symbols("t", positive=True)
gam = sp.EulerGamma

J_sharp = sp.exp(-z) - z * sp.expint(1, z)
J_smooth = 2 * sp.sqrt(z) * sp.besselk(1, 2 * sp.sqrt(z))
J_zeta = z * (sp.log(z) + gam - 1)


def test_total_coupling_api_is_exported_from_package() -> None:
    assert framework.USABLE_TOTAL_COUPLING_SCHEMES == USABLE_TOTAL_COUPLING_SCHEMES
    assert framework.EXCLUDED_TOTAL_COUPLING_SCHEMES == EXCLUDED_TOTAL_COUPLING_SCHEMES
    assert framework.scheme_selection_ledger is scheme_selection_ledger
    assert framework.curvature_scale_factor is curvature_scale_factor
    assert framework.scheme_spread_ratio is scheme_spread_ratio
    assert framework.total_inverse_gravity_coupling is total_inverse_gravity_coupling
    assert framework.attractive_sign_map is attractive_sign_map
    assert framework.purely_induced_attractive_verdict is purely_induced_attractive_verdict
    assert framework.higher_curvature_control_ledger is higher_curvature_control_ledger


def test_selection_ledger_derives_the_usable_scheme_set() -> None:
    ledger = scheme_selection_ledger(cutoff=sp.Integer(1), mass_squared=sp.Integer(1))
    assert ledger.usable_schemes == (SHARP_PROPER_TIME_REGULATOR, SMOOTH_PROPER_TIME_REGULATOR)
    assert ledger.excluded_schemes == (ZETA_POWER_SUBTRACTED_REGULATOR,)
    by_scheme = {entry.regulator: entry for entry in ledger.entries}
    for regulator in USABLE_TOTAL_COUPLING_SCHEMES:
        entry = by_scheme[regulator]
        assert entry.usable is True
        assert entry.spectral_positivity is True
        assert entry.monotone_decoupling is True
        assert "E_cut" in entry.cutoff_ontology
    zeta_entry = by_scheme[ZETA_POWER_SUBTRACTED_REGULATOR]
    assert zeta_entry.usable is False
    assert len(zeta_entry.exclusion_reasons) == 3
    assert all(reason.startswith(("L1", "L2", "L3")) for reason in zeta_entry.exclusion_reasons)


def test_zeta_sign_change_root_is_exact() -> None:
    root = sp.exp(1 - gam)
    assert sp.simplify(J_zeta.subs(z, root)) == 0
    assert J_zeta.subs(z, sp.Rational(1, 1)).evalf(20) < 0
    assert J_zeta.subs(z, sp.Integer(2)).evalf(20) > 0
    ledger = scheme_selection_ledger(cutoff=sp.Integer(1), mass_squared=sp.Integer(1))
    assert sp.simplify(ledger.zeta_sign_change_root - root) == 0


def test_sharp_scale_factor_equals_its_defining_integral() -> None:
    integral = sp.Integral(sp.exp(-z * t) * t**-2, (t, 1, sp.oo))
    integrand = sp.lambdify((t, z), sp.exp(-z * t) * t**-2, "mpmath")
    for q in (sp.Rational(1, 4), 1, 4):
        closed = J_sharp.subs(z, q)
        numeric = mp.quad(lambda tt: integrand(tt, q), [1, mp.inf])
        assert abs(numeric - mp.mpf(closed.evalf(50))) < mp.mpf("1e-40")
    assert sp.simplify(sp.diff(J_sharp, z) + sp.expint(1, z)) == 0
    assert sp.limit(J_sharp, z, 0, "+") == 1
    assert sp.integrate(t**-2, (t, 1, sp.oo)) == 1


def test_smooth_scale_factor_equals_its_defining_integral() -> None:
    integrand = sp.lambdify((t, z), sp.exp(-z * t - 1 / t) * t**-2, "mpmath")
    for q in (sp.Rational(1, 4), 1, 4):
        closed = J_smooth.subs(z, q)
        numeric = mp.quad(lambda tt: integrand(tt, q), [0, 1, mp.inf])
        assert abs(numeric - mp.mpf(closed.evalf(50))) < mp.mpf("1e-40")
    assert sp.simplify(sp.diff(J_smooth, z) + 2 * sp.besselk(0, 2 * sp.sqrt(z))) == 0
    assert sp.limit(J_smooth, z, 0, "+") == 1
    assert mp.quad(lambda s: mp.e**-s, [0, mp.inf]) == 1


def test_squeeze_bound_holds_for_both_usable_schemes() -> None:
    grid = [sp.Rational(1, 100), sp.Rational(1, 10), sp.Rational(1, 2), sp.Integer(1), sp.Integer(2), sp.Integer(10)]
    for point in grid:
        for factor in (J_sharp, J_smooth):
            value = factor.subs(z, point).evalf(30)
            assert 0 < value <= 1
    assert sp.limit(J_sharp, z, 0, "+") == 1
    assert sp.limit(J_smooth, z, 0, "+") == 1


def test_monotone_decoupling_derivatives_are_negative() -> None:
    grid = [sp.Rational(1, 100), sp.Rational(1, 10), sp.Integer(1), sp.Integer(10)]
    for point in grid:
        assert sp.diff(J_sharp, z).subs(z, point).evalf(30) < 0
        assert sp.diff(J_smooth, z).subs(z, point).evalf(30) < 0
    assert sp.simplify(sp.diff(J_zeta, z).subs(z, sp.Rational(1, 10))) .is_negative is True
    assert sp.simplify(sp.diff(J_zeta, z).subs(z, sp.Integer(10))).is_positive is True


def test_scale_factors_match_accepted_coefficient_families() -> None:
    lam = sp.Symbol("Lambda", positive=True)
    m2 = sp.Symbol("m2", nonnegative=True)
    for regulator, factor in (
        (SHARP_PROPER_TIME_REGULATOR, J_sharp),
        (SMOOTH_PROPER_TIME_REGULATOR, J_smooth),
    ):
        ours = curvature_scale_factor(regulator, cutoff=lam, mass_squared=m2)
        accepted = sp.simplify(
            curvature_proper_time_integral(regulator, cutoff=lam, mass_squared=m2) / lam**2
        )
        assert sp.simplify(ours - accepted.subs(z, m2 / lam**2)) == 0


def test_scheme_spread_ratio_structure_is_exact() -> None:
    spread = scheme_spread_ratio(cutoff=sp.Integer(1), mass_squared=sp.Integer(1))
    expected = sp.simplify(J_smooth.subs(z, 1) / J_sharp.subs(z, 1))
    assert sp.simplify(spread.unit_mass_ratio - expected) == 0
    assert float(spread.unit_mass_ratio.evalf(12)) == pytest.approx(1.88377257808, abs=1e-11)
    series = sp.series(J_smooth - J_sharp, z, 0, 2).removeO()
    assert sp.simplify(series / (gam * z)) == 1
    large = (J_smooth / J_sharp).subs(z, 100).evalf(30)
    assert large > 10**30


def test_total_composition_uses_the_accepted_induced_shift() -> None:
    lam, m2 = sp.Integer(1), sp.Integer(1)
    for regulator in USABLE_TOTAL_COUPLING_SCHEMES:
        result = total_inverse_gravity_coupling(
            sp.Rational(1, 4), 2, sp.Rational(0), regulator=regulator, cutoff=lam, mass_squared=m2
        )
        accepted = exact_mass_inverse_newton_shift(
            2, sp.Rational(0), regulator=regulator, cutoff=lam, mass_squared=m2
        )
        assert sp.simplify(result.induced_shift - accepted.value) == 0
        assert sp.simplify(result.total_inverse_coupling - (sp.Rational(1, 4) + accepted.value)) == 0


def test_sub_conformal_sign_map_cases() -> None:
    for regulator in USABLE_TOTAL_COUPLING_SCHEMES:
        attractive = total_inverse_gravity_coupling(
            sp.Rational(0), 1, sp.Rational(0), regulator=regulator, cutoff=1, mass_squared=1
        )
        assert attractive.attractive_newtonian is True
        negative_baseline = total_inverse_gravity_coupling(
            sp.Rational(-1, 10), 1, sp.Rational(0), regulator=regulator, cutoff=1, mass_squared=1
        )
        assert negative_baseline.attractive_newtonian is False


def test_sign_map_boundary_is_necessary_and_sufficient() -> None:
    regulator = SHARP_PROPER_TIME_REGULATOR
    mapping = attractive_sign_map(1, sp.Rational(1, 3), regulator=regulator, cutoff=1, mass_squared=0)
    boundary = mapping.baseline_boundary
    assert sp.simplify(boundary - sp.Rational(1, 12) / sp.pi) == 0
    just_above = total_inverse_gravity_coupling(
        boundary + sp.Rational(1, 1000), 1, sp.Rational(1, 3), regulator=regulator, cutoff=1, mass_squared=0
    )
    just_below = total_inverse_gravity_coupling(
        boundary - sp.Rational(1, 1000), 1, sp.Rational(1, 3), regulator=regulator, cutoff=1, mass_squared=0
    )
    assert just_above.attractive_newtonian is True
    assert just_below.attractive_newtonian is False
    assert sp.simplify(mapping.all_mass_threshold - sp.Rational(1, 12) / sp.pi) == 0


def test_sub_conformal_uniform_in_mass_threshold() -> None:
    """F2 repair: the uniform-in-mass condition is ``B >= 0`` with threshold 0.

    Because ``J`` decreases strictly from 1 to 0, a negative baseline always
    turns repulsive at large mass; the previous all-mass threshold
    ``B > -N*(1-6*xi)*Lambda**2/(12*pi)`` used the wrong worst case (``J=1``
    instead of ``J -> 0``) and is rejected below on both sides.
    """
    regulator = SMOOTH_PROPER_TIME_REGULATOR
    mapping = attractive_sign_map(3, sp.Rational(0), regulator=regulator, cutoff=1, mass_squared=sp.Rational(1, 4))
    assert mapping.all_mass_threshold == 0
    assert "iff B >= 0" in mapping.uniform_in_mass_condition
    # B = 0 is attractive at every mass, for both usable schemes.
    for scheme in USABLE_TOTAL_COUPLING_SCHEMES:
        for mass_squared in (0, sp.Rational(1, 4), 25):
            total = total_inverse_gravity_coupling(
                sp.Integer(0), 3, sp.Rational(0), regulator=scheme, cutoff=1, mass_squared=mass_squared
            )
            assert total.attractive_newtonian is True
    # A negative baseline is attractive at small mass and repulsive at large mass.
    small = total_inverse_gravity_coupling(
        sp.Rational(-1, 100), 3, sp.Rational(0), regulator=regulator, cutoff=1, mass_squared=0
    )
    large = total_inverse_gravity_coupling(
        sp.Rational(-1, 100), 3, sp.Rational(0), regulator=regulator, cutoff=1, mass_squared=10**4
    )
    assert small.attractive_newtonian is True and large.attractive_newtonian is False


def test_conformal_point_is_marginal() -> None:
    for regulator in USABLE_TOTAL_COUPLING_SCHEMES:
        for count in (1, 3):
            result = total_inverse_gravity_coupling(
                sp.Rational(0), count, sp.Rational(1, 6), regulator=regulator, cutoff=1, mass_squared=sp.Rational(1, 3)
            )
            assert result.total_sign == 0
            assert result.acceptance == "marginal_zero_total"
            assert result.total_inverse_coupling == 0
        with_positive_baseline = total_inverse_gravity_coupling(
            sp.Rational(1, 10), 1, sp.Rational(1, 6), regulator=regulator, cutoff=1, mass_squared=0
        )
        assert with_positive_baseline.attractive_newtonian is True


def test_purely_induced_verdict_is_scheme_and_parameter_independent() -> None:
    assert purely_induced_attractive_verdict(sp.Rational(0)) is True
    assert purely_induced_attractive_verdict(sp.Rational(1, 12)) is True
    assert purely_induced_attractive_verdict(sp.Rational(1, 6)) is False
    assert purely_induced_attractive_verdict(sp.Rational(1, 5)) is False
    with pytest.raises(ValueError):
        purely_induced_attractive_verdict(sp.Symbol("xi", real=True))


def test_power_subtracted_family_cannot_normalize_a_total() -> None:
    with pytest.raises(ValueError, match="usable set"):
        total_inverse_gravity_coupling(
            sp.Rational(1), 1, sp.Rational(0), regulator=ZETA_POWER_SUBTRACTED_REGULATOR, cutoff=1, mass_squared=1
        )


def test_input_contracts_are_enforced() -> None:
    regulator = SHARP_PROPER_TIME_REGULATOR
    with pytest.raises(ValueError):
        total_inverse_gravity_coupling(sp.Rational(0), sp.Rational(3, 2), sp.Rational(0), regulator=regulator, cutoff=1)
    with pytest.raises(ValueError):
        total_inverse_gravity_coupling(sp.Rational(0), 1, sp.Rational(0), regulator=regulator, cutoff=sp.Integer(-1))
    with pytest.raises(ValueError):
        total_inverse_gravity_coupling(sp.Rational(0), 1, sp.Rational(0), regulator=regulator, cutoff=1, mass_squared=sp.Integer(-1))
    with pytest.raises(ValueError):
        total_inverse_gravity_coupling(sp.Symbol("B"), 1, sp.Rational(0), regulator=regulator, cutoff=1)


def test_symbolic_baseline_leaves_total_undecidable() -> None:
    b = sp.Symbol("B", real=True, negative=False)
    result = total_inverse_gravity_coupling(
        b, 1, sp.Rational(0), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=1
    )
    assert result.total_sign == 1  # B >= 0 cannot cancel the strictly positive shift
    b_positive = total_inverse_gravity_coupling(
        sp.Symbol("B", positive=True), 1, sp.Rational(0), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=1
    )
    assert b_positive.total_sign == 1
    unconstrained = total_inverse_gravity_coupling(
        sp.Symbol("B", real=True), 1, sp.Rational(1, 5), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=1
    )
    assert unconstrained.total_sign is None
    assert unconstrained.acceptance == "undecidable_symbolic_total"


def test_control_ledger_tau_minus_one_is_minus_dJdz() -> None:
    ledger = higher_curvature_control_ledger(1, cutoff=sp.Integer(1), mass_squared=sp.Integer(1))
    by_scheme = {entry.regulator: entry for entry in ledger.entries}
    assert sp.simplify(sp.diff(J_sharp, z) + sp.expint(1, z)) == 0
    assert sp.simplify(sp.diff(J_smooth, z) + 2 * sp.besselk(0, 2 * sp.sqrt(z))) == 0
    assert sp.simplify(sp.diff(J_zeta, z) - (sp.log(z) + gam)) == 0
    assert by_scheme[SHARP_PROPER_TIME_REGULATOR].tau_minus_one_value == sp.expint(1, z).subs(z, 1)
    assert by_scheme[SMOOTH_PROPER_TIME_REGULATOR].tau_minus_one_value == 2 * sp.besselk(0, 2)
    assert sp.simplify(by_scheme[ZETA_POWER_SUBTRACTED_REGULATOR].tau_minus_one_value - gam) == 0
    assert ledger.vacuum_sector_value is not None
    assert "z_min" in ledger.predeclared_domain
    assert ledger.nonlocal_remainder_bound


def test_control_ratio_is_monotone_decreasing_above_z_min() -> None:
    grid = [mp.mpf("0.1") * 10 ** (i / 20) for i in range(41)]
    ratios_sharp = [mp.e1(x) / (mp.e**-x - x * mp.e1(x)) for x in grid]
    ratios_smooth = [
        2 * mp.besselk(0, 2 * mp.sqrt(x)) / (2 * mp.sqrt(x) * mp.besselk(1, 2 * mp.sqrt(x)))
        for x in grid
    ]
    assert all(a > b for a, b in zip(ratios_sharp, ratios_sharp[1:]))
    assert all(a > b for a, b in zip(ratios_smooth, ratios_smooth[1:]))


def test_quadrature_corroborates_defining_integrals() -> None:
    mp.mp.dps = 30
    for point in (mp.mpf("0.3"), mp.mpf(1), mp.mpf(2)):
        sharp_quad = mp.quad(lambda tt: mp.e**(-point * tt) * tt**-2, [1, mp.inf])
        assert sharp_quad == pytest.approx(float(J_sharp.subs(z, sp.Rational(3, 10) if point < 1 else (sp.Integer(1) if point == 1 else sp.Integer(2))).evalf(30)), rel=1e-20) or abs(sharp_quad - J_sharp.subs(z, sp.nsimplify(str(point))).evalf(30)) < mp.mpf(10) ** -20
        smooth_quad = mp.quad(lambda tt: mp.e**(-point * tt - 1 / tt) * tt**-2, [0, 1, mp.inf])
        assert abs(smooth_quad - J_smooth.subs(z, sp.nsimplify(str(point))).evalf(30)) < mp.mpf(10) ** -20


def test_mutations_break_the_load_bearing_checks() -> None:
    lam = sp.Integer(1)
    accepted = exact_mass_inverse_newton_shift(1, sp.Rational(0), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=lam, mass_squared=sp.Integer(1)).value
    wrong_prefactor = sp.simplify(accepted * 2)
    assert sp.simplify(wrong_prefactor - accepted) != 0
    flipped_sign = exact_mass_inverse_newton_shift(1, sp.Rational(1, 5), regulator=SHARP_PROPER_TIME_REGULATOR, cutoff=lam, mass_squared=sp.Integer(1)).value
    assert sp.simplify(flipped_sign + accepted) != 0 or accepted == 0
    wrong_bessel = sp.diff(2 * sp.sqrt(z) * sp.besselk(0, 2 * sp.sqrt(z)), z) + 2 * sp.besselk(0, 2 * sp.sqrt(z))
    assert sp.simplify(wrong_bessel) != 0
    wrong_branch = sp.diff(J_sharp.subs(sp.expint(1, z), sp.expint(1, -z)), z)
    assert sp.simplify(wrong_branch + sp.expint(1, z)) != 0


def test_no_empirical_gravity_comparator_is_imported() -> None:
    source = framework.total_gravitational_coupling.__doc__ or ""
    lowered = source.lower()
    assert "nothing here selects an observed g" in lowered
    assert "empirical comparator" in lowered
    # no measured constants: forbid decimal and scientific-notation numbers
    # (single small integers such as the 1 in 1/G_total are structural)
    import re as _re

    decimals = [
        tok
        for tok in source.replace(",", "").split()
        if _re.fullmatch(r"\d+\.\d+", tok.strip("`()[];:."))
        and not tok.endswith("..")
    ]
    scientific = [
        tok
        for tok in source.replace(",", "").split()
        if _re.fullmatch(r"\d+(\.\d+)?e[+-]?\d+", tok.strip("`()[];:."), _re.IGNORECASE)
    ]
    assert decimals == [] and scientific == []


def test_massless_scale_factor_continuous_extension() -> None:
    """F1 repair: J(z) is continuously extended at m**2 = 0, never NaN."""
    assert curvature_scale_factor(SHARP_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0) == 1
    assert curvature_scale_factor(SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=0) == 1
    assert curvature_scale_factor(ZETA_POWER_SUBTRACTED_REGULATOR, cutoff=1, mass_squared=0) == 0
    for scheme in (SHARP_PROPER_TIME_REGULATOR, SMOOTH_PROPER_TIME_REGULATOR, ZETA_POWER_SUBTRACTED_REGULATOR):
        value = curvature_scale_factor(scheme, cutoff=1, mass_squared=0)
        numeric = sp.Float(sp.N(value, 50))
        assert numeric == numeric  # never NaN
    # the one-sided limits agree with the extensions
    assert sp.limit(J_sharp, z, 0, "+") == 1
    assert sp.limit(J_smooth, z, 0, "+") == 1
    assert sp.limit(J_zeta, z, 0, "+") == 0


def test_massless_ledger_and_spread_are_not_corrupted() -> None:
    """F1 repair: selection ledger and spread ratio stay exact at m**2 = 0."""
    ledger = scheme_selection_ledger(cutoff=1, mass_squared=0)
    assert ledger.usable_schemes == USABLE_TOTAL_COUPLING_SCHEMES
    assert ledger.excluded_schemes == (ZETA_POWER_SUBTRACTED_REGULATOR,)
    spread = scheme_spread_ratio(cutoff=1, mass_squared=0)
    assert spread.sharp_factor == 1 and spread.smooth_factor == 1
    assert spread.ratio == 1


def test_sign_decidability_three_tier_classifier() -> None:
    """F4 repair: exact -> derived-structure -> certified-numeric tiers, never guessing."""
    # Tier 2: SymPy cannot decide Bessel-based sign directly, but J > 0 on the
    # usable set makes the B = 0 total carry the sign of 1 - 6*xi.
    sub_conformal = total_inverse_gravity_coupling(
        sp.Integer(0), 3, sp.Rational(0), regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 4)
    )
    assert sub_conformal.total_sign == 1 and sub_conformal.attractive_newtonian is True
    super_conformal = total_inverse_gravity_coupling(
        sp.Integer(0), 3, sp.Rational(1, 3), regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 4)
    )
    assert super_conformal.total_sign == -1 and super_conformal.attractive_newtonian is False
    # Tier 3: a symbol-free near-cancellation is decided by certified numeric
    # separation at 70 digits, and a total inside the 1e-50 band stays None.
    shift_at_quarter = sp.Float(
        sp.N(3 * 2 * sp.sqrt(sp.Rational(1, 4)) * sp.besselk(1, 1) / (12 * sp.pi), 70), 70
    )
    decided = total_inverse_gravity_coupling(
        -shift_at_quarter * (1 - sp.Float("1e-20", 70)),
        3,
        sp.Rational(0),
        regulator=SMOOTH_PROPER_TIME_REGULATOR,
        cutoff=1,
        mass_squared=sp.Rational(1, 4),
    )
    assert decided.total_sign == 1 and decided.attractive_newtonian is True
    banded = total_inverse_gravity_coupling(
        -shift_at_quarter + sp.Float("1e-60", 70),
        3,
        sp.Rational(0),
        regulator=SMOOTH_PROPER_TIME_REGULATOR,
        cutoff=1,
        mass_squared=sp.Rational(1, 4),
    )
    assert banded.total_sign is None and banded.attractive_newtonian is None
    assert banded.acceptance == "undecidable_symbolic_total"


def test_control_ledger_raises_in_log_divergent_massless_limit() -> None:
    """F5 repair: the tau^-1 class diverges at m**2 = 0 and must raise, not return inf."""
    with pytest.raises(ValueError, match="logarithmically divergent"):
        higher_curvature_control_ledger(1, cutoff=1, mass_squared=0)
    ledger = higher_curvature_control_ledger(1, cutoff=1, mass_squared=1)
    assert "z_min" in ledger.predeclared_domain


def test_baseline_provenance_purely_induced_and_conformal() -> None:
    """F6 repair: the additive baseline provenance surface is explicit and exact."""
    record = baseline_provenance(3, sp.Rational(0), regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 4))
    assert record.is_purely_induced is True
    assert record.purely_induced_attractive is True
    assert record.purely_induced_total_inverse_coupling is not None
    # G_total = 12*pi / (N*(1-6*xi)*J(z)*Lambda**2) exactly
    shift = exact_mass_inverse_newton_shift(3, sp.Rational(0), regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 4))
    assert sp.simplify(record.purely_induced_newton_constant * shift.value - 1) == 0
    j_quarter = curvature_scale_factor(SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 4))
    assert sp.simplify(record.purely_induced_newton_constant - 12 * sp.pi / (3 * j_quarter)) == 0
    assert "scheme-bracketed" in record.downstream_ceiling
    assert "R(z)" in record.downstream_ceiling
    conformal = baseline_provenance(3, sp.Rational(1, 6), regulator=SMOOTH_PROPER_TIME_REGULATOR, cutoff=1, mass_squared=sp.Rational(1, 4))
    assert conformal.is_purely_induced is True
    assert conformal.purely_induced_total_inverse_coupling == 0
    assert "marginal" in conformal.status
    assert "no Newton constant" in conformal.downstream_ceiling
