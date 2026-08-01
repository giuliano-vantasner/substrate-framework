from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.wilson_loops import (
    rectangular_area_law,
    rectangular_perimeter_law,
    static_potential_from_loop,
)


def test_declared_area_law_has_linear_static_potential() -> None:
    separation, duration, tension = sp.symbols("R T sigma", positive=True)
    loop = rectangular_area_law(separation, duration, tension)
    potential = static_potential_from_loop(loop, duration)
    assert potential == tension * separation
    assert sp.diff(potential, separation) == tension
    assert sp.diff(potential, separation, 2) == 0


def test_declared_perimeter_law_has_bounded_static_potential() -> None:
    separation, duration, coefficient = sp.symbols("R T rho", positive=True)
    loop = rectangular_perimeter_law(separation, duration, coefficient)
    potential = static_potential_from_loop(loop, duration)
    assert potential == 2 * coefficient
    assert sp.diff(potential, separation) == 0


def test_same_center_algebra_does_not_select_a_loop_law() -> None:
    separation, duration, tension, coefficient = sp.symbols(
        "R T sigma rho", positive=True
    )
    assert static_potential_from_loop(
        rectangular_area_law(separation, duration, tension), duration
    ) != static_potential_from_loop(
        rectangular_perimeter_law(separation, duration, coefficient), duration
    )


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: rectangular_area_law(0, 1, 1), "separation"),
        (lambda: rectangular_area_law(1, 0, 1), "euclidean_time"),
        (lambda: rectangular_area_law(1, 1, 0), "string_tension"),
        (lambda: rectangular_perimeter_law(1, 1, 0), "perimeter_coefficient"),
    ],
)
def test_positive_domains_are_enforced(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()


def test_extractor_requires_an_explicit_limit_symbol() -> None:
    with pytest.raises(TypeError, match="SymPy Symbol"):
        static_potential_from_loop(sp.exp(-1), 1)
