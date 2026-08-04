from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.boundary_scattering import (
    PassiveHalfLineScatteringLedger,
    passive_half_line_scattering_ledger,
)
from substrate_framework.branching import two_channel_allocation
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility


def test_symbolic_passive_half_line_scattering_ledger_is_exact() -> None:
    wave_speed, boundary_speed = sp.symbols("c zeta", positive=True)
    ledger = passive_half_line_scattering_ledger(wave_speed, boundary_speed)
    normalized = boundary_speed / wave_speed

    assert isinstance(ledger, PassiveHalfLineScatteringLedger)
    assert ledger.normalized_impedance == normalized
    assert sp.simplify(
        ledger.amplitude_reflection - (normalized - 1) / (normalized + 1)
    ) == 0
    assert sp.simplify(
        ledger.reflected_power_fraction
        - (normalized - 1) ** 2 / (normalized + 1) ** 2
    ) == 0
    assert sp.simplify(
        ledger.absorbed_power_fraction
        - 4 * normalized / (normalized + 1) ** 2
    ) == 0
    assert sp.simplify(
        ledger.reflected_power_fraction + ledger.absorbed_power_fraction - 1
    ) == 0


def test_plane_wave_substitution_derives_the_amplitude_not_just_its_square() -> None:
    wave_speed, boundary_speed, frequency = sp.symbols(
        "c zeta omega", positive=True
    )
    incident, reflected = sp.symbols("A_i A_r", nonzero=True)
    boundary_time_trace = -sp.I * frequency * (incident + reflected)
    boundary_spatial_trace = (
        -sp.I * frequency / wave_speed * (incident - reflected)
    )
    solution = sp.solve(
        sp.Eq(
            boundary_time_trace - boundary_speed * boundary_spatial_trace,
            0,
        ),
        reflected,
    )[0]
    ledger = passive_half_line_scattering_ledger(wave_speed, boundary_speed)
    assert sp.simplify(solution / incident - ledger.amplitude_reflection) == 0


def test_positive_boundary_speed_removes_right_half_line_bulk_energy() -> None:
    wave_speed, boundary_speed = sp.symbols("c zeta", positive=True)
    ledger = passive_half_line_scattering_ledger(wave_speed, boundary_speed)
    assert (
        ledger.bulk_energy_rate_per_spatial_trace_squared
        == -wave_speed**2 * boundary_speed
    )
    assert ledger.bulk_energy_rate_per_spatial_trace_squared.is_negative is True
    active_sign_coefficient = wave_speed**2 * boundary_speed
    assert active_sign_coefficient.is_positive is True


def test_impedance_match_is_reflectionless_and_fully_absorbing() -> None:
    ledger = passive_half_line_scattering_ledger(3, 3)
    assert ledger.normalized_impedance == 1
    assert ledger.amplitude_reflection == 0
    assert ledger.reflected_power_fraction == 0
    assert ledger.absorbed_power_fraction == 1
    assert ledger.reference_contrast == 1


def test_reciprocal_impedances_flip_phase_but_not_power_or_contrast() -> None:
    ledger = passive_half_line_scattering_ledger(2, 1)
    assert ledger.normalized_impedance == sp.Rational(1, 2)
    assert ledger.reciprocal_boundary_speed == 4
    assert ledger.amplitude_reflection == -sp.Rational(1, 3)
    assert ledger.reciprocal_amplitude_reflection == sp.Rational(1, 3)
    assert ledger.reflected_power_fraction == sp.Rational(1, 9)
    assert (
        ledger.reciprocal_reflected_power_fraction
        == ledger.reflected_power_fraction
    )
    assert ledger.absorbed_power_fraction == sp.Rational(8, 9)
    assert (
        ledger.reciprocal_absorbed_power_fraction
        == ledger.absorbed_power_fraction
    )
    assert ledger.reference_contrast == sp.Rational(4, 5)
    assert ledger.reciprocal_reference_contrast == ledger.reference_contrast


def test_reference_contrast_is_an_accepted_allocation_transform() -> None:
    wave_speed, boundary_speed = sp.symbols("c zeta", positive=True)
    ledger = passive_half_line_scattering_ledger(wave_speed, boundary_speed)
    allocation = two_channel_allocation(1, ledger.reflected_power_fraction)
    assert sp.simplify(
        ledger.reference_contrast
        - (allocation.first_fraction - allocation.second_fraction)
    ) == 0
    assert ledger.contrast_as_absorbed_transform_residual == 0
    assert sp.simplify(
        ledger.reference_contrast
        - 2 * wave_speed * boundary_speed / (wave_speed**2 + boundary_speed**2)
    ) == 0


def test_power_ratios_do_not_identify_which_reciprocal_impedance_applies() -> None:
    wave_speed, boundary_speed = sp.symbols("c zeta", positive=True)
    ledger = passive_half_line_scattering_ledger(wave_speed, boundary_speed)
    assert sp.simplify(
        ledger.reciprocal_reflected_power_fraction
        - ledger.reflected_power_fraction
    ) == 0
    assert sp.simplify(
        ledger.reciprocal_reference_contrast - ledger.reference_contrast
    ) == 0
    assert sp.simplify(
        ledger.reciprocal_amplitude_reflection
        + ledger.amplitude_reflection
    ) == 0


def test_zero_and_large_impedance_limits_are_power_reflecting() -> None:
    wave_speed, boundary_speed = sp.symbols("c zeta", positive=True)
    ledger = passive_half_line_scattering_ledger(wave_speed, boundary_speed)
    assert sp.limit(ledger.reflected_power_fraction, boundary_speed, 0, dir="+") == 1
    assert sp.limit(ledger.absorbed_power_fraction, boundary_speed, 0, dir="+") == 0
    assert sp.limit(ledger.reflected_power_fraction, boundary_speed, sp.oo) == 1
    assert sp.limit(ledger.absorbed_power_fraction, boundary_speed, sp.oo) == 0


@pytest.mark.parametrize(
    "call",
    [
        lambda: passive_half_line_scattering_ledger(0, 1),
        lambda: passive_half_line_scattering_ledger(1, 0),
        lambda: passive_half_line_scattering_ledger(-1, 1),
        lambda: passive_half_line_scattering_ledger(1, -1),
        lambda: passive_half_line_scattering_ledger(1.0, 1),
        lambda: passive_half_line_scattering_ledger(1, sp.Symbol("zeta")),
    ],
)
def test_scattering_ledger_requires_exact_explicitly_positive_speeds(call) -> None:
    with pytest.raises(ValueError, match="positive|exact|real"):
        call()


def test_boundary_scattering_module_has_no_numpy_integration_shape() -> None:
    path = Path("src/substrate_framework/boundary_scattering.py")
    audit = audit_numpy_trapezoid_compatibility(
        path.read_text(encoding="utf-8"), filename=str(path)
    )
    assert audit.legacy_references == 0
    assert audit.current_references == 0
    assert audit.eager_legacy_default_fallbacks == 0
