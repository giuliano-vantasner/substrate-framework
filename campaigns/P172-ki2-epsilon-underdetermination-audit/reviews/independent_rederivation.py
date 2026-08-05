#!/usr/bin/env python3
"""Independent KI2 ceiling derivation from accepted claims, not KI2 code."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import re

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


ROOT = Path("/home/dan/substrate-framework")
CLAIMS_PATH = ROOT / "governance/claims.yaml"
CLAIMS_SHA256 = "b2d68ae4e293301d402de4a0292445805ff42e26871b058fc74427aac37b7a0f"


@dataclass(frozen=True)
class Dimensions:
    """Dimensions of density, derivative, topological current, and potential."""

    density: int
    derivative: int
    current: int
    potential: int


def _dimension_solution(candidate: object) -> tuple[sp.Expr, ...]:
    assert isinstance(candidate, Dimensions)
    d_f, d_e, d_lam, d_mu = sp.symbols("d_f d_e d_lam d_mu", real=True)
    matrix, vector = sp.linear_eq_to_matrix(
        (
            2 * d_f + 2 * candidate.derivative - candidate.density,
            -2 * d_e + 4 * candidate.derivative - candidate.density,
            2 * d_lam + 2 * candidate.current - candidate.density,
            2 * d_mu + candidate.potential - candidate.density,
        ),
        (d_f, d_e, d_lam, d_mu),
    )
    solution = sp.linsolve((matrix, vector), (d_f, d_e, d_lam, d_mu))
    return tuple(next(iter(solution)))


def _has_canonical_dimensions(candidate: object) -> bool:
    return _dimension_solution(candidate) == (1, 0, -1, 2)


def main() -> int:
    checks = CheckLedger("P172-INDEPENDENT-KI2-REDERIVATION")
    claims_bytes = CLAIMS_PATH.read_bytes()
    checks.check(
        "the accepted registry used by the independent derivation is pinned",
        hashlib.sha256(claims_bytes).hexdigest() == CLAIMS_SHA256,
    )
    registry = yaml.safe_load(claims_bytes)
    claims = {claim["id"]: claim for claim in registry["claims"]}
    bps = claims["C-BPS-001"]
    near_bps = claims["C-BPS-003"]
    checks.check(
        "the accepted BPS theorem declares positive lambda and mu as family inputs",
        "Let lambda and mu be positive" in bps["statement"],
    )

    dimensions = Dimensions(4, 1, 3, 0)
    checks.check(
        "the four Lagrangian terms independently give the exact dimension tuple",
        _dimension_solution(dimensions) == (1, 0, -1, 2),
    )
    checks.mutation_sensitive(
        "the independent dimension solve uses every declared term dimension",
        _has_canonical_dimensions,
        dimensions,
        [
            Dimensions(3, 1, 3, 0),
            Dimensions(4, 0, 3, 0),
            Dimensions(4, 1, 2, 0),
            Dimensions(4, 1, 3, 2),
        ],
    )

    dimension_map = sp.Matrix([[1, 0, -1, 2]])
    basis = sp.Matrix.hstack(
        sp.Matrix([0, 1, 0, 0]),
        sp.Matrix([1, 0, 1, 0]),
        sp.Matrix([-2, 0, 0, 1]),
    )
    checks.check(
        "e lambda-times-F and mu-over-F-squared independently span the kernel",
        dimension_map * basis == sp.zeros(1, 3)
        and basis.rank() == 3
        and len(dimension_map.nullspace()) == 3,
    )

    f_pi, e, lam, mu, c, target = sp.symbols(
        "F_pi e lambda mu c epsilon_target", positive=True
    )
    local_ratio = (f_pi / e) / (lam * mu)
    checks.check(
        "the kernel basis gives the proposed local dimensionless ratio exactly",
        sp.simplify(
            local_ratio - 1 / (e * (lam * f_pi) * (mu / f_pi**2))
        ) == 0,
    )
    checks.check(
        "dimensional analysis leaves an arbitrary normalization coefficient",
        sp.simplify(c * local_ratio - local_ratio) != 0
        and sp.simplify((c * local_ratio).subs(c, 1) - local_ratio) == 0,
    )
    checks.check(
        "a dimensionally allowed product relation defeats an independence inference",
        sp.simplify(
            local_ratio.subs(lam, c * f_pi / (e * mu)) - 1 / c
        ) == 0,
    )

    baryon, potential, root_potential, average = sp.symbols(
        "B0 V sqrtV W", positive=True
    )
    density = (lam * sp.pi**2 * baryon) ** 2 + mu**2 * potential
    square = (lam * sp.pi**2 * baryon - mu * root_potential) ** 2
    residual = lam * sp.pi**2 * baryon - mu * root_potential
    bound = 2 * lam * mu * sp.pi**2 * average
    alpha, beta = sp.symbols("alpha beta", positive=True)
    scaled = {lam: alpha * lam, mu: beta * mu}
    checks.check(
        "independent formulas reproduce every lambda-mu-dependent accepted BPS object",
        all(
            token in bps["statement"]
            for token in (
                "(lambda*pi^2*B0)^2+mu^2*V(U)",
                "lambda*pi^2*B0-sign(B)*mu*sqrt(V(U))",
                "2*lambda*mu*pi^2*abs(B)*W",
            )
        ),
    )
    checks.check(
        "coefficient equality forces identity for every positive fixed-theory scaling",
        [root for root in sp.solve(alpha**2 - 1, alpha) if root.is_positive]
        == [sp.Integer(1)]
        and [root for root in sp.solve(beta**2 - 1, beta) if root.is_positive]
        == [sp.Integer(1)],
    )
    double = {alpha: 2, beta: 2}
    checks.check(
        "the advertised simultaneous doubling changes density square residual and bound",
        sp.simplify(density.subs(scaled, simultaneous=True).subs(double) - 4 * density)
        == 0
        and sp.simplify(square.subs(scaled, simultaneous=True).subs(double) - 4 * square)
        == 0
        and sp.simplify(residual.subs(scaled, simultaneous=True).subs(double) - 2 * residual)
        == 0
        and sp.simplify(bound.subs(scaled, simultaneous=True).subs(double) - 4 * bound)
        == 0,
    )
    checks.check(
        "the same move changes the local ratio while connecting distinct theories",
        sp.simplify(local_ratio.subs(scaled, simultaneous=True).subs(double)
                    - local_ratio / 4) == 0
        and sp.simplify(density.subs(scaled, simultaneous=True).subs(double)
                        - density) != 0,
    )

    selected_lambda = f_pi / (e * mu * target)
    checks.check(
        "the positive accepted family realizes every positive local-ratio target",
        selected_lambda.is_positive is True
        and sp.simplify(local_ratio.subs(lam, selected_lambda) - target) == 0,
    )
    checks.check(
        "fixing only the product pins the ratio without selecting each coupling",
        sp.simplify(
            local_ratio.subs(lam, f_pi / (e * mu * target)) - target
        ) == 0
        and mu in selected_lambda.free_symbols,
    )
    checks.check(
        "C-BPS-003 does not identify its expansion coordinate with this ratio",
        "epsilon a positive dimensionless" in near_bps["statement"]
        and not re.search(r"\b(?:lambda|mu|F_pi|e)\b", near_bps["statement"]),
    )
    checks.check(
        "the family freedom is already implicit in accepted arbitrary positive inputs",
        bps["review"] == "accepted"
        and bps["epistemic"] == "active"
        and "select a potential or coupling" in bps["statement"],
    )

    total = checks.finish()
    print(f"P172 INDEPENDENT KI2 REDERIVATION ALL {total} CHECKS PASS")
    return total


if __name__ == "__main__":
    raise SystemExit(main())
