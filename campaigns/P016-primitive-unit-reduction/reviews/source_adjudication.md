# Source adjudication: AS2 medium-constant reduction

## Decision

AS2 is qualified. Its exact primitive dimension matrix maps to `C-DIM-002`,
and its Debye-plus-constitutive substitution maps to the explicitly conditional
`C-MED-002` after correcting a missing factor `1/2`. AS2 does not derive the
Debye identification, the speed ratio, the density dictionary, a unique
physical primitive set, or an absolute medium scale.

## Check-family audit

AS2.0 correctly leaves `a`, `Theta`, and `kappa_s` symbolic. The absence of a
number proves only that this script did not fit a comparator; it does not turn
later physical premises into derivations.

AS2.1 correctly forms the `(M,L,T)` dimension matrix with columns
`c0=(0,1,-1)`, `S=(1,2,-1)`, and `a=(0,1,0)`. Its determinant is `-1`, rank is
three, and its kernel is zero. `C-DIM-002` strengthens the result by solving the
unique exponents for mass, energy, time, density, and stiffness. AS2.1G's rank-
two guard for `{c0,a}` is correct. The phrase “fixes all units” is accepted only
relative to this declared primitive set; it does not prove that a physical
theory contains no other dimensionful input.

AS2.2 checks that `S*c0/a` has energy dimension. The equation
`Theta=kappa_s*S*c0/a` is a declared Debye/zero-point model premise, not a
consequence of dimensions. `C-MED-002` retains both that conditional status and
the free positive dimensionless ratio `kappa_s`.

AS2.3a is duplicate conditional evidence for `C-MED-001`: common response
scaling gives `epsilon/mu_inverse=1/c0^2` and wave speed `c0`. AS2.3b–c make the
additional declared substitutions `n=a^-3` and the Debye scale. The resulting
response formulas are exactly `epsilon=kappa_s*S/(a^4*c0)` and
`mu_inverse=kappa_s*S*c0/a^4`.

AS2.3b contains a verifier-insensitive coefficient error. The prose declares
`rho_medium=epsilon/2`, but the implemented `rho_reduced` is just `epsilon` and
prints `S*kappa_s/(a^4*c0)` without the half. Its check tests dimensions and
symbol presence only, so it passes. `C-MED-002` corrects the conditional result
to `rho_medium=kappa_s*S/(2*a^4*c0)` and requires the missing-half mutation to
fail.

AS2.G1 distinguishes a symbol declared independent of `a` from the declared
Debye expression's `a` derivative. This shows the substitution is load-bearing;
it does not independently derive that the actual medium temperature follows
the Debye expression.

## Exact qualification

Accepted mappings are `C-DIM-002`, `C-MED-002`, and the prior `C-MED-001`.
AS2 is terminally qualified because its exact set-local dimension theorem and
conditional substitutions are represented, while the physical selection of
the Debye law, `kappa_s`, `n=a^-3`, `rho=epsilon/2`, observed/spent primitives,
unique one-length ontology, and absolute medium realization are not derived.
