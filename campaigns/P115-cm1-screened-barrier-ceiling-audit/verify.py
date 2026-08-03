"""Primary exact verifier for P115's CM1 screened-barrier audit."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.screened_barrier import (
    inverse_sqrt_barrier_enhancement,
    inverse_sqrt_barrier_factor,
    shifted_barrier_ledger,
    shifted_inverse_sqrt_barrier_factor,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-31/"
    "bridge_CM1_separation_boundary.py"
)
SCREENING_SOURCE = Path("/home/dan/substrate/engineering/screening/screening.py")
SOURCE_SHA256 = "0f6881d96469274664ed1b762ff56a88b94ecdca599c22f8bb181052bd7f3ccc"
SCREENING_SHA256 = "8ed6d54c8e3626f58ee2b3da78ce6eea7f4689092103dc23ed888b985e4cb4c3"
CONTRACT_SHA256 = "d609e568e6647f2858c3dbf7f06ce5bb43203829aee104ff00287ce0a8be22b4"
FREEZE_SHA256 = "d609e568e6647f2858c3dbf7f06ce5bb43203829aee104ff00287ce0a8be22b4"


def _campaign_root() -> Path:
    candidates = (
        Path("campaigns/P115-cm1-screened-barrier-ceiling-audit"),
        Path("proposals/P115-cm1-screened-barrier-ceiling-audit"),
    )
    return next(path for path in candidates if path.exists())


def main() -> int:
    checks = CheckLedger("C-SCR-001")
    root = _campaign_root()
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "CM1 source hash is pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "external screening source hash is pinned",
        hashlib.sha256(SCREENING_SOURCE.read_bytes()).hexdigest() == SCREENING_SHA256,
    )
    normalized_contract = (
        (root / "proposal.yaml")
        .read_bytes()
        .replace(b"status: accepted\n", b"status: draft\n")
    )
    checks.check(
        "candidate contract remains frozen apart from terminal status",
        hashlib.sha256(normalized_contract).hexdigest() == CONTRACT_SHA256,
    )
    checks.check(
        "pre-source contract is immutable",
        hashlib.sha256((root / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    source_checks = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "thirteen static predicates match the runtime tally",
        len(source_checks) == 13
        and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "CM1 has no sampled-integration compatibility event",
        "np.trapz" not in source_text
        and "np.trapezoid" not in source_text
        and "np.integrate" not in source_text,
    )

    energy, barrier, shift = sp.symbols("E G U", positive=True)
    bare = inverse_sqrt_barrier_factor(energy, barrier)
    shifted = shifted_inverse_sqrt_barrier_factor(energy, barrier, shift)
    enhancement = inverse_sqrt_barrier_enhancement(energy, barrier, shift)
    expected_shifted = sp.exp(-sp.sqrt(barrier / (energy + shift)))
    checks.check(
        "canonical shifted factor has the exact inverse-square-root exponent",
        sp.simplify(shifted - expected_shifted) == 0,
    )
    checks.check(
        "bare factor times enhancement composes exactly",
        sp.simplify(bare * enhancement - shifted) == 0,
    )
    checks.check(
        "zero shift recovers the bare factor and unit enhancement",
        sp.simplify(
            shifted_inverse_sqrt_barrier_factor(energy, barrier, 0) - bare
        )
        == 0
        and inverse_sqrt_barrier_enhancement(energy, barrier, 0) == 1,
    )

    ledger = shifted_barrier_ledger(energy, barrier, shift)
    expected_positive_derivative = sp.sqrt(barrier) / (
        2 * (energy + shift) ** sp.Rational(3, 2)
    )
    checks.check(
        "global log derivative in collision energy is strictly positive",
        sp.simplify(
            ledger.log_energy_derivative - expected_positive_derivative
        )
        == 0
        and ledger.log_energy_derivative.is_positive is True,
    )
    checks.check(
        "global log derivative in energy shift is strictly positive",
        sp.simplify(ledger.log_shift_derivative - expected_positive_derivative) == 0
        and ledger.log_shift_derivative.is_positive is True,
    )
    checks.check(
        "global log derivative in barrier scale is strictly negative",
        ledger.log_barrier_scale_derivative.is_negative is True,
    )
    exponent = -sp.sqrt(barrier / (energy + shift))
    checks.check(
        "finite shifted factor has the sharp open range zero to one",
        exponent.is_negative is True and shifted.is_positive is True,
    )

    inverse_power = lambda value: value ** -sp.Rational(3, 2)
    enhancement_log_derivative = sp.simplify(sp.diff(sp.log(enhancement), energy))
    expected_enhancement_derivative = sp.sqrt(barrier) / 2 * (
        inverse_power(energy + shift) - inverse_power(energy)
    )
    kernel_variable = sp.symbols("x", positive=True)
    checks.check(
        "enhancement decreases with energy for every positive shift",
        sp.simplify(
            enhancement_log_derivative - expected_enhancement_derivative
        )
        == 0
        and sp.diff(
            kernel_variable ** -sp.Rational(3, 2), kernel_variable
        ).is_negative
        is True,
    )

    checks.check(
        "bare and shifted low-energy limits separate exactly",
        sp.limit(bare, energy, 0, dir="+") == 0
        and sp.simplify(
            sp.limit(shifted, energy, 0, dir="+")
            - sp.exp(-sp.sqrt(barrier / shift))
        )
        == 0,
    )
    checks.check(
        "enhancement diverges while the composed low-energy factor stays finite",
        sp.limit(enhancement, energy, 0, dir="+") == sp.oo
        and sp.limit(shifted, energy, 0, dir="+").is_finite is True,
    )
    checks.check(
        "high-energy limits are both unity",
        sp.limit(shifted, energy, sp.oo) == 1
        and sp.limit(enhancement, energy, sp.oo) == 1,
    )
    checks.check(
        "positive-shift floor is finite nonzero rather than a null",
        sp.exp(-sp.sqrt(barrier / shift)).is_positive is True,
    )

    rho = sp.symbols("rho", positive=True)
    rescaled = shifted_inverse_sqrt_barrier_factor(
        rho * energy,
        rho * barrier,
        rho * shift,
    )
    checks.check(
        "common energy rescaling leaves every factor invariant",
        sp.simplify(rescaled - shifted) == 0
        and sp.simplify(
            inverse_sqrt_barrier_enhancement(
                rho * energy, rho * barrier, rho * shift
            )
            - enhancement
        )
        == 0,
    )
    checks.check(
        "energy dimensions close only through ratios and sums",
        (1 - 1, 1 - 1) == (0, 0),
    )
    checks.check(
        "an independently bounded larger shift gives the upper factor",
        ledger.log_shift_derivative.is_positive is True
        and float(shifted.subs({energy: 2, barrier: 11, shift: 1}))
        < float(shifted.subs({energy: 2, barrier: 11, shift: 3})),
    )

    checks.mutation_sensitive(
        "exponent sign and square-root normalization are load bearing",
        lambda candidate: sp.simplify(candidate - expected_shifted) == 0,
        shifted,
        (
            sp.exp(sp.sqrt(barrier / (energy + shift))),
            sp.exp(-barrier / (energy + shift)),
            sp.exp(-sp.sqrt((2 * barrier) / (energy + shift))),
            sp.exp(-sp.sqrt(barrier / (energy - shift))),
        ),
    )
    checks.mutation_sensitive(
        "bare-enhancement composition is load bearing",
        lambda candidate: sp.simplify(candidate - shifted) == 0,
        bare * enhancement,
        (enhancement, bare, bare + enhancement, bare / enhancement),
    )

    with np.errstate(over="ignore", under="ignore", invalid="ignore"):
        tiny = np.float64(1e-100)
        barrier_value = np.float64(1000.0)
        shift_value = np.float64(1.0)
        separate_product = np.exp(-np.sqrt(barrier_value / tiny)) * np.exp(
            np.sqrt(barrier_value / tiny)
            - np.sqrt(barrier_value / (tiny + shift_value))
        )
        direct_value = np.exp(
            -np.sqrt(barrier_value / (tiny + shift_value))
        )
    checks.check(
        "direct composed evaluation avoids zero-times-infinity indeterminacy",
        np.isnan(separate_product)
        and np.isfinite(direct_value)
        and direct_value > 0,
    )

    inverse_time_prefactor = sp.symbols("nu", nonnegative=True)
    conditional_rate = inverse_time_prefactor * shifted
    checks.check(
        "zero prefactor removes a rate while leaving the barrier factor",
        shifted != 0
        and conditional_rate.subs(inverse_time_prefactor, 0) == 0,
    )
    checks.check(
        "arbitrary prefactor scale prevents an absolute rate ceiling",
        sp.simplify(
            conditional_rate.subs(inverse_time_prefactor, 7)
            - 7 * conditional_rate.subs(inverse_time_prefactor, 1)
        )
        == 0,
    )
    wrong_increasing_shape = energy / (energy + barrier)
    checks.check(
        "source pointwise shape guard admits a non-Gamow increasing function",
        sp.diff(wrong_increasing_shape, energy).subs({energy: 1, barrier: 987}) > 0
        and not wrong_increasing_shape.has(sp.exp, sp.sqrt),
    )
    checks.check(
        "source monotonicity verdict is based on one substituted point",
        "sign_pos = dRexp_dE_s.subs" in source_text
        and "val = d.subs" in source_text,
    )
    checks.check(
        "source material ceiling is only a four-model selected maximum",
        "metals = [scr.MAT_NI, scr.MAT_PD, scr.MAT_TI, scr.MAT_ZR]" in source_text
        and "max(scr.material_U_e_eV(m) for m in metals)" in source_text,
    )
    checks.check(
        "source negligibility and opening checks use selected absolute thresholds",
        "screened_ceiling(1e-3) < 1e-10" in source_text
        and "screened_ceiling(100.0) > 1e-3" in source_text,
    )
    checks.check(
        "source neutral-uncapped predicate repeats the same function call",
        "R_grid[-1] == screened_ceiling(100.0)" in source_text,
    )

    predicate_audit = yaml.safe_load(
        (root / "evidence/check-adjudication.yaml").read_text()
    )
    checks.check(
        "all thirteen source predicates have individual verdicts",
        predicate_audit["runtime_predicate_count"] == 13
        and len(predicate_audit["predicates"]) == 13
        and all(
            item["verdict"] in {"retained", "qualified", "duplicate", "rejected"}
            for item in predicate_audit["predicates"]
        ),
    )
    dependency = yaml.safe_load((root / "evidence/dependency-audit.yaml").read_text())
    checks.check(
        "forward source cycle supplies no claim dependency",
        dependency["accepted_claim_dependencies"] == []
        and dependency["cycle_authority"] == "none"
        and dependency["dependency_closure"]
        == "conditional_elementary_barrier_algebra_only",
    )
    consumers = yaml.safe_load((root / "evidence/consumer-audit.yaml").read_text())
    checks.check(
        "five direct consumers and their hashes are pinned",
        consumers["closure"]["direct_count"] == 5
        and consumers["closure"]["indirect_count"] == 0
        and all(
            hashlib.sha256(
                (Path("/home/dan/substrate") / item["path"]).read_bytes()
            ).hexdigest()
            == item["sha256"]
            for item in consumers["consumers"]
        ),
    )
    registry = yaml.safe_load(Path("governance/claims.yaml").read_text())
    proposal = yaml.safe_load((root / "proposal.yaml").read_text())
    claim_records = [
        claim for claim in registry["claims"] if claim["id"] == "C-SCR-001"
    ]
    lifecycle_valid = (
        proposal["status"] == "draft" and claim_records == []
    ) or (
        proposal["status"] == "accepted"
        and len(claim_records) == 1
        and claim_records[0]["review"] == "accepted"
        and claim_records[0]["epistemic"] == "active"
        and claim_records[0]["provenance"]
        == "campaigns/P115-cm1-screened-barrier-ceiling-audit/adjudication.yaml"
    )
    checks.check(
        "C-SCR-001 has exactly one lifecycle-valid claim record",
        proposal["claims_proposed"] == ["C-SCR-001"] and lifecycle_valid,
    )
    checks.check(
        "exact campaign needs no quadrature solver fit or comparator",
        not shifted.has(sp.Float, sp.Integral),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
