---
description: Independent review of C-GW-011
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
# Review of C-GW-011

## Claim Under Review
Declare gravitonPolarizations(D)=D*(D-3)/2 on the integers, the transverse-traceless (TT) metric-perturbation polarization count of linearised gravity in D spacetime dimensions: a symmetric rank-2 perturbation has D*(D+1)/2 components, linearised diffeomorphism gauge freedom removes D, and TT transversality and tracelessness remove the remaining non-propagating ones, leaving D*(D-3)/2 - this counting decomposition is a declared input, not proved here. The integer division is exact because D*(D-3) is even for every integer D. Evaluated: D=4 gives exactly 2 propagating polarizations (the two gravitational-wave modes), D=3 gives 0, D=5 gives 5, and D=2 gives -1 (strictly nonpositive, no propagating TT polarization counted in two dimensions); the count strictly increases from D=3 to D=4 and D=4 exceeds D=3 by two. This is a conditional counting-arithmetic theorem on the declared function. It does not prove the gauge or counting decomposition, derive linearised gravity or any field equation, assert a physical graviton, helicity, quantum state, or dimension selection, or identify the count with the accepted spatial TT-projector rank of C-GW-002 beyond their shared D=4 value.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Phase5Gravity_GravitonTT.lean`),
the P232 census entry, the P233/P234/P235 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P233-lean-discrete-facts/reviews/C-GW-011-claim-review.md`.

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

Accepted into v0.163.0 through campaign P233.
