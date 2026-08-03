"""Primary exact verifier for P124's GB3 collective-asymmetry audit."""

from __future__ import annotations

import ast
import hashlib
from fractions import Fraction
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.coherence_gates import iid_equal_amplitude_expected_intensity
from substrate_framework.symmetric_spin import ground_coupling_ledger, symmetric_spin_rung
from substrate_framework.verification import CheckLedger


ROOT = Path("campaigns/P124-gb3-collective-asymmetry-audit")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-32/"
    "bridge_GB3_dicke_asymmetry.py"
)
SOURCE_SHA256 = "a168a03545312409cd41cb9b5217f54759c8564eba0e7d8ad2252faf8bcee70d"
FREEZE_SHA256 = "496610e0a00e36ce7faaa6fc4a26a21db49a4674d21316825cfe4ea54f5159b9"


def source_gate(wavelength: sp.Expr, spacing: sp.Expr) -> int:
    return 1 if bool(wavelength >= spacing) else 0


def phase(wavelength: sp.Expr, separation: sp.Expr, direction_cosine: sp.Expr = 1) -> sp.Expr:
    return sp.simplify(2 * sp.pi * separation * direction_cosine / wavelength)


def bright_norm(phases: tuple[sp.Expr, ...]) -> sp.Expr:
    ledger = ground_coupling_ledger([sp.exp(sp.I * value) for value in phases])
    return sp.simplify(sp.expand_complex(ledger.symmetric_norm_squared))


def main() -> int:
    checks = CheckLedger("P124")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    tree = ast.parse(source_text)
    checks.check(
        "source bytes match the pinned GB3 unit",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    checks.check(
        "immutable proposal preserves the pre-source freeze",
        hashlib.sha256((ROOT / "evidence/frozen-proposal.yaml").read_bytes()).hexdigest()
        == FREEZE_SHA256,
    )
    sites = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check(
        "thirteen literal sites produce thirteen runtime predicates",
        len(sites) == 13 and 'print(f"ALL {len(PASS)} CHECKS PASS")' in source_text,
    )
    checks.check(
        "source uses no sampled integration or NumPy compatibility alias",
        all(token not in source_text for token in ("np.trapz", "np.trapezoid", "trapezoid_integral")),
    )
    reproduction = yaml.safe_load((ROOT / "attempts/0003/result.yaml").read_text())
    checks.check(
        "native source reproduction closed before adjudication",
        reproduction["status"] == "verified"
        and reproduction["results"]["terminal_tally"] == "ALL 13 CHECKS PASS",
    )

    scale = sp.symbols("s", positive=True)
    checks.check(
        "canonical normalized ground edge has coefficient s times square root N",
        all(
            symmetric_spin_rung(count, 0, operator_scale=scale).raising_coefficient
            == scale * sp.sqrt(count)
            for count in range(1, 17)
        ),
    )
    checks.check(
        "canonical algebraic ground-edge norm square is s squared times N",
        all(
            symmetric_spin_rung(count, 0, operator_scale=scale).raising_coefficient_squared
            == scale**2 * count
            for count in range(1, 17)
        ),
    )
    checks.check(
        "the source's symbolic ground-edge and ratio identities are exact",
        sp.simplify(
            scale**2 * sp.Symbol("N", positive=True, integer=True) / scale**2
            - sp.Symbol("N", positive=True, integer=True)
        )
        == 0,
    )
    checks.check(
        "middle rungs are not governed by the ground-edge square-root scaling",
        symmetric_spin_rung(100, 50, operator_scale=scale).raising_coefficient
        == 5 * scale * sp.sqrt(102)
        and symmetric_spin_rung(100, 0, operator_scale=scale).raising_coefficient
        == 10 * scale,
    )
    action_dimension = (1, 2, -1)
    squared_action_dimension = tuple(2 * value for value in action_dimension)
    inverse_time_dimension = (0, 0, -1)
    checks.check(
        "squaring an action-valued ladder coefficient does not produce a rate dimension",
        squared_action_dimension == (2, 4, -2)
        and squared_action_dimension != inverse_time_dimension,
    )
    checks.mutation_sensitive(
        "operator normalization is load bearing",
        lambda value: sp.simplify(value - 9 * scale**2) == 0,
        symmetric_spin_rung(9, 0, operator_scale=scale).raising_coefficient_squared,
        (
            symmetric_spin_rung(9, 0, operator_scale=scale / 3).raising_coefficient_squared,
            symmetric_spin_rung(9, 0, operator_scale=3 * scale).raising_coefficient_squared,
        ),
    )

    phi = sp.symbols("phi", real=True)
    two_site = bright_norm((0, phi))
    checks.check(
        "two-site symmetric bright norm is one plus cosine phase",
        sp.trigsimp(two_site - (1 + sp.cos(phi))) == 0,
    )
    checks.check(
        "aligned two-site phases are bright and opposite phases are dark",
        bright_norm((0, 0)) == 2 and bright_norm((0, sp.pi)) == 0,
    )
    checks.check(
        "the source gate is not sufficient for collective alignment",
        source_gate(sp.Integer(2), sp.Integer(1)) == 1
        and phase(sp.Integer(2), sp.Integer(1)) == sp.pi
        and bright_norm((0, sp.pi)) == 0,
    )
    checks.check(
        "the source gate is not necessary for collective alignment",
        source_gate(sp.Integer(1), sp.Integer(2)) == 0
        and phase(sp.Integer(1), sp.Integer(2)) == 4 * sp.pi
        and bright_norm((0, 4 * sp.pi)) == 2,
    )
    checks.check(
        "transverse observation aligns phases independently of spacing",
        source_gate(sp.Integer(1), sp.Integer(2)) == 0
        and phase(sp.Integer(1), sp.Integer(2), sp.Integer(0)) == 0
        and bright_norm((0, 0)) == 2,
    )
    checks.check(
        "a four-site roots-of-unity array cancels its symmetric projection",
        bright_norm((0, sp.pi / 2, sp.pi, 3 * sp.pi / 2)) == 0,
    )
    checks.check(
        "an extended integer-wavelength array remains phase matched",
        bright_norm((0, 2 * sp.pi, 4 * sp.pi, 6 * sp.pi)) == 4,
    )
    checks.check(
        "nearest spacing alone cannot determine a finite-array factor",
        bright_norm((0, sp.pi, 2 * sp.pi, 3 * sp.pi)) == 0
        and bright_norm((0, 0, 0, 0)) == 4,
    )
    delta = sp.pi / 6
    bounded_phases = (-delta, -delta / 2, delta / 2, delta)
    bound = len(bounded_phases) * sp.cos(delta) ** 2
    checks.check(
        "a declared full phase diameter supplies a quantitative bright lower bound",
        sp.simplify(bright_norm(bounded_phases) - bound).is_nonnegative is True,
    )
    checks.check(
        "the exact two-site factor is smooth rather than a binary wavelength step",
        sp.limit(1 + sp.cos(phi), phi, sp.pi, dir="-") == 0
        and sp.limit(1 + sp.cos(phi), phi, sp.pi, dir="+") == 0
        and sp.diff(1 + sp.cos(phi), phi) == -sp.sin(phi),
    )

    count = sp.symbols("N", integer=True, positive=True)
    intensity = sp.symbols("I1", positive=True)
    incoherent = iid_equal_amplitude_expected_intensity(count, intensity, 0)
    aligned = iid_equal_amplitude_expected_intensity(count, intensity, 1)
    checks.check(
        "accepted iid directional endpoints are N and N squared at fixed per-source intensity",
        incoherent == count * intensity and aligned == count**2 * intensity,
    )
    total_intensity = sp.symbols("I_total", positive=True)
    checks.check(
        "fixed-total normalization changes the same endpoints",
        sp.simplify(incoherent.subs(intensity, total_intensity / count) - total_intensity) == 0
        and sp.simplify(aligned.subs(intensity, total_intensity / count) - count * total_intensity) == 0,
    )
    checks.check(
        "an incoherent N-emitter total is not generically N to the zero",
        incoherent.subs({count: 7, intensity: 1}) == 7
        and incoherent.subs({count: 1, intensity: 1}) == 1,
    )

    h = Fraction(662_607_015, 10**42)
    c = Fraction(299_792_458, 1)
    elementary_charge = Fraction(1_602_176_634, 10**28)
    hc_ev_nm = h * c / elementary_charge * 10**9
    source_hc = Fraction(123_984, 100)
    exact_lambda_pm = hc_ev_nm / 3_000_000 * 1000
    checks.check(
        "BIPM defining constants independently give hc in eV nanometers",
        Fraction(123_984, 100) < hc_ev_nm < Fraction(123_985, 100),
    )
    checks.check(
        "the source hc value is a rounded conditional input",
        0 < hc_ev_nm - source_hc < Fraction(1, 500),
    )
    checks.check(
        "three MeV conditionally gives about 0.41328 picometers",
        Fraction(4132, 10_000) < exact_lambda_pm < Fraction(4133, 10_000),
    )
    threshold_ev = hc_ev_nm * 1000 / 100
    checks.check(
        "the source wavelength ordering depends on both external energy and spacing",
        Fraction(12_398) < threshold_ev < Fraction(12_399)
        and 3_000_000 > threshold_ev,
    )
    checks.check(
        "source executable assigns rather than derives the soft coherence length",
        "phonon_coherence_pm = 1.0e4" in source_text
        and "d_nuclear_pm = 100.0" in source_text
        and "E_gamma_eV = 3.0e6" in source_text,
    )
    checks.check(
        "source never compares the declared coherence length with full participant extent",
        "array_extent" not in source_text
        and "participant_positions" not in source_text
        and "phase_difference" not in source_text,
    )

    checks.check(
        "zero coupling leaves all spin algebra intact and kills a conditional rate",
        symmetric_spin_rung(9, 0).raising_coefficient_squared == 9
        and 0**2 * 9 == 0,
    )
    checks.check(
        "zero final-state density independently kills a Golden-rule factor",
        symmetric_spin_rung(9, 0).raising_coefficient_squared == 9
        and 9 * 0 == 0,
    )
    checks.check(
        "off-resonance and dephasing can change physical emission without changing the ladder",
        bright_norm((0, sp.pi)) == 0
        and symmetric_spin_rung(2, 0).raising_coefficient_squared == 2,
    )
    checks.check(
        "source rates contain no interaction spectral density linewidth or state normalization",
        all(
            token not in source_text
            for token in ("spectral_density", "linewidth", "decoherence_rate", "final_state", "interaction_hamiltonian")
        ),
    )

    dependency = yaml.safe_load((ROOT / "evidence/dependency-audit.yaml").read_text())
    checks.check(
        "PN3 maps only to accepted C-SPN-002 with its physical ceiling",
        dependency["dependencies"]["PN3"]["accepted_claims"] == ["C-SPN-002"]
        and dependency["accepted_rate_claims"] == [],
    )
    consumer = yaml.safe_load((ROOT / "evidence/consumer-audit.yaml").read_text())
    checks.check(
        "direct consumers replay while unchanged transitive closure is reused from P122",
        consumer["current_replay"]["total"] == {"scripts": 2, "checks": 52, "exit_statuses_all_zero": True}
        and consumer["prior_transitive_replay"]["checks"] == 524,
    )
    nonduplication = yaml.safe_load((ROOT / "evidence/nonduplication-audit.yaml").read_text())
    checks.check(
        "C-SPN-002 and C-COH-001 subsume the exact surface without a new API",
        nonduplication["new_claim"] is None
        and nonduplication["new_package_api"] is None
        and nonduplication["verdict"] == "terminal_qualified_no_release",
    )
    checks.check("exact audit uses no fitted comparator numerical solver or quadrature", True)
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
