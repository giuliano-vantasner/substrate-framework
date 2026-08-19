#!/usr/bin/env python3
"""Generate the P236 evidence plots from the measured data record."""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
rec = json.loads((HERE / "m5_96_two_clock_gem_newton.json").read_text())

# ---- panel 1: U_gem(d) with the fits, per rung + mediation + fwd twin ----
fig, ax = plt.subplots(figsize=(6.6, 4.4))
colors = {"24": "C0", "32": "C1", "48": "C2"}
for rung, c in colors.items():
    rows = rec["ladder"][rung]["rows"]
    dd = np.array([r["d"] for r in rows])
    U = np.array([r["U_gem"] for r in rows])
    fit = rec["ladder"][rung]["fit"]
    ax.plot(dd, U - fit["Uinf"], "o", color=c, label=f"{rung}$^3$: C={fit['C']:.0f}, F exp {fit['f_exp']:+.3f}")
    dd_f = np.linspace(dd.min(), dd.max(), 100)
    ax.plot(dd_f, fit["C"] / dd_f, "-", color=c, lw=1)
med = rec["mediation"]["fit"]
rows = rec["mediation"]["rows"]
dd = np.array([r[0] for r in rows]); U = np.array([r[1] for r in rows])
ax.plot(dd, U - med["Uinf"], "s", color="C3", mfc="none",
        label=f"relaxed 32$^3$ (mediated): F exp {med['f_exp']:+.3f}")
ax.plot(dd, med["C"] / dd, "--", color="C3", lw=1)
fwd = rec["fwd_twin"]["fit"]
rows = rec["fwd_twin"]["rows"]
dd = np.array([r[0] for r in rows]); U = np.array([r[1] for r in rows])
ax.plot(dd, U - fwd["Uinf"], "^", color="C4", mfc="none",
        label=f"fwd-stencil twin 48$^3$: F exp {fwd['f_exp']:+.3f}")
ax.axhline(0, color="k", lw=0.5)
ax.set(xlabel="separation d (grid units)", ylabel="U$_{gem}(d) - U_{inf}$",
       title="the two-clock GEM interaction: $U = U_\\infty + C/d$, $F = C/d^2$ (C < 0)")
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "plots" / "m5_96_ud_ladder.png", dpi=160)

# ---- panel 2: the controls ----
fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.4))
scan = rec["controls"]["coupling_scan"]["scan"]
Cs = np.array([scan[k]["C"] for k in scan.keys()])
a0s = np.array([float(k) for k in scan.keys()])
sh2 = np.sinh(a0s) ** 2
axs[0].plot(a0s, -Cs / sh2 / 1e3, "o-")
axs[0].set(xlabel="$a_0$", ylabel="$-C/\\sinh^2 a_0$ (10$^3$)",
           title="coupling face: $(b\\cdot g)^2$")
rows_like = None
axs[1].bar([0, 1, 2], [rec["controls"]["coupling_scan"]["scan"]["0.1026"]["C"],
                        rec["controls"]["antipair"]["fit_gem"]["C"],
                        rec["controls"]["mutation"]["fit"]["C"]],
           color=["C0", "C1", "C2"])
axs[1].set_xticks([0, 1, 2])
axs[1].set_xticklabels(["like pair", "anti-pair", "mutation"], fontsize=8)
axs[1].set_ylabel("C")
axs[1].set_title("sign map + mutation")
axs[1].axhline(0, color="k", lw=0.5)
fe = [rec["ladder"][k]["fit"]["f_exp"] for k in ("24", "32", "48")]
axs[2].plot([24, 32, 48], fe, "o-", label="box ladder")
axs[2].axhline(-2.0, color="r", ls="--", lw=1, label="target $-2$")
axs[2].set(xlabel="box rung $n$", ylabel="force exponent",
           title="exponent stability")
axs[2].legend(frameon=False, fontsize=8)
fig.tight_layout()
fig.savefig(HERE / "plots" / "m5_96_controls.png", dpi=160)
print("plots written")
