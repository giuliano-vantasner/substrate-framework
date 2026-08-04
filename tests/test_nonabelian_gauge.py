from __future__ import annotations

from pathlib import Path

import pytest
import sympy as sp

from substrate_framework.nonabelian_gauge import (
    NonAbelianGaugeLedger,
    local_nonabelian_gauge_ledger,
    nonabelian_covariant_derivative,
    nonabelian_field_strength,
    su2_projected_connection,
    su2_projected_unitary,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su2_doublets import (
    su2_chiral_factor_ledger,
    su2_same_carrier_projector_ledger,
)


def _zero(matrix: sp.MatrixBase) -> bool:
    return sp.Matrix(matrix).applyfunc(sp.simplify) == sp.zeros(*matrix.shape)


@pytest.fixture(scope="module")
def exact_local_ledger() -> NonAbelianGaugeLedger:
    time, coordinate = sp.symbols("t x", real=True)
    coupling = sp.symbols("g", positive=True)
    alpha = sp.Function("alpha", real=True)(time, coordinate)
    unitary = sp.diag(sp.exp(sp.I * alpha / 2), sp.exp(-sp.I * alpha / 2))
    generators = (
        sp.Matrix([[0, 1], [1, 0]]) / 2,
        sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2,
        sp.diag(1, -1) / 2,
    )
    components = [
        sp.Function(f"w{mu}{index}", real=True)(time, coordinate)
        for mu in range(2)
        for index in range(3)
    ]
    connections = tuple(
        sum(
            (
                components[3 * mu + index] * generators[index]
                for index in range(3)
            ),
            sp.zeros(2),
        )
        for mu in range(2)
    )
    field = sp.Matrix(
        [
            sp.Function("psi0")(time, coordinate),
            sp.Function("psi1")(time, coordinate),
        ]
    )
    return local_nonabelian_gauge_ledger(
        field,
        connections,
        unitary,
        (time, coordinate),
        coupling,
    )


def test_finite_local_transformation_is_covariant(
    exact_local_ledger: NonAbelianGaugeLedger,
) -> None:
    assert all(_zero(residual) for residual in exact_local_ledger.covariance_residuals)


def test_curvature_transforms_by_conjugation(
    exact_local_ledger: NonAbelianGaugeLedger,
) -> None:
    assert _zero(exact_local_ledger.curvature_covariance_residual)


def test_covariant_commutator_derives_curvature(
    exact_local_ledger: NonAbelianGaugeLedger,
) -> None:
    assert _zero(exact_local_ledger.commutator_curvature_residual)


def test_curvature_trace_square_is_gauge_invariant(
    exact_local_ledger: NonAbelianGaugeLedger,
) -> None:
    assert exact_local_ledger.trace_invariance_residual == 0


def test_opposite_inhomogeneous_sign_breaks_covariance() -> None:
    time = sp.symbols("t", real=True)
    coupling = sp.symbols("g", positive=True)
    alpha = sp.Function("alpha", real=True)(time)
    unitary = sp.diag(sp.exp(sp.I * alpha / 2), sp.exp(-sp.I * alpha / 2))
    field = sp.Matrix([sp.Function("p0")(time), sp.Function("p1")(time)])
    connection = sp.zeros(2)
    wrong = sp.simplify(
        unitary * connection * unitary.H
        + sp.I / coupling * unitary.diff(time) * unitary.H
    )
    residual = nonabelian_covariant_derivative(
        unitary * field,
        wrong,
        time,
        coupling,
    ) - unitary * nonabelian_covariant_derivative(
        field,
        connection,
        time,
        coupling,
    )
    assert not _zero(residual)


def test_noncommuting_connections_require_the_commutator_term() -> None:
    time, coordinate = sp.symbols("t x", real=True)
    coupling = sp.symbols("g", positive=True)
    first = sp.Matrix([[0, 1], [1, 0]]) / 2
    second = sp.Matrix([[0, -sp.I], [sp.I, 0]]) / 2
    curvature = nonabelian_field_strength(
        (first, second),
        (time, coordinate),
        coupling,
    )
    curl_only = second.diff(time) - first.diff(coordinate)
    assert not _zero(curvature)
    assert _zero(curl_only)
    assert not _zero(curvature - curl_only)


def test_commuting_connection_limit_reduces_to_the_curl() -> None:
    time, coordinate = sp.symbols("t x", real=True)
    coupling = sp.symbols("g", positive=True)
    generator = sp.diag(1, -1) / 2
    first = sp.Function("a", real=True)(time, coordinate) * generator
    second = sp.Function("b", real=True)(time, coordinate) * generator
    curvature = nonabelian_field_strength(
        (first, second),
        (time, coordinate),
        coupling,
    )
    assert _zero(
        curvature - second.diff(time) + first.diff(coordinate)
    )


def test_projected_su2_connection_uses_an_independent_factor() -> None:
    projector = sp.diag(1, 0)
    components = sp.symbols("W1 W2 W3", real=True)
    connection = su2_projected_connection(components, projector)
    carrier = su2_chiral_factor_ledger(projector)
    right_block = sp.kronecker_product(
        sp.eye(2),
        carrier.complementary_projector,
    )
    assert connection.shape == (4, 4)
    assert _zero(connection - connection.H)
    assert _zero(connection * right_block)
    assert all(_zero(residual) for residual in carrier.left_commutator_residuals)


def test_projected_su2_unitary_is_identity_on_the_right_block() -> None:
    angle = sp.symbols("alpha", real=True)
    isospin = sp.diag(sp.exp(sp.I * angle / 2), sp.exp(-sp.I * angle / 2))
    projector = sp.diag(1, 0)
    transformation = su2_projected_unitary(isospin, projector)
    carrier = su2_chiral_factor_ledger(projector)
    right_block = sp.kronecker_product(
        sp.eye(2),
        carrier.complementary_projector,
    )
    assert _zero(transformation.H * transformation - sp.eye(4))
    assert _zero(transformation * right_block - right_block)


def test_same_carrier_projector_is_not_a_valid_left_su2_action() -> None:
    ledger = su2_same_carrier_projector_ledger(sp.diag(1, 0))
    assert sum(_zero(residual) for residual in ledger.hermiticity_residuals) == 1
    assert not all(_zero(residual) for residual in ledger.commutator_residuals)


@pytest.mark.parametrize(
    "call",
    [
        lambda: local_nonabelian_gauge_ledger(
            sp.Matrix([1, 0]), (sp.zeros(2), sp.zeros(2)), sp.eye(2),
            (sp.Symbol("x"), sp.Symbol("x")), 1,
        ),
        lambda: local_nonabelian_gauge_ledger(
            sp.Matrix([1, 0]), (sp.zeros(2),), sp.eye(2),
            (sp.Symbol("t"), sp.Symbol("x")), 1,
        ),
        lambda: local_nonabelian_gauge_ledger(
            sp.Matrix([1, 0]), (sp.zeros(2), sp.zeros(2)), sp.diag(2, 1),
            (sp.Symbol("t"), sp.Symbol("x")), 1,
        ),
        lambda: local_nonabelian_gauge_ledger(
            sp.Matrix([1, 0]), (sp.zeros(2), sp.zeros(2)), sp.eye(2),
            (sp.Symbol("t"), sp.Symbol("x")), 0,
        ),
        lambda: local_nonabelian_gauge_ledger(
            sp.Matrix([1.0, 0]), (sp.zeros(2), sp.zeros(2)), sp.eye(2),
            (sp.Symbol("t"), sp.Symbol("x")), 1,
        ),
        lambda: su2_projected_connection((1, 2), sp.diag(1, 0)),
        lambda: su2_projected_connection((1, 2, sp.Symbol("w")), sp.diag(1, 0)),
        lambda: su2_projected_unitary(sp.diag(1, -1), sp.diag(1, 0)),
    ],
)
def test_nonabelian_ledger_rejects_invalid_exact_domains(call) -> None:
    with pytest.raises(ValueError):
        call()


def test_nonabelian_gauge_module_has_no_numpy_integration_shape() -> None:
    path = Path("src/substrate_framework/nonabelian_gauge.py")
    audit = audit_numpy_trapezoid_compatibility(
        path.read_text(encoding="utf-8"), filename=str(path)
    )
    assert audit.legacy_references == 0
    assert audit.current_references == 0
    assert audit.eager_legacy_default_fallbacks == 0
