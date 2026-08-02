"""Exact Candidate B verifier for P054."""

from __future__ import annotations

import numpy as np
import sympy as sp

from substrate_framework.triaxial_l2 import (
    averaged_mode_equation_defect,
    real_l2_triple_stf_tensor,
    real_l2_tt_readout,
    regular_l_mode_origin_mismatch,
    temporal_coefficient_rank,
)
from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P054-EXACT")
    mu, phi = sp.symbols("mu phi", real=True)
    nx = sp.sqrt(1 - mu**2) * sp.cos(phi)
    ny = sp.sqrt(1 - mu**2) * sp.sin(phi)
    nz = mu
    harmonics = (
        (3 * nz**2 - 1) / 2,
        nx**2 - ny**2,
        2 * nx * ny,
        2 * nx * nz,
        2 * ny * nz,
    )

    def angular_laplacian(expression: sp.Expr) -> sp.Expr:
        return sp.simplify(
            (1 - mu**2) * sp.diff(expression, mu, 2)
            - 2 * mu * sp.diff(expression, mu)
            + sp.diff(expression, phi, 2) / (1 - mu**2)
        )

    ledger.check(
        "all five declared real l=2 shapes have angular eigenvalue minus six",
        all(sp.trigsimp(angular_laplacian(value) + 6 * value) == 0 for value in harmonics),
    )

    directions = (nx, ny, nz)
    angular_tensors = []
    for harmonic in harmonics:
        angular_tensors.append(
            sp.Matrix(
                3,
                3,
                lambda row, column: sp.simplify(
                    sp.integrate(
                        sp.integrate(
                            (3 * directions[row] * directions[column] - int(row == column))
                            * harmonic,
                            (phi, 0, 2 * sp.pi),
                        ),
                        (mu, -1, 1),
                    )
                    / (4 * sp.pi)
                ),
            )
        )
    expected = tuple(
        real_l2_triple_stf_tensor(**{name: 1})
        for name in ("p20", "m2_cosine", "m2_sine", "m1_cosine", "m1_sine")
    )
    ledger.check(
        "independent sphere integrals reproduce every real-l2 triple-STF basis tensor",
        tuple(angular_tensors) == expected,
    )
    ledger.check(
        "every real-l2 tensor is symmetric and trace free",
        all(value == value.T and sp.trace(value) == 0 for value in expected),
    )

    h20, h2c, h2s = sp.symbols("H_20 H_2c H_2s", real=True)
    tensor = real_l2_triple_stf_tensor(
        p20=h20, m2_cosine=h2c, m2_sine=h2s
    )
    readout = real_l2_tt_readout(tensor, [0, 0, 1], [1, 0, 0])
    ledger.check(
        "natural-axis conventional TT readouts are 2H2c/5 and 2H2s/5",
        sp.simplify(readout.conventional_plus_readout - 2 * h2c / 5) == 0
        and sp.simplify(readout.conventional_cross_readout - 2 * h2s / 5) == 0,
    )
    ledger.check(
        "normalized TT coordinates retain the explicit square-root-two scale",
        sp.simplify(readout.normalized_plus_coordinate - 2 * sp.sqrt(2) * h2c / 5) == 0
        and sp.simplify(readout.normalized_cross_coordinate - 2 * sp.sqrt(2) * h2s / 5) == 0,
    )
    ledger.check(
        "the accepted P2 axial eigenvalue and the real-m2 plus readout share 2H/5",
        real_l2_triple_stf_tensor(p20=h20)[2, 2]
        == real_l2_triple_stf_tensor(m2_cosine=h20)[0, 0],
    )

    amplitude, tau, perturbation = sp.symbols("a tau psi", real=True)
    defect = averaged_mode_equation_defect(
        amplitude * sp.cos(tau), sp.besselj(0, amplitude), perturbation
    )
    series = sp.expand(sp.series(defect, amplitude, 0, 4).removeO())
    ledger.check(
        "time averaging omits a nonzero twice-phase coefficient at leading order",
        sp.simplify(series.coeff(amplitude, 2) + perturbation * sp.cos(2 * tau) / 4) == 0,
    )
    ledger.mutation_sensitive(
        "averaged and full equations coincide only in the tested static mutation",
        lambda value: sp.simplify(
            averaged_mode_equation_defect(value * sp.cos(tau), sp.besselj(0, value), perturbation)
        )
        == 0,
        0,
        [sp.Rational(1, 2), 1],
    )

    ledger.check(
        "the regular r-squared origin series satisfies r psi_r minus 2 psi",
        regular_l_mode_origin_mismatch(3 * amplitude**2, 6 * amplitude, amplitude, 2) == 0,
    )
    ledger.check(
        "QB3's nonzero derivative paired with zero value fails the regular origin oracle",
        regular_l_mode_origin_mismatch(0, sp.Rational(1, 10_000), sp.Rational(1, 100), 2)
        == sp.Rational(1, 1_000_000),
    )

    time = np.linspace(0.0, 2.0 * np.pi, 513, endpoint=False)
    fixed = np.column_stack((np.cos(time), -2.5 * np.cos(time)))
    independent = np.column_stack((np.cos(time), np.sin(time)))
    ledger.mutation_sensitive(
        "two independent source traces require temporal coefficient rank two",
        lambda values: temporal_coefficient_rank(values) == 2,
        independent,
        [fixed, np.column_stack((np.cos(time), np.cos(time)))],
    )
    angle = 0.37
    rotation = np.array(
        [[np.cos(2 * angle), -np.sin(2 * angle)], [np.sin(2 * angle), np.cos(2 * angle)]]
    )
    ledger.check(
        "polarization-frame rotation preserves temporal coefficient rank",
        temporal_coefficient_rank(independent @ rotation) == 2
        and temporal_coefficient_rank(fixed @ rotation) == 1,
    )
    ledger.check(
        "zero real-m2 coefficients collapse the triaxial tensor to the declared axisymmetric sector",
        real_l2_triple_stf_tensor(p20=h20) == sp.diag(-h20 / 5, -h20 / 5, 2 * h20 / 5),
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
