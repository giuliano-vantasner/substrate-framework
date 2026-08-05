#!/usr/bin/env python3
"""Evaluate a direct descent direction using definitions from hash-pinned TX5."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import numpy as np

from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-40/"
    "bridge_TX5_full_field_stability.py"
)
SOURCE_SHA256 = "ea12c1fee0dab254c4d8cdc984ee694622199e7cb5380674d689cf1fe6f0e31a"


def load_source_definitions() -> dict[str, object]:
    """Execute only imports and function definitions from the pinned source."""

    source = SOURCE.read_bytes()
    if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
        raise RuntimeError("TX5 source hash changed")
    tree = ast.parse(source, filename=str(SOURCE))
    allowed = tuple(
        node
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
    )
    definitions: dict[str, object] = {}
    exec(compile(ast.Module(body=list(allowed), type_ignores=[]), str(SOURCE), "exec"), definitions)
    return definitions


def normalized_curve(phi: np.ndarray, direction: np.ndarray, epsilon: float) -> np.ndarray:
    value = phi + epsilon * direction
    return value / np.linalg.norm(value, axis=0, keepdims=True)


def main() -> int:
    checks = CheckLedger("P184-TX5-STATIONARITY")
    source = load_source_definitions()
    make_field = source["make_field"]
    evolve = source["evolve"]
    project = source["project"]
    egrad = source["egrad"]
    clamp_bdy = source["clamp_bdy"]
    etot = source["Etot"]
    gradnorm = source["gradnorm"]

    phi, dx, _ = make_field(2, 41, 6.0)
    relaxed = evolve(phi, dx, 100)
    direction = project(relaxed, egrad(relaxed, dx))
    direction = direction / np.max(np.abs(direction))
    base_energy = etot(relaxed, dx)
    rows = []
    for epsilon in (1.0e-3, 5.0e-4):
        plus = clamp_bdy(normalized_curve(relaxed, direction, epsilon))
        minus = clamp_bdy(normalized_curve(relaxed, direction, -epsilon))
        e_plus = etot(plus, dx)
        e_minus = etot(minus, dx)
        slope = (e_plus - e_minus) / (2 * epsilon)
        curve_second = (e_plus + e_minus - 2 * base_energy) / epsilon**2
        rows.append((epsilon, e_plus, e_minus, slope, curve_second))
        print(
            f"epsilon={epsilon:.1e} Eplus={e_plus:.12f} "
            f"Eminus={e_minus:.12f} slope={slope:.8e} "
            f"second={curve_second:.8e}"
        )

    residual = gradnorm(relaxed, dx)
    print(f"source_gradnorm={residual:.8e} base_energy={base_energy:.12f}")
    checks.check("source-generated relaxed field remains nonstationary", residual > 1.0e-3)
    checks.check(
        "the source-projected downhill direction lowers reported energy",
        all(e_plus < base_energy for _, e_plus, _, _, _ in rows),
    )
    checks.check(
        "the direct first derivative is negative and step stable",
        all(slope < 0 for _, _, _, slope, _ in rows)
        and abs(rows[0][3] - rows[1][3])
        < 1.0e-3 * max(abs(rows[1][3]), 1.0),
    )
    checks.check(
        "positive curve curvature can coexist with the descent slope",
        all(second > 0 for _, _, _, _, second in rows),
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
