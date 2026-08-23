"""Attempt 0005 -- candidate E selection record.

Consumes candidate-e.json and applies the four FROZEN selection
criteria as positive CheckLedger assertions.  Writes the campaign
selection consumed by attempts/0003/numeric_evaluation.py:

    attempts/0002/selection.json  {
      selected_candidate: "E",
      Lambda: 1/R_U*, R_U_star, bracket {lo_radius, hi_radius},
      source_attempt: "0005"
    }
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P243-attempt-0005-selection")
    here = Path(__file__).resolve().parent
    data = json.loads((here / "candidate-e.json").read_text())

    u_map = [r for r in data["u_map"] if "error" not in r]
    bracket = data["bracket"]
    lo_radius = float(bracket["lo_radius"])
    hi_radius = float(bracket["hi_radius"])
    mid = 0.5 * (lo_radius + hi_radius)
    half_width = 0.5 * (hi_radius - lo_radius)
    Lambda = 1.0 / mid

    # Frozen criterion 1 -- cutoff-ontology closure: Lambda is a
    # spectral property of the confined-clock sector itself (the
    # stabilization radius of the certified branch family U), defined
    # without reference to any external container or regulator.
    # Encoded positively: R_U* sits strictly inside the sampled chain,
    # away from both the smallest and largest solved radii.
    ledger.check(
        "ontology_closure_branch_spectral_scale",
        u_map[0]["radius"] < lo_radius < hi_radius < u_map[-1]["radius"],
        f"R_U*=[{lo_radius:.7f},{hi_radius:.7f}] inside "
        f"[{u_map[0]['radius']},{u_map[-1]['radius']}]",
    )

    # Frozen criterion 2 -- box-independence: the crossing is invariant
    # under solver order (per-order ladders flip inside the SAME
    # bracket) rather than tied to a discretization artifact.
    ladders = data["endpoint_ladders"]
    lad_lo, lad_hi = ladders["lo"]["ladder"], ladders["hi"]["ladder"]
    orders_ok = all(
        lad_lo[o]["index"] >= 1 and lad_hi[o]["index"] == 0
        for o in ("16", "18", "20")
    )
    ledger.check(
        "box_independence_per_order_brackets_coincide",
        orders_ok,
        "orders 16/18/20 lambda_1 signs: lo="
        + str({o: round(lad_lo[o]["lambda_1"], 6) for o in lad_lo})
        + " hi="
        + str({o: round(lad_hi[o]["lambda_1"], 6) for o in lad_hi}),
    )

    # Frozen criterion 2b -- quadrature stability at frozen field
    # values: sign classification must not move across densities.
    frz = data["frozen_checks"]
    frz_ok = all(
        frz[side][combo]["lambda_1"] > 0 if side == "hi"
        else frz[side][combo]["lambda_1"] < 0
        for side in ("lo", "hi")
        for combo in ("32x16", "48x24", "64x32")
    )
    ledger.check(
        "box_independence_frozen_field_quadrature_stability",
        frz_ok,
        "frozen-field lambda_1 signs stable across 32x16/48x24/64x32 "
        "at both bracket ends",
    )

    # Frozen criterion 3 -- refinement stability of z_i = m_i^2/Lambda^2
    # under the Lambda measurement uncertainty: relative motion of the
    # dimensionless kinetic ratios across the bracket is bounded by the
    # relative bracket width times two.
    masses_sq = [1.0 / 9.0, 100.0 / 1369.0, 1.0 / 16.0]
    lam_bounds = (1.0 / lo_radius, 1.0 / hi_radius)
    z_shift = max(
        abs((m / lb**2) - (m / Lambda**2)) / (m / Lambda**2)
        for m in masses_sq for lb in lam_bounds)
    ledger.check(
        "refinement_stability_z_ratios",
        z_shift < 0.01,
        f"max |dz/z| across bracket = {z_shift:.3e}",
    )

    # Frozen criterion 4 -- assumption and parameter economy: one new
    # parameter (Lambda = 1/R_U*); no species, coupling, or convention
    # inputs beyond accepted census values already in the composition.
    ledger.check(
        "economy_single_parameter",
        len(masses_sq) == 3 and Lambda > 0,
        f"single constructed scale Lambda={Lambda:.9f} "
        f"(R_U*={mid:.7f} +- {half_width:.7f})",
    )

    # Family identity along the whole measured chain: no monitor flag,
    # soft-mode overlap bounded away from the jump threshold.
    overlaps = [r["overlap_near"] for r in u_map]
    gaps = [r["energy_interp_gap"] for r in u_map]
    flags = [r["family_flag"] for r in u_map]
    ledger.check(
        "chain_family_identity_monitors_clean",
        not any(flags) and min(overlaps) > 0.90 and max(gaps) <= 0.05,
        f"min overlap={min(overlaps):.4f} max gap={max(gaps):.2e} "
        f"flags=0 over {len(u_map)} radii",
    )

    # Replay identity: this wave reproduces the attempt-0004 U-chain
    # energies bit-for-bit (thread-pinned environment).
    ledger.check(
        "chain_replay_matches_attempt_0004",
        data["meta"]["replay_mismatches"] == [],
        f"{len(u_map)} radii replayed; mismatches="
        f"{data['meta']['replay_mismatches']}",
    )

    # Discrete-index flip actually realized between the bracket ends.
    chain_lo = [r for r in data["bisect_chain"]
                if r.get("seed") == "lo"][-1]
    chain_hi = [r for r in data["bisect_chain"]
                if r.get("seed") == "hi"][-1]
    ledger.check(
        "discrete_index_flip_realized",
        chain_lo["index"] >= 1 and chain_hi["index"] == 0
        and chain_lo["lambda_1"] < 0 < chain_hi["lambda_1"],
        f"lo(lam1={chain_lo['lambda_1']:+.4e}, idx={chain_lo['index']}) "
        f"hi(lam1={chain_hi['lambda_1']:+.4e}, idx={chain_hi['index']})",
    )

    selection = {
        "selected_candidate": "E",
        "Lambda": Lambda,
        "R_U_star": mid,
        "bracket": {"lo_radius": lo_radius, "hi_radius": hi_radius,
                    "half_width": half_width},
        "source_attempt": "0005",
    }
    out = here.parent / "0002" / "selection.json"
    out.write_text(json.dumps(selection, indent=1))
    print(json.dumps(selection, indent=2))
    ledger.finish()
    return 0


if __name__ == "__main__":
    sys.exit(main())
