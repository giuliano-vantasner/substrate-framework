"""Primary promotion verifier for C-GW-008 and QB4's disposition."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
import yaml

from substrate_framework.conditional_triaxial_radiation import (
    conditional_real_m2_natural_axis_waveform,
    conditional_real_m2_power,
    conditional_scaled_stf_power,
    conditional_scaled_stf_waveform,
    real_m2_triple_stf_tensor,
)
from substrate_framework.triaxial_l2 import (
    real_l2_tt_readout,
    temporal_coefficient_rank,
)
from substrate_framework.tt_angular import frobenius_norm_squared
from substrate_framework.verification import CheckLedger


SOURCE_SHA256 = "4523ad68636413bf628cd353e496c61b25af3c7f30bdf3e1e061930054fb9291"


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text())


def _hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    parser.add_argument("--source-reproduction", type=Path, required=True)
    parser.add_argument("--source-audit", type=Path, required=True)
    parser.add_argument("--time-series-audit", type=Path, required=True)
    parser.add_argument("--independent-result", type=Path, required=True)
    parser.add_argument("--migration-queue", type=Path, required=True)
    parser.add_argument("--claims", type=Path, required=True)
    arguments = parser.parse_args()

    source = arguments.source_file.read_text()
    reproduction = _load(arguments.source_reproduction)
    source_audit = _load(arguments.source_audit)
    time_series = _load(arguments.time_series_audit)
    independent = _load(arguments.independent_result)
    queue = _load(arguments.migration_queue)
    claims = _load(arguments.claims)
    entry = next(item for item in queue["units"] if item["source_unit"] == "QB4")
    claim_entry = next(
        (claim for claim in claims["claims"] if claim["id"] == "C-GW-008"),
        None,
    )
    ledger = CheckLedger("P055-QB4")

    ledger.check(
        "QB4 is the hash-pinned primary source unit",
        _hash(arguments.source_file) == SOURCE_SHA256
        and entry["sha256"] == SOURCE_SHA256
        and entry["disposition"] in {"pending_adjudication", "qualified"},
    )
    ledger.check(
        "the clean source reproduction and complete tally are preserved",
        reproduction["process_exit_code"] == 0
        and reproduction["terminal_tally"] == "ALL 5 CHECKS PASS",
    )
    ledger.check(
        "the source uses current NumPy trapezoid before its legacy fallback",
        'np.trapezoid if hasattr(np, "trapezoid") else np.trapz' in source,
    )
    ledger.check(
        "the source applies a normalized power coefficient to a triple STF tensor",
        "return 3.0 * I - delta * np.trace(I)" in source
        and "P_t = (Geff / 5.0)" in source
        and "high by exactly a factor of nine" in source_audit["static_audit"]["quadrupole_scale"],
    )

    periodic = time_series["periodic_fft"]
    line = time_series["two_omega_power"]
    ledger.check(
        "QB4's claimed common FFT period fails frequency and endpoint closure",
        periodic["omega_2_over_omega"] != round(periodic["omega_2_over_omega"])
        and periodic["nearest_integer_defect"] > 0.1
        and periodic["endpoint_tensor_relative_defect"] > 0.09
        and periodic["frequency_closure_pass"] is False
        and periodic["endpoint_pass"] is False,
    )
    ledger.check(
        "the twice-frequency bin fails its preregistered derivative-norm dominance gate",
        line["source_interior_derivative_norm_fraction"] < 0.05
        and line["source_interior_derivative_norm_fraction"]
        < line["preregistered_minimum_fraction"]
        and line["dominance_pass"] is False,
    )
    ledger.check(
        "the same-bin spectral identity is recorded as non-independent",
        time_series["same_fft_bin_identity"]["relative_difference"] < 1.0e-12
        and time_series["same_fft_bin_identity"]["independent_oracle"] is False,
    )

    coupling, distance, scale = sp.symbols("G R s", nonzero=True, real=True)
    a, b, c, d, e = sp.symbols("a b c d e", real=True)
    tensor = sp.Matrix([[a, b, c], [b, d, e], [c, e, -a - d]])
    ledger.check(
        "canonical scaled-STF power has the exact convention-safe general form",
        sp.simplify(
            conditional_scaled_stf_power(tensor, coupling, scale)
            - coupling * frobenius_norm_squared(tensor) / (5 * scale**2)
        )
        == 0,
    )
    triple = 3 * sp.diag(a, -a, 0)
    expected_triple = coupling * frobenius_norm_squared(triple) / 45
    ledger.mutation_sensitive(
        "triple-STF power rejects normalized and other wrong scale factors",
        lambda candidate: sp.simplify(
            conditional_scaled_stf_power(triple, coupling, candidate)
            - expected_triple
        )
        == 0,
        3,
        [1, sp.Rational(3, 2), 9],
    )
    normalized_wave = conditional_scaled_stf_waveform(
        sp.diag(a, -a, 0), [0, 0, 1], coupling, distance, 1, [1, 0, 0]
    )
    triple_wave = conditional_scaled_stf_waveform(
        triple, [0, 0, 1], coupling, distance, 3, [1, 0, 0]
    )
    ledger.check(
        "normalized and triple scaled-STF waveforms are convention invariant",
        normalized_wave.waveform_tensor == triple_wave.waveform_tensor,
    )

    cosine2, sine2, cosine3, sine3 = sp.symbols(
        "q_c2 q_s2 q_c3 q_s3", real=True
    )
    m2_tensor = real_m2_triple_stf_tensor(cosine3, sine3)
    m2_wave = conditional_real_m2_natural_axis_waveform(
        cosine2, sine2, coupling, distance
    )
    ledger.check(
        "real-m2 tensor and natural-axis conditional waveform have exact components",
        m2_tensor
        == sp.Matrix(
            [[cosine3, sine3, 0], [sine3, -cosine3, 0], [0, 0, 0]]
        )
        and m2_wave.conventional_plus
        == 2 * coupling * cosine2 / (3 * distance)
        and m2_wave.conventional_cross
        == 2 * coupling * sine2 / (3 * distance),
    )
    ledger.check(
        "real-m2 conditional power has the exact two-G-over-forty-five form",
        conditional_real_m2_power(cosine3, sine3, coupling)
        == 2 * coupling * (cosine3**2 + sine3**2) / 45,
    )

    fixed_readout = real_l2_tt_readout(
        sp.diag(2, -1, -1), [1, 1, 1], [0, 0, 1]
    )
    plus = fixed_readout.conventional_plus_readout
    cross = fixed_readout.conventional_cross_readout
    time = np.linspace(0.0, 2.0 * np.pi, 513, endpoint=False)
    fixed = np.column_stack(
        (float(plus) * np.cos(time), float(cross) * np.cos(time))
    )
    independent_traces = np.column_stack((np.cos(time), np.sin(time)))
    ledger.check(
        "generic nonzero coordinates of one fixed tensor remain temporal rank one",
        plus != 0 and cross != 0 and temporal_coefficient_rank(fixed) == 1,
    )
    ledger.mutation_sensitive(
        "rank two requires nonproportional traces",
        lambda candidate: temporal_coefficient_rank(candidate) == 2,
        independent_traces,
        [fixed, np.column_stack((np.cos(time), -2 * np.cos(time)))],
    )
    phase, amplitude, frequency = sp.symbols(
        "tau A omega", nonzero=True, real=True
    )
    ledger.check(
        "quadrature real-m2 comparison has constant conditional power",
        sp.trigsimp(
            conditional_real_m2_power(
                amplitude * frequency**3 * sp.sin(phase),
                -amplitude * frequency**3 * sp.cos(phase),
                coupling,
            )
            - 2 * coupling * amplitude**2 * frequency**6 / 45
        )
        == 0,
    )
    ledger.check(
        "the independent Cartesian-sphere review has a clean sensitive tally",
        independent["process_exit_code"] == 0
        and independent["terminal_tally"]
        == "ALL 23 CHECKS PASS [P055-INDEPENDENT]",
    )
    ledger.check(
        "the promoted claim has the reviewed axes and dependency closure",
        claim_entry is not None
        and claim_entry["verification"] == "symbolic_verified"
        and claim_entry["review"] == "accepted"
        and claim_entry["compatibility"] == "compatible_extension"
        and claim_entry["epistemic"] == "active"
        and set(claim_entry["dependencies"])
        == {"C-GW-001", "C-GW-002", "C-GW-007"},
    )
    if entry["disposition"] == "qualified":
        ledger.check(
            "the terminal QB4 disposition maps only the accepted exact claim",
            set(entry["accepted_claims"]) == {"C-GW-008"},
        )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
