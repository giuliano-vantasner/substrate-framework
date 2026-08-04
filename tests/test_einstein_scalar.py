from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.einstein_scalar import (
    massless_scalar_flat_flrw,
    minimally_coupled_scalar_stress,
)


def test_homogeneous_scalar_stress_has_canonical_density_pressure_and_trace() -> None:
    a, velocity, potential = sp.symbols("a v V", positive=True)
    metric = sp.diag(-1, a**2, a**2, a**2)
    result = minimally_coupled_scalar_stress(
        metric, [velocity, 0, 0, 0], potential
    )
    density = velocity**2 / 2 + potential
    pressure = velocity**2 / 2 - potential
    assert result.covariant[0, 0] == density
    assert result.covariant[1, 1] == a**2 * pressure
    assert result.covariant[2, 2] == a**2 * pressure
    assert result.trace == velocity**2 - 4 * potential


def test_wrong_kinetic_sign_has_negative_gradient_energy() -> None:
    velocity = sp.symbols("v", positive=True)
    canonical = minimally_coupled_scalar_stress(
        sp.diag(-1, 1, 1, 1), [velocity, 0, 0, 0], 0
    )
    ghost = minimally_coupled_scalar_stress(
        sp.diag(-1, 1, 1, 1),
        [velocity, 0, 0, 0],
        0,
        kinetic_coefficient=-1,
    )
    assert canonical.covariant[0, 0] == velocity**2 / 2
    assert ghost.covariant[0, 0] == -velocity**2 / 2


def test_massless_flat_flrw_closes_every_declared_equation() -> None:
    kappa, t, t0, a0 = sp.symbols("kappa t t0 a0", positive=True)
    phi0 = sp.symbols("phi0", real=True)
    result = massless_scalar_flat_flrw(kappa, t, t0, a0, phi0)
    assert result.scale_factor == a0 * (t / t0) ** sp.Rational(1, 3)
    assert result.hubble_rate == 1 / (3 * t)
    assert result.energy_density == 1 / (3 * kappa * t**2)
    assert result.pressure == result.energy_density
    assert result.friedmann_residual == 0
    assert result.spatial_einstein_residual == 0
    assert result.scalar_equation_residual == 0
    assert result.continuity_residual == 0


def test_solution_curvature_and_singular_boundary_are_explicit() -> None:
    kappa, t, t0, a0 = sp.symbols("kappa t t0 a0", positive=True)
    phi0 = sp.symbols("phi0", real=True)
    result = massless_scalar_flat_flrw(kappa, t, t0, a0, phi0)
    assert result.ricci_scalar == -sp.Rational(2, 3) / t**2
    assert result.kretschmann_scalar == sp.Rational(20, 27) / t**4
    assert sp.limit(result.kretschmann_scalar, t, 0, dir="+") == sp.oo
    assert sp.limit(result.kretschmann_scalar, t, sp.oo) == 0


def test_scalar_branch_changes_field_not_geometry_or_stress() -> None:
    kappa, t, t0, a0 = sp.symbols("kappa t t0 a0", positive=True)
    phi0 = sp.symbols("phi0", real=True)
    positive = massless_scalar_flat_flrw(kappa, t, t0, a0, phi0, branch=1)
    negative = massless_scalar_flat_flrw(kappa, t, t0, a0, phi0, branch=-1)
    assert negative.scalar_velocity == -positive.scalar_velocity
    assert negative.energy_density == positive.energy_density
    assert negative.scale_factor == positive.scale_factor
    assert negative.ricci_scalar == positive.ricci_scalar


def test_one_third_scale_exponent_is_load_bearing() -> None:
    kappa, t = sp.symbols("kappa t", positive=True)
    scalar_velocity = sp.sqrt(sp.Rational(2, 3) / kappa) / t
    density = scalar_velocity**2 / 2

    def friedmann_residual(exponent: sp.Expr) -> sp.Expr:
        return sp.simplify(3 * (exponent / t) ** 2 - kappa * density)

    assert friedmann_residual(sp.Rational(1, 3)) == 0
    assert friedmann_residual(sp.Rational(1, 2)) != 0
    assert friedmann_residual(sp.Rational(2, 3)) != 0
    assert friedmann_residual(sp.Integer(0)) != 0


def test_constant_scalar_flat_space_is_the_zero_potential_vacuum_limit() -> None:
    phi0 = sp.symbols("phi0", real=True)
    result = minimally_coupled_scalar_stress(
        sp.diag(-1, 1, 1, 1), [0, 0, 0, 0], 0
    )
    assert result.covariant == sp.zeros(4)
    assert result.trace == 0
    assert phi0.is_real is True


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        ((0, sp.Symbol("t", positive=True), 1, 1, 0), "gravitational_coupling"),
        ((-1, sp.Symbol("t", positive=True), 1, 1, 0), "gravitational_coupling"),
        ((1.0, sp.Symbol("t", positive=True), 1, 1, 0), "gravitational_coupling"),
        ((1, 1.0, 1, 1, 0), "time"),
        ((1, 1, 1, 1, 0), "time"),
        ((1, sp.Symbol("t", positive=True), 0, 1, 0), "reference_time"),
        ((1, sp.Symbol("t", positive=True), 1, -1, 0), "reference_scale_factor"),
    ],
)
def test_flrw_input_guards(arguments: tuple[object, ...], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        massless_scalar_flat_flrw(*arguments)


def test_branch_and_stress_input_guards() -> None:
    t = sp.symbols("t", positive=True)
    with pytest.raises(ValueError, match="branch"):
        massless_scalar_flat_flrw(1, t, 1, 1, 0, branch=0)
    with pytest.raises(ValueError, match="symmetric"):
        minimally_coupled_scalar_stress(
            [[-1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            [1, 0, 0, 0],
            0,
        )
    with pytest.raises(ValueError, match="invertible"):
        minimally_coupled_scalar_stress(sp.zeros(4), [1, 0, 0, 0], 0)
    with pytest.raises(ValueError, match="kinetic_coefficient"):
        minimally_coupled_scalar_stress(
            sp.diag(-1, 1, 1, 1),
            [1, 0, 0, 0],
            0,
            kinetic_coefficient=0,
        )
