"""Tests for exact gauge-field dimension and convention ledgers."""

from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.gauge_dimensions import (
    canonical_gauge_dimensions,
    connection_gauge_dimensions,
    four_dimensional_form_factor_examples,
    gauge_convention_translation,
    polarization_dimensions,
    representation_rescaling,
)
from substrate_framework.vacuum_polarization import (
    scalar_qed2_vacuum_polarization,
)


def test_symbolic_canonical_and_connection_ledgers() -> None:
    dimension = sp.Symbol("D", positive=True)
    canonical = canonical_gauge_dimensions(dimension)
    connection = connection_gauge_dimensions(dimension)

    assert canonical.potential == (dimension - 2) / 2
    assert canonical.coupling == (4 - dimension) / 2
    assert canonical.coupling_squared == 4 - dimension
    assert canonical.curvature == dimension / 2
    assert canonical.curvature_squared == dimension
    assert canonical.local_kinetic_coefficient == 0
    assert canonical.projector_coefficient == 2
    assert connection.connection_potential == 1
    assert connection.connection_curvature == 2
    assert connection.connection_curvature_squared == 4
    assert connection.kinetic_coefficient == dimension - 4


def test_convention_translation_preserves_the_density() -> None:
    coupling, coefficient = sp.symbols("g kappa", positive=True)
    ledger = gauge_convention_translation(4, coupling, coefficient)

    assert ledger.connection_potential == coupling * ledger.canonical_potential
    assert ledger.connection_curvature == coupling * ledger.canonical_curvature
    assert ledger.connection_coefficient == coefficient / coupling**2
    assert ledger.density_residual == 0
    assert ledger.connection_dimensions.kinetic_coefficient == 0


def test_two_dimensional_accepted_loop_coefficient_translates_exactly() -> None:
    momentum_squared, mass, coupling = sp.symbols("Q m g", positive=True)
    loop = scalar_qed2_vacuum_polarization(
        momentum_squared,
        mass,
        coupling,
        species_count=3,
    )
    translation = gauge_convention_translation(
        2,
        coupling,
        loop.local_fmunu_squared_coefficient,
    )

    assert loop.local_fmunu_squared_coefficient == 3 * coupling**2 / (
        48 * sp.pi * mass**2
    )
    assert translation.connection_coefficient == 3 / (48 * sp.pi * mass**2)
    assert translation.canonical_dimensions.local_kinetic_coefficient == 0
    assert translation.connection_dimensions.kinetic_coefficient == -2
    assert translation.density_residual == 0


def test_pure_coupling_result_and_mass_scale_counterfamily() -> None:
    dimension = sp.Symbol("D", positive=True)
    ledger = polarization_dimensions(dimension)

    assert ledger.pure_coupling_residual == 2 - dimension
    assert sp.solve(sp.Eq(ledger.pure_coupling_residual, 0), dimension) == [2]
    assert ledger.unique_pure_coupling_dimension == 2
    assert ledger.scale_completion_mass_power == dimension - 2
    assert ledger.scale_completed_dimension == 2
    assert ledger.scale_completed_residual == 0


def test_four_dimensional_dimensions_do_not_select_a_logarithm() -> None:
    momentum_squared, mass = sp.symbols("Q M", positive=True)
    examples = four_dimensional_form_factor_examples(momentum_squared, mass)

    assert all(residual == 0 for residual in examples.form_factor_scale_residuals)
    assert all(residual == 0 for residual in examples.projector_scale_residuals)
    assert sp.simplify(
        examples.constant_form_factor - examples.rational_form_factor
    ) != 0
    assert sp.simplify(
        examples.rational_form_factor - examples.logarithmic_form_factor
    ) != 0


def test_generator_and_coupling_rescaling_preserves_the_loop_weight() -> None:
    trace_index, coupling, scale = sp.symbols("T_R g rho", positive=True)
    ledger = representation_rescaling(trace_index, coupling, scale)

    assert ledger.rescaled_trace_index == scale**2 * trace_index
    assert ledger.rescaled_coupling == coupling / scale
    assert ledger.original_weight == coupling**2 * trace_index
    assert ledger.rescaled_weight == ledger.original_weight
    assert ledger.invariant_residual == 0


@pytest.mark.parametrize(
    ("function", "arguments"),
    [
        (canonical_gauge_dimensions, (4.0,)),
        (connection_gauge_dimensions, (-1,)),
        (gauge_convention_translation, (4, -1)),
        (polarization_dimensions, (0,)),
        (four_dimensional_form_factor_examples, (sp.Integer(1), -1)),
        (representation_rescaling, (sp.Integer(1), sp.Integer(1), 0)),
    ],
)
def test_dimension_apis_reject_inexact_or_nonpositive_inputs(
    function: object,
    arguments: tuple[object, ...],
) -> None:
    with pytest.raises(ValueError):
        function(*arguments)
