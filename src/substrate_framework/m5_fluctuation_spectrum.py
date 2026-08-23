"""Confined-clock fluctuation census about the aligned M5 vacuum (P243).

The conditional P239 spectral-Cartan action is

    L = -1/2 <F_munu, F_munu>_h - V(spectrum)
        - kappa * eta^munu * q(d_mu P_t, d_nu P_t),

and its curvature two-form is quadratic in first derivatives of the order
parameter.  About an aligned vacuum (mixed ``X0 = eta^-1 M0`` diagonal with
distinct targets) the curvature sector therefore contributes nothing at
quadratic order: the free fluctuation theory is carried exactly by the pinned
spectrum potential, which supplies the stiffness matrix, and by the projector
current, which supplies the kinetic metric on the timelike-eigenvector orbit.

Exact first-order structure in the adapted frame (``t`` the simple timelike
index, distinct targets):

- potential orbit tangents preserve every trace power, so the stiffness is
  exactly zero on every off-diagonal direction;
- the projector variation is ``dP = du (u^T eta) + u (du^T eta)`` with the
  induced rotation ``eta(du, e_a) = w_mixed[a, t]/(lambda_t - lambda_a)``,
  so the projector bilinear sees only timelike-mixing directions;
- diagonal directions carry positive stiffness but no quadratic kinetics.

Classification per exact subspace:

- ``massive_stiff``: K > 0 and G = 0; static sectors without quadratic
  dynamics (their squared gaps are recorded from the potential Hessian);
- ``massless``: K = 0 and G > 0; propagating long-range sector with exactly
  zero gap;
- ``inert``: K = 0 and G = 0; no quadratic dynamics either way.

Units and conventions: mostly-plus Minkowski covariant order parameter,
targets ``(tau, lambda_1, lambda_2, lambda_3)`` with tau the simple timelike
value, potential weights per ``spectral_trace_potential``, projector bilinear
per ``projector_current_bilinear``.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations_with_replacement
from typing import Sequence

import sympy as sp

from .m5_covariant_action import (
    MINKOWSKI_MOSTLY_PLUS,
    projector_current_bilinear,
    spectral_trace_potential,
)


def _eta(dimension: int) -> sp.Matrix:
    return sp.Matrix(MINKOWSKI_MOSTLY_PLUS[:dimension, :dimension])


def _exact_targets(
    targets: Sequence[object],
) -> tuple[sp.Rational | sp.Integer, ...]:
    values = tuple(sp.nsimplify(sp.sympify(value)) for value in targets)
    for value in values:
        if not value.is_number:
            raise ValueError("targets must be exact numbers")
    return values  # type: ignore[return-value]


@dataclass(frozen=True)
class VacuumCensusLedger:
    """Exact free-fluctuation census of the aligned spectral-Cartan vacuum.

    ``stiffness`` and ``kinetic`` are the exact rational forms on the
    symmetric basis; the class counts follow from their exact nullspaces and
    the recorded gaps are exact rationals.
    """

    targets: tuple[sp.Expr, ...]
    weights: tuple[sp.Expr, ...]
    projector_stiffness: sp.Expr
    basis_dimension: int
    stiffness_rank: int
    kinetic_rank: int
    massless_count: int
    massive_stiff_gaps: tuple[sp.Expr, ...]
    inert_count: int
    kinetic_coefficients: tuple[sp.Expr, ...]
    stiffness: object
    kinetic: object


def _symmetric_basis(dimension: int) -> tuple[sp.Matrix, ...]:
    """Return elementary symmetric-matrix generators in canonical order."""

    basis = []
    for row, column in combinations_with_replacement(range(dimension), 2):
        matrix = sp.zeros(dimension, dimension)
        if row == column:
            matrix[row, column] = sp.Integer(1)
        else:
            matrix[row, column] = matrix[column, row] = sp.Integer(1)
        basis.append(sp.Matrix(matrix))
    return tuple(basis)


def aligned_vacuum(
    targets: Sequence[object],
) -> tuple[sp.Matrix, sp.Matrix]:
    """Return ``(M0 covariant, X0 mixed)`` with X0 diagonal in the targets."""

    values = _exact_targets(targets)
    dimension = len(values)
    eta = _eta(dimension)
    mixed = sp.diag(*values)
    covariant = eta * mixed
    return sp.Matrix(covariant), sp.Matrix(mixed)


def potential_stiffness_matrix(
    *,
    targets: Sequence[object],
    weights: Sequence[object] | None = None,
) -> tuple[tuple[sp.Matrix, ...], sp.Matrix]:
    """Return ``(basis, K)`` with ``V2(w) = w^T K w`` exactly.

    ``V2`` is the ``epsilon**2`` coefficient of the pinned trace-power
    potential evaluated at ``M0 + epsilon * w``; the off-diagonal entries
    come from the two-term polarization identity.
    """

    values = _exact_targets(targets)
    dimension = len(values)
    potential_weights = (
        (sp.Integer(1),) * dimension
        if weights is None
        else tuple(sp.sympify(value) for value in weights)
    )
    basis = _symmetric_basis(dimension)
    covariant, _ = aligned_vacuum(values)
    epsilon = sp.Symbol("_epsilon", positive=True)

    def second_coefficient(perturbation: sp.Matrix) -> sp.Expr:
        shifted = covariant + epsilon * perturbation
        series = sp.expand(
            spectral_trace_potential(
                shifted,
                values,
                _eta(dimension),
                potential_weights,
            )
        )
        return sp.cancel(series.coeff(epsilon, 2))

    size = len(basis)
    stiffness = sp.zeros(size, size)
    for index, element in enumerate(basis):
        stiffness[index, index] = second_coefficient(element)
    for first in range(size):
        for second in range(first + 1, size):
            pair = basis[first] + basis[second]
            cross = second_coefficient(pair) - stiffness[
                first, first
            ] - stiffness[second, second]
            entry = sp.cancel(cross / sp.Integer(2))
            stiffness[first, second] = entry
            stiffness[second, first] = entry
    return basis, sp.Matrix(stiffness)


def timelike_rotation_kinetic_metric(
    *,
    targets: Sequence[object],
    projector_stiffness: object = 1,
    basis: Sequence[sp.Matrix] | None = None,
) -> tuple[tuple[sp.Matrix, ...], sp.Matrix, list[sp.Matrix]]:
    """Return ``(basis, G, delta_projectors)`` for the projector current.

    The first variation of the timelike spectral projector at the aligned
    vacuum is ``dP = du (u^T eta) + u (du^T eta)`` with induced rotations
    ``eta(e_a, du) = w_mixed[a, t]/(lambda_t - lambda_a)`` on the adapted
    frame; ``u = e_t`` is the unit timelike eigenvector.  The kinetic form is
    ``G[w, w'] = kappa * q(dP[w], dP[w'])`` with the canonical bilinear.
    """

    values = _exact_targets(targets)
    dimension = len(values)
    eta = _eta(dimension)
    if basis is None:
        basis = _symmetric_basis(dimension)
    timelike = int(
        max(range(dimension), key=lambda index: values[index])
    )
    kappa = sp.sympify(projector_stiffness)
    size = len(basis)
    metric = sp.zeros(size, size)
    variations: list[sp.Matrix] = []
    for element in basis:
        mixed_element = eta * element
        du = sp.zeros(dimension, 1)
        for row in range(dimension):
            if row == timelike:
                continue
            du[row] = sp.cancel(
                mixed_element[row, timelike]
                / (values[timelike] - values[row])
            )
        u = sp.zeros(dimension, 1)
        u[timelike] = sp.Integer(1)
        # The timelike projector is P_t = -u (u^T eta) because eta(u, u)
        # is negative; its first variation carries the same overall sign.
        u_eta = u.T * eta
        delta = -(du * u_eta) - u * (du.T * eta)
        variations.append(sp.Matrix(delta))
    for first in range(size):
        for second in range(first, size):
            value = sp.cancel(
                kappa
                * projector_current_bilinear(
                    variations[first], variations[second]
                )
            )
            metric[first, second] = value
            metric[second, first] = value
    return tuple(basis), sp.Matrix(metric), variations


def certify_projector_variation(
    *,
    targets: Sequence[object],
    basis: Sequence[sp.Matrix] | None = None,
) -> list[int]:
    """Certify the analytic first variation by exact affine uniqueness.

    For each basis direction the true branch variation is the unique
    solution of the linearized defining system

        X0 dP + x P0 = lambda_t dP + dlambda P0   (right eigen-relation)
        dP X0 + P0 x = lambda_t dP + dlambda P0   (left eigen-relation)
        P0 dP + dP P0 = dP                        (idempotence)
        dP^T eta = eta dP                         (eta self-adjointness)

    in the unknowns ``(dP entries, dlambda)`` with ``x = eta * w`` the mixed
    perturbation.  The system is affine; the function checks per direction
    that (1) the analytic pair satisfies it exactly and (2) the associated
    homogeneous coefficient matrix has a trivial kernel, so distinct
    eigenvalues make the certified pair the only solution.  Returns a list
    of kernel dimensions (each must be 0; satisfaction failures record -1).
    """

    values = _exact_targets(targets)
    dimension = len(values)
    eta = _eta(dimension)
    if basis is None:
        basis = _symmetric_basis(dimension)
    timelike = int(max(range(dimension), key=lambda i: values[i]))
    mixed = sp.diag(*values)
    _, _, variations = timelike_rotation_kinetic_metric(
        targets=values, basis=basis
    )
    # P0 = -u (u^T eta) with u = e_t and eta(u,u) = -1 evaluates to the
    # single entry +1 at (t, t).
    projector_at = sp.zeros(dimension, dimension)
    projector_at[timelike, timelike] = sp.Integer(1)
    lambda_t = values[timelike]

    d_p = sp.symbols("dP0:16")
    dl = sp.Symbol("dl")
    d_p_matrix = sp.Matrix(4, 4, d_p)
    symbols = (*d_p, dl)

    dims: list[int] = []
    for element, delta in zip(basis, variations):
        perturbation = eta * element
        w_tt = perturbation[timelike, timelike]
        residual_blocks = [
            mixed * delta + perturbation * projector_at
            - lambda_t * delta - w_tt * projector_at,
            delta * mixed + projector_at * perturbation
            - lambda_t * delta - w_tt * projector_at,
            projector_at * delta + delta * projector_at - delta,
            delta.T * eta - eta * delta,
        ]
        satisfied = all(
            sp.simplify(entry) == 0
            for block in residual_blocks
            for entry in block
        )
        # Affine system A v = b split by constant part.
        symbolic_blocks = [
            mixed * d_p_matrix - lambda_t * d_p_matrix,
            d_p_matrix * mixed - lambda_t * d_p_matrix,
            projector_at * d_p_matrix + d_p_matrix * projector_at
            - d_p_matrix,
            d_p_matrix.T * eta - eta * d_p_matrix,
        ]
        constant_blocks = [
            perturbation * projector_at,
            projector_at * perturbation,
            sp.zeros(dimension, dimension),
            sp.zeros(dimension, dimension),
        ]
        dl_terms = [
            -dl * projector_at,
            -dl * projector_at,
            sp.zeros(dimension, dimension),
            sp.zeros(dimension, dimension),
        ]
        linear_rows = [
            sp.expand(sym_entry + dl_entry)
            for sym_block, dl_block in zip(symbolic_blocks, dl_terms)
            for sym_entry, dl_entry in zip(sym_block, dl_block)
        ]
        constant_rows = [
            -sp.expand(entry)
            for block in constant_blocks
            for entry in block
        ]
        matrix_a = sp.zeros(len(linear_rows), len(symbols))
        for row_index, row in enumerate(linear_rows):
            for column_index, symbol in enumerate(symbols):
                matrix_a[row_index, column_index] = row.coeff(symbol)
        rhs = sp.Matrix(constant_rows)
        analytic_vector = sp.Matrix(list(delta) + [w_tt])
        consistent = matrix_a * analytic_vector == rhs
        kernel_trivial = len(matrix_a.nullspace()) == 0
        dims.append(
            0 if (satisfied and consistent and kernel_trivial) else -1
        )
    return dims


def classify_census(
    *,
    targets: Sequence[object],
    weights: Sequence[object] | None = None,
    projector_stiffness: object = 1,
) -> VacuumCensusLedger:
    """Derive and classify the exact vacuum fluctuation census."""

    values = _exact_targets(targets)
    dimension = len(values)
    basis, stiffness = potential_stiffness_matrix(
        targets=values, weights=weights
    )
    _, kinetic, _ = timelike_rotation_kinetic_metric(
        targets=values, projector_stiffness=projector_stiffness, basis=basis
    )
    size = len(basis)

    def _column(matrix: sp.Matrix, index: int) -> sp.Matrix:
        return sp.Matrix([matrix[row, index] for row in range(size)])

    massless_count = 0
    inert_count = 0
    massive_stiff_gaps: list[sp.Expr] = []
    kinetic_coefficients: list[sp.Expr] = []
    for index in range(size):
        kinetic_zero = _column(kinetic, index) == sp.zeros(size, 1)
        stiff_zero = _column(stiffness, index) == sp.zeros(size, 1)
        if kinetic_zero and stiff_zero:
            inert_count += 1
        elif stiff_zero and not kinetic_zero:
            massless_count += 1
            kinetic_coefficients.append(sp.cancel(kinetic[index, index]))
        elif kinetic_zero and not stiff_zero:
            massive_stiff_gaps.append(sp.cancel(stiffness[index, index]))
        else:
            raise ValueError(
                "census classification met a joint nonzero direction; "
                "the declared vacuum structure does not hold"
            )
    return VacuumCensusLedger(
        targets=tuple(sp.Expr(v) for v in values),
        weights=tuple(
            sp.sympify(value)
            for value in (
                (sp.Integer(1),) * dimension
                if weights is None
                else weights
            )
        ),
        projector_stiffness=sp.sympify(projector_stiffness),
        basis_dimension=size,
        stiffness_rank=stiffness.rank(),
        kinetic_rank=kinetic.rank(),
        massless_count=massless_count,
        massive_stiff_gaps=tuple(massive_stiff_gaps),
        inert_count=inert_count,
        kinetic_coefficients=tuple(kinetic_coefficients),
        stiffness=stiffness,
        kinetic=kinetic,
    )
