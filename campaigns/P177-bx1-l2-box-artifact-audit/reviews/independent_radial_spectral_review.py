#!/usr/bin/env python3
"""Independent C-PDE-012 review without importing the proposed module."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-36/"
    "bridge_BX1_l2_mode_box_artifact.py"
)
PRIOR = (
    ROOT
    / "campaigns/P054-qb3-triaxial-l2-polarizations/evidence/numerical-audit.yaml"
)


def _j2(argument: sp.Expr) -> sp.Expr:
    return sp.simplify(
        ((3 - argument**2) * sp.sin(argument) - 3 * argument * sp.cos(argument))
        / argument**3
    )


def _j2_float(argument: float) -> float:
    return float(
        ((3.0 - argument**2) * np.sin(argument) - 3.0 * argument * np.cos(argument))
        / argument**3
    )


def _lowest_tridiagonal_level(radius_value: float, intervals: int) -> float:
    spacing = radius_value / (intervals + 1)
    radius = spacing * np.arange(1, intervals + 1, dtype=np.float64)
    diagonal = 2.0 / spacing**2 + 6.0 / radius**2 + 1.0
    off_diagonal = np.full(intervals - 1, -1.0 / spacing**2)
    values = eigh_tridiagonal(
        diagonal,
        off_diagonal,
        select="i",
        select_range=(0, 0),
        eigvals_only=True,
    )
    return float(values[0])


def main() -> int:
    checks = CheckLedger("P177-INDEPENDENT-C-PDE-012")
    checks.check(
        "independent review pins the immutable BX1 source",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest()
        == "a80364df834f23b5ad006b54e7097e0a38d846405ba40408e558a8773aa74fb3",
    )

    radius = sp.symbols("r", positive=True)
    ell = sp.symbols("ell", integer=True, nonnegative=True)
    energy = sp.symbols("E", real=True)
    potential = sp.Function("V")(radius)
    chi = sp.Function("chi")(radius)
    radial = chi / radius
    original = (
        -sp.diff(radial, radius, 2)
        - 2 * sp.diff(radial, radius) / radius
        + ell * (ell + 1) * radial / radius**2
        + (potential - energy) * radial
    )
    transformed = (
        -sp.diff(chi, radius, 2)
        + (ell * (ell + 1) / radius**2 + potential - energy) * chi
    )
    checks.check(
        "fresh generic Liouville reduction closes",
        sp.simplify(radius * original - transformed) == 0,
    )
    checks.check(
        "fresh real radial norm density closes",
        sp.simplify(radius**2 * radial**2 - chi**2) == 0,
    )
    power = sp.symbols("p", integer=True)
    trial_radial = radius**power
    checks.check(
        "regular radial and transformed powers differ by one",
        sp.simplify(radius * trial_radial - radius ** (power + 1)) == 0,
    )
    wrong = chi / radius**2
    wrong_residual = sp.simplify(
        radius
        * (-sp.diff(wrong, radius, 2) - 2 * sp.diff(wrong, radius) / radius)
        + sp.diff(chi, radius, 2)
    )
    checks.check(
        "fresh wrong-power mutation retains a first derivative",
        wrong_residual != 0 and wrong_residual.has(sp.diff(chi, radius)),
    )

    argument = sp.symbols("x", positive=True)
    j2 = _j2(argument)
    checks.check(
        "closed-form spherical j2 satisfies its exact ODE",
        sp.simplify(
            argument**2 * sp.diff(j2, argument, 2)
            + 2 * argument * sp.diff(j2, argument)
            + (argument**2 - 6) * j2
        )
        == 0,
    )
    zero = float(brentq(_j2_float, 5.0, 6.5, xtol=1.0e-13))
    checks.check(
        "fresh closed-form bracket gives the first positive l2 zero",
        abs(zero - 5.76345919689455) < 2.0e-13
        and abs(_j2_float(zero)) < 2.0e-16,
    )
    wall, threshold = sp.symbols("R mu2", positive=True)
    zero_symbol = sp.symbols("z", positive=True)
    wavenumber = zero_symbol / wall
    profile = _j2(wavenumber * radius)
    radial_residual = sp.simplify(
        -sp.diff(profile, radius, 2)
        - 2 * sp.diff(profile, radius) / radius
        + 6 * profile / radius**2
        - wavenumber**2 * profile
    )
    checks.check(
        "fresh j2 ball profile solves the radial operator",
        radial_residual == 0,
    )
    checks.check(
        "fresh root enforces the outer wall independently",
        abs(
            float(
                sp.N(
                    profile.subs(
                        {radius: sp.Integer(40), wall: sp.Integer(40), zero_symbol: zero}
                    ),
                    17,
                )
            )
        )
        < 2.0e-16,
    )
    level = threshold + (zero_symbol / wall) ** 2
    checks.check(
        "fresh vacuum level has exact inverse-wall-square gap",
        sp.simplify(
            (level - threshold)
            / (level.subs(wall, 2 * wall) - threshold)
            - 4
        )
        == 0,
    )
    wrong_centrifugal = sp.simplify(radial_residual - profile / radius**2)
    checks.check(
        "fresh wrong-centrifugal mutation breaks the vacuum equation",
        wrong_centrifugal != 0,
    )

    exact_r20 = 1.0 + (zero / 20.0) ** 2
    coarse_r20 = _lowest_tridiagonal_level(20.0, 2000)
    fine_r20 = _lowest_tridiagonal_level(20.0, 4000)
    checks.check(
        "independent tridiagonal route refines to the soluble R20 level",
        abs(coarse_r20 - exact_r20) / abs(fine_r20 - exact_r20) > 3.9
        and abs(fine_r20 - exact_r20) < 6.0e-9,
    )
    fine_r40 = _lowest_tridiagonal_level(40.0, 4000)
    checks.check(
        "independent wall doubling quarters only the threshold gap",
        abs((fine_r20 - 1.0) / (fine_r40 - 1.0) - 4.0) < 2.0e-6
        and fine_r20 > 1.0
        and fine_r40 > 1.0,
    )

    test_mode = radius**3 * sp.exp(-radius)
    positive_form = sp.integrate(
        sp.diff(test_mode, radius) ** 2 + 6 * test_mode**2 / radius**2,
        (radius, 0, sp.oo),
    )
    negative_form = sp.integrate(
        sp.diff(test_mode, radius) ** 2 - test_mode**2,
        (radius, 0, sp.oo),
    )
    checks.check(
        "fresh exact positive threshold-form control is nonnegative",
        positive_form == sp.Rational(45, 8),
    )
    checks.check(
        "fresh attractive mutation reverses the trial form verdict",
        negative_form == -sp.Rational(9, 2),
    )

    peak = sp.Rational(1, 5)
    floor = sp.Rational(1, 1000)
    tolerance = sp.Rational(1, 1000)
    checks.check(
        "fresh forced-zero endpoint predicate passes arithmetically",
        peak > floor and sp.Integer(0) < tolerance * peak,
    )
    checks.check(
        "fresh unforced endpoint mutation fails the same predicate",
        not (sp.Rational(1, 50) < tolerance * peak),
    )
    checks.check(
        "the source makes the endpoint value imposed rather than observed",
        "g_vac[rc > R_mode_qb3] = 0.0" in SOURCE.read_text(encoding="utf-8"),
    )

    prior = yaml.safe_load(PRIOR.read_text(encoding="utf-8"))
    averaged = prior["converged_averaged_operator"]
    checks.check(
        "prior accepted-background evidence is above threshold and wall-filled",
        averaged["lowest_eigenvalue_at_wall_40"] > 1.0
        and averaged["outer_quarter_v_norm_fraction"] > 0.24
        and averaged["wall_30_to_40_eigenvalue_difference"] > 0.015,
    )
    checks.check(
        "prior accepted-background algebraic residual is controlled",
        averaged["relative_eigenpair_residual"] < 2.0e-10
        and averaged["mesh_error_ratio"] > 4.0,
    )
    claims = {
        claim["id"]: claim
        for claim in yaml.safe_load(
            (ROOT / "governance/claims.yaml").read_text(encoding="utf-8")
        )["claims"]
    }
    checks.check(
        "fresh review retains the averaged versus Floquet ceiling",
        "defines a different equation" in claims["C-PDE-009"]["statement"]
        and "separate Floquet argument" in claims["C-PDE-009"]["statement"],
    )
    checks.check(
        "fresh review imports no proposed implementation",
        ("radial_spectral_" + "classification")
        not in Path(__file__).read_text(encoding="utf-8"),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
