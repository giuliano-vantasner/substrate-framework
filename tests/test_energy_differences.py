from __future__ import annotations

import math

import pytest

import substrate_framework as sf
from substrate_framework.energy_differences import (
    LinearDifferenceInterval,
    linear_difference_coefficient,
    linear_difference_interval,
    linear_energy_difference,
    normalized_linear_difference,
)


def test_energy_difference_api_is_package_exported() -> None:
    assert sf.LinearDifferenceInterval is LinearDifferenceInterval
    assert sf.linear_difference_coefficient is linear_difference_coefficient
    assert sf.linear_difference_interval is linear_difference_interval
    assert sf.linear_energy_difference is linear_energy_difference
    assert sf.normalized_linear_difference is normalized_linear_difference


def test_normalized_difference_preserves_sign_and_zero_surface() -> None:
    assert normalized_linear_difference(2.0, 3.0, multiplicity=2) == 1.0
    assert normalized_linear_difference(2.0, 4.0, multiplicity=2) == 0.0
    assert normalized_linear_difference(2.0, 5.0, multiplicity=2) == -1.0


def test_declared_normalization_and_scale_are_both_load_bearing() -> None:
    coefficient = linear_difference_coefficient(
        2.5,
        4.0,
        multiplicity=2,
        normalization=3.0,
    )
    assert coefficient == 3.0
    assert linear_energy_difference(
        2.5,
        4.0,
        multiplicity=2,
        normalization=3.0,
        energy_scale=7.0,
    ) == 21.0
    assert linear_difference_coefficient(
        2.5,
        4.0,
        multiplicity=3,
        normalization=3.0,
    ) != coefficient
    assert linear_difference_coefficient(
        2.5,
        4.0,
        multiplicity=2,
        normalization=4.0,
    ) != coefficient


def test_accepted_p105_values_give_corrected_conditional_coefficient() -> None:
    coefficient = linear_difference_coefficient(
        2.4162704269425106,
        4.54605799958882,
        multiplicity=2,
        normalization=3.0 * math.pi**2,
    )
    assert coefficient == pytest.approx(8.482417318795287, rel=2.0e-15)


def test_two_method_rectangular_envelope_is_monotone_and_contains_both() -> None:
    b2_values = (2.4162704269425106, 2.41627038555235)
    b4_values = (4.54605799958882, 4.546057999552492)
    envelope = linear_difference_interval(
        (min(b2_values), max(b2_values)),
        (min(b4_values), max(b4_values)),
        multiplicity=2,
        normalization=3.0 * math.pi**2,
    )
    coefficients = [
        linear_difference_coefficient(
            b2,
            b4,
            multiplicity=2,
            normalization=3.0 * math.pi**2,
        )
        for b2, b4 in zip(b2_values, b4_values, strict=True)
    ]
    assert envelope.lower == pytest.approx(8.48241486776822, rel=2.0e-15)
    assert envelope.upper == pytest.approx(8.482417319870916, rel=2.0e-15)
    assert envelope.width < 3.0e-6
    assert all(envelope.contains(value) for value in coefficients)
    assert envelope.lower > 0.0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: normalized_linear_difference(1.0, 1.0, multiplicity=0),
            "positive integer",
        ),
        (
            lambda: normalized_linear_difference(1.0, 1.0, multiplicity=1.5),
            "positive integer",
        ),
        (
            lambda: linear_difference_coefficient(
                1.0,
                1.0,
                multiplicity=1,
                normalization=0.0,
            ),
            "positive",
        ),
        (
            lambda: linear_energy_difference(
                1.0,
                1.0,
                multiplicity=1,
                normalization=1.0,
                energy_scale=float("inf"),
            ),
            "finite",
        ),
        (
            lambda: linear_difference_interval(
                (2.0, 1.0),
                (0.0, 1.0),
                multiplicity=1,
                normalization=1.0,
            ),
            "must not exceed",
        ),
    ],
)
def test_invalid_linear_difference_inputs_fail_explicitly(call, message: str) -> None:
    with pytest.raises((TypeError, ValueError), match=message):
        call()
