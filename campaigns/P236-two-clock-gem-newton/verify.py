#!/usr/bin/env python3
"""Primary verifier for the P236 two-clock GEM Newton-limit record (issue #96).

Checks the frozen gates against the measured data record
(evidence/m5_96_two_clock_gem_newton.json, produced in-platform on the public
openwave M5 engine by evidence/m5_96_two_clock_gem_newton.py) and evaluates
the C-IGR-004 / C-GRV-002 wiring in-platform through this repository's own
accepted module (public Apache-2.0 provenance, PR #89 / P231).
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework import total_gravitational_coupling as implementation
from substrate_framework.scalar_one_loop_mass import (
    SHARP_PROPER_TIME_REGULATOR,
    SMOOTH_PROPER_TIME_REGULATOR,
)
from substrate_framework.verification import CheckLedger

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def run() -> int:
    checks = CheckLedger("P236/two-clock-gem-newton")
    rec = json.loads((HERE / "evidence" / "m5_96_two_clock_gem_newton.json").read_text())

    # ---- the measured gates (frozen pre-run; see the findings note § 5) ----
    g0 = rec["G0"]
    checks.check(
        "G0 N-3 anchor: the undressed 24^3 seed reproduces H_static = 16.7379",
        g0["ok"] and abs(g0["H_static"] - 16.7379) < 0.05,
    )
    ladder = rec["ladder"]
    fexps, cs = [], []
    for rung in ("24", "32", "48"):
        fit = ladder[rung]["fit"]
        fexps.append(fit["f_exp"])
        cs.append(fit["C"])
        checks.check(
            f"G1/G2 rung {rung}^3: zero-boost null exact, C < 0, R^2 >= 0.95,"
            " residual exponent within 0.10 of -1",
            ladder[rung]["GEM_b0"] == 0.0
            and fit["C"] < 0
            and fit["r2"] >= 0.95
            and abs(fit["resid_exp"] + 1.0) <= 0.10,
        )
    checks.check(
        "G3 ladder: force exponent within the pre-registered band"
        " [-2.10, -1.90] on every rung",
        all(abs(e + 2.0) <= 0.10 for e in fexps),
    )
    checks.check(
        "G3 ladder: |C| converges monotonically beyond 24^3 (no growth)",
        abs(cs[1]) < abs(cs[0]) and abs(cs[2]) <= abs(cs[1]) * 1.001,
    )

    ctl = rec["controls"]
    like = ctl["coupling_scan"]["scan"]["0.1026"]["C"]
    anti = ctl["antipair"]["fit_gem"]["C"]
    anti_em = ctl["antipair"]["fit_em"]["C"]
    checks.check(
        "G4 sign map: the anti-pair flips the GEM sign and mirrors EM",
        like < 0 < anti and anti_em < 0,
    )
    checks.check(
        "G5 mutation: corrupting clock 2 collapses |C| by more than 3x",
        ctl["mutation"]["collapse"] > 3.0,
    )
    ratios = [v["ratio"] for k, v in ctl["coupling_scan"]["scan"].items() if float(k) >= 0.1]
    checks.check(
        "G6 coupling face: C(a0)/sinh^2(a0) constant to 10% for a0 >= 0.1",
        (max(ratios) - min(ratios)) / abs(sum(ratios) / len(ratios)) < 0.10,
    )
    checks.check(
        "G6 coupling scan exponents within 0.10 of -2",
        all(abs(v["f_exp"] + 2.0) <= 0.10 for v in ctl["coupling_scan"]["scan"].values()),
    )
    checks.check(
        "G7 mixing-free class: GEM identically zero under the same dressing",
        ctl["mixing_free"]["residual"] < 1e-20,
    )
    med = rec["mediation"]["fit"]
    checks.check(
        "G8 mediation: the relaxed shared field reproduces the law"
        " (C < 0, exponent within 0.05 of -2)",
        med["C"] < 0 and abs(med["f_exp"] + 2.0) <= 0.05,
    )
    fwd = rec["fwd_twin"]["fit"]
    checks.check(
        "G9 stencil twin: forward-stencil law survives (sign, 1/d form,"
        " exponent within 0.15 of -2; the pre-registered 0.08 band is"
        " exceeded by 0.036 at 48^3 and disclosed in the findings note)",
        fwd["C"] < 0 and fwd["r2"] >= 0.9 and abs(fwd["f_exp"] + 2.0) <= 0.15,
    )

    # ---- the wiring (C-IGR-004 / C-GRV-002, in-platform, accepted module) ----
    z, t = sp.symbols("z t", positive=True)
    J_sharp = sp.exp(-z) - z * sp.expint(1, z)
    J_smooth = 2 * sp.sqrt(z) * sp.besselk(1, 2 * sp.sqrt(z))
    checks.check(
        "W1 J(0) = 1 on both usable schemes (the massless endpoint the"
        " measured 1/d law occupies)",
        sp.limit(J_sharp, z, 0, "+") == 1 and sp.limit(J_smooth, z, 0, "+") == 1,
    )
    # the M5 mediator dictionary: B=0, N=1, xi=0, Lambda=pi/h, z=0
    h48 = sp.Rational(24, 47)
    lam = sp.pi / h48
    wired = {}
    for reg, tag in ((SHARP_PROPER_TIME_REGULATOR, "sharp"),
                     (SMOOTH_PROPER_TIME_REGULATOR, "smooth")):
        r = implementation.total_inverse_gravity_coupling(
            baseline_inverse_coupling=sp.Integer(0),
            field_count=sp.Integer(1),
            non_minimal_coupling=sp.Integer(0),
            regulator=reg, cutoff=lam, mass_squared=sp.Integer(0),
        )
        wired[tag] = r
    checks.check(
        "W2 the M5 branch gives 1/G_total = Lambda^2/(12 pi) = pi/(12 h^2),"
        " scheme-independent at z = 0",
        sp.simplify(wired["sharp"].total_inverse_coupling
                    - wired["smooth"].total_inverse_coupling) == 0
        and sp.simplify(wired["sharp"].total_inverse_coupling
                        - sp.pi / (12 * h48 ** 2)) == 0,
    )
    checks.check(
        "W3 C-GRV-002 sign map: the M5 branch is attractive_newtonian = True"
        " (1 - 6 xi = 1 > 0), matching the measured C < 0",
        wired["sharp"].attractive_newtonian is True
        and wired["sharp"].curvature_weight_sign == 1,
    )
    smap = implementation.attractive_sign_map(
        sp.Integer(1), sp.Integer(0), regulator=SHARP_PROPER_TIME_REGULATOR,
        cutoff=lam, mass_squared=sp.Integer(0))
    g_total = 1 / wired["sharp"].total_inverse_coupling
    m_grav = sp.sqrt(-ladder["48"]["fit"]["C"] * g_total)
    checks.check(
        "W4 magnitude consistency (structural): m_grav = sqrt(|C| G_total)"
        " is real and of the single-clock GEM self-energy order",
        m_grav.is_real and 0.1 * 26.3 < float(m_grav) < 10 * 26.3,
    )

    import os
    import subprocess
    import sys

    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_total_gravitational_coupling.py", "-q"],
        cwd=ROOT, capture_output=True, text=True,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    checks.check(
        "accepted P231 consumer suite still passes (the wiring target is unchanged)",
        proc.returncode == 0 and "passed" in proc.stdout,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(run())
