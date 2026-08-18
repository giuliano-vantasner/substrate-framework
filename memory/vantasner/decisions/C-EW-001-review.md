---
description: Independent review of C-EW-001
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
# Review of C-EW-001

## Claim Under Review
On the declared rational two-component Higgs-doublet encoding with VEV vev=(0,1)^T, standard SU(2)_L generators T_1=[[0,1/2],[1/2,0]] and T_3=diag(1/2,-1/2), hypercharge half-generator Yhalf=I/2, and electric-charge operator Qop=T_3+Yhalf (so Qop=diag(1,0)), a generator g is unbroken on the VEV when g*vev=0. Then exactly: the charge operator annihilates the VEV (Qop*vev=0, the massless-photon generator), while T_1 (a W generator, image (1/2,0)^T) and T_3 (a Z generator, image (0,-1/2)^T) do not annihilate it (broken, massive); and the annihilator is conditional on the doublet VEV, since Qop does not annihilate the different vector (1,0)^T. The electroweak group SU(2)_L x U(1)_Y, the generator identification, and the masslessness interpretation of the unbroken generator are declared inputs. This is a conditional finite matrix theorem. It does not derive the Higgs mechanism, assert gauge boson masses or a photon, build an action or vacuum, extend the check to T_2 or the hypercharge generator individually, or identify any physical particle.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Phase7EW_MasslessPhoton.lean`),
the P232 census entry, the P233/P234/P235 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P233-lean-discrete-facts/reviews/C-EW-001-claim-review.md`.

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
