---
description: Independent review of exact closed-projector Berry holonomy claim C-BER-001
author: vantasner-review
created: '2026-08-10T04:48:00Z'
updated: '2026-08-10T04:48:00Z'
tags: [substrate-framework, claim-review, berry-holonomy, projective-loop]
category: decisions
confidence: established
status: archived
---
# Review of C-BER-001

## Claim Under Review

C-BER-001 states an exact closed-ray Berry invariant for normalized sections
of an integer-winding rank-one projective loop. With
`A=i*psi_dagger*d_phi psi` and endpoint relation
`psi(2*pi)=tau*psi(0)`, the invariant is
`tau*exp(i*integral(A))`. The real and periodic gauges both give `(-1)^k`,
while a fixed-ray phase has corrected holonomy one.

## Sourced Inputs

The review reads v0.117.0, C-TOP-001 and the C-CHR-001, C-SPN-001,
C-DEF-001, and C-GAU-001 ceilings, frozen P152 and revision 0001, hash-pinned
B1 and dossier, attempts 0001 through 0009, the exact module and focused
tests, both derivations, and the five-node semantic consumer graph. Pending
M1, C1, NA1, and O1 grant no authority.

## Independence

The canonical route validates the normalized section and closed projector
before calculating its endpoint and integral data. The independent route
imports none of the Berry module: it reconstructs inner products, projectors,
connections, transitions, and exact integrals directly from SymPy matrices.
It independently obtains the same real, periodic, nonperiodic-gauge, and
fixed-ray results.

## Verification Status

The maximum verdict is `symbolic_verified`. Primary, independent, focused,
and graph routes pass 27, 12, 18, and 20 checks. Exact integration leaves no
unevaluated `Integral`. B1's numeric constant-integral check is only regression
evidence, and its removed `np.trapz` fallback is handled by an immutable
alias-only replay backed by `np.trapezoid`, not counted against the science.

## Sensitivity and Counterexamples

The fixed-ray mutation keeps B1's half connection and bare minus one but makes
the projector constant and the corrected holonomy plus one. Omitting the
endpoint transition changes that verdict. A nonperiodic gauge with phase
`phi/4` detects the connection-sign mutation; periodic phases change local
`A` without changing the invariant. Odd, even, negative, zero, and symbolic
integer windings test parity and reversal. Invalid normalization, dimension,
projector closure, interval, phase reality, and noninteger winding are
rejected.

## Framework Compatibility

The claim is an additive exact extension depending only on C-TOP-001. It does
not alter the accepted projective/full-polar distinction or the separately
declared local U1 convention. Its API is pure and exact, performs no numeric
quadrature, and names no physical vector potential, core source, dynamics,
electromagnetic field, material, fermion, coupling, or observation.

## Dependency and Consumer Replay

The source graph pins B1, C1, NA1, O1, and OM1, with 34 predicates and five
assertions. All 26 semantic-consumer source checks reproduce once, but pending
consumers gain no authority and qualified OM1 remains unchanged. Twenty other
queue hits are unrelated uses of the token `B1`. The only immutable legacy
shape is B1's eager fallback. GitNexus rates the named API LOW risk with one
direct canonical helper and no affected process.

## Competing Candidate Audit

The source's fixed-ray candidate fails the predeclared moving-projector and
endpoint criteria. The real and periodic moving-lift candidates agree exactly
and use the fewest assumptions. The flat-connection candidate establishes
local nonuniqueness, existing topology prevents duplication, and
same-holonomy countermodels delimit physical meaning. The advertised half
value and minus one did not select the theorem.

## Four-Axis Decision

The four axes are reviewed individually and support an additive promotion.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive exact projective-loop theorem depending on C-TOP-001

## Promotion Transaction

Promotion adds the exact module and tests, package exports, C-BER-001, release
v0.118.0, qualified B1 disposition, generated queue and documentation, and
accepted memory. The registry and release validators, targeted oracles, one
integrated workflow gate, staged graph detection, and diff check all pass.

## Continuation if Not Accepted

Nonacceptance would preserve B1's failed fixed-ray attempt and return to the
real or periodic moving-lift candidates. Physical medium or electromagnetic
interpretations remain open only to a separate proposal supplying the missing
bundle dictionary, dynamics, coupling, material, core, and observation.

## Done Gate

The exact invariant, two gauges, fixed-ray counterexample, mutations,
independent derivation, implementation, dependencies, consumers,
compatibility, nonduplication, B1 qualification, release, and generated state
must close with an empty debt ledger before acceptance.

## Cross-References

See P152, B1, C-TOP-001, C-CHR-001, C-SPN-001, C-DEF-001, C-GAU-001,
`berry_holonomy.py`, its focused tests, and the P152 evidence and reviews.
