from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.sine_gordon import (
    breather_action,
    breather_action_lattice_adjacent_gap,
    breather_action_lattice_energy,
    breather_action_lattice_frequency,
    breather_action_secant_ratio,
    breather_core_fundamental_sine_coefficient,
    boosted_breather_energy_momentum,
    boosted_breather_phase_components,
    breather_energy,
    breather_energy_second_moment,
    breather_energy_second_moment_extrema,
    breather_energy_from_action,
    breather_field,
    breather_inverse_width,
    breather_frequency_from_action,
    breather_mean_gradient_integral,
    breather_peak_amplitude,
    breather_period,
    breather_secant_action_scale,
    breather_temporal_argument_amplitude,
    breather_temporal_fundamental_sine_coefficient,
    breather_threshold_deficit,
    hamiltonian_density,
    light_cone_derivatives,
    naive_chiral_currents,
    naive_chiral_transport_defects,
    sine_gordon_residual,
    sine_gordon_chiral_sources,
    sine_gordon_lagrangian_density,
    sine_gordon_light_cone_chiral_sources,
    sine_gordon_light_cone_stress_balances,
    sine_gordon_light_cone_stress_components,
    sine_gordon_potential,
    spatial_parity_transform,
    static_kink_field,
    sine_gordon_stress_divergence,
    sine_gordon_stress_tensor_contravariant,
    sine_gordon_stress_tensor_covariant,
    sine_gordon_stress_trace,
    topological_charge_from_boundaries,
    topological_current,
    topological_current_divergence,
)


def test_exact_breather_residual_vanishes() -> None:
    x, t = sp.symbols("x t", real=True)
    omega = sp.symbols("omega", positive=True)
    field = breather_field(x, t, omega)
    assert sp.simplify(sine_gordon_residual(field, x, t)) == 0


def test_naive_chiral_currents_have_equal_sine_gordon_sources() -> None:
    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    current_plus, current_minus = naive_chiral_currents(field, x, t)
    assert current_plus == sp.diff(field, t) + sp.diff(field, x)
    assert current_minus == sp.diff(field, t) - sp.diff(field, x)

    defect_plus, defect_minus = naive_chiral_transport_defects(field, x, t)
    wave_operator = sp.diff(field, t, 2) - sp.diff(field, x, 2)
    assert sp.simplify(defect_plus - wave_operator) == 0
    assert sp.simplify(defect_minus - wave_operator) == 0
    assert sine_gordon_chiral_sources(field) == (-sp.sin(field), -sp.sin(field))
    assert sine_gordon_light_cone_chiral_sources(field) == (
        -sp.sin(field) / 2,
        -sp.sin(field) / 2,
    )


def test_topological_current_is_off_shell_conserved_with_load_bearing_sign() -> None:
    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    density, flux = topological_current(field, x, t)
    assert density == sp.diff(field, x) / (2 * sp.pi)
    assert flux == -sp.diff(field, t) / (2 * sp.pi)
    assert topological_current_divergence(field, x, t) == 0

    wrong_divergence = sp.simplify(
        sp.diff(density, t) + sp.diff(-flux, x)
    )
    assert wrong_divergence != 0


def test_kink_charge_and_parity_sector_exchange_are_exact() -> None:
    x, t = sp.symbols("x t", real=True)
    kink = static_kink_field(x)
    antikink = static_kink_field(x, orientation=-1)
    assert sp.simplify(sine_gordon_residual(kink, x, t)) == 0
    assert sp.simplify(sine_gordon_residual(antikink, x, t)) == 0
    assert topological_charge_from_boundaries(0, 2 * sp.pi) == 1
    assert topological_charge_from_boundaries(2 * sp.pi, 0) == -1
    assert sp.simplify(spatial_parity_transform(kink, x) - antikink) == 0


def test_sine_gordon_equation_is_spatial_parity_invariant() -> None:
    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    parity_field = spatial_parity_transform(field, x)
    parity_residual = sine_gordon_residual(parity_field, x, t)
    reflected_residual = sine_gordon_residual(field, x, t).subs(x, -x)
    assert sp.simplify(parity_residual - reflected_residual) == 0


def test_small_amplitude_sine_gordon_is_massive_not_chiral_wave_limit() -> None:
    epsilon = sp.symbols("epsilon", positive=True)
    profile = sp.symbols("f", real=True)
    source = sine_gordon_chiral_sources(epsilon * profile)[0]
    assert sp.limit(source / epsilon, epsilon, 0, dir="+") == -profile


def test_canonical_sine_gordon_stress_tensor_and_divergence() -> None:
    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    field_t = sp.diff(field, t)
    field_x = sp.diff(field, x)
    potential = sine_gordon_potential(field)
    assert potential == 1 - sp.cos(field)
    assert sine_gordon_lagrangian_density(field, x, t) == (
        field_t**2 / 2 - field_x**2 / 2 - potential
    )
    covariant = sine_gordon_stress_tensor_covariant(field, x, t)
    contravariant = sine_gordon_stress_tensor_contravariant(field, x, t)
    assert covariant == sp.Matrix(
        [
            [(field_t**2 + field_x**2) / 2 + potential, field_t * field_x],
            [field_t * field_x, (field_t**2 + field_x**2) / 2 - potential],
        ]
    )
    assert contravariant == sp.Matrix(
        [
            [covariant[0, 0], -field_t * field_x],
            [-field_t * field_x, covariant[1, 1]],
        ]
    )
    assert covariant[0, 0] == hamiltonian_density(field, x, t)
    residual = sine_gordon_residual(field, x, t)
    expected_divergence = sp.Matrix([field_t * residual, -field_x * residual])
    assert all(
        sp.simplify(entry) == 0
        for entry in (
            sine_gordon_stress_divergence(field, x, t) - expected_divergence
        )
    )
    assert sine_gordon_stress_trace(field, x, t) == 2 * potential


def test_light_cone_stress_components_and_off_shell_balances() -> None:
    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    current_plus, current_minus = naive_chiral_currents(field, x, t)
    plus_plus, minus_minus, plus_minus = sine_gordon_light_cone_stress_components(
        field,
        x,
        t,
    )
    assert sp.simplify(plus_plus - current_plus**2 / 4) == 0
    assert sp.simplify(minus_minus - current_minus**2 / 4) == 0
    assert plus_minus == sine_gordon_potential(field) / 2
    balance_plus, balance_minus = sine_gordon_light_cone_stress_balances(
        field,
        x,
        t,
    )
    residual = sine_gordon_residual(field, x, t)
    assert sp.simplify(balance_plus - current_plus * residual / 4) == 0
    assert sp.simplify(balance_minus - current_minus * residual / 4) == 0


def test_light_cone_operator_and_source_normalization_conversion() -> None:
    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    plus, minus = light_cone_derivatives(field, x, t)
    canonical_plus, canonical_minus, canonical_mixed = (
        sine_gordon_light_cone_stress_components(field, x, t)
    )
    source_plus = plus**2 / 2
    source_minus = minus**2 / 2
    source_theta = (sp.cos(field) - 1) / 4
    assert sp.simplify(source_plus - canonical_plus / 2) == 0
    assert sp.simplify(source_minus - canonical_minus / 2) == 0
    assert source_theta == -canonical_mixed / 2


def test_stress_parity_exchange_and_exact_kink_pressure() -> None:
    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    parity_field = spatial_parity_transform(field, x)
    parity_components = sine_gordon_light_cone_stress_components(
        parity_field,
        x,
        t,
    )
    original_components = tuple(
        item.subs(x, -x)
        for item in sine_gordon_light_cone_stress_components(field, x, t)
    )
    assert sp.simplify(parity_components[0] - original_components[1]) == 0
    assert sp.simplify(parity_components[1] - original_components[0]) == 0
    assert sp.simplify(parity_components[2] - original_components[2]) == 0

    kink = static_kink_field(x)
    kink_tensor = sine_gordon_stress_tensor_covariant(kink, x, t)
    assert sp.simplify(kink_tensor[1, 1]) == 0
    assert sp.simplify(kink_tensor[0, 0] - 2 * sine_gordon_potential(kink)) == 0


@pytest.mark.parametrize("orientation", [0, 2, -2])
def test_static_kink_rejects_nonunit_orientation(orientation: int) -> None:
    with pytest.raises(ValueError, match="orientation"):
        static_kink_field(sp.Symbol("x"), orientation=orientation)


def test_breather_formulas_at_exact_frequency() -> None:
    omega = sp.Rational(3, 5)
    assert breather_inverse_width(omega) == sp.Rational(4, 5)
    assert breather_energy(omega) == sp.Rational(64, 5)
    assert breather_threshold_deficit(omega) == sp.Rational(16, 5)
    assert breather_energy(omega) + breather_threshold_deficit(omega) == 16
    assert breather_period(omega) == 10 * sp.pi / 3
    assert breather_peak_amplitude(omega) == 4 * sp.atan(sp.Rational(4, 3))
    action = breather_action(omega)
    assert action == 16 * sp.acos(sp.Rational(3, 5))
    assert sp.simplify(breather_frequency_from_action(action) - omega) == 0
    assert sp.simplify(breather_energy_from_action(action) - breather_energy(omega)) == 0
    assert breather_mean_gradient_integral(omega) == 16 * (
        sp.Rational(4, 5) - sp.Rational(3, 5) * sp.acos(sp.Rational(3, 5))
    )
    assert breather_secant_action_scale(omega) == sp.Rational(64, 3)
    assert breather_action_secant_ratio(omega) == sp.Rational(3, 4) * sp.acos(
        sp.Rational(3, 5)
    )


def test_exact_breather_temporal_parity_and_half_wave_support() -> None:
    x, time = sp.symbols("x t", real=True)
    omega = sp.Rational(3, 5)
    period = breather_period(omega)
    field = breather_field(x, time, omega)
    assert sp.simplify(field.subs(time, -time) + field) == 0
    assert sp.simplify(field.subs(time, time + period / 2) + field) == 0

    phase = sp.symbols("y", real=True)
    phase_trace = field.subs(time, phase / omega)
    assert sp.simplify(phase_trace.subs(phase, 2 * sp.pi - phase) + phase_trace) == 0


def test_exact_breather_temporal_fundamental_coefficient() -> None:
    x = sp.symbols("x", real=True)
    omega = sp.Rational(3, 5)
    eta = sp.Rational(4, 5)
    amplitude = breather_temporal_argument_amplitude(x, omega)
    assert amplitude == 4 / (3 * sp.cosh(4 * x / 5))

    coefficient = breather_temporal_fundamental_sine_coefficient(x, omega)
    expected = 8 * amplitude / (sp.sqrt(1 + amplitude**2) + 1)
    assert sp.simplify(coefficient - expected) == 0
    assert breather_core_fundamental_sine_coefficient(omega) == 4
    assert sp.simplify(coefficient.subs(x, 0) - 4) == 0

    source_leading_term = 4 * eta / omega
    assert source_leading_term == sp.Rational(16, 3)
    assert source_leading_term != breather_core_fundamental_sine_coefficient(omega)


def test_breather_fundamental_coefficient_has_correct_small_amplitude_limit() -> None:
    amplitude = sp.symbols("a", positive=True)
    exact = 8 * amplitude / (sp.sqrt(1 + amplitude**2) + 1)
    assert sp.limit(exact / (4 * amplitude), amplitude, 0, dir="+") == 1
    assert sp.simplify(exact - 8 * (sp.sqrt(1 + amplitude**2) - 1) / amplitude) == 0


def test_breather_energy_second_moment_exact_phases_and_half_period() -> None:
    omega = sp.Rational(3, 5)
    eta = sp.Rational(4, 5)
    time = sp.symbols("t", real=True)
    moment = breather_energy_second_moment(omega, time)
    minimum, maximum = breather_energy_second_moment_extrema(omega)
    assert minimum == 5 * sp.pi**2 / 3
    assert maximum == minimum + 20 * sp.asinh(sp.Rational(4, 3)) ** 2
    assert moment.subs(time, 0) == minimum
    assert sp.simplify(moment.subs(time, sp.pi / (2 * omega)) - maximum) == 0
    assert sp.simplify(
        moment.subs(time, time + sp.pi / omega) - moment
    ) == 0
    assert sp.simplify(moment.subs(time, -time) - moment) == 0


def test_breather_energy_second_moment_special_value_is_not_a_pure_sinusoid() -> None:
    omega = 1 / sp.sqrt(2)
    moment = breather_energy_second_moment(omega, sp.symbols("t", real=True))
    minimum, maximum = breather_energy_second_moment_extrema(omega)
    assert minimum == 4 * sp.sqrt(2) * sp.pi**2 / 3
    assert sp.simplify(
        maximum
        - minimum
        - 16 * sp.sqrt(2) * sp.asinh(1) ** 2
    ) == 0
    assert moment.has(sp.asinh)


def test_conditional_action_lattice_and_adjacent_gap() -> None:
    level = 2
    action_quantum = sp.pi
    assert breather_action_lattice_frequency(level, action_quantum) == sp.cos(
        sp.pi / 8
    )
    assert breather_action_lattice_energy(level, action_quantum) == 16 * sp.sin(
        sp.pi / 8
    )
    assert sp.simplify(
        breather_action_lattice_adjacent_gap(level, action_quantum)
        - 32 * sp.sin(sp.pi / 32) * sp.cos(5 * sp.pi / 32)
    ) == 0


def test_boosted_breather_vectors_share_the_secant_scale() -> None:
    omega = sp.Rational(4, 5)
    velocity = sp.Rational(3, 5)
    phase = boosted_breather_phase_components(omega, velocity)
    momentum = boosted_breather_energy_momentum(omega, velocity)
    assert phase == (1, sp.Rational(3, 5))
    assert momentum == (12, sp.Rational(36, 5))
    scale = breather_secant_action_scale(omega)
    assert scale == 12
    assert momentum == tuple(sp.simplify(scale * item) for item in phase)


@pytest.mark.parametrize("omega", [0, 1, -sp.Rational(1, 2), 2, sp.I])
def test_numeric_frequency_domain_is_enforced(omega: sp.Expr) -> None:
    with pytest.raises(ValueError, match="0 < omega < 1"):
        breather_threshold_deficit(omega)


@pytest.mark.parametrize("action", [0, 8 * sp.pi, -1, 9 * sp.pi, sp.I])
def test_numeric_action_domain_is_enforced(action: sp.Expr) -> None:
    with pytest.raises(ValueError, match=r"0 < action < 8\*pi"):
        breather_energy_from_action(action)


@pytest.mark.parametrize(
    ("level", "action_quantum", "message"),
    [
        (0, 1, "positive integer"),
        (sp.Rational(1, 2), 1, "positive integer"),
        (1, 0, "real and positive"),
        (1, 8 * sp.pi, r"0 < action < 8\*pi"),
        (2, 3 * sp.pi, r"0 < action < 8\*pi"),
    ],
)
def test_numeric_action_lattice_domain_is_enforced(
    level: sp.Expr, action_quantum: sp.Expr, message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        breather_action_lattice_adjacent_gap(level, action_quantum)


@pytest.mark.parametrize("velocity", [-1, 1, 2, sp.I])
def test_numeric_velocity_domain_is_enforced(velocity: sp.Expr) -> None:
    with pytest.raises(ValueError, match=r"abs\(velocity\) < 1"):
        boosted_breather_phase_components(sp.Rational(1, 2), velocity)
