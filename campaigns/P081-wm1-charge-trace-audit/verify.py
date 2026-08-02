"""Primary exact verifier for P081 / provisional C-REP-001."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.charge_traces import (
    WeightedChargeState,
    abelian_normalization_ledger,
    charge_coupling_angle_ledger,
    common_trace_normalized_coupling_angle,
    finite_charge_trace_ledger,
    weighted_abelian_moment,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-23/"
    "bridge_WM1_sin2thetaw_trace_ratio.py"
)
SOURCE_SHA256 = "75dc34e168c39cd0af0a21cd4c7d039088ac74baefb6615ece98f5069f5b8953"
CONTRACT_SHA256 = "f89b80e04638400b792896305bbc65b41ce6aadea81e30a280bce5272d3f23bd"
FREEZE_SHA256 = "c6d8d6182a35d35d48f4ecf7341aecc31f3ad5335422fe45a9a9a12c0a05e6b9"


def _contract_path() -> Path:
    candidates = (
        Path("campaigns/P081-wm1-charge-trace-audit/proposal.yaml"),
        Path("proposals/P081-wm1-charge-trace-audit/proposal.yaml"),
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


def _replace_state(
    states: tuple[WeightedChargeState, ...],
    label: str,
    replacement: WeightedChargeState | None,
) -> tuple[WeightedChargeState, ...]:
    return tuple(
        candidate
        for state in states
        for candidate in (() if state.label == label and replacement is None else (
            replacement if state.label == label else state,
        ))
    )


def _exact_source_table(candidate: object) -> bool:
    ledger = finite_charge_trace_ledger(candidate)
    return bool(
        ledger.state_count == 15
        and ledger.trace_t3_squared == 2
        and ledger.trace_abelian_squared == sp.Rational(10, 3)
        and ledger.trace_cross == 0
        and ledger.trace_electric_squared == sp.Rational(16, 3)
        and ledger.trace_ratio == sp.Rational(3, 8)
    )


def main() -> int:
    checks = CheckLedger("P081")
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
        "source has nine literal checks and a dynamic terminal tally",
        source_text.count("check(") == 10
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    canonical_text = Path("src/substrate_framework/charge_traces.py").read_text(
        encoding="utf-8"
    )
    checks.check(
        "source and canonical routes use no NumPy quadrature alias",
        all(
            alias not in source_text and alias not in canonical_text
            for alias in ("np." + "trapz", "np." + "trapezoid")
        ),
    )

    states = _declared_generation()
    ledger = finite_charge_trace_ledger(states)
    checks.check(
        "declared table has fifteen weighted states",
        ledger.state_count == 15
        and tuple(state.multiplicity for state in states) == (3, 3, 3, 3, 1, 1, 1),
    )
    checks.check(
        "finite table traces are exact",
        ledger.trace_t3_squared == 2
        and ledger.trace_abelian_squared == sp.Rational(10, 3)
        and ledger.trace_cross == 0
        and ledger.trace_electric_squared == sp.Rational(16, 3),
    )
    checks.check(
        "direct electric trace equals the complete expansion",
        ledger.expanded_trace_electric_squared
        == ledger.trace_t3_squared
        + 2 * ledger.trace_cross
        + ledger.trace_abelian_squared
        and ledger.decomposition_residual == 0,
    )
    checks.check(
        "declared charge-table ratio is exactly three eighths",
        ledger.trace_ratio == sp.Rational(3, 8),
    )
    checks.check(
        "cross trace cancels separately inside both declared doublets",
        3
        * (
            sp.Rational(1, 2) * sp.Rational(1, 6)
            - sp.Rational(1, 2) * sp.Rational(1, 6)
        )
        == 0
        and sp.Rational(1, 2) * -sp.Rational(1, 2)
        + -sp.Rational(1, 2) * -sp.Rational(1, 2)
        == 0,
    )

    rho, coupling = sp.symbols("rho g_Y", positive=True)
    normalization = abelian_normalization_ledger(states, rho, coupling)
    checks.check(
        "holding the electric coefficient fixed produces a trace-ratio family",
        normalization.fixed_coefficient.trace_abelian_squared
        == sp.Rational(10, 3) * rho**2
        and normalization.fixed_coefficient.trace_electric_squared
        == 2 + sp.Rational(10, 3) * rho**2
        and normalization.fixed_coefficient.trace_ratio == 3 / (3 + 5 * rho**2),
    )
    checks.check(
        "covariantly transforming the electric coefficient preserves Q and its ratio",
        normalization.rescaled_electric_coefficient == 1 / rho
        and normalization.covariant.trace_electric_squared
        == ledger.trace_electric_squared
        and normalization.covariant.trace_ratio
        == ledger.trace_ratio
        == sp.Rational(3, 8),
    )
    checks.check(
        "inverse coupling rescaling preserves every Abelian charge product",
        normalization.rescaled_abelian_coupling == coupling / rho
        and normalization.charge_product_residuals == (0,) * len(states)
        and normalization.coupled_trace_norm_residual == 0,
    )

    checks.check(
        "homogeneous first and third Abelian moments vanish for the supplied table",
        weighted_abelian_moment(states, 1) == 0
        and weighted_abelian_moment(states, 3) == 0,
    )
    rescaled_states = normalization.rescaled_states
    checks.check(
        "homogeneous zero moments do not select the Abelian normalization",
        weighted_abelian_moment(rescaled_states, 1) == 0
        and weighted_abelian_moment(rescaled_states, 3) == 0,
    )
    mixed_su2 = sp.Rational(1, 2) * (
        3 * sp.Rational(1, 6) - sp.Rational(1, 2)
    )
    mixed_su3 = sp.Rational(1, 2) * (
        2 * sp.Rational(1, 6)
        - sp.Rational(2, 3)
        + sp.Rational(1, 3)
    )
    checks.check(
        "declared mixed linear anomaly sums also retain an arbitrary scale",
        mixed_su2 == mixed_su3 == 0
        and sp.simplify(rho * mixed_su2) == 0
        and sp.simplify(rho * mixed_su3) == 0,
    )

    generic_angle = charge_coupling_angle_ledger(
        ledger.trace_t3_squared,
        ledger.trace_abelian_squared,
        1,
        1,
    )
    checks.check(
        "equal supplied subgroup couplings do not equal the source trace angle",
        generic_angle.coupling_angle == sp.Rational(1, 2)
        and generic_angle.trace_angle == sp.Rational(3, 8)
        and generic_angle.angle_residual != 0,
    )
    checks.check(
        "trace-angle equality requires the extra three-fifths coupling ratio",
        generic_angle.required_coupling_squared_ratio == sp.Rational(3, 5)
        and generic_angle.coupling_squared_ratio == 1
        and generic_angle.equality_numerator != 0,
    )
    matched = charge_coupling_angle_ledger(
        ledger.trace_t3_squared,
        ledger.trace_abelian_squared,
        sp.sqrt(5),
        sp.sqrt(3),
    )
    checks.check(
        "a separately supplied three-fifths ratio is exactly sufficient",
        matched.coupling_squared_ratio == sp.Rational(3, 5)
        and matched.coupling_angle
        == matched.trace_angle
        == sp.Rational(3, 8)
        and matched.angle_residual == 0
        and matched.equality_numerator == 0,
    )
    common = sp.Symbol("C", positive=True)
    common_law = common_trace_normalized_coupling_angle(
        ledger.trace_t3_squared,
        ledger.trace_abelian_squared,
        common,
    )
    checks.check(
        "common inverse-trace kinetic coefficient is a conditional sufficient premise",
        common_law.coupling_angle == common_law.trace_angle == sp.Rational(3, 8)
        and common_law.su2_inverse_trace_coefficient == common
        and common_law.abelian_inverse_trace_coefficient == common,
    )
    unequal = charge_coupling_angle_ledger(
        2,
        sp.Rational(10, 3),
        sp.sqrt(sp.Rational(1, 4)),
        sp.sqrt(sp.Rational(3, 70)),
    )
    checks.check(
        "unequal kinetic coefficients break the trace-angle equality",
        unequal.su2_inverse_trace_coefficient == 2
        and unequal.abelian_inverse_trace_coefficient == 7
        and unequal.common_coefficient_residual == 5
        and unequal.angle_residual != 0,
    )

    no_colour = tuple(
        WeightedChargeState(
            state.label,
            1 if state.label.startswith(("Q_L", "u_R", "d_R")) else state.multiplicity,
            state.t3,
            state.abelian_charge,
        )
        for state in states
    )
    dropped = _replace_state(states, "e_R_conj", None)
    changed_doublet = _replace_state(
        states,
        "Q_L_up",
        WeightedChargeState("Q_L_up", 3, sp.Rational(1, 2), sp.Rational(1, 5)),
    )
    checks.mutation_sensitive(
        "state content and multiplicities are load bearing for the complete trace ledger",
        _exact_source_table,
        states,
        [no_colour, dropped, changed_doublet],
    )
    checks.check(
        "source colour and omission specializations reproduce conditionally",
        finite_charge_trace_ledger(no_colour).trace_ratio == sp.Rational(9, 28)
        and finite_charge_trace_ledger(dropped).trace_ratio == sp.Rational(6, 13),
    )

    flipped = _replace_state(
        states,
        "e_R_conj",
        WeightedChargeState("e_R_conj", 1, 0, -1),
    )
    flipped_ledger = finite_charge_trace_ledger(flipped)
    checks.check(
        "nonzero singlet-charge mutation can preserve every squared trace",
        flipped_ledger.trace_t3_squared == ledger.trace_t3_squared
        and flipped_ledger.trace_abelian_squared == ledger.trace_abelian_squared
        and flipped_ledger.trace_electric_squared == ledger.trace_electric_squared
        and flipped_ledger.trace_ratio == sp.Rational(3, 8)
        and weighted_abelian_moment(flipped, 1) != 0
        and weighted_abelian_moment(flipped, 3) != 0,
    )
    delta = sp.Symbol("delta", nonzero=True)
    source_guard_ratio = sp.simplify(
        2 / (sp.Rational(16, 3) + 2 * delta + delta**2)
    )
    checks.check(
        "WM1.6's only-at-zero statement has the exact nonzero delta minus two counterexample",
        sp.simplify(source_guard_ratio.subs(delta, -2) - sp.Rational(3, 8)) == 0
        and "sin2_pert_diff != 0" in source_text
        and "vanishes ONLY at" in source_text,
    )

    relabeled = tuple(
        WeightedChargeState(
            f"fabricated-{index}",
            state.multiplicity,
            state.t3,
            state.abelian_charge,
        )
        for index, state in enumerate(states)
    )
    checks.check(
        "fabricated labels preserve algebra and expose provenance as external",
        finite_charge_trace_ledger(relabeled).trace_ratio == ledger.trace_ratio
        and tuple(state.label for state in relabeled)
        != tuple(state.label for state in states),
    )

    assigned_names = {
        target.id
        for node in ast.walk(source_tree)
        if isinstance(node, (ast.Assign, ast.AnnAssign))
        for target in (
            node.targets if isinstance(node, ast.Assign) else [node.target]
        )
        if isinstance(target, ast.Name)
    }
    checks.check(
        "source computes a bare trace quotient and no gauge-coupling angle",
        "sin2_thetaW = tr_T3sq / tr_Qsq" in source_text
        and assigned_names.isdisjoint({"g2", "gY", "g_prime", "theta_W"}),
    )
    checks.check(
        "source performs no anomaly or kinetic-normalization derivation",
        [
            node
            for node in ast.walk(source_tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        == [
            node
            for node in ast.walk(source_tree)
            if isinstance(node, ast.Import)
            and len(node.names) == 1
            and node.names[0].name == "sympy"
            and node.names[0].asname == "sp"
        ]
        and len(
            [
                node
                for node in ast.walk(source_tree)
                if isinstance(node, (ast.Import, ast.ImportFrom))
            ]
        )
        == 1
        and "WM2" in source_text
        and "common-induction" in source_text
        and "trace FORMULA" in source_text,
    )
    literature = Path(
        _contract_path().parent / "evidence/literature-audit.yaml"
    ).read_text(encoding="utf-8")
    checks.check(
        "primary literature premises are recorded separately from source arithmetic",
        "10.1103/PhysRevLett.33.451" in literature
        and "simple_unified_group_embedding" in literature
        and "common_normalized_subgroup_coupling" in literature
        and "not_available_in_accepted_framework" in literature,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
