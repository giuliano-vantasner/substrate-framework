import numpy as np
import pytest
import sympy as sp

from substrate_framework.numerics import NumericalFailure
from substrate_framework.radial_qball import (
    LOCALIZATION_FREQUENCY_LIMIT,
    fit_radial_tail_rate,
    radial_profile_force,
    radial_qball_observables,
    radial_qball_rhs,
    radial_tail_rate,
    regular_origin_state,
    shoot_radial_qball,
    shooting_observables,
    smooth_complex_potential,
    smooth_complex_potential_derivative,
    solve_radial_qball_bvp,
    symbolic_radial_charge_density,
    symbolic_radial_energy_density,
    symbolic_radial_profile_residual,
    symbolic_radial_reduced_lagrangian,
)


@pytest.fixture(scope="module")
def branch():
    return solve_radial_qball_bvp(
        frequency=0.5,
        outer_radius=20.0,
        initial_mesh_points=1001,
        tolerance=1.0e-6,
    )


def test_exact_potential_series_derivative_and_radial_equation() -> None:
    rho, radius, omega = sp.symbols("rho radius omega", positive=True)
    profile = sp.Function("f")(radius)
    assert sp.series(smooth_complex_potential(rho), rho, 0, 4) == (
        rho / 2 - rho**2 / 24 + rho**3 / 720 + sp.Order(rho**4)
    )
    assert smooth_complex_potential_derivative(sp.Integer(0)) == sp.Rational(1, 2)
    expected = (
        sp.diff(profile, radius, 2)
        + 2 * sp.diff(profile, radius) / radius
        - sp.sin(profile) / 2
        + omega**2 * profile
    )
    assert sp.simplify(
        symbolic_radial_profile_residual(radius, profile, omega) - expected
    ) == 0
    lagrangian = symbolic_radial_reduced_lagrangian(radius, profile, omega)
    variation = sp.diff(sp.diff(lagrangian, sp.diff(profile, radius)), radius) - sp.diff(
        lagrangian, profile
    )
    assert sp.simplify(variation / (-2 * radius**2) - expected) == 0
    assert symbolic_radial_energy_density(radius, profile, omega) == radius**2 * (
        omega**2 * profile**2
        + sp.diff(profile, radius) ** 2
        - sp.cos(profile)
        + 1
    )
    assert symbolic_radial_charge_density(radius, profile, omega) == (
        2 * omega * radius**2 * profile**2
    )


def test_frequency_domain_origin_series_and_rhs() -> None:
    assert radial_tail_rate(0.5) == pytest.approx(0.5)
    with pytest.raises(ValueError):
        radial_tail_rate(LOCALIZATION_FREQUENCY_LIMIT)
    state = regular_origin_state(6.0, 0.5, 1.0e-4)
    force = float(radial_profile_force(6.0, 0.5))
    assert state[0] == pytest.approx(6.0 + force * 1.0e-8 / 6.0)
    assert state[1] == pytest.approx(force * 1.0e-4 / 3.0)
    rhs = radial_qball_rhs(1.0, np.asarray([1.0, -0.2]), 0.5)
    assert rhs == pytest.approx([-0.2, 0.5 * np.sin(1.0) - 0.25 + 0.4])


def test_bvp_is_nontrivial_regular_nodeless_monotone_and_virial_closed(branch) -> None:
    assert branch.central_amplitude == pytest.approx(6.1066789, rel=2.0e-7)
    assert branch.maximum_boundary_residual < 1.0e-10
    assert branch.evidence.max_rms_residual < 1.0e-6
    radius = np.linspace(branch.origin_epsilon, 19.0, 4001)
    amplitude, derivative = branch.state_at(radius)
    assert np.all(amplitude > 0.0)
    assert np.all(derivative < 0.0)
    observables = radial_qball_observables(branch)
    assert observables.energy == pytest.approx(2990.2493, rel=2.0e-6)
    assert observables.noether_charge == pytest.approx(4721.0179, rel=2.0e-6)
    assert observables.normalized_pohozaev_residual < 2.0e-6
    assert fit_radial_tail_rate(branch, fit_start=8.0, fit_stop=16.0) == pytest.approx(
        radial_tail_rate(0.5), rel=5.0e-3
    )


def test_trivial_collocation_branch_is_explicitly_rejected() -> None:
    with pytest.raises(NumericalFailure, match="trivial branch"):
        solve_radial_qball_bvp(
            frequency=0.5,
            outer_radius=10.0,
            initial_mesh_points=101,
            tolerance=1.0e-5,
            central_guess=1.0e-10,
            minimum_central_amplitude=1.0e-3,
        )


def test_independent_shooting_agrees_with_collocation(branch) -> None:
    shooting = shoot_radial_qball(
        frequency=0.5,
        central_bracket=(6.1, 6.125),
        outer_radius=20.0,
        sample_points=4001,
    )
    assert shooting.root_converged
    assert abs(shooting.robin_residual) < 1.0e-8
    assert shooting.central_amplitude == pytest.approx(branch.central_amplitude, rel=2.0e-6)
    assert np.all(shooting.ivp.state[0] > 0.0)
    assert np.all(shooting.ivp.state[1] < 0.0)
    collocation = radial_qball_observables(branch)
    independent = shooting_observables(shooting)
    assert independent.energy == pytest.approx(collocation.energy, rel=2.0e-6)
    assert independent.noether_charge == pytest.approx(
        collocation.noether_charge, rel=2.0e-6
    )
