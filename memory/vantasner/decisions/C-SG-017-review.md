---
description: Independent review of C-SG-017
author: vantasner-review
created: '2026-08-03T09:40:00Z'
updated: '2026-08-03T09:40:00Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- physical-units
category: decisions
confidence: working
status: archived
---
# Review of C-SG-017

## Claim Under Review

Conditional on `C-MED-003` and normalized `0<omega<1`, the proposed claim
pulls `C-SG-001` into physical coordinates. It gives angular frequency,
period, inverse-tail and profile scales, physical energy, canonical action,
`dE/dJ`, the exact sech-envelope one-over-e distance, and qualified
zero-onsite limits without asserting a material or universal gapless no-go.

## Sourced Inputs

The review read release `v0.80.0`, accepted `C-SG-001`, `C-SG-002`, and
`C-SG-003`, their canonical field/energy/action definitions, proposed
`C-MED-003`, P095's full attempt history, source audit, predicate ledger,
consumer map, and the hash-pinned normalized rung147 and MC1 sources.

## Independence

The primary route calls the canonical dimensional and normalized APIs. The
independent route writes the breather formula directly, differentiates its PDE
residual, derives the initial kinetic-energy slice through a verified
`tanh` antiderivative, transforms the canonical phase-space measure, and
differentiates physical energy by physical action without importing the new
module.

## Verification Status

The status is `symbolic_verified`. Exact differentiation proves the pulled-back
field equation. Exact measure transformations give
`E_scale=sqrt(T*mu)` and `J_scale=sqrt(lambda*T)`, and their ratio is
`omega_0`. The independent route verifies all promoted observables and retains
its intermediate SymPy representation failures append-only rather than
treating unevaluated integrals as proof.

## Sensitivity and Counterexamples

Wrong residual signs, partial coefficient rescalings, normalized or energy
scales substituted for the canonical action factor, and a doubled action all
fail their load-bearing checks. The exact one-over-e point counters the source's
width naming. Fixed normalized and fixed physical frequency give distinct
`mu->0` paths. A second periodic harmonic prevents the accepted breather from
solving a generic periodic-potential equation.

## Framework Compatibility

The claim is a compatible physical-coordinate lift of the normalized accepted
family. It preserves the normalized action convention in `C-SG-003`, restores
all coordinate and measure factors, and explicitly separates dimensionless
`omega` from physical `omega*omega_0`. No accepted normalized formula changes.

## Dependency and Consumer Replay

Dependencies are `C-MED-003`, `C-SG-001`, `C-SG-002`, and `C-SG-003`.
Governed consumers are the dimensional breather APIs, exports, tests, and P095
verifiers. Focused replay covers normalized sine-Gordon and action-scale tests.
External consumers that omit `sqrt(T*mu)` or assign frequency dimension to
`omega` remain noncanonical; no debt is transferred into this claim.

## Competing Candidate Audit

Candidate D supplies the exact field pullback and candidate E the energy/action
Jacobians. Candidates G-H prevent material and universal spectral overreach,
while I exposes consumer convention errors. They were registered before source
body, output, and consumer inspection. Structural consistency and independent
measure derivation select the claim, not a source tally or numerical match.

## Four-Axis Decision

The exact dimensional lift is accepted with explicit model and domain
conditions.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-MED-003 and C-SG-001 through C-SG-003; challenges and supersedes none

## Promotion Transaction

Promotion adds `C-SG-017`, the physical breather APIs and tests, immutable P095
evidence, qualified MC1 disposition, release `v0.81.0`, generated docs and
accepted memory, and parent-effort continuation. Registry membership and
release closure are validated together.

## Continuation if Not Accepted

This section is not invoked because the exact conditional lift is accepted.
A general gapless no-go, dispersion theorem, or material-frequency map remains
a separately governed objective rather than hidden claim debt.

## Done Gate

The positive physical lift, dependency closure, independent rederivation,
mutations, limits, API/tests, source ceiling, and consumers are closed with an
empty campaign ledger. The corpus effort continues to MC2.

## Cross-References

See P095, MC1, `C-MED-003`, `C-SG-001` through `C-SG-003`, the dimensional
sine-Gordon module, and the framework-migration effort.
