---
description: Independent review of C-BRK-001 periodic potential theorem
author: vantasner-review
created: '2026-08-02T19:45:00Z'
updated: '2026-08-02T19:45:00Z'
tags:
- substrate-framework
- claim-review
- periodic-potential
category: decisions
confidence: established
status: archived
---
# C-BRK-001 Claim Review

## Claim Under Review

C-BRK-001 states the exact value, period, Taylor data, origin curvature, and
generalized quadratic mass of the declared scalar potential
`A*(1-cos(q*x/F))` relative to a positive kinetic coefficient `K`. It also
states that a periodic cosine and a quadratic potential can share one Hessian
while differing globally. The claim excludes a physical field identity,
breaking source, coefficient, mass scale, and substrate map.

## Sourced Inputs

The review reads base release `v0.54.0`, C-SG-001, C-SYM-001, C-CHI-001, the
P061 contract and three append-only attempts, PG2 at pinned source hash
`0502a53...`, its reproduction and data-flow audit, the canonical module and
focused tests, the independent verifier, primary provenance, and the impact
report. PG2's Taylor coefficients survive only for its declared amplitude;
its physical and normalization narrative remains outside this claim.

## Independence

The independent route differentiates the potential at the origin through
sixth order and reconstructs its Taylor polynomial from derivative/factorial
data. It constructs the matched-curvature quadratic competitor directly and
tests periodic shifts and fourth derivatives. It does not import the
canonical evidence classes or PG2's expected coefficients as an oracle.

## Verification Status

The maximum verdict is `symbolic_verified`. Every promoted formula is an
evaluated exact SymPy expression. The primary route contributes 36 sensitive
checks across all three P061 claims and the independent route contributes 30;
the focused package replay passes 22 explicit-breaking and dependency tests.
No numeric approximation, unevaluated series, or physical comparator is used.

## Sensitivity and Counterexamples

Changing the amplitude sign reverses the curvature and generalized mass
squared. Changing `K` rescales mass while leaving potential curvature fixed.
Changing `q` changes the period and curvature with the derived powers. The
matched quadratic counterexample has the same Hessian but fails the periodic
shift identity and has a different fourth derivative. These mutations test
the headline objects rather than a terminal tally.

## Framework Compatibility

The claim is dependency-free declared-coordinate calculus and does not modify
C-SG-001's normalized potential. All coordinate, amplitude, scale,
multiplier, and kinetic inputs remain visible. It composes naturally with the
accepted distinction between a Hessian and `K^-1*H` and creates no physical
ontology.

## Dependency and Consumer Replay

The claim has no accepted dependencies. GitNexus reports LOW additive risk;
existing sine-Gordon and symmetry APIs are unchanged. The intended consumers
are the new package exports, focused tests, P061 verifiers, governance,
generated documentation, and later explicit-breaking audits. Full replay is
required before sealing and no unresolved consumer debt is accepted.

## Competing Candidate Audit

Candidates A through E were registered before source inspection. Candidate B
is selected for the general theorem, and Candidate D supplies the decisive
nonuniqueness guard. Candidate A is rejected because a named mass curvature
without kinetics or coefficient provenance cannot establish its physical
headline. No comparator value selected the potential.

## Four-Axis Decision

The axes support a new exact conditional theorem with no challenge or
supersession relationship.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new dependency-free declared-coordinate theorem

## Promotion Transaction

Promotion adds C-BRK-001 to the registry and release `v0.55.0`, exports and
tests the exact API, archives P061 evidence and this review, qualifies PG2,
regenerates the migration queue, and synchronizes generated docs and accepted
memory. Both exact verifiers, focused replay, registry checks, one full
workflow validation, GitNexus change detection, and `git diff --check` must
pass.

## Continuation if Not Accepted

This clause is inactive because the exact theorem is accepted. A future
physical explicit-breaking claim must independently derive its action,
coefficient, field map, dimensions, kinetic normalization, and dependency
closure; matching one Taylor coefficient is insufficient.

## Done Gate

The claim-level debt is empty after promotion replay and canonical
synchronization. The parent corpus migration remains active because later
queue units remain pending.

## Cross-References

See P061, PG2, `explicit_breaking.py`, `test_explicit_breaking.py`,
C-CHI-002, C-GMR-001, release `v0.55.0`, and the parent migration effort.
