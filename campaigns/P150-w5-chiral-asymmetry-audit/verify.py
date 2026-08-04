#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-SCT-001 and W5."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.boundary_scattering import (
    passive_half_line_scattering_ledger,
)
from substrate_framework.branching import two_channel_allocation
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P150-w5-chiral-asymmetry-audit"
SOURCE_ROOT = Path("/home/dan/substrate")
SOURCE = SOURCE_ROOT / "merged-framework/bridges/phase-6/bridge_W5_chiral_asymmetry_magnitude.py"
DOSSIER = SOURCE_ROOT / "merged-framework/bridges/phase-6/dossiers/W5_dossier.md"
SOLUTION = SOURCE_ROOT / "sg-breather-ionization/solution.md"
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
SOURCE_SHA256 = "5afea85e0e70236ddd076e2da585d6ab5861d52211239642eac1c951f1c6a71a"
DOSSIER_SHA256 = "761e30e9f93a6d74f7d017af0af89dae39cfa10c38c128bd0ef3c316fd1f6401"
SOLUTION_SHA256 = "a5a0ced9a097f07daea67e37b9516755307536e4850dfc975da72ee8eb876f86"
FROZEN_SHA256 = "4342a1b8dfc1bb842d558d4dbfe363f6f6bd746ee281efd0f779aeef541e6f35"
REVISION_SHA256 = "0427299aebadd0d65a1eea7e4957388a6c073ce6f89ec86d781fc335c27af03a"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    checks = CheckLedger("P150/C-SCT-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    dossier_text = DOSSIER.read_text(encoding="utf-8")
    solution_text = SOLUTION.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned W5 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("pinned W5 dossier hash", _sha256(DOSSIER) == DOSSIER_SHA256)
    checks.check("pinned imported solution hash", _sha256(SOLUTION) == SOLUTION_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)

    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    source_assertions = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    checks.check("twenty-seven source predicates", len(source_checks) == 27)
    checks.check("one source assertion", len(source_assertions) == 1)
    compatibility = audit_numpy_trapezoid_compatibility(source_text, filename=str(SOURCE))
    checks.check(
        "W5 has no NumPy integration compatibility shape",
        compatibility.legacy_references == 0
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
    checks.check("native W5 exits cleanly", native.returncode == 0)
    checks.check(
        "native W5 terminal tally is exact",
        native.stdout.splitlines()[-2] == "ALL 27 CHECKS PASS",
    )

    speed, boundary, frequency = sp.symbols("c zeta omega", positive=True)
    incident, reflected = sp.symbols("A_i A_r", nonzero=True)
    ledger = passive_half_line_scattering_ledger(speed, boundary)
    z = boundary / speed

    time_trace = -sp.I * frequency * (incident + reflected)
    spatial_trace = -sp.I * frequency / speed * (incident - reflected)
    solved = sp.solve(
        sp.Eq(time_trace - boundary * spatial_trace, 0),
        reflected,
    )[0]
    checks.check(
        "correctly oriented passive plane waves derive amplitude reflection",
        sp.simplify(solved / incident - ledger.amplitude_reflection) == 0,
    )
    checks.check(
        "reflection and absorbed fractions are exact",
        sp.simplify(ledger.reflected_power_fraction - (z - 1) ** 2 / (z + 1) ** 2) == 0
        and sp.simplify(ledger.absorbed_power_fraction - 4 * z / (z + 1) ** 2) == 0,
    )
    checks.check(
        "matched impedance is reflectionless",
        passive_half_line_scattering_ledger(speed, speed).amplitude_reflection == 0,
    )
    checks.check(
        "zero and infinite impedance limits are power reflecting",
        sp.limit(ledger.reflected_power_fraction, boundary, 0, dir="+") == 1
        and sp.limit(ledger.reflected_power_fraction, boundary, sp.oo) == 1,
    )

    bulk_rate = -speed**2 * sp.Symbol("phi_x", real=True) * sp.Symbol(
        "phi_t", real=True
    )
    spatial_value = sp.symbols("q", real=True, nonzero=True)
    checks.check(
        "passive sign removes right-half-line bulk energy",
        sp.simplify(
            bulk_rate.subs(
                {
                    sp.Symbol("phi_x", real=True): spatial_value,
                    sp.Symbol("phi_t", real=True): boundary * spatial_value,
                }
            )
            + speed**2 * boundary * spatial_value**2
        )
        == 0,
    )
    checks.check(
        "source displayed sign injects rather than absorbs energy",
        sp.simplify(
            bulk_rate.subs(
                {
                    sp.Symbol("phi_x", real=True): spatial_value,
                    sp.Symbol("phi_t", real=True): -boundary * spatial_value,
                }
            )
            - speed**2 * boundary * spatial_value**2
        )
        == 0,
    )
    checks.check(
        "source labels outgoing and incoming waves in reverse on x positive",
        "A_in e^{i(k x - w t)} + A_R e^{i(-k x - w t)}" in source_text,
    )

    coupling, inertia = sp.symbols("lambda mu", positive=True)
    potential_force, drive, spatial_rate = sp.symbols("Vprime J phi_xt")
    eliminated_time_trace = sp.simplify(
        (potential_force - drive) / coupling
        - inertia * spatial_rate / coupling**2
    )
    checks.check(
        "piston equations retain an inertial spatial-trace derivative",
        sp.simplify(
            eliminated_time_trace
            + inertia * spatial_rate / coupling**2
            - (potential_force - drive) / coupling
        )
        == 0
        and spatial_rate in eliminated_time_trace.free_symbols,
    )
    checks.check(
        "source solution explicitly admits inertial terms",
        "+ (inertial terms from" in solution_text
        and "inertial terms" in dossier_text,
    )
    checks.check(
        "dropping drive and potential does not create a local impedance law",
        sp.simplify(
            eliminated_time_trace.subs({potential_force: 0, drive: 0})
            + inertia * spatial_rate / coupling**2
        )
        == 0,
    )

    checks.check(
        "reciprocal impedances flip amplitude phase",
        sp.simplify(
            ledger.reciprocal_amplitude_reflection
            + ledger.amplitude_reflection
        )
        == 0,
    )
    checks.check(
        "reciprocal impedances preserve power data",
        sp.simplify(
            ledger.reciprocal_reflected_power_fraction
            - ledger.reflected_power_fraction
        )
        == 0
        and sp.simplify(
            ledger.reciprocal_absorbed_power_fraction
            - ledger.absorbed_power_fraction
        )
        == 0,
    )
    checks.check(
        "power ratios cannot identify the reciprocal boundary speed",
        sp.simplify(ledger.reciprocal_boundary_speed - boundary) != 0,
    )

    allocation = two_channel_allocation(1, ledger.reflected_power_fraction)
    checks.check(
        "declared perfect-reflection reference gives the source contrast algebra",
        sp.simplify(
            allocation.first_fraction
            - allocation.second_fraction
            - 2 * z / (z**2 + 1)
        )
        == 0,
    )
    checks.check(
        "contrast is a deterministic absorbed-fraction transform",
        ledger.contrast_as_absorbed_transform_residual == 0,
    )
    positive_channel = sp.symbols("rho", positive=True)
    equal_channels = two_channel_allocation(positive_channel, positive_channel)
    checks.check(
        "equal assigned channels give zero arithmetic contrast",
        equal_channels.first_fraction - equal_channels.second_fraction == 0,
    )
    checks.check(
        "source assigns rather than derives the perfect-reflection reference",
        "R_R = sp.Integer(1)" in source_text,
    )
    checks.check(
        "source contains no independent chiral-state or detector solver",
        not {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load)
        }.intersection(
            {"solve_ivp", "solve_bvp", "detector_response", "weak_current", "charged_state"}
        ),
    )

    wrong_sign_solution = sp.solve(
        sp.Eq(time_trace + boundary * spatial_trace, 0),
        reflected,
    )[0]
    checks.check(
        "boundary-sign mutation inverts the amplitude ratio",
        sp.simplify(
            wrong_sign_solution / incident * ledger.amplitude_reflection - 1
        )
        == 0
        and sp.simplify(wrong_sign_solution / incident - ledger.amplitude_reflection)
        != 0,
    )
    source_spatial_trace = sp.I * frequency / speed * (incident - reflected)
    double_error_solution = sp.solve(
        sp.Eq(time_trace + boundary * source_spatial_trace, 0),
        reflected,
        dict=True,
    )[0][reflected]
    checks.check(
        "W5 wave-role and boundary-sign errors cancel in amplitude algebra",
        sp.simplify(
            double_error_solution / incident - ledger.amplitude_reflection
        )
        == 0,
    )
    checks.check(
        "reference-channel mutation changes the contrast",
        sp.simplify(
            (
                two_channel_allocation(2, ledger.reflected_power_fraction).first_fraction
                - two_channel_allocation(2, ledger.reflected_power_fraction).second_fraction
            )
            - ledger.reference_contrast
        )
        != 0,
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/boundary_scattering.py"
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P150 and canonical code has no legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P150 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
