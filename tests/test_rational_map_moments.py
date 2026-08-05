from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import sympy as sp

import substrate_framework as sf
from substrate_framework.numerics import SolverTolerances
from substrate_framework.rational_map_moments import (
    degree_one_rational_map_angular_stf_moments,
    degree_two_axial_rational_map_angular_stf_moments,
    degree_two_profile_intrinsic_moments,
    factorized_rational_map_energy_moments,
    rational_map_local_energy_density,
)
from substrate_framework.rational_map_radial import (
    rational_map_radial_energy_density,
    solve_rational_map_radial_profile,
)
from substrate_framework.rational_maps import axial_rational_map_angular_integral


def test_rational_map_moment_public_api_is_exported() -> None:
    assert sf.degree_two_profile_intrinsic_moments is degree_two_profile_intrinsic_moments
    assert sf.rational_map_local_energy_density is rational_map_local_energy_density


def test_local_density_reduces_exactly_to_the_accepted_radial_functional() -> None:
    field, derivative = sp.symbols("f fp", real=True)
    radius, jacobian, degree, angular = sp.symbols("r J B I", positive=True)
    local = rational_map_local_energy_density(field, derivative, radius, jacobian)
    polynomial = sp.Poly(sp.expand(radius**2 * local), jacobian)
    averaged_volume_density = (
        polynomial.coeff_monomial(1)
        + degree * polynomial.coeff_monomial(jacobian)
        + angular * polynomial.coeff_monomial(jacobian**2)
    )
    accepted = rational_map_radial_energy_density(
        field,
        derivative,
        radius,
        degree,
        angular,
    )
    assert sp.simplify(averaged_volume_density - accepted) == 0


def test_degree_one_angular_density_has_an_exact_STF_null() -> None:
    angular = degree_one_rational_map_angular_stf_moments()
    assert angular.normalized_mean == 1
    assert angular.normalized_squared_mean == 1
    assert angular.linear_stf == sp.zeros(3)
    assert angular.quadratic_stf == sp.zeros(3)
    factored = factorized_rational_map_energy_moments(
        angular,
        isotropic_monopole_radial=1,
        linear_monopole_radial=2,
        quadratic_monopole_radial=3,
        linear_second_radial=5,
        quadratic_second_radial=7,
    )
    assert factored.normalized_stf == sp.zeros(3)
    assert factored.triple_normalized_quadrupole == sp.zeros(3)


def test_degree_two_angular_coefficients_are_exactly_rederived() -> None:
    angular = degree_two_axial_rational_map_angular_stf_moments()
    u = next(iter(angular.conformal_jacobian.free_symbols))
    jacobian = angular.conformal_jacobian
    assert sp.simplify(sp.integrate(jacobian, (u, -1, 1)) / 2) == 2
    assert sp.simplify(
        sp.integrate(jacobian**2, (u, -1, 1)) / 2
        - (sp.pi + sp.Rational(8, 3))
    ) == 0
    linear_zz = sp.simplify(
        2 * sp.pi * sp.integrate(jacobian * (u**2 - sp.Rational(1, 3)), (u, -1, 1))
    )
    quadratic_zz = sp.simplify(
        2
        * sp.pi
        * sp.integrate(jacobian**2 * (u**2 - sp.Rational(1, 3)), (u, -1, 1))
    )
    assert linear_zz == angular.linear_stf[2, 2]
    assert quadratic_zz == angular.quadratic_stf[2, 2]
    assert linear_zz.is_negative is True
    assert quadratic_zz.is_negative is True
    assert sp.simplify(sp.trace(angular.linear_stf)) == 0
    assert sp.simplify(sp.trace(angular.quadratic_stf)) == 0


def test_degree_two_factorization_fixes_axial_form_sign_and_convention() -> None:
    angular = degree_two_axial_rational_map_angular_stf_moments()
    h1, h2 = sp.symbols("H1 H2", positive=True)
    factored = factorized_rational_map_energy_moments(
        angular,
        isotropic_monopole_radial=1,
        linear_monopole_radial=1,
        quadratic_monopole_radial=1,
        linear_second_radial=h1,
        quadratic_second_radial=h2,
    )
    normalized = factored.normalized_stf
    assert sp.simplify(normalized[0, 0] - normalized[1, 1]) == 0
    assert sp.simplify(normalized[0, 0] + normalized[2, 2] / 2) == 0
    assert normalized[2, 2].is_negative is True
    assert normalized[0, 0].is_positive is True
    assert normalized == sp.diag(*normalized.diagonal())
    assert sp.simplify(
        factored.triple_normalized_quadrupole - 3 * normalized
    ) == sp.zeros(3)


@pytest.fixture(scope="module")
def degree_two_profile() -> object:
    return solve_rational_map_radial_profile(
        2,
        float(axial_rational_map_angular_integral(2)),
        outer_radius=24.0,
        sample_points=1201,
        tolerances=SolverTolerances(rtol=3e-10, atol=3e-12, max_step=0.05),
    )


def test_corrected_degree_two_profile_has_a_nonzero_oblate_intrinsic_moment(
    degree_two_profile: object,
) -> None:
    evidence = degree_two_profile_intrinsic_moments(degree_two_profile)
    assert np.all(np.isfinite(evidence.normalized_stf))
    assert np.trace(evidence.normalized_stf) == pytest.approx(0.0, abs=2e-13)
    assert evidence.normalized_stf[2, 2] < 0 < evidence.normalized_stf[0, 0]
    assert evidence.normalized_stf[0, 0] == pytest.approx(
        evidence.normalized_stf[1, 1],
        rel=2e-15,
    )
    assert evidence.normalized_axial_ratio < -0.1
    assert evidence.triple_axial_ratio == pytest.approx(
        3 * evidence.normalized_axial_ratio,
        rel=2e-15,
    )
    assert evidence.profile_energy_closure_relative_error < 2e-12


def test_degree_two_profile_rejects_wrong_degree() -> None:
    wrong = solve_rational_map_radial_profile(
        1,
        1.0,
        outer_radius=16.0,
        sample_points=401,
        tolerances=SolverTolerances(rtol=1e-8, atol=1e-10, max_step=0.1),
    )
    with pytest.raises(ValueError, match="degree two"):
        degree_two_profile_intrinsic_moments(wrong)


def test_canonical_moment_module_uses_only_shared_trapezoidal_integration() -> None:
    source = Path("src/substrate_framework/rational_map_moments.py").read_text(
        encoding="utf-8"
    )
    assert "np.tr" + "apz" not in source
    assert "np.tr" + "apezoid" not in source
    assert "trapezoid_integral" in source
