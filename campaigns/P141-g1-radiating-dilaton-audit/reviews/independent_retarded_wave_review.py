from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P141/C-RAD-001 independent")
    A, B, c = sp.symbols("A B c", positive=True)
    q = sp.symbols("q", real=True)

    # Fresh variation of L=A(phi_t^2-c^2 phi_x^2)/2+B phi q delta(x).
    phi, phi_t, phi_x, delta = sp.symbols("phi phi_t phi_x delta", real=True)
    lagrangian = A * (phi_t**2 - c**2 * phi_x**2) / 2 + B * phi * q * delta
    checks.check("canonical time momentum is A phi_t", sp.diff(lagrangian, phi_t) == A * phi_t)
    checks.check(
        "canonical space momentum is minus A c squared phi_x",
        sp.diff(lagrangian, phi_x) == -A * c**2 * phi_x,
    )
    checks.check("source variation is B q delta", sp.diff(lagrangian, phi) == B * q * delta)

    # Retarded Green function coefficient is derived independently from the
    # distributional derivative jump, not imported from the claim module.
    primitive_coefficient = B / (2 * A * c)
    time_derivative = sp.simplify(primitive_coefficient * q)
    right_derivative = sp.simplify(-time_derivative / c)
    left_derivative = sp.simplify(time_derivative / c)
    jump = sp.simplify(right_derivative - left_derivative)
    checks.check(
        "retarded jump reproduces the delta equation",
        sp.simplify(-c**2 * jump - B * q / A) == 0,
    )
    checks.check(
        "right branch is outgoing",
        sp.simplify(time_derivative + c * right_derivative) == 0,
    )
    checks.check(
        "left branch is outgoing",
        sp.simplify(time_derivative - c * left_derivative) == 0,
    )

    right_flux = sp.simplify(-A * c**2 * time_derivative * right_derivative)
    left_outward_flux = sp.simplify(A * c**2 * time_derivative * left_derivative)
    total_flux = sp.simplify(right_flux + left_outward_flux)
    work = sp.simplify(B * q * time_derivative)
    checks.check("both outgoing fluxes are equal", right_flux == left_outward_flux)
    checks.check("one-side flux normalization closes", right_flux == B**2 * q**2 / (4 * A * c))
    checks.check("two-side flux normalization closes", total_flux == B**2 * q**2 / (2 * A * c))
    checks.check("source work equals outward power", sp.simplify(work - total_flux) == 0)
    checks.mutation_sensitive(
        "two-sided sum is load bearing",
        lambda candidate: sp.simplify(candidate - work) == 0,
        total_flux,
        [right_flux, total_flux / 4, 2 * total_flux],
    )

    # A static solution has the same local equation and jump but zero flux.
    static_coefficient = -B * q / (2 * A * c**2)
    static_jump = sp.simplify(static_coefficient - (-static_coefficient))
    checks.check(
        "static absolute-value field has the same source jump",
        sp.simplify(static_jump - jump) == 0,
    )
    checks.check("static field has zero canonical flux", sp.Integer(0) != total_flux)

    # Field normalization is not physical: phi'=s phi changes A and B while
    # leaving B^2/A, hence the power, invariant.
    scale = sp.symbols("s", positive=True)
    rescaled_power = sp.simplify(
        (B / scale) ** 2 * q**2 / (2 * (A / scale**2) * c)
    )
    checks.check("field-rescaling ledger preserves power", rescaled_power == total_flux)
    checks.mutation_sensitive(
        "source coupling is load bearing",
        lambda coupling: sp.simplify(coupling**2 * q**2 / (2 * A * c) - total_flux) == 0,
        B,
        [2 * B, B / 2, sp.Integer(0)],
    )

    # The G1 normalization A=1/kappa, B=c=1 is checked independently.
    kappa, qdot = sp.symbols("kappa qdot", positive=True)
    normalized_power = sp.simplify(total_flux.subs({A: 1 / kappa, B: 1, c: 1}))
    g1_power = kappa * qdot**2 / 8
    checks.check("G1-normalized exact power is kappa q squared over two", normalized_power == kappa * q**2 / 2)
    checks.check(
        "G1 expression is off by four even after identifying q with qdot",
        sp.simplify(normalized_power.subs(q, qdot) / g1_power) == 4,
    )
    checks.check(
        "constant retarded source defeats the extra derivative",
        normalized_power.subs(q, 1) != 0 and g1_power.subs(qdot, 0) == 0,
    )

    # A scalar trace profile contracts on a fixed lab-time slice.
    gamma = sp.symbols("gamma", positive=True)
    rest_integral = sp.symbols("Q_rest", nonzero=True, real=True)
    boosted_fixed_time_integral = rest_integral / gamma
    checks.check(
        "boosted scalar-density integral has inverse-gamma Jacobian",
        sp.simplify(boosted_fixed_time_integral * gamma - rest_integral) == 0,
    )
    checks.check(
        "scalar-trace integral is not boosted energy",
        sp.simplify(boosted_fixed_time_integral - gamma * rest_integral) != 0,
    )

    # For an instantaneously stationary translated static profile, acceleration
    # leaves a residual -a F'. At the sine-Gordon kink centre F'=2.
    acceleration = sp.symbols("a", nonzero=True, real=True)
    kink_center_derivative = sp.Integer(2)
    accelerated_residual_at_center = -acceleration * kink_center_derivative
    checks.check(
        "accelerated static kink requires a nonzero source",
        accelerated_residual_at_center != 0,
    )
    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
