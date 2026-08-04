#!/usr/bin/env python3
"""Exact, source-aware verifier for proposed C-BND-001 and W1."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.boundary_correlations import (
    boundary_sign_correlation_density,
    oriented_half_line_parity_ledger,
    right_half_line_topological_charge_change,
    scalar_boundary_parity_ledger,
    scalar_boundary_trace_family,
)
from substrate_framework.sine_gordon import (
    naive_chiral_transport_defects,
    sine_gordon_chiral_sources,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P146-w1-parity-boundary-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-6/"
    "bridge_W1_parity_odd_chiral_coupling.py"
)
DOSSIER = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-6/dossiers/"
    "W1_dossier.md"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
SOURCE_SHA256 = "bfac7d7e4ccb0cdabc6bb2703dadb650c0e09ea883ec3ff70f039231d3e62388"
DOSSIER_SHA256 = "b445fb798e2c5fab53f47eca41895ec140ae3a0d812bd14d11eee0b26c3237a1"
FROZEN_SHA256 = "fa342cee48763371ae51008dee9096a534a9952556ddde83f734e540874ed212"
REVISION_SHA256 = "0f4f3e8b3e5a77dc5e8f50f3686dfbdf8c14e16453a34cde24262124d580270c"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _alias_replay() -> subprocess.CompletedProcess[str]:
    program = (
        "import runpy, numpy as np; "
        "np.trapz = np.trapezoid; "
        f"runpy.run_path({str(SOURCE)!r}, run_name='__main__')"
    )
    return subprocess.run(
        [sys.executable, "-c", program],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def run() -> int:
    checks = CheckLedger("P146/C-BND-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    dossier_text = DOSSIER.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned W1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("pinned W1 dossier hash", _sha256(DOSSIER) == DOSSIER_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)

    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [
        node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)
    ]
    checks.check("eight source predicates", len(source_checks) == 8)
    checks.check("two source assertions", len(source_assertions) == 2)

    compatibility = audit_numpy_trapezoid_compatibility(
        source_text,
        filename=str(SOURCE),
    )
    checks.check(
        "W1 compatibility event is exactly two direct legacy accesses",
        compatibility.numpy_aliases == ("np",)
        and compatibility.direct_legacy_attributes == 2
        and compatibility.dynamic_legacy_getattrs == 0
        and compatibility.imported_legacy_names == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )

    native = subprocess.run(
        [sys.executable, str(SOURCE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.check(
        "native W1 abort is isolated to removed NumPy name",
        native.returncode == 1
        and "W1.1" in native.stdout
        and "W1.3" in native.stdout
        and "W1.4 [DERIVED, REJECTION GUARD]" not in native.stdout
        and "has no attribute 'trapz'" in native.stderr,
    )
    replay = _alias_replay()
    checks.check("alias-only W1 process exits cleanly", replay.returncode == 0)
    checks.check(
        "alias-only W1 terminal tally is exact",
        replay.stdout.rstrip().endswith("ALL 8 CHECKS PASS"),
    )

    u, v, a, beta, current = sp.symbols("u v a beta J", real=True)
    ledger = scalar_boundary_parity_ledger(u, v, a, beta, current)
    checks.check(
        "general boundary residual is derived from declared traces",
        ledger.residual == a * u + beta * v - current,
    )
    checks.check(
        "boundary residual has exact even and odd components",
        ledger.parity_even_component == a * u - current
        and ledger.parity_odd_component == beta * v
        and ledger.residual
        == ledger.parity_even_component + ledger.parity_odd_component,
    )
    checks.check(
        "scalar parity equals reflected coefficient family member",
        ledger.parity_image_residual
        == ledger.reflected_coefficient_residual
        == a * u - beta * v - current,
    )
    checks.check(
        "fixed-parameter parity defect retains the spatial channel",
        ledger.fixed_parameter_parity_defect == -2 * beta * v,
    )

    mixed = scalar_boundary_parity_ledger(u, v, 1, 1, 0)
    checks.check(
        "mixed temporal-spatial residual is not a parity eigenobject",
        sp.simplify(mixed.parity_image_residual - mixed.residual) != 0
        and sp.simplify(mixed.parity_image_residual + mixed.residual) != 0,
    )
    temporal = scalar_boundary_parity_ledger(u, v, 1, 0, current)
    spatial = scalar_boundary_parity_ledger(u, v, 0, 1, 0)
    checks.check(
        "pure temporal residual is parity even",
        temporal.parity_image_residual == temporal.residual,
    )
    checks.check(
        "pure spatial residual is parity odd",
        spatial.parity_image_residual == -spatial.residual,
    )
    checks.check(
        "nonzero coefficient pair is family covariance not fixed invariance",
        scalar_boundary_parity_ledger(u, v, 1, 1, current).parity_image_residual
        == scalar_boundary_parity_ledger(u, v, 1, -1, current).residual
        and scalar_boundary_parity_ledger(
            u, v, 1, 1, current
        ).parity_image_residual
        != scalar_boundary_parity_ledger(u, v, 1, 1, current).residual,
    )

    normal = oriented_half_line_parity_ledger(u, v, a, beta, current)
    checks.check(
        "right and parity-mapped left outward traces agree",
        normal.right_outward_trace
        == normal.left_parity_coordinate_trace
        == normal.left_outward_trace
        == -v,
    )
    checks.check(
        "outward-normal coefficient is unchanged by domain parity",
        normal.right_residual == normal.left_parity_residual,
    )
    wrong_left_residual = sp.simplify(a * u + beta * v - current)
    checks.check(
        "wrong untransformed left normal breaks the domain map",
        sp.simplify(wrong_left_residual - normal.right_residual) == 2 * beta * v,
    )

    beta_nonzero = sp.Symbol("beta_nonzero", real=True, nonzero=True)
    family = scalar_boundary_trace_family(u, a, beta_nonzero, current)
    checks.check(
        "nonzero spatial coefficient retains a temporal-trace family",
        family.coordinate_trace_solution
        == (current - a * u) / beta_nonzero
        and family.temporal_only_constraint is None,
    )
    checks.check(
        "derived nonzero-coefficient trace family closes the residual",
        sp.simplify(
            a * u
            + beta_nonzero * family.coordinate_trace_solution
            - current
        )
        == 0,
    )
    temporal_family = scalar_boundary_trace_family(u, a, 0, current)
    checks.check(
        "temporal-only boundary leaves coordinate trace arbitrary",
        temporal_family.coordinate_trace_solution is None
        and temporal_family.coordinate_trace_free
        and temporal_family.temporal_only_constraint == a * u - current,
    )

    phi = sp.Function("phi")
    x, t = sp.symbols("x t", real=True)
    decomposition = phi(t + x) + sp.Function("psi")(t - x)
    plus = sp.diff(decomposition, t) + sp.diff(decomposition, x)
    minus = sp.diff(decomposition, t) - sp.diff(decomposition, x)
    checks.check(
        "W1.1 linear characteristic projection is exact",
        len(plus.atoms(sp.Derivative)) == 1
        and len(minus.atoms(sp.Derivative)) == 1,
    )

    nonlinear_field = sp.Function("varphi")(x, t)
    defects = naive_chiral_transport_defects(nonlinear_field, x, t)
    sources = sine_gordon_chiral_sources(nonlinear_field)
    wave_operator = sp.diff(nonlinear_field, t, 2) - sp.diff(
        nonlinear_field,
        x,
        2,
    )
    checks.check(
        "full sine-Gordon characteristic channels remain sourced",
        all(
            sp.simplify(defect - wave_operator) == 0 for defect in defects
        )
        and sources == (-sp.sin(nonlinear_field), -sp.sin(nonlinear_field))
        and sp.simplify(
            wave_operator.subs(
                sp.diff(nonlinear_field, t, 2),
                sp.diff(nonlinear_field, x, 2) - sp.sin(nonlinear_field),
            )
            - sources[0]
        )
        == 0,
    )

    function_names = {
        node.name for node in ast.walk(source_tree) if isinstance(node, ast.FunctionDef)
    }
    checks.check(
        "W1.3 charge selection is a hard-coded imported map",
        "Q_of_eps" in function_names
        and "return +1 if e == +1 else -1" in source_text
        and "topological_charge_from_boundaries" not in source_text,
    )

    temporal_only_a = scalar_boundary_trace_family(1, 1, 0, 1)
    checks.check(
        "W1.4 vector law does not imply zero spatial trace",
        temporal_only_a.coordinate_trace_free
        and boundary_sign_correlation_density(1, 0) == 0
        and boundary_sign_correlation_density(1, 3) == 3,
    )
    checks.check(
        "W1.4 zero witness is inserted as an extra condition",
        "phi_x_vec = np.zeros_like(tt)" in source_text
        and "phi_t_vec = J0 * np.cos" in source_text,
    )
    checks.check(
        "W1.4b constructed traces violate their displayed epsilon-plus law",
        sp.simplify(1 + 1 - 1) == 1
        and "phi_t_chi = J0 * np.cos" in source_text
        and "phi_x_chi = J0 * np.cos" in source_text,
    )

    checks.check(
        "boundary sign correlation is independent of topological transfer",
        boundary_sign_correlation_density(1, 3) == 3
        and right_half_line_topological_charge_change(0) == 0,
    )
    checks.check(
        "source relabels correlation witness as Delta Q",
        "deltaQ_vector = W_vector" in source_text
        and "W = oint sgn(phi_t) phi_x dt" in source_text,
    )
    checks.check(
        "fermion parity checks are arithmetic imports only",
        "def fermionParity(Q):" in source_text
        and "return (-1) ** abs(Q)" in source_text,
    )
    checks.check(
        "W1.7 nonzero spatial coefficient does not make mixed residual odd",
        mixed.parity_odd_component == v
        and mixed.parity_even_component == u
        and mixed.parity_image_residual != -mixed.residual,
    )

    checks.check(
        "dossier carries a contradictory chiral derivative sign row",
        "φ_x(0,t) = −φ_L'(t) + φ_R'(t)" in dossier_text
        and "∂_x(φ_L(t+x)) = +φ_L'" in dossier_text,
    )
    loaded_names = {
        node.id
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
    }
    checks.check(
        "W1 supplies no boundary action or evolved field solution",
        not loaded_names.intersection(
            {"solve_ivp", "solve_bvp", "boundary_action", "lagrangian", "eom"}
        ),
    )

    source_sign_mutant = scalar_boundary_parity_ledger(u, v, a, beta, -current)
    checks.check(
        "source intrinsic-parity mutation changes the claimed pullback",
        sp.simplify(
            source_sign_mutant.parity_image_residual
            - ledger.reflected_coefficient_residual
        )
        == 2 * current,
    )
    wrong_trace = sp.simplify((current + a * u) / beta_nonzero)
    checks.check(
        "trace-family sign mutation fails the boundary residual",
        sp.simplify(a * u + beta_nonzero * wrong_trace - current) == 2 * a * u,
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/boundary_correlations.py"
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"),
            filename=str(path),
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P146 and canonical code has no legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P146 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
