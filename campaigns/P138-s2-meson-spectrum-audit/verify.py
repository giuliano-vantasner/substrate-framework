from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework.numerics import trapezoid_integral
from substrate_framework.radial_modes import (
    option_c_continuum_threshold,
    option_c_hedgehog_rhs,
    option_c_operator_coefficients,
    option_c_second_variation,
    solve_option_c_hedgehog,
    solve_radial_finite_box_spectrum,
)
from substrate_framework.skyrme_relations import (
    conditional_anw_mass,
    conditional_topological_mass,
    matched_pion_coupling_ratio,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "48a9eadf6fbc1e3ebe7fcd6b98c2d60cc10a3f5282404c84e4626910f296eaf7"
DOSSIER_SHA256 = "74e77d5130c9f2f96132572bd9720d90b8da0902130dfb0866b4b4035de783ed"
FROZEN_PROPOSAL_SHA256 = "8e54ead36c74e87475abebb019f151740999a0216518b296a0af1ebd3546e608"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assigned_names(tree: ast.Module, target: str) -> set[str]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(item, ast.Name) and item.id == target for item in node.targets):
            return {
                descendant.id
                for descendant in ast.walk(node.value)
                if isinstance(descendant, ast.Name)
            }
    raise AssertionError(f"missing assignment for {target}")


def _profile_and_spectrum(
    outer_radius: float,
    sample_points: int,
) -> tuple[float, float, float, tuple[float, ...], tuple[float, ...], tuple[bool, ...]]:
    profile = solve_option_c_hedgehog(
        outer_radius=outer_radius,
        sample_points=sample_points,
    )
    radius = profile.radius
    field = profile.field
    derivative = profile.radial_derivative
    inertia_density = (
        radius**2
        * np.sin(field) ** 2
        * (1.0 + derivative**2 + np.sin(field) ** 2 / radius**2)
    )
    domain_inertia = trapezoid_integral(inertia_density, radius)
    # For f=c/r^2+O(r^-6), the leading missing integral is c^2/R.
    leading_tail = float(field[-1] ** 2 * outer_radius**3)
    second_derivative = np.asarray(
        [
            option_c_hedgehog_rhs(
                float(radial_point),
                (float(field_value), float(derivative_value)),
            )[1]
            for radial_point, field_value, derivative_value in zip(
                radius,
                field,
                derivative,
                strict=True,
            )
        ],
        dtype=np.float64,
    )
    gradient, potential, weight, correction = option_c_operator_coefficients(
        radius,
        field,
        derivative,
        second_derivative,
    )
    spectrum = solve_radial_finite_box_spectrum(
        radius,
        gradient,
        potential,
        weight,
        mode_count=4,
        continuum_threshold=0.0,
    )
    source_window = (radius >= 0.3) & (radius <= min(12.0, outer_radius))
    truncated_inertia = trapezoid_integral(
        inertia_density[source_window],
        radius[source_window],
    )
    return (
        domain_inertia + leading_tail,
        truncated_inertia,
        float(np.max(np.abs(correction[source_window]))),
        spectrum.eigenvalues,
        spectrum.relative_residuals,
        spectrum.below_continuum,
    )


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parent / "evidence" / "frozen-proposal.yaml"
    source_text = source_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(source_path))
    checks = CheckLedger("P138/S2")

    checks.check("pinned S2 source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("pinned S2 dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check(
        "frozen proposal hash",
        _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256,
    )

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("ten source predicates", len(source_checks) == 10)
    checks.check(
        "only the local check helper asserts",
        len(assertions) == 1 and assertions[0].lineno < source_checks[0].lineno,
    )

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(source_path),
    )
    checks.check(
        "S2 compatibility event is exactly three direct immutable references",
        compatibility.direct_legacy_attributes == 3
        and compatibility.dynamic_legacy_getattrs == 0
        and compatibility.imported_legacy_names == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    radius = sp.Symbol("r", positive=True)
    profile = sp.Function("f")(radius)
    variation = option_c_second_variation(profile, radius)
    checks.check(
        "complete radial Hessian retains the mixed correction",
        sp.simplify(
            variation.potential_coefficient
            - variation.local_half_hessian
            - variation.mixed_boundary_correction
        )
        == 0
        and sp.simplify(variation.mixed_boundary_correction) != 0,
    )
    checks.check(
        "source assembles the local half-Hessian and omits its own documented correction",
        "C_pot = 0.5 * (d2_sin2f + d2_skyrme_grad + d2_sin4f / fr ** 2)"
        in source_text
        and "subtract the cross term" in source_text
        and "C_pot = C_pot" not in source_text,
    )
    checks.check(
        "massless continuum edge is exactly zero",
        option_c_continuum_threshold() == 0,
    )

    refinements = tuple(
        _profile_and_spectrum(wall, points)
        for wall, points in ((12.0, 801), (18.0, 1201), (24.0, 1601))
    )
    full_inertias = tuple(item[0] for item in refinements)
    truncated_inertias = tuple(item[1] for item in refinements)
    correction_norms = tuple(item[2] for item in refinements)
    lowest_levels = tuple(item[3][0] for item in refinements)
    maximum_residual = max(value for item in refinements for value in item[4])
    below_flags = tuple(flag for item in refinements for flag in item[5])

    checks.check(
        "full inertia functional converges under domain growth",
        max(full_inertias) - min(full_inertias) < 3.0e-5,
    )
    checks.check(
        "source inertia window omits a load-bearing positive contribution",
        full_inertias[-1] - truncated_inertias[-1] > 0.4,
    )
    checks.check(
        "mixed Hessian correction is numerically load bearing",
        min(correction_norms) > 1.0,
    )
    checks.check(
        "corrected lowest levels collapse as the wall grows",
        lowest_levels[0] > lowest_levels[1] > lowest_levels[2] > 0.0,
    )
    checks.check(
        "corrected levels form an inverse-wall-squared ladder",
        abs(18.0**2 * lowest_levels[1] - 24.0**2 * lowest_levels[2])
        / (24.0**2 * lowest_levels[2])
        < 0.02,
    )
    checks.check(
        "no computed box level lies below the continuum",
        not any(bool(flag) for flag in below_flags),
    )
    checks.check(
        "sparse generalized eigensolves have controlled residuals",
        maximum_residual < 5.0e-9,
    )

    inertia_symbol = sp.Symbol("I", positive=True)
    nucleon_spin = sp.Rational(1, 2)
    delta_spin = sp.Rational(3, 2)
    rotor_split = sp.simplify(
        (
            delta_spin * (delta_spin + 1)
            - nucleon_spin * (nucleon_spin + 1)
        )
        / (2 * inertia_symbol)
    )
    classical_split = sp.simplify(
        (delta_spin**2 - nucleon_spin**2) / (2 * inertia_symbol)
    )
    checks.check(
        "declared rotor arithmetic is exact",
        rotor_split == sp.Rational(3, 2) / inertia_symbol
        and classical_split == 1 / inertia_symbol,
    )
    checks.check(
        "rotor labels and collective Hamiltonian are imported rather than derived",
        "Finkelstein-Rubinstein constraint J=I (IMPORTED" in source_text
        and "H_rot = J(J+1)/(2I) (symmetric top)" in source_text,
    )

    delta_dependencies = _assigned_names(tree, "DeltaN_MeV")
    inertia_dependencies = _assigned_names(tree, "Lambda_phys_GeVinv")
    checks.check(
        "restored splitting bypasses the solved inertia functional",
        "Lambda_phys_GeVinv" in delta_dependencies
        and "L_shape" not in delta_dependencies
        and not inertia_dependencies,
    )
    target = sp.Symbol("target", positive=True)
    fitted_inertia = 1500 / target
    checks.check(
        "the fitted inertia round-trips any target splitting",
        sp.simplify(3 * 1000 / (2 * fitted_inertia) - target) == 0,
    )

    fpp_dependencies = _assigned_names(tree, "fpp_exact")
    eom_dependencies = _assigned_names(tree, "eom_residual")
    checks.check(
        "machine-epsilon EOM residual substitutes its defining right-hand side",
        {"ri", "fi", "fpi"} <= fpp_dependencies
        and "fpp_exact" in eom_dependencies,
    )

    eigenvalue = sp.Symbol("lambda")
    shift = sp.Integer(50)
    checks.check(
        "tachyon injection shifts every generalized eigenvalue by construction",
        sp.simplify((eigenvalue - shift) - (eigenvalue - 50)) == 0
        and "C_tachyon = C_pot - 50.0 * W_kin" in source_text,
    )

    first_operator = sp.diag(1, 4)
    second_operator = sp.diag(1, 9)
    checks.check(
        "one shared scalar value does not identify operators or spectra",
        first_operator != second_operator
        and first_operator.eigenvals() != second_operator.eigenvals()
        and first_operator[0, 0] == second_operator[0, 0],
    )
    checks.check(
        "identical lift notation supplies no fluctuation intertwiner",
        "E_shadow = E0 * Nn ** sp.Rational(-1, 2)" in source_text
        and "E_vantasner = E0 / sp.sqrt(Nn)" in source_text
        and "intertwiner" not in source_text,
    )

    coefficient, electron_energy, pion_scale, coupling = sp.symbols(
        "B1 E_e F_pi e",
        positive=True,
    )
    topological = conditional_topological_mass(coefficient, electron_energy)
    anw = conditional_anw_mass(coefficient, pion_scale, coupling)
    ratio = matched_pion_coupling_ratio(electron_energy)
    checks.check(
        "S2 check ten is exactly the accepted conditional mass matching",
        sp.simplify(anw.subs(pion_scale, coupling * ratio) - topological) == 0,
    )
    checks.check(
        "source supplies no meson channel spectrum resonance pole or width",
        "phase_shift" not in source_text
        and "resonance_width" not in source_text
        and "quasi_normal" not in source_text,
    )
    checks.check(
        "dossier itself distinguishes missing pion and qualified Roper inputs",
        "The pion mass is not derived in S2" in dossier_text
        and "The Roper resonance N*(1440)" in dossier_text,
    )

    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    parser.add_argument("dossier_file")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file, arguments.dossier_file))
