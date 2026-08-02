"""Primary verifier for P054's exact claim delta and QB3 disposition."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.triaxial_l2 import (
    averaged_mode_equation_defect,
    real_l2_triple_stf_tensor,
    real_l2_tt_readout,
    regular_l_mode_origin_mismatch,
    temporal_coefficient_rank,
)
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "e9626f2e4829084635386eea271d0abdd39c81dfcd6899765d2f4bffac83e0c8"


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--source-audit", type=Path, required=True)
    parser.add_argument("--numerical-audit", type=Path, required=True)
    parser.add_argument("--independent-result", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    arguments = parser.parse_args()

    source = arguments.source_file.read_text()
    reproduction = _load(arguments.source_reproduction)
    source_audit = _load(arguments.source_audit)
    numerical = _load(arguments.numerical_audit)
    independent = _load(arguments.independent_result)
    queue = _load(arguments.migration_queue)
    claims = _load(arguments.claims)
    entry = next(item for item in queue["units"] if item["source_unit"] == "QB3")
    claim_ids = {claim["id"] for claim in claims["claims"]}
    ledger = CheckLedger("P054-QB3")

    ledger.check(
        "QB3 is the hash-pinned primary source unit",
        _hash(arguments.source_file) == SOURCE_SHA256
        and entry["sha256"] == SOURCE_SHA256
        and entry["disposition"] in {"pending_adjudication", "qualified"},
    )
    ledger.check(
        "the clean source reproduction and complete tally are preserved",
        reproduction["process_exit_code"] == 0
        and reproduction["terminal_tally"] == "ALL 4 CHECKS PASS",
    )
    ledger.check(
        "the source uses the current NumPy trapezoid API before its legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source,
    )
    ledger.check(
        "the audit records the averaged-operator, origin, wall, moment, and temporal-rank defects",
        source_audit["static_audit"]["perturbation_operator"].startswith("The BVP replaces")
        and "no nonzero regular" in source_audit["static_audit"]["origin_data"]
        and "standing-wave" in source_audit["static_audit"]["outer_data"]
        and "omits the angular-gradient" in source_audit["static_audit"]["energy_density"]
        and "one source mode" in source_audit["static_audit"]["temporal_rank"],
    )

    converged = numerical["converged_averaged_operator"]
    ledger.check(
        "the corrected averaged eigenpair is converged against its residual and soluble vacuum limit",
        converged["relative_eigenpair_residual"] < 1.0e-8
        and numerical["soluble_limit"]["absolute_error"] < 5.0e-4
        and converged["mesh_error_ratio"] > 2.0,
    )
    ledger.check(
        "the averaged mode fails the preregistered localized-state gates",
        converged["lowest_eigenvalue_at_wall_40"] > converged["continuum_threshold"]
        and converged["outer_quarter_v_norm_fraction"] > 0.1
        and converged["wall_30_to_40_eigenvalue_difference"] > 2.0e-3,
    )

    h20, h2c, h2s, h1c, h1s = sp.symbols("H20 H2c H2s H1c H1s", real=True)
    tensor = real_l2_triple_stf_tensor(h20, h2c, h2s, h1c, h1s)
    expected = sp.Matrix(
        [
            [-h20 / 5 + 2 * h2c / 5, 2 * h2s / 5, 2 * h1c / 5],
            [2 * h2s / 5, -h20 / 5 - 2 * h2c / 5, 2 * h1s / 5],
            [2 * h1c / 5, 2 * h1s / 5, 2 * h20 / 5],
        ]
    )
    ledger.check(
        "the canonical real-l2 map has the complete exact triple-STF normalization",
        tensor == expected and tensor == tensor.T and sp.trace(tensor) == 0,
    )
    pure_m2 = real_l2_triple_stf_tensor(m2_cosine=h2c)
    ledger.check(
        "a nonzero pure real-m2 coefficient gives the exact triaxial eigenstructure",
        pure_m2 == sp.diag(2 * h2c / 5, -2 * h2c / 5, 0),
    )
    readout = real_l2_tt_readout(
        real_l2_triple_stf_tensor(m2_cosine=h2c, m2_sine=h2s),
        [0, 0, 1],
        [1, 0, 0],
    )
    ledger.check(
        "natural-axis TT readouts keep conventional and normalized scales distinct",
        readout.conventional_plus_readout == 2 * h2c / 5
        and readout.conventional_cross_readout == 2 * h2s / 5
        and readout.normalized_plus_coordinate == 2 * sp.sqrt(2) * h2c / 5
        and readout.normalized_cross_coordinate == 2 * sp.sqrt(2) * h2s / 5,
    )
    ledger.check(
        "the accepted P2 axial trace transfers exactly to a genuine real-m2 plus trace",
        real_l2_triple_stf_tensor(p20=h20)[2, 2]
        == real_l2_triple_stf_tensor(m2_cosine=h20)[0, 0],
    )

    amplitude, tau, mode = sp.symbols("a tau psi", real=True)
    defect = averaged_mode_equation_defect(
        amplitude * sp.cos(tau), sp.besselj(0, amplitude), mode
    )
    series = sp.expand(sp.series(defect, amplitude, 0, 4).removeO())
    ledger.mutation_sensitive(
        "full time-dependent equation rejects the averaged coefficient mutation",
        lambda value: sp.simplify(value + mode * sp.cos(2 * tau) / 4) == 0,
        series.coeff(amplitude, 2),
        [0, mode * sp.cos(2 * tau) / 4],
    )
    ledger.check(
        "QB3's BVP start fails the exact regular-origin condition",
        regular_l_mode_origin_mismatch(0, sp.Rational(1, 10_000), sp.Rational(1, 100), 2)
        == sp.Rational(1, 1_000_000),
    )

    time = np.linspace(0.0, 2.0 * np.pi, 513, endpoint=False)
    one_direction = np.column_stack((np.cos(time), 2.0 * np.cos(time)))
    two_directions = np.column_stack((np.cos(time), np.sin(time)))
    ledger.mutation_sensitive(
        "two source modes require rank-two temporal coefficients",
        lambda values: temporal_coefficient_rank(values) == 2,
        two_directions,
        [one_direction, np.column_stack((np.cos(time), np.cos(time)))],
    )
    ledger.check(
        "the independent Cartesian-Bessel review has a clean sensitive tally",
        independent["process_exit_code"] == 0
        and independent["terminal_tally"] == "ALL 22 CHECKS PASS [P054-INDEPENDENT]",
    )
    ledger.check(
        "the exact claim delta is promoted atomically or remains wholly prospective",
        {"C-PDE-009", "C-GW-007"}.issubset(claim_ids)
        or {"C-PDE-009", "C-GW-007"}.isdisjoint(claim_ids),
    )
    if entry["disposition"] == "qualified":
        ledger.check(
            "the terminal QB3 disposition maps both accepted exact claims",
            set(entry["accepted_claims"]) == {"C-PDE-009", "C-GW-007"},
        )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
