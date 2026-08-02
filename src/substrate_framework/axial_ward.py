"""Exact conditional axial-current and Goldberger--Treiman ledgers.

The APIs in this module keep the on-shell current convention, PCAC form-factor
identity, pion-pole assumption, analytic discrepancy premise, and parameter
identifiability separate.  They do not derive a QCD current, physical pion or
nucleon state, coupling value, chiral effective action, or substrate map.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import sympy as sp


def _positive(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number and expression.is_positive is not True:
        raise ValueError(f"{name} must be positive")
    return expression


def _real(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_number and expression.is_real is not True:
        raise ValueError(f"{name} must be real")
    return expression


def _variable(value: Any, name: str) -> sp.Symbol:
    if not isinstance(value, sp.Symbol):
        raise ValueError(f"{name} must be a SymPy symbol")
    return value


def _evaluated_limit(expression: sp.Expr, variable: sp.Symbol, point: Any) -> sp.Expr:
    result = sp.simplify(sp.limit(expression, variable, point))
    if result.has(sp.Limit) or result in (sp.oo, -sp.oo, sp.zoo, sp.nan):
        raise ValueError("required limit must exist as a finite evaluated expression")
    return result


@dataclass(frozen=True)
class AxialDimensionLedger:
    """Mass dimensions of the two terms inside the axial-current bracket."""

    axial_term_mass_dimension: sp.Expr
    induced_term_mass_dimension: sp.Expr
    dimension_residual: sp.Expr

    @property
    def convention_is_dimensionally_consistent(self) -> bool:
        """Whether the axial and induced-pseudoscalar terms have equal dimension."""

        return sp.simplify(self.dimension_residual) == 0


def axial_form_factor_dimension_ledger(
    *,
    axial_form_factor_mass_dimension: Any = 0,
    induced_form_factor_mass_dimension: Any = 0,
    induced_scale_mass_dimension: Any = 1,
) -> AxialDimensionLedger:
    """Return the dimension check for ``gamma_mu*G_A+q_mu*G_P/scale``.

    Momentum has mass dimension one.  Dimensionless ``G_A`` and ``G_P``
    therefore require a mass-dimension-one induced scale, conventionally
    ``2*M``.  Omitting that scale while retaining a dimensionless pole formula
    is inconsistent.
    """

    axial_dimension = _real(
        axial_form_factor_mass_dimension,
        "axial form-factor mass dimension",
    )
    induced_dimension = sp.simplify(
        1
        + _real(
            induced_form_factor_mass_dimension,
            "induced form-factor mass dimension",
        )
        - _real(induced_scale_mass_dimension, "induced scale mass dimension")
    )
    return AxialDimensionLedger(
        axial_term_mass_dimension=axial_dimension,
        induced_term_mass_dimension=induced_dimension,
        dimension_residual=sp.simplify(induced_dimension - axial_dimension),
    )


@dataclass(frozen=True)
class AxialDivergenceEvidence:
    """On-shell divergence in one explicit spacelike-transfer convention."""

    nucleon_mass: sp.Expr
    transfer_squared: sp.Expr
    axial_form_factor: sp.Expr
    induced_pseudoscalar_form_factor: sp.Expr
    induced_scale: sp.Expr
    unnormalized_divergence_coefficient: sp.Expr
    normalized_divergence_coefficient: sp.Expr


def on_shell_axial_divergence(
    nucleon_mass: Any,
    transfer_squared: Any,
    axial_form_factor: Any,
    induced_pseudoscalar_form_factor: Any,
    *,
    induced_scale: Any | None = None,
) -> AxialDivergenceEvidence:
    """Derive the coefficient after contracting a declared axial current.

    Use metric ``(+,-,-,-)``, ``q=p'-p``, and ``Q^2=-q^2``.  The declared
    matrix-element bracket is
    ``[gamma_mu*G_A+q_mu*G_P/scale]*gamma5``.  Equal-mass on-shell Dirac
    equations and gamma-five anticommutation give
    ``ubar*qslash*gamma5*u=2*M*ubar*gamma5*u``.  With the standard
    ``scale=2*M``, division by ``2*M`` yields
    ``G_A-Q^2*G_P/(4*M^2)`` because ``q^2=-Q^2``.
    """

    mass = _positive(nucleon_mass, "nucleon mass")
    q_squared = _real(transfer_squared, "transfer squared")
    axial = sp.sympify(axial_form_factor)
    induced = sp.sympify(induced_pseudoscalar_form_factor)
    scale = 2 * mass if induced_scale is None else _positive(
        induced_scale,
        "induced scale",
    )
    unnormalized = sp.simplify(2 * mass * axial - q_squared * induced / scale)
    return AxialDivergenceEvidence(
        nucleon_mass=mass,
        transfer_squared=q_squared,
        axial_form_factor=axial,
        induced_pseudoscalar_form_factor=induced,
        induced_scale=sp.simplify(scale),
        unnormalized_divergence_coefficient=unnormalized,
        normalized_divergence_coefficient=sp.simplify(unnormalized / (2 * mass)),
    )


@dataclass(frozen=True)
class GeneralizedAxialWardEvidence:
    """Exact conditional form-factor PCAC and pion-pole-dominance ledger."""

    transfer_variable: sp.Symbol
    nucleon_mass: sp.Expr
    pion_mass_squared: sp.Expr
    decay_scale: sp.Expr
    axial_form_factor: sp.Expr
    induced_pseudoscalar_form_factor: sp.Expr
    pion_nucleon_form_factor: sp.Expr
    normalized_divergence: sp.Expr
    pcac_pion_pole_source: sp.Expr
    generalized_identity_residual: sp.Expr
    pole_dominance_induced_form_factor: sp.Expr
    pole_dominance_reduced_residual: sp.Expr
    pion_pole_residue: sp.Expr
    coupling_at_zero_transfer: sp.Expr
    coupling_at_pion_pole: sp.Expr
    zero_transfer_gt_residual: sp.Expr
    pion_pole_gt_residual: sp.Expr


def generalized_axial_ward_evidence(
    transfer_variable: sp.Symbol,
    nucleon_mass: Any,
    pion_mass_squared: Any,
    decay_scale: Any,
    axial_form_factor: Any,
    induced_pseudoscalar_form_factor: Any,
    pion_nucleon_form_factor: Any,
) -> GeneralizedAxialWardEvidence:
    """Return a convention-complete generalized PCAC/GT identity.

    This function declares, rather than derives, the form-factor PCAC source
    ``F*m_pi^2*G_piNN/[M*(m_pi^2+Q^2)]``.  It also displays what the additional
    pion-pole-dominance ansatz
    ``G_P=4*M*F*G_piNN/(m_pi^2+Q^2)`` would imply.  The coupling is evaluated
    separately at ``Q^2=0`` and at the physical pion pole ``Q^2=-m_pi^2``.
    """

    q2 = _variable(transfer_variable, "transfer variable")
    mass = _positive(nucleon_mass, "nucleon mass")
    pion_mass2 = _positive(pion_mass_squared, "pion mass squared")
    scale = _positive(decay_scale, "decay scale")
    axial = sp.sympify(axial_form_factor)
    induced = sp.sympify(induced_pseudoscalar_form_factor)
    pion_nucleon = sp.sympify(pion_nucleon_form_factor)
    normalized = on_shell_axial_divergence(
        mass,
        q2,
        axial,
        induced,
    ).normalized_divergence_coefficient
    source = sp.simplify(
        scale * pion_mass2 * pion_nucleon / (mass * (pion_mass2 + q2))
    )
    ppd_induced = sp.simplify(
        4 * mass * scale * pion_nucleon / (pion_mass2 + q2)
    )
    ppd_normalized = on_shell_axial_divergence(
        mass,
        q2,
        axial,
        ppd_induced,
    ).normalized_divergence_coefficient
    coupling_zero = sp.simplify(pion_nucleon.subs(q2, 0))
    coupling_pole = _evaluated_limit(pion_nucleon, q2, -pion_mass2)
    axial_zero = sp.simplify(axial.subs(q2, 0))
    axial_pole = _evaluated_limit(axial, q2, -pion_mass2)
    return GeneralizedAxialWardEvidence(
        transfer_variable=q2,
        nucleon_mass=mass,
        pion_mass_squared=pion_mass2,
        decay_scale=scale,
        axial_form_factor=axial,
        induced_pseudoscalar_form_factor=induced,
        pion_nucleon_form_factor=pion_nucleon,
        normalized_divergence=normalized,
        pcac_pion_pole_source=source,
        generalized_identity_residual=sp.simplify(normalized - source),
        pole_dominance_induced_form_factor=ppd_induced,
        pole_dominance_reduced_residual=sp.simplify(ppd_normalized - source),
        pion_pole_residue=_evaluated_limit(
            (pion_mass2 + q2) * ppd_induced,
            q2,
            -pion_mass2,
        ),
        coupling_at_zero_transfer=coupling_zero,
        coupling_at_pion_pole=coupling_pole,
        zero_transfer_gt_residual=sp.simplify(
            mass * axial_zero - scale * coupling_zero
        ),
        pion_pole_gt_residual=sp.simplify(
            mass * axial_pole - scale * coupling_pole
        ),
    )


@dataclass(frozen=True)
class PionPoleRemainderEvidence:
    """Pion pole plus a separately visible regular induced-form-factor term."""

    full_induced_form_factor: sp.Expr
    generalized_identity_residual: sp.Expr
    reduced_residual: sp.Expr
    pion_pole_residue: sp.Expr
    zero_transfer_residual: sp.Expr


def pion_pole_remainder_evidence(
    transfer_variable: sp.Symbol,
    nucleon_mass: Any,
    pion_mass_squared: Any,
    decay_scale: Any,
    axial_form_factor: Any,
    pion_nucleon_form_factor: Any,
    regular_induced_remainder: Any,
) -> PionPoleRemainderEvidence:
    """Derive the exact Ward residual with a pole plus regular remainder.

    If the supplied remainder is finite at zero and at the pion pole, it does
    not change the pole residue and its zero-transfer contribution vanishes.
    It does change the generalized identity away from zero by
    ``-Q^2*R/(4*M^2)`` and therefore cannot be silently called pole dominance.
    """

    q2 = _variable(transfer_variable, "transfer variable")
    mass = _positive(nucleon_mass, "nucleon mass")
    pion_mass2 = _positive(pion_mass_squared, "pion mass squared")
    scale = _positive(decay_scale, "decay scale")
    axial = sp.sympify(axial_form_factor)
    pion_nucleon = sp.sympify(pion_nucleon_form_factor)
    remainder = sp.sympify(regular_induced_remainder)
    if _evaluated_limit(remainder, q2, 0).has(sp.oo, sp.zoo, sp.nan):
        raise ValueError("regular remainder must be finite at zero transfer")
    _evaluated_limit(remainder, q2, -pion_mass2)
    pole = sp.simplify(4 * mass * scale * pion_nucleon / (pion_mass2 + q2))
    full = sp.simplify(pole + remainder)
    evidence = generalized_axial_ward_evidence(
        q2,
        mass,
        pion_mass2,
        scale,
        axial,
        full,
        pion_nucleon,
    )
    reduced = sp.simplify(
        axial - scale * pion_nucleon / mass - q2 * remainder / (4 * mass**2)
    )
    return PionPoleRemainderEvidence(
        full_induced_form_factor=full,
        generalized_identity_residual=evidence.generalized_identity_residual,
        reduced_residual=reduced,
        pion_pole_residue=_evaluated_limit(
            (pion_mass2 + q2) * full,
            q2,
            -pion_mass2,
        ),
        zero_transfer_residual=sp.simplify(reduced.subs(q2, 0)),
    )


@dataclass(frozen=True)
class PCACLimitOrderEvidence:
    """Noncommuting limits of the pion-pole kernel."""

    kernel: sp.Expr
    zero_transfer_then_chiral: sp.Expr
    chiral_then_zero_transfer: sp.Expr
    fixed_ratio_path: sp.Expr


def pcac_limit_order_evidence(
    transfer_squared: sp.Symbol,
    pion_mass_squared: sp.Symbol,
    path_ratio: Any,
) -> PCACLimitOrderEvidence:
    """Evaluate both iterated limits of ``m_pi^2/(m_pi^2+Q^2)`` exactly."""

    q2 = _variable(transfer_squared, "transfer squared")
    mass2 = _variable(pion_mass_squared, "pion mass squared")
    ratio = _positive(path_ratio, "path ratio")
    kernel = sp.simplify(mass2 / (mass2 + q2))
    return PCACLimitOrderEvidence(
        kernel=kernel,
        zero_transfer_then_chiral=sp.limit(sp.limit(kernel, q2, 0), mass2, 0),
        chiral_then_zero_transfer=sp.limit(sp.limit(kernel, mass2, 0), q2, 0),
        fixed_ratio_path=sp.simplify(kernel.subs(q2, ratio * mass2)),
    )


@dataclass(frozen=True)
class AnalyticGTDiscrepancyEvidence:
    """Exact mass-squared factor under a declared regular coupling expansion."""

    coupling_at_zero: sp.Expr
    coupling_at_pion_pole: sp.Expr
    dimensionless_discrepancy: sp.Expr
    mass_squared_factor: sp.Expr
    leading_mass_squared_coefficient: sp.Expr
    chiral_limit: sp.Expr


def analytic_gt_discrepancy_evidence(
    pion_mass_squared: sp.Symbol,
    coupling_at_zero: Any,
    transfer_slope_at_zero: Any,
    quadratic_remainder_at_pole: Any,
) -> AnalyticGTDiscrepancyEvidence:
    """Derive an exact discrepancy from a declared regular pole-point expansion.

    Declare
    ``G_piNN(-m_pi^2)=g0-s*m_pi^2+R*m_pi^4`` and separately impose the
    zero-transfer relation ``M*g_A=F*g0``.  Then
    ``Delta_GT=1-M*g_A/(F*g_pole)=1-g0/g_pole`` has an exact factor of
    ``m_pi^2`` and tends to zero.  The slope and remainder are inputs; PCAC
    alone does not determine them.
    """

    mass2 = _variable(pion_mass_squared, "pion mass squared")
    g0 = _positive(coupling_at_zero, "zero-transfer coupling")
    slope = sp.sympify(transfer_slope_at_zero)
    remainder = sp.sympify(quadratic_remainder_at_pole)
    pole_coupling = sp.simplify(g0 - slope * mass2 + remainder * mass2**2)
    discrepancy = sp.simplify(1 - g0 / pole_coupling)
    return AnalyticGTDiscrepancyEvidence(
        coupling_at_zero=g0,
        coupling_at_pion_pole=pole_coupling,
        dimensionless_discrepancy=discrepancy,
        mass_squared_factor=sp.factor(discrepancy / mass2),
        leading_mass_squared_coefficient=sp.simplify(
            sp.limit(discrepancy / mass2, mass2, 0)
        ),
        chiral_limit=sp.simplify(sp.limit(discrepancy, mass2, 0)),
    )


@dataclass(frozen=True)
class GTRelationLedger:
    """Parameter rank and exact rescaling families of a supplied GT equation."""

    relation_residual: sp.Expr
    solved_axial_charge: sp.Expr
    solved_pion_nucleon_coupling: sp.Expr
    monomial_exponent_row: sp.ImmutableMatrix
    exponent_nullspace: sp.ImmutableMatrix
    independent_parameter_directions: int
    common_scale_covariance_residual: sp.Expr
    inverse_decay_coupling_residual: sp.Expr
    inverse_mass_axial_residual: sp.Expr


def gt_relation_ledger(
    pion_nucleon_coupling: Any,
    decay_scale: Any,
    axial_charge: Any,
    nucleon_mass: Any,
    rescaling_parameter: Any,
) -> GTRelationLedger:
    """Expose the three free directions in ``g_piNN*F=M*g_A`` exactly."""

    coupling = _positive(pion_nucleon_coupling, "pion-nucleon coupling")
    scale = _positive(decay_scale, "decay scale")
    axial = _positive(axial_charge, "axial charge")
    mass = _positive(nucleon_mass, "nucleon mass")
    rho = _positive(rescaling_parameter, "rescaling parameter")
    residual = sp.simplify(coupling * scale - axial * mass)
    exponent_row = sp.ImmutableMatrix([[1, 1, -1, -1]])
    null_columns = sp.Matrix(exponent_row).nullspace()
    nullspace = sp.ImmutableMatrix.hstack(
        *(sp.ImmutableMatrix(column) for column in null_columns)
    )
    return GTRelationLedger(
        relation_residual=residual,
        solved_axial_charge=sp.simplify(coupling * scale / mass),
        solved_pion_nucleon_coupling=sp.simplify(axial * mass / scale),
        monomial_exponent_row=exponent_row,
        exponent_nullspace=nullspace,
        independent_parameter_directions=int(nullspace.cols),
        common_scale_covariance_residual=sp.simplify(
            coupling * (rho * scale) - axial * (rho * mass) - rho * residual
        ),
        inverse_decay_coupling_residual=sp.simplify(
            (rho * coupling) * (scale / rho) - axial * mass - residual
        ),
        inverse_mass_axial_residual=sp.simplify(
            coupling * scale - (rho * axial) * (mass / rho) - residual
        ),
    )
