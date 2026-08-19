#!/usr/bin/env python3
"""Independent cylindrical REFUTE pipeline for P236.

This audit does not import the production driver, its frame builder, sector
evaluator, quadrature, or fit code.  It consumes only the relaxed rapidities
stored in the production record, reconstructs the M5 field directly, and
uses a uniform cylindrical finite-difference lattice with the exact
``2*pi*rho`` measure.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from openwave.xperiments.m5_liquid_crystal.research.sandbox_v8.m5_8_2a_4d_hamiltonian import (  # noqa: E402
    SP_PAIRS,
    TM_PAIRS,
    boost_field,
    conj,
    matmul,
)
from openwave.xperiments.m5_liquid_crystal.research.sandbox_v8.m5_8_2c1_full_evolution import (  # noqa: E402
    A_BOOST,
    B_STAR,
)
from openwave.xperiments.m5_liquid_crystal.research.sandbox_vn.m5_8_2h_omega_attractor import (  # noqa: E402
    np_commf,
)

HERE = Path(__file__).resolve().parent
EVIDENCE = HERE.parent / "evidence"
PRIMARY = EVIDENCE / "m5_96_two_clock_gem_newton.json"
OUTPUT = EVIDENCE / "m5_96_independent_audit.json"

G_TIME = 8.0
DELTA = 0.3
R_W = 3.5
RC = 0.8
RHOC = 0.8
D4 = np.diag([G_TIME, 1.0, DELTA, 0.0])
DOMAIN = 120.0
SPACING = 0.75


def central(field: np.ndarray, axis: int, spacing: float) -> np.ndarray:
    result = np.zeros_like(field)
    center = [slice(None)] * field.ndim
    plus = [slice(None)] * field.ndim
    minus = [slice(None)] * field.ndim
    center[axis] = slice(1, -1)
    plus[axis] = slice(2, None)
    minus[axis] = slice(None, -2)
    result[tuple(center)] = (
        field[tuple(plus)] - field[tuple(minus)]
    ) / (2 * spacing)
    return result


def frame(polar_angle: np.ndarray, phi: float) -> np.ndarray:
    radial = np.stack(
        [
            np.sin(polar_angle) * np.cos(phi),
            np.sin(polar_angle) * np.sin(phi),
            np.cos(polar_angle),
        ],
        axis=-1,
    )
    azimuthal = np.empty_like(radial)
    azimuthal[..., 0] = -np.sin(phi)
    azimuthal[..., 1] = np.cos(phi)
    azimuthal[..., 2] = 0.0
    polar = np.cross(azimuthal, radial)
    spatial = np.stack([radial, polar, azimuthal], axis=-1)
    result = np.zeros(spatial.shape[:-2] + (4, 4))
    result[..., 0, 0] = 1.0
    result[..., 1:4, 1:4] = spatial
    return result


def matrix_field(
    rapidity: np.ndarray, polar_angle: np.ndarray, phi: float
) -> np.ndarray:
    dressed = matmul(frame(polar_angle, phi), boost_field(rapidity, A_BOOST))
    return conj(dressed, D4)


def density(
    rapidity: np.ndarray,
    polar_angle: np.ndarray,
    radius: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    matrix = matrix_field(rapidity, polar_angle, 0.0)
    epsilon_phi = 1.0e-5
    plus = matrix_field(rapidity, polar_angle, epsilon_phi)
    minus = matrix_field(rapidity, polar_angle, -epsilon_phi)
    derivatives = (
        central(matrix, 0, SPACING),
        (plus - minus) / (2 * epsilon_phi * radius[..., None, None]),
        central(matrix, 1, SPACING),
    )
    em = np.zeros(radius.shape)
    gem = np.zeros(radius.shape)
    for i in range(3):
        for j in range(i + 1, 3):
            curvature = np_commf(derivatives[i], derivatives[j])
            em += 4.0 * sum(curvature[..., a, b] ** 2 for a, b in SP_PAIRS)
            gem -= 4.0 * sum(curvature[..., a, b] ** 2 for a, b in TM_PAIRS)
    return em, gem


def fields(
    radius: np.ndarray,
    axial: np.ndarray,
    centers: tuple[float, ...],
    ambient_rapidity: float,
) -> tuple[np.ndarray, np.ndarray]:
    polar_angle = sum(
        np.arctan2(radius, axial - center) for center in centers
    )
    weights = [
        np.exp(
            -(
                np.sqrt(radius**2 + (axial - center) ** 2) / R_W
            )
            ** 2
        )
        for center in centers
    ]
    rapidity = np.full_like(radius, ambient_rapidity)
    remaining = np.ones_like(radius)
    for weight in weights:
        rapidity += (B_STAR - ambient_rapidity) * weight * remaining
        remaining *= 1.0 - weight
    return rapidity, polar_angle


def interaction(separation: float, rapidity: float) -> dict[str, float]:
    radial_axis = np.arange(SPACING / 2, DOMAIN, SPACING)
    axial_axis = np.arange(-DOMAIN + SPACING / 2, DOMAIN, SPACING)
    radius, axial = np.meshgrid(radial_axis, axial_axis, indexing="ij")
    centers = (-separation / 2, separation / 2)
    pair = density(*fields(radius, axial, centers, rapidity), radius)
    singles = [
        density(*fields(radius, axial, (center,), rapidity), radius)
        for center in centers
    ]
    distances = [
        np.sqrt(radius**2 + (axial - center) ** 2) for center in centers
    ]
    active = np.zeros(radius.shape, dtype=bool)
    active[2:-2, 2:-2] = True
    active &= radius > RHOC
    for distance in distances:
        active &= distance > 2 * RC
    weight = 2 * np.pi * radius * SPACING**2
    return {
        "em": float(
            np.sum(
                weight[active]
                * (pair[0] - singles[0][0] - singles[1][0])[active]
            )
        ),
        "gem": float(
            np.sum(
                weight[active]
                * (pair[1] - singles[0][1] - singles[1][1])[active]
            )
        ),
    }


def fit_rows(rows: list[dict[str, float]]) -> dict[str, object]:
    distance = np.asarray([row["d"] for row in rows])
    energy = np.asarray([row["gem"] for row in rows])
    force = -np.diff(energy) / np.diff(distance)
    midpoint = 0.5 * (distance[1:] + distance[:-1])
    exponent = float(np.polyfit(np.log(midpoint), np.log(-force), 1)[0])
    design = np.stack([np.ones_like(distance), 1.0 / distance], axis=1)
    coefficient = np.linalg.lstsq(design, energy, rcond=None)[0]
    residual = energy - design @ coefficient
    alternatives = {}
    for name, basis in (("log", np.log(distance)), ("linear", distance)):
        matrix = np.stack([np.ones_like(distance), basis], axis=1)
        parameters = np.linalg.lstsq(matrix, energy, rcond=None)[0]
        alternatives[name] = float(
            np.sqrt(np.mean((energy - matrix @ parameters) ** 2))
        )
    return {
        "force": force.tolist(),
        "force_exponent": exponent,
        "Uinf": float(coefficient[0]),
        "C": float(coefficient[1]),
        "rmse": float(np.sqrt(np.mean(residual**2))),
        "alternative_rmse": alternatives,
    }


def run() -> dict[str, object]:
    primary = json.loads(PRIMARY.read_text())
    primary48 = primary["grid_refinement"]["48"]
    rows = []
    for source_row in primary48["rows"]:
        row = {
            "d": float(source_row["d"]),
            "rapidity": float(source_row["relaxation"]["rapidity"]),
        }
        row.update(interaction(row["d"], row["rapidity"]))
        rows.append(row)
        print(
            f"audit d={row['d']:g} U_gem={row['gem']:+.9f}", flush=True
        )
    fit = fit_rows(rows)
    c_relative = abs(fit["C"] - primary48["fit"]["C"]) / abs(
        primary48["fit"]["C"]
    )
    exponent_delta = abs(
        fit["force_exponent"] - primary48["force_exponent"]
    )
    doors = {
        "A_force_is_attractive": all(value < 0 for value in fit["force"]),
        "B_exponent_is_inverse_square": abs(fit["force_exponent"] + 2) < 0.1,
        "C_independent_magnitude_agrees": c_relative < 0.06,
        "D_independent_exponent_agrees": exponent_delta < 0.08,
        "E_1_over_d_beats_alternatives": fit["rmse"]
        < min(fit["alternative_rmse"].values()) / 10,
    }
    record = {
        "pipeline": "uniform cylindrical finite differences; no production imports",
        "domain": DOMAIN,
        "spacing": SPACING,
        "rows": rows,
        "fit": fit,
        "primary_C_relative_difference": c_relative,
        "primary_exponent_absolute_difference": exponent_delta,
        "refute_doors": doors,
        "all_pass": all(doors.values()),
    }
    return record


def main() -> int:
    record = run()
    if "--write" in sys.argv:
        OUTPUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    print(json.dumps(record["refute_doors"], indent=2, sort_keys=True))
    return 0 if record["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
