"""Tests for exact affine homogenization of isotropic filament ensembles."""

from __future__ import annotations

import sympy as sp

from substrate_framework.homogenization import (
    affine_lame_moduli,
    affine_poisson_ratio,
    axial_moment_identity,
    cauchy_born_energy_density,
    sphere_fourth_moment_direct,
    sphere_fourth_moment_isotropic,
    sphere_second_moment,
    straight_line_tension,
)


def test_second_moment_direct_integration() -> None:
    moment = sphere_second_moment()
    assert sp.simplify(moment[0, 0] - sp.Rational(1, 3)) == 0
    assert moment[0, 1] == 0


def test_fourth_moment_two_routes_agree() -> None:
    direct = sphere_fourth_moment_direct()
    closure = sphere_fourth_moment_isotropic()
    for index, value in direct.items():
        assert sp.simplify(value - closure[index]) == 0


def test_axial_moment_identity_general_strain() -> None:
    exx, eyy, ezz, exy, exz, eyz = sp.symbols("a b c p q r", real=True)
    strain = sp.Matrix([[exx, exy, exz], [exy, eyy, eyz], [exz, eyz, ezz]])
    assert axial_moment_identity(strain) == 0


def test_affine_moduli_by_coefficient_matching() -> None:
    stiffness, density = sp.symbols("E_f L_v", positive=True)
    lam, mu = affine_lame_moduli(stiffness, density)
    assert sp.simplify(lam - stiffness * density / 15) == 0
    assert sp.simplify(mu - stiffness * density / 15) == 0


def test_poisson_ratio_quarter_and_speed_ratio() -> None:
    stiffness, density = sp.symbols("E_f L_v", positive=True)
    assert affine_poisson_ratio(stiffness, density) == sp.Rational(1, 4)


def test_line_tension_derived_from_biotsavart_integral() -> None:
    rho, gamma, outer, core = sp.symbols("rho Gamma R a", positive=True)
    tension = straight_line_tension(rho, gamma, outer, core)
    expected = rho * gamma**2 * sp.log(outer / core) / (4 * sp.pi)
    assert sp.simplify(tension - expected) == 0
