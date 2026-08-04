from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.massive_dipoles import (
    massive_triplet_dipole_extrema,
    massive_triplet_dipole_interaction,
    yukawa_radial_hessian,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "ebe1ba930be26f17671d8e82779d14fc00e7a8b988a4aada722a32d0d9328ddd"
DOSSIER_SHA256 = "d3536930433f3d02b86f15735a40499ac2e4e1614a27743f88431719d7ba2079"
FROZEN_PROPOSAL_SHA256 = "e266a0a9f5f6bc2eba36ab26bebfd1ae37b5958aa5f4c4b5f4aff32966ecae4d"


def _inventory(source: Path) -> tuple[str, ast.Module, list[ast.Call], set[str]]:
    text = source.read_text(encoding="utf-8")
    tree = ast.parse(text)
    calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    imports = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imports.update(
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    )
    return text, tree, calls, imports


def _labels(calls: list[ast.Call]) -> tuple[str, ...]:
    labels: list[str] = []
    for call in calls:
        first = call.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            labels.append(first.value)
        else:
            labels.append("")
    return tuple(labels)


def main(source_file: str, dossier_file: str) -> int:
    checks = CheckLedger("P137/C-SKY-001/S1")
    source = Path(source_file).resolve()
    dossier = Path(dossier_file).resolve()
    campaign = Path(__file__).resolve().parent
    frozen = campaign / "evidence" / "frozen-proposal.yaml"
    text, tree, source_calls, imports = _inventory(source)
    labels = _labels(source_calls)

    checks.check(
        "pinned S1 source hash",
        hashlib.sha256(source.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "pinned S1 dossier hash",
        hashlib.sha256(dossier.read_bytes()).hexdigest() == DOSSIER_SHA256,
    )
    checks.check(
        "frozen proposal hash",
        hashlib.sha256(frozen.read_bytes()).hexdigest()
        == FROZEN_PROPOSAL_SHA256,
    )
    checks.check("eleven source predicates", len(source_calls) == 11)
    checks.check(
        "source assertions are helper plus solve cardinality only",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 2,
    )
    checks.check(
        "source import inventory is closed",
        imports == {"numpy", "sympy", "scipy.integrate"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        text, filename=str(source)
    )
    checks.check(
        "S1 has no executable trapezoid compatibility event",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    prefixes = (
        "S1.1",
        "S1.2",
        "S1.3",
        "S1.4",
        "S1.5",
        "S1.6",
        "S1.7",
        "S1.8",
        "S1.9",
        "S1.G1",
        "S1.G2",
    )
    dispositions = (
        "retained_as_C_CC_001_reproduction",
        "retained_for_declared_profile_only",
        "retained_as_first_order_profile_potential",
        "retained_as_C_RPROF_001_massless_tail",
        "rejected_as_orientation_derivation",
        "rejected_wrong_numeric_equation_and_no_refinement",
        "retained_as_C_VIR_001_reproduction",
        "retained_for_declared_yukawa_profile",
        "qualified_as_formula_regression_not_cross_energy",
        "retained_as_declared_profile_sign_mutation",
        "rejected_as_schematic_assigned_orientation_literals",
    )
    checks.check(
        "all source predicates receive individual dispositions",
        len(labels) == len(dispositions) == len(prefixes)
        and all(prefix in label for prefix, label in zip(prefixes, labels)),
    )
    checks.check(
        "source tally mixes retained qualified and rejected predicates",
        sum(item.startswith("rejected") for item in dispositions) == 3
        and sum(item.startswith("retained") for item in dispositions) == 7
        and sum(item.startswith("qualified") for item in dispositions) == 1,
    )

    radius, mass, stiffness, strength = sp.symbols(
        "R m K P", positive=True
    )
    hessian = yukawa_radial_hessian(radius, mass)
    green = sp.exp(-mass * radius) / (4 * sp.pi * radius)
    transverse = -sp.exp(-mass * radius) * (1 + mass * radius) / (
        4 * sp.pi * radius**3
    )
    longitudinal = sp.exp(-mass * radius) * (
        mass**2 * radius**2 + 2 * mass * radius + 2
    ) / (4 * sp.pi * radius**3)
    anisotropic = sp.exp(-mass * radius) * (
        mass**2 * radius**2 + 3 * mass * radius + 3
    ) / (4 * sp.pi * radius**3)
    checks.check(
        "Yukawa Green function solves the homogeneous massive radial equation",
        sp.simplify(
            sp.diff(green, radius, 2)
            + 2 * sp.diff(green, radius) / radius
            - mass**2 * green
        )
        == 0,
    )
    checks.check(
        "canonical radial Hessian coefficients have exact normalization",
        sp.simplify(hessian.green - green) == 0
        and sp.simplify(hessian.transverse - transverse) == 0
        and sp.simplify(hessian.longitudinal - longitudinal) == 0
        and sp.simplify(hessian.anisotropic - anisotropic) == 0,
    )

    direction = sp.ImmutableMatrix((0, 0, 1))
    arbitrary = sp.ImmutableMatrix(
        ((0, 0, 1), (1, 0, 0), (0, 1, 0))
    )
    interaction = massive_triplet_dipole_interaction(
        radius,
        mass,
        stiffness,
        strength,
        direction,
        arbitrary,
    )
    hessian_matrix = (
        transverse * sp.eye(3)
        + anisotropic * direction * direction.T
    )
    direct_contraction = sp.trace(arbitrary.T * hessian_matrix)
    checks.check(
        "cross energy is the rotated Yukawa Hessian contraction",
        sp.simplify(
            interaction.interaction_energy
            - strength**2 * direct_contraction / stiffness
        )
        == 0,
    )
    source_pairing = -strength**2 * direct_contraction
    checks.check(
        "on-shell source pairing fixes the cross-energy sign",
        sp.simplify(
            interaction.interaction_energy + source_pairing / stiffness
        )
        == 0,
    )

    extrema = massive_triplet_dipole_extrema(
        radius, mass, stiffness, strength
    )
    minimum = -strength**2 * longitudinal / stiffness
    maximum = strength**2 * (longitudinal - 2 * transverse) / stiffness
    identity = strength**2 * mass**2 * green / stiffness
    checks.check(
        "three distinguished orientations match exact energy formulas",
        sp.simplify(extrema.most_attractive_energy - minimum) == 0
        and sp.simplify(extrema.most_repulsive_energy - maximum) == 0
        and sp.simplify(extrema.identity_energy - identity) == 0,
    )

    cosine, axial_square = sp.symbols("c z", real=True)
    contraction = (
        transverse
        + cosine * (transverse + longitudinal)
        + (longitudinal - transverse) * (1 - cosine) * axial_square
    )
    lower_certificate = (
        (transverse + longitudinal) * (1 + cosine)
        + (longitudinal - transverse) * (1 - cosine) * axial_square
    )
    upper_certificate = (
        (-2 * transverse) * (1 + cosine)
        + (longitudinal - transverse)
        * (1 - cosine)
        * (1 - axial_square)
    )
    checks.check(
        "Rodrigues lower-bound certificate is an exact identity",
        sp.simplify(contraction + longitudinal - lower_certificate) == 0,
    )
    checks.check(
        "Rodrigues upper-bound certificate is an exact identity",
        sp.simplify(
            longitudinal - 2 * transverse - contraction - upper_certificate
        )
        == 0,
    )
    checks.check(
        "all factors in both SO3 certificates have the required sign",
        sp.factor(transverse + longitudinal)
        == sp.exp(-mass * radius)
        * (mass**2 * radius**2 + mass * radius + 1)
        / (4 * sp.pi * radius**3)
        and sp.factor(longitudinal - transverse) == anisotropic
        and transverse.could_extract_minus_sign(),
    )

    minimum_interaction = massive_triplet_dipole_interaction(
        radius,
        mass,
        stiffness,
        strength,
        direction,
        extrema.most_attractive_orientation,
    )
    maximum_interaction = massive_triplet_dipole_interaction(
        radius,
        mass,
        stiffness,
        strength,
        direction,
        extrema.most_repulsive_orientation,
    )
    checks.check(
        "representative pi rotations saturate the global bounds",
        sp.simplify(minimum_interaction.interaction_energy - minimum) == 0
        and sp.simplify(maximum_interaction.interaction_energy - maximum) == 0,
    )
    checks.check(
        "most-attractive force is the negative fixed-orientation gradient",
        sp.simplify(
            extrema.most_attractive_radial_force
            + sp.diff(extrema.most_attractive_energy, radius)
        )
        == 0
        and extrema.most_attractive_radial_force.could_extract_minus_sign(),
    )
    checks.check(
        "massive interaction is finite range",
        sp.limit(radius**10 * extrema.most_attractive_energy, radius, sp.oo)
        == 0,
    )
    checks.check(
        "massless limit is the exact inverse-cube dipole energy",
        sp.simplify(
            sp.limit(extrema.most_attractive_energy, mass, 0, dir="+")
            + strength**2 / (2 * sp.pi * stiffness * radius**3)
        )
        == 0,
    )
    checks.check(
        "zero source stiffness and mass mutations remain visible",
        massive_triplet_dipole_extrema(
            radius, mass, stiffness, 0
        ).most_attractive_energy
        == 0
        and sp.simplify(
            extrema.most_attractive_energy.subs(stiffness, 2 * stiffness)
            - extrema.most_attractive_energy / 2
        )
        == 0
        and sp.simplify(
            extrema.most_attractive_energy.subs(strength, 2 * strength)
            - 4 * extrema.most_attractive_energy
        )
        == 0,
    )

    # S1's numeric RHS omits the final 1/R in the exact derivative of its own
    # declared profile. Its sign-only test cannot detect this mutation.
    source_numeric_rhs = -sp.exp(-mass * radius) * (
        mass + 1 / radius
    )
    exact_profile_rhs = sp.diff(sp.exp(-mass * radius) / radius, radius)
    checks.check(
        "S1 numeric force differs from its symbolic force by radius",
        sp.simplify(source_numeric_rhs / exact_profile_rhs - radius) == 0,
    )

    profile_amplitude, signal_speed = sp.symbols("kappa c0", positive=True)
    index = 1 + profile_amplitude * sp.exp(-mass * radius) / radius
    exact_slow_acceleration = (
        signal_speed**2 * sp.diff(index, radius) / (2 * index**3)
    )
    exact_slow_potential = signal_speed**2 * (index**-2 - 1) / 4
    checks.check(
        "declared optical profile has an exact conditional slow potential",
        sp.simplify(
            -sp.diff(exact_slow_potential, radius)
            - exact_slow_acceleration
        )
        == 0,
    )
    checks.check(
        "S1 Yukawa well is only the first-order optical profile term",
        sp.simplify(
            sp.diff(exact_slow_potential, profile_amplitude).subs(
                profile_amplitude, 0
            )
            + signal_speed**2 * sp.exp(-mass * radius) / (2 * radius)
        )
        == 0,
    )
    checks.check(
        "source-sign mutation reverses the interaction verdict",
        (-extrema.most_attractive_energy).could_extract_minus_sign() is False
        and (-extrema.most_repulsive_energy).could_extract_minus_sign(),
    )

    return checks.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    parser.add_argument("dossier_file")
    arguments = parser.parse_args()
    raise SystemExit(main(arguments.source_file, arguments.dossier_file))
