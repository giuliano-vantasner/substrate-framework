from __future__ import annotations

import numpy as np
import pytest
import sympy as sp

from substrate_framework.abelian_higgs_vortex import (
    VortexParameters,
    angular_log_coefficient,
    asymptotic_masses,
    euler_lagrange_residuals,
    quantized_flux,
    radial_energy_lagrangian,
    solve_vortex_bvp,
    vortex_boundary_residual,
    vortex_energy_density,
    vortex_tension,
)


def test_radial_functional_varies_to_general_coupling_equations() -> None:
    radius = sp.symbols("r", positive=True)
    winding = sp.symbols("n", integer=True, positive=True)
    coupling, lam, vacuum = sp.symbols("g lambda v", positive=True)
    scalar = sp.Function("f")(radius)
    gauge = sp.Function("a")(radius)
    lagrangian = radial_energy_lagrangian(
        radius, scalar, gauge, winding, lam, vacuum, coupling
    )
    scalar_variation = sp.simplify(
        (
            sp.diff(sp.diff(lagrangian, sp.diff(scalar, radius)), radius)
            - sp.diff(lagrangian, scalar)
        )
        / radius
    )
    gauge_variation = sp.simplify(
        coupling**2
        * radius
        * (
            sp.diff(sp.diff(lagrangian, sp.diff(gauge, radius)), radius)
            - sp.diff(lagrangian, gauge)
        )
    )
    expected_scalar, expected_gauge = euler_lagrange_residuals(
        radius, scalar, gauge, winding, lam, vacuum, coupling
    )
    assert sp.simplify(scalar_variation - expected_scalar) == 0
    assert sp.simplify(gauge_variation - expected_gauge) == 0


def test_finite_energy_boundary_flux_and_linearized_masses() -> None:
    winding = sp.symbols("n", integer=True, positive=True)
    vacuum, coupling, lam = sp.symbols("v g lambda", positive=True)
    asymptotic = sp.symbols("a_infinity", real=True)
    coefficient = angular_log_coefficient(vacuum, winding, asymptotic)
    assert sp.solve(sp.Eq(coefficient, 0), asymptotic) == [winding]
    assert angular_log_coefficient(vacuum, winding, 0) == vacuum**2 * winding**2
    assert quantized_flux(winding, coupling) == 2 * sp.pi * winding / coupling
    assert asymptotic_masses(vacuum, lam, coupling) == (
        coupling * vacuum,
        vacuum * sp.sqrt(2 * lam),
    )


def test_numeric_vortex_smoke_retains_solver_and_energy_evidence() -> None:
    parameters = VortexParameters()
    solution = solve_vortex_bvp(
        parameters,
        outer_radius=10.0,
        initial_points=80,
        tolerance=1.0e-5,
    )
    assert solution.evidence.max_rms_residual < 1.1e-5
    residual = vortex_boundary_residual(
        solution.evidence.state[:, 0], solution.evidence.state[:, -1], parameters
    )
    assert np.max(np.abs(residual)) < 1.0e-10
    density = vortex_energy_density(
        solution.evidence.coordinate, solution.evidence.state, parameters
    )
    assert np.all(density >= 0.0)
    assert 4.20 < vortex_tension(solution, quadrature_points=5_001) < 4.23


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: VortexParameters(vacuum_scale=0), "vacuum_scale"),
        (lambda: VortexParameters(winding=0), "winding"),
        (lambda: VortexParameters(self_coupling=0), "self_coupling"),
        (lambda: VortexParameters(gauge_coupling=0), "gauge_coupling"),
        (lambda: quantized_flux(sp.Rational(1, 2), 1), "winding"),
        (lambda: solve_vortex_bvp(inner_radius=0), "inner_radius"),
        (
            lambda: solve_vortex_bvp(inner_radius=2, outer_radius=1),
            "outer_radius",
        ),
        (lambda: solve_vortex_bvp(initial_points=4), "initial_points"),
    ],
)
def test_invalid_domains_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
