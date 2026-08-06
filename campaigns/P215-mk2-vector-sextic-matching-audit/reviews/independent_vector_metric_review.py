"""Independent exact review for P215 without importing its canonical APIs."""

from __future__ import annotations

from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path(__file__).resolve().parents[3]


def main() -> int:
    checks = CheckLedger("P215-independent")
    mass, coupling = sp.symbols("m g", positive=True)
    current, vector = sp.symbols("B w", real=True)
    lagrangian = mass**2 * vector**2 / 2 + coupling * vector * current
    stationary = sp.solve(sp.Eq(sp.diff(lagrangian, vector), 0), vector)
    checks.check(
        "fresh variation has one stationary vector solution",
        stationary == [-coupling * current / mass**2],
    )
    reduced = sp.simplify(lagrangian.subs(vector, stationary[0]))
    checks.check(
        "fresh substitution derives the squared-current coefficient",
        reduced == -coupling**2 * current**2 / (2 * mass**2),
    )
    lambda_a, lambda_b = sp.symbols("lambda_A lambda_B", positive=True)
    checks.check(
        "fresh convention solve finds the pi-squared map",
        sp.solve(sp.Eq(lambda_a**2, sp.pi**4 * lambda_b**2), lambda_a)
        == [sp.pi**2 * lambda_b],
    )

    momentum_squared = sp.symbols("q2", nonzero=True, real=True)
    full_inverse = 1 / (mass**2 - momentum_squared)
    local_inverse = mass**-2
    checks.check(
        "fresh full inverse differs from its local leading term",
        sp.simplify(full_inverse - local_inverse) != 0,
    )
    checks.check(
        "fresh inverse series exposes the first derivative correction",
        sp.series(full_inverse, momentum_squared, 0, 2).removeO()
        == local_inverse + momentum_squared / mass**4,
    )

    entries = sp.symbols("h00 h01 h02 h03 h11 h12 h13 h22 h23 h33")
    h00, h01, h02, h03, h11, h12, h13, h22, h23, h33 = entries
    metric = sp.Matrix(
        [
            [h00, h01, h02, h03],
            [h01, h11, h12, h13],
            [h02, h12, h22, h23],
            [h03, h13, h23, h33],
        ]
    )
    equations: list[sp.Expr] = []
    for axis in range(3):
        generator = sp.zeros(4)
        for first in range(3):
            for second in range(3):
                generator[first + 1, second + 1] = sp.LeviCivita(
                    axis,
                    first,
                    second,
                )
        equations.extend(generator.T * metric + metric * generator)
    invariant_family = sp.linsolve(equations, entries)
    checks.check(
        "fresh adjoint equations leave two invariant coefficients",
        invariant_family
        == sp.FiniteSet((h00, 0, 0, 0, h33, 0, 0, h33, 0, h33)),
    )
    unequal = sp.diag(5, 2, 2, 2)
    checks.check(
        "fresh unequal singlet metric is positive",
        unequal.is_positive_definite is True,
    )
    checks.check(
        "fresh unequal metric remains invariant under every triplet generator",
        all(
            (generator.T * unequal + unequal * generator) == sp.zeros(4)
            for generator in [
                sp.Matrix(
                    [
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 1],
                        [0, 0, -1, 0],
                    ]
                ),
                sp.Matrix(
                    [
                        [0, 0, 0, 0],
                        [0, 0, 0, -1],
                        [0, 0, 0, 0],
                        [0, 1, 0, 0],
                    ]
                ),
                sp.Matrix(
                    [
                        [0, 0, 0, 0],
                        [0, 0, 1, 0],
                        [0, -1, 0, 0],
                        [0, 0, 0, 0],
                    ]
                ),
            ]
        ),
    )

    fixed_lambda = sp.symbols("ell", positive=True)
    pair_one = (mass, sp.sqrt(2) * fixed_lambda * mass)
    pair_two = (9 * mass, 9 * sp.sqrt(2) * fixed_lambda * mass)
    checks.check(
        "fresh fixed-ratio family leaves mass and coupling separate",
        sp.simplify(pair_one[1] / (sp.sqrt(2) * pair_one[0]) - fixed_lambda)
        == 0
        and sp.simplify(pair_two[1] / (sp.sqrt(2) * pair_two[0]) - fixed_lambda)
        == 0
        and pair_one != pair_two,
    )

    color, decay, hls_parameter = sp.symbols("N F a", positive=True)
    conditional = sp.simplify(
        (color * coupling / 2)
        / (sp.sqrt(2) * sp.sqrt(hls_parameter * coupling**2 * decay**2))
    )
    checks.check(
        "fresh conditional cancellation retains the HLS parameter",
        conditional == color / (2 * sp.sqrt(2) * sp.sqrt(hls_parameter) * decay),
    )
    checks.check(
        "a equals two is load bearing for the source formula",
        sp.simplify(conditional.subs(hls_parameter, 2) - color / (4 * decay))
        == 0
        and sp.simplify(conditional.subs(hls_parameter, 1) - color / (4 * decay))
        != 0,
    )
    checks.check(
        "accepted-convention composition retains pi squared",
        sp.simplify(
            conditional.subs(hls_parameter, 2) / sp.pi**2
            - color / (4 * sp.pi**2 * decay)
        )
        == 0,
    )

    claims = {
        claim["id"]: claim
        for claim in yaml.safe_load((ROOT / "governance/claims.yaml").read_text())[
            "claims"
        ]
    }
    checks.check(
        "fresh registry read finds no accepted physical baryon map",
        "physical baryon current" in claims["C-TOP-002"]["statement"],
    )
    checks.check(
        "fresh registry read finds no accepted Nc level identification",
        "identify k with N_c" in claims["C-WZW-002"]["statement"],
    )
    checks.check(
        "fresh registry read keeps KSRF conditional",
        "the KSRF premise or a=2" in claims["C-VEC-001"]["statement"]
        and any(
            "neither it nor a=2 follows" in assumption
            for assumption in claims["C-VEC-001"]["assumptions"]
        ),
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
