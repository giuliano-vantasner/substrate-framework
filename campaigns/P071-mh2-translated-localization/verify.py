"""Primary exact and regression verifier for P071 / C-OVL-002."""

from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad

from substrate_framework.normalized_overlaps import matched_width_sech_overlap
from substrate_framework.translated_localization import (
    normalized_gaussian_overlap,
    poschl_teller_ground_ledger,
    poschl_teller_ground_state,
    poschl_teller_operator,
    poschl_sech_overlap_tail_ledger,
    reciprocal_rate_spacing_rescaling,
    sech_convolution,
    sech_overlap_tail_ledger,
    tail_spacing_ledger,
    translated_sech_overlap,
)
from substrate_framework.verification import CheckLedger


SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_MH2_overlap_hierarchy.py"
)
SOURCE_SHA256 = "0596c06fb98205f5deca9cfcd99e1442216c95925d6182788c6cb01686a161d9"


def stable_sech(value: float) -> float:
    """Evaluate sech without overflowing in large-tail quadrature."""

    tail = np.exp(-abs(value))
    return float(2.0 * tail / (1.0 + tail * tail))


def exact_source_overlaps() -> tuple[np.ndarray, np.ndarray]:
    """Reconstruct MH2's planted wells through their exact ground states."""

    kappa = float(np.sqrt(0.5 - 0.45**2))
    amplitude = 2.0 * np.sqrt(6.0) * kappa
    well = poschl_teller_ground_ledger(12, sp.Rational(7, 10), 0)
    index = float(well.index)
    normalization = float(well.normalization)

    def one(center: float) -> float:
        value, error = quad(
            lambda x: normalization**2
            * stable_sech((x - center) / 0.7) ** (2.0 * index)
            * amplitude
            * stable_sech(kappa * x),
            -60.0,
            60.0,
            epsabs=1.0e-13,
            epsrel=1.0e-12,
            limit=300,
        )
        if error > 1.0e-10:
            raise RuntimeError(f"source-overlap quadrature error {error}")
        return float(value)

    overlaps = np.asarray([one(4.0 * n) for n in range(6)])
    return overlaps, np.diff(np.log(overlaps))


def main() -> int:
    ledger = CheckLedger("P071")

    source_bytes = SOURCE.read_bytes()
    ledger.check(
        "source hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA256,
    )
    source_text = source_bytes.decode("utf-8")
    ledger.check("source plants one well per rung", "rn = n * D_SPACING" in source_text)
    ledger.check("source domain crosses Cartesian origin", "np.linspace(-6.0, Lbox" in source_text)
    ledger.check("source contains no obsolete quadrature alias", "np.trapz" not in source_text)

    for alpha, beta, offset in ((2, 1, 1), (1, 2, 2), (2, 2, 3)):
        exact = float(sp.N(sech_convolution(alpha, beta, offset), 30))
        numeric, error = quad(
            lambda z: stable_sech(z - offset) ** alpha * stable_sech(z) ** beta,
            -50.0,
            50.0,
            epsabs=1.0e-13,
            epsrel=1.0e-12,
            limit=300,
        )
        ledger.check(f"convolution {alpha},{beta},{offset} quadrature closes", error < 1.0e-10)
        ledger.check(
            f"convolution {alpha},{beta},{offset} exact value",
            abs(numeric - exact) < 2.0e-11,
        )

    reflected = sech_convolution(3, sp.Rational(3, 2), -sp.Rational(7, 5))
    ledger.check(
        "translated convolution reflection symmetry",
        reflected == sech_convolution(3, sp.Rational(3, 2), sp.Rational(7, 5)),
    )

    for power in (1, 2, sp.Rational(3, 2)):
        shifted = translated_sech_overlap(power, 1, 3, 2, 0)
        centered = matched_width_sech_overlap(power, 1, 3, 2)
        ledger.check(
            f"zero displacement closes p={power}",
            sp.simplify(shifted.normalized_overlap - centered.normalized_overlap) == 0,
        )
    ledger.check(
        "dimensionless displacement covariance",
        sp.simplify(
            translated_sech_overlap(1, 1, 2, 3, 4).normalized_overlap
            - translated_sech_overlap(1, 1, 2, 6, 2).normalized_overlap
        )
        == 0,
    )

    profile_slow = sech_overlap_tail_ledger(1, 1, 1, 1)
    ledger.check("slower profile tail selected", profile_slow.dimensionless_decay_power == 1)
    ledger.check(
        "slower profile leading coefficient derived",
        sp.simplify(
            profile_slow.normalized_leading_coefficient.rewrite(sp.gamma) - sp.pi
        )
        == 0,
    )
    mode_slow = sech_overlap_tail_ledger(sp.Rational(1, 2), 2, 1, 1)
    ledger.check("slower mode tail selected", mode_slow.dimensionless_decay_power == 1)
    equal = sech_overlap_tail_ledger(1, 2, 1, 1)
    ledger.check("equal tails carry resonance power", equal.polynomial_prefactor_power == 1)
    ledger.check("equal-tail leading coefficient", equal.normalized_leading_coefficient == 8)
    scaled_equal = []
    for offset in (12, 24):
        overlap = translated_sech_overlap(1, 2, 1, 1, offset).normalized_overlap
        scaled_equal.append(
            float(sp.N(overlap, 50) * sp.N(sp.exp(2 * offset), 50) / offset)
        )
    ledger.check(
        "equal-tail scaled limit converges",
        0.0 < 8.0 - scaled_equal[1] < 8.0 - scaled_equal[0],
    )
    ledger.check(
        "pure exponential equal-tail mutation rejected",
        scaled_equal[0] * 12.0 > 80.0,
    )

    x = sp.symbols("x", real=True)
    ground = poschl_teller_ground_ledger(2, 1, 3)
    ledger.check("Poschl index equation", sp.simplify(ground.index * (ground.index + 1) - 2) == 0)
    ledger.check("Poschl ground eigenvalue", ground.eigenvalue == -1)
    ledger.check("Poschl density tail rate", ground.density_tail_rate == 2)
    ledger.check(
        "Poschl spectrum is center independent",
        poschl_teller_ground_ledger(2, 1, -8).eigenvalue == ground.eigenvalue,
    )
    mode = poschl_teller_ground_state(x, 2, 1, 3)
    residual = poschl_teller_operator(mode, x, 2, 1, 3) - ground.eigenvalue * mode
    ledger.check("Poschl exact operator residual", sp.simplify(residual.rewrite(sp.exp)) == 0)
    mode_norm = sp.sqrt(sp.pi) * sp.gamma(ground.index) / sp.gamma(
        ground.index + sp.Rational(1, 2)
    )
    ledger.check(
        "Poschl exact L2 normalization",
        sp.simplify(ground.normalization**2 * mode_norm - 1) == 0,
    )

    source_well = poschl_teller_ground_ledger(12, sp.Rational(7, 10), 0)
    source_kappa = sp.sqrt(sp.Rational(1, 2) - sp.Rational(45, 100) ** 2)
    source_ladder = tail_spacing_ledger(source_well.density_tail_rate, source_kappa, 4)
    source_tail = poschl_sech_overlap_tail_ledger(
        12,
        sp.Rational(7, 10),
        2 * sp.sqrt(6) * source_kappa,
        source_kappa,
    )
    ledger.check(
        "MH2 mode density tail is faster than core",
        float(source_well.density_tail_rate) > float(source_kappa),
    )
    ledger.check("MH2 slower core rate selected", source_ladder.overlap_tail_rate == source_kappa)
    ledger.check("MH2 exact tail ledger selects core", source_tail.overlap_tail_rate == source_kappa)
    ledger.check("MH2 exact tail coefficient positive", float(source_tail.leading_coefficient) > 0.0)
    ledger.check(
        "MH2 conditional slope derived",
        abs(float(source_ladder.asymptotic_log_ratio) + 2.181742423) < 1.0e-9,
    )
    overlaps, log_ratios = exact_source_overlaps()
    recorded = np.asarray(
        [2.61235098, 0.608274859, 0.0696859366, 0.00786522207, 0.000887551108, 0.000100155474]
    )
    ledger.check(
        "exact ground states reproduce source overlaps",
        np.max(np.abs((overlaps - recorded) / recorded)) < 8.0e-8,
    )
    ledger.check("source overlaps strictly attenuate", bool(np.all(log_ratios < 0.0)))
    ledger.check(
        "source tail ratios converge to derived slope",
        abs(log_ratios[-1] - float(source_ladder.asymptotic_log_ratio)) < 5.0e-8,
    )
    scaled_tail = overlaps[-1] * np.exp(float(source_kappa) * 20.0)
    ledger.check(
        "source overlap reaches exact tail coefficient",
        abs(scaled_tail - float(source_tail.leading_coefficient)) < 3.0e-8,
    )
    ledger.check("source finite ladder spans three decades", overlaps[0] / overlaps[-1] > 1.0e3)

    changed_spacing = tail_spacing_ledger(source_well.density_tail_rate, source_kappa, 2)
    ledger.check(
        "spacing mutation changes hierarchy slope",
        changed_spacing.asymptotic_log_ratio != source_ladder.asymptotic_log_ratio,
    )
    changed_profile = tail_spacing_ledger(source_well.density_tail_rate, 10, 4)
    ledger.check(
        "faster-profile mutation changes selected tail",
        changed_profile.overlap_tail_rate == source_well.density_tail_rate,
    )
    rate, spacing, invariant = reciprocal_rate_spacing_rescaling(2, 3, 5)
    ledger.check("rate-spacing reciprocal direction", rate * spacing == invariant == 6)

    gaussian = normalized_gaussian_overlap(2, 3, 5, sp.symbols("R", real=True))
    ledger.check("Gaussian countermodel has quadratic log", sp.diff(sp.log(gaussian), sp.symbols("R", real=True), 2) != 0)
    gaussian_values = np.asarray(
        [float(normalized_gaussian_overlap(2, 3, 5, n)) for n in range(4)]
    )
    gaussian_log_ratios = np.diff(np.log(gaussian_values))
    ledger.check(
        "Gaussian ladder rejects constant log ratio",
        not bool(np.allclose(gaussian_log_ratios[1:], gaussian_log_ratios[1])),
    )

    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
