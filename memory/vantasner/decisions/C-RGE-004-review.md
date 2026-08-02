---
description: Independent review of C-RGE-004 exact affine coupling intersection and inverse reconstruction
author: vantasner-review
created: '2026-08-03T23:15:00Z'
updated: '2026-08-03T23:15:00Z'
tags:
- substrate-framework
- claim-review
- renormalization
- migration-WM3
category: decisions
confidence: established
status: active
---
# C-RGE-004 Review

## Claim Under Review

C-RGE-004 conditionally classifies a finite exact family
`a_i=A+B*b_i`: coefficient/augmented rank decides a common intersection;
distinct pairs cross at `(a_i-a_j)/(b_i-b_j)`; equal coefficients distinguish
coincident from parallel-disjoint lines; a unique solution identifies `A` and
`B`; and reference shifts translate `B` while preserving `A`. It also gives
the exact electroweak-form inverse reconstruction from separately supplied
positive `E`, `S`, and `n`, with denominator
`D=b2+n*b1-(1+n)*b3`, conditional boundary `1/(1+n)`, and explicit Abelian
coordinate covariance. The claim derives no beta function, physical sector,
normalization, observation, matching boundary, threshold model, scheme, or
perturbative domain.

## Sourced Inputs

The review reads release `v0.73.0`, C-LIN-001, the P083 frozen proposal,
`renormalization.py`, focused tests, both exact verifiers, both attempt records,
all source records, candidate comparison, primary/literature provenance, impact
analysis, and the hash-pinned WM3 source. QCD3 is qualified only through its
accepted conditional SU3 mappings; SM4 is pending; WM1 and WM2 supply no
accepted physical boundary or common induction.

## Independence

The independent reviewer does not import the new renormalization APIs. It
forms and inverts the exact matrices directly, independently eliminates the
common and running coordinates, recomputes the fixed-data augmented rank and
three pairwise crossings, and derives the normalization and threshold
counterfamilies from fresh SymPy expressions.

## Verification Status

The claim earns `symbolic_verified`. The primary verifier passes 37 exact
checks and the independent route passes 16. Exact rational elimination,
rank, left-null compatibility, pairwise branches, reference covariance,
normalization transforms, singular cases, and threshold counterfamilies match
the claim. The legacy numerical solve is regression coverage only and does not
raise the verdict.

## Sensitivity and Counterexamples

Mutating either observation, any of the three coefficients, or the
hypercharge weight changes the reconstructed object. Deleting the strong row
restores a weak-coordinate null direction. Equal slopes make the inverse solve
singular; equal intercept/coefficient pairs are coincident while equal slopes
with unequal intercepts are disjoint. The fixed measured weak coordinate is an
exact inconsistent counterexample to common intersection. Reference shifts
translate only the crossing coordinate, paired Abelian rescaling preserves the
electromagnetic row but not cross-sector equality, and sector offsets realize
arbitrary targets. These tests are load-bearing rather than approximate target
checks.

## Framework Compatibility

The claim is a compatible extension of C-LIN-001. It keeps the existing
positive-`b0` one-coupling API unchanged and names a separate signed affine
convention, so no sign or normalization convention is mixed. All dimensionful
content stays in a supplied positive reference scale; `B` is dimensionless.
The result naturally fits the framework as a conditional diagnostic and
excludes every unavailable physical import.

## Dependency and Consumer Replay

Direct consumers are the canonical renormalization tests and P083. The pending
SM4 pairwise-running audit is a distinct planned consumer. Package-root exports,
claim/release generation, source queue, docs, accepted memory, claim index,
inventory, repository validation, and the parent migration effort are indirect
consumers. Focused scientific and canonical replays pass; governance and the
single integrated boundary are required in the promotion transaction.

## Competing Candidate Audit

Eight candidates and ordered structural criteria were frozen before source
and comparator access. Literal promotion fails dependency closure; the
inverse-fit and fixed-data branches answer different questions; thresholds
and normalization expose free directions; degeneracies and mutations establish
sensitivity. C-RGE-004 is selected because it adds a reusable signed-affine
coupling API and future SM4 consumer, not because `0.20757` is near a
comparator.

## Four-Axis Decision

The four axes distinguish the exact conditional object from WM3's physical
narrative.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new claim depending on C-LIN-001; no challenge or supersession

## Promotion Transaction

Promotion adds C-RGE-004 to `governance/claims.yaml`, retains the pure APIs and
focused tests, moves P083 unchanged into `campaigns/`, creates `v0.74.0`,
regenerates docs and accepted memory, records WM3 as qualified in
`migration/dispositions.yaml`, regenerates `migration/source-claims.yaml`, and
updates the parent effort. The exact evidence paths must exist before the
disposition is registered. Targeted replay precedes one unchanged integrated
`scripts/validate.sh` gate and final record-sensitive validation.

## Continuation if Not Accepted

This section is inactive because the conditional diagnostic is accepted. Its
acceptance does not close the parent corpus migration or promote WM3's physical
mechanism; the next sequential pending unit remains active after P083.

## Done Gate

C-RGE-004 may be accepted only after registry/release closure, generated-state
agreement, affected consumers, and the integrated gate pass with empty P083
debt. The parent effort remains incomplete while pending source units remain.

## Cross-References

The controlling records are the P083 proposal, `verify.py`, independent
reviewer, source/candidate/literature evidence, C-LIN-001, canonical
renormalization module/tests, WM3 disposition, `v0.74.0`, and the framework
migration effort.
