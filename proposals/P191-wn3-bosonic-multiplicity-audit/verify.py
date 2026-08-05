#!/usr/bin/env python3
"""Primary exact verifier for the WN3 bosonic Fock audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.bosonic_fock import (
    bosonic_cosine_matrix_element,
    bosonic_cosine_matrix_element_square,
    bosonic_fock_rung,
    factorial_one_mass,
    factorial_one_modes,
    factorial_one_total_mass,
    normalized_factorial_one_mass,
    truncated_bosonic_fock_ladder,
)
from substrate_framework.cosine_vertices import vacuum_one_high_coefficient
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
PROPOSAL = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-37/"
    "bridge_WN3_amplitude_scale_and_multiplicity.py"
)
SOURCE_SHA256 = "8a13c8b2af4d89297a11b3ef7460cc1f35fe274dc4affb2b9a7d3649bc237e88"
RELEASE_SHA256 = "d871dcd50df14cf7acf3d8def8a4d9e7b1f59e99ab6b6ba57ee060dd686e89cb"
FORMULA_FREEZE_SHA256 = "8e743fe13581c2b454c1d1509cd2ff098afde9d55c98088ad9c53c2d39d3dd88"


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("C-OSC-001")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.141.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        _digest(PROPOSAL / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "source predicate inventory remains exact",
        len(source_checks) == 19
        and not any(isinstance(node, ast.Assert) for node in ast.walk(source_tree)),
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "immutable source has no NumPy quadrature compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source parity switch and rate labels remain explicit audit targets",
        all(
            token in source_text
            for token in (
                "for n in [1, 3, 5, 7, 9]",
                "derived = lambda n",
                "even orders must be open",
                "FGR rate weight",
            )
        ),
    )

    for level in range(25):
        rung = bosonic_fock_rung(level)
        checks.check(
            f"infinite rung {level} has exact ladder and factorial data",
            rung.annihilation_coefficient == sp.sqrt(level)
            and rung.creation_coefficient == sp.sqrt(level + 1)
            and rung.number_coefficient == level
            and rung.reverse_number_coefficient == level + 1
            and rung.commutator_coefficient == 1
            and rung.repeated_creation_vacuum_coefficient
            == sp.sqrt(sp.factorial(level))
            and rung.repeated_creation_vacuum_norm_squared == sp.factorial(level),
        )
    checks.check(
        "repeated-creation coefficient obeys the universal induction step",
        all(
            sp.simplify(
                bosonic_fock_rung(level + 1).repeated_creation_vacuum_coefficient
                - sp.sqrt(level + 1)
                * bosonic_fock_rung(level).repeated_creation_vacuum_coefficient
            )
            == 0
            for level in range(24)
        ),
    )
    selected_rung = bosonic_fock_rung(5)
    expected_rung = (
        sp.sqrt(5),
        sp.sqrt(6),
        sp.Integer(5),
        sp.Integer(6),
        sp.Integer(1),
        sp.sqrt(120),
        sp.Integer(120),
    )
    checks.mutation_sensitive(
        "ladder coefficients commutator and factorial norm",
        lambda candidate: candidate == expected_rung,
        (
            selected_rung.annihilation_coefficient,
            selected_rung.creation_coefficient,
            selected_rung.number_coefficient,
            selected_rung.reverse_number_coefficient,
            selected_rung.commutator_coefficient,
            selected_rung.repeated_creation_vacuum_coefficient,
            selected_rung.repeated_creation_vacuum_norm_squared,
        ),
        (
            (sp.sqrt(6), sp.sqrt(5), 5, 6, 1, sp.sqrt(120), 120),
            (sp.sqrt(5), sp.sqrt(6), 5, 6, -1, sp.sqrt(120), 120),
            (sp.sqrt(5), sp.sqrt(6), 5, 6, 1, sp.sqrt(24), 24),
        ),
    )

    for dimension in (1, 2, 5, 12):
        truncated = truncated_bosonic_fock_ladder(dimension)
        checks.check(
            f"dimension {dimension} has the exact top-state commutator defect",
            truncated.commutator == truncated.expected_commutator
            and truncated.identity_minus_commutator
            == dimension * truncated.top_projector
            and truncated.commutator_trace == 0
            and sp.trace(truncated.identity) == dimension,
        )
    truncated = truncated_bosonic_fock_ladder(12)
    checks.check(
        "source dimension has identity interior and negative eleven top entry",
        truncated.commutator[:11, :11] == sp.eye(11)
        and truncated.commutator[11, 11] == -11,
    )
    checks.mutation_sensitive(
        "finite top-state defect coefficient",
        lambda candidate: candidate == truncated.commutator,
        truncated.identity - 12 * truncated.top_projector,
        (
            truncated.identity,
            truncated.identity - 11 * truncated.top_projector,
            -truncated.identity + 12 * truncated.top_projector,
        ),
    )

    coordinate = truncated.annihilation + truncated.creation
    vacuum = sp.zeros(12, 1)
    vacuum[0] = 1
    for order in range(10):
        target = sp.zeros(1, 12)
        target[0, order] = 1
        checks.check(
            f"full coordinate power reaches level {order} with sqrt factorial",
            sp.simplify((target * coordinate**order * vacuum)[0])
            == sp.sqrt(sp.factorial(order)),
        )

    amplitude, high_scale, low_scale = sp.symbols("U h ell", real=True, nonzero=True)
    for order in range(10):
        element = bosonic_cosine_matrix_element(
            order,
            amplitude=amplitude,
            high_scale=high_scale,
            low_scale=low_scale,
        )
        classical = vacuum_one_high_coefficient(
            order,
            amplitude=amplitude,
            high_scale=high_scale,
            low_scale=low_scale,
        )
        checks.check(
            f"order {order} composition equals coefficient times factorial norm",
            sp.simplify(element - classical * sp.sqrt(sp.factorial(order))) == 0,
        )
        square = bosonic_cosine_matrix_element_square(
            order,
            amplitude=amplitude,
            high_scale=high_scale,
            low_scale=low_scale,
        )
        expected_square = (
            amplitude**2
            * high_scale**2
            * low_scale ** (2 * order)
            / sp.factorial(order)
            if order % 2
            else 0
        )
        checks.check(
            f"order {order} square retains parity and one factorial",
            sp.simplify(square - expected_square) == 0,
        )
    selected_square = bosonic_cosine_matrix_element_square(
        5,
        amplitude=amplitude,
        high_scale=high_scale,
        low_scale=low_scale,
    )
    checks.mutation_sensitive(
        "conditional composition powers parity and factorial",
        lambda candidate: sp.simplify(candidate - selected_square) == 0,
        amplitude**2 * high_scale**2 * low_scale**10 / sp.factorial(5),
        (
            amplitude**2 * high_scale**2 * low_scale**5 / sp.factorial(5),
            amplitude**2 * high_scale**2 * low_scale**10 / sp.factorial(5) ** 2,
            amplitude * high_scale**2 * low_scale**10 / sp.factorial(5),
            -selected_square,
        ),
    )
    checks.check(
        "no bosonic factor reopens any sampled even cosine order",
        all(
            bosonic_cosine_matrix_element_square(order) == 0
            for order in range(0, 14, 2)
        ),
    )

    intensity = sp.Symbol("S", positive=True)
    totals = {
        support: factorial_one_total_mass(intensity=intensity, support=support)
        for support in ("all_nonnegative", "positive", "positive_odd")
    }
    checks.check(
        "three declared supports have distinct exact normalizers",
        totals["all_nonnegative"] == sp.exp(intensity)
        and totals["positive"] == sp.exp(intensity) - 1
        and totals["positive_odd"] == sp.sinh(intensity),
    )
    checks.check(
        "support predicates distinguish vacuum positive and positive odd orders",
        factorial_one_mass(0, intensity=intensity, support="all_nonnegative") == 1
        and factorial_one_mass(0, intensity=intensity, support="positive") == 0
        and factorial_one_mass(2, intensity=intensity, support="positive_odd") == 0
        and factorial_one_mass(3, intensity=intensity, support="positive_odd")
        == intensity**3 / 6,
    )
    checks.check(
        "normalized positive-odd composition uses sinh and retains even zero",
        normalized_factorial_one_mass(
            3,
            intensity=intensity,
            support="positive_odd",
        )
        == intensity**3 / (6 * sp.sinh(intensity))
        and normalized_factorial_one_mass(
            2,
            intensity=intensity,
            support="positive_odd",
        )
        == 0,
    )
    checks.mutation_sensitive(
        "factorial-one sample-space normalizers",
        lambda candidate: candidate
        == (
            sp.exp(intensity),
            sp.exp(intensity) - 1,
            sp.sinh(intensity),
        ),
        tuple(totals[support] for support in ("all_nonnegative", "positive", "positive_odd")),
        (
            (sp.exp(intensity) - 1, sp.exp(intensity), sp.sinh(intensity)),
            (sp.exp(intensity), sp.exp(intensity) - 1, sp.cosh(intensity)),
            (sp.exp(intensity), sp.exp(intensity), sp.sinh(intensity)),
        ),
    )

    symbolic_order = sp.Symbol("n", integer=True, nonnegative=True)
    adjacent_ratio = sp.combsimp(
        (intensity ** (symbolic_order + 1) / sp.factorial(symbolic_order + 1))
        / (intensity**symbolic_order / sp.factorial(symbolic_order))
    )
    adjacent_odd_ratio = sp.combsimp(
        (intensity ** (symbolic_order + 2) / sp.factorial(symbolic_order + 2))
        / (intensity**symbolic_order / sp.factorial(symbolic_order))
    )
    checks.check(
        "fresh adjacent ratios derive the ordinary and odd mode criteria",
        adjacent_ratio == intensity / (symbolic_order + 1)
        and sp.simplify(
            adjacent_odd_ratio
            - intensity**2 / ((symbolic_order + 1) * (symbolic_order + 2))
        )
        == 0,
    )
    checks.check(
        "integer source intensity preserves every ordinary tie",
        factorial_one_modes(intensity=25, support="all_nonnegative") == (24, 25)
        and factorial_one_modes(intensity=25, support="positive") == (24, 25),
    )
    checks.check(
        "positive-odd source composition has a distinct unique mode",
        factorial_one_modes(intensity=25, support="positive_odd") == (25,)
        and factorial_one_modes(intensity=49, support="positive_odd") == (49,),
    )
    checks.mutation_sensitive(
        "mode support and tie handling",
        lambda candidate: candidate == ((24, 25), (25,), (4, 5)),
        (
            factorial_one_modes(intensity=25, support="positive"),
            factorial_one_modes(intensity=25, support="positive_odd"),
            factorial_one_modes(intensity=5, support="positive"),
        ),
        (
            ((25,), (25,), (5,)),
            ((24, 25), (24, 25), (4, 5)),
        ),
    )

    algebraic_square = bosonic_cosine_matrix_element_square(3, low_scale=5)
    coupling, spectral_density = sp.symbols("g rho", real=True)
    candidate_rate = sp.factor(coupling**2 * algebraic_square * spectral_density)
    checks.check(
        "zero coupling and zero spectral density independently null a putative rate",
        candidate_rate.subs(coupling, 0) == 0
        and candidate_rate.subs(spectral_density, 0) == 0
        and algebraic_square != 0,
    )
    checks.check(
        "single-mode occupation and physical ceilings are explicit",
        "not a count of distinct single-mode final states"
        in " ".join(bosonic_fock_rung.__doc__.split())
        and "not a rate" in " ".join(bosonic_cosine_matrix_element.__doc__.split())
        and "not a physical occurrence law or rate"
        in " ".join(factorial_one_mass.__doc__.split())
        and "high-sector operator and state element"
        in " ".join(bosonic_cosine_matrix_element.__doc__.split()),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
