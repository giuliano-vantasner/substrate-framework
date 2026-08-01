---
description: Independent review of C-RGE-001
author: vantasner-review
created: '2026-08-01T14:24:53Z'
updated: '2026-08-01T14:24:53Z'
tags:
- substrate-framework
- claim-review
- one-loop-rg-invariant
category: decisions
confidence: working
status: archived
---
# Review of C-RGE-001

## Claim Under Review
For positive `b0`, `mu0`, and `g0`, a positive coupling satisfying the declared
one-loop ODE `mu*dg/dmu=-b0*g^3/(16*pi^2)` and boundary `g(mu0)=g0` obeys
`1/g(mu)^2=1/g0^2+b0*log(mu/mu0)/(8*pi^2)`. Its formal inverse-coupling zero is
`Lambda=mu0*exp(-8*pi^2/(b0*g0^2))`. `Lambda` has zero total derivative along
the declared flow, not zero partial derivative at fixed `g0`; no beta function,
physical sector, or confinement result is derived.

## Sourced Inputs
The review read `v0.18.0`, P021, attempt `0001`, both exact derivations,
package APIs/tests, hash-pinned EL4 and its source adjudication. EL4's pending
QCD3, CF4, AS, B, OD, and soliton dependencies were audited but were not used as
accepted inputs.

## Independence
The main path verifies the package flow solution and differentiates the
invariant field. The independent review instead sets `h=1/g^2`, integrates
`dh/dlog(mu)=b0/(8*pi^2)`, solves for its zero in logarithmic scale, and only
then exponentiates. It imports neither renormalization API.

## Verification Status
Exact separation, boundary recovery, zero-scale substitution, and vector-field
differentiation support `symbolic_verified`. The 22-check main audit and
five-check independent review test the actual conditional theorem. EL4's
hedgehog shooting result is outside this claim and contributes no exact status.

## Sensitivity and Counterexamples
Reversing the beta sign, halving the beta denominator, or halving the invariant
exponent breaks total-derivative invariance. At fixed coupling,
`partial Lambda/partial mu0=Lambda/mu0`, directly rejecting the ambiguous
source shorthand. Weak-coupling and infinite-coupling limits give scale ratios
zero and one, respectively.

## Framework Compatibility
The theorem is a compatible conditional extension. It introduces no fitted
number: `b0`, the reference scale, and reference coupling are explicit inputs.
It makes no claim about the validity of the one-loop equation at its formal
strong-coupling zero and does not promote QCD or confinement semantics.

## Dependency and Consumer Replay
The claim has no accepted scientific dependency beyond exact positive-real
calculus. Direct consumers are the renormalization APIs, tests, P021,
`C-DIM-005`, EL4's disposition, and future CF4/AS audits. Thirty-three focused
renormalization and dimensional-coordinate tests pass. No debt remains.

## Competing Candidate Audit
Conditional invariant promotion, coordinate-only duplication, and physical
electron closure were registered before the source body and values were read.
The independently integrated ODE supplies a distinct exact object, selecting
conditional promotion without numerical comparison.

## Four-Axis Decision

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new conditional theorem from an explicitly declared ODE

## Promotion Transaction
Promotion adds pure renormalization APIs/tests, P021's frozen evidence,
`C-RGE-001`, qualified EL4 disposition, the release manifest, and regenerated
canonical records. Terminal qualification is supported by P021's source
adjudication and exact counterexamples.

## Continuation if Not Accepted
A failed coefficient mutation or independent integration would reject the
claim. A physical beta function could not be inferred from dimensional form;
it would require a separately adjudicated source claim.

## Done Gate
The exact conditional theorem, independent derivation, mutations, limits,
consumer replay, and premise inventory are complete with no claim debt.

## Cross-References
See P021, EL4, `C-DIM-005`, renormalization APIs/tests, and the parent migration
effort.
