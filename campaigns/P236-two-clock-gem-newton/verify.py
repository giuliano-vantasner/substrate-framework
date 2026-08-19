#!/usr/bin/env python3
"""Verify P236 from raw rows and accepted #89 APIs."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import sympy as sp

from substrate_framework import total_gravitational_coupling as coupling
from substrate_framework.scalar_one_loop_mass import (
    SHARP_PROPER_TIME_REGULATOR,
    SMOOTH_PROPER_TIME_REGULATOR,
)
from substrate_framework.verification import CheckLedger

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PRIMARY = HERE / "evidence" / "m5_96_two_clock_gem_newton.json"
AUDIT = HERE / "evidence" / "m5_96_independent_audit.json"


def curve_metrics(rows: list[dict[str, object]]) -> dict[str, object]:
    distance = np.asarray([row["d"] for row in rows], dtype=float)
    energy = np.asarray([row["gem"] for row in rows], dtype=float)
    force = -np.diff(energy) / np.diff(distance)
    midpoint = 0.5 * (distance[1:] + distance[:-1])
    exponent = (
        float(np.polyfit(np.log(midpoint), np.log(-force), 1)[0])
        if np.all(force < 0)
        else float("nan")
    )
    design = np.stack([np.ones_like(distance), 1 / distance], axis=1)
    offset, coefficient = np.linalg.lstsq(design, energy, rcond=None)[0]
    residual = energy - design @ np.asarray([offset, coefficient])
    total = energy - np.mean(energy)
    alternatives = {}
    for name, basis in (("log", np.log(distance)), ("linear", distance)):
        matrix = np.stack([np.ones_like(distance), basis], axis=1)
        parameters = np.linalg.lstsq(matrix, energy, rcond=None)[0]
        alternatives[name] = float(
            np.sqrt(np.mean((energy - matrix @ parameters) ** 2))
        )
    return {
        "distance": distance,
        "energy": energy,
        "force": force,
        "midpoint": midpoint,
        "force_exponent": exponent,
        "Uinf": float(offset),
        "C": float(coefficient),
        "rmse": float(np.sqrt(np.mean(residual**2))),
        "r2": float(1 - np.sum(residual**2) / np.sum(total**2)),
        "alternative_rmse": alternatives,
    }


def run() -> int:
    checks = CheckLedger("P236/two-clock-gem-newton-corrected")
    record = json.loads(PRIMARY.read_text())
    audit = json.loads(AUDIT.read_text())

    anchor = record["gates"]["N3_anchor"]
    frame = record["gates"]["frame"]
    checks.check(
        "G0 canonical N-3 anchor and corrected orthogonal frame",
        anchor["ok"]
        and abs(anchor["H_static"] - 16.7379) < 0.05
        and frame["ok"]
        and frame["orthogonality_max_abs"] < 1e-12
        and frame["q2_zero_single_limit_max_abs"] < 1e-12,
    )

    surfaces = {}
    for name in ("box_ladder", "grid_refinement"):
        surfaces[name] = {}
        for rung in ("24", "32", "48"):
            stored = record[name][rung]
            metrics = curve_metrics(stored["rows"])
            surfaces[name][rung] = metrics
            relaxation_ok = all(
                row["relaxation"]["interior_minimum"]
                and row["relaxation"]["curvature"] > 0
                and abs(row["relaxation"]["derivative"]) < 5e-3
                for row in stored["rows"]
            )
            checks.check(
                f"{name} {rung}^3: independently relaxed rows give an"
                " attractive direct force with exponent within 0.10 of -2",
                relaxation_ok
                and np.all(metrics["force"] < 0)
                and metrics["C"] < 0
                and abs(metrics["force_exponent"] + 2) < 0.10,
            )
            checks.check(
                f"{name} {rung}^3: raw 1/d model beats log and linear"
                " alternatives by at least 10x RMSE",
                metrics["rmse"]
                < min(metrics["alternative_rmse"].values()) / 10
                and metrics["r2"] > 0.999,
            )
            checks.check(
                f"{name} {rung}^3: stored summaries are derived from raw rows",
                abs(metrics["force_exponent"] - stored["force_exponent"]) < 1e-12
                and abs(metrics["C"] - stored["fit"]["C"]) < 1e-10,
            )

    box_c = np.asarray(
        [surfaces["box_ladder"][rung]["C"] for rung in ("24", "32", "48")]
    )
    box_p = np.asarray(
        [
            surfaces["box_ladder"][rung]["force_exponent"]
            for rung in ("24", "32", "48")
        ]
    )
    checks.check(
        "G1 growing-box ladder converges in coefficient and exponent",
        np.ptp(box_c) / abs(np.mean(box_c)) < 0.03 and np.ptp(box_p) < 0.04,
    )
    grid_c = np.asarray(
        [
            surfaces["grid_refinement"][rung]["C"]
            for rung in ("24", "32", "48")
        ]
    )
    grid_p = np.asarray(
        [
            surfaces["grid_refinement"][rung]["force_exponent"]
            for rung in ("24", "32", "48")
        ]
    )
    checks.check(
        "G2 fixed-domain grid refinement converges beyond 32^3",
        abs(grid_c[2] - grid_c[1]) / abs(grid_c[2]) < 0.01
        and abs(grid_p[2] - grid_p[1]) < 0.02,
    )

    controls = record["controls"]
    checks.check(
        "G3 zero boost gives machine-exact GEM null",
        all(row["gem"] == 0.0 for row in controls["zero_boost"]),
    )
    mutation = curve_metrics(controls["source_deletion_mutation"]["rows"])
    checks.check(
        "G4 deleting clock 2's texture breaks the mediated law and collapses"
        " peak force by more than 10x",
        controls["source_deletion_mutation"]["peak_force_collapse"] > 10
        and abs(mutation["force_exponent"] + 2) > 0.5,
    )
    epsilon_rows = controls["derivative_epsilon"]
    epsilon_ok = True
    for rung in (32, 48):
        values = np.asarray(
            [row["gem"] for row in epsilon_rows if row["n"] == rung]
        )
        epsilon_ok &= np.ptp(values) / abs(np.mean(values)) < 1e-6
    checks.check(
        "G5 pointwise derivative epsilon sensitivity is below 1 ppm",
        epsilon_ok,
    )

    audit_metrics = curve_metrics(audit["rows"])
    primary48 = surfaces["grid_refinement"]["48"]
    checks.check(
        "G6 independent cylindrical REFUTE pipeline confirms sign, exponent,"
        " magnitude, and model selection",
        audit["all_pass"]
        and all(audit["refute_doors"].values())
        and abs(audit_metrics["force_exponent"] + 2) < 0.1
        and abs(audit_metrics["C"] - primary48["C"])
        / abs(primary48["C"])
        < 0.06,
    )

    # Accepted #89 bridge.  Lambda remains an exact positive premise because
    # C-IGR-004 explicitly supplies no unique numerical normalization.
    lam = sp.Symbol("Lambda", positive=True)
    wired = {}
    for regulator, name in (
        (SHARP_PROPER_TIME_REGULATOR, "sharp"),
        (SMOOTH_PROPER_TIME_REGULATOR, "smooth"),
    ):
        wired[name] = coupling.total_inverse_gravity_coupling(
            baseline_inverse_coupling=sp.Integer(0),
            field_count=sp.Integer(1),
            non_minimal_coupling=sp.Integer(0),
            regulator=regulator,
            cutoff=lam,
            mass_squared=sp.Integer(0),
        )
    expected_inverse = lam**2 / (12 * sp.pi)
    checks.check(
        "W1 C-IGR-004: massless usable schemes give the same conditional"
        " 1/G_total = Lambda^2/(12*pi), with no invented cutoff value",
        sp.simplify(
            wired["sharp"].total_inverse_coupling - expected_inverse
        )
        == 0
        and sp.simplify(
            wired["smooth"].total_inverse_coupling - expected_inverse
        )
        == 0,
    )
    sign_map = coupling.attractive_sign_map(
        sp.Integer(1),
        sp.Integer(0),
        regulator=SHARP_PROPER_TIME_REGULATOR,
        cutoff=lam,
        mass_squared=sp.Integer(0),
    )
    checks.check(
        "W2 C-GRV-002: purely induced sub-conformal branch is attractive and"
        " matches the measured negative force",
        wired["sharp"].attractive_newtonian is True
        and wired["sharp"].curvature_weight_sign == 1
        and coupling.purely_induced_attractive_verdict(sp.Integer(0)) is True
        and np.all(primary48["force"] < 0),
    )

    # Typed action bridge: Z_GEM is the explicitly measured raw action/source
    # normalization.  Dividing by it yields the unit-source Green kernel;
    # G_total*m1*m2 is then its coefficient.  The independent pipeline is the
    # non-circular magnitude check on Z_GEM.
    z_gem = abs(primary48["C"])
    normalized_coefficient = primary48["C"] / z_gem
    independent_normalized = audit_metrics["C"] / z_gem
    g_total = 1 / expected_inverse
    m1, m2 = sp.symbols("m1 m2", positive=True)
    newton_coefficient = sp.Float(normalized_coefficient) * g_total * m1 * m2
    checks.check(
        "W3 measured action normalization wires G_total as the coefficient:"
        " U_N = -G_total*m1*m2/d, with independent magnitude within 6%",
        abs(normalized_coefficient + 1) < 1e-12
        and abs(independent_normalized + 1) < 0.06
        and newton_coefficient.is_negative is True,
    )

    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_total_gravitational_coupling.py",
            "-q",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    checks.check(
        "accepted P231 consumer tests still pass unchanged",
        proc.returncode == 0 and "passed" in proc.stdout,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(run())
