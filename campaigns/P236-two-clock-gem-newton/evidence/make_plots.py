#!/usr/bin/env python3
"""Render corrected P236 plots from raw records."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
PLOTS = HERE / "plots"
PLOTS.mkdir(exist_ok=True)
record = json.loads((HERE / "m5_96_two_clock_gem_newton.json").read_text())
audit = json.loads((HERE / "m5_96_independent_audit.json").read_text())

colors = {"24": "C0", "32": "C1", "48": "C2"}

fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.2))
for rung, color in colors.items():
    curve = record["box_ladder"][rung]
    distance = np.asarray([row["d"] for row in curve["rows"]])
    energy = np.asarray([row["gem"] for row in curve["rows"]])
    compensated = energy - curve["fit"]["Uinf"]
    axes[0].plot(
        distance,
        compensated,
        "o",
        color=color,
        label=f"{rung}$^3$: C={curve['fit']['C']:.2f}",
    )
    axes[0].plot(
        distance,
        curve["fit"]["C"] / distance,
        "-",
        color=color,
        linewidth=1,
    )
    force = -np.asarray(curve["force"])
    midpoint = np.asarray(curve["midpoint"])
    axes[1].loglog(
        midpoint,
        force,
        "o-",
        color=color,
        label=f"{rung}$^3$: p={curve['force_exponent']:.3f}",
    )
axes[0].axhline(0, color="black", linewidth=0.5)
axes[0].set(
    xlabel="separation d",
    ylabel="$U_{gem}-U_{inf}$",
    title="relaxed GEM energy: $C/d$, $C<0$",
)
axes[1].set(
    xlabel="midpoint separation",
    ylabel="$-F$",
    title="directly differenced attractive force",
)
axes[0].legend(frameon=False, fontsize=8)
axes[1].legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(PLOTS / "m5_96_ud_ladder.png", dpi=180)

fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.7))
grid_c = [record["grid_refinement"][r]["fit"]["C"] for r in ("24", "32", "48")]
box_c = [record["box_ladder"][r]["fit"]["C"] for r in ("24", "32", "48")]
axes[0].plot([24, 32, 48], box_c, "o-", label="growing box")
axes[0].plot([24, 32, 48], grid_c, "s--", label="fixed D=120")
axes[0].axhline(audit["fit"]["C"], color="C3", linestyle=":", label="cylinder audit")
axes[0].set(xlabel="lattice nodes per axis", ylabel="C", title="magnitude convergence")
axes[0].legend(frameon=False, fontsize=8)

box_p = [record["box_ladder"][r]["force_exponent"] for r in ("24", "32", "48")]
grid_p = [record["grid_refinement"][r]["force_exponent"] for r in ("24", "32", "48")]
axes[1].plot([24, 32, 48], box_p, "o-", label="growing box")
axes[1].plot([24, 32, 48], grid_p, "s--", label="fixed D=120")
axes[1].axhline(-2, color="black", linestyle=":")
axes[1].axhline(audit["fit"]["force_exponent"], color="C3", linestyle=":")
axes[1].set(xlabel="lattice nodes per axis", ylabel="force exponent", title="inverse-square convergence")

healthy = np.abs(np.asarray(record["box_ladder"]["24"]["force"]))
mutation = np.abs(
    np.asarray(record["controls"]["source_deletion_mutation"]["force"])
)
midpoint = np.asarray(record["box_ladder"]["24"]["midpoint"])
axes[2].semilogy(midpoint, healthy, "o-", label="two sources")
axes[2].semilogy(midpoint, mutation, "s--", label="clock 2 deleted")
axes[2].set(xlabel="midpoint separation", ylabel="$|F|$", title="load-bearing mutation")
axes[2].legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(PLOTS / "m5_96_controls.png", dpi=180)
print("plots written")
