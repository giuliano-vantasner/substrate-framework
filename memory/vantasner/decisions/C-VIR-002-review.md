---
description: Independent review of C-VIR-002
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
# Review of C-VIR-002

## Claim Under Review
For positive real wave speed c and positive period T, if a total nonnegative density magnitude M satisfies the period-integrated virial relation 6*c^2*M*T=0, then M=0: a positive-period, positive-speed configuration with vanishing period-integrated virial forces the total density to vanish. The supporting finite certificates hold exactly: a sum of four real squares a^2+b^2+d^2+e^2 equals zero only termwise; a real affine function nonnegative on all of the real line has zero slope; and the single-crossing identity R0^2+3*c^2*(R0/c)^2=4*R0^2. These are the finite algebraic implications of the Comparsi exact-breather virial nonexistence route; the PDE differentiation and integration-by-parts identities that produce the virial relation are declared inputs verified symbolically in the source workspace, not here. This is a conditional finite-implication theorem. It does not prove the virial identity for any PDE, establish nonexistence of periodic solutions by itself, or treat any physical breather.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/ComparsiVirial.lean`),
the P231 census entry, the P232/P233/P234 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P232-lean-discrete-facts/reviews/C-VIR-002-claim-review.md`.

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
