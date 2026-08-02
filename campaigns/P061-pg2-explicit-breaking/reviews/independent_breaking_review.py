"""Independent derivative and eigenvalue review for P061."""

from __future__ import annotations

import sympy as sp

from substrate_framework.verification import CheckLedger


def main() -> int:
    ledger = CheckLedger("P061-INDEPENDENT")
    field = sp.Symbol("x", real=True)
    amplitude, scale, kinetic = sp.symbols("A F K", positive=True)
    multiplier = sp.Symbol("q", positive=True)
    angle = multiplier * field / scale
    potential = amplitude * (1 - sp.cos(angle))

    derivatives = [
        sp.simplify(sp.diff(potential, field, n).subs(field, 0)) for n in range(7)
    ]
    ledger.check("zeroth derivative", derivatives[0] == 0)
    ledger.check("first derivative", derivatives[1] == 0)
    ledger.check(
        "second derivative", derivatives[2] == amplitude * multiplier**2 / scale**2
    )
    ledger.check("third derivative", derivatives[3] == 0)
    ledger.check(
        "fourth derivative", derivatives[4] == -amplitude * multiplier**4 / scale**4
    )
    ledger.check("fifth derivative", derivatives[5] == 0)
    ledger.check(
        "sixth derivative", derivatives[6] == amplitude * multiplier**6 / scale**6
    )
    ledger.check(
        "Taylor reconstruction from derivatives",
        sp.expand(sum(derivatives[n] * field**n / sp.factorial(n) for n in range(7)))
        == sp.expand(sp.series(potential, field, 0, 7).removeO()),
    )
    ledger.check(
        "independent generalized mass",
        sp.simplify(derivatives[2] / kinetic)
        == amplitude * multiplier**2 / (kinetic * scale**2),
    )

    tau3 = sp.diag(1, -1)
    eigenvalues = tau3.eigenvals()
    ledger.check(
        "Pauli eigenvalues derived",
        eigenvalues == {sp.Integer(-1): 1, sp.Integer(1): 1},
    )
    trace_from_eigenvalues = sp.simplify(
        sum(
            multiplicity * sp.exp(sp.I * multiplier * field * eigenvalue / scale)
            for eigenvalue, multiplicity in eigenvalues.items()
        )
        - 2
    ).rewrite(sp.cos)
    ledger.check(
        "trace from eigenvalues",
        sp.simplify(trace_from_eigenvalues - (2 * sp.cos(angle) - 2)) == 0,
    )

    kinetic_prefactor, trace_prefactor = sp.symbols("Z C", positive=True)
    trace_gram = sp.trace((multiplier * tau3) ** 2)
    scalar_kinetic = sp.simplify(2 * kinetic_prefactor * trace_gram / scale**2)
    trace_potential = sp.simplify(-trace_prefactor * trace_from_eigenvalues)
    trace_curvature = sp.simplify(sp.diff(trace_potential, field, 2).subs(field, 0))
    ledger.check("trace Gram derived", trace_gram == 2 * multiplier**2)
    ledger.check(
        "scalar kinetic derived",
        scalar_kinetic == 4 * kinetic_prefactor * multiplier**2 / scale**2,
    )
    ledger.check(
        "trace curvature derived",
        trace_curvature == 2 * trace_prefactor * multiplier**2 / scale**2,
    )
    ledger.check(
        "coordinate-free generalized mass",
        sp.simplify(trace_curvature / scalar_kinetic)
        == trace_prefactor / (2 * kinetic_prefactor),
    )
    mass = sp.Symbol("m", positive=True)
    source_substitutions = {
        kinetic_prefactor: scale**2 / 16,
        trace_prefactor: mass**2 * scale**2 / 8,
    }
    ledger.check(
        "source pair generalized mass",
        sp.simplify((trace_curvature / scalar_kinetic).subs(source_substitutions))
        == mass**2,
    )
    ledger.check(
        "source pair independent of multiplier",
        not (trace_curvature / scalar_kinetic).has(multiplier),
    )

    cited_trace_potential = sp.simplify(
        trace_potential.subs(source_substitutions).subs(multiplier, 1)
    )
    pg2_potential = mass**2 * scale**2 * (1 - sp.cos(field / scale))
    ledger.check(
        "cited potential factor",
        sp.simplify(cited_trace_potential / pg2_potential) == sp.Rational(1, 4),
    )
    ledger.check(
        "headline one-eighth equality is false",
        sp.simplify(cited_trace_potential - pg2_potential) != 0,
    )
    matching_prefactor = sp.solve(
        sp.Eq(
            -sp.Symbol("C_match") * trace_from_eigenvalues.subs(multiplier, 1),
            pg2_potential,
        ),
        sp.Symbol("C_match"),
    )[0]
    ledger.check(
        "matching trace prefactor derived",
        sp.simplify(matching_prefactor - mass**2 * scale**2 / 2) == 0,
    )
    ledger.check(
        "matching-to-cited ratio",
        sp.simplify(matching_prefactor / (mass**2 * scale**2 / 8)) == 4,
    )

    curvature = sp.Symbol("h", positive=True)
    cosine = curvature * scale**2 * (1 - sp.cos(field / scale))
    quadratic = curvature * field**2 / 2
    ledger.check(
        "competitor Hessians match",
        sp.simplify(
            (sp.diff(cosine, field, 2) - sp.diff(quadratic, field, 2)).subs(field, 0)
        )
        == 0,
    )
    ledger.check(
        "competitor fourth derivatives differ",
        sp.simplify(
            (sp.diff(cosine, field, 4) - sp.diff(quadratic, field, 4)).subs(field, 0)
        )
        == -curvature / scale**2,
    )
    ledger.check(
        "only cosine is periodic",
        sp.trigsimp(cosine.subs(field, field + 2 * sp.pi * scale) - cosine) == 0
        and sp.expand(quadratic.subs(field, field + 2 * sp.pi * scale) - quadratic)
        != 0,
    )

    quark_mass, factor = sp.symbols("m_q c", positive=True)
    condensate = sp.Symbol("Sigma", negative=True)
    declared_mass = -factor * quark_mass * condensate / scale**2
    ledger.check(
        "declared GMOR residual",
        sp.simplify(declared_mass * scale**2 + factor * quark_mass * condensate) == 0,
    )
    ledger.check(
        "declared GMOR quark exponent",
        sp.simplify(quark_mass * sp.diff(declared_mass, quark_mass) / declared_mass)
        == 1,
    )
    ledger.check(
        "declared GMOR scale exponent",
        sp.simplify(scale * sp.diff(declared_mass, scale) / declared_mass) == -2,
    )
    rho = sp.Symbol("rho", positive=True)
    ledger.check(
        "free-input degeneracy independently derived",
        sp.simplify(
            declared_mass.subs(
                {scale: rho * scale, condensate: rho**2 * condensate},
                simultaneous=True,
            )
            - declared_mass
        )
        == 0,
    )
    ledger.check(
        "negative condensate gives positive mass", declared_mass.is_positive is True
    )
    mass_dimensions = {
        "mass_squared": 2,
        "decay_scale_squared": 2,
        "quark_mass": 1,
        "condensate": 3,
    }
    ledger.check(
        "dimension ledger independently closes",
        mass_dimensions["mass_squared"] + mass_dimensions["decay_scale_squared"]
        == mass_dimensions["quark_mass"] + mass_dimensions["condensate"],
    )
    return ledger.finish()


if __name__ == "__main__":
    raise SystemExit(main())
