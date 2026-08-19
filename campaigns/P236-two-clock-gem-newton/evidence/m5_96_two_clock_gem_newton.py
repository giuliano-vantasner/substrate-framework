#!/usr/bin/env python3
"""M5.96: relaxed two-clock GEM Newton-limit measurement.

This is an OpenWave drop-in driver.  It uses the public M5.8 engine, the
orthogonal M5.17 two-centre angle-superposition frame, and the guarded
M5.21.8 rigid-rapidity family.  At every separation the single shared
rapidity is minimized with both fixed-clock cores present.  The interaction
density is then formed pointwise on one common mask before integration:

    u_int = u_pair - u_single,1 - u_single,2.

The force is differenced directly from the raw energy rows.  No fitted
offset is used to determine its exponent.

Run from an OpenWave checkout after creating the repository-documented
``sandbox_v8``/``sandbox_vn`` shims:

    python m5_96_two_clock_gem_newton.py all
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar

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
    central,
    tw,
)
from openwave.xperiments.m5_liquid_crystal.research.sandbox_v8.m5_8_2cb_taichi_constrained import (  # noqa: E402
    build_grid_n,
)
from openwave.xperiments.m5_liquid_crystal.research.sandbox_vn.m5_8_2h_omega_attractor import (  # noqa: E402
    np_commf,
)

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "m5_96_two_clock_gem_newton.json"

G_TIME = 8.0
DELTA = 0.3
R_W = 3.5
RC = 0.8
RHOC = 0.8
BETA_SAT = 1.558
D4 = np.diag([G_TIME, 1.0, DELTA, 0.0])
DISTANCES = np.arange(24.0, 80.0, 8.0)
DERIVATIVE_EPSILON = 2.0e-4
BOX_RUNGS = ((24, 96.0), (32, 108.0), (48, 120.0))
GRID_RUNGS = ((24, 120.0), (32, 120.0), (48, 120.0))


def M_of(rapidity: np.ndarray, frame: np.ndarray) -> np.ndarray:
    dressed = matmul(frame, boost_field(rapidity, A_BOOST))
    return conj(dressed, D4)


def u_density(matrix: np.ndarray, spacing: float) -> np.ndarray:
    derivatives = [central(matrix, axis, spacing) for axis in range(3)]
    density = 0.0
    for i in range(3):
        for j in range(i + 1, 3):
            curvature = np_commf(derivatives[i], derivatives[j])
            density = density + 2.0 * np.einsum(
                "...ab,...ab->...", curvature, tw(curvature)
            )
    return density


def total_static(rapidity: np.ndarray, grid: dict[str, np.ndarray]) -> float:
    signed = u_density(M_of(rapidity, grid["O4"]), float(grid["h"]))
    density = signed + BETA_SAT * signed**2
    return float(np.sum(density[grid["act"]])) * float(grid["h"]) ** 3


def gate_n3_anchor() -> dict[str, float | bool]:
    grid = build_grid_n(24, 6.0)
    active = np.zeros(grid["r"].shape, dtype=bool)
    active[2:-2, 2:-2, 2:-2] = True
    grid["act"] = active & (grid["r"] > 2 * RC) & (grid["rho"] > RHOC)
    rapidity = B_STAR * np.exp(-((grid["r"] / R_W) ** 2))
    value = total_static(rapidity, grid)
    return {
        "H_static": value,
        "target": 16.7379,
        "absolute_error": abs(value - 16.7379),
        "ok": abs(value - 16.7379) < 0.05,
    }


def orthogonal_frame(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    centers: tuple[float, ...],
    charges: tuple[float, ...] | None = None,
) -> np.ndarray:
    """Orthogonal cylindrical frame; q2=0 is exactly the single frame."""
    if charges is None:
        charges = (1.0,) * len(centers)
    rho = np.sqrt(x**2 + y**2)
    polar_angle = sum(
        charge * np.arctan2(rho, z - center)
        for center, charge in zip(centers, charges)
    )
    cos_phi = x / np.maximum(rho, 1.0e-300)
    sin_phi = y / np.maximum(rho, 1.0e-300)
    radial = np.stack(
        [
            np.sin(polar_angle) * cos_phi,
            np.sin(polar_angle) * sin_phi,
            np.cos(polar_angle),
        ],
        axis=-1,
    )
    azimuthal = np.stack([-sin_phi, cos_phi, np.zeros_like(rho)], axis=-1)
    polar = np.cross(azimuthal, radial)
    spatial = np.stack([radial, polar, azimuthal], axis=-1)
    result = np.zeros(spatial.shape[:-2] + (4, 4))
    result[..., 0, 0] = 1.0
    result[..., 1:4, 1:4] = spatial
    return result


def matrix_field(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    centers: tuple[float, ...],
    ambient_rapidity: float,
    *,
    charges: tuple[float, ...] | None = None,
    core_rapidities: tuple[float, ...] | None = None,
) -> np.ndarray:
    distances = [
        np.sqrt(x**2 + y**2 + (z - center) ** 2) for center in centers
    ]
    weights = [np.exp(-((distance / R_W) ** 2)) for distance in distances]
    if core_rapidities is None:
        core_rapidities = (B_STAR,) * len(centers)
    rapidity = np.full_like(x, ambient_rapidity, dtype=float)
    remaining = np.ones_like(x, dtype=float)
    for weight, core_rapidity in zip(weights, core_rapidities):
        rapidity += (core_rapidity - ambient_rapidity) * weight * remaining
        remaining *= 1.0 - weight
    return M_of(rapidity, orthogonal_frame(x, y, z, centers, charges))


def sector_density(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    centers: tuple[float, ...],
    ambient_rapidity: float,
    *,
    charges: tuple[float, ...] | None = None,
    core_rapidities: tuple[float, ...] | None = None,
    epsilon: float = DERIVATIVE_EPSILON,
) -> tuple[np.ndarray, np.ndarray]:
    coordinates = [x, y, z]
    derivatives = []
    for axis in range(3):
        plus = list(coordinates)
        minus = list(coordinates)
        plus[axis] = plus[axis] + epsilon
        minus[axis] = minus[axis] - epsilon
        derivatives.append(
            (
                matrix_field(
                    *plus,
                    centers,
                    ambient_rapidity,
                    charges=charges,
                    core_rapidities=core_rapidities,
                )
                - matrix_field(
                    *minus,
                    centers,
                    ambient_rapidity,
                    charges=charges,
                    core_rapidities=core_rapidities,
                )
            )
            / (2 * epsilon)
        )
    em = np.zeros_like(x)
    gem = np.zeros_like(x)
    for i in range(3):
        for j in range(i + 1, 3):
            curvature = np_commf(derivatives[i], derivatives[j])
            em += 4.0 * sum(curvature[..., a, b] ** 2 for a, b in SP_PAIRS)
            gem -= 4.0 * sum(curvature[..., a, b] ** 2 for a, b in TM_PAIRS)
    return em, gem


def composite_nodes(
    total: int, boundaries: list[float]
) -> tuple[np.ndarray, np.ndarray, list[int]]:
    edges = np.asarray(boundaries, dtype=float)
    widths = np.diff(edges)
    counts = np.full(len(widths), total // len(widths), dtype=int)
    remainder = total - int(np.sum(counts))
    if remainder:
        for index in np.argsort(widths)[-remainder:]:
            counts[index] += 1
    nodes, weights = [], []
    for left, right, count in zip(edges[:-1], edges[1:], counts):
        local_x, local_w = np.polynomial.legendre.leggauss(int(count))
        nodes.append(0.5 * (right - left) * local_x + 0.5 * (right + left))
        weights.append(0.5 * (right - left) * local_w)
    return np.concatenate(nodes), np.concatenate(weights), counts.tolist()


def lattice(
    count: int, domain: float, separation: float
) -> dict[str, np.ndarray | list[int] | tuple[float, float]]:
    transverse_edges = [
        -domain,
        -32.0,
        -8.0,
        -2.0,
        0.0,
        2.0,
        8.0,
        32.0,
        domain,
    ]
    z1, z2 = -separation / 2, separation / 2
    axial_edges = sorted(
        set(
            [
                -domain,
                z1 - 8.0,
                z1 - 2.0,
                z1 + 2.0,
                z1 + 8.0,
                z2 - 8.0,
                z2 - 2.0,
                z2 + 2.0,
                z2 + 8.0,
                domain,
            ]
        )
    )
    x, wx, cx = composite_nodes(count, transverse_edges)
    y, wy, cy = composite_nodes(count, transverse_edges)
    z, wz, cz = composite_nodes(count, axial_edges)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    W = wx[:, None, None] * wy[None, :, None] * wz[None, None, :]
    rho = np.sqrt(X**2 + Y**2)
    r1 = np.sqrt(rho**2 + (Z - z1) ** 2)
    r2 = np.sqrt(rho**2 + (Z - z2) ** 2)
    active = (rho > RHOC) & (r1 > 2 * RC) & (r2 > 2 * RC)
    return {
        "X": X,
        "Y": Y,
        "Z": Z,
        "W": W,
        "active": active,
        "centers": (z1, z2),
        "counts": {"x": cx, "y": cy, "z": cz},
    }


def pair_total(
    count: int,
    domain: float,
    separation: float,
    rapidity: float,
    *,
    charges: tuple[float, float] = (1.0, 1.0),
) -> float:
    grid = lattice(count, domain, separation)
    em, gem = sector_density(
        grid["X"],
        grid["Y"],
        grid["Z"],
        grid["centers"],
        rapidity,
        charges=charges,
    )
    signed = em + gem
    density = signed + BETA_SAT * signed**2
    active = grid["active"]
    return float(np.sum(grid["W"][active] * density[active]))


def relax_pair(
    count: int,
    domain: float,
    separation: float,
    *,
    charges: tuple[float, float] = (1.0, 1.0),
) -> dict[str, float | int | bool]:
    result = minimize_scalar(
        lambda value: pair_total(
            count, domain, separation, float(value), charges=charges
        ),
        bounds=(0.0, 0.3),
        method="bounded",
        options={"xatol": 1.0e-8, "maxiter": 100},
    )
    rapidity = float(result.x)
    energy = pair_total(count, domain, separation, rapidity, charges=charges)
    step = 1.0e-4
    minus = pair_total(
        count, domain, separation, rapidity - step, charges=charges
    )
    plus = pair_total(
        count, domain, separation, rapidity + step, charges=charges
    )
    derivative = (plus - minus) / (2 * step)
    curvature = (plus - 2 * energy + minus) / step**2
    return {
        "rapidity": rapidity,
        "energy": energy,
        "derivative": derivative,
        "curvature": curvature,
        "evaluations": int(result.nfev) + 3,
        "interior_minimum": bool(
            result.success
            and 0.0 < rapidity < 0.3
            and abs(derivative) < 5.0e-3
            and curvature > 0.0
        ),
    }


def interaction(
    count: int,
    domain: float,
    separation: float,
    rapidity: float,
    *,
    charges: tuple[float, float] = (1.0, 1.0),
    core_rapidities: tuple[float, float] | None = None,
    epsilon: float = DERIVATIVE_EPSILON,
) -> dict[str, float | dict[str, list[int]]]:
    grid = lattice(count, domain, separation)
    pair = sector_density(
        grid["X"],
        grid["Y"],
        grid["Z"],
        grid["centers"],
        rapidity,
        charges=charges,
        core_rapidities=core_rapidities,
        epsilon=epsilon,
    )
    cores = core_rapidities or (B_STAR, B_STAR)
    singles = [
        sector_density(
            grid["X"],
            grid["Y"],
            grid["Z"],
            (center,),
            rapidity,
            core_rapidities=(core,),
            epsilon=epsilon,
        )
        for center, core in zip(grid["centers"], cores)
    ]
    active = grid["active"]
    weight = grid["W"]
    em_density = pair[0] - singles[0][0] - singles[1][0]
    gem_density = pair[1] - singles[0][1] - singles[1][1]
    return {
        "em": float(np.sum(weight[active] * em_density[active])),
        "gem": float(np.sum(weight[active] * gem_density[active])),
        "counts": grid["counts"],
    }


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    distance = np.asarray([row["d"] for row in rows], dtype=float)
    energy = np.asarray([row["gem"] for row in rows], dtype=float)
    force = -np.diff(energy) / np.diff(distance)
    midpoint = 0.5 * (distance[1:] + distance[:-1])
    if not np.all(force < 0.0):
        force_exponent = float("nan")
    else:
        force_exponent = float(
            np.polyfit(np.log(midpoint), np.log(-force), 1)[0]
        )
    design = np.stack([np.ones_like(distance), 1.0 / distance], axis=1)
    offset, coefficient = np.linalg.lstsq(design, energy, rcond=None)[0]
    residual = energy - design @ np.asarray([offset, coefficient])
    total = energy - np.mean(energy)
    rmse = float(np.sqrt(np.mean(residual**2)))
    alternatives = {}
    for name, basis in (("log", np.log(distance)), ("linear", distance)):
        alternative = np.stack([np.ones_like(distance), basis], axis=1)
        parameters = np.linalg.lstsq(alternative, energy, rcond=None)[0]
        alternatives[name] = float(
            np.sqrt(np.mean((energy - alternative @ parameters) ** 2))
        )
    return {
        "force": force.tolist(),
        "midpoint": midpoint.tolist(),
        "force_exponent": force_exponent,
        "fit": {
            "Uinf": float(offset),
            "C": float(coefficient),
            "rmse": rmse,
            "r2": float(1.0 - np.sum(residual**2) / np.sum(total**2)),
        },
        "alternative_rmse": alternatives,
    }


def run_curve(
    count: int,
    domain: float,
    *,
    charges: tuple[float, float] = (1.0, 1.0),
) -> dict[str, object]:
    rows = []
    for distance in DISTANCES:
        relaxation = relax_pair(
            count, domain, float(distance), charges=charges
        )
        observable = interaction(
            count,
            domain,
            float(distance),
            float(relaxation["rapidity"]),
            charges=charges,
        )
        row = {"d": float(distance), "relaxation": relaxation, **observable}
        rows.append(row)
        print(
            f"{count}^3 D={domain:g} d={distance:g} "
            f"a={relaxation['rapidity']:.9f} U_gem={observable['gem']:+.9f}",
            flush=True,
        )
    return {"n": count, "domain": domain, "rows": rows, **summarize(rows)}


def frame_gates() -> dict[str, float | bool]:
    axis = np.linspace(-20.0, 20.0, 25)
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    rho = np.sqrt(x**2 + y**2)
    active = rho > RHOC
    pair = orthogonal_frame(x, y, z, (-8.0, 8.0))
    metric = np.einsum("...ji,...jk->...ik", pair, pair)
    orthogonality = float(np.max(np.abs(metric[active] - np.eye(4))))
    single = matrix_field(x, y, z, (0.0,), 0.085)
    q2_zero = matrix_field(
        x,
        y,
        z,
        (0.0, 11.0),
        0.085,
        charges=(1.0, 0.0),
        core_rapidities=(B_STAR, 0.085),
    )
    single_error = float(np.max(np.abs(single[active] - q2_zero[active])))
    return {
        "orthogonality_max_abs": orthogonality,
        "q2_zero_single_limit_max_abs": single_error,
        "ok": orthogonality < 1.0e-12 and single_error < 1.0e-12,
    }


def run_controls(box24: dict[str, object]) -> dict[str, object]:
    zero_rows = []
    for distance in (24.0, 48.0, 72.0):
        zero_rows.append(
            {
                "d": distance,
                **interaction(
                    24,
                    96.0,
                    distance,
                    0.0,
                    core_rapidities=(0.0, 0.0),
                ),
            }
        )
    mutation = run_curve(24, 96.0, charges=(1.0, 0.0))
    healthy_force = np.asarray(box24["force"], dtype=float)
    mutated_force = np.asarray(mutation["force"], dtype=float)
    mutation["peak_force_collapse"] = float(
        np.max(np.abs(healthy_force)) / np.max(np.abs(mutated_force))
    )
    epsilon_rows = []
    rapidities = {
        32: 0.08570724656408474,
        48: 0.08413551399491796,
    }
    for count, rapidity in rapidities.items():
        for epsilon in (1.0e-4, 2.0e-4, 5.0e-4, 1.0e-3):
            value = interaction(
                count,
                120.0,
                40.0,
                rapidity,
                epsilon=epsilon,
            )
            epsilon_rows.append(
                {"n": count, "epsilon": epsilon, "gem": value["gem"]}
            )
    return {
        "zero_boost": zero_rows,
        "source_deletion_mutation": mutation,
        "derivative_epsilon": epsilon_rows,
    }


def run_all() -> dict[str, object]:
    cache: dict[tuple[int, float], dict[str, object]] = {}
    for rung in sorted(set(BOX_RUNGS + GRID_RUNGS)):
        cache[rung] = run_curve(*rung)
    box = {str(count): cache[(count, domain)] for count, domain in BOX_RUNGS}
    grid = {str(count): cache[(count, domain)] for count, domain in GRID_RUNGS}
    record = {
        "task": "M5.96 / P236 corrected transaction",
        "source": "openwave-labs/openwave@614a223fff4ca0fa53a5c4fbc79cc5347a341d69",
        "instrument": {
            "derivative": "pointwise Cartesian central difference",
            "derivative_epsilon": DERIVATIVE_EPSILON,
            "quadrature": "composite Gauss-Legendre tensor lattice",
            "interaction_subtraction": "pointwise on common pair mask",
            "relaxation": "bounded minimization of guarded M5.21.8 shared rapidity",
            "guard": "M5.21.14 constrained smooth profile requirement",
        },
        "gates": {"N3_anchor": gate_n3_anchor(), "frame": frame_gates()},
        "box_ladder": box,
        "grid_refinement": grid,
        "controls": run_controls(box["24"]),
    }
    OUTPUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUTPUT}")
    return record


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode == "all":
        run_all()
        return 0
    if mode == "anchor":
        print(json.dumps({"N3_anchor": gate_n3_anchor(), "frame": frame_gates()}, indent=2))
        return 0
    raise SystemExit("modes: all | anchor")


if __name__ == "__main__":
    raise SystemExit(main())
