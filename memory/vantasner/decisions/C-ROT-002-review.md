---
description: Independent review of C-ROT-002
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
# Review of C-ROT-002

## Claim Under Review
Declare the quantum symmetric-top rotational band M(J)=Mcl+J*(J+1)/(2*Lambda) and the classical rotor band Mcl_prime(J)=Mcl+J^2/(2*Lambda) for real classical mass Mcl and nonzero moment of inertia Lambda. Then the J=3/2 member lies strictly above the J=1/2 member for positive Lambda, with exact splitting M(3/2)-M(1/2)=3/(2*Lambda) independent of Mcl; the excitation energies stand in exact ratio M(3/2)-Mcl = 5*(M(1/2)-Mcl) for every nonzero Lambda, while the classical rotor gives ratio 9 and a different splitting, so the quantum band splitting is not the classical one. Adding an arbitrary one-loop vacuum energy E1 to the mass, Mtot(J)=Mcl+E1+J*(J+1)/(2*Lambda), leaves the splitting exactly 3/(2*Lambda) for every E1 - it is a function of the inertia alone, with zero derivative in E1 and identical splittings for distinct vacuum energies - while every individual level strictly increases with E1. In the corpus inertia frame Lambda=L*(1+lambda1)/(3*e^4*m_e) the splitting equals (9/2)*e^4*m_e/(L*(1+lambda1)) identically and is strictly decreasing in the inertia correction lambda1>-1, with distinct corrections giving distinct splittings; the two one-loop questions (level shift by E1, splitting shift by lambda1) are independent. This is a conditional band-structure theorem on the declared spectra. It does not derive the moment of inertia from a field theory, quantize a rotor, identify Delta or nucleon states, fix Mcl, E1, Lambda, or any coupling, or compare to observed splittings.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Phase47BM_RigidTopSpectrum.lean`, `formal/SubstrateFramework/Ingested/Phase48CE_OperatorAndGap.lean`),
the P231 census entry, the P232/P233/P234 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P232-lean-discrete-facts/reviews/C-ROT-002-claim-review.md`.

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
