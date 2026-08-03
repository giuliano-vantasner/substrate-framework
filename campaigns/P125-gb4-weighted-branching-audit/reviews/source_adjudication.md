# GB4 Source Adjudication

## Exact result

GB4's two displayed fractions are already the weighted specialization of
C-BRN-001. With fixed positive rho and fixed positive weight, the gamma share
has the advertised negative derivative on a positive-real interpolation. A
fresh direct calculation also gives a strictly negative adjacent-integer
difference, so the discrete population statement does not depend on borrowing
calculus.

The relative expression `w(n)N/w(1)` is exactly the weighted-to-comparison odds
relative to a population-one baseline only when both evaluations use the same
positive channel baselines. Its value is one when N is one and the current
weight equals the baseline weight.

## Fixed and coupled weights

The source differentiates with respect to N while treating n, alpha, k, and the
substituted weight as independent of N. Under that fixed-n premise, linear,
exponential, and power weights are simply positive constants and the derivative
sign is identical.

If the intended subdivision count varies with population, positivity is not
enough. The total continuous sign is controlled by `w+Nw'`; the adjacent-
integer sign is controlled by whether `(N+1)w_(N+1)` exceeds `Nw_N`. A positive
inverse-population weight makes the gamma share constant, and a faster inverse
weight makes it increase. With n=N and `w=exp(-alpha*n)`, `Nw` peaks at
`alpha*N=1`, so the gamma share decreases before that point and increases
afterward. Linear and positive-power n=N examples retain the decline.

GB4 therefore proves a fixed-n partial derivative, not regime independence
under an unspecified coupled n(N) law.

## Source oracle

All twenty-three source predicates reproduce. The bound checks and the
suppression helper use isolated samples; the helper accepts an expression that
declines at its one chosen point but rises elsewhere. The rho-free-symbol check
cannot see parameter dependence hidden inside modeled weights, and the
enhancement derivative again holds the weight fixed.

The symmetric-N fake cancels exactly because the same factor multiplies both
declared inputs. Its local rejection does not derive the asymmetric physical
rates. A fraction tending to one is not an uncapped rate, and a unit baseline
identity is not proof of no physical suppression.

## Physical interpretation

Rho, weight normalization, n, alpha, k, and any n(N) law remain free. Every
interior gamma fraction can be fitted by a positive rho. Unequal channel gates
or an omitted third channel change the fraction, while zero physical coupling
removes both rates without changing the formal allocation expressions.

No common initial state, exhaustive channel set, interaction, final-state
measure or spectral density, kinetics, channel normalization, parameter
provenance, or measurement map is supplied. No physical gamma suppression,
soft channel, nuclear branching, emitted spectrum, material rate, enhancement
magnitude, yield, heat, or observation is accepted.

## Dependencies and consumers

GB1 maps to C-BRN-001. GB3, PN2, and PN3 supply no physical rate or weight law.
All fourteen P122 consumer hashes remain unchanged, preserving its 576-check
replay without repeating an unchanged pending cycle. GitNexus reports LOW risk,
zero affected processes, and no canonical change.

## Decision

C-BRN-001 already subsumes every reusable exact result. The direct integer
difference is an immediate corollary, and the coupled-weight counterexamples
qualify the source rather than creating a new positive API. GB4 is terminally
qualified without a new claim, package module, or release.

## Compatibility

GB4 and its durable consumer closure contain no `np.trapz` call and require no
sampled integration, so no NumPy compatibility event occurs.
