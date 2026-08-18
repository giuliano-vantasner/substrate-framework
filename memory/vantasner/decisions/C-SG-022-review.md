---
description: Independent review of C-SG-022
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
# Review of C-SG-022

## Claim Under Review
Declare the Landau-Zener phase probability lzProbPhase(Gamma0,Delta)=exp(-pi*Gamma0/|cos(Delta)|) for the phase-window ionization model. Then for every Gamma0>0 and every threshold P_min with P_min < exp(-pi*Gamma0) there exists a phase Delta with P_min < lzProbPhase(Gamma0,Delta) (the basin of outcome windows above threshold is nonempty); and for thresholds 0 < P_min < P_max < 1 with P_min < exp(-pi*Gamma0), the intermediate basin {Delta : P_min < lzProbPhase(Gamma0,Delta) < P_max} has positive measure, by continuity, the intermediate-value theorem, and strict monotonicity of the phase probability on the interval. This is a conditional basin-nonemptiness theorem on the declared probability model. It does not derive the Landau-Zener probability from a two-level Hamiltonian, prove that the physical ionization outcome realizes this window model, or establish any measured basin.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Basin.lean`),
the P232 census entry, the P233/P234/P235 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P233-lean-discrete-facts/reviews/C-SG-022-claim-review.md`.

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
