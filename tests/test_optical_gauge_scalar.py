from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.optical_gauge_scalar import (
    affine_gauge_plane_wave,
    berry_one_form_to_u1_connection,
    charged_optical_scalar_euler_operator,
    charged_optical_scalar_lagrangian_density,
    circle_optical_gauge_mode,
    constant_optical_gauge_dispersion,
)


def test_constant_plane_wave_euler_operator_matches_invariant_mass_shell() -> None:
    t, x = sp.symbols("t x", real=True)
    n, c0, m, e = sp.symbols("n c0 m e", positive=True)
    omega, k, a_t, a_x = sp.symbols("omega k A_t A_x", real=True)
    field = sp.exp(sp.I * (k * x - omega * t))
    result = constant_optical_gauge_dispersion(n, c0, m, e, omega, k, a_t, a_x)
    euler = charged_optical_scalar_euler_operator(
        field, n, c0, m, e, (a_t, a_x), (t, x)
    )
    assert result.inverse_metric == sp.diag(-n, c0**2 / n)
    assert result.volume_density == 1 / c0
    assert sp.simplify(euler / field - (result.mass_shell_lhs - m**2)) == 0
    assert result.invariant_frequency == omega + e * a_t
    assert result.invariant_wavenumber == k - e * a_x


def test_declared_action_density_is_affine_gauge_invariant() -> None:
    t, x = sp.symbols("t x", real=True)
    n, c0, m, e = sp.symbols("n c0 m e", positive=True)
    omega, k, a_t, a_x, alpha, beta = sp.symbols(
        "omega k A_t A_x alpha beta", real=True
    )
    field = sp.exp(sp.I * (k * x - omega * t))
    field_bar = sp.exp(-sp.I * (k * x - omega * t))
    chi = alpha * t + beta * x
    baseline = charged_optical_scalar_lagrangian_density(
        field, field_bar, n, c0, m, e, (a_t, a_x), (t, x)
    )
    transformed = charged_optical_scalar_lagrangian_density(
        sp.exp(sp.I * e * chi) * field,
        sp.exp(-sp.I * e * chi) * field_bar,
        n,
        c0,
        m,
        e,
        (a_t + alpha, a_x + beta),
        (t, x),
    )
    assert sp.simplify(transformed - baseline) == 0


def test_affine_labels_preserve_invariants_and_remove_constant_line_connection() -> None:
    omega, k, a_t, a_x, e = sp.symbols(
        "omega k A_t A_x e", real=True, positive=True
    )
    removed = affine_gauge_plane_wave(omega, k, a_t, a_x, e, -a_t, -a_x)
    assert removed.temporal_connection == 0
    assert removed.spatial_connection == 0
    assert removed.frequency == omega + e * a_t
    assert removed.wavenumber == k - e * a_x
    assert removed.invariant_frequency == omega + e * a_t
    assert removed.invariant_wavenumber == k - e * a_x


def test_circle_mode_is_invariant_under_large_gauge_relabeling() -> None:
    n, c0, m, e, length = sp.symbols("n c0 m e L", positive=True)
    a_x, theta = sp.symbols("A_x theta", real=True)
    mode, winding = sp.symbols("q ell", integer=True)
    baseline = circle_optical_gauge_mode(n, c0, m, e, a_x, length, mode, theta)
    shifted = circle_optical_gauge_mode(
        n,
        c0,
        m,
        e,
        a_x + 2 * sp.pi * winding / (e * length),
        length,
        mode + winding,
        theta,
    )
    assert sp.simplify(shifted.invariant_wavenumber - baseline.invariant_wavenumber) == 0
    assert sp.simplify(
        shifted.invariant_frequency_squared - baseline.invariant_frequency_squared
    ) == 0
    assert sp.simplify(shifted.connection_holonomy - baseline.connection_holonomy) == 0


def test_variable_index_requires_the_covariant_divergence_term() -> None:
    t, x = sp.symbols("t x", real=True)
    c0, m, e = sp.symbols("c0 m e", positive=True)
    n = sp.Function("n", positive=True)(x)
    a_x = sp.Function("A_x", real=True)(x)
    field = sp.Function("Psi")(t, x)
    exact = charged_optical_scalar_euler_operator(
        field, n, c0, m, e, (0, a_x), (t, x)
    )
    d_t = sp.diff(field, t)
    d_x = sp.diff(field, x) - sp.I * e * a_x * field
    d_x_twice = sp.diff(d_x, x) - sp.I * e * a_x * d_x
    naive = n * sp.diff(field, t, 2) * -1 + c0**2 * d_x_twice / n - m**2 * field
    difference = sp.simplify(exact - naive)
    assert sp.simplify(difference + c0**2 * sp.diff(n, x) * d_x / n**2) == 0
    assert difference != 0


def test_berry_pullback_has_the_same_phase_sign_and_dimensioned_texture_factor() -> None:
    x = sp.symbols("x", real=True)
    length, e = sp.symbols("L e", positive=True)
    phi = 2 * sp.pi * x / length
    connection = berry_one_form_to_u1_connection(sp.Rational(1, 2), phi, x, e)
    assert connection == -sp.pi / (e * length)
    assert sp.simplify(sp.exp(sp.I * e * connection * length)) == -1
    assert connection != sp.Rational(1, 2)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: constant_optical_gauge_dispersion(0, 1, 1, 1, 0, 0), "index"),
        (lambda: constant_optical_gauge_dispersion(1, 1.0, 1, 1, 0, 0), "signal_speed"),
        (lambda: circle_optical_gauge_mode(1, 1, 1, 1, 0, 1, sp.Rational(1, 2)), "mode"),
        (
            lambda: charged_optical_scalar_euler_operator(
                sp.Symbol("Psi"),
                sp.Function("n", positive=True)(sp.Symbol("t", real=True)),
                1,
                1,
                1,
                (0, 0),
                (sp.Symbol("t", real=True), sp.Symbol("x", real=True)),
            ),
            "static",
        ),
    ],
)
def test_input_guards(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
