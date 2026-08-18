---
description: Independent review of C-GW-014
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
# Review of C-GW-014

## Claim Under Review
Composing the accepted spherical STF null (C-MOM-003), the accepted 2*omega quadratic-moment doubling (C-SG-009), and the accepted two-dimensional TT projection (C-GW-002): for the declared radiating-channel index radiatedQuadrupole(ell)=ell for ell>=2 and 0 otherwise, a spherical (ell=0) source has identically zero radiated-quadrupole content while the ell=2 channel is nonzero (the guard), the monopole (ell=0) and dipole (ell=1) channels are silent (radiates false) and every channel at or above ell=2 radiates, so the first radiating channel is the quadrupole; and the tied harmonic content of a quadratic breathing source sits on the even line with lowest order 2*omega. The three accepted facts compose into the single channel statement: the radiating channel of a breathing mass source is the ell=2, frequency-doubled, two-dimensional-transverse channel - spherical monopole and dipole silent by the STF null and conservation structure, doubled frequency by the quadratic moment, two transverse dimensions by the TT projection. This is a conditional channel-index composition theorem. It does not re-derive any dependency, construct a 3+1 source or solution, compute radiated power or a waveform, or claim physical radiation from any configuration.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Phase14P3D_SphericalNull.lean`),
the P231 census entry, the P232/P233/P234 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P234-lean-radiating-channel/reviews/C-GW-014-claim-review.md`.

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

Accepted into v0.162.0 through campaign P234.
