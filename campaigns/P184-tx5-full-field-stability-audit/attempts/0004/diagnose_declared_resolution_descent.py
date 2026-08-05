#!/usr/bin/env python3
"""Test direct descent at TX5's declared coarse resolution and flow count."""

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
    source = SOURCE.read_bytes()
    if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
        raise RuntimeError("TX5 source hash changed")
    tree = ast.parse(source, filename=str(SOURCE))
    allowed = [
        node
        for node in tree.body
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef))
    ]
    definitions: dict[str, object] = {}
    exec(compile(ast.Module(body=allowed, type_ignores=[]), str(SOURCE), "exec"), definitions)
    return definitions


def constrained(phi: np.ndarray, direction: np.ndarray, epsilon: float) -> np.ndarray:
    value = phi + epsilon * direction
    return value / np.linalg.norm(value, axis=0, keepdims=True)


def main() -> int:
    checks = CheckLedger("P184-TX5-DECLARED-RESOLUTION-DESCENT")
    source = load_source_definitions()
    phi, dx, _ = source["make_field"](2, 91, 6.0)
    relaxed = source["evolve"](phi, dx, 600)
    raw_direction = source["project"](
        relaxed, source["egrad"](relaxed, dx)
    )
    direction = raw_direction / np.max(np.abs(raw_direction))
    base = source["Etot"](relaxed, dx)
    rows = []
    for epsilon in (1.0e-3, 5.0e-4):
        plus = source["clamp_bdy"](constrained(relaxed, direction, epsilon))
        minus = source["clamp_bdy"](constrained(relaxed, direction, -epsilon))
        e_plus = source["Etot"](plus, dx)
        e_minus = source["Etot"](minus, dx)
        slope = (e_plus - e_minus) / (2 * epsilon)
        curve_second = (e_plus + e_minus - 2 * base) / epsilon**2
        rows.append((epsilon, e_plus, e_minus, slope, curve_second))
        print(
            f"epsilon={epsilon:.1e} Eplus={e_plus:.12f} "
            f"Eminus={e_minus:.12f} slope={slope:.8e} "
            f"second={curve_second:.8e}"
        )
    residual = source["gradnorm"](relaxed, dx)
    one_more = source["evolve"](relaxed.copy(), dx, 1)
    next_energy = source["Etot"](one_more, dx)
    print(
        f"source_gradnorm={residual:.8e} base_energy={base:.12f} "
        f"one_more_step_energy={next_energy:.12f}"
    )

    checks.check(
        "declared coarse-resolution relaxed field remains materially nonstationary",
        residual > 1.0e-2,
    )
    checks.check(
        "the source projected direction lowers its reported energy",
        all(e_plus < base for _, e_plus, _, _, _ in rows),
    )
    checks.check(
        "negative first derivative is stable under step halving",
        all(slope < 0 for _, _, _, slope, _ in rows)
        and abs(rows[0][3] - rows[1][3])
        < 1.0e-3 * max(abs(rows[1][3]), 1.0),
    )
    checks.check(
        "reversing the direction reverses the first derivative sign",
        all(
            (e_minus - e_plus) / (2 * epsilon) > 0
            for epsilon, e_plus, e_minus, _, _ in rows
        ),
    )
    checks.check(
        "one additional source flow step still lowers reported energy",
        next_energy < base,
    )
    print(
        "curve_second_values="
        + repr([second for _, _, _, _, second in rows])
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
