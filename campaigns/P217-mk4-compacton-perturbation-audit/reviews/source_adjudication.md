# P217 MK4 Source Adjudication

## Decision

MK4 is qualified rather than accepted wholesale. Its conditional compacton,
exact edge classification, and balanced degree-linear cancellation survive,
but the logarithmically divergent L2 expectation is an obstruction rather
than a controlled correction. P107 already owns every exact survivor, so no
claim or package API is promoted.

## Source Reproduction and Oracle Scope

The pinned 18,532-byte source at SHA-256 `9f2e2990...7295` imports SymPy and
SciPy's current `trapezoid`, contains six literal/runtime checks and one
fail-fast assertion, and reaches `ALL 6 CHECKS PASS` natively in 2.46 seconds.
It has no legacy NumPy integration surface. The native tally proves that the
source predicates execute; exact substitution and limits, not its sampled
residual or quadrature, decide the mathematical claims.

## MK4.1

MK4.1 is valid in its declared reduced radial convention. Integrating
`b0=-(2B/pi) sin(F)^2 F_r/(4 pi r^2)` over the radial measure and endpoints
`F(0)=pi`, `F(infinity)=0` returns `B`. This is a normalization identity for
the reduced ansatz, not a pointwise arbitrary-degree field construction or a
general equality-existence theorem.

## MK4.2

MK4.2 is an exact conditional compacton result. For
`V(F)=1-cos(F)` and the declared radial BPS equation, the interior profile
`F(r)=2 acos(r/R)` satisfies the equation exactly when
`R^3=2 sqrt(2) lambda B/mu`; `F=0` continues it outside. Doubling the radius
coefficient makes the exact residual nonzero. C-BPS-001 supplies neither the
potential nor equality attainment, and MK1/MK2 do not supply physical
couplings, so the result cannot be read as a selected physical state.

## MK4.3

MK4.3 correctly identifies the L2 edge obstruction, subject to a transcription
correction. With `x=1-r/R`, the profile behaves as `2 sqrt(2x)` and its first
radial derivative behaves as `-sqrt(2)/(R sqrt(x))`. Therefore
`r^2 F_r^2` has a simple pole with dimensionless coefficient two. The
generated queue's `F''^2` wording is not the source calculation: a second
derivative would have a different power and is not the L2 density checked by
the executable body.

## MK4.4

MK4.4 is exact duplicate obstruction evidence. The truncated radial integral
is
`4R[atanh(1-delta)-(1-delta)]`, diverging as
`2R log(1/delta)+O(R)`. The source's numerical quadrature agrees with this
formula but earns regression status only. Keeping `delta` explicit shows that
no regulator-independent naive first-order L2 coefficient follows.

## MK4.5

MK4.5 correctly separates the quartic edge factors. Their limits are
`16/R^2` and zero, so the L4 contribution has no analogous edge divergence.
This finite positive term cannot cancel or regularize the separately positive
divergent L2 contribution. P107 already verifies both limits.

## MK4.6

MK4.6 is qualified conditional bookkeeping. If BPS energies are actually
attained and linear in absolute degree, their contribution cancels in the
balanced difference `2 M(2)-M(4)`. A nonlinear degree mutation breaks that
cancellation. C-BPS-002 states this attainment-conditioned result; the lower
bound alone is not the energy. The source also uses the MK2 lambda convention
without the accepted `lambda_A=pi^2 lambda_BPS` conversion, but normalization
does not alter the purely structural linear cancellation.

## Verification and Sensitivity

Nineteen primary and eight fresh independent exact checks pass. They mutate
the compacton radius, regulator, and degree law, distinguish exact limits from
numerical regression, and audit the accepted existence and controlled-
expansion ceilings. The independent route imports neither MK4, the primary
verifier, nor a canonical compacton API.

## Dependency and Consumer Replay

The eleven-node graph pins 70 source predicates and 13 assertions. MK4 is
replayed freshly. E2's inherited current-first fallback is compatibility
provenance only, and MK4 already uses current SciPy `trapezoid`. MK5, MK6,
MR2, and MR6 remain pending reverse consumers and grant no backward authority;
their hashes match the unchanged clean executions recorded by P215.

## Terminal Scope

MK4 maps conditional field algebra and obstruction evidence to existing BPS
claims and P107. It does not promote equality existence, physical couplings, a
finite first-order correction, a controlled C-BPS-003 expansion, or a solved
full model. The positive continuation is a separately declared smooth-
potential, boundary-layer, or direct full-model problem. A terminal
`qualified` disposition is the smallest honest state.

