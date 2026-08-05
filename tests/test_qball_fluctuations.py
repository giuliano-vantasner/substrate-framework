from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.qball_fluctuations import (
    quartic_binding_coupling_ledger,
    quartic_curvature_deficit,
    quartic_fluctuation_bound_eigenvalues,
    quartic_fluctuation_bound_modes,
    quartic_fluctuation_continuum_threshold,
    quartic_fluctuation_operator,
    quartic_fluctuation_potential,
    quartic_qball_effective_potential,
    solve_quartic_fluctuation_spectrum,
)
from substrate_framework.quartic_qball import (
    quartic_qball_inverse_width,
    quartic_qball_profile,
)


def test_second_variation_derives_poschl_teller_potential() -> None:
    coordinate, field = sp.symbols("x f", real=True)
    frequency = sp.symbols("omega", positive=True)
    energy_potential = quartic_qball_effective_potential(field, frequency)
    profile = quartic_qball_profile(coordinate, frequency)
    assert sp.simplify(
        sp.diff(energy_potential, field)
        - (
            (sp.Rational(1, 2) - frequency**2) * field
            - field**3 / 12
        )
    ) == 0
    assert sp.simplify(
        sp.diff(energy_potential, field, 2).subs(field, profile)
        - quartic_fluctuation_potential(coordinate, frequency)
    ) == 0


def test_quartic_curvature_deficit_is_derived_before_profile_substitution() -> None:
    field, frequency = sp.symbols("f omega", real=True)
    assert quartic_curvature_deficit(field, frequency) == field**2 / 4


def test_linear_coupling_lock_retains_its_supplied_normalization() -> None:
    field, frequency = sp.symbols("f omega", real=True)
    scale = sp.symbols("lambda", nonzero=True, real=True)
    ledger = quartic_binding_coupling_ledger(field, frequency, scale)
    assert ledger.vacuum_curvature == sp.Rational(1, 2) - frequency**2
    assert ledger.field_curvature == (
        sp.Rational(1, 2) - frequency**2 - field**2 / 4
    )
    assert ledger.curvature_deficit == field**2 / 4
    assert ledger.local_coupling == scale * field
    assert ledger.lock_coefficient == 1 / (4 * scale**2)
    assert ledger.lock_residual == 0


def test_profile_substitution_gives_the_exact_quartic_well_depth() -> None:
    coordinate, frequency = sp.symbols("x omega", real=True)
    kappa = quartic_qball_inverse_width(frequency)
    profile = quartic_qball_profile(coordinate, frequency)
    assert sp.simplify(
        quartic_curvature_deficit(profile, frequency)
        - 6 * kappa**2 * sp.sech(kappa * coordinate) ** 2
    ) == 0


def test_lock_is_sensitive_to_coupling_and_potential_mutations() -> None:
    field, frequency, epsilon = sp.symbols("f omega epsilon", real=True)
    baseline = quartic_binding_coupling_ledger(field, frequency)
    nonlinear_coupling_residual = sp.simplify(
        baseline.curvature_deficit - field**4 / 4
    )
    deformed_potential = baseline.effective_potential + epsilon * field**6
    deformed_deficit = sp.simplify(
        sp.diff(deformed_potential, field, 2).subs(field, 0)
        - sp.diff(deformed_potential, field, 2)
    )
    assert nonlinear_coupling_residual != 0
    assert deformed_deficit == field**2 / 4 - 30 * epsilon * field**4
    assert sp.simplify(deformed_deficit - baseline.curvature_deficit) != 0


@pytest.mark.parametrize("scale", [0, sp.I])
def test_binding_coupling_ledger_rejects_invalid_numeric_scale(scale) -> None:
    with pytest.raises(ValueError, match="real and nonzero"):
        quartic_binding_coupling_ledger(1, sp.Rational(1, 2), scale)


def test_exact_bound_modes_and_eigenvalues() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    modes = quartic_fluctuation_bound_modes(coordinate, frequency)
    eigenvalues = quartic_fluctuation_bound_eigenvalues(frequency)
    for mode, eigenvalue in zip(modes, eigenvalues, strict=True):
        assert sp.simplify(
            quartic_fluctuation_operator(mode, coordinate, frequency)
            - eigenvalue * mode
        ) == 0


def test_modes_are_l2_orthogonal_and_have_expected_parity() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency = sp.Rational(1, 2)
    kappa = quartic_qball_inverse_width(frequency)
    even_mode, odd_mode = quartic_fluctuation_bound_modes(
        coordinate, frequency
    )
    assert even_mode.subs(coordinate, -coordinate) == even_mode
    assert sp.simplify(
        odd_mode.subs(coordinate, -coordinate) + odd_mode
    ) == 0
    assert sp.integrate(
        even_mode.rewrite(sp.cosh) ** 2,
        (coordinate, -sp.oo, sp.oo),
    ) == (
        4 / (3 * kappa)
    )
    assert sp.integrate(
        odd_mode.rewrite(sp.exp) ** 2,
        (coordinate, -sp.oo, sp.oo),
    ) == (
        2 / (3 * kappa)
    )
    assert sp.integrate(
        even_mode * odd_mode, (coordinate, -sp.oo, sp.oo)
    ) == 0


def test_zero_mode_is_translation_tangent_and_threshold_is_positive() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    profile = quartic_qball_profile(coordinate, frequency)
    _, translation_mode = quartic_fluctuation_bound_modes(
        coordinate, frequency
    )
    ratio = sp.simplify(sp.diff(profile, coordinate) / translation_mode)
    assert sp.diff(ratio, coordinate) == 0
    assert quartic_fluctuation_continuum_threshold(frequency) == (
        sp.Rational(1, 2) - frequency**2
    )


def test_finite_difference_spectrum_refines_to_exact_pair() -> None:
    frequency = sp.Rational(11, 20)
    coarse = solve_quartic_fluctuation_spectrum(
        frequency, points=2001
    )
    fine = solve_quartic_fluctuation_spectrum(
        frequency, points=4001
    )
    box = solve_quartic_fluctuation_spectrum(
        frequency, half_extent_in_widths=32.0, points=5335
    )
    exact = tuple(
        float(value)
        for value in quartic_fluctuation_bound_eigenvalues(frequency)
    )
    assert len(coarse.bound_eigenvalues) == 2
    assert len(fine.bound_eigenvalues) == 2
    assert len(box.bound_eigenvalues) == 2
    assert max(
        abs(observed - expected)
        for observed, expected in zip(
            fine.bound_eigenvalues, exact, strict=True
        )
    ) < 2.0e-5
    assert max(
        abs(a - b)
        for a, b in zip(
            coarse.bound_eigenvalues,
            fine.bound_eigenvalues,
            strict=True,
        )
    ) < 5.0e-5
    assert max(
        abs(a - b)
        for a, b in zip(
            fine.bound_eigenvalues,
            box.bound_eigenvalues,
            strict=True,
        )
    ) < 2.0e-5


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"points": 99}, "points"),
        ({"half_extent_in_widths": 0}, "half_extent"),
        ({"threshold_margin": 0}, "margin"),
    ],
)
def test_numeric_spectrum_guards(kwargs, message) -> None:
    with pytest.raises(ValueError, match=message):
        solve_quartic_fluctuation_spectrum(sp.Rational(1, 2), **kwargs)


def test_numeric_spectrum_requires_numeric_frequency() -> None:
    frequency = sp.symbols("omega", positive=True)
    with pytest.raises(ValueError, match="numeric"):
        solve_quartic_fluctuation_spectrum(frequency)
