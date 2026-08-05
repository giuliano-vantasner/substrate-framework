#!/usr/bin/env python3
"""Primary exact verifier for the GK3D6 accepted-composition audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.charge_traces import (
    charge_coupling_angle_ledger,
    common_trace_normalized_coupling_angle,
)
from substrate_framework.kinetic_scale_matching import (
    inverse_length_scale_kinetic_evidence,
    one_loop_scale_matched_kinetic_evidence,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = Path(__file__).resolve().parent
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-41/"
    "bridge_GK3D6_oneloop_accuracy_and_exact_ratios.py"
)
SOURCE_SHA256 = "e0ab2a2db57affe023e6838ed835656412cf01188225f31084e6a6a1baf8e036"
RELEASE_SHA256 = "18dffeef5efd516018c918f65b45173c81ac0e1ba99fdd8a96274cc1df5c72db"
FORMULA_FREEZE_SHA256 = (
    "ef2a13c08f4804feac7006f20628d59aede0e4b9a13cf99b9e89f7ca76cc0af0"
)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(path: Path) -> dict:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"expected mapping in {path}")
    return value


def main() -> int:
    checks = CheckLedger("P203-GK3D6-SCHEME-RATIO")
    checks.check("source hash remains pinned", _digest(SOURCE) == SOURCE_SHA256)
    checks.check(
        "base release remains pinned",
        _digest(ROOT / "governance/releases/v0.150.0.yaml") == RELEASE_SHA256,
    )
    checks.check(
        "formula freeze remains pinned",
        _digest(CAMPAIGN / "evidence/formula-freeze.yaml")
        == FORMULA_FREEZE_SHA256,
    )

    source_text = SOURCE.read_text(encoding="utf-8")
    source_tree = ast.parse(source_text, filename=str(SOURCE))
    check_calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    assertions = [node for node in ast.walk(source_tree) if isinstance(node, ast.Assert)]
    checks.check(
        "source predicate inventory remains exact",
        len(check_calls) == 10 and len(assertions) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "source has no trapezoidal compatibility surface",
        compatibility.legacy_references == 0
        and compatibility.current_references == 0
        and compatibility.eager_legacy_default_fallbacks == 0,
    )
    checks.check(
        "source hardcodes its common zero-boundary family",
        all(
            token in source_text
            for token in (
                "Z_i = (bi / (8 * sp.pi**2)) * (L - sp.log(c))",
                "Z_j = (bj / (8 * sp.pi**2)) * (L - sp.log(c))",
                "TrYsq = sp.Rational(5, 3) * TrT3sq",
                "8 * math.pi**2 / (7 * 0.245)",
                "math.log(1e20)",
            )
        ),
    )
    checks.check(
        "source supplies no two-loop scheme compensation or particle map",
        not any(
            token in source_text
            for token in (
                "two_loop_coefficient",
                "two_loop_beta",
                "propagator_pole",
                "quantize_radial",
                "determinant_field_map",
            )
        ),
    )

    K = 8 * sp.pi**2
    bi, bj = sp.symbols("b_i b_j", positive=True)
    zi, zj = sp.symbols("z_i z_j", real=True)
    L, s = sp.symbols("L s", real=True)
    Xi = L - s
    Zi = zi + bi * Xi / K
    Zj = zj + bj * Xi / K
    ratio = sp.cancel(Zj / Zi)
    derivative = sp.factor(sp.diff(ratio, s))
    expected_derivative = sp.factor((bi * zj - bj * zi) / (K * Zi**2))
    checks.check(
        "general common-scale inverse-coordinate ratio retains boundaries",
        sp.simplify(ratio - Zj / Zi) == 0 and ratio.has(zi, zj),
    )
    checks.check(
        "scheme derivative has the exact proportional-boundary numerator",
        sp.simplify(derivative - expected_derivative) == 0,
    )
    numerator, denominator = sp.together(derivative).as_numer_denom()
    checks.check(
        "nonzero-domain cancellation is equivalent to proportional boundaries",
        sp.factor(numerator) == K * (bi * zj - bj * zi)
        and denominator != 0,
    )
    alpha = sp.Symbol("alpha", real=True)
    checks.check(
        "proportional nonzero boundaries cancel conditionally",
        sp.simplify(ratio.subs({zi: alpha * bi, zj: alpha * bj}) - bj / bi)
        == 0,
    )
    zero_ratio = sp.simplify(ratio.subs({zi: 0, zj: 0}) - bj / bi)
    checks.check("zero matching recovers the source ratio", zero_ratio == 0)
    checks.mutation_sensitive(
        "common-scale ratio premises",
        lambda candidate: sp.simplify(candidate - bj / bi) == 0,
        ratio.subs({zi: 0, zj: 0}),
        [
            ratio.subs({zi: 1, zj: 0}),
            ratio.subs({zi: 0, zj: 1}),
            ratio.subs({zi: bi, zj: 2 * bj}),
        ],
    )

    Li, Lj, si, sj = sp.symbols("L_i L_j s_i s_j", real=True)
    Xi_general = Li - si
    Xj_general = Lj - sj
    Zi_general = zi + bi * Xi_general / K
    Zj_general = zj + bj * Xj_general / K
    residual = sp.factor(bi * Zj_general - bj * Zi_general)
    expected_residual = sp.factor(
        bi * zj - bj * zi + bi * bj * (Xj_general - Xi_general) / K
    )
    checks.check(
        "factorwise logs add an exact load-bearing residual",
        sp.simplify(residual - expected_residual) == 0
        and residual.has(Li, Lj, si, sj),
    )
    checks.mutation_sensitive(
        "factorwise logarithm and scale-factor equality",
        lambda candidate: sp.simplify(candidate) == 0,
        residual.subs({zi: 0, zj: 0, Li: L, Lj: L, si: s, sj: s}),
        [
            residual.subs({zi: 0, zj: 0, Li: L, Lj: L + 1, si: s, sj: s}),
            residual.subs({zi: 0, zj: 0, Li: L, Lj: L, si: s, sj: s + 1}),
            residual.subs({zi: 0, zj: 0, Li: L, Lj: -L, si: s, sj: s}),
        ],
    )

    ell0, ell1, k0, k1 = sp.symbols("ell_0 ell_1 K_0 K_1", positive=True)
    scale = inverse_length_scale_kinetic_evidence(
        ell0,
        ell1,
        k0,
        k1,
        0,
        0,
        0,
        1,
    )
    checks.check(
        "accepted inverse-length composition retains conversion factors",
        sp.simplify(
            scale.scale_logarithm - sp.log((ell1 / ell0) / (k1 / k0))
        )
        == 0,
    )
    rho = sp.Symbol("rho", positive=True)
    checks.check(
        "common length rescaling cancels while one conversion mutation does not",
        scale.common_rescaling_log_residual == 0
        and sp.simplify(
            scale.scale_logarithm.subs(k1, rho * k1) - scale.scale_logarithm
        )
        != 0,
    )

    g2, b0, mu0 = sp.symbols("g2 b0 mu0", positive=True)
    matched_i = one_loop_scale_matched_kinetic_evidence(
        mu0,
        g2,
        b0,
        reference_conversion=1,
        transmuted_conversion=1,
        renormalized_local_coefficient=zi,
        finite_matching_offset=0,
        scalar_weight=0,
        dirac_weight=bi,
    )
    matched_j = one_loop_scale_matched_kinetic_evidence(
        mu0,
        g2,
        b0,
        reference_conversion=1,
        transmuted_conversion=1,
        renormalized_local_coefficient=zj,
        finite_matching_offset=0,
        scalar_weight=0,
        dirac_weight=bj,
    )
    checks.check(
        "accepted one-loop match retains both affine boundaries",
        matched_i.general_kinetic_coefficient.has(zi)
        and matched_j.general_kinetic_coefficient.has(zj)
        and matched_i.zero_matching_is_separate_premise
        and matched_j.zero_matching_is_separate_premise,
    )
    checks.check(
        "source inverse-weight ratio is only the explicit zero branch",
        sp.simplify(
            matched_i.zero_matching_inverse_kinetic_coordinate
            / matched_j.zero_matching_inverse_kinetic_coordinate
            - bj / bi
        )
        == 0,
    )

    Z_at_c = bi * (L - s) / K
    Z_at_one = bi * L / K
    g_at_c = 1 / Z_at_c
    g_at_one = 1 / Z_at_one
    relative_Z = sp.simplify((Z_at_c - Z_at_one) / Z_at_one)
    relative_g = sp.simplify((g_at_c - g_at_one) / g_at_one)
    checks.check("normalization shift is exactly minus s over L", relative_Z == -s / L)
    checks.check(
        "inverse-coordinate shift is distinct and retains the scale factor",
        relative_g == s / (L - s) and relative_g != relative_Z,
    )
    checks.check(
        "large-log asymptotics require a separately bounded fixed shift",
        sp.limit(L * relative_g, L, sp.oo) == s
        and sp.simplify(Z_at_c.subs(s, L)) == 0,
    )

    conditional_angle = common_trace_normalized_coupling_angle(
        2, sp.Rational(10, 3), sp.Symbol("C", positive=True)
    )
    independent_angle = charge_coupling_angle_ledger(
        2, sp.Rational(10, 3), 1, 1
    )
    checks.check(
        "three eighths is a conditional common-trace coordinate",
        conditional_angle.coupling_angle == sp.Rational(3, 8)
        and conditional_angle.common_coefficient_residual == 0,
    )
    checks.check(
        "independent couplings preserve traces while refuting automatic three eighths",
        independent_angle.trace_angle == sp.Rational(3, 8)
        and independent_angle.coupling_angle == sp.Rational(1, 2),
    )

    dispositions = _load(ROOT / "migration/dispositions.yaml")["units"]
    checks.check(
        "AS7 already rejects the alleged independent numerical routes",
        dispositions["AS7"]["disposition"] == "qualified"
        and "true by construction" in dispositions["AS7"]["qualification"]
        and "not derived" in dispositions["AS7"]["qualification"],
    )
    qball_text = (ROOT / "src/substrate_framework/radial_qball.py").read_text(
        encoding="utf-8"
    )
    checks.check(
        "accepted radial branch exports no particle determinant or substrate identity",
        "does not quantize the branch" in qball_text
        and "make it a determinant field" in qball_text
        and "asymptotic\nparticle" in qball_text,
    )
    claims = {claim["id"]: claim for claim in _load(ROOT / "governance/claims.yaml")["claims"]}
    checks.check(
        "accepted composition owns the corrected object and C-VAC-006 is absent",
        all(
            claims[claim_id]["review"] == "accepted"
            for claim_id in (
                "C-RGE-003",
                "C-IDN-002",
                "C-VAC-003",
                "C-VAC-004",
                "C-REP-001",
                "C-QBL-004",
            )
        )
        and "C-VAC-006" not in claims,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
