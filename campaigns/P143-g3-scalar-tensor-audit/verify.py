from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.einstein_scalar import (
    massless_scalar_flat_flrw,
    minimally_coupled_scalar_stress,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "8d462ce2bfd57bfced9fdedd511e9d2711e0c2454bc0d0441c681288495719ba"
DOSSIER_SHA256 = "4860923f422d5dfc24155a5b5d6788e9d3245e42cdfa1cc0ed982d430925faf6"
FROZEN_PROPOSAL_SHA256 = "1dbc99be96409e7cef4e6b433412286f5db03aed0c2c75b8da38890d0a4dfe98"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _curvature(metric: sp.Matrix, coordinates: tuple[sp.Symbol, ...]) -> tuple[sp.Matrix, sp.Expr]:
    dimension = len(coordinates)
    inverse = metric.inv()
    christoffel = [
        [
            [
                sp.simplify(
                    sum(
                        inverse[a, d]
                        * (
                            sp.diff(metric[d, c], coordinates[b])
                            + sp.diff(metric[d, b], coordinates[c])
                            - sp.diff(metric[b, c], coordinates[d])
                        )
                        / 2
                        for d in range(dimension)
                    )
                )
                for c in range(dimension)
            ]
            for b in range(dimension)
        ]
        for a in range(dimension)
    ]
    ricci = sp.zeros(dimension)
    for a in range(dimension):
        for b in range(dimension):
            ricci[a, b] = sp.simplify(
                sum(
                    sp.diff(christoffel[c][a][b], coordinates[c])
                    - sp.diff(christoffel[c][a][c], coordinates[b])
                    + sum(
                        christoffel[c][c][d] * christoffel[d][a][b]
                        - christoffel[c][b][d] * christoffel[d][a][c]
                        for d in range(dimension)
                    )
                    for c in range(dimension)
                )
            )
    scalar = sp.simplify(
        sum(inverse[a, b] * ricci[a, b] for a in range(dimension) for b in range(dimension))
    )
    return (ricci - metric * scalar / 2).applyfunc(sp.simplify), scalar


def _source_witness() -> tuple[sp.Expr, sp.Matrix, sp.Expr]:
    t, x, y, z = sp.symbols("t x y z", real=True)
    coordinates = (t, x, y, z)
    transverse = 1 + sp.exp(-x**2) / 5
    metric = sp.diag(-1, 1, transverse, transverse)
    einstein, _ = _curvature(metric, coordinates)
    index = 1 + sp.Rational(3, 10) * sp.exp(-x**2)
    scalar = sp.log(index)
    stress = minimally_coupled_scalar_stress(
        metric,
        [0, sp.diff(scalar, x), 0, 0],
        0,
    ).covariant
    coupling = sp.simplify((einstein[0, 0] / stress[0, 0]).subs(x, 1))
    residual = (einstein - coupling * stress).applyfunc(
        lambda entry: sp.simplify(entry.subs(x, 1))
    )
    sqrt_minus_g = sp.sqrt(-metric.det())
    scalar_residual = sp.simplify(
        sp.diff(sqrt_minus_g * sp.diff(scalar, x), x) / sqrt_minus_g
    ).subs(x, 1)
    return coupling, residual, sp.simplify(scalar_residual)


def main(source_file: str, dossier_file: str) -> int:
    source_path = Path(source_file)
    dossier_path = Path(dossier_file)
    frozen_path = Path(__file__).parent / "evidence" / "frozen-proposal.yaml"
    source_text = source_path.read_text(encoding="utf-8")
    dossier_text = dossier_path.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(source_path))
    checks = CheckLedger("P143/C-STG-001")

    checks.check("pinned G3 source hash", _sha256(source_path) == SOURCE_SHA256)
    checks.check("pinned G3 dossier hash", _sha256(dossier_path) == DOSSIER_SHA256)
    checks.check("frozen proposal hash", _sha256(frozen_path) == FROZEN_PROPOSAL_SHA256)

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("eleven source predicates", len(source_checks) == 11)
    checks.check("one source assertion", len(source_assertions) == 1)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(source_path)
    )
    checks.check(
        "G3 has no NumPy integration compatibility event",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    kappa_stores = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == "kappa" and isinstance(node.ctx, ast.Store)
    ]
    kappa_loads = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.Name) and node.id == "kappa" and isinstance(node.ctx, ast.Load)
    ]
    checks.check(
        "declared positive kappa is never used by executable source",
        len(kappa_stores) == 1 and len(kappa_loads) == 0,
    )
    checks.check(
        "source chooses metric and scalar profiles independently",
        "C_conc = 1 + sp.Rational(1, 5) * sp.exp(-x**2)" in source_text
        and "n_bump = 1 + sp.Rational(3, 10) * sp.exp(-x**2)" in source_text
        and "kappa_eff_free_val = float(G_tt_free_val / T_tt_free_val)" in source_text,
    )
    checks.check(
        "source and dossier admit the coupled problem remains unsolved",
        "full coupled Einstein+scalar PDE" in source_text
        and "does NOT pin A(n),B(n),C(n)" in source_text
        and "G3 DOES NOT CLOSE THE FULL 3+1 MATCHING PROBLEM" in dossier_text,
    )

    coupling, residual, scalar_residual = _source_witness()
    e = sp.E
    expected_coupling = sp.simplify(
        (3 + 10 * e) ** 2 * (-10 * e - 1)
        / (18 * (1 + 10 * e + 25 * e**2))
    )
    checks.check(
        "source one-point fitted coupling has forbidden negative sign",
        sp.simplify(coupling - expected_coupling) == 0 and coupling.is_negative is True,
    )
    checks.check(
        "source one-point fit fails remaining Einstein components",
        residual[0, 0] == 0
        and residual[1, 1] == 2 / (1 + 5 * e)
        and residual[2, 2] == -1 / (5 * e)
        and residual[3, 3] == -1 / (5 * e),
    )
    expected_scalar_residual = sp.simplify(
        6 * (3 + 15 * e + 50 * e**2) / ((1 + 5 * e) * (3 + 10 * e) ** 2)
    )
    checks.check(
        "source massless scalar witness is off shell",
        sp.simplify(scalar_residual - expected_scalar_residual) == 0
        and scalar_residual.is_positive is True,
    )

    epsilon = sp.symbols("epsilon", positive=True)
    optical_ratio_at_one = -sp.E / epsilon + sp.Rational(1, 2)
    checks.check(
        "optical effective ratio diverges rather than tending to zero",
        sp.limit(optical_ratio_at_one, epsilon, 0, dir="+") == -sp.oo
        and "kappa_eff = G_tt/T_tt ~ 1/eps DIVERGES" in source_text
        and "gives kappa_eff = 0" in source_text,
    )

    x = sp.symbols("x", real=True)
    index = sp.exp(x)
    delta = sp.simplify(
        (-index * sp.diff(index, x, 2)
         - sp.log(index) * sp.diff(index, x) ** 2 / 2
         + 2 * sp.diff(index, x) ** 2)
        / index**2
    )
    checks.check(
        "zero optical Delta does not imply vacuum",
        delta.subs(x, 2) == 0 and sp.diff(index, x).subs(x, 2) != 0,
    )

    velocity, potential = sp.symbols("velocity potential", real=True)
    scale = sp.symbols("scale", positive=True)
    stress = minimally_coupled_scalar_stress(
        sp.diag(-1, scale**2, scale**2, scale**2),
        [velocity, 0, 0, 0],
        potential,
    )
    checks.check(
        "canonical action fixes density pressure and trace",
        stress.covariant[0, 0] == velocity**2 / 2 + potential
        and stress.covariant[1, 1] == scale**2 * (velocity**2 / 2 - potential)
        and stress.trace == velocity**2 - 4 * potential,
    )

    kappa, time, time_zero, scale_zero = sp.symbols(
        "kappa time time_zero scale_zero", positive=True
    )
    scalar_zero = sp.symbols("scalar_zero", real=True)
    solution = massless_scalar_flat_flrw(
        kappa, time, time_zero, scale_zero, scalar_zero
    )
    checks.check(
        "exact massless flat FLRW solution closes all field equations",
        solution.energy_density == 1 / (3 * kappa * time**2)
        and solution.friedmann_residual == 0
        and solution.spatial_einstein_residual == 0
        and solution.scalar_equation_residual == 0
        and solution.continuity_residual == 0,
    )
    checks.check(
        "exact solution has explicit curvature domain and limits",
        solution.ricci_scalar == -sp.Rational(2, 3) / time**2
        and solution.kretschmann_scalar == sp.Rational(20, 27) / time**4
        and sp.limit(solution.kretschmann_scalar, time, 0, dir="+") == sp.oo
        and sp.limit(solution.kretschmann_scalar, time, sp.oo) == 0,
    )

    scalar_velocity = sp.sqrt(sp.Rational(2, 3) / kappa) / time
    density = scalar_velocity**2 / 2
    checks.mutation_sensitive(
        "one-third expansion exponent is load bearing",
        lambda exponent: sp.simplify(3 * (exponent / time) ** 2 - kappa * density) == 0,
        sp.Rational(1, 3),
        [sp.Rational(1, 2), sp.Rational(2, 3), sp.Integer(0)],
    )
    checks.mutation_sensitive(
        "scalar normalization is load bearing",
        lambda coefficient: sp.simplify(
            3 * solution.hubble_rate**2
            - kappa * (coefficient / time) ** 2 / 2
        ) == 0,
        sp.sqrt(sp.Rational(2, 3) / kappa),
        [1 / sp.sqrt(kappa), 2 / sp.sqrt(kappa), sp.Integer(0)],
    )
    ghost = minimally_coupled_scalar_stress(
        sp.diag(-1, scale**2, scale**2, scale**2),
        [scalar_velocity, 0, 0, 0],
        0,
        kinetic_coefficient=-1,
    )
    checks.check(
        "wrong kinetic sign breaks positive-energy Einstein closure",
        ghost.covariant[0, 0] == -density
        and sp.simplify(3 * solution.hubble_rate**2 - kappa * ghost.covariant[0, 0]) != 0,
    )
    checks.check(
        "cosmological solution has no localized breather interpretation",
        solution.energy_density.is_positive is True
        and sp.integrate(solution.energy_density, (x, -sp.oo, sp.oo)) == sp.oo,
    )
    return checks.finish()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", required=True)
    parser.add_argument("--dossier-file", required=True)
    return parser


if __name__ == "__main__":
    arguments = _parser().parse_args()
    raise SystemExit(main(arguments.source_file, arguments.dossier_file))
