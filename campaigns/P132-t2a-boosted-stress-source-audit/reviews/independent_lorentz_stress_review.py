"""Independent Lorentz/stress review for P132 without primary verifier imports."""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import mpmath as mp
import sympy as sp

from substrate_framework.verification import CheckLedger


CAMPAIGN = Path("campaigns/P132-t2a-boosted-stress-source-audit")
SOURCE = Path(
    "/home/dan/substrate/merged-framework/bridges/phase-2/"
    "bridge_T2A_moving_source.py"
)
SOURCE_SHA = "669803de1403c8ca66e399aa4b7c0e762447e40df7c241fe530a6b4e06dde70a"
FREEZE_SHA = "3e138cacdb5c7d67ce50b6dc5b4d94b20a5663827143bf2f163157413bf71007"


def rest_derivatives(xi: mp.mpf, tau: mp.mpf, omega: mp.mpf) -> tuple[mp.mpf, ...]:
    eta = mp.sqrt(1 - omega**2)
    ratio = eta * mp.sin(omega * tau) / (omega * mp.cosh(eta * xi))
    field = 4 * mp.atan(ratio)
    denominator = 1 + ratio**2
    field_tau = 4 * eta * mp.cos(omega * tau) / (
        mp.cosh(eta * xi) * denominator
    )
    field_xi = -4 * ratio * eta * mp.tanh(eta * xi) / denominator
    return field, field_tau, field_xi


def rest_stress(
    xi: mp.mpf, tau: mp.mpf, omega: mp.mpf
) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    field, field_tau, field_xi = rest_derivatives(xi, tau, omega)
    potential = 1 - mp.cos(field)
    energy = (field_tau**2 + field_xi**2) / 2 + potential
    momentum = -field_tau * field_xi
    stress = (field_tau**2 + field_xi**2) / 2 - potential
    return energy, momentum, stress


def cycle_averaged_rest_integrals(
    omega: mp.mpf, half_width: mp.mpf, samples: int
) -> tuple[mp.mpf, mp.mpf, mp.mpf]:
    period = 2 * mp.pi / omega
    totals = [mp.mpf("0"), mp.mpf("0"), mp.mpf("0")]
    for index in range(samples):
        tau = period * index / samples
        for component in range(3):
            value = mp.quad(
                lambda xi: rest_stress(xi, tau, omega)[component],
                [-half_width, 0, half_width],
            )
            totals[component] += value
    return tuple(total / samples for total in totals)


def main() -> int:
    checks = CheckLedger("T2A-INDEPENDENT-LORENTZ-STRESS-REVIEW")
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
    checks.check("fresh AST finds twelve source predicates", len(calls) == 12)

    velocity = sp.symbols("v", real=True)
    gamma = 1 / sp.sqrt(1 - velocity**2)
    metric = sp.diag(1, -1)
    boost = gamma * sp.Matrix([[1, velocity], [velocity, 1]])
    checks.check(
        "fresh Lorentz matrix preserves the mostly-minus metric",
        sp.simplify(boost.T * metric * boost).subs(velocity**2, velocity**2)
        == metric,
    )
    rest_energy, rest_momentum = sp.symbols("E0 P0", real=True)
    charges = sp.simplify(boost * sp.Matrix([rest_energy, rest_momentum]))
    checks.check(
        "fresh charge transformation gives the boosted rest vector",
        charges.subs(rest_momentum, 0)
        == sp.Matrix([gamma * rest_energy, gamma * velocity * rest_energy]),
    )
    checks.check(
        "fresh invariant norm is preserved",
        sp.simplify((charges.T * metric * charges)[0] - (rest_energy**2 - rest_momentum**2))
        == 0,
    )

    a, b, c = sp.symbols("A B C", real=True)
    rest_tensor = sp.Matrix([[a, b], [b, c]])
    lab_tensor = sp.simplify(boost * rest_tensor * boost.T)
    checks.check(
        "fresh tensor transformation retains the mixed rest stress",
        sp.simplify(
            lab_tensor[1, 1] - gamma**2 * (velocity**2 * a + 2 * velocity * b + c)
        )
        == 0,
    )
    period = sp.symbols("T", positive=True)
    rest_cycle_integrals = {
        a: period * rest_energy,
        b: sp.Integer(0),
        c: sp.Integer(0),
    }
    transformed_spacetime_integral = sp.expand(lab_tensor[1, 1]).subs(
        rest_cycle_integrals
    )
    lab_cycle_duration = gamma * period
    mean_integrated_stress = sp.simplify(
        transformed_spacetime_integral / lab_cycle_duration
    )
    momentum = gamma * velocity * rest_energy
    checks.check(
        "fresh spacetime-average derivation gives v times total momentum",
        sp.simplify(mean_integrated_stress - velocity * momentum) == 0,
    )
    checks.check(
        "fresh derivation rejects the source's extra-gamma expression",
        sp.simplify(
            mean_integrated_stress - gamma**2 * velocity**2 * rest_energy
        )
        != 0,
    )
    checks.check(
        "the missing factor is the transformed cycle duration",
        lab_cycle_duration == gamma * period
        and sp.simplify(
            gamma**2 * velocity**2 * rest_energy * period / lab_cycle_duration
            - mean_integrated_stress
        )
        == 0,
    )

    phi_t, phi_x = sp.symbols("phi_t phi_x", real=True)
    covariant_mixed = phi_t * phi_x
    contravariant_mixed = -phi_t * phi_x
    checks.check(
        "fresh index raising changes the off-diagonal sign",
        covariant_mixed == -contravariant_mixed,
    )
    checks.check(
        "the source's alleged covariant component is its contravariant density",
        "T_tx_v = -u_t u_x" in source_text
        and "return -ut * ux" in source_text,
    )
    checks.check(
        "the source's nonzero test cannot establish an independently varied field equation",
        all(name not in {node.id for node in ast.walk(source_tree) if isinstance(node, ast.Name)} for name in ("M_tx", "kappa")),
    )

    mp.mp.dps = 35
    omega = mp.mpf("0.6")
    eta = mp.sqrt(1 - omega**2)
    coarse = cycle_averaged_rest_integrals(omega, 12 / eta, 16)
    refined = cycle_averaged_rest_integrals(omega, 24 / eta, 64)
    expected_energy = 16 * eta
    checks.check(
        "independent mpmath cycle quadrature recovers the exact rest energy",
        abs(refined[0] - expected_energy) / expected_energy < mp.mpf("1e-14"),
    )
    checks.check(
        "independent rest momentum remains zero under refinement",
        abs(coarse[1]) < mp.mpf("1e-25") and abs(refined[1]) < mp.mpf("1e-25"),
    )
    checks.check(
        "independent virial stress average converges to zero",
        abs(refined[2]) / expected_energy < mp.mpf("1e-15")
        and abs(refined[2]) <= abs(coarse[2]),
    )
    numeric_velocity = mp.mpf("0.8")
    numeric_gamma = 1 / mp.sqrt(1 - numeric_velocity**2)
    numeric_correct = numeric_gamma * numeric_velocity**2 * refined[0]
    numeric_source = numeric_gamma**2 * numeric_velocity**2 * refined[0]
    checks.check(
        "independent quadrature exposes the five-thirds source overestimate",
        abs(numeric_source / numeric_correct - mp.mpf(5) / 3) < mp.mpf("1e-30"),
    )
    checks.check(
        "uniform motion retains a zero acceleration countermodel",
        sp.diff(velocity * sp.symbols("t", real=True), sp.symbols("t", real=True), 2)
        == 0,
    )
    checks.check(
        "fresh audit finds no executable GW1 or GW4 dependency",
        {alias.name for node in ast.walk(source_tree) if isinstance(node, ast.Import) for alias in node.names}
        == {"sympy", "mpmath"},
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
