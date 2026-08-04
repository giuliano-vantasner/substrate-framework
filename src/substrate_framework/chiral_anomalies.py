"""Exact anomaly coefficients for separately supplied chiral multiplets.

The coefficient formulas in this module are an explicitly imported piece of
four-dimensional chiral gauge theory.  The implementation derives exact sums,
homogeneity, and the complete zero set of one fixed five-row local system.  It
does not derive the supplied representations, a physical matter sector, a
global gauge group, Yukawa interactions, observed charges, or a substrate map.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence

import sympy as sp


@dataclass(frozen=True)
class ChiralGaugeMultiplet:
    """One left-handed row for ``G_a x SU(2) x U(1)``.

    Quadratic indices are unsigned, while ``factor_a_cubic_index`` carries the
    representation/conjugate-representation sign.  The final Boolean is a
    supplied indicator for a fundamental ``G_b = SU(2)`` doublet; it is not a
    generic classifier for higher SU(2) representations.
    """

    label: str
    factor_a_dimension: int
    factor_b_dimension: int
    abelian_charge: Any
    factor_a_quadratic_index: Any
    factor_b_quadratic_index: Any
    factor_a_cubic_index: Any
    factor_b_fundamental_doublet: bool


@dataclass(frozen=True)
class ChiralAnomalyLedger:
    """Exact ``G_a x SU(2) x U(1)`` coefficients and doublet parity."""

    multiplets: tuple[ChiralGaugeMultiplet, ...]
    mixed_factor_a_squared_abelian: sp.Expr
    mixed_factor_b_squared_abelian: sp.Expr
    abelian_cubed: sp.Expr
    mixed_gravity_squared_abelian: sp.Expr
    factor_a_cubed: sp.Expr
    factor_b_fundamental_doublet_count: int
    factor_b_fundamental_doublet_parity_even: bool
    local_coefficients: tuple[sp.Expr, ...]
    local_anomalies_cancel: bool
    all_supplied_conditions_cancel: bool


@dataclass(frozen=True)
class FiveRowAnomalyBranch:
    """One affine line in the complete fixed-carrier local zero set."""

    name: str
    parameter: sp.Symbol
    charges: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr]


@dataclass(frozen=True)
class FiveRowLocalAnomalySolutionVariety:
    """Elimination and all irreducible lines of the five-row local system."""

    charge_symbols: tuple[sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol, sp.Symbol]
    normalized_local_equations: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]
    linear_solution: tuple[tuple[sp.Symbol, sp.Expr], ...]
    reduced_cubic: sp.Expr
    branches: tuple[FiveRowAnomalyBranch, ...]


@dataclass(frozen=True)
class FiveRowSolutionMembership:
    """Exact residuals and component membership for one five-charge tuple."""

    charges: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr, sp.Expr]
    normalized_local_residuals: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]
    is_solution: bool
    matching_branches: tuple[str, ...]


def _exact_real(value: Any, name: str) -> sp.Expr:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an exact real scalar")
    expression = sp.sympify(value)
    if expression.has(sp.Float):
        raise ValueError(f"{name} must be exact rather than floating")
    if expression.is_real is not True:
        raise ValueError(f"{name} must be provably real")
    return sp.simplify(expression)


def _nonnegative_exact(value: Any, name: str) -> sp.Expr:
    expression = _exact_real(value, name)
    if expression.is_nonnegative is not True:
        raise ValueError(f"{name} must be nonnegative")
    return expression


def _positive_integer(value: Any, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a positive integer")
    expression = sp.sympify(value)
    if (
        expression.is_number is not True
        or expression.is_integer is not True
        or expression.is_positive is not True
    ):
        raise ValueError(f"{name} must be a positive integer")
    return int(expression)


def _normalize_multiplet(
    multiplet: ChiralGaugeMultiplet,
    index: int,
) -> ChiralGaugeMultiplet:
    if not isinstance(multiplet, ChiralGaugeMultiplet):
        raise TypeError("multiplets must contain ChiralGaugeMultiplet records")
    if not isinstance(multiplet.label, str) or not multiplet.label.strip():
        raise ValueError("multiplet labels must be non-empty strings")
    if not isinstance(multiplet.factor_b_fundamental_doublet, bool):
        raise ValueError("factor_b_fundamental_doublet must be Boolean")
    prefix = f"multiplets[{index}]"
    factor_a_dimension = _positive_integer(
        multiplet.factor_a_dimension,
        f"{prefix}.factor_a_dimension",
    )
    factor_b_dimension = _positive_integer(
        multiplet.factor_b_dimension,
        f"{prefix}.factor_b_dimension",
    )
    if multiplet.factor_b_fundamental_doublet and factor_b_dimension != 2:
        raise ValueError("a supplied fundamental SU(2) doublet must have dimension two")
    return ChiralGaugeMultiplet(
        label=multiplet.label,
        factor_a_dimension=factor_a_dimension,
        factor_b_dimension=factor_b_dimension,
        abelian_charge=_exact_real(
            multiplet.abelian_charge,
            f"{prefix}.abelian_charge",
        ),
        factor_a_quadratic_index=_nonnegative_exact(
            multiplet.factor_a_quadratic_index,
            f"{prefix}.factor_a_quadratic_index",
        ),
        factor_b_quadratic_index=_nonnegative_exact(
            multiplet.factor_b_quadratic_index,
            f"{prefix}.factor_b_quadratic_index",
        ),
        factor_a_cubic_index=_exact_real(
            multiplet.factor_a_cubic_index,
            f"{prefix}.factor_a_cubic_index",
        ),
        factor_b_fundamental_doublet=multiplet.factor_b_fundamental_doublet,
    )


def _normalize_multiplets(
    multiplets: Iterable[ChiralGaugeMultiplet],
) -> tuple[ChiralGaugeMultiplet, ...]:
    table = tuple(
        _normalize_multiplet(multiplet, index)
        for index, multiplet in enumerate(multiplets)
    )
    if not table:
        raise ValueError("at least one multiplet is required")
    labels = tuple(multiplet.label for multiplet in table)
    if len(set(labels)) != len(labels):
        raise ValueError("multiplet labels must be unique provenance keys")
    return table


def chiral_anomaly_ledger(
    multiplets: Iterable[ChiralGaugeMultiplet],
) -> ChiralAnomalyLedger:
    """Evaluate supplied ``G_a x SU(2) x U(1)`` coefficients exactly.

    The local tuple is ordered as ``G_a^2 U(1)``, ``G_b^2 U(1)``,
    ``U(1)^3``, ``gravity^2 U(1)``, and ``G_a^3``.  The separate parity field
    applies only when the supplied Boolean marks all fundamental SU(2)
    doublets. Higher-representation SU(2) global anomalies are outside this
    ledger, and the API does not silently classify them.
    """

    table = _normalize_multiplets(multiplets)
    mixed_a = sp.simplify(
        sum(
            row.factor_b_dimension
            * row.factor_a_quadratic_index
            * row.abelian_charge
            for row in table
        )
    )
    mixed_b = sp.simplify(
        sum(
            row.factor_a_dimension
            * row.factor_b_quadratic_index
            * row.abelian_charge
            for row in table
        )
    )
    abelian_cubed = sp.simplify(
        sum(
            row.factor_a_dimension
            * row.factor_b_dimension
            * row.abelian_charge**3
            for row in table
        )
    )
    mixed_gravity = sp.simplify(
        sum(
            row.factor_a_dimension
            * row.factor_b_dimension
            * row.abelian_charge
            for row in table
        )
    )
    factor_a_cubed = sp.simplify(
        sum(row.factor_b_dimension * row.factor_a_cubic_index for row in table)
    )
    doublet_count = sum(
        row.factor_a_dimension
        for row in table
        if row.factor_b_fundamental_doublet
    )
    local_coefficients = (
        mixed_a,
        mixed_b,
        abelian_cubed,
        mixed_gravity,
        factor_a_cubed,
    )
    local_cancel = all(coefficient == 0 for coefficient in local_coefficients)
    parity_even = doublet_count % 2 == 0
    return ChiralAnomalyLedger(
        multiplets=table,
        mixed_factor_a_squared_abelian=mixed_a,
        mixed_factor_b_squared_abelian=mixed_b,
        abelian_cubed=abelian_cubed,
        mixed_gravity_squared_abelian=mixed_gravity,
        factor_a_cubed=factor_a_cubed,
        factor_b_fundamental_doublet_count=doublet_count,
        factor_b_fundamental_doublet_parity_even=parity_even,
        local_coefficients=local_coefficients,
        local_anomalies_cancel=local_cancel,
        all_supplied_conditions_cancel=local_cancel and parity_even,
    )


def charge_conjugate_chiral_multiplet(
    multiplet: ChiralGaugeMultiplet,
    *,
    label: str,
) -> ChiralGaugeMultiplet:
    """Conjugate the supplied Abelian and ``G_a`` cubic orientation signs."""

    row = _normalize_multiplet(multiplet, 0)
    if not isinstance(label, str) or not label.strip():
        raise ValueError("conjugate label must be a non-empty string")
    return ChiralGaugeMultiplet(
        label=label,
        factor_a_dimension=row.factor_a_dimension,
        factor_b_dimension=row.factor_b_dimension,
        abelian_charge=sp.simplify(-row.abelian_charge),
        factor_a_quadratic_index=row.factor_a_quadratic_index,
        factor_b_quadratic_index=row.factor_b_quadratic_index,
        factor_a_cubic_index=sp.simplify(-row.factor_a_cubic_index),
        factor_b_fundamental_doublet=row.factor_b_fundamental_doublet,
    )


def five_row_chiral_anomaly_ledger(
    q: Any,
    u: Any,
    d: Any,
    l: Any,
    e: Any,
) -> ChiralAnomalyLedger:
    """Specialize the exact ledger to the fixed five-row left-handed carrier.

    The argument order is ``(Q_L, u_R^c, d_R^c, L, e_R^c)``.  Representation
    dimensions and indices are fixed inputs; only the five Abelian coordinates
    vary.
    """

    charges = tuple(
        _exact_real(value, f"charges[{index}]")
        for index, value in enumerate((q, u, d, l, e))
    )
    half = sp.Rational(1, 2)
    rows = (
        ChiralGaugeMultiplet("Q_L", 3, 2, charges[0], half, half, 1, True),
        ChiralGaugeMultiplet("u_R^c", 3, 1, charges[1], half, 0, -1, False),
        ChiralGaugeMultiplet("d_R^c", 3, 1, charges[2], half, 0, -1, False),
        ChiralGaugeMultiplet("L", 1, 2, charges[3], 0, half, 0, True),
        ChiralGaugeMultiplet("e_R^c", 1, 1, charges[4], 0, 0, 0, False),
    )
    return chiral_anomaly_ledger(rows)


def _five_row_normalized_equations(
    charges: Sequence[sp.Expr],
) -> tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]:
    q, u, d, l, e = charges
    return tuple(
        sp.expand(expression)
        for expression in (
            2 * q + u + d,
            3 * q + l,
            6 * q + 3 * u + 3 * d + 2 * l + e,
            6 * q**3 + 3 * u**3 + 3 * d**3 + 2 * l**3 + e**3,
        )
    )


def five_row_local_anomaly_solution_variety() -> FiveRowLocalAnomalySolutionVariety:
    """Return the complete affine zero set of the four Abelian local equations.

    Linear elimination gives ``l=-3q``, ``e=6q``, and ``d=-2q-u``.  The
    remaining cubic is ``18*q*(2*q-u)*(4*q+u)``; retaining every factor without
    dividing by ``q`` yields exactly three affine lines.
    """

    q, u, d, l, e = sp.symbols("q u d l e", real=True)
    equations = _five_row_normalized_equations((q, u, d, l, e))
    linear_solution = ((l, -3 * q), (e, 6 * q), (d, -2 * q - u))
    substitutions = dict(linear_solution)
    reduced_cubic = sp.factor(equations[3].subs(substitutions))
    displayed_parameter, exchanged_parameter, vectorlike_parameter = sp.symbols(
        "t_displayed t_exchanged t_vectorlike",
        real=True,
    )
    branches = (
        FiveRowAnomalyBranch(
            name="displayed_line",
            parameter=displayed_parameter,
            charges=(
                displayed_parameter,
                -4 * displayed_parameter,
                2 * displayed_parameter,
                -3 * displayed_parameter,
                6 * displayed_parameter,
            ),
        ),
        FiveRowAnomalyBranch(
            name="row_exchanged_line",
            parameter=exchanged_parameter,
            charges=(
                exchanged_parameter,
                2 * exchanged_parameter,
                -4 * exchanged_parameter,
                -3 * exchanged_parameter,
                6 * exchanged_parameter,
            ),
        ),
        FiveRowAnomalyBranch(
            name="vectorlike_line",
            parameter=vectorlike_parameter,
            charges=(0, vectorlike_parameter, -vectorlike_parameter, 0, 0),
        ),
    )
    return FiveRowLocalAnomalySolutionVariety(
        charge_symbols=(q, u, d, l, e),
        normalized_local_equations=equations,
        linear_solution=linear_solution,
        reduced_cubic=reduced_cubic,
        branches=branches,
    )


def five_row_local_anomaly_membership(
    charges: Sequence[Any],
) -> FiveRowSolutionMembership:
    """Test exact membership in the fixed-carrier local anomaly zero set."""

    if len(charges) != 5:
        raise ValueError("exactly five charges are required")
    values = tuple(
        _exact_real(value, f"charges[{index}]")
        for index, value in enumerate(charges)
    )
    residuals = _five_row_normalized_equations(values)
    is_solution = all(residual == 0 for residual in residuals)
    q, u, d, l, e = values
    predicates = (
        (
            "displayed_line",
            (u + 4 * q, d - 2 * q, l + 3 * q, e - 6 * q),
        ),
        (
            "row_exchanged_line",
            (u - 2 * q, d + 4 * q, l + 3 * q, e - 6 * q),
        ),
        ("vectorlike_line", (q, l, e, d + u)),
    )
    matching = tuple(
        name
        for name, branch_residuals in predicates
        if is_solution
        and all(sp.simplify(residual) == 0 for residual in branch_residuals)
    )
    return FiveRowSolutionMembership(
        charges=values,
        normalized_local_residuals=residuals,
        is_solution=is_solution,
        matching_branches=matching,
    )
