# KI4 source adjudication

## Verdict

KI4 is qualified through C-IDN-002 and C-XOV-001. Its same-datum inverse
identities are exact on their proper domains and correctly warn that
reconstructing the datum used to fit a parameter is not an independent test.
Its zero-information, directed-cycle, arbitrary-target, comparator-inertness,
and provenance-proof headlines are rejected or narrowed.

## Predicate findings

KI4.1 proves three example compositions. It omits `y<K`; a positive target
`y=2K` gives a negative Pade inverse and complex exponential and tanh inverses.
The result applies to a declared invertible map, not every unknown physical map.

KI4.2 confuses two set constructions. Before observation, the Pade response can
produce every output in `(0,K)`. After observing `y=K/2` through that fixed
injective map, the compatible epsilon set is the singleton `{1}`, not its
positive prior. The script instead tests eleven samples and then literally
assigns `posterior = prior`. Its output-support statement is conditional; its
information-about-epsilon statement is false, and its framework-wide bracket
premise was rejected in P173.

KI4.3 creates a cycle by adding `kappa_predicted -> kappa_emp`. Ordinary
calibration has edges from observed data to the fit, from the fit to a
reconstruction, and from observed and reconstructed values to a residual. That
graph is acyclic. Same-datum reuse can be non-independent without being a
directed computational cycle.

KI4.4 uses stale 8.4563 rather than accepted 8.4824 and makes 0.929 load-bearing
for `disagreement > 5`. Disagreement cannot prove that a result was derived
rather than fitted, and C-RDIFF-002 does not identify its conditional coordinate
as a physical prediction.

KI4.5 correctly observes that inverse algebra needs no empirical number. It
does not make KI4.4 comparator-inert, and it tests
`backsolve_is_a_derivation = False`, a hard-coded verdict rather than an oracle.

## Positive route and formal scope

C-IDN-002 already classifies same-row zero residual as inverse reconstruction,
not independent overdetermination. C-XOV-001 supplies conditional inverse and
range semantics. Calibration itself is legitimate: fitting `theta` from one
observable and predicting an independent second observable remains falsifiable.

The unchanged Lean file proves reconstruction for one Pade map. Its
`zero_information_gain` set starts by intersecting with the prior output range
and proves reachable output support equals that range. It defines no observed-
target epsilon posterior, entropy, mutual information, graph, or held-out test.
Its prior clean execution is reused without recompilation ceremony.
