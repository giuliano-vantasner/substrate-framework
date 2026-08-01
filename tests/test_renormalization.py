from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.renormalization import (
    one_loop_inverse_coupling_squared,
    one_loop_transmutation_scale,
    transmuted_mass_coordinate,
)


def test_one_loop_inverse_coupling_has_boundary_and_flow() -> None:
    scale, reference, coupling, coefficient = sp.symbols(
        "mu mu0 g0 b0", positive=True
    )
    inverse = one_loop_inverse_coupling_squared(
        scale, reference, coupling, coefficient
    )
    assert inverse.subs(scale, reference) == 1 / coupling**2
    assert sp.simplify(scale * sp.diff(inverse, scale)) == coefficient / (
        8 * sp.pi**2
    )


def test_transmutation_scale_is_inverse_coupling_zero() -> None:
    reference, coupling, coefficient = sp.symbols("mu0 g0 b0", positive=True)
    invariant = one_loop_transmutation_scale(reference, coupling, coefficient)
    assert (
        sp.simplify(
            one_loop_inverse_coupling_squared(
                invariant, reference, coupling, coefficient
            )
        )
        == 0
    )


def test_transmuted_mass_coordinate_retains_all_dimensionless_inputs() -> None:
    coupling_squared, coefficient, ratio = sp.symbols("beta2 b0 q", positive=True)
    coordinate = transmuted_mass_coordinate(
        coupling_squared, coefficient, ratio
    )
    assert coordinate == ratio * sp.exp(
        -8 * sp.pi**2 / (coefficient * coupling_squared)
    )
    assert sp.diff(coordinate, ratio) != 0
    assert sp.diff(coordinate, coupling_squared) != 0
    assert sp.diff(coordinate, coefficient) != 0


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: one_loop_inverse_coupling_squared(0, 1, 1, 1), "scale"),
        (
            lambda: one_loop_inverse_coupling_squared(1, 0, 1, 1),
            "reference_scale",
        ),
        (
            lambda: one_loop_inverse_coupling_squared(1, 1, 0, 1),
            "reference_coupling",
        ),
        (
            lambda: one_loop_inverse_coupling_squared(1, 1, 1, 0),
            "beta_coefficient",
        ),
        (lambda: one_loop_transmutation_scale(0, 1, 1), "reference_scale"),
        (lambda: one_loop_transmutation_scale(1, 0, 1), "reference_coupling"),
        (lambda: one_loop_transmutation_scale(1, 1, 0), "beta_coefficient"),
        (lambda: transmuted_mass_coordinate(0, 1, 1), "coupling_squared"),
        (lambda: transmuted_mass_coordinate(1, 0, 1), "beta_coefficient"),
        (lambda: transmuted_mass_coordinate(1, 1, 0), "mass_energy_ratio"),
    ],
)
def test_positive_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
