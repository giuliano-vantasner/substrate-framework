---
description: Independent review of C-SPN-001 pure-spin-1 orbit and conditional mean-field selection
author: vantasner-review
created: '2026-08-03T02:45:00Z'
updated: '2026-08-03T03:05:00Z'
tags:
- substrate-framework
- claim-review
- spin-1
category: decisions
confidence: established
status: archived
---
# C-SPN-001 Claim Review

## Claim Under Review

C-SPN-001 states the exact invariant and projective endpoint-orbit
classification for every nonzero complex pure spin-1 spinor in the standard
`m=(+1,0,-1)` convention. It then gives the complete fixed-density minimizer
set of the separately supplied energy `(c2/2)|Psi^dagger F Psi|^2` for positive,
negative, and zero `c2`, with the correct density-squared energy gap and a
strict ceiling against material or continuum interpretations.

## Sourced Inputs

The review reads release `v0.60.0`, the frozen P067 contract, hash-pinned ME1,
attempts 0001 through 0003, source reproduction and audit, primary provenance,
canonical module and tests, both exact verifier routes, and the pre-change
impact boundary. O1, ME2, and ME3 remain pending and supply no premise. The
source's material citations and physical BEC labels are not imported.

## Independence

The independent review imports no `spin1_mean_field` API. It reconstructs the
three matrices, expands a six-real-parameter complex spinor, independently
derives the singlet invariant, builds the spherical/Cartesian transformation,
and obtains the cross-product and self-dot identities. It separately checks a
complete polar solution chart, a coherent-state orbit, and endpoint energy
selection for both signs and the zero boundary.

## Verification Status

The maximum verdict is `symbolic_verified`. Every promoted relation is exact
finite-dimensional algebra. The primary route expands the general complex
state, the Cartesian Lagrange identity, endpoint normal forms, and an exact
attainability path. The independent route reconstructs the result without the
canonical API. No sample, tolerance, quadrature, empirical value, unevaluated
object, or comparator enters the accepted result.

## Sensitivity and Counterexamples

The primary and independent oracles reject a wrong singlet sign, a missing
factor two, and incorrect conjugation placement. Density three rejects the
source's unit-density gap and every missing or linear density factor. Positive,
negative, and zero couplings produce distinct ledgers. Zero spinors, matrices
standing in for mixed density states, nonpositive density, malformed vectors,
nonreal couplings, and undecidable signs are refused. The source interpolation
claim fails exactly at `pi/4`, while an alternative exact path attains both
endpoints and the full interval.

## Framework Compatibility

The claim is a native exact representation theorem with no accepted claim
dependency. It freezes the Hermitian basis, pure-state scope, norm `n`, global
phase quotient, and spatial `SO(3)` action. The polar ray orbit is `RP^2`; the
ferromagnetic ray orbit is `S^2` with an `SO(2)` stabilizer. These projective
orbits are not the full condensate order-parameter manifolds. The energy
selection remains conditional on a supplied fixed-density functional and
exactly decided coupling sign.

## Dependency and Consumer Replay

Direct consumers are the new pure module, package export, focused tests, P067
verifiers, governance registry, release manifest, generated docs and memory,
ME1 disposition, and the parent migration effort. No accepted API changes any
existing signature or semantics. Focused tests pass 13 checks, the primary verifier
passes 33 checks, and the independent verifier passes 13 checks. The full
promotion workflow passes all 527 repository tests. Staged graph detection
maps no symbol because its index predates the entirely additive P067 surface;
that empty result is treated as a limitation, not evidence.

## Competing Candidate Audit

Candidates B and C are selected because their invariant and Cartesian routes
jointly prove the bound and exhaust both equality sets. Candidate D is selected
because exact interval minimization handles both signs, zero coupling, and
density scaling without extra assumptions. Candidate A is insufficient as a
global proof; Candidate F is representative-only. Candidate E is structurally
valid but not selected because a local Hessian is weaker than and redundant to
the exact global minimizer theorem. No source label or endpoint number selected
the construction.

## Four-Axis Decision

The independent evidence supports the accepted exact conditional theorem.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `native`
- Epistemic: `active`
- Relationship: new root representation theorem with no accepted dependency

## Promotion Transaction

Promotion adds C-SPN-001 to release `v0.61.0`, qualifies ME1 through the
editable disposition source, regenerates the queue, and synchronizes the
package, tests, campaign, registry, current and pinned manifests, generated
docs, accepted memory, decision memory, and parent effort. Staged impact
detection, the two exact verifiers, focused tests, `scripts/validate.sh`, the
full test suite, and `git diff --check` pass at the promotion boundary.

## Continuation if Not Accepted

If the exact endpoint normal-form proof or synchronization gate fails, P067
continues with a repaired Cartesian convention or an explicit constrained
stationary classification. A source failure alone cannot close the campaign.

## Done Gate

The claim-level debt is empty after canonical synchronization and the
527-test promotion replay. The parent corpus migration remains active while
later queue units are pending.

## Cross-References

See P067, ME1, `spin1_mean_field.py`, `test_spin1_mean_field.py`, release
`v0.60.0`, and the parent migration effort.
