#!/usr/bin/env python3
"""Exact fixed-theory and parameter-family audit of predecessor source KI2."""

from __future__ import annotations

import ast
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys

import sympy as sp
import yaml

from substrate_framework.bps_energy import (
    bogomolny_density_decomposition,
    bps_bound_per_absolute_degree,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


FRAMEWORK_ROOT = Path("/home/dan/substrate-framework")
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / (
    "merged-framework/bridges/phase-34/"
    "bridge_KI2_epsilon_underdetermination.py"
)
DOSSIER = SOURCE_ROOT / (
    "merged-framework/bridges/phase-34/dossiers/Phase34-KI-dossier.md"
)

PINNED_HASHES = {
    SOURCE: "9e16fc6fafa940f43d559ea0f6a9c2730940d1247f36f655375c2f75f6fd1e81",
    DOSSIER: "e01fbee40d81ebae1fc6f9452c321e2914cb185cdf257ae226d849ea6392702b",
    FRAMEWORK_ROOT / "governance/releases/current.yaml":
        "d530afe41d0e88e3236c0f048a1352394028006f9217ed8019b6fdd30f4f7cb6",
    FRAMEWORK_ROOT / "governance/claims.yaml":
        "b2d68ae4e293301d402de4a0292445805ff42e26871b058fc74427aac37b7a0f",
    FRAMEWORK_ROOT / "src/substrate_framework/bps_energy.py":
        "09e3bb41b98ba21f2909117ab1361020dfc7f12ef2722e9f620a65336bbe7d13",
    FRAMEWORK_ROOT / "tests/test_bps_energy.py":
        "b52db01583cf351891074cd656ac51414bdb13d9dac2536398c9847cb0863edb",
    FRAMEWORK_ROOT / "campaigns/P171-ki1-exhaustive-coupling-inventory-audit/adjudication.yaml":
        "e1edc940b5dde99f19604d191d84bd76023714b76154d442472aa9c7277351b7",
    FRAMEWORK_ROOT / "memory/vantasner/decisions/KI1-refuted-review.md":
        "30496111961b7efa3773b7b4be6755901f631d97ee9c24687d8f925af592d8bd",
}


@dataclass(frozen=True)
class DimensionModel:
    """Declared natural-unit dimensions entering the four Lagrangian terms."""

    density: int
    derivative: int
    baryon_current: int
    potential: int


@dataclass(frozen=True)
class CouplingFlow:
    """Power-law scaling of lambda and mu by a positive parameter t."""

    lambda_power: int
    mu_power: int


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _run_source() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SOURCE)],
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def _solve_dimensions(model: DimensionModel) -> dict[sp.Symbol, sp.Expr]:
    d_f, d_e, d_lam, d_mu = sp.symbols("d_F d_e d_lam d_mu", real=True)
    equations = (
        sp.Eq(2 * d_f + 2 * model.derivative, model.density),
        sp.Eq(-2 * d_e + 4 * model.derivative, model.density),
        sp.Eq(2 * d_lam + 2 * model.baryon_current, model.density),
        sp.Eq(2 * d_mu + model.potential, model.density),
    )
    return sp.solve(equations, (d_f, d_e, d_lam, d_mu), dict=True)[0]


def _canonical_dimension_solution(candidate: object) -> bool:
    assert isinstance(candidate, DimensionModel)
    values = tuple(_solve_dimensions(candidate).values())
    return values == (1, 0, -1, 2)


def _preserves_fixed_bps_energy(candidate: object) -> bool:
    assert isinstance(candidate, CouplingFlow)
    t = sp.symbols("t", positive=True)
    baryon, potential, lam, mu = sp.symbols("B0 V lambda mu", positive=True)
    result = bogomolny_density_decomposition(
        baryon, potential, lam, mu, orientation=1
    )
    transformed = result.energy_density.subs(
        {
            lam: t ** candidate.lambda_power * lam,
            mu: t ** candidate.mu_power * mu,
        },
        simultaneous=True,
    )
    return sp.simplify(transformed - result.energy_density) == 0


def main() -> int:
    checks = CheckLedger("P172-KI2-FIXED-THEORY-AND-PARAMETER-FAMILY")
    for path, expected in PINNED_HASHES.items():
        checks.check(
            f"pinned artifact {path.name} retains its audited bytes",
            _digest(path) == expected,
        )

    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))
    check_calls = sorted(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ),
        key=lambda node: node.lineno,
    )
    labels = [
        re.match(r"(KI2\.[1-6])", ast.literal_eval(node.args[0])).group(1)
        for node in check_calls
    ]
    checks.check(
        "KI2 has exactly its six advertised predicates in order",
        labels == [f"KI2.{index}" for index in range(1, 7)],
    )
    imports = {
        alias.name
        for node in tree.body
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    checks.check(
        "KI2 has one assertion and imports only SymPy",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1
        and imports == {"sympy"},
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "KI2 has no NumPy integration-name compatibility surface",
        compatibility.numpy_aliases == ()
        and compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    replay = _run_source()
    checks.check(
        "native KI2 executes all six predicates with its exact terminal tally",
        replay.returncode == 0
        and replay.stderr == ""
        and replay.stdout.count("  PASS\n") == 6
        and "ALL 6 CHECKS PASS" in replay.stdout,
        replay.stderr[-500:],
    )

    canonical_dimensions = DimensionModel(4, 1, 3, 0)
    solved = _solve_dimensions(canonical_dimensions)
    d_f, d_e, d_lam, d_mu = tuple(solved)
    checks.check(
        "KI2.1's natural-unit dimension solution is exact and unique",
        tuple(solved.values()) == (1, 0, -1, 2)
        and sp.linear_eq_to_matrix(
            (
                2 * d_f + 2 - 4,
                -2 * d_e + 4 - 4,
                2 * d_lam + 6 - 4,
                2 * d_mu - 4,
            ),
            (d_f, d_e, d_lam, d_mu),
        )[0].rank() == 4,
    )
    checks.mutation_sensitive(
        "the dimension solution depends on density derivative current and potential inputs",
        _canonical_dimension_solution,
        canonical_dimensions,
        [
            DimensionModel(3, 1, 3, 0),
            DimensionModel(4, 0, 3, 0),
            DimensionModel(4, 1, 2, 0),
            DimensionModel(4, 1, 3, 2),
        ],
    )

    dimension_row = sp.Matrix([[1, 0, -1, 2]])
    declared_basis = sp.Matrix(
        [
            [0, 1, 0, 0],
            [1, 0, 1, 0],
            [-2, 0, 0, 1],
        ]
    ).T
    checks.check(
        "KI2.4's three exponent vectors form a basis of the dimension kernel",
        dimension_row.rank() == 1
        and len(dimension_row.nullspace()) == 3
        and dimension_row * declared_basis == sp.zeros(1, 3)
        and declared_basis.rank() == 3,
    )

    f_pi, e, lam, mu, coefficient = sp.symbols(
        "F_pi e lambda mu c_epsilon", positive=True
    )
    epsilon_ratio = (f_pi / e) / (lam * mu)
    quotient_identity = sp.simplify(
        epsilon_ratio
        - 1 / (e * (lam * f_pi) * (mu / f_pi**2))
    )
    checks.check(
        "the displayed quotient identity is exact for the locally defined ratio",
        quotient_identity == 0,
    )
    checks.check(
        "an arbitrary declared dimensionless normalization changes that ratio",
        coefficient in (coefficient * epsilon_ratio).free_symbols
        and coefficient not in epsilon_ratio.free_symbols
        and sp.simplify((coefficient * epsilon_ratio).subs(coefficient, 1)
                        - epsilon_ratio) == 0
        and sp.simplify((coefficient * epsilon_ratio).subs(coefficient, 2)
                        - epsilon_ratio) != 0,
    )
    checks.check(
        "equal energy dimensions do not prove two scales are independent",
        sp.simplify((lam * mu).subs(lam, coefficient * f_pi / (e * mu))
                    - coefficient * f_pi / e) == 0,
    )
    checks.check(
        "KI2 derives no map identifying its local ratio with C-BPS-003 epsilon",
        "eps_expr = (Fpi / ee) / (lam * muu)" in source_text
        and "from substrate_framework" not in source_text
        and "near_bps_mass_difference" not in source_text,
    )

    derived_assignment = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "derived_quantities"
                for target in node.targets)
    )
    assert isinstance(derived_assignment.value, ast.Dict)
    derived_values = tuple(ast.unparse(value) for value in derived_assignment.value.values)
    checks.check(
        "KI2.3's alleged complete invariant list has six standard-sector expressions only",
        len(derived_values) == 6
        and all(not re.search(r"\blam\b|\bmuu\b", value) for value in derived_values),
    )

    baryon, potential, average, t = sp.symbols(
        "B0 V W t", positive=True
    )
    decomposition = bogomolny_density_decomposition(
        baryon, potential, lam, mu, orientation=1
    )
    bound = bps_bound_per_absolute_degree(lam, mu, average)
    source_flow = {lam: t * lam, mu: t * mu}
    flowed_energy = sp.simplify(
        decomposition.energy_density.subs(source_flow, simultaneous=True)
    )
    flowed_square = sp.simplify(
        decomposition.square_density.subs(source_flow, simultaneous=True)
    )
    flowed_residual = sp.simplify(
        decomposition.saturation_residual.subs(source_flow, simultaneous=True)
    )
    flowed_bound = sp.simplify(bound.subs(source_flow, simultaneous=True))
    checks.check(
        "KI2's source flow scales the accepted BPS density and square by t squared",
        sp.simplify(flowed_energy - t**2 * decomposition.energy_density) == 0
        and sp.simplify(flowed_square - t**2 * decomposition.square_density) == 0,
    )
    checks.check(
        "the same flow scales the saturation residual by t and the bound by t squared",
        sp.simplify(flowed_residual - t * decomposition.saturation_residual) == 0
        and sp.simplify(flowed_bound - t**2 * bound) == 0,
    )
    checks.check(
        "KI2.6 itself admits that lambda times mu moves under the alleged symmetry",
        "lam_mu_moves = sp.simplify(Phi(lam * muu) - lam * muu) != 0" in source_text
        and sp.simplify((lam * mu).subs(source_flow, simultaneous=True) - lam * mu)
        != 0,
    )
    checks.mutation_sensitive(
        "fixed-theory energy invariance rejects every nontrivial declared coupling flow",
        _preserves_fixed_bps_energy,
        CouplingFlow(0, 0),
        [CouplingFlow(1, 1), CouplingFlow(1, -1), CouplingFlow(0, 1)],
    )
    checks.check(
        "the only positive power-law scaling preserving both fixed energy coefficients is identity",
        sp.linsolve(
            (2 * sp.Symbol("a"), 2 * sp.Symbol("b")),
            (sp.Symbol("a"), sp.Symbol("b")),
        ) == sp.FiniteSet((0, 0)),
    )

    epsilon_flowed = sp.simplify(
        epsilon_ratio.subs(source_flow, simultaneous=True)
    )
    checks.check(
        "the locally defined ratio does scale as epsilon over t squared and sweeps positive values",
        sp.simplify(epsilon_flowed - epsilon_ratio / t**2) == 0
        and sp.limit(epsilon_flowed, t, 0, "+") == sp.oo
        and sp.limit(epsilon_flowed, t, sp.oo) == 0,
    )
    target = sp.symbols("epsilon_target", positive=True)
    selected_lambda = sp.simplify(f_pi / (e * mu * target))
    checks.check(
        "the accepted positive parameter family realizes every positive ratio value",
        selected_lambda.is_positive is True
        and sp.simplify(epsilon_ratio.subs(lam, selected_lambda) - target) == 0,
    )
    checks.check(
        "this surjectivity is a family-of-theories statement because accepted objects change",
        sp.simplify(
            bound.subs(lam, selected_lambda)
            - bound.subs(lam, 2 * selected_lambda)
        ) != 0,
    )
    checks.check(
        "fixing the complete standard sector still leaves the declared ratio free across BPS inputs",
        sp.diff(epsilon_ratio.subs({f_pi: 93, e: 5}), lam) != 0
        and sp.diff(epsilon_ratio.subs({f_pi: 93, e: 5}), mu) != 0,
    )
    checks.check(
        "a product relation can pin the ratio without importing lambda and mu separately",
        sp.simplify(
            epsilon_ratio.subs(lam, f_pi / (e * mu * target)) - target
        ) == 0,
    )
    checks.check(
        "no finite current registry can prove KI2's claim about all future derived quantities",
        "present OR future" in source_text
        and "no derived quantity" in source_text,
    )

    registry = yaml.safe_load(
        (FRAMEWORK_ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
    )
    claims = {claim["id"]: claim for claim in registry["claims"]}
    checks.check(
        "C-BPS-001 explicitly contains the lambda-mu-dependent energy and bound",
        "(lambda*pi^2*B0)^2+mu^2*V(U)" in claims["C-BPS-001"]["statement"]
        and "2*lambda*mu*pi^2*abs(B)*W" in claims["C-BPS-001"]["statement"],
    )
    checks.check(
        "C-BPS-003 keeps epsilon abstract and does not identify KI2's ratio",
        "epsilon a positive dimensionless" in claims["C-BPS-003"]["statement"]
        and not re.search(
            r"\b(?:lambda|mu)\b", claims["C-BPS-003"]["statement"]
        ),
    )
    checks.check(
        "C-SK-001 fixes only a conditional standard scale and no individual parameter",
        "F_pi/e=16*pi*E_e" in claims["C-SK-001"]["statement"]
        and "No numerical comparator, individual F_pi or e value"
        in claims["C-SK-001"]["assumptions"][-1],
    )

    inventory = yaml.safe_load(
        (FRAMEWORK_ROOT / "migration/source-claims.yaml").read_text(encoding="utf-8")
    )
    units = {entry["source_unit"]: entry for entry in inventory["units"]}
    checks.check(
        "refuted KI1 cannot support KI2 while all MK counterrelations remain pending",
        units["KI1"]["disposition"] == "refuted"
        and all(units[label]["disposition"] == "pending_adjudication"
                for label in ("MK1", "MK2", "MK3")),
    )
    checks.check(
        "KI2 enters P172 with no accepted claim mapping",
        units["KI2"]["disposition"] == "pending_adjudication"
        and units["KI2"]["accepted_claims"] == [],
    )

    total = checks.finish()
    print(f"P172 KI2 FIXED THEORY AND PARAMETER FAMILY ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
