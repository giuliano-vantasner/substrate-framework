#!/usr/bin/env python3
"""Exact quartic spectrum and FG2 interpretation audit."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

from substrate_framework.exact_sine_qball import exact_sine_qball_peak_amplitude
from substrate_framework.qball_fluctuations import (
    quartic_fluctuation_bound_eigenvalues,
    quartic_fluctuation_bound_modes,
    quartic_fluctuation_continuum_threshold,
    quartic_fluctuation_operator,
    quartic_fluctuation_potential,
    quartic_qball_effective_potential,
    solve_quartic_fluctuation_spectrum,
)
from substrate_framework.quartic_qball import (
    quartic_qball_inverse_width,
    quartic_qball_profile,
)
from substrate_framework.verification import CheckLedger


FG2_SHA256 = "aef0ed225fca1f12fcccb284015d97ce3faa25291f07addda24e82ebbc5ae166"


@dataclass(frozen=True)
class WellConvention:
    constant_shift: sp.Expr
    depth: sp.Expr


def run(source_file: Path) -> int:
    checks = CheckLedger("P033-FG2")
    payload = source_file.read_bytes()
    source_text = payload.decode("utf-8")
    checks.check(
        "the audited FG2 source is the hash-pinned candidate unit",
        hashlib.sha256(payload).hexdigest() == FG2_SHA256,
    )

    coordinate, field = sp.symbols("x f", real=True)
    frequency = sp.symbols("omega", positive=True)
    kappa = quartic_qball_inverse_width(frequency)
    energy_potential = quartic_qball_effective_potential(field, frequency)
    checks.check(
        "the conditional energy derivative reproduces C-QBL-001's profile ODE",
        sp.simplify(
            sp.diff(energy_potential, field)
            - (kappa**2 * field - field**3 / 12)
        )
        == 0,
    )
    background = quartic_qball_profile(coordinate, frequency)
    fluctuation_potential = quartic_fluctuation_potential(
        coordinate, frequency
    )
    checks.check(
        "the exact second variation is the depth-six Poschl-Teller well",
        sp.simplify(
            sp.diff(energy_potential, field, 2).subs(field, background)
            - fluctuation_potential
        )
        == 0
        and sp.simplify(
            fluctuation_potential
            - kappa**2
            + 6 * kappa**2 * sp.sech(kappa * coordinate) ** 2
        )
        == 0,
    )

    modes = quartic_fluctuation_bound_modes(coordinate, frequency)
    eigenvalues = quartic_fluctuation_bound_eigenvalues(frequency)
    for index, (mode, eigenvalue) in enumerate(
        zip(modes, eigenvalues, strict=True), start=1
    ):
        checks.check(
            f"exact bound eigenpair {index} satisfies the operator equation",
            sp.simplify(
                quartic_fluctuation_operator(
                    mode, coordinate, frequency
                )
                - eigenvalue * mode
            )
            == 0,
        )

    negative_mode, translation_mode = modes
    checks.check(
        "the ground mode is even and nodeless while the zero mode is odd with one node",
        sp.simplify(
            negative_mode.subs(coordinate, -coordinate) - negative_mode
        )
        == 0
        and sp.simplify(
            translation_mode.subs(coordinate, -coordinate) + translation_mode
        )
        == 0
        and negative_mode.subs(coordinate, 0) == 1
        and translation_mode.subs(coordinate, 0) == 0,
    )
    norm_coordinate = sp.symbols("y_norm", real=True)
    scaled_even = sp.sech(norm_coordinate) ** 2
    scaled_odd = sp.sech(norm_coordinate) * sp.tanh(norm_coordinate)
    checks.check(
        "both modes are square integrable and parity orthogonal",
        sp.integrate(
            scaled_even.rewrite(sp.cosh) ** 2,
            (norm_coordinate, -sp.oo, sp.oo),
        )
        == sp.Rational(4, 3)
        and sp.integrate(
            scaled_odd.rewrite(sp.exp) ** 2,
            (norm_coordinate, -sp.oo, sp.oo),
        )
        == sp.Rational(2, 3)
        and sp.integrate(
            scaled_even * scaled_odd,
            (norm_coordinate, -sp.oo, sp.oo),
        )
        == 0,
    )
    translation_ratio = sp.simplify(
        sp.diff(background, coordinate) / translation_mode
    )
    checks.check(
        "the zero eigenfunction is exactly the translation tangent",
        sp.diff(translation_ratio, coordinate) == 0
        and translation_ratio != 0,
    )
    threshold = quartic_fluctuation_continuum_threshold(frequency)
    checks.check(
        "the asymptotic potential fixes the positive continuum threshold",
        sp.limit(
            fluctuation_potential.subs(frequency, sp.Rational(1, 2)),
            coordinate,
            sp.oo,
        )
        == threshold.subs(frequency, sp.Rational(1, 2))
        and threshold == kappa**2,
    )

    scaled_coordinate = sp.symbols("y", real=True)
    test_function = sp.Function("g")(scaled_coordinate)

    def lowering(value: sp.Expr, level: int) -> sp.Expr:
        return sp.diff(value, scaled_coordinate) + level * sp.tanh(
            scaled_coordinate
        ) * value

    def raising(value: sp.Expr, level: int) -> sp.Expr:
        return -sp.diff(value, scaled_coordinate) + level * sp.tanh(
            scaled_coordinate
        ) * value

    def unshifted_operator(value: sp.Expr, level: int) -> sp.Expr:
        return -sp.diff(value, scaled_coordinate, 2) - level * (
            level + 1
        ) * sp.sech(scaled_coordinate) ** 2 * value

    checks.check(
        "factorization gives K_s=A_s_dagger*A_s-s_squared",
        sp.simplify(
            raising(lowering(test_function, 2), 2)
            - unshifted_operator(test_function, 2)
            - 4 * test_function
        )
        == 0,
    )
    checks.check(
        "the partner factorization descends from s=2 to s=1",
        sp.simplify(
            lowering(raising(test_function, 2), 2)
            - unshifted_operator(test_function, 1)
            - 4 * test_function
        )
        == 0,
    )
    checks.check(
        "the s=1 partner descends to the free nonnegative operator",
        sp.simplify(
            lowering(raising(test_function, 1), 1)
            + sp.diff(test_function, scaled_coordinate, 2)
            - test_function
        )
        == 0,
    )
    partner_ground = sp.sech(scaled_coordinate)
    lifted = sp.simplify(raising(partner_ground, 2))
    checks.check(
        "the sole s=1 bound seed lifts to the odd zero mode",
        sp.simplify(lifted / (sp.sech(scaled_coordinate) * sp.tanh(scaled_coordinate)))
        == 3,
    )
    checks.check(
        "factorization closes exactly two bound levels below the threshold",
        sp.simplify(eigenvalues[0] + 3 * kappa**2) == 0
        and eigenvalues[1] == 0
        and sp.simplify(eigenvalues[1] - eigenvalues[0]) == 3 * kappa**2
        and sp.simplify(threshold - eigenvalues[1]) == kappa**2,
    )

    coarse = solve_quartic_fluctuation_spectrum(
        sp.Rational(11, 20), points=2001
    )
    fine = solve_quartic_fluctuation_spectrum(
        sp.Rational(11, 20), points=4001
    )
    doubled_box = solve_quartic_fluctuation_spectrum(
        sp.Rational(11, 20),
        half_extent_in_widths=32.0,
        points=5335,
    )
    exact_numeric = tuple(
        float(value)
        for value in quartic_fluctuation_bound_eigenvalues(
            sp.Rational(11, 20)
        )
    )
    checks.check(
        "finite differences preserve the exact two-level count under mesh and box refinement",
        len(coarse.bound_eigenvalues) == 2
        and len(fine.bound_eigenvalues) == 2
        and len(doubled_box.bound_eigenvalues) == 2
        and max(
            abs(a - b)
            for a, b in zip(
                coarse.bound_eigenvalues,
                fine.bound_eigenvalues,
                strict=True,
            )
        )
        < 5.0e-5,
    )
    checks.check(
        "the refined numerical pair approaches the exact eigenvalues",
        max(
            abs(a - b)
            for a, b in zip(
                fine.bound_eigenvalues, exact_numeric, strict=True
            )
        )
        < 2.0e-5,
    )

    frequency_value = 0.45
    exact_sine_kappa = math.sqrt(0.5 - frequency_value**2)
    source_half_box = 28.0 / exact_sine_kappa
    source_grid = np.linspace(0.0, source_half_box, 8000)
    peak = exact_sine_qball_peak_amplitude(frequency_value)

    def exact_sine_ode(_x: float, state: np.ndarray) -> tuple[float, float]:
        return (
            float(state[1]),
            0.5 * math.sin(float(state[0]))
            - frequency_value**2 * float(state[0]),
        )

    source_background = solve_ivp(
        exact_sine_ode,
        (0.0, source_half_box),
        (peak, 0.0),
        t_eval=source_grid,
        rtol=1.0e-11,
        atol=1.0e-13,
        method="DOP853",
    )
    checks.check(
        "FG2's exact-sine background is not localized at its declared box wall",
        source_background.success
        and abs(float(source_background.y[0, -1])) > 0.25
        and float(np.min(np.abs(source_background.y[0]))) < 1.0e-5,
    )
    checks.check(
        "FG2 omits box refinement for its near-threshold third exact-sine level",
        "w_sg_2N" in source_text
        and "w_sg_box" not in source_text
        and "2.93328e-01" not in source_text,
    )

    checks.check(
        "the exact quartic spectrum contains a negative mode and a symmetry zero mode",
        eigenvalues[0].subs(frequency, sp.Rational(1, 2)) < 0
        and eigenvalues[1] == 0,
    )
    checks.check(
        "FG2 relabels Hessian eigenvalues as masses without a mass dictionary",
        "internal-mode 'masses'" in source_text
        and "m0 = -3 kappa^2" in source_text,
    )
    checks.check(
        "FG2 supplies no executable Standard-Model quantum-number map",
        "same quantum numbers" in source_text.lower()
        and "SM2" in source_text
        and "import" not in source_text.split('"""', 2)[-1].splitlines()[0],
    )
    checks.check(
        "a scalar negative/zero Hessian pair does not establish constrained Q-ball stability",
        "constrained" not in source_text.lower()
        and "charge-fixed" not in source_text.lower(),
    )

    def exact_pair_survives(candidate: object) -> bool:
        convention = candidate
        assert isinstance(convention, WellConvention)
        argument = kappa * coordinate
        potential = kappa**2 * (
            convention.constant_shift
            - convention.depth * sp.sech(argument) ** 2
        )
        trial_values = (-3 * kappa**2, sp.Integer(0))
        return all(
            sp.simplify(
                -sp.diff(mode, coordinate, 2)
                + potential * mode
                - eigenvalue * mode
            )
            == 0
            for mode, eigenvalue in zip(modes, trial_values, strict=True)
        )

    checks.mutation_sensitive(
        "well shift and depth",
        exact_pair_survives,
        WellConvention(sp.Integer(1), sp.Integer(6)),
        [
            WellConvention(sp.Integer(0), sp.Integer(6)),
            WellConvention(sp.Integer(1), sp.Integer(5)),
            WellConvention(sp.Integer(1), sp.Integer(7)),
        ],
    )

    total = checks.finish()
    print(f"P033 FG2 QUARTIC FLUCTUATION AUDIT ALL {total} CHECKS PASS")
    return total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-file", type=Path, required=True)
    args = parser.parse_args()
    run(args.source_file)


if __name__ == "__main__":
    main()
