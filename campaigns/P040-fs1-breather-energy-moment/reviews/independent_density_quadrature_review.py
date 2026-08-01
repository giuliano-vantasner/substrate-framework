#!/usr/bin/env python3
"""Independent field-density quadrature and harmonic review for P040."""

from __future__ import annotations

import math

import numpy as np
from scipy.integrate import quad

from substrate_framework.verification import CheckLedger


ABS_TOL = 1.0e-11
REL_TOL = 1.0e-11
QUAD_LIMIT = 300


def density(x: float, time: float, omega: float, weights=(0.5, 0.5, 1.0)) -> float:
    eta = math.sqrt(1.0 - omega**2)
    hyperbolic_cosine = math.cosh(eta * x)
    hyperbolic_sine = math.sinh(eta * x)
    phase = eta * math.sin(omega * time) / omega
    denominator = hyperbolic_cosine**2 + phase**2
    field = 4.0 * math.atan(phase / hyperbolic_cosine)
    field_x = -4.0 * eta * phase * hyperbolic_sine / denominator
    field_t = (
        4.0
        * eta
        * math.cos(omega * time)
        * hyperbolic_cosine
        / denominator
    )
    time_weight, space_weight, potential_weight = weights
    return (
        time_weight * field_t**2
        + space_weight * field_x**2
        + potential_weight * (1.0 - math.cos(field))
    )


def direct_moment(
    omega: float,
    time: float,
    scaled_half_domain: float,
    weights=(0.5, 0.5, 1.0),
) -> float:
    eta = math.sqrt(1.0 - omega**2)
    half_domain = scaled_half_domain / eta
    value, error = quad(
        lambda coordinate: coordinate**2
        * density(coordinate, time, omega, weights),
        -half_domain,
        half_domain,
        epsabs=ABS_TOL,
        epsrel=REL_TOL,
        limit=QUAD_LIMIT,
    )
    if not math.isfinite(value) or not math.isfinite(error):
        raise RuntimeError("adaptive quadrature did not return finite evidence")
    return value


def exact_moment(omega: float, time: float) -> float:
    eta = math.sqrt(1.0 - omega**2)
    return (
        4.0 * math.pi**2 / (3.0 * eta)
        + 16.0
        / eta
        * math.asinh(eta * math.sin(omega * time) / omega) ** 2
    )


def main() -> int:
    ledger = CheckLedger("P040-INDEPENDENT")
    cases = [
        (0.35, 0.0),
        (0.35, 0.71),
        (1.0 / math.sqrt(2.0), 1.3),
        (0.9, 0.47),
    ]
    errors = []
    refinements = []
    for omega, time in cases:
        values = [direct_moment(omega, time, domain) for domain in (12.0, 18.0, 24.0)]
        expected = exact_moment(omega, time)
        errors.append(abs(values[-1] - expected) / expected)
        refinements.append(abs(values[-1] - values[-2]) < abs(values[-2] - values[-3]))
    ledger.check(
        "direct adaptive field-density quadrature matches the transform formula across the family",
        max(errors) < 2.0e-10,
    )
    ledger.check(
        "scaled-domain tail refinement improves for every audited case",
        all(refinements),
    )

    omega = 1.0 / math.sqrt(2.0)
    time = 1.3
    expected = exact_moment(omega, time)
    wrong_time_weight = direct_moment(omega, time, 24.0, (1.0, 0.5, 1.0))
    missing_potential = direct_moment(omega, time, 24.0, (0.5, 0.5, 0.0))
    ledger.check(
        "doubling the time-kinetic half factor breaks the exact moment",
        abs(wrong_time_weight - expected) / expected > 0.05,
    )
    ledger.check(
        "dropping the potential term breaks the exact moment",
        abs(missing_potential - expected) / expected > 0.05,
    )

    period = 2.0 * math.pi / omega
    samples = 4096
    times = np.linspace(0.0, period, samples, endpoint=False)
    moments = np.array([exact_moment(omega, value) for value in times])
    centered = moments - np.mean(moments)
    transform = np.fft.rfft(centered)
    angular_frequencies = 2.0 * math.pi * np.fft.rfftfreq(
        samples,
        times[1] - times[0],
    )
    peak_index = int(np.argmax(np.abs(transform[1:])) + 1)
    ledger.check(
        "the exact special-frequency series independently reproduces FS1's dominant 2-omega peak",
        abs(angular_frequencies[peak_index] - 2.0 * omega) < 1.0e-12,
    )
    ledger.check(
        "odd harmonics vanish while higher even harmonics show the moment is not a pure sinusoid",
        abs(transform[1]) / abs(transform[2]) < 1.0e-12
        and abs(transform[3]) / abs(transform[2]) < 1.0e-12
        and abs(transform[4]) / abs(transform[2]) > 1.0e-3,
    )
    ledger.check(
        "the sampled special mean independently resolves to the source value",
        abs(np.mean(moments) - 2.0 * math.sqrt(2.0) * math.pi**2) < 2.0e-12,
    )

    kink_moment, kink_error = quad(
        lambda coordinate: 4.0 * coordinate**2 / math.cosh(coordinate) ** 2,
        -24.0,
        24.0,
        epsabs=ABS_TOL,
        epsrel=REL_TOL,
        limit=QUAD_LIMIT,
    )
    ledger.check(
        "the correctly differentiated static kink has exact second moment 2*pi-squared over three",
        kink_error < 1.0e-10
        and abs(kink_moment - 2.0 * math.pi**2 / 3.0) < 1.0e-10,
    )
    ledger.check(
        "a time-independent density remains a constant-moment counterexample",
        len({kink_moment for _ in range(7)}) == 1,
    )

    count = ledger.finish()
    print(f"P040 INDEPENDENT DENSITY-QUADRATURE REVIEW ALL {count} CHECKS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
