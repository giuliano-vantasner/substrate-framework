from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.mode_counting import (
    isotropic_continuum_dos_on_band,
    isotropic_continuum_mode_count,
    isotropic_continuum_target_cutoff,
    isotropic_gapped_angular_frequency,
    unit_sphere_surface,
)


def test_unit_sphere_surface_first_three_dimensions() -> None:
    assert unit_sphere_surface(1) == 2
    assert unit_sphere_surface(2) == 2 * sp.pi
    assert unit_sphere_surface(3) == 4 * sp.pi


def test_gapped_dispersion_retains_speed_and_gap() -> None:
    k, c, omega_0 = sp.symbols("k c omega_0", positive=True)
    frequency = isotropic_gapped_angular_frequency(k, c, omega_0)
    assert sp.simplify(frequency**2 - omega_0**2 - c**2 * k**2) == 0
    assert frequency.subs(k, 0) == omega_0
    assert sp.limit(frequency.subs(omega_0, 0) / (c * k), k, sp.oo) == 1


def test_dos_specializations_keep_dimension_and_branches_separate() -> None:
    omega, omega_0, V, c = sp.symbols("omega omega_0 V c", positive=True)
    g1 = isotropic_continuum_dos_on_band(omega, V, c, omega_0, 1)
    g2 = isotropic_continuum_dos_on_band(omega, V, c, omega_0, 2)
    g3 = isotropic_continuum_dos_on_band(omega, V, c, omega_0, 3)
    assert g1 == V * omega / (sp.pi * c * sp.sqrt(omega**2 - omega_0**2))
    assert g2 == V * omega / (2 * sp.pi * c**2)
    assert g3 == V * omega * sp.sqrt(omega**2 - omega_0**2) / (2 * sp.pi**2 * c**3)
    assert isotropic_continuum_dos_on_band(
        omega, V, c, omega_0, 3, branches=3
    ) == 3 * g3


def test_frequency_integral_reconstructs_ball_count_and_loses_gap() -> None:
    omega, omega_0, V, c, K = sp.symbols(
        "omega omega_0 V c K", positive=True
    )
    upper = isotropic_gapped_angular_frequency(K, c, omega_0)
    for dimension in (1, 2, 3):
        density = isotropic_continuum_dos_on_band(
            omega,
            V,
            c,
            omega_0,
            dimension,
            branches=2,
        )
        integrated = sp.simplify(sp.integrate(density, (omega, omega_0, upper)))
        expected = isotropic_continuum_mode_count(
            K,
            V,
            dimension,
            branches=2,
        )
        assert sp.simplify(integrated - expected) == 0
        assert sp.simplify(sp.diff(integrated, omega_0)) == 0


def test_target_cutoff_exactly_inverts_continuum_count() -> None:
    target, V = sp.symbols("N V", positive=True)
    for dimension in (1, 2, 3, 4):
        cutoff = isotropic_continuum_target_cutoff(
            target,
            V,
            dimension,
            branches=3,
        )
        recovered = isotropic_continuum_mode_count(
            cutoff,
            V,
            dimension,
            branches=3,
        )
        assert sp.simplify(recovered - target) == 0


def test_md1_cutoff_is_a_typed_target_matching_corollary() -> None:
    V, a = sp.symbols("V a", positive=True)
    target = 3 * V / a**3
    cutoff = isotropic_continuum_target_cutoff(target, V, 3, branches=3)
    assert sp.simplify(cutoff - (6 * sp.pi**2) ** sp.Rational(1, 3) / a) == 0
    assert isotropic_continuum_mode_count(cutoff, V, 3, branches=1) == V / a**3
    assert isotropic_continuum_mode_count(cutoff, V, 3, branches=3) == target


def test_spatial_dimension_does_not_select_branch_degeneracy() -> None:
    V, K = sp.symbols("V K", positive=True)
    scalar_count = isotropic_continuum_mode_count(K, V, 3, branches=1)
    vector_count = isotropic_continuum_mode_count(K, V, 3, branches=3)
    assert sp.simplify(vector_count / scalar_count) == 3
    assert scalar_count != vector_count


def test_continuum_ball_volume_is_not_exact_finite_lattice_count() -> None:
    box_length = 2 * sp.pi
    cutoff = 1
    continuum = isotropic_continuum_mode_count(cutoff, box_length, 1)
    periodic_integer_wavevectors = tuple(n for n in range(-1, 2) if abs(n) <= cutoff)
    assert continuum == 2
    assert len(periodic_integer_wavevectors) == 3
    assert continuum != len(periodic_integer_wavevectors)


def test_sphere_normalization_and_branch_factor_are_load_bearing() -> None:
    V, K = sp.symbols("V K", positive=True)
    correct = isotropic_continuum_mode_count(K, V, 3, branches=2)
    wrong_surface = 2 * V * 2 * sp.pi * K**3 / (3 * (2 * sp.pi) ** 3)
    wrong_branch = isotropic_continuum_mode_count(K, V, 3, branches=1)
    assert sp.simplify(correct - wrong_surface) != 0
    assert sp.simplify(correct - wrong_branch) != 0


@pytest.mark.parametrize(
    ("call", "match"),
    [
        (lambda: unit_sphere_surface(0), "dimension"),
        (lambda: unit_sphere_surface(sp.Rational(3, 2)), "dimension"),
        (lambda: isotropic_gapped_angular_frequency(-1, 1, 0), "wavenumber"),
        (lambda: isotropic_gapped_angular_frequency(1, 0, 0), "signal_speed"),
        (lambda: isotropic_gapped_angular_frequency(1, 1, -1), "gap_frequency"),
        (lambda: isotropic_continuum_dos_on_band(1, 1, 1, 1, 3), "exceed"),
        (lambda: isotropic_continuum_mode_count(1, 1, 3, branches=0), "branches"),
        (lambda: isotropic_continuum_target_cutoff(0, 1, 3), "target_count"),
    ],
)
def test_invalid_domains_are_rejected(call, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        call()
