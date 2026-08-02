import sympy as sp
import pytest

from substrate_framework.charge_traces import (
    WeightedChargeState,
    abelian_normalization_ledger,
    charge_coupling_angle_ledger,
    common_trace_normalized_coupling_angle,
    finite_charge_trace_ledger,
    weighted_abelian_moment,
)


def _declared_generation() -> tuple[WeightedChargeState, ...]:
    return (
        WeightedChargeState("Q_L_up", 3, sp.Rational(1, 2), sp.Rational(1, 6)),
        WeightedChargeState("Q_L_down", 3, -sp.Rational(1, 2), sp.Rational(1, 6)),
        WeightedChargeState("u_R_conj", 3, 0, -sp.Rational(2, 3)),
        WeightedChargeState("d_R_conj", 3, 0, sp.Rational(1, 3)),
        WeightedChargeState("L_neutrino", 1, sp.Rational(1, 2), -sp.Rational(1, 2)),
        WeightedChargeState("L_electron", 1, -sp.Rational(1, 2), -sp.Rational(1, 2)),
        WeightedChargeState("e_R_conj", 1, 0, 1),
    )


def test_declared_generation_traces_are_exact_table_properties() -> None:
    ledger = finite_charge_trace_ledger(_declared_generation())
    assert ledger.state_count == 15
    assert ledger.trace_t3_squared == 2
    assert ledger.trace_abelian_squared == sp.Rational(10, 3)
    assert ledger.trace_cross == 0
    assert ledger.trace_electric_squared == sp.Rational(16, 3)
    assert ledger.decomposition_residual == 0
    assert ledger.trace_ratio == sp.Rational(3, 8)


def test_nonzero_cross_trace_is_retained_in_decomposition() -> None:
    states = (
        WeightedChargeState("one", 2, sp.Rational(1, 2), sp.Rational(1, 3)),
        WeightedChargeState("two", 1, -1, sp.Rational(2, 3)),
    )
    coefficient = sp.Rational(5, 2)
    ledger = finite_charge_trace_ledger(
        states,
        electric_coefficient=coefficient,
    )
    assert ledger.trace_cross != 0
    assert ledger.trace_electric_squared == ledger.expanded_trace_electric_squared
    assert ledger.decomposition_residual == 0


def test_trace_ratio_is_withheld_when_denominator_nonzero_status_is_unknown() -> None:
    coordinate = sp.Symbol("coordinate", real=True)
    ledger = finite_charge_trace_ledger(
        (WeightedChargeState("symbolic", 1, coordinate, 0),)
    )
    assert ledger.trace_electric_squared == coordinate**2
    assert ledger.trace_electric_squared.is_zero is None
    assert ledger.trace_ratio is None


def test_fixed_coefficient_rescaling_changes_the_source_trace_ratio() -> None:
    rho, coupling = sp.symbols("rho g_Y", positive=True)
    ledger = abelian_normalization_ledger(
        _declared_generation(), rho, coupling
    )
    assert ledger.fixed_coefficient.trace_abelian_squared == sp.Rational(10, 3) * rho**2
    assert ledger.fixed_coefficient.trace_cross == 0
    assert ledger.fixed_coefficient.trace_electric_squared == 2 + sp.Rational(10, 3) * rho**2
    assert ledger.fixed_coefficient.trace_ratio == 3 / (3 + 5 * rho**2)
    assert ledger.fixed_coefficient.trace_ratio.subs(rho, 2) == sp.Rational(3, 23)


def test_covariant_generator_change_preserves_charge_and_coupled_norm() -> None:
    rho, coupling = sp.symbols("rho g_Y", positive=True)
    ledger = abelian_normalization_ledger(
        _declared_generation(), rho, coupling
    )
    assert ledger.rescaled_abelian_coupling == coupling / rho
    assert ledger.rescaled_electric_coefficient == 1 / rho
    assert ledger.covariant.trace_electric_squared == ledger.base.trace_electric_squared
    assert ledger.covariant.trace_ratio == ledger.base.trace_ratio == sp.Rational(3, 8)
    assert ledger.charge_product_residuals == (0,) * len(_declared_generation())
    assert ledger.coupled_trace_norm_residual == 0


def test_coupling_angle_is_not_a_trace_angle_without_extra_premise() -> None:
    generic = charge_coupling_angle_ledger(2, sp.Rational(10, 3), 1, 1)
    assert generic.coupling_angle == sp.Rational(1, 2)
    assert generic.trace_angle == sp.Rational(3, 8)
    assert generic.angle_residual != 0
    assert generic.equality_numerator != 0
    assert generic.coupling_squared_ratio == 1
    assert generic.required_coupling_squared_ratio == sp.Rational(3, 5)


def test_required_coupling_ratio_is_exactly_sufficient() -> None:
    ledger = charge_coupling_angle_ledger(
        2,
        sp.Rational(10, 3),
        sp.sqrt(5),
        sp.sqrt(3),
    )
    assert ledger.coupling_squared_ratio == sp.Rational(3, 5)
    assert ledger.coupling_angle == ledger.trace_angle == sp.Rational(3, 8)
    assert ledger.angle_residual == 0
    assert ledger.equality_numerator == 0
    assert ledger.common_coefficient_residual == 0


def test_common_inverse_trace_law_is_conditional_and_coefficient_independent() -> None:
    common = sp.Symbol("C", positive=True)
    ledger = common_trace_normalized_coupling_angle(
        2,
        sp.Rational(10, 3),
        common,
    )
    assert ledger.coupling_angle == ledger.trace_angle == sp.Rational(3, 8)
    assert ledger.su2_inverse_trace_coefficient == common
    assert ledger.abelian_inverse_trace_coefficient == common
    assert ledger.common_coefficient_residual == 0


def test_unequal_inverse_trace_coefficients_break_trace_angle_equality() -> None:
    trace_2, trace_y = sp.Integer(2), sp.Rational(10, 3)
    c2, cy = sp.Integer(2), sp.Integer(7)
    g2 = sp.sqrt(1 / (c2 * trace_2))
    gy = sp.sqrt(1 / (cy * trace_y))
    ledger = charge_coupling_angle_ledger(trace_2, trace_y, g2, gy)
    assert ledger.su2_inverse_trace_coefficient == c2
    assert ledger.abelian_inverse_trace_coefficient == cy
    assert ledger.common_coefficient_residual == cy - c2
    assert ledger.angle_residual != 0


def test_homogeneous_abelian_moments_preserve_zero_under_rescaling() -> None:
    states = _declared_generation()
    rho = sp.Symbol("rho", positive=True)
    rescaled = tuple(
        WeightedChargeState(
            state.label,
            state.multiplicity,
            state.t3,
            rho * state.abelian_charge,
        )
        for state in states
    )
    assert weighted_abelian_moment(states, 1) == 0
    assert weighted_abelian_moment(states, 3) == 0
    assert weighted_abelian_moment(rescaled, 1) == 0
    assert weighted_abelian_moment(rescaled, 3) == 0


def test_nonzero_singlet_charge_flip_can_leave_the_trace_ratio_unchanged() -> None:
    states = list(_declared_generation())
    states[-1] = WeightedChargeState("e_R_conj", 1, 0, -1)
    flipped = finite_charge_trace_ledger(states)
    assert flipped.trace_ratio == sp.Rational(3, 8)
    assert flipped.trace_abelian_squared == sp.Rational(10, 3)


@pytest.mark.parametrize(
    "states,error",
    [
        ((), ValueError),
        ((WeightedChargeState("", 1, 0, 0),), ValueError),
        ((WeightedChargeState("a", 0, 0, 0),), ValueError),
        ((WeightedChargeState("a", 1, 0.5, 0),), ValueError),
        (
            (
                WeightedChargeState("a", 1, 0, 0),
                WeightedChargeState("a", 1, 0, 1),
            ),
            ValueError,
        ),
    ],
)
def test_invalid_state_tables_are_rejected(
    states: tuple[WeightedChargeState, ...], error: type[Exception]
) -> None:
    with pytest.raises(error):
        finite_charge_trace_ledger(states)


@pytest.mark.parametrize(
    "call",
    [
        lambda: abelian_normalization_ledger(_declared_generation(), 0, 1),
        lambda: abelian_normalization_ledger(_declared_generation(), 1, -1),
        lambda: charge_coupling_angle_ledger(0, 1, 1, 1),
        lambda: charge_coupling_angle_ledger(1, 1, 0, 1),
        lambda: common_trace_normalized_coupling_angle(1, 1, 0),
        lambda: weighted_abelian_moment(_declared_generation(), -1),
    ],
)
def test_invalid_normalization_and_coupling_domains_are_rejected(call: object) -> None:
    with pytest.raises(ValueError):
        call()
