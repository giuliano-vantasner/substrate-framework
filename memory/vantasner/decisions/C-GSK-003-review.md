---
description: Independent review of C-GSK-003
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
# Review of C-GSK-003

## Claim Under Review
Declare the generalized-Skyrme linearized quadratic weights Aw(x,s,c6,alpha)=x^2*(1+(1+alpha^2)*(s/x)^2+alpha^2*c6*(s/x)^4) and Kw(x,s,p,c6,alpha)=x^2*(1+(1-alpha^2)*p^2+(1+alpha^2)*(s/x)^2+alpha^2*c6*(s/x)^4+(1-alpha^2)*c6*p^2*(s/x)^2) for nonzero real x, real s, p, alpha, and nonnegative sextic coefficient c6. Then exactly Kw-Aw=(1-alpha^2)*p^2*(x^2+c6*s^2); Aw is strictly positive; Kw=Aw holds exactly when alpha^2=1 or p=0; and for |alpha|<1 with nonzero p the kinetic weight strictly exceeds the gradient weight, Aw<Kw. Consequently the declared refractive index n=sqrt(Kw/Aw) equals 1 exactly in the longitudinal case alpha^2=1 and strictly exceeds 1 whenever |alpha|<1 with p nonzero: transverse disturbances in the declared generalized-Skyrme medium propagate with index above one while longitudinal ones do not. This is a conditional weight-comparison theorem on the declared quadratic forms. It does not derive the generalized Skyrme action or its linearization, prove a medium exists, identify x, s, p with physical momentum components beyond the declared reading, or assert a physical refractive medium.

## Sourced Inputs
The review read the Lean sources (`formal/SubstrateFramework/Ingested/Phase48CE_OperatorAndGap.lean`),
the P231 census entry, the P232/P233/P234 proposal manifests and attempt records, the
registry-wide identifier collision search, and the campaign review
`campaigns/P232-lean-discrete-facts/reviews/C-GSK-003-claim-review.md`.

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
