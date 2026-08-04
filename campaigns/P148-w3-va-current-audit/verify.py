#!/usr/bin/env python3
"""Verify the accepted current classification and audit every W3 predicate."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.boundary_correlations import (
    right_half_line_topological_charge_change,
    sinusoidal_boundary_sign_correlation,
)
from substrate_framework.sine_gordon import (
    naive_chiral_currents,
    naive_chiral_transport_defects,
    sine_gordon_chiral_sources,
    topological_current,
    topological_current_divergence,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.su2_doublets import (
    su2_common_charge_ledger,
    su2_fundamental_ledger,
)
from substrate_framework.u1_charge import u1_current_components
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / "merged-framework/bridges/phase-6/bridge_W3_VA_charged_current.py"
DOSSIER = SOURCE_ROOT / "merged-framework/bridges/phase-6/dossiers/W3_dossier.md"
CHARGE_LEAN = SOURCE_ROOT / "sg-breather-ionization/dynamics_lean/ChargeDiscrimination.lean"
U1_LEAN = SOURCE_ROOT / "sg-breather-ionization/dynamics_lean/Phase3EM_U1Current.lean"
SOLUTION = SOURCE_ROOT / "sg-breather-ionization/solution.md"
FROZEN = ROOT / "campaigns/P148-w3-va-current-audit/evidence/frozen-proposal.yaml"
REVISION = ROOT / "campaigns/P148-w3-va-current-audit/evidence/proposal-revision-0001.yaml"
REPRODUCTION = ROOT / "campaigns/P148-w3-va-current-audit/evidence/source-reproduction.yaml"

SOURCE_SHA256 = "b49a0bd1075b16b5906719b6ed51454ed04adab5168be7ec98178599313b3f17"
DOSSIER_SHA256 = "c9b327bba0fa227083017173cae475728f061e7b82da0f1810dbfb9f74e00b5b"
CHARGE_LEAN_SHA256 = "c692eb12d9aa81f7547f855fe24ed03f7ba2403ac3fc4710c33c42ff80364056"
U1_LEAN_SHA256 = "0e5483768c84943278955aca66df56b0a945d6d622d5d364fc2aeb2f711270e2"
SOLUTION_SHA256 = "a5a0ced9a097f07daea67e37b9516755307536e4850dfc975da72ee8eb876f86"
FROZEN_SHA256 = "cb2a40d9879b92ab1f5d9634fcaaefc25e26b8dc3052649f97c5857d564fbd7f"
REVISION_SHA256 = "ebf9bf106101aa754eacce7ae5a3b6ae90af098cf01cac0d85bed4e4eab96e7b"
REPRODUCTION_SHA256 = "226977aec99ae722a8f7adbd6e740d159af2a5496e049e0b4ba9f8f045989ff3"


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


def _all_zero(matrices: tuple[sp.ImmutableMatrix, ...]) -> bool:
    return all(matrix == sp.zeros(*matrix.shape) for matrix in matrices)


def run() -> int:
    checks = CheckLedger("P148/W3")
    source_text = SOURCE.read_text(encoding="utf-8")
    dossier_text = DOSSIER.read_text(encoding="utf-8")
    charge_lean_text = CHARGE_LEAN.read_text(encoding="utf-8")
    u1_lean_text = U1_LEAN.read_text(encoding="utf-8")
    solution_text = SOLUTION.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    for name, path, digest in (
        ("W3 source", SOURCE, SOURCE_SHA256),
        ("W3 dossier", DOSSIER, DOSSIER_SHA256),
        ("ChargeDiscrimination Lean", CHARGE_LEAN, CHARGE_LEAN_SHA256),
        ("Phase3 U1 Lean", U1_LEAN, U1_LEAN_SHA256),
        ("solution", SOLUTION, SOLUTION_SHA256),
        ("frozen proposal", FROZEN, FROZEN_SHA256),
        ("proposal revision", REVISION, REVISION_SHA256),
        ("source reproduction", REPRODUCTION, REPRODUCTION_SHA256),
    ):
        checks.check(f"pinned {name} hash", _sha256(path) == digest)

    source_checks = sum(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
        for node in ast.walk(tree)
    )
    source_assertions = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    checks.check("seven source predicates", source_checks == 7)
    checks.check("one source assertion", source_assertions == 1)

    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "W3 compatibility shape is exactly two direct legacy accesses",
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
        "native W3 abort is isolated to removed NumPy name",
        native.returncode == 1
        and "W3.1" in native.stdout
        and "W3.3" in native.stdout
        and "W3.4" in native.stdout
        and "has no attribute 'trapz'" in native.stderr,
    )
    replay = _alias_replay()
    checks.check("alias-only W3 process exits cleanly", replay.returncode == 0)
    checks.check(
        "alias-only W3 terminal tally is exact",
        "ALL 7 CHECKS PASS" in replay.stdout and replay.stderr == "",
    )

    ell, right = sp.symbols("ell right", real=True)
    temporal = ell + right
    coordinate = ell - right
    checks.check(
        "direct chain rule fixes both characteristic traces",
        sp.simplify(temporal + coordinate - 2 * ell) == 0
        and sp.simplify(temporal - coordinate - 2 * right) == 0,
    )
    checks.check(
        "W3 assigns the negative spatial derivative",
        "phi_x = phiR - phiL" in source_text
        and sp.simplify((right - ell) + coordinate) == 0,
    )
    checks.check(
        "W3 check three separates its algebra from its desired channel label",
        "plus_is_2phiR" in source_text
        and "minus_is_2phiL" in source_text
        and "eps_plus_is_left = sp.simplify(J0_left - 2 * phiL) == 0" in source_text,
    )

    x, t = sp.symbols("x t", real=True)
    field = sp.Function("phi")(x, t)
    current_plus, current_minus = naive_chiral_currents(field, x, t)
    defect_plus, defect_minus = naive_chiral_transport_defects(field, x, t)
    wave = sp.diff(field, t, 2) - sp.diff(field, x, 2)
    checks.check(
        "accepted characteristics are derivative identities",
        current_plus == sp.diff(field, t) + sp.diff(field, x)
        and current_minus == sp.diff(field, t) - sp.diff(field, x)
        and sp.simplify(defect_plus - wave) == 0
        and sp.simplify(defect_minus - wave) == 0,
    )
    on_shell = sp.diff(field, x, 2) - sp.sin(field)
    checks.check(
        "full sine-Gordon sources both characteristic channels",
        tuple(
            sp.simplify(defect.subs(sp.diff(field, t, 2), on_shell))
            for defect in (defect_plus, defect_minus)
        )
        == sine_gordon_chiral_sources(field)
        == (-sp.sin(field), -sp.sin(field)),
    )

    derivative_vector = sp.Matrix([sp.diff(field, t), -sp.diff(field, x)])
    dual_vector = sp.Matrix([sp.diff(field, x), -sp.diff(field, t)])
    derivative_divergence = sp.simplify(
        sp.diff(derivative_vector[0], t) + sp.diff(derivative_vector[1], x)
    )
    dual_divergence = sp.simplify(
        sp.diff(dual_vector[0], t) + sp.diff(dual_vector[1], x)
    )
    checks.check(
        "gradient derivative divergence is the wave operator",
        sp.simplify(derivative_divergence - wave) == 0,
    )
    checks.check(
        "epsilon-dual derivative is off-shell conserved",
        dual_divergence == 0
        and topological_current_divergence(field, x, t) == 0
        and sp.simplify(
            dual_vector - 2 * sp.pi * sp.Matrix(topological_current(field, x, t))
        )
        == sp.zeros(2, 1),
    )
    checks.check(
        "W3 never evaluates the divergences of its named currents",
        "sp.diff(V0" not in source_text
        and "sp.diff(A0" not in source_text
        and "u1_div = sp.I * (b_c - a_c)" in source_text,
    )
    checks.check(
        "W3 axial-shift equality is assigned before comparison",
        "dAxial = sp.Integer(1)" in source_text
        and "dQ_plus = sp.Integer(1)" in source_text,
    )
    checks.check(
        "finite potential displacement is not a current-divergence calculation",
        "axial_shift = sp.simplify(V_cos_axial - V_cos)" in source_text
        and "axial_breaks =" in source_text
        and dual_divergence == 0,
    )

    u, v = sp.symbols("u v", real=True)
    d = sp.Matrix([u, -v])
    a = sp.Matrix([v, -u])
    parity_matrix = sp.diag(1, -1)
    d_parity_field = sp.Matrix([u, v])
    a_parity_field = sp.Matrix([-v, -u])
    checks.check(
        "scalar parity gives vector and axial transformation laws",
        d_parity_field == parity_matrix * d
        and a_parity_field == -parity_matrix * a,
    )
    checks.check(
        "parity exchanges the null derivative combinations",
        d_parity_field - a_parity_field == parity_matrix * (d + a)
        and d_parity_field + a_parity_field == parity_matrix * (d - a),
    )
    checks.check(
        "W3 supplies no parity-breaking action or selected coupling",
        "Lagrangian" not in source_text[source_text.find("import numpy"):]
        and "coupling normalised" in source_text
        and '"  to 1 (W5 magnitude obligation)' in source_text,
    )

    checks.check(
        "W3 Gaussian has the desired area by construction",
        "-(2 * np.pi) / (np.sqrt(2 * np.pi) * sigma)" in source_text
        and sp.integrate(
            -2 * sp.pi / (sp.sqrt(2 * sp.pi) * sp.Symbol("s", positive=True))
            * sp.exp(-sp.Symbol("tau", real=True) ** 2 / (2 * sp.Symbol("s", positive=True) ** 2)),
            (sp.Symbol("tau", real=True), -sp.oo, sp.oo),
        )
        == -2 * sp.pi,
    )
    checks.check(
        "half-line charge follows only after supplied boundary field change",
        right_half_line_topological_charge_change(-2 * sp.pi) == 1
        and right_half_line_topological_charge_change(0) == 0,
    )
    fundamental = su2_fundamental_ledger()
    charge = su2_common_charge_ledger(0, assigned_labels=(1, -1))
    checks.check(
        "W2 ladder step and W2 assigned label transition remain distinct",
        fundamental.raising_operator * sp.Matrix([0, 1]) == sp.Matrix([1, 0])
        and (sp.Integer(1) - sp.Integer(-1)) == 2
        and charge.eigenvalue_separation == 1
        and charge.labels_compatible is False,
    )

    real_u1 = u1_current_components(field, field, x, t)
    checks.check(
        "a genuinely real field has zero complex-Noether current",
        real_u1 == (0, 0),
    )
    checks.check(
        "W3 equates distinct complex and real-field objects by assignment",
        "J0_EM = V0 - A0_EM" in source_text
        and "em_is_phit = sp.simplify(J0_EM - phi_t) == 0" in source_text
        and "The Lagrangian, the EOM, and Noether's procedure are the physics INPUT" in u1_lean_text,
    )
    checks.check(
        "imported charge Lean proves declared integer arithmetic only",
        "def reflectedCharge_cplus : ℤ := 1" in charge_lean_text
        and "if F₀ < 0 then reflectedCharge_cplus else reflectedCharge_cminus" in charge_lean_text,
    )

    correlation_nonzero = sinusoidal_boundary_sign_correlation(1, 2, 3, 0)
    checks.check(
        "nonzero sign correlation can have zero topological transfer",
        correlation_nonzero == sp.Rational(8, 3)
        and right_half_line_topological_charge_change(0) == 0,
    )
    checks.check(
        "zero sign correlation can accompany nonzero topological transfer",
        sinusoidal_boundary_sign_correlation(1, 2, 3, sp.pi / 2) == 0
        and right_half_line_topological_charge_change(2 * sp.pi) == -1,
    )
    checks.check(
        "W3 guard computes one chosen quadrature trace rather than charge",
        "phi_x_sym = np.sin" in source_text
        and "phi_t_sym = np.cos" in source_text
        and "rect_zero = abs(rect) < 1e-2" in source_text
        and "pureV_dQ_zero = rect_zero" in source_text,
    )
    checks.check(
        "solution keeps chiral and rectification steps noncanonical",
        "Chiral boundary condition derivation | `theoretical_analysis`" in solution_text
        and "Topological rectification condition | `theoretical_analysis`" in solution_text,
    )
    checks.check(
        "dossier itself exposes mutually inconsistent current signs",
        "J^0_cc ∝ (φ_L' + φ_R') − (φ_L' − φ_R') = 2 φ_R'" in dossier_text
        and "J^0_cc = V^0 − A^0 ∝ 2 φ_L'(t)" in dossier_text,
    )

    def orientation_predicate(sign: int) -> bool:
        candidate = sp.Matrix([sign * sp.diff(field, x), -sign * sp.diff(field, t)])
        return sp.simplify(
            sp.diff(candidate[0], t) + sp.diff(candidate[1], x)
        ) == 0 and candidate == dual_vector

    checks.mutation_sensitive(
        "epsilon-dual orientation",
        orientation_predicate,
        1,
        [-1, 0],
    )

    def source_sign_predicate(sign: int) -> bool:
        candidate_v = sign * (ell - right)
        return bool(
            sp.simplify(temporal + candidate_v - 2 * ell) == 0
            and sp.simplify(temporal - candidate_v - 2 * right) == 0
        )

    checks.mutation_sensitive("chain-rule spatial sign", source_sign_predicate, 1, [-1, 0])

    mutable_paths = tuple((ROOT / "campaigns/P148-w3-va-current-audit").rglob("*.py"))
    mutable_audits = tuple(
        audit_numpy_trapezoid_compatibility(path.read_text(encoding="utf-8"), filename=str(path))
        for path in mutable_paths
    )
    checks.check(
        "mutable P148 code has no executable legacy integration access",
        all(audit.legacy_references == 0 for audit in mutable_audits),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(run())
