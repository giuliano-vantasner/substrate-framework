from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.nonabelian_vacuum_polarization import (
    SU2ScalarVacuumPolarization,
    su2_scalar_qed2_vacuum_polarization,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility


def _fundamental_generators() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )


def _adjoint_generators() -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    return (
        sp.Matrix([[0, 0, 0], [0, 0, -sp.I], [0, sp.I, 0]]),
        sp.Matrix([[0, 0, sp.I], [0, 0, 0], [-sp.I, 0, 0]]),
        sp.Matrix([[0, -sp.I, 0], [sp.I, 0, 0], [0, 0, 0]]),
    )


@pytest.fixture(scope="module")
def symbols() -> tuple[sp.Symbol, sp.Symbol, sp.Symbol]:
    return sp.symbols("Q m g", positive=True)


def test_fundamental_representation_multiplies_the_scalar_kernel_by_one_half(
    symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> None:
    q2, mass, coupling = symbols
    ledger = su2_scalar_qed2_vacuum_polarization(
        _fundamental_generators(), q2, mass, coupling, species_count=2
    )

    assert isinstance(ledger, SU2ScalarVacuumPolarization)
    assert ledger.dynkin_index == sp.Rational(1, 2)
    assert ledger.trace_metric == sp.eye(3) / 2
    assert ledger.trace_metric_residual == sp.zeros(3)
    assert all(residual == sp.zeros(2) for residual in ledger.commutator_residuals)
    assert ledger.color_projector_coefficient == (
        sp.eye(3) * ledger.abelian_ledger.projector_coefficient / 2
    )
    assert ledger.ward_tadpole_residual == sp.zeros(3)


def test_adjoint_and_direct_sum_examples_expose_representation_index(
    symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> None:
    q2, mass, coupling = symbols
    adjoint = su2_scalar_qed2_vacuum_polarization(
        _adjoint_generators(), q2, mass, coupling
    )
    doubled = su2_scalar_qed2_vacuum_polarization(
        tuple(sp.diag(generator, generator) for generator in _fundamental_generators()),
        q2,
        mass,
        coupling,
    )

    assert adjoint.carrier_dimension == 3
    assert adjoint.dynkin_index == 2
    assert doubled.carrier_dimension == 4
    assert doubled.dynkin_index == 1
    assert sp.simplify(
        adjoint.local_component_fmunu_squared_coefficient
        / doubled.local_component_fmunu_squared_coefficient
    ) == 2


def test_component_and_trace_density_coefficients_are_typed_separately(
    symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> None:
    q2, mass, coupling = symbols
    ledger = su2_scalar_qed2_vacuum_polarization(
        _fundamental_generators(), q2, mass, coupling, species_count=3
    )

    assert ledger.local_trace_fmunu_squared_coefficient == (
        coupling**2 / (16 * sp.pi * mass**2)
    )
    assert ledger.local_component_fmunu_squared_coefficient == (
        coupling**2 / (32 * sp.pi * mass**2)
    )
    assert sp.simplify(
        ledger.local_component_fmunu_squared_coefficient
        - ledger.dynkin_index * ledger.local_trace_fmunu_squared_coefficient
    ) == 0


def test_background_field_coefficient_independently_closes_local_invariant(
    symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> None:
    q2, mass, coupling = symbols
    ledger = su2_scalar_qed2_vacuum_polarization(
        _fundamental_generators(), q2, mass, coupling
    )

    assert ledger.heat_kernel_curvature_weight == sp.Rational(1, 12)
    assert ledger.heat_kernel_free_factor == 1 / (4 * sp.pi)
    assert ledger.proper_time_mass_integral == 1 / mass**2
    assert ledger.heat_kernel_trace_fmunu_squared_coefficient == (
        coupling**2 / (48 * sp.pi * mass**2)
    )
    assert ledger.covariant_completion_residual == 0
    wrong_real_scalar_prefactor = (
        ledger.heat_kernel_trace_fmunu_squared_coefficient / 2
    )
    assert sp.simplify(
        wrong_real_scalar_prefactor
        - ledger.local_trace_fmunu_squared_coefficient
    ) != 0


def test_limits_and_scalar_numerator_reject_YM1_massless_scaffold(
    symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> None:
    q2, mass, coupling = symbols
    ledger = su2_scalar_qed2_vacuum_polarization(
        _fundamental_generators(), q2, mass, coupling
    )
    x = ledger.abelian_ledger.parameter

    assert sp.factor(ledger.abelian_ledger.projector_parameter_integrand).has(
        (2 * x - 1) ** 2
    )
    assert ledger.abelian_ledger.massless_projector_limit == sp.oo
    assert ledger.abelian_ledger.heavy_mass_projector_limit == 0
    assert ledger.abelian_ledger.zero_momentum_projector_limit == 0
    assert ledger.color_projector_coefficient != (
        sp.eye(3) * coupling**2 / (2 * sp.pi)
    )


def test_bubble_seagull_and_representation_factor_are_load_bearing(
    symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> None:
    q2, mass, coupling = symbols
    ledger = su2_scalar_qed2_vacuum_polarization(
        _fundamental_generators(), q2, mass, coupling, species_count=2
    )

    assert ledger.bubble_ward_tadpole_coefficient == 2 * coupling**2 * sp.eye(3)
    assert ledger.seagull_ward_tadpole_coefficient == -2 * coupling**2 * sp.eye(3)
    assert ledger.ward_tadpole_residual == sp.zeros(3)
    assert (
        ledger.bubble_ward_tadpole_coefficient
        - ledger.seagull_ward_tadpole_coefficient
    ) != sp.zeros(3)
    assert ledger.color_projector_coefficient != (
        sp.eye(3) * ledger.abelian_ledger.projector_coefficient
    )


@pytest.mark.parametrize(
    "generators, error",
    [
        (_fundamental_generators()[:2], "exactly three"),
        (
            (_fundamental_generators()[0], sp.eye(3), _fundamental_generators()[2]),
            "common square shape",
        ),
        (
            (
                sp.Matrix([[0, 1], [0, 0]]),
                _fundamental_generators()[1],
                _fundamental_generators()[2],
            ),
            "Hermitian",
        ),
        (
            tuple(2 * generator for generator in _fundamental_generators()),
            "commutators",
        ),
        (
            tuple(generator.evalf() for generator in _fundamental_generators()),
            "exact entries",
        ),
    ],
)
def test_representation_validation_rejects_hidden_normalization(
    generators, error: str, symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
) -> None:
    q2, mass, coupling = symbols
    with pytest.raises(ValueError, match=error):
        su2_scalar_qed2_vacuum_polarization(
            generators, q2, mass, coupling
        )


def test_api_rejects_inexact_or_nonpositive_continuous_inputs(
    symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> None:
    q2, mass, coupling = symbols
    with pytest.raises(ValueError, match="momentum squared"):
        su2_scalar_qed2_vacuum_polarization(
            _fundamental_generators(), 1.0, mass, coupling
        )
    with pytest.raises(ValueError, match="scalar mass"):
        su2_scalar_qed2_vacuum_polarization(
            _fundamental_generators(), q2, 0, coupling
        )
    with pytest.raises(ValueError, match="coupling"):
        su2_scalar_qed2_vacuum_polarization(
            _fundamental_generators(), q2, mass, 0
        )
    with pytest.raises(TypeError, match="integer"):
        su2_scalar_qed2_vacuum_polarization(
            _fundamental_generators(), q2, mass, coupling, species_count=1.0
        )


def test_module_has_no_numpy_integration_shape() -> None:
    path = Path("src/substrate_framework/nonabelian_vacuum_polarization.py")
    audit = audit_numpy_trapezoid_compatibility(
        path.read_text(encoding="utf-8"), filename=str(path)
    )
    assert audit.legacy_references == 0
    assert audit.current_references == 0
    assert audit.eager_legacy_default_fallbacks == 0
