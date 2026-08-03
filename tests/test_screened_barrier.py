from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.screened_barrier import (
    inverse_sqrt_barrier_enhancement,
    inverse_sqrt_barrier_factor,
    shifted_barrier_ledger,
    shifted_inverse_sqrt_barrier_factor,
)


E, G, U = sp.symbols("E G U", positive=True)


def test_exact_factor_and_enhancement_composition() -> None:
    bare = inverse_sqrt_barrier_factor(E, G)
    shifted = shifted_inverse_sqrt_barrier_factor(E, G, U)
    enhancement = inverse_sqrt_barrier_enhancement(E, G, U)
    assert sp.simplify(bare * enhancement - shifted) == 0


def test_zero_shift_recovers_bare_factor_and_unit_enhancement() -> None:
    assert sp.simplify(shifted_inverse_sqrt_barrier_factor(E, G, 0) - inverse_sqrt_barrier_factor(E, G)) == 0
    assert inverse_sqrt_barrier_enhancement(E, G, 0) == 1


def test_exact_endpoint_limits() -> None:
    shifted = shifted_inverse_sqrt_barrier_factor(E, G, U)
    bare = inverse_sqrt_barrier_factor(E, G)
    enhancement = inverse_sqrt_barrier_enhancement(E, G, U)
    assert sp.limit(bare, E, 0, dir="+") == 0
    assert sp.simplify(sp.limit(shifted, E, 0, dir="+") - sp.exp(-sp.sqrt(G / U))) == 0
    assert sp.limit(enhancement, E, 0, dir="+") == sp.oo
    assert sp.limit(shifted, E, sp.oo) == 1
    assert sp.limit(enhancement, E, sp.oo) == 1


def test_log_derivatives_have_exact_signs() -> None:
    ledger = shifted_barrier_ledger(E, G, U)
    expected_positive = sp.sqrt(G) / (2 * (E + U) ** sp.Rational(3, 2))
    assert sp.simplify(ledger.log_energy_derivative - expected_positive) == 0
    assert sp.simplify(ledger.log_shift_derivative - expected_positive) == 0
    assert ledger.log_energy_derivative.is_positive is True
    assert ledger.log_shift_derivative.is_positive is True
    assert ledger.log_barrier_scale_derivative.is_negative is True


def test_enhancement_decreases_with_energy_for_positive_shift() -> None:
    enhancement = inverse_sqrt_barrier_enhancement(E, G, U)
    derivative = sp.simplify(sp.diff(sp.log(enhancement), E))
    x = sp.symbols("x", positive=True)
    decreasing_kernel = x ** -sp.Rational(3, 2)
    expected = sp.sqrt(G) / 2 * (
        decreasing_kernel.subs(x, E + U) - decreasing_kernel.subs(x, E)
    )
    assert sp.simplify(derivative - expected) == 0
    assert sp.diff(decreasing_kernel, x).is_negative is True


def test_common_energy_rescaling_is_invariant() -> None:
    rho = sp.symbols("rho", positive=True)
    original = shifted_inverse_sqrt_barrier_factor(E, G, U)
    rescaled = shifted_inverse_sqrt_barrier_factor(rho * E, rho * G, rho * U)
    assert sp.simplify(rescaled - original) == 0


def test_shift_ceiling_direction_is_upward() -> None:
    u_low, u_high = sp.symbols("u_low u_high", positive=True)
    low = shifted_inverse_sqrt_barrier_factor(2, 11, u_low)
    high = shifted_inverse_sqrt_barrier_factor(2, 11, u_high)
    assert float(low.subs(u_low, 1)) < float(high.subs(u_high, 3))


def test_direct_shifted_evaluation_avoids_separate_factor_singularity() -> None:
    tiny_energy = sp.Float("1e-100")
    shifted = shifted_inverse_sqrt_barrier_factor(tiny_energy, 1000, 1)
    direct_value = sp.N(shifted, 40)
    assert direct_value.is_finite is True
    assert direct_value > 0


@pytest.mark.parametrize(
    ("function", "arguments"),
    [
        (inverse_sqrt_barrier_factor, (0, 1)),
        (inverse_sqrt_barrier_factor, (1, 0)),
        (shifted_inverse_sqrt_barrier_factor, (1, 1, -1)),
        (shifted_inverse_sqrt_barrier_factor, (sp.I, 1, 0)),
    ],
)
def test_invalid_domains_are_rejected(function: object, arguments: tuple[object, ...]) -> None:
    with pytest.raises(ValueError):
        function(*arguments)  # type: ignore[operator]
