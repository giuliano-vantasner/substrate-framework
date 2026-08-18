---
description: Independent review of C-GW-013
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
# Review of C-GW-013

## Claim Under Review
Composing the accepted two-dimensional TT projection (C-GW-002) with the accepted axisymmetric zero-cross waveform (C-GW-005): for the declared two-class source-symmetry classification (axisymmetric vs triaxial breathing source), an axisymmetric source excites exactly one of the two TT polarization dimensions - the cross excitation is zero, the plus excitation present - while a triaxial source excites both; the polarization count equals two exactly when the cross polarization is excited; every source in the classification excites at least the plus polarization and at most two; and the triaxial count equals the declared D=4 TT count 2 (saturation) while the axisymmetric count lies strictly below it. The glue is the symmetry-to-count dictionary tying the accepted projector dimension to the accepted axisymmetric cross-zero statement; no new physical premise enters. This is a conditional discrete dictionary theorem. It does not derive either dependency, construct a source, assert physical radiation or a detector signal, or extend the classification beyond the declared two classes.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Phase16QB_TwoPolarizations.lean`),
the P232 census entry, the P233/P234/P235 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P234-lean-polarization-split/reviews/C-GW-013-claim-review.md`.

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

Accepted into v0.163.0 through campaign P234.
