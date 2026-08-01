#!/usr/bin/env python3
"""Independent quadrature and convention review for P037."""

from __future__ import annotations

import numpy as np
import sympy as sp

from substrate_framework.tt_angular import (
    conditional_tt_power,
    frobenius_norm_squared,
    waveform_prefactor_for_quadrupole_convention,
)
from substrate_framework.verification import CheckLedger


def numerical_sphere_tt_norm(tensor: np.ndarray, polar_order: int, azimuth_order: int) -> float:
    """Tensor-product Gauss-Legendre/periodic quadrature of the TT norm."""

    cos_theta, weights = np.polynomial.legendre.leggauss(polar_order)
    azimuths = 2 * np.pi * np.arange(azimuth_order) / azimuth_order
    total = 0.0
    identity = np.eye(3)
    for cosine, weight in zip(cos_theta, weights):
        sine = np.sqrt(1.0 - cosine**2)
        for azimuth in azimuths:
            direction = np.array(
                [sine * np.cos(azimuth), sine * np.sin(azimuth), cosine]
            )
            projector = identity - np.outer(direction, direction)
            transverse = projector @ tensor @ projector
            tt_tensor = transverse - projector * np.trace(transverse) / 2
            total += weight * (2 * np.pi / azimuth_order) * np.sum(tt_tensor**2)
    return float(total)


def main() -> int:
    ledger = CheckLedger("P037-INDEPENDENT")
    tensor = np.array(
        [[1.25, -0.5, 0.75], [-0.5, -2.0, 0.25], [0.75, 0.25, 0.75]],
        dtype=float,
    )
    trace_free = tensor - np.eye(3) * np.trace(tensor) / 3
    expected = 8 * np.pi / 5 * np.sum(trace_free**2)
    refinements = [
        numerical_sphere_tt_norm(tensor, polar_order, 2 * polar_order)
        for polar_order in (4, 8, 16)
    ]
    errors = [abs(value - expected) for value in refinements]
    ledger.check(
        "independent sphere quadrature resolves the exact TT contraction",
        errors[-1] < 2e-12,
    )
    ledger.check(
        "quadrature refinement is stable rather than a one-mesh coincidence",
        max(errors) < 2e-12
        and max(abs(refinements[i] - refinements[-1]) for i in range(2)) < 2e-12,
    )
    ledger.check(
        "an independently shifted trace gives the same angular result",
        abs(
            numerical_sphere_tt_norm(tensor + 13 * np.eye(3), 12, 24)
            - expected
        )
        < 2e-12,
    )

    coupling = sp.symbols("G", positive=True)
    normalized = sp.diag(1, -1, 0)
    triple = 3 * normalized
    flux = 1 / (32 * sp.pi * coupling)
    normalized_power = conditional_tt_power(normalized, 2 * coupling, flux)
    converted_power = conditional_tt_power(
        triple,
        waveform_prefactor_for_quadrupole_convention(2 * coupling, 3),
        flux,
    )
    ledger.check(
        "independent rescaling preserves the waveform tensor",
        sp.simplify(2 * coupling * normalized - 2 * coupling / 3 * triple)
        == sp.zeros(3),
    )
    ledger.check(
        "the same rescaling preserves total conditional power",
        sp.simplify(normalized_power - converted_power) == 0,
    )
    ledger.check(
        "using the normalized waveform coefficient on triple Q creates a factor-nine error",
        sp.simplify(
            conditional_tt_power(triple, 2 * coupling, flux)
            - 9 * normalized_power
        )
        == 0,
    )

    time, frequency, mass, radius = sp.symbols(
        "t omega mu a", positive=True, real=True
    )
    relative = sp.Matrix(
        [radius * sp.cos(frequency * time), radius * sp.sin(frequency * time), 0]
    )
    moment = mass * (relative * relative.T - radius**2 * sp.eye(3) / 3)
    third = sp.simplify(moment.diff(time, 3))
    ledger.check(
        "direct particle differentiation gives the circular norm without a lookup formula",
        sp.trigsimp(
            frobenius_norm_squared(third)
            - 32 * mass**2 * radius**4 * frequency**6
        )
        == 0,
    )
    ledger.check(
        "the conditional circular power has the normalized thirty-two-over-five factor",
        sp.trigsimp(
            conditional_tt_power(third, 2 * coupling, flux)
            - sp.Rational(32, 5)
            * coupling
            * mass**2
            * radius**4
            * frequency**6
        )
        == 0,
    )

    ledger.check(
        "nonzero pure trace is a counterexample to zero power iff raw tensor zero",
        frobenius_norm_squared(7 * sp.eye(3)) != 0
        and conditional_tt_power(7 * sp.eye(3), 2 * coupling, flux) == 0,
    )
    count = ledger.finish()
    print(f"P037 INDEPENDENT TT NORMALIZATION REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
