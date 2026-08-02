# P074 Source Adjudication: AS3

AS3 is qualified. Its exact dimensional and substitution algebra survives,
but its induced-gravity, source-coupling, and scale-pinning headlines do not.

## Reproduction

The hash-pinned source exits cleanly and prints `ALL 8 CHECKS PASS`. It uses
only SymPy and no numerical quadrature. Its M,L,T solve correctly gives powers
`(-2,1,-3)` for inverse G in the declared `(a,hbar,c0)` basis, and substituting
the declared cutoff energy reproduces the same expression.

## Dimension and Coefficient Audit

The exponent solution fixes powers only. It does not derive the cutoff-squared
effective-action term, identify the cutoff with granularity, select a field
spectrum or regulator, set the sign, or determine the dimensionless
coefficient. In the source's own M,L,T convention, `c0^3/(s_G*hbar)` is not
dimensionless, so G is not literally `a^2` times a dimensionless number. The
valid statement is the complete monomial `G=a^2*c0^3/(s_G*hbar)` under the
declared zero-baseline induced form.

## Primary-Literature Audit

The source cites Sakharov and Visser. The audited arXiv source gives a
regulated, unrenormalized one-loop inverse Newton coupling containing a
zero-loop `1/G0`, a cutoff-squared supertrace coefficient, mass-log terms, and
finite terms. The leading coefficient depends on statistics and curvature
couplings. The pure Sakharov reading additionally assumes zero tree terms,
one-loop dominance, order-one dimensionless data, an explicit cutoff, and
neglect of other gravitational operators. P074 therefore treats the leading
shift as a declared input and retains an independent additive baseline.

## Identifiability Audit

At fixed compatible references the pure relation gives the exact row
`2*log(a_ratio)-log(s_ratio)=log(G_reduced_ratio)`. Its nullspace spans
`(1,2)`: changing `a_ratio` by `rho` and `s_ratio` by `rho^2` preserves G.
AS3.4 solves for a only by treating the still-free `s_G` as supplied. It does
not pin a, and its derivative comparison against a free kappa never computes
the rank or compatibility of an over-determination system.

## Coupling and Dependency Audit

The step `kappa=8*pi*G_eff` is imported from pending G5/note-13 and is not an
accepted consequence of C-OG-003, which explicitly leaves its 1+1 source
coupling unnormalized. A dimensionless multiplier is permitted only when the
source equation requires the same dimension as G. For a dimensionless scalar
operator sourced by mass density, the normalization needs dimensions of
`c^-2`; for energy density it needs `c^-4`. AS3 declares neither accepted
source dimension nor conversion. Its G5 cross-check becomes an identity after
substituting both imported premises and adds no independent evidence.

## Terminal Decision

The source maps to C-DIM-001, C-IDN-001, C-OG-003's normalization ceiling, and
the new conditional C-GRV-001 ledger. It does not establish a physical
Sakharov mechanism, 3+1 Einstein gravity, medium field content, a Newton
constant, a lattice cutoff, a pinned optical coupling, over-determination, or
absolute-scale closure. All later AS, G, OD, and S5 narratives remain outside
the accepted dependency closure.
