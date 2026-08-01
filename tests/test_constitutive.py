from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.constitutive import (
    co_scaled_inverse_permeability,
    co_scaled_permittivity,
    co_scaled_wave_speed,
    local_wave_speed,
)


def test_co_scaled_responses_cancel_from_wave_speed() -> None:
    density, thermal, speed = sp.symbols("rho Theta c", positive=True)
    epsilon = co_scaled_permittivity(density, thermal, speed)
    inverse_mu = co_scaled_inverse_permeability(density, thermal)
    assert sp.simplify(epsilon / inverse_mu - 1 / speed**2) == 0
    assert co_scaled_wave_speed(density, thermal, speed) == speed


def test_local_wave_speed_uses_inverse_permeability() -> None:
    assert local_wave_speed(sp.Rational(2, 9), 2) == 3


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: co_scaled_permittivity(0, 1, 1), "density"),
        (lambda: co_scaled_inverse_permeability(1, -1), "thermal_scale"),
        (lambda: co_scaled_wave_speed(1, 1, 0), "reference_speed"),
        (lambda: local_wave_speed(-1, 1), "permittivity"),
    ],
)
def test_numeric_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
