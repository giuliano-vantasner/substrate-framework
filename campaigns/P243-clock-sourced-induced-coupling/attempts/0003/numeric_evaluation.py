"""Attempt 0003 completion: unblinded numeric evaluation.

Runs only after a selection record exists with a chosen candidate
(attempt 0005 candidate E or later).  Evaluates the composed coupling
at the selected cutoff with the R_U* bracket quoted as sensitivity.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp
from substrate_framework.m5_induced_coupling import (
    massless_substrate_coupling,
    numeric_induced_shift,
)
from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P243-attempt-0003-numeric")
    here = Path(__file__).resolve().parent
    selection_path = here.parent / "0002" / "selection.json"
    if not selection_path.exists():
        print("SELECTION NOT RECORDED YET")
        return 1
    selection = json.loads(selection_path.read_text())
    if selection.get("selected_candidate") is None:
        print("SELECTION REFUTED: no cutoff candidate; numerics stay "
              "blinded until a box-independent UV length is constructed")
        return 1
    # Canonical composition modules demand exact inputs: carry the
    # measured splitting as an exact binary rational under the sqrt.
    lam_sq_exact = sp.nsimplify(float(selection["Lambda_squared"]),
                                rational=True)
    cutoff = sp.sqrt(lam_sq_exact)
    bounds = selection.get("Lambda_bounds")
    if bounds is not None:
        # Bounds already store Lambda values (not squares).
        cutoff_low = sp.nsimplify(float(bounds[0]), rational=True)
        cutoff_high = sp.nsimplify(float(bounds[1]), rational=True)
    else:
        bracket = selection.get("bracket") or {}
        cutoff_low = 1.0 / float(bracket["hi_radius"])
        cutoff_high = 1.0 / float(bracket["lo_radius"])
    Lambda = float(selection["Lambda"])
    primary = numeric_induced_shift(
        massless_count=3,
        non_minimal_coupling=sp.Integer(0),
        cutoff=cutoff,
        baseline=sp.Integer(0),
    )
    delta = float(primary["induced_shift"])
    # With baseline 0 (no bare gravity) total_inverse_newton IS the
    # induced shift: 1/G_total = Delta, so G_total = 4 pi / Lambda^2.
    inv_g_total = float(primary["total_inverse_newton"])
    g_total = 1.0 / inv_g_total

    # Closed form: Delta = 3 Lambda^2 / (12 pi) = Lambda^2 / (4 pi).
    expected_delta = Lambda**2 / (4.0 * 3.141592653589793)
    ledger.check(
        "delta_matches_closed_form",
        abs(delta - expected_delta) / expected_delta < 1e-12,
        f"Delta={delta:.6e} expected={expected_delta:.6e}",
    )
    # Purely-induced reading B=0: G_total = 4 pi / Lambda^2.
    expected_g = 4.0 * 3.141592653589793 / Lambda**2
    ledger.check(
        "g_total_purely_induced",
        abs(g_total - expected_g) / expected_g < 1e-12,
        f"G_total={g_total:.6e} expected={expected_g:.6e}",
    )
    # Species additivity mutation: N=4 moves Delta by 4/3.
    four = numeric_induced_shift(
        massless_count=4,
        non_minimal_coupling=sp.Integer(0),
        cutoff=cutoff,
        baseline=sp.Integer(0),
    )
    ratio = float(four["induced_shift"]) / delta
    ledger.check(
        "count_mutation_linear",
        abs(ratio - 4.0 / 3.0) < 1e-12,
        f"Delta(N=4)/Delta(N=3)={ratio:.12f}",
    )
    # Declared sensitivity band across the R_U* measurement bracket:
    # Delta scales as Lambda^2, so the bracket ends bound the shift.
    band_hi = numeric_induced_shift(
        massless_count=3,
        non_minimal_coupling=sp.Integer(0),
        cutoff=cutoff_high,
        baseline=sp.Integer(0),
    )
    band_lo = numeric_induced_shift(
        massless_count=3,
        non_minimal_coupling=sp.Integer(0),
        cutoff=cutoff_low,
        baseline=sp.Integer(0),
    )
    band_ratio_hi = float(band_hi["induced_shift"]) / delta
    band_ratio_lo = float(band_lo["induced_shift"]) / delta
    ledger.check(
        "sensitivity_band_recorded",
        0.5 < band_ratio_lo < 2.0 and 0.5 < band_ratio_hi < 2.0
        and min(band_ratio_lo, band_ratio_hi) < 1.0
        < max(band_ratio_lo, band_ratio_hi),
        f"Delta bracket ratios=[{band_ratio_lo:.9f}, "
        f"{band_ratio_hi:.9f}]",
    )

    print(json.dumps({
        "Lambda": Lambda,
        "Lambda_bounds": [float(cutoff_low), float(cutoff_high)],
        "Delta_invG_xi0": delta,
        "G_total_B0": g_total,
        "band_ratios": [band_ratio_lo, band_ratio_hi],
    }, indent=2))
    ledger.finish()
    return 0


if __name__ == "__main__":
    sys.exit(main())
