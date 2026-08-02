# P078 Source Adjudication: AS7

AS7 is qualified. Its pure-branch inverse calculations reproduce, but it does
not derive a Planck granularity, a physical coupling, or independent
cross-sector over-determination.

## Reproduction

The hash-pinned source exits cleanly and prints `ALL 6 CHECKS PASS`. It uses
observed `G`, `hbar`, `c`, a `1.4 fm` length, `b0=7`, selected coefficient
samples, and a hard-coded metre band. Calling the final quantities
dimensionless does not remove these dimensionful and modeling premises. This
campaign is exact symbolic work and uses neither `np.trapz` nor
`np.trapezoid`.

## Pure and Additive Gravity Branches

On the separately imposed zero-baseline branch, supplying positive
`G,c,hbar,s` gives
`a=sqrt(s*hbar*G/c^3)`. Consequently a supplied closed coefficient interval
`[s_-,s_+]` maps monotonically to the conditional cutoff interval with those
endpoint square roots. Widening the coefficient interval changes the cutoff
interval. The range is a premise, not a theorem, and naming its image a
Planck band adds no derivation.

Conversely, every supplied positive target cutoff `a_t` has the coefficient
preimage `s_t=a_t^2*c^3/(hbar*G)`. In the general accepted inverse-coupling
family, the additive baseline
`B=1/G-s*hbar/(a^2*c^3)` realizes any supplied positive total for arbitrary
positive cutoff and nonzero real coefficient. AS7 neither derives `B=0` nor
excludes these families.

## Joint Rank and Inverse Reconstruction

Use compatible positive references and define
`u=log(a/a0)`, `v=log(s/s0)`, and `y=1/g^2`. The pure gravity row is
`2u-v=log(G/G0)`. A separately supplied formal relation
`L/a=C*exp(K*y)`, with `K=8*pi^2/b0`, gives
`u+K*y=log((L/a0)/C)`. Their coefficient matrix is

```text
[[2, -1, 0],
 [1,  0, K]]
```

It has rank two, nullity one, and null vector `(-K,-2K,1)`. No coordinate is
identified by these two rows. Adding the separately supplied row
`v=log(s/s0)` raises the rank to three and gives
`u=(log(G/G0)+v)/2` and
`y=(log((L/a0)/C)-u)/K`. A positive coupling exists only if this solved `y`
is positive. Changing the supplied coefficient, conversion, beta coefficient,
target length, or length orientation changes the inferred value.

AS7 defines `b2_star` from its gravity-selected cutoff and then substitutes
that same value into the length inverse. The resulting equality is a zero
residual by construction. It is not an independent compatibility oracle, and
matrix row rank alone would not prove causal or statistical independence even
if an additional measured row were supplied.

## Source Checks

- AS7.0 reproduces a conditional ratio after importing observed constants; it
  does not establish a no-import theorem.
- AS7.1 reconstructs a large coefficient from supplied targets and calls it
  absurd using an unaccepted coefficient prior.
- AS7.2 samples a supplied coefficient range against a hard-coded metre band.
- AS7.3 inversely solves the coupling from the supplied hierarchy.
- AS7.4 reuses that solve in the alleged independent route.
- AS7.5 hard-codes `245/1000`; C-SYM-002 accepted no physical self-dual
  operating point for it to refute.

The source also reverses C-RGE-003's accepted AS1 executable length
orientation unless the two physical roles are independently remapped. Neither
ME3 nor QCD3 provides the missing cutoff ontology, coefficient range, hadron
dictionary, or physical selection of `b0=7`.

## Terminal Decision

AS7 maps to C-IDN-002's exact feasibility and inverse-reconstruction ledger,
with C-GRV-001, C-RGE-003, C-IDN-001, C-DIM-008, and C-SYM-002 supplying its
dependencies and interpretation ceilings. It establishes no observed Newton
constant, absolute cutoff, Planck or hadron identity, field-count prior,
physical beta function, selected coupling, vacuum, QCD realization, lattice
termination, or substrate granularity.
