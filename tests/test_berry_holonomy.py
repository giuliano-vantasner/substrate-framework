from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.berry_holonomy import (
    closed_ray_berry_ledger,
    phase_transform_section,
    projective_loop_berry_ledger,
    projective_loop_section,
)


phi = sp.symbols("phi", real=True)


@pytest.mark.parametrize("winding", [-3, -2, -1, 0, 1, 2, 3])
def test_real_and_periodic_projective_sections_have_the_same_holonomy(
    winding: int,
) -> None:
    result = projective_loop_berry_ledger(winding, phi)
    expected = sp.Integer(-1) ** winding

    assert result.parity_character == expected
    assert result.real_lift.berry_connection == 0
    assert result.real_lift.endpoint_transition == expected
    assert result.real_lift.bare_integral_phase == 1
    assert result.real_lift.holonomy == expected
    assert result.periodic_section.berry_connection == sp.Rational(winding, 2)
    assert result.periodic_section.endpoint_transition == 1
    assert result.periodic_section.bare_integral_phase == expected
    assert result.periodic_section.holonomy == expected
    assert result.real_lift.projector == result.periodic_section.projector


def test_symbolic_integer_winding_proves_the_parity_formula() -> None:
    winding = sp.symbols("k", integer=True)
    result = projective_loop_berry_ledger(winding, phi)

    assert result.real_lift.endpoint_transition == (-1) ** winding
    assert result.periodic_section.berry_connection == winding / 2
    assert result.real_lift.holonomy == (-1) ** winding
    assert result.periodic_section.holonomy == (-1) ** winding


def test_nonperiodic_gauge_change_moves_phase_between_transition_and_integral() -> None:
    lift = projective_loop_section(1, phi)
    baseline = closed_ray_berry_ledger(lift, phi)
    transformed = closed_ray_berry_ledger(
        phase_transform_section(lift, -3 * phi / 2), phi
    )

    assert baseline.berry_connection == 0
    assert baseline.endpoint_transition == -1
    assert transformed.berry_connection == sp.Rational(3, 2)
    assert transformed.endpoint_transition == 1
    assert transformed.bare_integral_phase == -1
    assert transformed.holonomy == baseline.holonomy == -1


def test_periodic_gauge_changes_local_connection_but_not_holonomy() -> None:
    lift = projective_loop_section(1, phi)
    baseline = closed_ray_berry_ledger(lift, phi)
    transformed = closed_ray_berry_ledger(
        phase_transform_section(lift, 2 * phi), phi
    )

    assert transformed.berry_connection == -2
    assert transformed.endpoint_transition == -1
    assert transformed.connection_integral == -4 * sp.pi
    assert transformed.holonomy == baseline.holonomy == -1


def test_fixed_ray_phase_has_bare_minus_one_but_corrected_plus_one() -> None:
    fixed_ray = sp.ImmutableMatrix([sp.exp(-sp.I * phi / 2), 0])
    result = closed_ray_berry_ledger(fixed_ray, phi)

    assert result.projector_is_constant
    assert result.berry_connection == sp.Rational(1, 2)
    assert result.endpoint_transition == -1
    assert result.bare_integral_phase == -1
    assert result.holonomy == 1


def test_reversal_inverts_connection_transition_and_holonomy() -> None:
    forward = projective_loop_berry_ledger(1, phi).periodic_section
    reverse = projective_loop_berry_ledger(-1, phi).periodic_section

    assert reverse.berry_connection == -forward.berry_connection
    assert reverse.connection_integral == -forward.connection_integral
    assert reverse.endpoint_transition == sp.conjugate(forward.endpoint_transition)
    assert reverse.holonomy == sp.conjugate(forward.holonomy)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: closed_ray_berry_ledger([1], phi), "dimension at least two"),
        (lambda: closed_ray_berry_ledger([2, 0], phi), "normalized"),
        (
            lambda: closed_ray_berry_ledger([sp.cos(phi / 4), sp.sin(phi / 4)], phi),
            "closed rank-one projector",
        ),
        (lambda: closed_ray_berry_ledger([1, 0], phi, end=0), "greater"),
        (lambda: projective_loop_section(sp.Rational(1, 2), phi), "integer"),
        (
            lambda: phase_transform_section([1, 0], sp.I * phi),
            "explicitly real",
        ),
    ],
)
def test_berry_API_rejects_untyped_or_invalid_inputs(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
