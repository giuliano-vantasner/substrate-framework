---
description: Independent review of C-DEF-001 angular-defect energy and polar topology ledgers
author: vantasner-review
created: '2026-08-03T04:00:00Z'
updated: '2026-08-03T04:20:00Z'
tags:
- substrate-framework
- claim-review
- angular-defects
category: decisions
confidence: established
status: archived
---
# C-DEF-001 Claim Review

## Claim Under Review

C-DEF-001 states the exact fixed-degree annular Dirichlet energy, a declared
fixed-total-charge matched-shell split ledger, the distinct projective and full
polar fundamental groups, and the two-stiffness/core residual governing an
isolated half-pair comparison. Every model boundary and physical ceiling is
part of the claim.

## Sourced Inputs

The review reads release `v0.61.0`, C-SPN-001, the frozen P068 contract,
hash-pinned ME2, all three attempts, source audit and adjudication, primary
provenance, canonical module and tests, both exact verifier routes, and the
impact analysis. O1 remains pending and supplies no premise.

## Independence

The independent review imports no `angular_defects` API. It directly integrates
the polar-coordinate energy, derives the circlewise Cauchy lower bound,
reconstructs the near/far shell formula, implements both deck groups, and
independently derives the two-stiffness/core residual.

## Verification Status

The maximum verdict is `symbolic_verified`. All promoted results are exact
integration, algebra, or discrete covering transformations. The shell result
is explicitly a declared scale-matched model, not evidence for an exact
finite-domain multi-core solution. No numerical sample, quadrature, tolerance,
empirical comparator, or material input enters the claim.

## Sensitivity and Counterexamples

Mutations reject missing pi, the wrong charge power, an omitted common far
field, wrong coincident and boundary-separated limits, swapped projective/full
generator squares, hidden director stiffness, and omitted core costs. At
`xi=1,d=4,R=16` the fixed-charge half split has ratio `3/4`, contradicting
ME2's universal `1/2`. Equal phase/director stiffness gives isolated field
ratio one, and positive half-core costs can reverse a softer-director benefit.

## Framework Compatibility

The claim is a compatible extension of C-SPN-001's projective `RP2` orbit. It
does not alter the accepted gauge-vortex sector or equate global and local
U1. The full polar manifold is separately typed as `(S2 x U1)/Z2`, whose deck
group is `Z`; the projective director quotient alone has group `Z2`.

## Dependency and Consumer Replay

The sole accepted dependency is C-SPN-001. Consumers are the additive module,
package exports, focused tests, both P068 verifiers, governance, generated
docs and memory, ME2 disposition, and future defect audits. Focused tests pass
14 tests, the primary route passes 43 checks, and the independent route passes
17 checks. The full promotion workflow passes all 541 repository tests. The
stale graph index maps no new symbol, which is treated as a limitation rather
than evidence; the direct consumer map is explicit.

## Competing Candidate Audit

Candidates B through E are selected because they jointly type the energy
domain, retain the far field, classify the two loop groups, and expose the
preference inequality. Candidate A is insufficient as a pair-energy theorem.
Candidate F survives only as the independent-copy endpoint. The source's
familiar one-half value did not select the accepted object.

## Four-Axis Decision

The evidence supports the accepted exact conditional theorem.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: depends on C-SPN-001 only for the projective polar ray orbit

## Promotion Transaction

Promotion adds C-DEF-001 to `v0.62.0`, qualifies ME2 through the disposition
source, regenerates the queue, and synchronizes implementation, tests,
campaign, registry, manifests, docs, memory, and the parent effort. Staged
impact detection, both exact verifiers, focused tests, `scripts/validate.sh`,
the full suite, and `git diff --check` pass at the promotion boundary.

## Continuation if Not Accepted

If the topology or boundary ledger fails, P068 continues with a repaired cover
or an explicit numerical multi-core PDE proposal. Source failure alone cannot
close the campaign.

## Done Gate

The claim-level debt is empty after canonical synchronization and the
541-test promotion replay. The parent migration remains active while units
are pending.

## Cross-References

See P068, ME2, C-SPN-001, `angular_defects.py`,
`test_angular_defects.py`, release `v0.61.0`, and the parent effort.
