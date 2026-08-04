#!/usr/bin/env python3
"""Exact source-aware verifier for proposed C-BER-001 and B1."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path
import subprocess
import sys

import sympy as sp

from substrate_framework.berry_holonomy import (
    closed_ray_berry_ledger,
    phase_transform_section,
    projective_loop_berry_ledger,
    projective_loop_section,
)
from substrate_framework.source_audit import audit_numpy_trapezoid_compatibility
from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN = ROOT / "campaigns/P152-b1-berry-connection-audit"
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-7/"
    "bridge_B1_disclination_berry_connection.py"
)
FROZEN = CAMPAIGN / "evidence/frozen-proposal.yaml"
REVISION = CAMPAIGN / "evidence/proposal-revision-0001.yaml"
REPRODUCTION = CAMPAIGN / "evidence/source-reproduction.yaml"
SOURCE_SHA256 = "2de4faa60ecc1f87ca356afd55c2a531a89327c3c46e4296176052113de7b0b6"
FROZEN_SHA256 = "26de0d87e687a7334616d0f06e8fd30697535c9b8a02444daf26f0ca1235a4a1"
REVISION_SHA256 = "6e795a9a8551082928d989c626fad6a3714536ee11dc79de2bef11d7ca3c7962"
REPRODUCTION_SHA256 = "a554831edcef1c4258e1872f79fa3f065a22604f63b762428ed6ad0f28467fb0"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run() -> int:
    checks = CheckLedger("P152/C-BER-001")
    source_text = SOURCE.read_text(encoding="utf-8")
    tree = ast.parse(source_text, filename=str(SOURCE))

    checks.check("pinned B1 source hash", _sha256(SOURCE) == SOURCE_SHA256)
    checks.check("initial proposal hash", _sha256(FROZEN) == FROZEN_SHA256)
    checks.check("proposal revision hash", _sha256(REVISION) == REVISION_SHA256)
    checks.check("source reproduction hash", _sha256(REPRODUCTION) == REPRODUCTION_SHA256)
    source_checks = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("eight source predicates", len(source_checks) == 8)
    checks.check(
        "one source assertion",
        sum(isinstance(node, ast.Assert) for node in ast.walk(tree)) == 1,
    )
    compatibility = audit_numpy_trapezoid_compatibility(
        source_text, filename=str(SOURCE)
    )
    checks.check(
        "B1 compatibility shape is the pinned eager legacy fallback",
        compatibility.direct_legacy_attributes == 0
        and compatibility.dynamic_legacy_getattrs == 1
        and compatibility.current_references == 1
        and compatibility.eager_legacy_default_fallbacks == 1,
    )

    native = subprocess.run(
        [sys.executable, str(SOURCE)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    native_is_compatible = native.returncode == 0 and native.stdout.rstrip().endswith(
        "ALL 8 CHECKS PASS"
    )
    native_is_version_event = (
        native.returncode != 0
        and "has no attribute 'trapz'" in native.stderr
        and native.stdout.count("  PASS") == 6
    )
    checks.check(
        "native result is either compatible or only the known NumPy version event",
        native_is_compatible or native_is_version_event,
    )
    alias_code = (
        "import numpy as np,runpy;"
        "setattr(np,'trapz',np.trapezoid);"
        f"runpy.run_path({str(SOURCE)!r},run_name='__main__')"
    )
    replay = subprocess.run(
        [sys.executable, "-c", alias_code],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    checks.check("alias-only immutable replay exits cleanly", replay.returncode == 0)
    checks.check(
        "alias-only immutable replay reaches the exact tally",
        replay.stdout.rstrip().endswith("ALL 8 CHECKS PASS"),
    )

    phi = sp.symbols("phi", real=True)
    winding = sp.symbols("k", integer=True)
    exact = projective_loop_berry_ledger(winding, phi)
    parity = (-1) ** winding
    checks.check(
        "real lift is normalized and closes as a moving projector",
        exact.real_lift.projector_is_constant is False
        and exact.real_lift.endpoint_transition == parity,
    )
    checks.check(
        "real lift carries holonomy in the endpoint transition",
        exact.real_lift.berry_connection == 0
        and exact.real_lift.bare_integral_phase == 1
        and exact.real_lift.holonomy == parity,
    )
    checks.check(
        "periodic section carries holonomy in the connection integral",
        exact.periodic_section.berry_connection == winding / 2
        and exact.periodic_section.endpoint_transition == 1
        and exact.periodic_section.bare_integral_phase == parity
        and exact.periodic_section.holonomy == parity,
    )
    checks.check(
        "real and periodic sections have the identical projector path",
        exact.real_lift.projector == exact.periodic_section.projector,
    )

    fixed = closed_ray_berry_ledger(
        sp.ImmutableMatrix([sp.exp(-sp.I * phi / 2), 0]), phi
    )
    checks.check(
        "B1 stated spinor has a constant projector",
        fixed.projector_is_constant,
    )
    checks.check(
        "B1 bare minus one is cancelled by its endpoint transition",
        fixed.berry_connection == sp.Rational(1, 2)
        and fixed.endpoint_transition == -1
        and fixed.bare_integral_phase == -1
        and fixed.holonomy == 1,
    )
    checks.check(
        "omitting the endpoint transition changes the fixed-ray verdict",
        fixed.bare_integral_phase != fixed.holonomy,
    )

    real_lift = projective_loop_section(1, phi)
    nonperiodic = closed_ray_berry_ledger(
        phase_transform_section(real_lift, phi / 4), phi
    )
    checks.check(
        "nonperiodic phase change preserves corrected holonomy",
        nonperiodic.berry_connection == -sp.Rational(1, 4)
        and nonperiodic.endpoint_transition == -sp.I
        and nonperiodic.holonomy == -1,
    )
    wrong_sign_phase = sp.simplify(
        nonperiodic.endpoint_transition
        * sp.exp(-sp.I * nonperiodic.connection_integral)
    )
    checks.check(
        "Berry-sign mutation breaks the nonperiodic-gauge verdict",
        wrong_sign_phase != nonperiodic.holonomy,
    )
    periodic = closed_ray_berry_ledger(
        phase_transform_section(real_lift, 2 * phi), phi
    )
    checks.check(
        "periodic gauge changes local A but preserves holonomy",
        periodic.berry_connection == -2
        and periodic.endpoint_transition == -1
        and periodic.holonomy == -1,
    )
    reverse = projective_loop_berry_ledger(-1, phi).periodic_section
    forward = projective_loop_berry_ledger(1, phi).periodic_section
    checks.check(
        "path reversal reverses the connection integral",
        reverse.connection_integral == -forward.connection_integral,
    )
    integer_loop = projective_loop_berry_ledger(2, phi)
    checks.check(
        "integer-strength limit has plus-one holonomy in both gauges",
        integer_loop.real_lift.holonomy == 1
        and integer_loop.periodic_section.holonomy == 1,
    )

    checks.check(
        "source fixed spinor and moving director are distinct paths",
        "psi = sp.simplify(su2_z(phi) * ket_up)" in source_text
        and "n_vec = sp.Matrix([sp.cos(theta), sp.sin(theta)])" in source_text,
    )
    checks.check(
        "source B2 exponentiates only the open-section integral",
        "holonomy_from_A = sp.simplify(sp.exp(I * loop_integral))" in source_text
        and "endpoint" not in source_text[0:source_text.index("holonomy_from_A")],
    )
    checks.check(
        "source B3 equates scalar values from separately typed constructions",
        "one_value = len({holonomy_from_A" in source_text
        and "are ONE object" in source_text,
    )
    checks.check(
        "canonical API names no physical field dictionary",
        not {
            "electromagnetic",
            "material",
            "fermion",
            "core_source",
            "field_strength",
        }.intersection(
            {
                node.id
                for node in ast.walk(
                    ast.parse(
                        (ROOT / "src/substrate_framework/berry_holonomy.py").read_text(
                            encoding="utf-8"
                        )
                    )
                )
                if isinstance(node, ast.Name)
            }
        ),
    )

    mutable_python = sorted(CAMPAIGN.rglob("*.py")) + [
        ROOT / "src/substrate_framework/berry_holonomy.py",
        ROOT / "tests/test_berry_holonomy.py",
    ]
    mutable_compatibility = [
        audit_numpy_trapezoid_compatibility(
            path.read_text(encoding="utf-8"), filename=str(path)
        )
        for path in mutable_python
    ]
    checks.check(
        "mutable P152 and canonical code has no executable legacy integration access",
        all(item.legacy_references == 0 for item in mutable_compatibility),
    )

    tally = checks.finish()
    print(f"P152 PRIMARY ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
