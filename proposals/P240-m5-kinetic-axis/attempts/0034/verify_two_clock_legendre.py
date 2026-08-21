"""Exact fixed-J two-clock algebra for the P240 issue-146 goal."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

from substrate_framework.verification import CheckLedger


HERE = Path(__file__).resolve().parent


def main() -> int:
    ledger = CheckLedger("P240/attempt-0034/fixed-J-two-clock")

    inertia_one, inertia_two, cross = sp.symbols("I1 I2 C", real=True)
    momentum_one, momentum_two = sp.symbols("J1 J2", real=True)
    inertia = sp.Matrix([[inertia_one, cross], [cross, inertia_two]])
    momentum = sp.Matrix([momentum_one, momentum_two])
    determinant = sp.expand(inertia.det())
    inverse = sp.Matrix(
        [[inertia_two, -cross], [-cross, inertia_one]]
    ) / determinant
    ledger.check("displayed inverse is exact", sp.simplify(inertia * inverse) == sp.eye(2))

    fixed_j = sp.factor((momentum.T * inverse * momentum)[0] / 4)
    expected_fixed_j = sp.factor(
        (
            inertia_two * momentum_one**2
            - 2 * cross * momentum_one * momentum_two
            + inertia_one * momentum_two**2
        )
        / (4 * determinant)
    )
    ledger.check("generic two-clock fixed-J Legendre energy is exact", sp.simplify(fixed_j - expected_fixed_j) == 0)
    frequency = sp.simplify(inverse * momentum / 2)
    ledger.check("frequency is one half I inverse J", sp.simplify(2 * inertia * frequency - momentum) == sp.zeros(2, 1))
    ledger.check("fixed-J momentum derivative returns frequency", sp.simplify(sp.Matrix([sp.diff(fixed_j, momentum_one), sp.diff(fixed_j, momentum_two)]) - frequency) == sp.zeros(2, 1))

    inertia_zero, coupling, clock_momentum = sp.symbols(
        "I0 C0 j", positive=True
    )
    equal_inertia = inertia.subs(
        {inertia_one: inertia_zero, inertia_two: inertia_zero, cross: coupling}
    )
    ledger.check(
        "equal-defect common and counter-clock vectors diagonalize inertia",
        equal_inertia * sp.Matrix([1, 1]) == (inertia_zero + coupling) * sp.Matrix([1, 1])
        and equal_inertia * sp.Matrix([1, -1]) == (inertia_zero - coupling) * sp.Matrix([1, -1]),
    )

    like_energy = sp.factor(
        fixed_j.subs(
            {
                inertia_one: inertia_zero,
                inertia_two: inertia_zero,
                cross: coupling,
                momentum_one: clock_momentum,
                momentum_two: clock_momentum,
            }
        )
    )
    opposite_energy = sp.factor(
        fixed_j.subs(
            {
                inertia_one: inertia_zero,
                inertia_two: inertia_zero,
                cross: coupling,
                momentum_one: clock_momentum,
                momentum_two: -clock_momentum,
            }
        )
    )
    separated_energy = clock_momentum**2 / (2 * inertia_zero)
    like_interaction = sp.factor(like_energy - separated_energy)
    opposite_interaction = sp.factor(opposite_energy - separated_energy)
    ledger.check("like-clock energy uses the common inertia eigenvalue", sp.simplify(like_energy - clock_momentum**2 / (2 * (inertia_zero + coupling))) == 0)
    ledger.check("counter-clock energy uses the antisymmetric inertia eigenvalue", sp.simplify(opposite_energy - clock_momentum**2 / (2 * (inertia_zero - coupling))) == 0)
    ledger.check("positive cross inertia lowers the like-clock fixed-J energy", sp.simplify(like_interaction + clock_momentum**2 * coupling / (2 * inertia_zero * (inertia_zero + coupling))) == 0)
    ledger.check("positive cross inertia raises the counter-clock fixed-J energy", sp.simplify(opposite_interaction - clock_momentum**2 * coupling / (2 * inertia_zero * (inertia_zero - coupling))) == 0)

    like_frequency = sp.simplify(
        frequency.subs(
            {
                inertia_one: inertia_zero,
                inertia_two: inertia_zero,
                cross: coupling,
                momentum_one: clock_momentum,
                momentum_two: clock_momentum,
            }
        )
    )
    ledger.check("like-clock frequencies are equal and finite away from the SPD boundary", sp.simplify(like_frequency - sp.Matrix([clock_momentum / (2 * (inertia_zero + coupling))] * 2)) == sp.zeros(2, 1))

    radius, tail_amplitude = sp.symbols("r A", positive=True)
    tail_interaction = sp.factor(like_interaction.subs(coupling, tail_amplitude / radius))
    leading_coefficient = sp.limit(radius * tail_interaction, radius, sp.oo)
    ledger.check("positive A/r cross inertia gives an attractive 1/r fixed-J tail", sp.simplify(leading_coefficient + clock_momentum**2 * tail_amplitude / (2 * inertia_zero**2)) == 0)
    ledger.check("the next asymptotic correction is order r^-2", sp.simplify(sp.limit(radius**2 * (tail_interaction - leading_coefficient / radius), radius, sp.oo) - clock_momentum**2 * tail_amplitude**2 / (2 * inertia_zero**3)) == 0)

    angular_speed = sp.symbols("omega", positive=True)
    fixed_frequency_interaction = 2 * coupling * angular_speed**2
    ledger.check("fixed-omega like-clock cross energy has the opposite leading sign", fixed_frequency_interaction > 0)
    ledger.check("fixed-J and fixed-omega are inequivalent interaction oracles", sp.diff(like_interaction, coupling).subs(coupling, 0) == -clock_momentum**2 / (2 * inertia_zero**2) and sp.diff(fixed_frequency_interaction, coupling) == 2 * angular_speed**2)

    ledger.check("cross-inertia sign mutation reverses the leading fixed-J force sign", sp.diff(like_interaction.subs(coupling, -coupling), coupling).subs(coupling, 0) == clock_momentum**2 / (2 * inertia_zero**2))
    ledger.check("second-momentum sign mutation exchanges common and counter-clock channels", sp.simplify(like_energy - opposite_energy.subs(coupling, -coupling)) == 0)

    mass = sp.symbols("m", positive=True)
    newton_coefficient = sp.factor(
        clock_momentum**2 * tail_amplitude / (2 * inertia_zero**2 * mass**2)
    )
    ledger.check("conditional Newton coefficient is positive under typed positive inputs", newton_coefficient > 0)
    ledger.check("the coefficient bridge reproduces -K_N m^2/r", sp.simplify(-newton_coefficient * mass**2 - leading_coefficient) == 0)

    result = {
        "campaign": "P240",
        "attempt": "0034",
        "candidate": "D_fixed_j_two_clock",
        "generic_fixed_j_energy": "(I2*J1^2-2*C*J1*J2+I1*J2^2)/(4*(I1*I2-C^2))",
        "frequency": "omega=(1/2)*I^-1*J",
        "equal_defects": {
            "like_interaction": "-j^2*C/(2*I0*(I0+C))",
            "counter_rotating_interaction": "+j^2*C/(2*I0*(I0-C))",
            "spd_domain": "I0>0 and |C|<I0",
        },
        "asymptotic_condition": "C(r)=A/r+O(r^-2), A>0",
        "asymptotic_result": "Delta E_J=-j^2*A/(2*I0^2*r)+O(r^-2)",
        "conditional_newton_coefficient": "K_N=j^2*A/(2*I0^2*m^2)>0",
        "ensemble_warning": "At fixed omega the leading like-clock cross energy is +2*C*omega^2. Attraction is a fixed-J result and the numerical oracle must hold the typed momenta fixed.",
        "verdict": "symbolically_open_requires_relaxed_positive_one_over_r_cross_inertia",
        "scope": "Exact implication only. It does not establish the sign, exponent, or nonzero value of C(r) for M5 fields, nor one-body stationarity.",
        "check_count": len(ledger.passed),
    }
    (HERE / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
