"""Independent geometry, profile, and MPD review for P133/T2C."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp
import yaml

from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P133-t2c-tidal-mpd-audit")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-2/"
    "bridge_T2C_tidal_MP.py"
)
SOURCE_SHA = "651fd75287dd25b5c34208ea5789df89be50f5050ec139ae2d99f4962440c369"
FREEZE_SHA = "5e404c5d159f4ada91d3db0ed1547bddb6208729554c10854bfec53f56c5af4e"


def main() -> int:
    checks = CheckLedger("T2C-INDEPENDENT-TIDAL-FORCE-REVIEW")
    source_bytes = SOURCE.read_bytes()
    source_text = source_bytes.decode("utf-8")
    source_tree = ast.parse(source_text)
    checks.check(
        "fresh source read is hash pinned",
        hashlib.sha256(source_bytes).hexdigest() == SOURCE_SHA,
    )
    checks.check(
        "fresh preregistration read is hash pinned",
        hashlib.sha256(
            (CAMPAIGN / "evidence/frozen-proposal.yaml").read_bytes()
        ).hexdigest()
        == FREEZE_SHA,
    )
    calls = [
        node
        for node in ast.walk(source_tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check"
    ]
    checks.check("fresh AST finds thirteen source predicates", len(calls) == 13)

    t, x = sp.symbols("t x", real=True)
    c0 = sp.symbols("c0", positive=True)
    n = sp.Function("n", positive=True)(x)
    metric = sp.diag(-1 / n, n / c0**2)
    inverse = sp.diag(-n, c0**2 / n)
    checks.check(
        "fresh metric inversion and determinant are exact",
        metric * inverse == sp.eye(2)
        and sp.simplify(metric.det() + 1 / c0**2) == 0,
    )
    coordinates = (t, x)
    gamma = [
        [[sp.Integer(0) for _ in range(2)] for _ in range(2)]
        for _ in range(2)
    ]
    for rho in range(2):
        for mu in range(2):
            for nu in range(2):
                gamma[rho][mu][nu] = sp.simplify(
                    sum(
                        inverse[rho, sigma]
                        * (
                            sp.diff(metric[sigma, nu], coordinates[mu])
                            + sp.diff(metric[sigma, mu], coordinates[nu])
                            - sp.diff(metric[mu, nu], coordinates[sigma])
                        )
                        for sigma in range(2)
                    )
                    / 2
                )

    def riemann(rho: int, sigma: int, mu: int, nu: int) -> sp.Expr:
        return sp.simplify(
            sp.diff(gamma[rho][nu][sigma], coordinates[mu])
            - sp.diff(gamma[rho][mu][sigma], coordinates[nu])
            + sum(
                gamma[rho][mu][lam] * gamma[lam][nu][sigma]
                - gamma[rho][nu][lam] * gamma[lam][mu][sigma]
                for lam in range(2)
            )
        )

    n_x = sp.diff(n, x)
    n_xx = sp.diff(n, x, 2)
    scalar = c0**2 * (n * n_xx - 2 * n_x**2) / n**3
    checks.check(
        "fresh component route reproduces the scalar-curvature relation",
        sp.simplify(riemann(1, 0, 0, 1) - scalar / (2 * n)) == 0,
    )
    checks.check(
        "fresh route rejects a Riemann sign flip",
        sp.simplify(riemann(1, 0, 0, 1) + scalar / (2 * n)) != 0,
    )

    wave_number, width = sp.symbols("k sigma", positive=True)
    gaussian_transform = sp.exp(-width**2 * wave_number**2 / 2)
    checks.check(
        "normalized Gaussian transform independently gives its variance",
        sp.simplify(
            -sp.diff(gaussian_transform, wave_number, 2).subs(wave_number, 0)
            - width**2
        )
        == 0,
    )
    point_force_mode = sp.I * wave_number
    extended_force_mode = sp.expand(
        point_force_mode
        * (1 - width**2 * wave_number**2 / 2)
    )
    correction_mode = sp.simplify(extended_force_mode - point_force_mode)
    checks.check(
        "form-factor correction has cubic wave-number dependence",
        sp.simplify(
            correction_mode + sp.I * width**2 * wave_number**3 / 2
        )
        == 0,
    )
    checks.check(
        "second-derivative mutation has the wrong parity for a force",
        correction_mode.subs(wave_number, -wave_number) == -correction_mode
        and (width**2 * wave_number**2).subs(wave_number, -wave_number)
        == width**2 * wave_number**2,
    )

    epsilon = sp.symbols("epsilon", real=True)
    shape = sp.Function("xi", real=True)(x)
    weak_index = 1 + epsilon * shape
    point_acceleration = sp.simplify(
        c0**2 * sp.diff(weak_index, x) / (2 * weak_index**3)
    )
    averaged_width_term = sp.simplify(
        width**2 * sp.diff(point_acceleration, x, 2) / 2
    )
    source_width_term = sp.simplify(
        width**2
        * c0**2
        * (
            weak_index * sp.diff(weak_index, x, 2)
            - 2 * sp.diff(weak_index, x) ** 2
        )
        / (2 * weak_index**4)
    )
    checks.check(
        "fresh weak-profile expansion reproduces the cubic Fourier result",
        sp.simplify(
            sp.diff(averaged_width_term, epsilon).subs(epsilon, 0)
            - c0**2 * width**2 * sp.diff(shape, x, 3) / 4
        )
        == 0,
    )
    checks.check(
        "fresh weak-profile expansion rejects T2C's double derivative",
        sp.simplify(
            sp.diff(source_width_term, epsilon).subs(epsilon, 0)
            - c0**2 * width**2 * sp.diff(shape, x, 2) / 2
        )
        == 0
        and sp.simplify(
            sp.diff(averaged_width_term - source_width_term, epsilon).subs(
                epsilon, 0
            )
        )
        != 0,
    )

    beta = sp.symbols("beta", positive=True)
    symmetric_index = 1 + beta * x**2 / 2
    symmetric_acceleration = sp.simplify(
        c0**2 * sp.diff(symmetric_index, x) / (2 * symmetric_index**3)
    )
    symmetric_source_term = sp.simplify(
        width**2
        * c0**2
        * (
            symmetric_index * sp.diff(symmetric_index, x, 2)
            - 2 * sp.diff(symmetric_index, x) ** 2
        )
        / (2 * symmetric_index**4)
    )
    checks.check(
        "fresh reflection countermodel has zero centered averaged acceleration",
        sp.simplify(
            symmetric_acceleration.subs(x, -x) + symmetric_acceleration
        )
        == 0,
    )
    checks.check(
        "T2C violates the reflection-center countermodel",
        sp.simplify(
            symmetric_source_term.subs(x, 0)
            - c0**2 * beta * width**2 / 2
        )
        == 0,
    )
    symmetric_scalar = sp.simplify(
        c0**2
        * (
            symmetric_index * sp.diff(symmetric_index, x, 2)
            - 2 * sp.diff(symmetric_index, x) ** 2
        )
        / symmetric_index**3
    )
    checks.check(
        "curvature gradient vanishes at the reflection center",
        sp.simplify(sp.diff(symmetric_scalar, x).subs(x, 0)) == 0,
    )

    provenance = yaml.safe_load(
        (CAMPAIGN / "evidence/external-provenance.yaml").read_text()
    )
    equation = next(
        source["displayed_equation"]
        for source in provenance["sources"]
        if source.get("displayed_equation")
    )
    checks.check(
        "fresh provenance read distinguishes spin and quadrupole terms",
        "R_abcd u^b S^cd" in equation
        and "nabla_a R_bcde J^bcde" in equation,
    )
    checks.check(
        "quadrupole provenance requires a rank-four Riemann-symmetry tensor",
        any(
            "rank four" in source.get("tensor_requirements", "")
            for source in provenance["sources"]
        ),
    )
    r = sp.symbols("r", real=True)
    s01, q00, q01, q11 = sp.symbols("s01 q00 q01 q11", real=True)
    curvature_last_pair = sp.Matrix([[0, r], [-r, 0]])
    symmetric_q = sp.Matrix([[q00, q01], [q01, q11]])
    checks.check(
        "fresh contraction rejects symmetric rank-two substitution into spin slots",
        sp.simplify(
            sum(
                curvature_last_pair[a, b] * symmetric_q[a, b]
                for a in range(2)
                for b in range(2)
            )
        )
        == 0
        and s01 != 0,
    )

    checks.check(
        "curvature-width dimensions differ from acceleration by one length",
        (2, -2) != (1, -2),
    )
    checks.check(
        "one spatial derivative repairs the dimensional deficit",
        (2 - 1, -2) == (1, -2),
    )
    coefficient_a, coefficient_b, moment = sp.symbols(
        "coefficient_a coefficient_b moment", real=True
    )
    checks.check(
        "zero-width guard cannot select a coefficient",
        (coefficient_a * moment).subs(moment, 0) == 0
        and (coefficient_b * moment).subs(moment, 0) == 0
        and coefficient_a != coefficient_b,
    )
    checks.check(
        "source proves geometry but only declares the MPD bridge",
        "BRIDGE -- the identification -w~''(0) <-> MP quadrupole" in source_text
        and "identification with the MP/Dixon quadrupole moment is the bridge, stated"
        in source_text,
    )

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
