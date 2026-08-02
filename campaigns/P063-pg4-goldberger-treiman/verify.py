"""Primary exact verifier for P063 axial Ward-identity claims."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.axial_ward import (
    analytic_gt_discrepancy_evidence,
    axial_form_factor_dimension_ledger,
    generalized_axial_ward_evidence,
    gt_relation_ledger,
    on_shell_axial_divergence,
    pcac_limit_order_evidence,
    pion_pole_remainder_evidence,
)
from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-18/"
    "bridge_PG4_goldberger_treiman.py"
)
SOURCE_SHA256 = "e13e68536d14bedb1c8fa7ec10110172d0a1b73e08ce365863013dc7db66f1e9"


def _zero(expression: object) -> bool:
    return sp.simplify(sp.sympify(expression)) == 0


def main() -> int:
    ledger = CheckLedger("P063")
    ledger.check("hash-pinned PG4 source exists", SOURCE.is_file())
    ledger.check(
        "hash-pinned PG4 source integrity",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    ledger.check(
        "source discrepancy proportionality is a literal assignment",
        "R_residual = K * m_pi**2" in source_text,
    )
    ledger.check(
        "source current omits induced two-mass scale",
        "+ q_mu gamma_5 G_P(q^2)" in source_text
        and "GP_pole = 4 * MN * Fpi" in source_text,
    )

    standard_dimensions = axial_form_factor_dimension_ledger()
    omitted_scale_dimensions = axial_form_factor_dimension_ledger(
        induced_scale_mass_dimension=0
    )
    ledger.check(
        "standard dimensionless form-factor convention closes",
        standard_dimensions.convention_is_dimensionally_consistent,
    )
    ledger.check(
        "PG4 omitted-scale convention fails dimensions",
        not omitted_scale_dimensions.convention_is_dimensionally_consistent
        and omitted_scale_dimensions.dimension_residual == 1,
    )

    mass, q2, pion_mass2, decay = sp.symbols("M Q2 mu2 F", positive=True)
    axial0, axial_slope, induced0 = sp.symbols("a0 a1 p0", real=True)
    coupling0, coupling_slope = sp.symbols("g0 s", positive=True)
    axial = axial0 + axial_slope * q2
    coupling = coupling0 + coupling_slope * q2
    divergence = on_shell_axial_divergence(mass, q2, axial, induced0)
    ledger.check(
        "on-shell divergence retains q over two mass convention",
        _zero(
            divergence.normalized_divergence_coefficient
            - (axial - q2 * induced0 / (4 * mass**2))
        ),
    )
    source_like_divergence = on_shell_axial_divergence(
        mass,
        q2,
        axial,
        induced0,
        induced_scale=1,
    )
    ledger.check(
        "omitted induced scale changes load-bearing divergence",
        not _zero(
            source_like_divergence.unnormalized_divergence_coefficient
            - divergence.unnormalized_divergence_coefficient
        ),
    )

    ward = generalized_axial_ward_evidence(
        q2,
        mass,
        pion_mass2,
        decay,
        axial,
        induced0,
        coupling,
    )
    ledger.check(
        "generalized PCAC source keeps pion pole and mass normalization",
        _zero(
            ward.pcac_pion_pole_source
            - decay * pion_mass2 * coupling / (mass * (pion_mass2 + q2))
        ),
    )
    ledger.check(
        "generalized identity retains independent induced form factor",
        ward.generalized_identity_residual.has(induced0),
    )
    ledger.check(
        "pion-pole dominance is a separate simplifying premise",
        _zero(
            ward.pole_dominance_reduced_residual
            - (axial - decay * coupling / mass)
        ),
    )
    ledger.check(
        "pole residue evaluates coupling at pion pole",
        _zero(
            ward.pion_pole_residue
            - 4
            * mass
            * decay
            * (coupling0 - coupling_slope * pion_mass2)
        ),
    )
    ledger.check(
        "zero and pion-pole coupling points remain distinct",
        ward.coupling_at_zero_transfer == coupling0
        and ward.coupling_at_pion_pole
        == coupling0 - coupling_slope * pion_mass2,
    )

    remainder0, remainder1 = sp.symbols("R0 R1", real=True)
    remainder = remainder0 + remainder1 * q2
    pole_plus_remainder = pion_pole_remainder_evidence(
        q2,
        mass,
        pion_mass2,
        decay,
        axial,
        coupling,
        remainder,
    )
    ledger.check(
        "regular remainder leaves pole residue unchanged",
        _zero(pole_plus_remainder.pion_pole_residue - ward.pion_pole_residue),
    )
    ledger.check(
        "regular remainder changes off-zero Ward identity",
        pole_plus_remainder.reduced_residual.has(remainder0)
        and pole_plus_remainder.reduced_residual.has(remainder1),
    )
    ledger.check(
        "finite regular remainder drops out only at zero transfer",
        _zero(
            pole_plus_remainder.zero_transfer_residual
            - (axial0 - decay * coupling0 / mass)
        ),
    )

    path_ratio = sp.Symbol("rho", positive=True)
    limit_order = pcac_limit_order_evidence(q2, pion_mass2, path_ratio)
    ledger.check(
        "zero-transfer then chiral pole-kernel limit",
        limit_order.zero_transfer_then_chiral == 1,
    )
    ledger.check(
        "chiral then zero-transfer pole-kernel limit",
        limit_order.chiral_then_zero_transfer == 0,
    )
    ledger.check(
        "fixed-ratio limit exposes a continuum of path values",
        limit_order.fixed_ratio_path == 1 / (path_ratio + 1),
    )
    ledger.check(
        "PCAC pole-kernel limits do not commute",
        limit_order.zero_transfer_then_chiral
        != limit_order.chiral_then_zero_transfer,
    )

    slope, quadratic_remainder = sp.symbols("s_GT R_GT", real=True)
    discrepancy = analytic_gt_discrepancy_evidence(
        pion_mass2,
        coupling0,
        slope,
        quadratic_remainder,
    )
    ledger.check(
        "regular coupling expansion derives exact mass-squared factor",
        _zero(
            discrepancy.dimensionless_discrepancy
            - pion_mass2 * discrepancy.mass_squared_factor
        ),
    )
    ledger.check(
        "discrepancy leading coefficient is derived from slope",
        discrepancy.leading_mass_squared_coefficient == -slope / coupling0,
    )
    ledger.check("regular discrepancy chiral limit", discrepancy.chiral_limit == 0)
    nonanalytic = sp.simplify(
        1 - coupling0 / (coupling0 + sp.sqrt(pion_mass2))
    )
    ledger.check(
        "current conservation alone does not force mass-squared discrepancy",
        sp.limit(nonanalytic / pion_mass2, pion_mass2, 0, dir="+") == sp.oo,
    )

    axial_charge, coupling_symbol = sp.symbols("g_A g_piNN", positive=True)
    ledger_gt = gt_relation_ledger(
        coupling_symbol,
        decay,
        axial_charge,
        mass,
        path_ratio,
    )
    ledger.check("GT monomial constraint has rank one", ledger_gt.monomial_exponent_row.rank() == 1)
    ledger.check(
        "GT equation retains three parameter directions",
        ledger_gt.independent_parameter_directions == 3
        and ledger_gt.monomial_exponent_row * ledger_gt.exponent_nullspace
        == sp.zeros(1, 3),
    )
    ledger.check(
        "g_A solve-back is bookkeeping",
        ledger_gt.solved_axial_charge == coupling_symbol * decay / mass,
    )
    ledger.check(
        "three exact rescaling families preserve supplied GT equation",
        ledger_gt.common_scale_covariance_residual
        == ledger_gt.inverse_decay_coupling_residual
        == ledger_gt.inverse_mass_axial_residual
        == 0,
    )

    q_timelike = sp.Symbol("q2", real=True)
    source_gp = 4 * mass * decay * coupling_symbol / (pion_mass2 - q_timelike)
    source_rhs = (
        2 * decay * coupling_symbol * pion_mass2 / (pion_mass2 - q_timelike)
    )
    source_full_matching = sp.simplify(
        2 * mass * axial_charge + q_timelike * source_gp - source_rhs
    )
    source_full_on_gt = sp.simplify(
        source_full_matching.subs(axial_charge, decay * coupling_symbol / mass)
    )
    ledger.check(
        "PG4 full mixed-convention matching does not close on GT",
        source_full_on_gt != 0 and source_full_on_gt.has(q_timelike),
    )
    corrected_gp = 4 * mass * decay * coupling_symbol / (
        pion_mass2 - q_timelike
    )
    corrected_normalized_matching = sp.simplify(
        axial_charge
        + q_timelike * corrected_gp / (4 * mass**2)
        - decay
        * coupling_symbol
        * pion_mass2
        / (mass * (pion_mass2 - q_timelike))
    )
    ledger.check(
        "corrected dimensionless convention reduces pointwise to GT",
        _zero(
            corrected_normalized_matching
            - (axial_charge - decay * coupling_symbol / mass)
        ),
    )
    ledger.check(
        "wrong pole sign fails pointwise reduction",
        not _zero(
            axial_charge
            - q_timelike * corrected_gp / (4 * mass**2)
            - decay
            * coupling_symbol
            * pion_mass2
            / (mass * (pion_mass2 - q_timelike))
            - (axial_charge - decay * coupling_symbol / mass)
        ),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
