"""Primary exact verifier for P069 scalar-lattice continuum ledgers."""

from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

from substrate_framework.lattice_scalar import (
    centered_second_difference,
    centered_taylor_laplacian,
    centered_taylor_remainder_bound,
    lattice_laplacian_symbol,
    lattice_mode_relative_deficit,
    lattice_spatial_frequency_squared,
    linearized_lattice_dispersion_squared,
    periodic_action_error_bound,
    periodic_lattice_eom_residual,
    periodic_lattice_lagrangian,
)
from substrate_framework.verification import CheckLedger

SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-20/"
    "bridge_ME3_lattice_continuum.py"
)
SOURCE_SHA256 = "8b5f888708b2edc202cb1acba37780aa62e7d71d002dc5042fd92e8afefbb0d0"


def main() -> int:
    ledger = CheckLedger("P069")
    ledger.check("hash-pinned ME3 source exists", SOURCE.is_file())
    ledger.check(
        "hash-pinned ME3 source integrity",
        hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA256,
    )
    source_text = SOURCE.read_text(encoding="utf-8")
    ledger.check(
        "ME3 prose includes the Riemann spacing weight in its declared action",
        "] * a" in source_text,
    )
    ledger.check(
        "ME3 checks never construct the declared site sum or vary the action",
        "sp.Sum" not in source_text
        and "euler_lagrange" not in source_text
        and "diff(S_disc" not in source_text,
    )
    ledger.check(
        "ME3 imports neither ME1 nor ME2 into its executable mathematics",
        "from bridge_ME1" not in source_text and "from bridge_ME2" not in source_text,
    )

    a = sp.symbols("a", positive=True)
    jet = sp.symbols("d0:9", real=True)
    expansion = centered_taylor_laplacian(jet[:7], a)
    expected_expansion = jet[2] + a**2 * jet[4] / 12 + a**4 * jet[6] / 360
    ledger.check(
        "two-neighbour Taylor construction derives every surviving coefficient",
        sp.simplify(expansion - expected_expansion) == 0,
    )
    ledger.check(
        "centered symmetry cancels value and odd derivative jets",
        all(not expansion.has(jet[index]) for index in (0, 1, 3, 5)),
    )
    ledger.mutation_sensitive(
        "Taylor oracle rejects sign factorial and copied-coefficient mutations",
        lambda candidate: sp.simplify(candidate - expected_expansion) == 0,
        expansion,
        [
            jet[2] - a**2 * jet[4] / 12 + a**4 * jet[6] / 360,
            jet[2] + a**2 * jet[4] / 24 + a**4 * jet[6] / 360,
            jet[2] + a**2 / 12 + a**4 / 360,
        ],
    )
    bound = centered_taylor_remainder_bound(a, jet[8])
    ledger.check(
        "eighth-derivative bound controls the sixth-order retained stencil",
        bound == a**6 * jet[8] / 20160,
    )
    ledger.mutation_sensitive(
        "remainder oracle retains derivative bound spacing order and factorial",
        lambda candidate: sp.simplify(candidate - a**6 * jet[8] / 20160) == 0,
        bound,
        [a**4 * jet[8] / 20160, a**6 / 20160, a**6 * jet[8] / 40320],
    )

    x = sp.symbols("x", real=True)
    for degree in (0, 1, 2, 3):
        polynomial = x**degree
        exact = centered_second_difference(
            polynomial.subs(x, x - a),
            polynomial,
            polynomial.subs(x, x + a),
            a,
        )
        ledger.check(
            f"positive spacing has zero lattice correction for degree {degree}",
            sp.simplify(exact - sp.diff(polynomial, x, 2)) == 0,
        )
    quartic = x**4
    quartic_exact = centered_second_difference(
        quartic.subs(x, x - a), quartic, quartic.subs(x, x + a), a
    )
    ledger.check(
        "quartic field activates the exact a-squared correction",
        sp.simplify(quartic_exact - sp.diff(quartic, x, 2) - 2 * a**2) == 0,
    )

    k, mass = sp.symbols("k m", real=True, positive=True)
    shift_symbol = sp.simplify(
        (sp.exp(sp.I * k * a) - 2 + sp.exp(-sp.I * k * a)) / a**2
    )
    shift_symbol = sp.simplify(sp.expand_complex(shift_symbol))
    symbol = lattice_laplacian_symbol(k, a)
    ledger.check(
        "shift eigenvalue independently equals the exact sine symbol",
        sp.trigsimp(shift_symbol - symbol) == 0,
    )
    ledger.check(
        "exact symbol is even and reciprocal-lattice periodic",
        sp.simplify(symbol - lattice_laplacian_symbol(-k, a)) == 0
        and sp.trigsimp(symbol - lattice_laplacian_symbol(k + 2 * sp.pi / a, a))
        == 0,
    )
    ledger.check(
        "zero and Brillouin-edge modes remain distinct exact limits",
        lattice_spatial_frequency_squared(0, a) == 0
        and lattice_spatial_frequency_squared(sp.pi / a, a) == 4 / a**2,
    )
    ledger.check(
        "one reciprocal-lattice shift aliases the same sampled mode",
        sp.trigsimp(
            lattice_spatial_frequency_squared(k + 2 * sp.pi / a, a)
            - lattice_spatial_frequency_squared(k, a)
        )
        == 0,
    )

    dispersion = linearized_lattice_dispersion_squared(k, a, mass)
    dispersion_series = sp.series(dispersion, a, 0, 6).removeO().expand()
    expected_dispersion = mass**2 + k**2 - a**2 * k**4 / 12 + a**4 * k**6 / 360
    ledger.check(
        "exact lattice dispersion gives controlled long-wave coefficients",
        sp.simplify(dispersion_series - expected_dispersion) == 0,
    )
    ledger.check(
        "modewise fixed-k continuum limit recovers normalized Klein-Gordon line",
        sp.limit(dispersion, a, 0) == mass**2 + k**2,
    )
    ledger.mutation_sensitive(
        "dispersion oracle rejects sign mass and coefficient mutations",
        lambda candidate: sp.simplify(candidate - expected_dispersion) == 0,
        dispersion_series,
        [
            mass**2 + k**2 + a**2 * k**4 / 12 + a**4 * k**6 / 360,
            mass + k**2 - a**2 * k**4 / 12 + a**4 * k**6 / 360,
            mass**2 + k**2 - a**2 * k**4 / 24 + a**4 * k**6 / 360,
        ],
    )
    deficit = lattice_mode_relative_deficit(k, a)
    ledger.check(
        "relative mode deficit starts at a-squared k-squared over twelve",
        sp.series(deficit, a, 0, 6).removeO().expand()
        == a**2 * k**2 / 12 - a**4 * k**4 / 360,
    )
    ledger.check(
        "Brillouin-edge deficit is finite and not a long-wave-small correction",
        sp.simplify(
            lattice_mode_relative_deficit(sp.pi / a, a) - (1 - 4 / sp.pi**2)
        )
        == 0,
    )

    q = sp.symbols("q0:3", real=True)
    velocity = sp.symbols("v0:3", real=True)
    acceleration = sp.symbols("b0:3", real=True)
    lagrangian = periodic_lattice_lagrangian(q, velocity, a, mass)
    residuals = periodic_lattice_eom_residual(q, acceleration, a, mass)
    for index in range(3):
        direct_variation = a * acceleration[index] - sp.diff(lagrangian, q[index])
        ledger.check(
            f"site {index} variation gives the discrete sine-Gordon residual",
            sp.simplify(direct_variation - a * residuals[index]) == 0,
        )
    ledger.mutation_sensitive(
        "site residual retains spatial sign spacing and onsite sine",
        lambda candidate: sp.simplify(candidate - residuals[0]) == 0,
        residuals[0],
        [
            acceleration[0]
            + centered_second_difference(q[2], q[0], q[1], a)
            + mass**2 * sp.sin(q[0]),
            acceleration[0] - (q[1] - 2 * q[0] + q[2]) / a + mass**2 * sp.sin(q[0]),
            acceleration[0]
            - centered_second_difference(q[2], q[0], q[1], a)
            + mass**2 * q[0],
        ],
    )

    length = sp.symbols("L", positive=True)
    site_count = sp.symbols("N", integer=True, positive=True)
    constant_field_lagrangian = periodic_lattice_lagrangian(
        (sp.pi, sp.pi), (0, 0), length / 2, 1
    )
    ledger.check(
        "Riemann-normalized constant-field action density has a finite fixed-length value",
        constant_field_lagrangian == -2 * length,
    )
    unweighted_constant_sum = -2 * site_count
    ledger.check(
        "omitting the spacing weight diverges at fixed length as sites refine",
        sp.limit(unweighted_constant_sum.subs(site_count, length / a), a, 0, dir="+")
        == -sp.oo,
    )

    duration = sp.symbols("T", positive=True)
    mx, mxx, mt, mtx = sp.symbols("Mx Mxx Mt Mtx", nonnegative=True)
    action_bound = periodic_action_error_bound(
        length, duration, a, mx, mxx, mt, mtx, mass
    )
    expected_bound = duration * length * (
        a * mt * mtx / 2
        + a * mass**2 * mx / 2
        + a * mx * mxx
        + a**2 * mxx**2 / 8
    )
    ledger.check(
        "action error bound retains kinetic potential gradient and forward-error terms",
        sp.simplify(action_bound - expected_bound) == 0,
    )
    ledger.check(
        "fixed smoothness bounds force the sampled action error to zero",
        sp.limit(action_bound, a, 0, dir="+") == 0,
    )
    ledger.mutation_sensitive(
        "action convergence oracle rejects omitted measure and derivative terms",
        lambda candidate: sp.simplify(candidate - expected_bound) == 0,
        action_bound,
        [
            expected_bound / a,
            expected_bound - duration * length * a * mt * mtx / 2,
            expected_bound - duration * length * a**2 * mxx**2 / 8,
        ],
    )

    canonical_source = Path("src/substrate_framework/lattice_scalar.py").read_text(
        encoding="utf-8"
    )
    ledger.check(
        "canonical exact lattice module uses no NumPy quadrature alias",
        "np." + "trapz" not in canonical_source
        and "np." + "trapezoid" not in canonical_source,
    )
    ledger.check(
        "ME3 cannot infer positive-spacing detectability from its leading term",
        lattice_spatial_frequency_squared(0, 1) == 0
        and centered_second_difference(1, 1, 1, 1) == 0,
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
