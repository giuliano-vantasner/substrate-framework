from __future__ import annotations

import pytest
import sympy as sp

from substrate_framework.gauge_scalar_mass import (
    gauge_scalar_mass_evidence,
    positive_gauge_kinetic_mass_evidence,
    su2_u1_lower_doublet_mass_evidence,
    transform_gauge_quadratic_forms,
)


def test_general_gram_identity_and_real_stabilizer_kernel() -> None:
    g, v = sp.symbols("g v", positive=True)
    generators = (
        sp.diag(1, 0),
        sp.diag(0, 1),
        sp.Matrix([[0, 1], [1, 0]]),
    )
    evidence = gauge_scalar_mass_evidence(
        generators,
        (g, g, g),
        sp.Matrix([v, 0]),
    )

    assert evidence.gram_identity_certified
    assert evidence.stabilizer_kernel_certified
    assert evidence.mass_matrix == 2 * g**2 * v**2 * sp.diag(1, 0, 1)
    assert evidence.orbit_rank == evidence.mass_rank == 2
    assert evidence.coefficient_kernel_dimension == 1
    assert evidence.generator_basis_independent
    assert evidence.stabilizer_dimension == 1


def test_quadratic_density_uses_one_half_real_field_convention() -> None:
    a, b = sp.symbols("a b", real=True)
    evidence = gauge_scalar_mass_evidence(
        (sp.diag(1, 0), sp.diag(0, 1)),
        (sp.Integer(1), sp.Integer(1)),
        sp.Matrix([1, sp.I]),
    )

    assert evidence.mass_matrix == 2 * sp.eye(2)
    assert evidence.quadratic_density((a, b)) == a**2 + b**2
    with pytest.raises(ValueError, match="match the generator count"):
        evidence.quadratic_density((a,))


def test_real_coefficients_exclude_a_complex_only_column_relation() -> None:
    sigma_x = sp.Matrix([[0, 1], [1, 0]])
    sigma_y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    evidence = gauge_scalar_mass_evidence(
        (sigma_x, sigma_y),
        (sp.Integer(1), sp.Integer(1)),
        sp.Matrix([1, 0]),
    )

    assert evidence.coupled_orbit_vectors[:, 1] == sp.I * evidence.coupled_orbit_vectors[:, 0]
    assert evidence.real_orbit_map.rank() == 2
    assert evidence.coefficient_kernel_dimension == 0
    assert evidence.mass_matrix == 2 * sp.eye(2)


def test_dependent_generators_and_zero_couplings_block_stabilizer_label() -> None:
    dependent = gauge_scalar_mass_evidence(
        (sp.eye(1), sp.eye(1)),
        (sp.Integer(1), sp.Integer(1)),
        sp.Matrix([1]),
    )
    assert not dependent.generator_basis_independent
    with pytest.raises(ValueError, match="independent generator basis"):
        _ = dependent.stabilizer_dimension

    uncoupled = gauge_scalar_mass_evidence(
        (sp.diag(1, 0), sp.diag(0, 1)),
        (sp.Integer(1), sp.Integer(0)),
        sp.Matrix([1, 1]),
    )
    assert not uncoupled.all_couplings_nonzero
    with pytest.raises(ValueError, match="nonzero couplings"):
        _ = uncoupled.stabilizer_dimension


def test_positive_kinetic_metric_changes_raw_mass_eigenvalue() -> None:
    mass = sp.diag(6, 0)
    kinetic = sp.diag(3, 2)
    lam = sp.symbols("lam", real=True)
    evidence = positive_gauge_kinetic_mass_evidence(
        mass,
        kinetic,
        spectral_parameter=lam,
    )

    assert evidence.generalized_mass_operator == sp.diag(2, 0)
    assert sp.factor(evidence.generalized_characteristic_polynomial) == 6 * lam * (lam - 2)
    assert evidence.kernel_certified


def test_congruence_flips_neutral_sign_without_changing_spectrum() -> None:
    g, gp, v = sp.symbols("g gp v", positive=True)
    doublet = su2_u1_lower_doublet_mass_evidence(g, gp, v)
    sign_flip = sp.diag(1, -1)
    congruence = transform_gauge_quadratic_forms(
        doublet.neutral_mass_matrix,
        sp.eye(2),
        sign_flip,
    )

    assert congruence.transformed_mass_matrix[0, 1] == g * gp * v**2 / 4
    assert congruence.original_nullity == congruence.transformed_nullity == 1
    assert congruence.generalized_spectrum_covariant
    assert congruence.transformed_kinetic_metric == sp.eye(2)


def test_su2_u1_lower_doublet_specialization() -> None:
    g, gp, v = sp.symbols("g gp v", positive=True)
    result = su2_u1_lower_doublet_mass_evidence(g, gp, v)
    expected = v**2 / 4 * sp.Matrix(
        [
            [g**2, 0, 0, 0],
            [0, g**2, 0, 0],
            [0, 0, g**2, -g * gp],
            [0, 0, -g * gp, gp**2],
        ]
    )

    assert result.general_evidence.mass_matrix == expected
    assert result.general_evidence.mass_rank == 3
    assert result.general_evidence.stabilizer_dimension == 1
    assert result.charge_vacuum_residual == sp.zeros(2, 1)
    assert result.neutral_mass_matrix * result.neutral_null_vector == sp.zeros(2, 1)
    assert sp.simplify(
        result.neutral_mass_matrix * result.neutral_massive_vector
        - result.neutral_mass_squared * result.neutral_massive_vector
    ) == sp.zeros(2, 1)
    assert result.charged_mass_squared == g**2 * v**2 / 4
    assert result.rho == 1


def test_alternative_triplet_vacuum_changes_rank_and_coefficients() -> None:
    g, v = sp.symbols("g v", positive=True)
    root_two = sp.sqrt(2)
    generators = (
        sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) / root_two,
        sp.Matrix([[0, -sp.I, 0], [sp.I, 0, -sp.I], [0, sp.I, 0]]) / root_two,
        sp.diag(1, 0, -1),
    )
    triplet = gauge_scalar_mass_evidence(
        generators,
        (g, g, g),
        sp.Matrix([0, v, 0]),
    )

    assert triplet.mass_matrix == sp.diag(2 * g**2 * v**2, 2 * g**2 * v**2, 0)
    assert triplet.mass_rank == 2
    assert triplet.stabilizer_dimension == 1


@pytest.mark.parametrize(
    ("generators", "couplings", "vacuum", "message"),
    [
        ((), (), (), "generators must be nonempty"),
        ((sp.eye(2),), (1,), sp.Matrix([[1, 0]]), "column vector"),
        ((sp.Matrix([[0, 1], [0, 0]]),), (1,), sp.Matrix([1, 0]), "Hermitian"),
        ((sp.eye(1),), (sp.I,), sp.Matrix([1]), "explicitly real"),
        ((sp.eye(1),), (1.0,), sp.Matrix([1]), "exact"),
    ],
)
def test_general_input_validation(
    generators: tuple[object, ...],
    couplings: tuple[object, ...],
    vacuum: object,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        gauge_scalar_mass_evidence(generators, couplings, vacuum)  # type: ignore[arg-type]


def test_positive_kinetic_and_congruence_input_validation() -> None:
    with pytest.raises(ValueError, match="positive definite"):
        positive_gauge_kinetic_mass_evidence(sp.eye(2), sp.diag(1, 0))
    with pytest.raises(ValueError, match="symmetric"):
        positive_gauge_kinetic_mass_evidence(sp.eye(2), sp.Matrix([[1, 1], [0, 1]]))
    with pytest.raises(ValueError, match="invertible"):
        transform_gauge_quadratic_forms(sp.eye(2), sp.eye(2), sp.diag(1, 0))


def test_doublet_requires_exact_positive_inputs() -> None:
    with pytest.raises(ValueError, match="explicitly positive"):
        su2_u1_lower_doublet_mass_evidence(sp.Integer(1), sp.Integer(-1), sp.Integer(1))
    with pytest.raises(ValueError, match="exact"):
        su2_u1_lower_doublet_mass_evidence(1.0, sp.Integer(1), sp.Integer(1))
