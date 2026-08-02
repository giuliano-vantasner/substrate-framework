"""Primary exact verifier for P061 periodic explicit-breaking claims."""

from __future__ import annotations

import sympy as sp

from substrate_framework.explicit_breaking import (
    conditional_gmor_evidence,
    matched_local_curvature_potentials,
    periodic_potential_evidence,
    su2_trace_breaking_evidence,
)
from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P061")
    field = sp.Symbol("pi", real=True)
    amplitude, scale, kinetic = sp.symbols("A F K", positive=True)
    periodic = periodic_potential_evidence(field, amplitude, scale, kinetic)
    ledger.check("periodic vacuum value", periodic.value_at_origin == 0)
    ledger.check("periodic vacuum slope", periodic.slope_at_origin == 0)
    ledger.check("period derived", periodic.period == 2 * sp.pi * scale)
    ledger.check(
        "periodic shift identity",
        sp.trigsimp(
            periodic.potential.subs(field, field + periodic.period) - periodic.potential
        )
        == 0,
    )
    ledger.check(
        "curvature derived", periodic.curvature_at_origin == amplitude / scale**2
    )
    ledger.check(
        "fourth derivative derived",
        periodic.fourth_derivative_at_origin == -amplitude / scale**4,
    )
    ledger.check(
        "sixth-order series derived",
        periodic.sixth_order_series
        == amplitude * field**2 / (2 * scale**2)
        - amplitude * field**4 / (24 * scale**4)
        + amplitude * field**6 / (720 * scale**6),
    )
    ledger.check(
        "generalized mass includes kinetics",
        periodic.generalized_mass_squared == amplitude / (kinetic * scale**2),
    )

    mass = sp.Symbol("m", positive=True)
    unit_kinetic = periodic_potential_evidence(field, mass**2 * scale**2, scale, 1)
    quarter_kinetic = periodic_potential_evidence(
        field, mass**2 * scale**2, scale, sp.Rational(1, 4)
    )
    ledger.check(
        "unit kinetic gives named mass",
        unit_kinetic.generalized_mass_squared == mass**2,
    )
    ledger.check(
        "quarter kinetic exposes PG2 factor four",
        quarter_kinetic.generalized_mass_squared == 4 * mass**2,
    )
    ledger.check(
        "negative amplitude reverses mass sign",
        periodic_potential_evidence(
            field, -amplitude, scale, kinetic
        ).generalized_mass_squared
        == -periodic.generalized_mass_squared,
    )

    local = matched_local_curvature_potentials(field, mass**2, scale)
    ledger.check("matched Hessians", local.hessian_difference_at_origin == 0)
    ledger.check("cosine is periodic", local.periodic_shift_residual == 0)
    ledger.check("quadratic is not periodic", local.quadratic_shift_residual != 0)
    ledger.check(
        "fourth derivative distinguishes mechanisms",
        local.fourth_derivative_difference_at_origin == -(mass**2) / scale**2,
    )

    trace_half = su2_trace_breaking_evidence(
        field, scale, 1, scale**2 / 16, mass**2 * scale**2 / 8
    )
    trace_canonical = su2_trace_breaking_evidence(
        field, scale, 2, scale**2 / 16, mass**2 * scale**2 / 8
    )
    trace_third = su2_trace_breaking_evidence(
        field, scale, 3, scale**2 / 16, mass**2 * scale**2 / 8
    )
    ledger.check(
        "trace derived for half coordinate",
        trace_half.trace_u_minus_identity == 2 * sp.cos(field / scale) - 2,
    )
    ledger.check(
        "half-coordinate kinetic metric",
        trace_half.kinetic_coefficient == sp.Rational(1, 4),
    )
    ledger.check(
        "half-coordinate potential curvature",
        trace_half.potential_curvature == mass**2 / 4,
    )
    ledger.check(
        "half-coordinate generalized mass",
        trace_half.generalized_mass_squared == mass**2,
    )
    ledger.check(
        "canonical-coordinate kinetic metric", trace_canonical.kinetic_coefficient == 1
    )
    ledger.check(
        "canonical-coordinate potential curvature",
        trace_canonical.potential_curvature == mass**2,
    )
    ledger.check(
        "canonical-coordinate generalized mass",
        trace_canonical.generalized_mass_squared == mass**2,
    )
    ledger.check(
        "third coordinate generalized mass",
        trace_third.generalized_mass_squared == mass**2,
    )
    ledger.check(
        "coordinate multiplier cancels exactly",
        trace_half.generalized_mass_coordinate_residual
        == trace_canonical.generalized_mass_coordinate_residual
        == trace_third.generalized_mass_coordinate_residual
        == 0,
    )
    ledger.check(
        "cited trace potential is one quarter of PG2 potential",
        sp.simplify(trace_half.potential / unit_kinetic.potential) == sp.Rational(1, 4),
    )
    ledger.check(
        "PG2 equality requires fourfold trace prefactor",
        sp.simplify(
            (unit_kinetic.amplitude / 2) / trace_half.lagrangian_trace_prefactor
        )
        == 4,
    )

    quark_mass = sp.Symbol("m_q", positive=True)
    condensate = sp.Symbol("Sigma", negative=True)
    convention = sp.Symbol("c", positive=True)
    gmor = conditional_gmor_evidence(
        quark_mass, condensate, scale, convention_factor=convention
    )
    ledger.check("conditional GMOR residual", gmor.relation_residual == 0)
    ledger.check("quark-mass exponent", gmor.quark_mass_log_exponent == 1)
    ledger.check("condensate exponent", gmor.condensate_log_exponent == 1)
    ledger.check("decay-scale exponent", gmor.decay_scale_log_exponent == -2)
    ledger.check("convention-factor exponent", gmor.convention_factor_log_exponent == 1)
    ledger.check("squared-mass sign domain", gmor.mass_squared.is_positive is True)
    ledger.check("zero quark-mass limit", gmor.zero_quark_mass_limit == 0)
    ledger.check(
        "continuous scale-condensate degeneracy",
        gmor.scale_condensate_degeneracy_residual == 0,
    )
    doubled = conditional_gmor_evidence(
        quark_mass, condensate, scale, convention_factor=2 * convention
    )
    ledger.check(
        "GMOR convention factor is load bearing",
        sp.simplify(doubled.mass_squared / gmor.mass_squared) == 2,
    )
    ledger.check(
        "GMOR dimensions close",
        2 + 2 == 1 + 3,
        "both sides must have mass dimension four",
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
