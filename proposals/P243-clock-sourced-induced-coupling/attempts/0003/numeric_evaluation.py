"""Attempt 0003 completion: unblinded numeric evaluation.

Runs only after the attempt 0002 selection record exists (branch identity
and frozen-criteria verdict recorded).  Evaluates the composed coupling at
the selected cutoff with the R in [8, 10] band quoted as sensitivity.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

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
    scale = json.loads(
        (here.parent / "0002" / "scale-results.json").read_text()
    )
    primary = numeric_induced_shift(
        massless_count=3,
        non_minimal_coupling=0.0,
        cutoff=lambda_r8,
        baseline=0.0,
    )
    delta = float(primary["induced_shift"])
    g_total = float(primary["total_inverse_newton"])

    # Closed form: Delta = 3 Lambda^2 / (12 pi) = Lambda^2 / (4 pi).
    expected_delta = lambda_r8**2 / (4.0 * 3.141592653589793)
    ledger.check(
        "delta_matches_closed_form",
        abs(delta - expected_delta) / expected_delta < 1e-12,
        f"Delta={delta:.6e} expected={expected_delta:.6e}",
    )
    # Purely-induced reading B=0: G_total = 4 pi / Lambda^2.
    expected_g = 4.0 * 3.141592653589793 / lambda_r8**2
    ledger.check(
        "g_total_purely_induced",
        abs(g_total - expected_g) / expected_g < 1e-12,
        f"G_total={g_total:.6e} expected={expected_g:.6e}",
    )
    # Species additivity mutation: N=4 moves Delta by 4/3.
    four = numeric_induced_shift(
        massless_count=4,
        non_minimal_coupling=0.0,
        cutoff=lambda_r8,
        baseline=0.0,
    )
    ratio = float(four["induced_shift"]) / delta
    ledger.check(
        "count_mutation_linear",
        abs(ratio - 4.0 / 3.0) < 1e-12,
        f"Delta(N=4)/Delta(N=3)={ratio:.12f}",
    )
    # Declared sensitivity band across the stable window radii.
    band = numeric_induced_shift(
        massless_count=3,
        non_minimal_coupling=0.0,
        cutoff=lambda_r10,
        baseline=0.0,
    )
    band_ratio = float(band["induced_shift"]) / delta
    ledger.check(
        "sensitivity_band_recorded",
        0.5 < band_ratio < 2.0,
        f"Delta(Lambda_R10)/Delta(Lambda_R8)={band_ratio:.6f}",
    )

    print(json.dumps({
        "Lambda_R8": lambda_r8,
        "Lambda_R10": lambda_r10,
        "Delta_invG_xi0": delta,
        "G_total_B0": g_total,
        "band_ratio": band_ratio,
    }, indent=2))
    ledger.finish()
    return 0


if __name__ == "__main__":
    sys.exit(main())
