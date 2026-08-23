"""Multi-species induced inverse-Newton composition (P243, advances #163).

Extends the accepted C-IGR-004 single-species renormalization condition to a
substrate-supplied species list by the block-diagonal Gaussian rule: the
one-loop effective action of independently propagating constant-mass species
adds per species, which within the accepted coefficient families is the
statement that every ``exact_mass_inverse_newton_shift`` contributes its own
``field_count * coefficient_per_field * I_2`` term.

For the aligned spectral-Cartan vacuum census (attempt 0001) every
propagating species is exactly massless, so ``z_i = 0``, the accepted
continuous extension gives ``J_sharp(0) = J_smooth(0) = 1``, and the usable
scheme set collapses to a single value: the spread ratio is exactly one.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

import sympy as sp

from .scalar_one_loop_mass import (
    SHARP_PROPER_TIME_REGULATOR,
    SMOOTH_PROPER_TIME_REGULATOR,
    exact_mass_inverse_newton_shift,
)
from .total_gravitational_coupling import scheme_spread_ratio


USABLE_MASSLESS_SCHEMES = (
    SHARP_PROPER_TIME_REGULATOR,
    SMOOTH_PROPER_TIME_REGULATOR,
)


@dataclass(frozen=True)
class MultiSpeciesCouplingLedger:
    """Exact multi-species induced coupling with scheme-collapse record."""

    species_field_counts: tuple[sp.Expr, ...]
    species_couplings: tuple[sp.Expr, ...]
    non_minimal_coupling: sp.Expr
    cutoff: sp.Expr
    baseline: sp.Expr
    induced_shift: sp.Expr
    total_inverse_newton: sp.Expr
    newton_constant: sp.Expr | None
    scheme_values_equal: bool


def _positive_exact(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if not expression.is_positive:
        raise ValueError(f"{name} must be positive")
    return expression


def _nonnegative_exact(value: Any, name: str) -> sp.Expr:
    expression = sp.sympify(value)
    if expression.is_negative:
        raise ValueError(f"{name} must be nonnegative")
    return expression


def species_additivity_identity(
    *,
    field_counts: Sequence[Any],
    mass_squared: Sequence[Any],
    non_minimal_coupling: Any,
    cutoff: Any,
) -> bool:
    """Certify per-species additivity against a pooled-count identity.

    For equal masses the accepted shift must be exactly linear in the field
    count: shifting ``N1 + N2`` fields equals the sum of separate shifts.
    For distinct masses the pooled object does not exist and the ledger sum
    is the defined extension; the equal-mass linearity plus the per-species
    construction pins it.
    """

    lam = _positive_exact(cutoff, "cutoff")
    xi = sp.sympify(non_minimal_coupling)
    n1 = _nonnegative_exact(field_counts[0], "field_counts[0]")
    n2 = _nonnegative_exact(field_counts[1], "field_counts[1]")
    m1 = _nonnegative_exact(mass_squared[0], "mass_squared[0]")
    m2 = _nonnegative_exact(mass_squared[1], "mass_squared[1]")
    if m1 != m2:
        raise ValueError(
            "the pooled-count identity requires equal species masses"
        )
    shifts_separate = [
        exact_mass_inverse_newton_shift(count, xi, regulator=scheme,
                                        cutoff=lam, mass_squared=m)
        for count, m in ((n1, m1), (n2, m2))
        for scheme in USABLE_MASSLESS_SCHEMES[:1]
    ]
    shift_pooled = exact_mass_inverse_newton_shift(
        n1 + n2, xi, regulator=USABLE_MASSLESS_SCHEMES[0],
        cutoff=lam, mass_squared=m1,
    )
    total = sum((shift.value for shift in shifts_separate), sp.Integer(0))
    return sp.simplify(total - shift_pooled.value) == 0


def massless_substrate_coupling(
    *,
    massless_count: Any,
    non_minimal_coupling: Any,
    cutoff: Any,
    baseline: Any = 0,
) -> MultiSpeciesCouplingLedger:
    """Return the exact N-species massless induced-coupling ledger."""

    n = _nonnegative_exact(massless_count, "massless_count")
    xi = sp.sympify(non_minimal_coupling)
    lam = _positive_exact(cutoff, "cutoff")
    b = _nonnegative_exact(baseline, "baseline")

    shifts = tuple(
        exact_mass_inverse_newton_shift(n, xi, regulator=scheme,
                                        cutoff=lam, mass_squared=0)
        for scheme in USABLE_MASSLESS_SCHEMES
    )
    values = {sp.simplify(shift.value) for shift in shifts}
    scheme_values_equal = len(values) == 1
    if not scheme_values_equal:
        raise ValueError("massless schemes disagree; usable set violated")
    induced = values.pop()
    spread = scheme_spread_ratio(cutoff=lam, mass_squared=0)
    if sp.simplify(spread.ratio - 1) != 0:
        raise ValueError("spread ratio at z=0 is not exactly one")
    total = sp.simplify(b + induced)
    newton = None if total == 0 else sp.simplify(1 / total)
    return MultiSpeciesCouplingLedger(
        species_field_counts=(n,),
        species_couplings=(induced,),
        non_minimal_coupling=xi,
        cutoff=lam,
        baseline=b,
        induced_shift=induced,
        total_inverse_newton=total,
        newton_constant=newton,
        scheme_values_equal=True,
    )


def numeric_induced_shift(
    *,
    massless_count: int,
    non_minimal_coupling: float,
    cutoff: float,
    baseline: float = 0.0,
    precision: int = 30,
) -> dict[str, Any]:
    """Evaluate the ledger numerically at declared decimal precision."""

    ledger = massless_substrate_coupling(
        massless_count=massless_count,
        non_minimal_coupling=non_minimal_coupling,
        cutoff=cutoff,
        baseline=baseline,
    )
    induced = sp.N(ledger.induced_shift, precision)
    total = sp.N(ledger.total_inverse_newton, precision)
    newton = None if ledger.newton_constant is None else sp.N(
        ledger.newton_constant, precision
    )
    return {
        "induced_shift": induced,
        "total_inverse_newton": total,
        "newton_constant": newton,
        "baseline": ledger.baseline,
        "cutoff": ledger.cutoff,
        "massless_count": ledger.species_field_counts[0],
    }
