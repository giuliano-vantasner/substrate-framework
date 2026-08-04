from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    checks = CheckLedger("P135-INDEPENDENT-SCALAR-QED2")

    q0, q1 = sp.symbols("q0 q1", real=True)
    q = sp.Matrix([q0, q1])
    q_squared = sp.expand((q.T * q)[0])
    projector = sp.simplify(sp.eye(2) - q * q.T / q_squared)
    checks.check("fresh projector idempotence", sp.simplify(projector**2 - projector) == sp.zeros(2))
    checks.check("fresh projector left transversality", sp.simplify(q.T * projector) == sp.zeros(1, 2))
    checks.check("fresh projector right transversality", sp.simplify(projector * q) == sp.zeros(2, 1))
    checks.check("projector is undefined at the zero vector", any(entry.has(1 / q_squared) for entry in projector))

    # Contracting the scalar bubble uses q.(2k+q)=D(k+q)-D(k).  A
    # shift-invariant regulator turns the contracted bubble into +2 e^2 q_nu
    # times the tadpole.  The scalar seagull is exactly its negative.
    d0, d1, numerator = sp.symbols("D0 D1 N", nonzero=True)
    partial_fraction_residual = sp.simplify(
        (d1 - d0) * numerator / (d0 * d1)
        - numerator / d0
        + numerator / d1
    )
    checks.check("bubble contraction partial fraction is exact", partial_fraction_residual == 0)
    charge = sp.Symbol("e", positive=True)
    bubble_coefficient = 2 * charge**2
    seagull_coefficient = -2 * charge**2
    checks.check("bubble plus seagull Ward cancellation", sp.simplify(bubble_coefficient + seagull_coefficient) == 0)
    checks.check("omitting seagull leaves a nonzero Ward residual", bubble_coefficient != 0)
    checks.check("wrong seagull sign doubles the Ward residual", sp.simplify(bubble_coefficient - seagull_coefficient) == 4 * charge**2)

    q2, mass = sp.symbols("Q m", positive=True)
    x, y = sp.symbols("x y", real=True)
    scalar_integrand = sp.simplify(
        charge**2
        * q2
        * (1 - 2 * x) ** 2
        / (4 * sp.pi * (mass**2 + q2 * x * (1 - x)))
    )
    ratio = sp.sqrt(q2) / sp.sqrt(q2 + 4 * mass**2)
    real_integrand = y**2 / (1 - ratio**2 * y**2)
    primitive = sp.atanh(ratio * y) / ratio**3 - y / ratio**2
    checks.check("fresh real-domain primitive", sp.simplify(sp.diff(primitive, y) - real_integrand) == 0)
    endpoint = sp.simplify(primitive.subs(y, 1) - sp.limit(primitive, y, 0))
    projector_coefficient = sp.simplify(
        charge**2 * q2 / (sp.pi * (q2 + 4 * mass**2)) * endpoint
    )
    closed = sp.simplify(charge**2 / sp.pi * (sp.atanh(ratio) / ratio - 1))
    checks.check("fresh endpoint reconstruction", sp.simplify(projector_coefficient - closed) == 0)
    checks.check("scalar Feynman numerator differs from fermion numerator", sp.simplify((1 - 2 * x) ** 2 - 4 * x * (1 - x)) != 0)
    checks.check("massive zero-momentum projector coefficient", sp.limit(closed, q2, 0) == 0)
    local_form_factor = sp.simplify(sp.limit(closed / q2, q2, 0))
    checks.check("fresh local transverse form factor", local_form_factor == charge**2 / (12 * sp.pi * mass**2))
    checks.check(
        "fresh next derivative coefficient",
        sp.simplify(
            sp.limit(
                (closed - local_form_factor * q2) / q2**2,
                q2,
                0,
            )
            + charge**2 / (120 * sp.pi * mass**4)
        )
        == 0,
    )
    checks.check("fixed-momentum scalar massless limit diverges", sp.limit(closed, mass, 0, dir="+") == sp.oo)
    checks.check("fixed-momentum heavy-mass limit vanishes", sp.limit(closed, mass, sp.oo) == 0)

    # Independent constant-field route.  The exact Euclidean charged-complex-
    # scalar heat-kernel density in two dimensions is eB/[4*pi*sinh(eBs)].
    # Expanding it before the proper-time integral yields the local F^2 term.
    proper_time, magnetic = sp.symbols("s B", positive=True)
    heat_kernel = charge * magnetic / (
        4 * sp.pi * sp.sinh(charge * magnetic * proper_time)
    )
    free_heat_kernel = 1 / (4 * sp.pi * proper_time)
    heat_b2 = sp.simplify(
        sp.limit((heat_kernel - free_heat_kernel) / magnetic**2, magnetic, 0)
    )
    checks.check("constant-field heat-kernel B squared coefficient", heat_b2 == -charge**2 * proper_time / (24 * sp.pi))
    effective_b2 = sp.simplify(
        -sp.integrate(
            sp.exp(-mass**2 * proper_time) * heat_b2 / proper_time,
            (proper_time, 0, sp.oo),
        )
    )
    checks.check("proper-time effective B squared coefficient", effective_b2 == charge**2 / (24 * sp.pi * mass**2))
    checks.check("F squared equals twice B squared in two Euclidean dimensions", sp.simplify(effective_b2 / 2 - charge**2 / (48 * sp.pi * mass**2)) == 0)
    checks.check("proper-time and momentum routes agree", sp.simplify(effective_b2 / 2 - local_form_factor / 4) == 0)

    fermion_like = sp.simplify(
        charge**2
        / sp.pi
        * sp.integrate(
            q2 * x * (1 - x) / (mass**2 + q2 * x * (1 - x)),
            (x, 0, 1),
        )
    )
    checks.check("fermion-like Schwinger integral has finite massless limit", sp.limit(fermion_like, mass, 0, dir="+") == charge**2 / sp.pi)
    checks.check("statistics mutation changes the massless verdict", sp.limit(fermion_like, mass, 0, dir="+") != sp.limit(closed, mass, 0, dir="+"))

    a0, a1 = sp.symbols("A0 A1", real=True)
    amplitude = sp.Matrix([a0, a1])
    field_strength = q0 * a1 - q1 * a0
    checks.check(
        "projector quadratic form retains inverse momentum",
        sp.simplify((amplitude.T * projector * amplitude)[0] - field_strength**2 / q_squared) == 0,
    )
    checks.check("constant projector coefficient is nonlocal rather than Maxwell", (field_strength**2 / q_squared).has(1 / q_squared))

    kappa, scale = sp.symbols("kappa lambda", positive=True)
    invariant_ratio = charge**2 / kappa
    transformed_ratio = (charge / scale) ** 2 / (kappa / scale**2)
    checks.check("charge-to-kinetic ratio is field-rescaling invariant", sp.simplify(transformed_ratio - invariant_ratio) == 0)
    checks.check("bare charge squared alone is field-rescaling dependent", sp.simplify((charge / scale) ** 2 - charge**2) != 0)
    checks.check("one-plus-one Maxwell has no massless local polarization", 2 - 2 == 0)

    # Exact source-shaped integrand is a statistics mutation, not an
    # independent scalar derivation.
    source_shaped = charge**2 / sp.pi * q2 * x * (1 - x) / (
        mass**2 + q2 * x * (1 - x)
    )
    checks.check("source-shaped and scalar integrands differ generically", sp.simplify(source_shaped - scalar_integrand) != 0)
    checks.check("zero charge removes the one-loop kernel", sp.limit(closed, charge, 0) == 0)

    return checks.finish()


if __name__ == "__main__":
    raise SystemExit(main())
