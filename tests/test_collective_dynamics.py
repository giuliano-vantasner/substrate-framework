from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.collective_dynamics import (
    optical_collective_acceleration,
    optical_collective_lagrangian,
    slow_optical_collective_acceleration,
    slow_optical_profile_width_correction,
    virial_scaling_exponents,
)
from substrate_framework.optical_geometry import slow_geodesic_acceleration_1d
from substrate_framework.variational import solve_euler_lagrange_acceleration


def test_optical_action_derives_exact_collective_acceleration() -> None:
    time = sp.symbols("t", real=True)
    coordinate = sp.Function("q", real=True)(time)
    index_function = sp.Function("n", positive=True)
    index = index_function(coordinate)
    signal_speed, energy_scale = sp.symbols("c0 E0", positive=True)
    lagrangian = optical_collective_lagrangian(
        coordinate, time, index, signal_speed, energy_scale
    )
    assert sp.simplify(
        solve_euler_lagrange_acceleration(lagrangian, coordinate, time)
        - optical_collective_acceleration(
            coordinate, time, index, signal_speed
        )
    ) == 0


def test_slow_limit_matches_accepted_optical_geometry() -> None:
    coordinate = sp.symbols("x", real=True)
    index = 1 + coordinate**2
    signal_speed = sp.symbols("c0", positive=True)
    assert sp.simplify(
        slow_optical_collective_acceleration(
            coordinate, index, signal_speed
        )
        - slow_geodesic_acceleration_1d(index, coordinate, signal_speed)
    ) == 0


def test_centered_profile_width_correction_is_second_acceleration_derivative() -> None:
    coordinate = sp.symbols("x", real=True)
    index = sp.Function("n", positive=True)(coordinate)
    signal_speed, variance = sp.symbols("c0 sigma2", positive=True)
    point_acceleration = slow_optical_collective_acceleration(
        coordinate, index, signal_speed
    )
    correction = slow_optical_profile_width_correction(
        coordinate, index, signal_speed, variance
    )
    assert sp.simplify(
        correction - variance * sp.diff(point_acceleration, coordinate, 2) / 2
    ) == 0


def test_profile_width_correction_has_third_derivative_weak_limit() -> None:
    coordinate, epsilon = sp.symbols("x epsilon", real=True)
    signal_speed, variance = sp.symbols("c0 sigma2", positive=True)
    shape = sp.Function("xi", real=True)(coordinate)
    correction = slow_optical_profile_width_correction(
        coordinate,
        1 + epsilon * shape,
        signal_speed,
        variance,
    )
    assert sp.simplify(
        sp.diff(correction, epsilon).subs(epsilon, 0)
        - signal_speed**2
        * variance
        * sp.diff(shape, coordinate, 3)
        / 4
    ) == 0


def test_profile_width_correction_respects_reflection_center() -> None:
    coordinate = sp.symbols("x", real=True)
    signal_speed, variance, curvature = sp.symbols(
        "c0 sigma2 beta", positive=True
    )
    correction = slow_optical_profile_width_correction(
        coordinate,
        1 + curvature * coordinate**2 / 2,
        signal_speed,
        variance,
    )
    assert sp.simplify(correction.subs(coordinate, 0)) == 0


def test_conditional_virial_exponents_select_option_c() -> None:
    assert virial_scaling_exponents(0, 1) == (
        sp.Rational(-1, 2),
        sp.Rational(-1, 2),
    )
    assert virial_scaling_exponents(1, 0) != (
        sp.Rational(-1, 2),
        sp.Rational(-1, 2),
    )
    assert virial_scaling_exponents(1, 1) != (
        sp.Rational(-1, 2),
        sp.Rational(-1, 2),
    )


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: optical_collective_lagrangian(
                sp.Function("q")(sp.symbols("t")),
                sp.symbols("t"),
                0,
                1,
                1,
            ),
            "index",
        ),
        (
            lambda: slow_optical_collective_acceleration(
                sp.symbols("x"), 1, -1
            ),
            "signal_speed",
        ),
        (
            lambda: slow_optical_profile_width_correction(
                sp.symbols("x"), 1, 1, -1
            ),
            "spatial_variance",
        ),
    ],
)
def test_numeric_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
