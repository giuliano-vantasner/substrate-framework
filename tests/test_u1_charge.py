from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.u1_charge import (
    breather_charge_energy_product,
    breather_charge_secant_product,
    breather_parameterized_u1_charge,
    charge_scale_exponent_matrix,
    sech_profile_u1_charge,
    stationary_phase_field,
    u1_current_components,
)


def test_stationary_profile_current_and_charge_are_exact() -> None:
    x, t = sp.symbols("x t", real=True)
    omega = sp.Rational(3, 5)
    amplitude = sp.Rational(2, 3)
    eta = sp.Rational(4, 5)
    profile = amplitude / sp.cosh(eta * x)
    field = stationary_phase_field(profile, t, omega)
    conjugate = profile * sp.exp(sp.I * omega * t)
    density, flux = u1_current_components(field, conjugate, x, t)
    assert sp.simplify(density - 2 * omega * profile**2) == 0
    assert flux == 0
    assert sech_profile_u1_charge(omega, eta, amplitude) == sp.Rational(4, 3)


def test_breather_parameterized_charge_products_retain_amplitude() -> None:
    omega = sp.Rational(3, 5)
    amplitude = sp.Rational(2, 3)
    assert breather_parameterized_u1_charge(omega, amplitude) == sp.Rational(4, 3)
    assert breather_charge_energy_product(omega, amplitude) == sp.Rational(256, 15)
    assert breather_charge_secant_product(omega, amplitude) == sp.Rational(256, 9)


def test_charge_scale_exponent_kernel_has_two_generators() -> None:
    matrix = charge_scale_exponent_matrix()
    generators = (
        sp.Matrix([1, 1, 0, 0]),
        sp.Matrix([1, 0, 1, -1]),
    )
    assert matrix.rank() == 2
    assert all(matrix * generator == sp.zeros(2, 1) for generator in generators)
    assert sp.Matrix.hstack(*generators).rank() == 2


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: sech_profile_u1_charge(0, 1), "frequency"),
        (lambda: sech_profile_u1_charge(1, 0), "inverse_width"),
        (lambda: sech_profile_u1_charge(1, 1, 0), "amplitude"),
        (lambda: breather_parameterized_u1_charge(1), "0 < omega < 1"),
    ],
)
def test_numeric_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
