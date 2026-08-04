from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.vacuum_polarization import (
    euclidean_transverse_projector,
    scalar_qed2_vacuum_polarization,
)


def test_euclidean_projector_is_transverse_only_away_from_zero_momentum() -> None:
    q0, q1 = sp.symbols("q0 q1", real=True)
    ledger = euclidean_transverse_projector((q0, q1))

    assert ledger.momentum_squared == q0**2 + q1**2
    assert ledger.idempotence_residual == sp.zeros(2)
    assert ledger.left_transversality_residual == sp.zeros(1, 2)
    assert ledger.right_transversality_residual == sp.zeros(2, 1)
    with pytest.raises(ValueError, match="zero momentum"):
        euclidean_transverse_projector((0, 0))


def test_scalar_qed2_closed_form_follows_from_real_parameter_integral() -> None:
    q2, mass, charge = sp.symbols("Q m e", positive=True)
    ledger = scalar_qed2_vacuum_polarization(q2, mass, charge)
    ratio = ledger.dimensionless_ratio
    y = ledger.real_parameter

    assert ledger.antiderivative_residual == 0
    endpoint_integral = sp.simplify(
        ledger.real_antiderivative.subs(y, 1)
        - sp.limit(ledger.real_antiderivative, y, 0)
    )
    expected_endpoint = sp.atanh(ratio) / ratio**3 - 1 / ratio**2
    assert sp.simplify(endpoint_integral - expected_endpoint) == 0

    transformed = sp.simplify(
        charge**2
        * q2
        / (sp.pi * (q2 + 4 * mass**2))
        * endpoint_integral
    )
    assert sp.simplify(transformed - ledger.projector_coefficient) == 0


def test_massive_scalar_generates_a_local_low_momentum_f_squared_term() -> None:
    q2, mass, charge = sp.symbols("Q m e", positive=True)
    ledger = scalar_qed2_vacuum_polarization(q2, mass, charge, species_count=3)

    assert sp.simplify(
        sp.limit(ledger.projector_coefficient / q2, q2, 0)
        - 3 * charge**2 / (12 * sp.pi * mass**2)
    ) == 0
    assert ledger.low_momentum_form_factor == charge**2 / (
        4 * sp.pi * mass**2
    )
    assert ledger.local_fmunu_squared_coefficient == charge**2 / (
        16 * sp.pi * mass**2
    )
    assert ledger.local_f01_squared_coefficient == charge**2 / (
        8 * sp.pi * mass**2
    )
    assert sp.limit(ledger.projector_coefficient, q2, 0) == 0


def test_massless_scalar_limit_is_not_the_fermionic_schwinger_coefficient() -> None:
    q2, mass, charge = sp.symbols("Q m e", positive=True)
    ledger = scalar_qed2_vacuum_polarization(q2, mass, charge)

    assert sp.limit(ledger.projector_coefficient, mass, 0, dir="+") == sp.oo
    assert ledger.massless_projector_limit == sp.oo
    assert ledger.projector_coefficient != charge**2 / sp.pi
    assert sp.limit(ledger.projector_coefficient, mass, sp.oo) == 0
    assert ledger.heavy_mass_projector_limit == 0


def test_scalar_bubble_and_seagull_are_both_load_bearing_for_ward_identity() -> None:
    q2, mass, charge = sp.symbols("Q m e", positive=True)
    ledger = scalar_qed2_vacuum_polarization(q2, mass, charge, species_count=2)

    assert ledger.bubble_ward_tadpole_coefficient == 4 * charge**2
    assert ledger.seagull_ward_tadpole_coefficient == -4 * charge**2
    assert ledger.ward_tadpole_residual == 0
    assert ledger.bubble_ward_tadpole_coefficient != 0
    assert ledger.bubble_ward_tadpole_coefficient - (
        ledger.seagull_ward_tadpole_coefficient
    ) != 0


def test_scalar_qed2_api_rejects_hidden_domain_choices() -> None:
    q2, mass, charge = sp.symbols("Q m e", positive=True)
    with pytest.raises(ValueError, match="momentum squared"):
        scalar_qed2_vacuum_polarization(0, mass, charge)
    with pytest.raises(ValueError, match="scalar mass"):
        scalar_qed2_vacuum_polarization(q2, 0, charge)
    with pytest.raises(ValueError, match="charge magnitude"):
        scalar_qed2_vacuum_polarization(q2, mass, 0)
    with pytest.raises(TypeError, match="integer"):
        scalar_qed2_vacuum_polarization(q2, mass, charge, 1.0)
    with pytest.raises(ValueError, match="species count"):
        scalar_qed2_vacuum_polarization(q2, mass, charge, 0)
