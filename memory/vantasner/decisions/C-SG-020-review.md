---
description: Independent review of C-SG-020
author: vantasner-review
created: '2026-08-18T21:50:00+02:00'
updated: '2026-08-18T21:50:00+02:00'
tags:
- substrate-framework
- claim-review
- lean-promotion
category: decisions
confidence: working
status: archived
---
# Review of C-SG-020

## Claim Under Review
Declare the kink exchange-phase function Theta(beta^2)=beta^2/4 with phase factor exp(i*Theta(beta^2)) for the normalized sine-Gordon kink-antikink exchange (the derivation of the phase from the bosonic commutator and BCH structure is a declared input). Then the phase is real-homogeneous, Theta(a*beta^2)=a*Theta(beta^2); at the free-fermion coupling beta^2=4*pi the exchange-phase factor is exactly -1 (exp(i*pi)=-1) and the sign-ordered anticommutator factor exp(i*pi*sgn(x-y)) equals -1 for every x != y, while at coupling one the factor is exp(i/4). This is a conditional phase-evaluation theorem on the declared family. It does not derive the exchange phase from the exact S-matrix or bosonization, prove that sine-Gordon kinks are fermions, establish the free-fermion point as a limit, or identify a physical particle.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Bridge.lean`),
the P231 census entry, the P232/P233/P234 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P232-lean-discrete-facts/reviews/C-SG-020-claim-review.md`.

## Independence
The theorem statements were re-derived from the file definitions rather than the module-doc
narrative, and each entrypoint was matched clause-by-clause against the claim statement;
every physics premise in the narrative was confirmed to appear in the claim assumptions as
a declared input rather than machine-checked content.

## Verification Status
formal_verified: kernel-checked at the repository-pinned toolchain (Lean v4.28.0, mathlib
8f9d9cff6bd7) inside the library gate that passed at the ingestion commit; the formal
surface is unchanged by the promotion, so the gate carries without a rebuild. Axiom
footprints are subsets of Mathlib standard axioms; no proof escapes.

## Sensitivity and Counterexamples
The promoting file carries its own non-tautology guards (wrong-dimension, wrong-spin,
dropped-VEV, wrong-coupling, wrong-polarity, order-flip witnesses as applicable), matched
to the claim's discriminating clauses in the census. Where a file used pasted values
instead of evaluating the defining object (ProductionAmplitude), the census recorded a
class-4 disposition rather than a promotion; this claim passed that discipline.

## Framework Compatibility
Append-only compatible_extension: no existing claim altered, no new import beyond the
ingested file, conditional premises named, interpretive physics excluded from the
machine-checked statement. Nearest accepted neighbours state different objects.

## Dependency and Consumer Replay
No existing consumer changes; the generated index, release manifest, and accepted claim
memory regenerate from registry state. Replay is the repository validation suite at the
merge boundary.

## Competing Candidate Audit
Fixed theorem, one complete proof route; the alternative classification (corroboration)
was tested against the registry and rejected by statement-level search (census record).

## Four-Axis Decision
- Verification: formal_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active

Accepted into v0.162.0 through campaign P232.
