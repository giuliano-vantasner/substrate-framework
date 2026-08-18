---
description: Independent review of C-WK-001
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
# Review of C-WK-001

## Claim Under Review
Declare the two-element chirality type (left, right) with the parity involution parityCh swapping left and right (parityCh(parityCh(c))=c), the left-only weak coupling weakCoupling with weakCoupling(left)=1 and weakCoupling(right)=0, and the vector coupling vectorCoupling with value 1 on both chiralities. Then the weak coupling is not parity invariant: weakCoupling(left)=1 differs from weakCoupling(parityCh(left))=0. In the (vector, axial) coupling plane, the declared V-A current (g_V,g_A)=(1,-1) maps under parity to (1,1) and is therefore not parity invariant, while the pure vector current (1,0) is parity invariant. The physical premises - that parity swaps chirality, that the weak interaction couples only to left-chiral states with unit strength, and the V-A form of the charged current - are declared inputs. This is a conditional discrete-function theorem. It does not derive parity violation from a Lagrangian or the standard model, establish maximal parity violation as an experimental fact, prove the V-A structure, or exclude parity-symmetric extensions.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Phase6Weak_MaxParityViolation.lean`),
the P232 census entry, the P233/P234/P235 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P233-lean-discrete-facts/reviews/C-WK-001-claim-review.md`.

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
