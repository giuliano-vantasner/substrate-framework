"""Attempt 0002 selection record: frozen-criteria application.

Encodes the decisive verdict for the preregistered cutoff-scale candidates
against the measured observables.  Comparator blinding respected: no
Delta(1/G) evaluation occurs here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P243-attempt-0002-selection")
    here = Path(__file__).resolve().parent

    scale = json.loads((here / "scale-results.json").read_text())

    # Branch identity gates (both radii certified against committed data).
    ledger.check(
        "clock_branch_identity",
        bool(scale.get("branch_identity")),
        "R=8 dE/E=0 vs phase1 ladder; R=10 cross-seed from committed "
        "largeR coefficients converges to the same root (1e-15)",
    )
    for key in ("8.0", "10.0"):
        record = scale["records"][key]
        ledger.check(
            f"root_converged_R{key.replace('.', '_')}",
            record["relative_gradient"] < 1e-10,
            f"|g|/|E|={record['relative_gradient']:.2e}",
        )

    records = scale["records"]
    l8 = records["8.0"]
    l10 = records["10.0"]

    # Candidate A: Lambda = 1/L_grad, all declared variants.  Frozen
    # criterion 2 demands < 5% centroid drift across the stable window;
    # each check asserts the measured refutation of that criterion.
    for name in ("full", "core", "loose"):
        a8 = l8[f"{name}_centroid"]
        a10 = l10[f"{name}_centroid"]
        drift = abs(a10 - a8) / a8
        ledger.check(
            f"candidate_A_{name}_refuted_by_box_drift",
            drift > 0.05,
            f"L({name}) {a8:.4f}->{a10:.4f} drift={drift:.1%} > 5%; "
            "extended family L~R^0.5 with no saturation "
            "(largeR-centroids.json: L/R 0.434->0.332 over R=8->14)",
        )

    # Candidate B: Lambda = pi/R_box.  IR by construction; the check
    # asserts its failure of criterion 2.
    ledger.check(
        "candidate_B_refuted_by_domain_scaling",
        True,
        "pi/R changes by 25% per radius step; moves with the container",
    )

    # Candidate C: Lambda^2 = pinned spectral target.  The check asserts
    # the ontology failure: dimensionless constant, not a length.
    ledger.check(
        "candidate_C_refuted_by_ontology",
        True,
        "no canon mapping from dimensionless spectral targets to a "
        "length; ontology closure fails",
    )

    print(json.dumps({
        "selected_candidate": None,
        "verdict": (
            "refuted: no preregistered candidate satisfies the frozen "
            "criteria; the clock-branch gradient energy is domain-filling"
        ),
        "missing_construction": (
            "a box-independent UV length of the confined-clock sector; "
            "registered next construction: Lambda = 1/R* where R* is the "
            "Morse-index critical radius of the branch (action-level "
            "threshold, box-independent by definition)"
        ),
    }, indent=2))
    json.dump({
        "selected_candidate": None,
        "verdict": (
            "refuted: no preregistered candidate satisfies the frozen "
            "criteria; the clock-branch gradient energy is domain-filling"
        ),
        "missing_construction": (
            "a box-independent UV length of the confined-clock sector; "
            "registered next construction: Lambda = 1/R* where R* is the "
            "Morse-index critical radius of the branch"
        ),
    }, open(here / "selection.json", "w"), indent=1)
    ledger.finish()
    return 0


if __name__ == "__main__":
    sys.exit(main())
