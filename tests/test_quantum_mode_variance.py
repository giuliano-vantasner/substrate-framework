from __future__ import annotations

import ast
from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.quantum_mode_variance import (
    gapped_vacuum_kernel,
    mode_variance_ledger,
    scalar_continuum_vacuum_variance_3d,
    scalar_mode_ground_state_variance,
)


def test_one_mode_ground_state_normalization_is_explicit() -> None:
    hbar, V, kappa, c, omega = sp.symbols(
        "hbar V kappa c omega", positive=True
    )
    variance = scalar_mode_ground_state_variance(hbar, V, kappa, c, omega)
    assert variance == hbar * c**2 / (2 * V * kappa * omega)
    assert sp.simplify(variance * (V * kappa / c**2) * omega - hbar / 2) == 0


def test_J_kernel_is_the_exact_inverse_frequency_radial_integral() -> None:
    x, X = sp.symbols("x X", nonnegative=True)
    kernel = gapped_vacuum_kernel(X)
    assert sp.simplify(sp.diff(kernel, X) - X**2 / sp.sqrt(1 + X**2)) == 0
    assert kernel.subs(X, 0) == 0
    integrated = sp.integrate(x**2 / sp.sqrt(1 + x**2), (x, 0, X))
    assert sp.simplify(kernel - integrated) == 0


def test_d3_continuum_formula_matches_direct_radial_integration() -> None:
    hbar, kappa, c, omega_0, K, k = sp.symbols(
        "hbar kappa c omega_0 K k", positive=True
    )
    frequency = sp.sqrt(omega_0**2 + c**2 * k**2)
    direct = sp.integrate(
        hbar * c**2 * k**2 / (4 * sp.pi**2 * kappa * frequency),
        (k, 0, K),
    )
    canonical = scalar_continuum_vacuum_variance_3d(
        hbar, kappa, c, omega_0, K
    )
    assert sp.simplify(canonical - direct) == 0


def test_MD2_beta_and_kernel_form_is_only_a_reparameterization() -> None:
    hbar, kappa, c, omega_0, K = sp.symbols(
        "hbar kappa c omega_0 K", positive=True
    )
    ell = c / omega_0
    beta_squared = hbar * c / (kappa * ell**2)
    canonical = scalar_continuum_vacuum_variance_3d(
        hbar, kappa, c, omega_0, K
    )
    reparameterized = beta_squared * gapped_vacuum_kernel(K * ell) / (
        4 * sp.pi**2
    )
    assert sp.simplify(canonical - reparameterized) == 0


def test_gapless_limit_and_exact_zero_gap_branch_agree() -> None:
    hbar, kappa, c, omega_0, K = sp.symbols(
        "hbar kappa c omega_0 K", positive=True
    )
    gapped = scalar_continuum_vacuum_variance_3d(
        hbar, kappa, c, omega_0, K
    )
    gapless = scalar_continuum_vacuum_variance_3d(hbar, kappa, c, 0, K)
    expected = hbar * c * K**2 / (8 * sp.pi**2 * kappa)
    assert gapless == expected
    assert sp.simplify(sp.limit(gapped, omega_0, 0, dir="+") - expected) == 0


def test_small_cutoff_limit_keeps_gap_and_cubic_phase_volume() -> None:
    hbar, kappa, c, omega_0, K = sp.symbols(
        "hbar kappa c omega_0 K", positive=True
    )
    variance = scalar_continuum_vacuum_variance_3d(
        hbar, kappa, c, omega_0, K
    )
    leading = hbar * c**2 * K**3 / (12 * sp.pi**2 * kappa * omega_0)
    assert sp.limit(variance / leading, K, 0, dir="+") == 1


def test_cutoff_and_branch_factors_are_load_bearing() -> None:
    hbar, kappa, c, omega_0, K = sp.symbols(
        "hbar kappa c omega_0 K", positive=True
    )
    scalar = scalar_continuum_vacuum_variance_3d(
        hbar, kappa, c, omega_0, K
    )
    triple = scalar_continuum_vacuum_variance_3d(
        hbar, kappa, c, omega_0, K, branches=3
    )
    expected_derivative = hbar * c**2 * K**2 / (
        4 * sp.pi**2 * kappa * sp.sqrt(omega_0**2 + c**2 * K**2)
    )
    assert triple == 3 * scalar
    assert sp.simplify(sp.diff(scalar, K) - expected_derivative) == 0
    assert scalar.subs(K, 2 * K) != scalar


def test_fixed_set_factorization_allows_unequal_variances() -> None:
    a, b, c = sp.symbols("a b c", nonnegative=True)
    ledger = mode_variance_ledger((a, b, c))
    assert ledger.count == 3
    assert ledger.total == a + b + c
    assert ledger.arithmetic_mean == (a + b + c) / 3
    assert ledger.factorization_residual == 0


def test_set_growth_can_change_count_and_total_independently() -> None:
    base = mode_variance_ledger((1, 3))
    zero_added = mode_variance_ledger((1, 3, 0))
    positive_added = mode_variance_ledger((1, 3, 5))
    assert zero_added.count != base.count and zero_added.total == base.total
    assert positive_added.count != base.count and positive_added.total != base.total
    assert positive_added.arithmetic_mean == 3
    assert base.arithmetic_mean == 2


def test_holding_mean_fixed_is_a_distinct_family_not_a_consequence() -> None:
    two_modes = mode_variance_ledger((2, 2))
    three_modes = mode_variance_ledger((2, 2, 2))
    assert two_modes.arithmetic_mean == three_modes.arithmetic_mean
    assert two_modes.total == 4 and three_modes.total == 6
    assert two_modes.total != three_modes.total


def test_mutating_ground_state_half_or_fourier_measure_breaks_formula() -> None:
    hbar, kappa, c, omega_0, K = sp.symbols(
        "hbar kappa c omega_0 K", positive=True
    )
    correct = scalar_continuum_vacuum_variance_3d(
        hbar, kappa, c, omega_0, K
    )
    missing_half = 2 * correct
    missing_fourier_cube = (2 * sp.pi) ** 3 * correct
    assert sp.simplify(correct - missing_half) != 0
    assert sp.simplify(correct - missing_fourier_cube) != 0


def test_mutable_module_has_no_legacy_numpy_trapezoid_access() -> None:
    path = Path(__file__).parents[1] / "src/substrate_framework/quantum_mode_variance.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    attributes = {
        node.attr for node in ast.walk(tree) if isinstance(node, ast.Attribute)
    }
    assert "trapz" not in attributes


@pytest.mark.parametrize(
    ("call", "match"),
    [
        (lambda: scalar_mode_ground_state_variance(0, 1, 1, 1, 1), "action_scale"),
        (lambda: scalar_mode_ground_state_variance(1, 0, 1, 1, 1), "quantization_volume"),
        (lambda: scalar_mode_ground_state_variance(1, 1, 0, 1, 1), "stiffness"),
        (lambda: scalar_mode_ground_state_variance(1, 1, 1, 0, 1), "signal_speed"),
        (lambda: scalar_mode_ground_state_variance(1, 1, 1, 1, 0), "angular_frequency"),
        (lambda: gapped_vacuum_kernel(-1), "argument"),
        (lambda: scalar_continuum_vacuum_variance_3d(1, 1, 1, -1, 1), "gap_frequency"),
        (lambda: scalar_continuum_vacuum_variance_3d(1, 1, 1, 1, 0), "radial_cutoff"),
        (lambda: scalar_continuum_vacuum_variance_3d(1, 1, 1, 1, 1, branches=0), "branches"),
        (lambda: mode_variance_ledger(()), "nonempty"),
        (lambda: mode_variance_ledger((1, -1)), "variance"),
    ],
)
def test_invalid_domains_are_rejected(call, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        call()
