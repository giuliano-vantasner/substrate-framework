from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.maxwell import static_maxwell_point_source
from substrate_framework.momentum_kernels import (
    critical_riesz_log_kernel,
    leading_power_ledger,
    massive_parameter_kernel,
    riesz_radial_force_law,
    riesz_green_kernel,
    spectral_moment_expansion,
)


def test_massive_parameter_kernel_has_exact_beta_coefficient_sequence() -> None:
    q2 = sp.Symbol("Q2", positive=True)
    m2, coefficient = sp.symbols("m2 C", positive=True)
    evidence = massive_parameter_kernel(q2, m2, coefficient)
    assert evidence.first_coefficient == coefficient / (6 * m2)
    assert evidence.second_coefficient == -coefficient / (30 * m2**2)
    for order in range(1, 7):
        direct = sp.integrate(
            coefficient
            * (-1) ** (order - 1)
            * (evidence.parameter * (1 - evidence.parameter)) ** order
            / m2**order,
            (evidence.parameter, 0, 1),
        )
        assert sp.simplify(evidence.coefficient(order) - direct) == 0
    assert evidence.convergence_radius == 4 * m2


def test_massive_parameter_closed_form_and_remainder_match_integrand() -> None:
    q2 = sp.Symbol("Q2", positive=True)
    m2 = sp.Symbol("m2", positive=True)
    evidence = massive_parameter_kernel(q2, m2)
    auxiliary = sp.Symbol("z", real=True)
    denominator = 4 * m2 + q2 - q2 * auxiliary**2
    primitive = (
        4
        * m2
        * sp.atanh(auxiliary * sp.sqrt(q2 / (4 * m2 + q2)))
        / sp.sqrt(q2 * (4 * m2 + q2))
    )
    assert sp.simplify(sp.diff(primitive, auxiliary) - 4 * m2 / denominator) == 0
    complementary_integral = sp.simplify(primitive.subs(auxiliary, 1) - primitive.subs(auxiliary, 0))
    assert sp.simplify(evidence.closed_form - (1 - complementary_integral)) == 0
    for order in range(0, 5):
        pointwise_series = sum(
            (
                (-1) ** (index - 1)
                * (evidence.parameter * (1 - evidence.parameter) * q2 / m2) ** index
                for index in range(1, order + 1)
            ),
            sp.S.Zero,
        )
        assert sp.simplify(
            evidence.integrand - pointwise_series - evidence.pointwise_remainder_integrand(order)
        ) == 0


def test_massive_and_zero_transfer_limits_do_not_commute() -> None:
    q2 = sp.Symbol("Q2", positive=True)
    m2 = sp.Symbol("m2", positive=True)
    coefficient = sp.Symbol("C", positive=True)
    evidence = massive_parameter_kernel(q2, m2, coefficient)
    assert evidence.zero_transfer_limit == 0
    assert evidence.massless_at_fixed_positive_transfer == coefficient
    assert sp.limit(sp.limit(evidence.closed_form, q2, 0, dir="+"), m2, 0, dir="+") == 0
    assert sp.limit(sp.limit(evidence.closed_form, m2, 0, dir="+"), q2, 0, dir="+") == coefficient


def test_spectral_moment_identity_keeps_convergence_as_a_premise() -> None:
    q2, t = sp.symbols("Q2 t", positive=True)
    gap = sp.Symbol("Delta", positive=True)
    density = sp.Function("rho")(t)
    evidence = spectral_moment_expansion(q2, t, density, gap, 4)
    assert evidence.pointwise_identity_residual == 0
    assert len(evidence.inverse_moments) == 4
    assert evidence.inverse_moments[0] == sp.Integral(density / t, (t, gap, sp.oo))
    assert sp.expand(evidence.series_polynomial).coeff(q2, 1) == evidence.inverse_moments[0]
    assert sp.expand(evidence.series_polynomial).coeff(q2, 2) == -evidence.inverse_moments[1]
    assert isinstance(evidence.exact_kernel, sp.Integral)
    assert isinstance(evidence.exact_remainder, sp.Integral)


def test_gap_alone_does_not_supply_finite_or_nonzero_first_moment() -> None:
    q2, t = sp.symbols("Q2 t", positive=True)
    gap = sp.Integer(1)
    divergent = spectral_moment_expansion(q2, t, t, gap, 1)
    assert divergent.inverse_moments[0].doit() == sp.oo
    zero_density = spectral_moment_expansion(q2, t, 0, gap, 2)
    assert all(moment.doit() == 0 for moment in zero_density.inverse_moments)


def test_leading_power_combines_terms_and_exposes_exact_cancellation() -> None:
    k2 = sp.Symbol("k2", positive=True)
    ledger = leading_power_ledger(k2, [(1, 3), (2, 5), (1, -1)])
    assert ledger.combined_terms == ((sp.Rational(1), sp.Integer(2)), (sp.Rational(2), sp.Integer(5)))
    assert ledger.leading_exponent == 1
    assert ledger.propagator_momentum_exponent == 2
    cancelled = leading_power_ledger(k2, [(1, 3), (1, -3), (2, 5)])
    assert cancelled.leading_exponent == 2
    assert cancelled.propagator_momentum_exponent == 4


def test_leading_power_refuses_undecidable_symbolic_coefficient() -> None:
    k2 = sp.Symbol("k2", positive=True)
    z = sp.Symbol("Z", real=True)
    with pytest.raises(ValueError, match="provably nonzero"):
        leading_power_ledger(k2, [(1, z), (2, 1)])
    nonzero_z = sp.Symbol("Z_nz", real=True, nonzero=True)
    assert leading_power_ledger(k2, [(1, nonzero_z), (2, 1)]).leading_exponent == 1


def test_fractional_bare_power_dominates_analytic_corrections() -> None:
    k2 = sp.Symbol("k2", positive=True)
    amplitude = sp.Symbol("A", positive=True)
    ledger = leading_power_ledger(k2, [(sp.Rational(2, 3), amplitude), (1, -2), (2, 7)])
    assert ledger.leading_exponent == sp.Rational(2, 3)
    assert ledger.propagator_momentum_exponent == sp.Rational(4, 3)


def test_riesz_kernel_derives_general_normalization_before_coulomb_case() -> None:
    radius = sp.Symbol("r", positive=True)
    dimension, power = sp.symbols("d s", positive=True)
    conditional = riesz_green_kernel(dimension, power, radius)
    assert conditional.normalization == (
        sp.gamma(dimension / 2 - power)
        / (4**power * sp.pi ** (dimension / 2) * sp.gamma(power))
    )
    assert conditional.radial_power == -dimension + 2 * power
    coulomb = riesz_green_kernel(3, 1, radius)
    assert coulomb.green_kernel == 1 / (4 * sp.pi * radius)
    assert coulomb.radial_derivative == -1 / (4 * sp.pi * radius**2)


def test_riesz_kernel_is_sensitive_to_dimension_power_and_normalization() -> None:
    radius = sp.Symbol("r", positive=True)
    baseline = riesz_green_kernel(3, 1, radius)
    changed_dimension = riesz_green_kernel(4, 1, radius)
    changed_power = riesz_green_kernel(3, sp.Rational(1, 2), radius)
    changed_coefficient = riesz_green_kernel(3, 1, radius, 2)
    assert changed_dimension.green_kernel != baseline.green_kernel
    assert changed_power.green_kernel != baseline.green_kernel
    assert changed_coefficient.green_kernel == baseline.green_kernel / 2
    with pytest.raises(ValueError, match="requires"):
        riesz_green_kernel(2, 1, radius)
    with pytest.raises(ValueError, match="Fourier"):
        riesz_green_kernel(3, 1, radius, fourier_convention="unitary")


def test_critical_riesz_limit_is_reference_subtracted_before_limiting() -> None:
    dimension, coefficient = sp.symbols("d A", positive=True)
    radius, reference = sp.symbols("r r0", positive=True)
    ledger = critical_riesz_log_kernel(
        dimension,
        radius,
        reference,
        coefficient,
    )

    expected_normalization = 2 / (
        coefficient
        * 4 ** (dimension / 2)
        * sp.pi ** (dimension / 2)
        * sp.gamma(dimension / 2)
    )
    assert ledger.limit_reconstruction_residual == 0
    assert sp.simplify(
        ledger.logarithmic_normalization - expected_normalization
    ) == 0
    assert sp.simplify(
        ledger.logarithmic_kernel
        - expected_normalization * sp.log(reference / radius)
    ) == 0
    assert ledger.reference_residual == 0
    assert sp.simplify(
        ledger.radial_derivative + expected_normalization / radius
    ) == 0


def test_critical_two_dimensional_kernel_matches_maxwell_log_branch() -> None:
    radius, reference = sp.symbols("r r0", positive=True)
    coefficient = sp.Symbol("kappa", positive=True)
    source = sp.Symbol("Q", real=True)
    critical = critical_riesz_log_kernel(2, radius, reference, coefficient)
    maxwell = static_maxwell_point_source(
        2,
        radius,
        source,
        1,
        coefficient,
        reference_radius=reference,
    )

    assert sp.simplify(
        critical.logarithmic_kernel
        - sp.log(reference / radius) / (2 * sp.pi * coefficient)
    ) == 0
    assert sp.simplify(
        source * critical.logarithmic_kernel - maxwell.potential
    ) == 0
    assert sp.simplify(
        source * (-critical.radial_derivative)
        - maxwell.radial_electric_field
    ) == 0


def test_subcritical_radial_force_exposes_inverse_square_family() -> None:
    radius = sp.Symbol("r", positive=True)
    source, probe, coefficient = sp.symbols("Q q A", real=True, nonzero=True)
    power = sp.Rational(3, 4)
    dimension = sp.Rational(5, 2)
    ledger = riesz_radial_force_law(
        dimension,
        power,
        radius,
        source,
        probe,
        coefficient,
    )

    assert ledger.force_radial_power == -2
    assert ledger.inverse_square_dimension_family == dimension
    assert ledger.inverse_square_residual == 0
    assert sp.simplify(
        ledger.radial_force
        + sp.diff(ledger.potential_energy, radius)
    ) == 0


def test_coulomb_force_specialization_matches_conditional_maxwell_branch() -> None:
    radius = sp.Symbol("r", positive=True)
    source, probe = sp.symbols("Q q", real=True)
    coefficient = sp.Symbol("kappa", positive=True)
    fractional = riesz_radial_force_law(
        3,
        1,
        radius,
        source,
        probe,
        coefficient,
    )
    maxwell = static_maxwell_point_source(
        3,
        radius,
        source,
        probe,
        coefficient,
    )

    assert sp.simplify(fractional.potential - maxwell.potential) == 0
    assert sp.simplify(
        fractional.potential_energy - maxwell.potential_energy
    ) == 0
    assert sp.simplify(fractional.radial_force - maxwell.radial_force) == 0
    assert fractional.inverse_square_dimension_family == 3


def test_reference_source_and_probe_inputs_remain_visible() -> None:
    radius, reference_a, reference_b = sp.symbols(
        "r r_a r_b", positive=True
    )
    critical_a = critical_riesz_log_kernel(2, radius, reference_a)
    critical_b = critical_riesz_log_kernel(2, radius, reference_b)
    assert sp.simplify(
        sp.diff(
            critical_a.logarithmic_kernel
            - critical_b.logarithmic_kernel,
            radius,
        )
    ) == 0
    assert critical_a.logarithmic_kernel != critical_b.logarithmic_kernel

    zero_source = riesz_radial_force_law(3, 1, radius, 0, 1)
    zero_probe = riesz_radial_force_law(3, 1, radius, 1, 0)
    assert zero_source.potential == 0
    assert zero_source.radial_force == 0
    assert zero_probe.potential != 0
    assert zero_probe.radial_force == 0
