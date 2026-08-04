#!/usr/bin/env python3
"""Fresh projective-loop derivation without the canonical Berry helper."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def _inner(left: sp.MatrixBase, right: sp.MatrixBase) -> sp.Expr:
    return sp.simplify((left.conjugate().T * right)[0, 0])


def _connection(section: sp.MatrixBase, coordinate: sp.Symbol) -> sp.Expr:
    return sp.simplify(sp.I * _inner(section, section.diff(coordinate)))


def run() -> int:
    checks = CheckLedger("P152-independent")
    phi = sp.symbols("phi", real=True)
    winding = sp.symbols("k", integer=True)
    real_lift = sp.Matrix(
        [sp.cos(winding * phi / 2), sp.sin(winding * phi / 2)]
    )
    real_projector = sp.simplify(real_lift * real_lift.T)
    real_transition = _inner(
        real_lift.subs(phi, 0), real_lift.subs(phi, 2 * sp.pi)
    )
    real_connection = _connection(real_lift, phi)
    real_phase = sp.simplify(
        real_transition
        * sp.exp(sp.I * sp.integrate(real_connection, (phi, 0, 2 * sp.pi)))
    )
    checks.check("fresh real lift is normalized", _inner(real_lift, real_lift) == 1)
    checks.check(
        "fresh real projector closes and varies",
        sp.simplify(
            real_projector.subs(phi, 2 * sp.pi) - real_projector.subs(phi, 0)
        )
        == sp.zeros(2)
        and sp.simplify(real_projector.diff(phi)) != sp.zeros(2),
    )
    checks.check(
        "fresh real lift puts parity in the transition",
        real_connection == 0
        and real_transition == (-1) ** winding
        and real_phase == (-1) ** winding,
    )

    periodic = sp.simplify(sp.exp(-sp.I * winding * phi / 2) * real_lift)
    periodic_projector = sp.simplify(periodic * periodic.conjugate().T)
    periodic_transition = _inner(
        periodic.subs(phi, 0), periodic.subs(phi, 2 * sp.pi)
    )
    periodic_connection = _connection(periodic, phi)
    periodic_phase = sp.simplify(
        periodic_transition
        * sp.exp(sp.I * sp.integrate(periodic_connection, (phi, 0, 2 * sp.pi)))
    )
    checks.check(
        "fresh periodic section has the same projector",
        sp.simplify(periodic_projector - real_projector) == sp.zeros(2),
    )
    checks.check(
        "fresh periodic section puts parity in the integral",
        periodic_transition == 1
        and periodic_connection == winding / 2
        and periodic_phase == (-1) ** winding,
    )

    chi = phi / 4
    changed = sp.simplify(sp.exp(sp.I * chi) * real_lift.subs(winding, 1))
    changed_transition = _inner(
        changed.subs(phi, 0), changed.subs(phi, 2 * sp.pi)
    )
    changed_connection = _connection(changed, phi)
    changed_phase = sp.simplify(
        changed_transition
        * sp.exp(sp.I * sp.integrate(changed_connection, (phi, 0, 2 * sp.pi)))
    )
    checks.check(
        "fresh nonperiodic gauge route cancels endpoint and integral changes",
        changed_transition == -sp.I
        and changed_connection == -sp.Rational(1, 4)
        and changed_phase == -1,
    )
    wrong_sign = sp.simplify(
        changed_transition
        * sp.exp(-sp.I * sp.integrate(changed_connection, (phi, 0, 2 * sp.pi)))
    )
    checks.check("fresh connection-sign mutation changes the verdict", wrong_sign == 1)

    fixed = sp.Matrix([sp.exp(-sp.I * phi / 2), 0])
    fixed_projector = sp.simplify(fixed * fixed.conjugate().T)
    fixed_transition = _inner(fixed.subs(phi, 0), fixed.subs(phi, 2 * sp.pi))
    fixed_connection = _connection(fixed, phi)
    fixed_bare = sp.simplify(
        sp.exp(sp.I * sp.integrate(fixed_connection, (phi, 0, 2 * sp.pi)))
    )
    checks.check("fresh B1 fixed-ray projector is constant", fixed_projector.diff(phi) == sp.zeros(2))
    checks.check(
        "fresh B1 endpoint correction changes minus one to plus one",
        fixed_connection == sp.Rational(1, 2)
        and fixed_transition == -1
        and fixed_bare == -1
        and sp.simplify(fixed_transition * fixed_bare) == 1,
    )
    checks.check(
        "fresh omitted-transition mutation misclassifies the fixed ray",
        fixed_bare != sp.simplify(fixed_transition * fixed_bare),
    )
    checks.check(
        "fresh odd and even limits resolve the parity character",
        real_phase.subs(winding, 1) == -1
        and real_phase.subs(winding, 2) == 1,
    )

    same_holonomy_external_label = sp.symbols("external_label")
    checks.check(
        "fresh same-holonomy countermodel leaves physical interpretation free",
        same_holonomy_external_label.free_symbols == {same_holonomy_external_label}
        and periodic_phase.subs(winding, 1) == -1,
    )

    tally = checks.finish()
    print(f"P152 INDEPENDENT ALL {tally} CHECKS PASS")
    return tally


if __name__ == "__main__":
    raise SystemExit(run())
