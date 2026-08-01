from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.quartic_qball import (
    quartic_qball_amplitude,
    quartic_qball_charge,
    quartic_qball_charge_derivative,
    quartic_qball_inverse_width,
    quartic_qball_profile,
    quartic_qball_residual,
)
from substrate_framework.u1_charge import stationary_u1_charge_density


def test_exact_profile_solves_declared_quartic_ode() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    profile = quartic_qball_profile(coordinate, frequency)
    assert sp.simplify(
        sp.expand_trig(quartic_qball_residual(profile, coordinate, frequency))
    ) == 0


def test_nonzero_sech_ansatz_forces_width_and_amplitude_coefficients() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency, inverse_width, amplitude = sp.symbols(
        "omega kappa A", positive=True
    )
    profile = amplitude * sp.sech(inverse_width * coordinate)
    shape_square = sp.symbols("s2")
    reduced = sp.simplify(
        quartic_qball_residual(profile, coordinate, frequency)
        / (amplitude * sp.sech(inverse_width * coordinate))
    ).subs(
        sp.cosh(inverse_width * coordinate) ** -2, shape_square
    ).subs(
        sp.sech(inverse_width * coordinate) ** 2, shape_square
    )
    coefficient_one = sp.expand(reduced).coeff(shape_square, 0)
    coefficient_three = sp.expand(reduced).coeff(shape_square, 1)
    assert coefficient_one == inverse_width**2 + frequency**2 - sp.Rational(1, 2)
    assert coefficient_three == amplitude**2 / 12 - 2 * inverse_width**2
    assert sp.solve(
        [coefficient_one, coefficient_three],
        [inverse_width**2, amplitude**2],
        dict=True,
    ) == [{
        inverse_width**2: sp.Rational(1, 2) - frequency**2,
        amplitude**2: 12 - 24 * frequency**2,
    }]


def test_profile_center_localization_and_first_integral() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency = sp.Rational(1, 2)
    center = sp.Rational(3, 2)
    profile = quartic_qball_profile(coordinate, frequency, center)
    kappa = quartic_qball_inverse_width(frequency)
    assert kappa == sp.Rational(1, 2)
    assert profile.subs(coordinate, center) == quartic_qball_amplitude(frequency)
    assert sp.diff(profile, coordinate).subs(coordinate, center) == 0
    assert sp.limit(profile, coordinate, sp.oo) == 0
    assert sp.limit(profile, coordinate, -sp.oo) == 0
    first_integral = (
        sp.diff(profile, coordinate) ** 2
        - kappa**2 * profile**2
        + profile**4 / 24
    )
    argument = (coordinate - center) / 2
    assert sp.simplify(
        first_integral.subs(
            sp.tanh(argument) ** 2, 1 - sp.sech(argument) ** 2
        )
    ) == 0


def test_charge_is_accepted_current_integral() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency = sp.symbols("omega", positive=True)
    profile = quartic_qball_profile(coordinate, frequency)
    density = stationary_u1_charge_density(profile, frequency)
    scaled_coordinate = sp.symbols("u", real=True)
    kappa = quartic_qball_inverse_width(frequency)
    scaled_density = sp.simplify(
        density.subs(coordinate, scaled_coordinate / kappa) / kappa
    ).subs(
        sp.sech(scaled_coordinate) ** 2,
        sp.cosh(scaled_coordinate) ** -2,
    )
    integrated = sp.integrate(
        scaled_density, (scaled_coordinate, -sp.oo, sp.oo)
    )
    assert sp.simplify(integrated - quartic_qball_charge(frequency)) == 0
    assert sp.simplify(
        quartic_qball_charge(frequency)
        - 96 * frequency * sp.sqrt(sp.Rational(1, 2) - frequency**2)
    ) == 0


def test_charge_endpoints_maximum_and_slope_branches() -> None:
    frequency = sp.symbols("omega", positive=True)
    charge = quartic_qball_charge(frequency)
    slope = quartic_qball_charge_derivative(frequency)
    assert sp.limit(charge, frequency, 0, dir="+") == 0
    assert sp.limit(charge, frequency, sp.sqrt(sp.Rational(1, 2)), dir="-") == 0
    assert quartic_qball_charge(sp.Rational(1, 2)) == 24
    assert quartic_qball_charge_derivative(sp.Rational(1, 4)) > 0
    assert quartic_qball_charge_derivative(sp.Rational(1, 2)) == 0
    assert quartic_qball_charge_derivative(sp.Rational(3, 5)) < 0
    assert sp.simplify(slope - sp.diff(charge, frequency)) == 0


def test_wrong_width_amplitude_and_profile_fail_the_equation() -> None:
    coordinate = sp.symbols("x", real=True)
    frequency = sp.Rational(1, 2)
    correct = quartic_qball_profile(coordinate, frequency)
    wrong_width = quartic_qball_amplitude(frequency) * sp.sech(
        sp.sqrt(1 - frequency**2) * coordinate
    )
    gaussian = quartic_qball_amplitude(frequency) * sp.exp(-coordinate**2 / 4)
    for mutation in (correct / 2, wrong_width, gaussian):
        residual = quartic_qball_residual(mutation, coordinate, frequency)
        assert sp.simplify(residual.subs(coordinate, 0)) != 0


@pytest.mark.parametrize(
    "frequency", [0, -sp.Rational(1, 3), sp.sqrt(sp.Rational(1, 2)), 1, sp.I]
)
def test_frequency_domain_is_open_and_real(frequency) -> None:
    with pytest.raises(ValueError, match="omega"):
        quartic_qball_profile(0, frequency)
