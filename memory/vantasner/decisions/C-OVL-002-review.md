---
description: Independent review of C-OVL-002 translated-localization ledgers
author: vantasner-review
created: '2026-08-03T07:10:00Z'
updated: '2026-08-03T07:20:00Z'
tags:
- substrate-framework
- claim-review
- translated-localization
category: decisions
confidence: established
status: archived
---
# C-OVL-002 Claim Review

## Claim Under Review

C-OVL-002 states the exact matched-width translated-sech expectation, its
slower-tail and equal-rate-resonance asymptotics, the exact normalized ground
state and translation equivalence of a declared Pöschl--Teller well, the
corresponding sech-core tail ledger, the free rate-spacing product, and a
Gaussian nonuniqueness countermodel. Cartesian measure, supplied centers, and
the physical ceiling are part of the claim.

## Sourced Inputs

The review reads release `v0.64.0`, C-QBL-001, C-QBL-003, C-OVL-001, the
frozen P071 contract, hash-pinned MH2, all five attempts, source audit and
adjudication, primary provenance, canonical module and tests, both verifier
routes, and the impact analysis. MH3 and O1 remain pending and supply no
premise.

## Independence

The independent review imports no `translated_localization` API. It derives
the exponential-variable beta integral, reconstructs the zero-shift gamma
endpoint, checks both unequal tail orderings and the equal-rate closed form,
derives the Pöschl index, eigenvalue, normalization and translated residual,
reconstructs MH2's exact planted-well overlaps and tail coefficient through
adaptive quadrature, and supplies an independent Gaussian log-curvature
countermodel.

## Verification Status

The maximum verdict is `symbolic_verified`. The promoted content is exact
beta/hypergeometric algebra, exact asymptotics with explicit convergence
domains, exact one-dimensional spectral algebra, or finite parameter-rank
bookkeeping. SciPy quadrature independently regresses the formulas and source
specialization with declared error estimates; those floating values are not
promoted as exact claims. The canonical module uses no numerical quadrature.

## Sensitivity and Counterexamples

Mutations reject floating hypergeometric simplification as a proof route, a
finite value substituted for an asymptotic limit, universal selection of the
core tail when the mode density decays more slowly, omission of the equal-rate
linear prefactor, center-dependent translated-well eigenvalues, hidden or
changed spacing, and constant log ratios for Gaussian localization. The
reciprocal rate/spacing direction leaves the limiting ratio invariant.

## Framework Compatibility

The claim is a compatible extension of C-OVL-001. It leaves C-QBL-003's two
modes and physical ceiling unchanged. The Pöschl operator is a separately
declared mathematical family: translating its external well preserves its
spectrum and does not add bound levels. No Cartesian result is renamed radial,
and no origin, radial Jacobian, physical condensate, flavor field, or
generation premise is introduced.

## Dependency and Consumer Replay

The sole direct accepted dependency is C-OVL-001. Consumers are the additive
module, package exports, focused tests, P071 primary verifier, governance,
generated artifacts, MH2 disposition, and future localization audits. The
independent verifier deliberately shares no canonical localization API.
Focused tests pass 27 tests, the primary route passes 43 checks, and the
independent route passes 27 checks. The focused/governance replay passes 44
tests and the full promotion workflow passes all 609 tests. The stale graph
currently sees only the touched package export and cannot index the new module;
direct search supplies the complete additive consumer map.

## Competing Candidate Audit

Candidates B through D supply the exact positive object, and Candidate F
proves nonuniqueness. Candidate A survives only as finite-grid regression.
Candidate E is not selected because MH2 contains no half-line radial operator
to validate; inventing one would expand the objective. The source's lepton
comparators did not select a spacing, well, or claim.

## Four-Axis Decision

The exact evidence and synchronized repository replay support acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-OVL-001 and challenges no accepted claim

## Promotion Transaction

Promotion adds C-OVL-002 to `v0.65.0`, qualifies MH2 through the disposition
source, regenerates the queue, and synchronizes implementation, tests, campaign,
registry, manifests, docs, and accepted memory. Staged impact detection, both
exact verifiers, focused tests, `scripts/validate.sh`, the full suite, and
`git diff --check` pass at the promotion boundary.

## Continuation if Not Accepted

If the tail coefficient or operator translation fails, P071 continues with a
narrower exact convolution or direct unitary proof. Source failure alone cannot
close the campaign, and no radial or flavor premise is imported to rescue it.

## Done Gate

The claim-level debt is empty after canonical synchronization and the 609-test
promotion replay. The parent migration remains active while units are pending.

## Cross-References

See P071, MH2, C-QBL-001, C-QBL-003, C-OVL-001,
`translated_localization.py`, `test_translated_localization.py`, release
`v0.64.0`, and the parent effort.
