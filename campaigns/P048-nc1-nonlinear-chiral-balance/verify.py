#!/usr/bin/env python3
"""Verify P048's nonlinear chiral balance theorem and audit NC1."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.governance import load_yaml
from substrate_framework.sine_gordon import (
    naive_chiral_currents,
    naive_chiral_transport_defects,
    sine_gordon_chiral_sources,
    sine_gordon_light_cone_chiral_sources,
    sine_gordon_residual,
    spatial_parity_transform,
    static_kink_field,
    topological_charge_from_boundaries,
    topological_current,
    topological_current_divergence,
)
from substrate_framework.verification import CheckLedger


EXPECTED_SOURCE_SHA256 = (
    "b7206df001095b2706818ea5f3ffde13d24887816d867f7252da460588b010f5"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    args = parser.parse_args()
    ledger = CheckLedger("P048-NC1")

    source_bytes = args.source_file.read_bytes()
    reproduction = load_yaml(args.source_reproduction)
    ledger.check(
        "the audited NC1 source is the hash-pinned candidate unit",
        hashlib.sha256(source_bytes).hexdigest() == EXPECTED_SOURCE_SHA256,
    )
    ledger.check(
        "the predecessor executable exits successfully with all eight checks",
        reproduction.get("sha256") == EXPECTED_SOURCE_SHA256
        and reproduction.get("exit_code") == 0
        and reproduction.get("terminal_tally") == "ALL 8 CHECKS PASS",
    )

    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    current_plus, current_minus = naive_chiral_currents(field, x, t)
    defect_plus, defect_minus = naive_chiral_transport_defects(field, x, t)
    wave_operator = sp.diff(field, t, 2) - sp.diff(field, x, 2)
    ledger.check(
        "both characteristic-current defects derive to the same wave operator",
        sp.simplify(defect_plus - wave_operator) == 0
        and sp.simplify(defect_minus - wave_operator) == 0,
    )

    on_shell_acceleration = sp.diff(field, x, 2) - sp.sin(field)
    derived_plus = sp.simplify(
        defect_plus.subs(sp.diff(field, t, 2), on_shell_acceleration)
    )
    derived_minus = sp.simplify(
        defect_minus.subs(sp.diff(field, t, 2), on_shell_acceleration)
    )
    expected_sources = sine_gordon_chiral_sources(field)
    ledger.check(
        "the full sine-Gordon equation sources both currents by minus sine phi",
        derived_plus == expected_sources[0]
        and derived_minus == expected_sources[1]
        and derived_plus == derived_minus,
    )

    def source_coefficient_predicate(candidate: object) -> bool:
        proposed = sp.sympify(candidate) * sp.sin(field)
        return bool(
            sp.simplify(derived_plus - proposed) == 0
            and sp.simplify(derived_minus - proposed) == 0
        )

    ledger.mutation_sensitive(
        "on-shell characteristic source coefficient",
        source_coefficient_predicate,
        -1,
        [0, 1, -2],
    )

    light_cone_sources = sine_gordon_light_cone_chiral_sources(field)
    ledger.check(
        "the explicit light-cone convention gives equal minus-one-half sources",
        sp.simplify(
            (sp.diff(current_plus, t) - sp.diff(current_plus, x)).subs(
                sp.diff(field, t, 2), on_shell_acceleration
            )
            / 2
            - light_cone_sources[0]
        )
        == 0
        and sp.simplify(
            (sp.diff(current_minus, t) + sp.diff(current_minus, x)).subs(
                sp.diff(field, t, 2), on_shell_acceleration
            )
            / 2
            - light_cone_sources[1]
        )
        == 0,
    )

    def light_cone_factor_predicate(candidate: object) -> bool:
        factor = sp.sympify(candidate)
        return bool(sp.simplify(factor * derived_plus + sp.sin(field) / 2) == 0)

    ledger.mutation_sensitive(
        "light-cone derivative normalization",
        light_cone_factor_predicate,
        sp.Rational(1, 2),
        [1, 2, sp.Rational(1, 4)],
    )

    density, flux = topological_current(field, x, t)
    ledger.check(
        "the normalized topological current has the antisymmetric orientation sign",
        density == sp.diff(field, x) / (2 * sp.pi)
        and flux == -sp.diff(field, t) / (2 * sp.pi),
    )
    ledger.check(
        "topological-current conservation is an off-shell mixed-partial identity",
        topological_current_divergence(field, x, t) == 0
        and defect_plus.has(sp.diff(field, t, 2)),
    )

    def flux_sign_predicate(candidate: object) -> bool:
        candidate_flux = sp.sympify(candidate) * sp.diff(field, t) / (2 * sp.pi)
        divergence = sp.simplify(sp.diff(density, t) + sp.diff(candidate_flux, x))
        return bool(divergence == 0)

    ledger.mutation_sensitive(
        "antisymmetric topological flux sign",
        flux_sign_predicate,
        -1,
        [0, 1],
    )

    n_minus, n_plus = sp.symbols("n_minus n_plus", integer=True)
    winding = topological_charge_from_boundaries(
        2 * sp.pi * n_minus,
        2 * sp.pi * n_plus,
    )
    ledger.check(
        "finite-energy vacuum boundaries give the integer winding difference",
        sp.simplify(winding - (n_plus - n_minus)) == 0,
    )

    def charge_normalization_predicate(candidate: object) -> bool:
        denominator = sp.sympify(candidate)
        kink_charge = sp.simplify((2 * sp.pi - 0) / denominator)
        antikink_charge = sp.simplify((0 - 2 * sp.pi) / denominator)
        return bool(kink_charge == 1 and antikink_charge == -1)

    ledger.mutation_sensitive(
        "unit-winding charge normalization",
        charge_normalization_predicate,
        2 * sp.pi,
        [sp.pi, 4 * sp.pi],
    )

    parity_field = spatial_parity_transform(field, x)
    parity_density, parity_flux = topological_current(parity_field, x, t)
    reflected_density = density.subs(x, -x)
    reflected_flux = flux.subs(x, -x)
    ledger.check(
        "the topological current is axial under scalar-field spatial parity",
        sp.simplify(parity_density + reflected_density) == 0
        and sp.simplify(parity_flux - reflected_flux) == 0,
    )
    ledger.check(
        "spatial parity exchanges winding sectors while preserving the SG equation",
        sp.simplify(
            sine_gordon_residual(parity_field, x, t)
            - sine_gordon_residual(field, x, t).subs(x, -x)
        )
        == 0
        and sp.simplify(
            topological_charge_from_boundaries(
                2 * sp.pi * n_plus,
                2 * sp.pi * n_minus,
            )
            + winding
        )
        == 0,
    )

    kink = static_kink_field(x)
    antikink = static_kink_field(x, orientation=-1)
    kink_limits = (sp.limit(kink, x, -sp.oo), sp.limit(kink, x, sp.oo))
    antikink_limits = (
        sp.limit(antikink, x, -sp.oo),
        sp.limit(antikink, x, sp.oo),
    )
    ledger.check(
        "the explicit kink and antikink are exact opposite-winding solutions",
        sp.simplify(sine_gordon_residual(kink, x, t)) == 0
        and sp.simplify(sine_gordon_residual(antikink, x, t)) == 0
        and topological_charge_from_boundaries(*kink_limits) == 1
        and topological_charge_from_boundaries(*antikink_limits) == -1
        and sp.simplify(spatial_parity_transform(kink, x) - antikink) == 0,
    )
    kink_integral = sp.integrate(
        topological_current(kink, x, t)[0],
        (x, -sp.oo, sp.oo),
    )
    antikink_integral = sp.integrate(
        topological_current(antikink, x, t)[0],
        (x, -sp.oo, sp.oo),
    )
    ledger.check(
        "independent whole-line density integrals reproduce both boundary charges",
        sp.simplify(kink_integral - 1) == 0
        and sp.simplify(antikink_integral + 1) == 0,
    )

    epsilon = sp.symbols("epsilon", positive=True)
    profile = sp.Function("f")(x, t)
    scaled_field = epsilon * profile
    linearized_residual = sp.simplify(
        sp.limit(
            sine_gordon_residual(scaled_field, x, t) / epsilon,
            epsilon,
            0,
            dir="+",
        )
    )
    linearized_source = sp.simplify(
        sp.limit(
            sine_gordon_chiral_sources(scaled_field)[0] / epsilon,
            epsilon,
            0,
            dir="+",
        )
    )
    ledger.check(
        "the small-amplitude SG limit is massive Klein-Gordon rather than a chiral wave split",
        linearized_residual
        == sp.diff(profile, t, 2) - sp.diff(profile, x, 2) + profile
        and linearized_source == -profile,
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
