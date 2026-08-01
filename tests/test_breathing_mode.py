from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.separable_moments import (
    axisymmetric_separable_stf_derivative,
    axisymmetric_stf_tt_readout,
)
from substrate_framework.sine_gordon import (
    breather_energy_second_moment,
    breather_energy_second_moment_derivative,
)
from substrate_framework.tt_angular import (
    conditional_tt_power,
    frobenius_norm_squared,
)


def test_exact_breather_moment_derivative_api() -> None:
    omega = sp.symbols("omega", positive=True, real=True)
    time = sp.symbols("t", real=True)
    moment = breather_energy_second_moment(omega, time)
    for order in range(4):
        derivative = breather_energy_second_moment_derivative(omega, time, order)
        assert sp.simplify(derivative - sp.diff(moment, time, order)) == 0
    with pytest.raises(ValueError):
        breather_energy_second_moment_derivative(omega, time, -1)
    with pytest.raises(ValueError):
        breather_energy_second_moment_derivative(omega, time, 1.5)


def test_third_derivative_symmetry_zeros_and_nonzero_phase() -> None:
    omega = sp.sqrt(2) / 2
    time = sp.symbols("t", real=True)
    third = breather_energy_second_moment_derivative(omega, time, 3)
    period = sp.pi / omega
    assert sp.simplify(third.subs(time, -time) + third) == 0
    assert sp.simplify(third.subs(time, time + period) - third) == 0
    assert third.subs(time, 0) == 0
    assert sp.simplify(third.subs(time, period / 2)) == 0
    assert sp.simplify(third.subs(time, period / 4) + sp.Rational(64, 3)) == 0


def test_normalized_and_triple_conditional_power_are_convention_invariant() -> None:
    derivative, coupling = sp.symbols("d G", positive=True, real=True)
    normalized = axisymmetric_separable_stf_derivative(derivative)
    triple = axisymmetric_separable_stf_derivative(derivative, 3)
    flux_prefactor = 1 / (32 * sp.pi * coupling)
    normalized_power = conditional_tt_power(normalized, 2 * coupling, flux_prefactor)
    triple_power = conditional_tt_power(triple, 2 * coupling / 3, flux_prefactor)
    assert sp.simplify(frobenius_norm_squared(normalized) - 2 * derivative**2 / 3) == 0
    assert sp.simplify(frobenius_norm_squared(triple) - 6 * derivative**2) == 0
    assert sp.simplify(normalized_power - 2 * coupling * derivative**2 / 15) == 0
    assert sp.simplify(triple_power - normalized_power) == 0
    assert sp.simplify(
        conditional_tt_power(triple, 2 * coupling, flux_prefactor)
        - 9 * normalized_power
    ) == 0


def test_axisymmetric_readout_has_sine_squared_pattern_and_no_cross() -> None:
    derivative = sp.symbols("d", real=True)
    inclination = sp.symbols("i", real=True)
    readout = axisymmetric_stf_tt_readout(derivative, inclination)
    assert sp.trigsimp(
        readout.normalized_plus_coordinate
        - derivative * sp.sin(inclination) ** 2 / sp.sqrt(2)
    ) == 0
    assert readout.normalized_cross_coordinate == 0
    assert sp.trigsimp(
        readout.conventional_plus_readout
        - derivative * sp.sin(inclination) ** 2 / 2
    ) == 0
    assert readout.conventional_cross_readout == 0
    assert axisymmetric_stf_tt_readout(derivative, 0).projected_tensor == sp.zeros(3)
    assert axisymmetric_stf_tt_readout(
        derivative,
        sp.pi / 2,
    ).projected_tensor == sp.diag(derivative / 2, -derivative / 2, 0)
