"""Primary exact verifier for P068 angular-defect energy and topology."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.angular_defects import (
    annular_angular_energy,
    equal_split_shell_ledger,
    full_polar_deck_transformation,
    full_polar_loop_class,
    half_quantum_pair_ledger,
    polar_topology_ledger,
    projective_rp2_loop_class,
)
from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_ME2_half_quantum_vortex.py"
)
SOURCE_SHA256 = "40eec343312cc85d442471a224c0501071ea556308b517e5c8b1efe067a789e4"


def main() -> int:
    ledger = CheckLedger("P068")
    ledger.check("hash-pinned ME2 source exists", SOURCE.is_file())
    ledger.check(
        "hash-pinned ME2 source integrity",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    ledger.check(
        "ME2 energy helper is additive isolated-copy arithmetic",
        "return count * K * charge ** 2 * L" in source_text,
    )
    ledger.check(
        "ME2 constructs no separation interaction director stiffness or core term",
        all(
            token not in source_text
            for token in (
                "separation_radius",
                "director_stiffness",
                "core_energy",
                "cross_energy",
            )
        ),
    )
    ledger.check(
        "ME2 topology is implemented as charge modulo one",
        "z2_class = sp.Mod(2 * half, 1)" in source_text
        and "classes = {sp.Mod(0, 1), sp.Mod(half, 1)}" in source_text,
    )

    radius, angle = sp.symbols("r phi", positive=True, real=True)
    stiffness, charge = sp.symbols("K q", positive=True, real=True)
    inner, outer = sp.symbols("xi R", positive=True, real=True)
    direct = sp.integrate(
        stiffness * (charge / radius) ** 2 * radius / 2,
        (angle, 0, 2 * sp.pi),
        (radius, inner, outer),
    )
    ledger.check(
        "direct polar integration gives the annular logarithmic energy",
        sp.simplify(
            direct - sp.pi * stiffness * charge**2 * sp.log(outer / inner)
        )
        == 0,
    )
    ledger.check(
        "canonical annular API retains charge squared and both cutoffs",
        annular_angular_energy(3, sp.Rational(1, 2), 1, 16)
        == 3 * sp.pi * sp.log(2),
    )
    ledger.mutation_sensitive(
        "annular normalization rejects missing pi half and charge square",
        lambda candidate: sp.simplify(candidate - 2 * sp.pi) == 0,
        annular_angular_energy(2, 1, 1, sp.E),
        [sp.Integer(2), sp.pi, 4 * sp.pi],
    )

    split = equal_split_shell_ledger(1, 1, 2, 1, 4, 16)
    ledger.check(
        "fixed-charge half split retains near and common far shells",
        split.near_energy == sp.pi * sp.log(2)
        and sp.simplify(split.far_energy - 2 * sp.pi * sp.log(2)) == 0
        and split.field_energy_ratio == sp.Rational(3, 4),
    )
    ledger.check(
        "ME2 one-half ratio is the vanished-far-shell endpoint",
        equal_split_shell_ledger(1, 1, 2, 1, 16, 16).field_energy_ratio
        == sp.Rational(1, 2)
        and split.independent_copy_ratio == sp.Rational(1, 2),
    )
    ledger.check(
        "coincident split scale restores the unsplit field energy",
        equal_split_shell_ledger(1, 1, 2, 1, 1, 16).field_energy_ratio == 1,
    )
    ledger.mutation_sensitive(
        "fixed-boundary split oracle requires the common far field",
        lambda candidate: sp.simplify(candidate - split.split_total_energy) == 0,
        split.near_energy + split.far_energy,
        [split.near_energy, 2 * split.near_energy, split.unsplit_field_energy],
    )
    costly = equal_split_shell_ledger(
        1, 1, 2, 1, 4, 16, piece_core_energy=sp.pi, unsplit_core_energy=0
    )
    ledger.check(
        "declared core energies can reverse the field-only split preference",
        split.split_minus_unsplit < 0 and costly.split_minus_unsplit > 0,
    )
    for count in (1, 2, 3, 5):
        result = equal_split_shell_ledger(2, 1, count, 1, 4, 16)
        expected = sp.simplify(
            2 * sp.pi * (sp.Rational(1, count) * sp.log(4) + sp.log(4))
        )
        ledger.check(
            f"{count}-piece shell ledger keeps total-charge far energy",
            sp.simplify(result.split_total_energy - expected) == 0,
        )

    topology = polar_topology_ledger()
    ledger.check(
        "projective polar loops form Z2 with order-two generator",
        topology.projective_fundamental_group == "Z2"
        and projective_rp2_loop_class(1) == 1
        and projective_rp2_loop_class(2) == 0,
    )
    ledger.check(
        "full polar deck transformations form an infinite integer chain",
        topology.full_polar_fundamental_group == "Z"
        and full_polar_loop_class(1) == 1
        and full_polar_loop_class(2) == 2
        and full_polar_loop_class(3) == 3,
    )
    first = full_polar_deck_transformation(1)
    second = full_polar_deck_transformation(2)
    ledger.check(
        "half generator squares to a nontrivial integer phase vortex in full polar order",
        first.director_sign == -1
        and first.phase_shift == sp.pi
        and second.director_sign == 1
        and second.phase_shift == 2 * sp.pi
        and topology.full_generator_square == "nontrivial_integer_phase_vortex",
    )
    ledger.mutation_sensitive(
        "topology oracle distinguishes projective and full generator squares",
        lambda candidate: candidate == (0, 2),
        (projective_rp2_loop_class(2), full_polar_loop_class(2)),
        [(0, 0), (2, 0), (1, 2)],
    )

    equal_stiffness = half_quantum_pair_ledger(1, 1, 1, sp.E)
    soft_director = half_quantum_pair_ledger(1, sp.Rational(1, 2), 1, sp.E)
    ledger.check(
        "equal phase and director stiffness removes ME2's claimed one-half advantage",
        equal_stiffness.zero_core_field_ratio == 1
        and equal_stiffness.pair_minus_integer == 0,
    )
    ledger.check(
        "softer director gives a conditional field-only half-pair advantage",
        soft_director.zero_core_field_ratio == sp.Rational(3, 4)
        and soft_director.pair_minus_integer == -sp.pi / 4,
    )
    core_reversed = half_quantum_pair_ledger(
        1,
        sp.Rational(1, 2),
        1,
        sp.E,
        half_core_energy=sp.pi,
        integer_core_energy=0,
    )
    ledger.check(
        "half-core cost can reverse an unequal-stiffness preference",
        core_reversed.pair_minus_integer > 0,
    )
    ledger.mutation_sensitive(
        "half-pair comparison retains director stiffness and both core terms",
        lambda candidate: sp.simplify(candidate - soft_director.pair_minus_integer)
        == 0,
        soft_director.pair_minus_integer,
        [
            -sp.pi / 2,
            soft_director.pair_minus_integer + sp.pi,
            -soft_director.pair_minus_integer,
        ],
    )

    invalid_rejections = []
    for operation in (
        lambda: annular_angular_energy(1, 1, 2, 1),
        lambda: equal_split_shell_ledger(1, 1, 0, 1, 2, 4),
        lambda: equal_split_shell_ledger(1, 1, 2, 1, 5, 4),
        lambda: full_polar_deck_transformation(sp.Rational(1, 2)),
        lambda: half_quantum_pair_ledger(1, 0, 1, 2),
    ):
        try:
            operation()
        except ValueError:
            invalid_rejections.append(True)
    ledger.check(
        "defect APIs reject invalid radii counts deck steps and stiffnesses",
        invalid_rejections == [True, True, True, True, True],
    )
    canonical_source = Path("src/substrate_framework/angular_defects.py").read_text(
        encoding="utf-8"
    )
    ledger.check(
        "P068 exact ledgers use no NumPy quadrature alias",
        "np." + "trapz" not in canonical_source
        and "np." + "trapezoid" not in canonical_source,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
