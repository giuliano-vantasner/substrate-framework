"""Primary exact verifier for P082 / WM2 common-induction audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.charge_traces import (
    WeightedChargeState,
    abelian_normalization_ledger,
    common_trace_normalized_coupling_angle,
    finite_charge_trace_ledger,
)
from substrate_framework.governance import load_yaml
from substrate_framework.su3 import invariants
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-23/"
    "bridge_WM2_common_induction_normalization.py"
)
SOURCE_SHA256 = "3c656894fc782dd40dcb495a91de5bbf5a46ec378bb3593eb30d7d4b387f34a3"
CONTRACT_SHA256 = "3b56490c92229e727217a932f1852be2129c4e9d36a78f0c3c805bfe5b3551e0"
FREEZE_SHA256 = "8a0d6332e2f1f581959b827ff6f9d4f09ad77d77f1a8f3923d1b5fc5fe3c065e"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P082-wm2-common-induction-audit/proposal.yaml"),
        Path("proposals/P082-wm2-common-induction-audit/proposal.yaml"),
    )
    return next(path for path in candidates if path.exists())


def _declared_generation() -> tuple[WeightedChargeState, ...]:
    return (
        WeightedChargeState("Q_L_up", 3, sp.Rational(1, 2), sp.Rational(1, 6)),
        WeightedChargeState("Q_L_down", 3, -sp.Rational(1, 2), sp.Rational(1, 6)),
        WeightedChargeState("u_R_conj", 3, 0, -sp.Rational(2, 3)),
        WeightedChargeState("d_R_conj", 3, 0, sp.Rational(1, 3)),
        WeightedChargeState("L_neutrino", 1, sp.Rational(1, 2), -sp.Rational(1, 2)),
        WeightedChargeState("L_electron", 1, -sp.Rational(1, 2), -sp.Rational(1, 2)),
        WeightedChargeState("e_R_conj", 1, 0, 1),
    )


def _inverse_coupling_ratio(
    trace_2: sp.Expr,
    trace_y: sp.Expr,
    coefficient_2: sp.Expr,
    coefficient_y: sp.Expr,
    baseline_2: sp.Expr = sp.Integer(0),
    baseline_y: sp.Expr = sp.Integer(0),
) -> sp.Expr:
    inverse_2 = baseline_2 + coefficient_2 * trace_2
    inverse_y = baseline_y + coefficient_y * trace_y
    return sp.factor(inverse_2 / inverse_y)


def main() -> int:
    checks = CheckLedger("P082")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(
            _contract_path()
            .read_bytes()
            .replace(b"status: accepted\n", b"status: draft\n")
        ).hexdigest()
        == CONTRACT_SHA256,
    )
    freeze_path = _contract_path().parent / "evidence/frozen-proposal.yaml"
    checks.check(
        "pre-source contract commitment is immutable",
        hashlib.sha256(freeze_path.read_bytes()).hexdigest() == FREEZE_SHA256,
    )
    checks.check(
        "source has ten literal checks and a dynamic terminal tally",
        source_text.count("check(") == 11
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "exact routes use no NumPy integration alias",
        all(alias not in source_text for alias in ("np." + "trapz", "np." + "trapezoid")),
    )

    states = _declared_generation()
    table = finite_charge_trace_ledger(states)
    trace_2 = table.trace_t3_squared
    trace_y = table.trace_abelian_squared
    trace_3 = 4 * invariants().dynkin_index
    checks.check(
        "declared finite traces reproduce conditionally",
        trace_2 == 2
        and trace_y == sp.Rational(10, 3)
        and table.trace_cross == 0
        and trace_3 == 2,
    )
    checks.check(
        "strong trace is a supplied triplet count times the accepted convention",
        invariants().dynkin_index == sp.Rational(1, 2)
        and trace_3 == 4 * sp.Rational(1, 2),
    )

    common = sp.Symbol("C", positive=True) / sp.pi
    conditional = common_trace_normalized_coupling_angle(
        trace_2,
        trace_y,
        common,
    )
    checks.check(
        "zero-baseline common law reproduces the source ratio conditionally",
        conditional.coupling_squared_ratio == sp.Rational(3, 5)
        and conditional.coupling_angle == sp.Rational(3, 8)
        and conditional.su2_inverse_trace_coefficient == common
        and conditional.abelian_inverse_trace_coefficient == common,
    )

    rho, physical_g_y = sp.symbols("rho g_Y", positive=True)
    normalization = abelian_normalization_ledger(states, rho, physical_g_y)
    covariant_common = common_trace_normalized_coupling_angle(
        trace_2,
        rho**2 * trace_y,
        common,
    )
    checks.check(
        "common inverse-trace law survives every positive Abelian coordinate rescaling",
        covariant_common.su2_inverse_trace_coefficient == common
        and covariant_common.abelian_inverse_trace_coefficient == common
        and covariant_common.coupling_squared_ratio
        == sp.Rational(3, 5) / rho**2,
    )
    checks.check(
        "inverse coupling rescaling preserves the coupled charge and trace norm",
        normalization.rescaled_abelian_coupling == physical_g_y / rho
        and normalization.charge_product_residuals == (0,) * len(states)
        and normalization.coupled_trace_norm_residual == 0,
    )
    target = sp.Symbol("r", positive=True)
    target_rho = sp.sqrt(sp.Rational(3, 5) / target)
    checks.check(
        "common law permits every positive squared-coupling coordinate",
        sp.simplify(
            covariant_common.coupling_squared_ratio.subs(rho, target_rho)
            - target
        )
        == 0,
    )

    canonical_rho = sp.sqrt(sp.Rational(3, 5))
    canonical = common_trace_normalized_coupling_angle(
        trace_2,
        canonical_rho**2 * trace_y,
        common,
    )
    checks.check(
        "canonical generator rescaling makes trace and coupling coordinates equal by construction",
        sp.simplify(canonical_rho**2 * trace_y) == trace_2 == trace_3 == 2
        and canonical.coupling_squared_ratio == 1
        and canonical.coupling_angle == sp.Rational(1, 2),
    )
    checks.check(
        "covariant electric coefficient keeps the original physical charge quotient",
        normalization.covariant.trace_ratio == table.trace_ratio == sp.Rational(3, 8)
        and normalization.rescaled_electric_coefficient == 1 / rho,
    )

    c2, cy = sp.symbols("C2 CY", positive=True)
    independent_ratio = _inverse_coupling_ratio(trace_2, trace_y, c2, cy)
    checks.check(
        "sector-specific coefficients retain their free ratio",
        independent_ratio == 3 * c2 / (5 * cy)
        and sp.simplify(independent_ratio.subs(cy, c2) - sp.Rational(3, 5)) == 0,
    )
    k2, ky = sp.symbols("K2 KY", nonnegative=True)
    affine_ratio = _inverse_coupling_ratio(trace_2, trace_y, common, common, k2, ky)
    checks.check(
        "additive tree or counterterm baselines prevent common-factor cancellation",
        {k2, ky} <= affine_ratio.free_symbols
        and sp.simplify(affine_ratio.subs({k2: 0, ky: 0}) - sp.Rational(3, 5)) == 0
        and sp.simplify(affine_ratio.subs({k2: 1, ky: 0}) - sp.Rational(3, 5)) != 0,
    )
    checks.mutation_sensitive(
        "common zero-baseline premise is load bearing",
        lambda values: sp.simplify(
            _inverse_coupling_ratio(trace_2, trace_y, *values)
            - sp.Rational(3, 5)
        )
        == 0,
        (common, common, sp.Integer(0), sp.Integer(0)),
        [
            (2 * common, common, sp.Integer(0), sp.Integer(0)),
            (common, common, sp.Integer(1), sp.Integer(0)),
            (common, common, sp.Integer(0), sp.Integer(1)),
        ],
    )

    queue = load_yaml("migration/source-claims.yaml")
    pending_dependencies = {"EM5", "YM1", "QCD1", "S2", "S3", "SM3", "SM4", "W2"}
    records = {
        unit["source_unit"]: unit
        for unit in queue["units"]
        if unit["source_unit"] in pending_dependencies
    }
    checks.check(
        "every advertised induction or representation dependency lacks accepted closure",
        set(records) == pending_dependencies
        and all(record["disposition"] == "pending_adjudication" for record in records.values())
        and all(record["accepted_claims"] == [] for record in records.values()),
    )

    imports = [
        node for node in ast.walk(source_tree) if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    assigned_names = {
        target_node.id
        for node in ast.walk(source_tree)
        if isinstance(node, (ast.Assign, ast.AnnAssign))
        for target_node in (node.targets if isinstance(node, ast.Assign) else [node.target])
        if isinstance(target_node, ast.Name)
    }
    checks.check(
        "source executes only standalone SymPy algebra rather than cited induction mechanisms",
        len(imports) == 1
        and isinstance(imports[0], ast.Import)
        and imports[0].names[0].name == "sympy"
        and assigned_names.isdisjoint({"Lambda", "regulator", "counterterm", "gauge_action"}),
    )
    checks.check(
        "source explicitly declares rather than derives its decisive common coefficient",
        "DECLARED      -- the SINGLE-MEDIUM premise" in source_text
        and 'C = sp.Symbol("C", positive=True)' in source_text
        and "The new physics is the SINGLE-MEDIUM premise" in source_text,
    )
    checks.check(
        "source contains no executable loop determinant profile or action derivation",
        all(
            word not in assigned_names
            for word in ("determinant", "profile", "loop_integral", "effective_action", "tree_term")
        ),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
