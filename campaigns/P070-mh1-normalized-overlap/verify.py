"""Primary exact verifier for P070 normalized whole-line overlap ledgers."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.normalized_overlaps import (
    conditional_overlap_mass_ledger,
    matched_width_sech_overlap,
    normalized_expectation_bounds,
    overlap_mass_ratio,
    quartic_bound_mode_overlap_ledger,
    reciprocal_overlap_scale_rescaling,
    sech_power_integral,
)
from substrate_framework.qball_fluctuations import (
    quartic_fluctuation_bound_eigenvalues,
)
from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_MH1_yukawa_overlap_mass_formula.py"
)
SOURCE_SHA256 = "6e32edbd129c40ed587408fa70128951f65c04f379a633414fd8202e80ca1854"


def main() -> int:
    ledger = CheckLedger("P070")
    ledger.check("hash-pinned MH1 source exists", SOURCE.is_file())
    ledger.check(
        "hash-pinned MH1 source integrity",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    ledger.check(
        "MH1 samples only three integer pure-sech powers",
        "for p in (1, 2, 3)" in source_text,
    )
    ledger.check(
        "MH1 never evaluates the accepted odd sech-times-tanh mode",
        "eta0_shape" in source_text and "tanh(kappa * x)" not in source_text,
    )
    ledger.check(
        "MH1 mass linearity check differentiates its declared product",
        "sp.diff(m_n, v) - y_ns" in source_text,
    )
    ledger.check(
        "MH1 executable has no fermion or Yukawa interaction term",
        all(token not in source_text for token in ("psi_bar", "gamma5", "L_yukawa", "fermion_field")),
    )

    exponent, kappa = sp.symbols("s kappa", positive=True)
    beta_form = sp.beta(sp.Rational(1, 2), exponent / 2) / kappa
    gamma_form = sech_power_integral(exponent, kappa)
    ledger.check(
        "sech-power integral equals the beta-substitution form",
        sp.simplify(sp.expand_func(beta_form) - gamma_form) == 0,
    )
    exact_values = {
        1: sp.pi / kappa,
        2: 2 / kappa,
        3: sp.pi / (2 * kappa),
        4: 4 / (3 * kappa),
        5: 3 * sp.pi / (8 * kappa),
    }
    for power, expected in exact_values.items():
        ledger.check(
            f"whole-line sech power {power} has its exact normalization",
            sp.simplify(sech_power_integral(power, kappa) - expected) == 0,
        )

    p, r, amplitude = sp.symbols("p r A", positive=True)
    general = matched_width_sech_overlap(p, r, amplitude, kappa)
    expected_general = amplitude * sp.gamma(p + r / 2) * sp.gamma(
        p + sp.Rational(1, 2)
    ) / (sp.gamma(p) * sp.gamma(p + r / 2 + sp.Rational(1, 2)))
    ledger.check(
        "general positive powers give the normalized gamma ratio",
        sp.simplify(general.normalized_overlap - expected_general) == 0,
    )
    ledger.check(
        "matched common width cancels from the normalized ratio",
        sp.simplify(sp.diff(general.normalized_overlap, kappa)) == 0,
    )
    ledger.mutation_sensitive(
        "general overlap oracle retains normalization amplitude and both powers",
        lambda candidate: sp.simplify(candidate - expected_general) == 0,
        general.normalized_overlap,
        [
            general.raw_overlap,
            expected_general / amplitude,
            amplitude * sech_power_integral(2 * p + r, kappa) / sech_power_integral(p, kappa),
        ],
    )
    source_expected = {
        1: sp.pi * amplitude / 4,
        2: 9 * sp.pi * amplitude / 32,
        3: 75 * sp.pi * amplitude / 256,
    }
    for power, expected in source_expected.items():
        result = matched_width_sech_overlap(power, 1, amplitude, kappa)
        ledger.check(
            f"source p={power} normalized ratio is reproduced exactly",
            sp.simplify(result.normalized_overlap - expected) == 0,
        )
    ledger.check(
        "source finite substitutions do not constitute the all-positive-p proof",
        source_text.count("overlap_sechp(p)") == 2
        and "sp.gamma" not in source_text
        and "sp.beta" not in source_text,
    )

    positive_overlap = matched_width_sech_overlap(2, 1, amplitude, kappa).normalized_overlap
    negative_overlap = matched_width_sech_overlap(2, 1, -amplitude, kappa).normalized_overlap
    ledger.check(
        "expectation sign follows the supplied multiplier amplitude",
        sp.simplify(positive_overlap + negative_overlap) == 0,
    )
    ledger.check(
        "normalized positive-profile expectation lies strictly between zero and amplitude",
        normalized_expectation_bounds(0, amplitude) == (0, amplitude)
        and sp.simplify(positive_overlap / amplitude - 9 * sp.pi / 32) == 0
        and bool(0 < 9 * sp.pi / 32 < 1),
    )
    ledger.mutation_sensitive(
        "expectation bound rejects missing normalization and wrong sign",
        lambda candidate: bool(0 < candidate.subs({amplitude: 1, kappa: 1}) < 1),
        positive_overlap,
        [
            matched_width_sech_overlap(2, 1, amplitude, kappa).raw_overlap,
            negative_overlap,
            2 * amplitude,
        ],
    )

    modes = quartic_bound_mode_overlap_ledger(amplitude, kappa)
    ledger.check(
        "actual even and odd C-QBL-003 mode norms are distinct",
        sp.simplify(modes.even_mode_norm - 4 / (3 * kappa)) == 0
        and sp.simplify(modes.odd_mode_norm - 2 / (3 * kappa)) == 0,
    )
    ledger.check(
        "actual squared-density overlaps are exact and positive for positive amplitude",
        modes.even_overlap == 9 * sp.pi * amplitude / 32
        and modes.odd_overlap == 3 * sp.pi * amplitude / 16,
    )
    ledger.check(
        "even multiplier kills the normalized even-odd cross overlap by parity",
        modes.weighted_cross_overlap == 0,
    )
    ledger.mutation_sensitive(
        "actual odd-mode oracle rejects treating it as a pure-sech p=1 mode",
        lambda candidate: sp.simplify(candidate - modes.odd_overlap) == 0,
        modes.odd_overlap,
        [
            matched_width_sech_overlap(1, 1, amplitude, kappa).normalized_overlap,
            modes.even_overlap,
            sp.Integer(0),
        ],
    )

    ledger.check(
        "same-profile even-to-odd ratio is order one and not a hierarchy",
        overlap_mass_ratio(modes.odd_overlap, modes.even_overlap) == sp.Rational(2, 3),
    )
    ledger.check(
        "independent amplitudes remain in cross-profile ratios",
        overlap_mass_ratio(
            3 * sp.pi * sp.Symbol("A1", positive=True) / 16,
            9 * sp.pi * sp.Symbol("A0", positive=True) / 32,
        )
        == 2 * sp.Symbol("A1", positive=True) / (3 * sp.Symbol("A0", positive=True)),
    )

    overlap_symbol, scale = sp.symbols("y v", positive=True)
    dimension = conditional_overlap_mass_ledger(
        overlap_symbol,
        scale,
        profile_mass_dimension=sp.Rational(1, 2),
        scale_mass_dimension=sp.Rational(1, 2),
    )
    ledger.check(
        "conditional product retains both inputs and closes dimensions only when supplied",
        dimension.mapped_mass == overlap_symbol * scale
        and dimension.mapped_mass_dimension == 1,
    )
    ledger.mutation_sensitive(
        "mass ledger rejects hidden scale and wrong dimension sum",
        lambda candidate: candidate == (overlap_symbol * scale, sp.Integer(1)),
        (dimension.mapped_mass, dimension.mapped_mass_dimension),
        [(overlap_symbol, sp.Integer(1)), (overlap_symbol * scale, sp.Rational(1, 2)), (scale, sp.Integer(1))],
    )
    rho = sp.symbols("rho", positive=True)
    rescaled_overlap, rescaled_scale, invariant = reciprocal_overlap_scale_rescaling(
        overlap_symbol, scale, rho
    )
    ledger.check(
        "reciprocal amplitude-scale rescaling leaves the declared product unidentified",
        sp.simplify(rescaled_overlap * rescaled_scale - invariant) == 0
        and invariant == overlap_symbol * scale,
    )

    negative_level, zero_level = quartic_fluctuation_bound_eigenvalues(sp.Rational(1, 2))
    ledger.check(
        "accepted Hessian levels are negative and zero rather than positive masses",
        negative_level == -sp.Rational(3, 4) and zero_level == 0,
    )
    ledger.check(
        "spectral no-go does not uniquely select one positive functional",
        positive_overlap != positive_overlap + amplitude / 10
        and bool((positive_overlap + amplitude / 10).subs({amplitude: 1, kappa: 1}) > 0),
    )

    canonical_source = Path("src/substrate_framework/normalized_overlaps.py").read_text(
        encoding="utf-8"
    )
    ledger.check(
        "canonical exact overlap module uses no NumPy quadrature alias",
        "np." + "trapz" not in canonical_source
        and "np." + "trapezoid" not in canonical_source,
    )
    invalid = []
    for operation in (
        lambda: sech_power_integral(0, 1),
        lambda: matched_width_sech_overlap(1, 0, 1, 1),
        lambda: normalized_expectation_bounds(2, 1),
        lambda: overlap_mass_ratio(1, 0),
        lambda: reciprocal_overlap_scale_rescaling(1, 1, 0),
    ):
        try:
            operation()
        except ValueError:
            invalid.append(True)
    ledger.check(
        "overlap APIs reject invalid powers bounds references and rescalings",
        invalid == [True, True, True, True, True],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
