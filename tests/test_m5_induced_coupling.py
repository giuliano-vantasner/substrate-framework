"""Multi-species massless induced-coupling tests (P243, advances #163).

Closed-form expectations come from the accepted C-IGR-004 composition at
z=0 (J(0)=1, spread ratio R(0)=1) and the attempt-0003 record
Delta(1/G) = (1-6*xi)*N*Lambda^2/(12*pi); they are not read back from the
module under test.
"""

from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.m5_induced_coupling import (
    USABLE_MASSLESS_SCHEMES,
    massless_substrate_coupling,
    numeric_induced_shift,
    species_additivity_identity,
)
from substrate_framework.scalar_one_loop_mass import (
    SHARP_PROPER_TIME_REGULATOR,
    SMOOTH_PROPER_TIME_REGULATOR,
)


def _closed_form_delta(n: int, xi, lam) -> sp.Expr:
    return n * (1 - 6 * xi) * lam**2 / (12 * sp.pi)


def test_usable_massless_schemes_are_the_accepted_pair() -> None:
    assert USABLE_MASSLESS_SCHEMES == (
        SHARP_PROPER_TIME_REGULATOR,
        SMOOTH_PROPER_TIME_REGULATOR,
    )


@pytest.mark.parametrize("xi", [sp.Integer(0), sp.Rational(1, 10)])
def test_equal_mass_additivity_holds_exactly(xi) -> None:
    assert species_additivity_identity(
        field_counts=(2, 3),
        mass_squared=(sp.Rational(1, 4), sp.Rational(1, 4)),
        non_minimal_coupling=xi,
        cutoff=sp.Integer(1),
    )


def test_pooled_identity_requires_equal_species_masses() -> None:
    with pytest.raises(ValueError, match="equal species masses"):
        species_additivity_identity(
            field_counts=(2, 3),
            mass_squared=(sp.Rational(1, 4), sp.Integer(1)),
            non_minimal_coupling=0,
            cutoff=sp.Integer(1),
        )


def test_massless_ledger_matches_the_closed_form() -> None:
    ledger = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=0,
        cutoff=sp.Integer(1), baseline=0,
    )
    expected = _closed_form_delta(3, 0, sp.Integer(1))
    assert sp.simplify(ledger.induced_shift - expected) == 0
    assert sp.simplify(ledger.total_inverse_newton - expected) == 0
    assert sp.simplify(ledger.newton_constant - 4 * sp.pi) == 0
    assert ledger.scheme_values_equal is True


def test_selected_scale_ledger_reproduces_unblinded_values() -> None:
    """Lambda^2 = E_U - E_S mean from attempts/0005, entered as an exact
    decimal rational; the module cutoff parameter is Lambda itself, so the
    exact square root enters. The ledger must reproduce the unblinded
    Delta and G_total recorded after the structural freeze."""
    lam_squared = sp.Rational("0.26847204181661866")
    ledger = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=0,
        cutoff=sp.sqrt(lam_squared), baseline=0,
    )
    delta = ledger.induced_shift
    assert abs(float(delta) - 0.02136432626854447) < 1e-15
    assert abs(float(ledger.newton_constant) - 46.80699908016004) < 1e-9


def test_conformal_point_cancels_exactly() -> None:
    ledger = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=sp.Rational(1, 6),
        cutoff=sp.Integer(1),
    )
    assert ledger.induced_shift == 0
    assert ledger.total_inverse_newton == 0
    assert ledger.newton_constant is None


def test_superconformal_sign_flips_to_repulsive() -> None:
    ledger = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=sp.Rational(1, 5),
        cutoff=sp.Integer(1),
    )
    assert ledger.induced_shift.is_negative
    assert ledger.newton_constant < 0


def test_positive_baseline_adds_additively() -> None:
    b = sp.Rational(1, 7)
    ledger = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=0,
        cutoff=sp.Integer(1), baseline=b,
    )
    expected = b + _closed_form_delta(3, 0, sp.Integer(1))
    assert sp.simplify(ledger.total_inverse_newton - expected) == 0


def test_input_contracts_reject_nonpositive_and_inexact_values() -> None:
    with pytest.raises(ValueError):
        massless_substrate_coupling(massless_count=-1,
                                    non_minimal_coupling=0,
                                    cutoff=sp.Integer(1))
    with pytest.raises(ValueError):
        massless_substrate_coupling(massless_count=3,
                                    non_minimal_coupling=0,
                                    cutoff=0)
    with pytest.raises(ValueError, match="exact"):
        massless_substrate_coupling(massless_count=3,
                                    non_minimal_coupling=0.0,
                                    cutoff=sp.Integer(1))
    with pytest.raises(ValueError, match="exact"):
        massless_substrate_coupling(massless_count=3,
                                    non_minimal_coupling=sp.Integer(0),
                                    cutoff=1.0)


def test_numeric_evaluation_matches_closed_form_at_declared_precision() -> None:
    result = numeric_induced_shift(
        massless_count=3, non_minimal_coupling=sp.Integer(0),
        cutoff=sp.Integer(1), baseline=sp.Integer(0),
    )
    assert result["induced_shift"] == sp.N(1 / (4 * sp.pi), 30)
    assert result["newton_constant"] == sp.N(4 * sp.pi, 30)
    assert result["massless_count"] == 3
    assert result["baseline"] == sp.Integer(0)
    assert result["cutoff"] == sp.Integer(1)


def test_scheme_spread_ratio_is_exactly_one_at_z_zero() -> None:
    from substrate_framework.total_gravitational_coupling import (
        scheme_spread_ratio,
    )

    spread = scheme_spread_ratio(cutoff=sp.Integer(1), mass_squared=0)
    assert sp.simplify(spread.ratio - 1) == 0


def test_species_ledger_is_frozen() -> None:
    ledger = massless_substrate_coupling(
        massless_count=3, non_minimal_coupling=0, cutoff=sp.Integer(1),
    )
    with pytest.raises(Exception):
        ledger.induced_shift = sp.Integer(1)
