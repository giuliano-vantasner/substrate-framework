#!/usr/bin/env python3
"""Primary exact verifier for TX4 and C-FLO/ROT/RMAP promotion candidates."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.rational_map_stability import (
    degree_two_rational_map_hessian,
    degree_two_rational_map_quadratic_form,
)
from substrate_framework.rotating_stability import (
    axisymmetric_density_inertia_relation,
    axisymmetric_transverse_rotor_evidence,
    co_rotating_linear_system_evidence,
    finite_matrix_power_evidence,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-40/"
    "bridge_TX4_floquet_stability.py"
)
SOURCE_SHA256 = "c88ff5fe65473756d36a29546fae4da417c56d7539dcfd8e58304bd0ab7b335f"
RELEASE_SHA256 = "910087c9ccfa45867b6bf8a1bb47246481ccbabc2c00fdbfa2a5ae85c55060c6"
EXACT_SHAPE_ORACLE = (
    ROOT
    / "campaigns/P183-tx4-floquet-stability-audit/attempts/0006/"
    "derive_exact_shape_hessian.py"
)
EXACT_SHAPE_ORACLE_SHA256 = (
    "7f2a3d6f721ba50bc658f79d08df69cc640ea464a81413ca6bd3dd4bb20bd97c"
)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    checks = CheckLedger("P183/TX4/C-FLO-001/C-ROT-001/C-RMAP-003")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.134.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "frozen exact shape oracle remains pinned",
        _digest(EXACT_SHAPE_ORACLE) == EXACT_SHAPE_ORACLE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    lexical_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source lexical and assertion inventory is exact",
        len(lexical_checks) == 8 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "TX4 has no NumPy trapezoidal compatibility surface",
        compatibility.current_references == 0
        and compatibility.legacy_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "unconditional dynamic-stability headline is not one source predicate",
        "The rotating B=2 Skyrmion is DYNAMICALLY STABLE" in source_text
        and not any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
            and any(
                isinstance(argument, ast.Constant)
                and isinstance(argument.value, str)
                and "DYNAMICALLY STABLE" in argument.value
                for argument in node.args
            )
            for node in ast.walk(tree)
        ),
    )

    omega = sp.Symbol("Omega", positive=True)
    period = 2 * sp.pi / omega
    frame = sp.ImmutableMatrix([[0, -omega], [omega, 0]])
    nilpotent = sp.ImmutableMatrix([[0, 1], [0, 0]])
    rotating = co_rotating_linear_system_evidence(
        frame + nilpotent, frame, period
    )
    checks.check(
        "periodic co-rotating change gives the exact autonomous generator",
        rotating.frame_periodic
        and rotating.transformed_generator == nilpotent
        and rotating.generator_identity_residual == sp.zeros(2),
    )
    checks.check(
        "laboratory and body monodromy agree only after the periodic frame closes",
        rotating.frame_at_period == sp.eye(2)
        and rotating.laboratory_monodromy
        == rotating.transformed_monodromy
        == sp.eye(2) + period * nilpotent,
    )
    checks.check(
        "unit multipliers with a Jordan block are not power bounded",
        rotating.transformed_power_evidence.modulus_squared == (1,)
        and rotating.transformed_power_evidence.unit_circle_eigenvalues_semisimple
        is False
        and rotating.transformed_power_evidence.powers_bounded is False,
    )
    unstable = finite_matrix_power_evidence(sp.diag(sp.E, 1))
    bounded = finite_matrix_power_evidence(sp.diag(-1, 1))
    checks.check(
        "exact finite-matrix criterion separates exponential growth and bounded powers",
        unstable.all_inside_closed_unit_disk is False
        and unstable.powers_bounded is False
        and bounded.all_inside_closed_unit_disk is True
        and bounded.unit_circle_eigenvalues_semisimple is True
        and bounded.powers_bounded is True,
    )
    checks.check(
        "time independence alone is insensitive to stability",
        nilpotent.is_nilpotent()
        and finite_matrix_power_evidence((period * nilpotent).exp()).powers_bounded
        is False
        and finite_matrix_power_evidence(sp.eye(2)).powers_bounded is True,
    )

    inertia = sp.Symbol("A", positive=True)
    excess = sp.Symbol("Delta", positive=True)
    time = sp.Symbol("t", real=True)
    rotor = axisymmetric_transverse_rotor_evidence(
        inertia, inertia + excess, omega, time
    )
    checks.check(
        "declared oblate free-rotor equilibrium and Euler generator are exact",
        rotor.euler_rhs.subs(
            dict(zip(rotor.angular_velocity_symbols, rotor.base_equilibrium, strict=True))
        )
        == sp.zeros(3, 1)
        and rotor.linearized_generator.rank() == 1
        and rotor.linearized_generator**2 == sp.zeros(3),
    )
    checks.check(
        "rotor fundamental matrix exposes the defective unit monodromy",
        rotor.fundamental_matrix == sp.eye(3) + time * rotor.linearized_generator
        and rotor.monodromy_power_evidence.modulus_squared == (1,)
        and rotor.monodromy_power_evidence.unit_circle_eigenvalues_semisimple
        is False
        and rotor.monodromy_power_evidence.powers_bounded is False,
    )
    checks.check(
        "both declared rotor invariants have zero exact derivative",
        rotor.invariant_derivatives == (0, 0),
    )
    checks.check(
        "nearby rotor trajectory solves the nonlinear Euler equations exactly",
        rotor.exact_solution_residual == sp.zeros(3, 1),
    )
    epsilon = next(
        symbol
        for symbol in rotor.fixed_equilibrium_initial_distance_squared.free_symbols
        if symbol.name == "axial_perturbation"
    )
    checks.check(
        "arbitrarily small axial perturbations leave one fixed equilibrium by order one",
        sp.limit(
            rotor.fixed_equilibrium_initial_distance_squared,
            epsilon,
            0,
            dir="+",
        )
        == 0
        and sp.limit(
            rotor.fixed_equilibrium_witness_distance_squared,
            epsilon,
            0,
            dir="+",
        )
        == 2 * omega**2,
    )
    radius = next(
        symbol
        for symbol in rotor.equilibrium_circle_distance_squared.free_symbols
        if symbol.name == "transverse_radius"
    )
    checks.check(
        "distance to the whole transverse equilibrium circle stays constant",
        rotor.equilibrium_circle_distance_squared
        == (omega - radius) ** 2 + epsilon**2
        and not rotor.equilibrium_circle_distance_squared.has(time),
    )
    density = axisymmetric_density_inertia_relation(
        sp.Symbol("R2", real=True), sp.Symbol("Z", real=True)
    )
    checks.check(
        "ordinary density inertia relation is exact in the declared STF convention",
        density.relation_residual == 0
        and sp.simplify(
            density.symmetry_axis_inertia
            - density.transverse_axis_inertia
            + sp.Rational(3, 2) * density.normalized_stf_zz
        )
        == 0,
    )
    checks.check(
        "wrong STF normalization mutation breaks the inertia relation",
        sp.simplify(
            density.symmetry_axis_inertia
            - density.transverse_axis_inertia
            + density.normalized_stf_zz
        )
        != 0,
    )

    shape = degree_two_rational_map_hessian()
    checks.check(
        "degree-two axial map is exactly stationary at the accepted angular value",
        shape.angular_functional == sp.pi + sp.Rational(8, 3)
        and shape.gradient == sp.zeros(10, 1),
    )
    checks.check(
        "exact chart Hessian is symmetric positive semidefinite with rank five",
        shape.hessian == shape.hessian.T
        and shape.hessian.is_positive_semidefinite is True
        and shape.hessian_rank == 5
        and shape.hessian_nullity == 5,
    )
    expected_eigenvalues = (
        (sp.S.Zero, 5),
        (sp.pi, 1),
        (sp.pi + sp.Rational(16, 3), 2),
        (7 * sp.pi + sp.Rational(64, 3), 2),
    )
    checks.check(
        "all exact Hessian eigenvalues and multiplicities are derived",
        all(
            sum(sp.simplify(item - value) == 0 for item in shape.eigenvalues)
            == count
            for value, count in expected_eigenvalues
        ),
    )
    checks.check(
        "five independent group tangents span the entire exact kernel",
        shape.symmetry_rank == 5
        and shape.symmetry_residual == sp.zeros(10, 5)
        and shape.kernel_is_exact_symmetry_span
        and sp.Matrix.hstack(
            *shape.hessian.nullspace(), *shape.symmetry_tangents.columnspace()
        ).rank()
        == 5,
    )
    restricted = sp.simplify(
        shape.positive_complement.T
        * shape.hessian
        * shape.positive_complement
    )
    a = sp.pi / 2 + sp.Rational(8, 3)
    b = sp.Rational(32, 3) + 7 * sp.pi / 2
    checks.check(
        "declared complementary chart directions have exact positive curvature",
        shape.positive_on_declared_complement
        and restricted == sp.diag(4 * a, 4 * a, 4 * b, 4 * b, sp.pi),
    )
    direction = sp.zeros(10, 1)
    direction[8] = 1
    checks.check(
        "canonical quadratic form agrees with the exact Hessian normalization",
        degree_two_rational_map_quadratic_form(direction) == sp.pi / 2,
    )
    negative_mutation = shape.hessian - 2 * sp.pi * direction * direction.T
    checks.check(
        "negative-curvature and nonstationary mutations break local-minimum evidence",
        negative_mutation.is_positive_semidefinite is False
        and (direction.T * negative_mutation * direction)[0] == -sp.pi
        and shape.gradient + direction != sp.zeros(10, 1),
    )
    source_positive = (3.14191, 8.47528, 8.47528, 43.3256, 43.3256)
    checks.check(
        "source finite-difference positive modes agree within their stated resolution",
        all(
            abs(observed - float(exact.evalf())) < 2e-3
            for observed, exact in zip(
                source_positive, shape.positive_eigenvalues, strict=True
            )
        ),
    )

    rotating_text = (
        ROOT / "src/substrate_framework/rotating_stability.py"
    ).read_text(encoding="utf-8")
    shape_text = (
        ROOT / "src/substrate_framework/rational_map_stability.py"
    ).read_text(encoding="utf-8")
    checks.check(
        "canonical APIs state collective and full-field scope ceilings",
        "does not construct a field action" in rotating_text
        and "need not equal a field theory's collective rotational metric" in rotating_text
        and "not a full three-dimensional field Hessian" in shape_text
        and "dynamical stability" in shape_text,
    )
    mutable_compatibility = audit_numpy_trapezoid_compatibility(
        rotating_text + "\n" + shape_text,
        filename="P183 canonical modules",
    )
    checks.check(
        "mutable P183 modules contain no legacy NumPy integration name",
        mutable_compatibility.legacy_references == 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
