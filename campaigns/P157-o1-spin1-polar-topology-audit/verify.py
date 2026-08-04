#!/usr/bin/env python3
"""Exact source-aware verifier for the qualified O1 disposition."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.angular_defects import (
    full_polar_deck_transformation,
    full_polar_loop_class,
    polar_topology_ledger,
    projective_rp2_loop_class,
)
from substrate_framework.berry_holonomy import (
    closed_ray_berry_ledger,
    phase_transform_section,
)
from substrate_framework.nonabelian_holonomy import su2_holonomy_evidence
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.spin1_mean_field import (
    cartesian_to_spin1,
    fixed_density_spin1_selection,
    spin1_expectation,
    spin1_matrices,
    spin1_norm,
    spin1_orbit_ledger,
)
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P157-o1-spin1-polar-topology-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-7/"
    "bridge_O1_spin1_bec_rp2.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_AUDIT = CAMPAIGN / "evidence/source-audit.yaml"
SOURCE_SHA256 = "270877b5ae3507ba5000643333a06269dce2c6a2ec7dbd9ae86f8e2b6e77ef64"
FROZEN_SHA256 = "56a1431c8341d548ffc80359d4e0bc0e972e3dd0c896075b9de517a72d444a3c"
REVISION_SHA256 = "4389fabc4a5ca197602f1bd3abab27dcbdb1adcb6c194c6e5b2101265d3c1182"
REPRODUCTION_SHA256 = "d9c1b82ba56c3931301bb5e96c0a6068dd8ab9b517dcc23b686b1c610287b648"
SOURCE_AUDIT_SHA256 = "e03567c1be5b10342d3edeed291d0f8626a722a6126a2540ec7a5322f1c74e33"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _zero(value: object) -> bool:
    if isinstance(value, sp.MatrixBase):
        return all(sp.simplify(entry) == 0 for entry in value)
    return sp.simplify(value) == 0


def run() -> int:
    checks = CheckLedger("P157/O1-qualified")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned O1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check("source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256)
    checks.check("source audit hash", _sha256(SOURCE_AUDIT) == SOURCE_AUDIT_SHA256)
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("seven source predicates", len(source_checks) == 7)
    checks.check(
        "one source assertion",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    source_compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "O1 has no numerical integration compatibility surface",
        source_compatibility.numpy_aliases == ()
        and source_compatibility.legacy_references == 0
        and source_compatibility.current_references == 0,
    )
    checks.check(
        "source declares a fixed-ray phase section",
        "psi_chi = sp.exp(I * chi / 2) * (R_spin1(2, chi) * psi_polar_ref)"
        in source_text
        and "R_z(chi)|0> = |0>" in source_text,
    )
    checks.check(
        "source verdict omits the endpoint transition",
        "holo_2pi = sp.simplify(sp.exp(I * oint_2pi))" in source_text
        and "endpoint_transition" not in source_text,
    )

    phi = sp.Symbol("phi", real=True)
    reference = sp.ImmutableMatrix([0, 1, 0])
    fixed_section = sp.exp(sp.I * phi / 2) * reference
    fixed = closed_ray_berry_ledger(fixed_section, phi)
    checks.check(
        "O1 section has a constant projector and local minus one half connection",
        fixed.projector_is_constant
        and fixed.berry_connection == -sp.Rational(1, 2)
        and fixed.connection_integral == -sp.pi,
    )
    checks.check(
        "endpoint correction makes the fixed-ray holonomy trivial",
        fixed.endpoint_transition == -1
        and fixed.bare_integral_phase == -1
        and fixed.holonomy == 1,
    )
    opposite = closed_ray_berry_ledger(
        sp.exp(-sp.I * phi / 2) * reference,
        phi,
    )
    checks.check(
        "opposite phase gauge changes the local sign but not the fixed-ray holonomy",
        opposite.projector == fixed.projector
        and opposite.berry_connection == sp.Rational(1, 2)
        and opposite.endpoint_transition == -1
        and opposite.holonomy == fixed.holonomy == 1,
    )
    checks.check(
        "omitting the endpoint is a load-bearing mutation",
        fixed.bare_integral_phase != fixed.holonomy
        and opposite.bare_integral_phase != opposite.holonomy,
    )

    director = sp.ImmutableMatrix([sp.cos(phi / 2), sp.sin(phi / 2), 0])
    real_lift = cartesian_to_spin1(director)
    real_director = closed_ray_berry_ledger(real_lift, phi)
    checks.check(
        "genuine projective director loop moves the projector",
        not real_director.projector_is_constant
        and real_director.projector != fixed.projector,
    )
    checks.check(
        "real director lift carries its minus sign at the endpoint",
        real_director.berry_connection == 0
        and real_director.endpoint_transition == -1
        and real_director.bare_integral_phase == 1
        and real_director.holonomy == -1,
    )
    periodic_lift = phase_transform_section(real_lift, -phi / 2)
    periodic_director = closed_ray_berry_ledger(periodic_lift, phi)
    checks.check(
        "periodic director gauge carries the same holonomy in the integral",
        periodic_director.endpoint_transition == 1
        and periodic_director.berry_connection == sp.Rational(1, 2)
        and periodic_director.bare_integral_phase == -1
        and periodic_director.holonomy == real_director.holonomy == -1,
    )
    full_polar_section = phase_transform_section(real_lift, phi / 2)
    full_polar = closed_ray_berry_ledger(full_polar_section, phi)
    checks.check(
        "full-polar half generator closes by combined phase and director motion",
        full_polar.endpoint_transition == 1
        and not full_polar.projector_is_constant
        and full_polar.berry_connection == -sp.Rational(1, 2)
        and full_polar.holonomy == -1,
    )

    reference_orbit = spin1_orbit_ledger(reference)
    director_orbit = spin1_orbit_ledger(real_lift)
    checks.check(
        "accepted spin-one invariant classifies the representatives as polar",
        spin1_norm(real_lift) == 1
        and spin1_expectation(real_lift) == (0, 0, 0)
        and reference_orbit.projective_orbit == director_orbit.projective_orbit == "polar",
    )
    checks.check(
        "antipodal director maps to the same ray with the opposite spinor",
        _zero(cartesian_to_spin1(-director) + real_lift)
        and _zero(
            real_lift * real_lift.H
            - cartesian_to_spin1(-director) * cartesian_to_spin1(-director).H
        ),
    )
    spin_one_2pi = sp.ImmutableMatrix(
        (-sp.I * 2 * sp.pi * spin1_matrices()[2]).exp()
    )
    su2 = su2_holonomy_evidence()
    checks.check(
        "two-pi center action is representation typed",
        spin_one_2pi == sp.eye(3)
        and su2.adjoint_2pi == sp.eye(3)
        and su2.fundamental_2pi == -sp.eye(2),
    )
    checks.check(
        "O1 two-pi minus sign is the inserted phase not spin-one transport",
        _zero(fixed.section.subs(phi, 2 * sp.pi) + fixed.section.subs(phi, 0))
        and spin_one_2pi != -sp.eye(3),
    )

    topology = polar_topology_ledger()
    deck_one = full_polar_deck_transformation(1)
    deck_two = full_polar_deck_transformation(2)
    checks.check(
        "projective and full polar loop groups remain distinct",
        topology.projective_manifold == "RP2"
        and topology.projective_fundamental_group == "Z2"
        and topology.full_polar_manifold == "(S2 x U1)/Z2"
        and topology.full_polar_fundamental_group == "Z",
    )
    checks.check(
        "squaring the full-polar half generator is not the identity",
        deck_one.director_sign == -1
        and deck_one.phase_shift == sp.pi
        and deck_two.director_sign == 1
        and deck_two.phase_shift == 2 * sp.pi
        and projective_rp2_loop_class(2) == 0
        and full_polar_loop_class(2) == 2,
    )

    positive = fixed_density_spin1_selection(1, 1)
    negative = fixed_density_spin1_selection(1, -1)
    zero = fixed_density_spin1_selection(1, 0)
    checks.check(
        "polar phase selection requires the declared interaction sign",
        positive.minimizing_projective_orbits == ("polar",)
        and negative.minimizing_projective_orbits == ("ferromagnetic",)
        and zero.minimizing_projective_orbits == ("all_pure_spin1_rays",),
    )
    scalar_periodic = sp.exp(sp.I * phi)
    scalar_half = sp.exp(sp.I * phi / 2)
    checks.check(
        "scalar spin-frame control does not establish half-integer U1 closure",
        sp.diff(sp.Integer(1), phi) == 0
        and sp.simplify(scalar_periodic.subs(phi, 2 * sp.pi) - scalar_periodic.subs(phi, 0)) == 0
        and sp.simplify(scalar_half.subs(phi, 2 * sp.pi) - scalar_half.subs(phi, 0)) != 0,
    )
    same_values = {
        "director_ray_holonomy": real_director.holonomy,
        "fundamental_su2_center": su2.fundamental_2pi[0, 0],
        "abstract_parity_character": sp.Integer(-1),
    }
    checks.check(
        "equal minus-one values leave their physical dictionaries free",
        len(set(same_values)) == 3
        and all(value == -1 for value in same_values.values()),
    )
    checks.check(
        "mutable P157 code has no executable legacy integration access",
        all(
            audit_numpy_trapezoid_compatibility(
                path.read_text(encoding="utf-8"),
                filename=str(path),
            ).legacy_references
            == 0
            for path in (
                Path(__file__),
                CAMPAIGN / "reviews/independent_spin1_topology_review.py",
                CAMPAIGN / "reviews/replay_source_graph.py",
            )
        ),
    )

    return checks.finish()


if __name__ == "__main__":
    tally = run()
    print(f"P157 PRIMARY ALL {tally} CHECKS PASS")
