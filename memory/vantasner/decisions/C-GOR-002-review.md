---
description: Accepted review of exact Gordon canonical-scalar compatibility claim C-GOR-002
author: vantasner-review
created: '2026-08-11T06:49:00Z'
updated: '2026-08-11T06:49:00Z'
tags: [substrate-framework, claim-review, C-GOR-002, gordon-metric]
category: decisions
confidence: established
status: archived
---
# C-GOR-002 Claim Review

## Claim Under Review

C-GOR-002 is an exact local compatibility theorem for the accepted transverse
Gordon Einstein tensor and a canonical real scalar stress. For every uniform
subluminal boost, every covariant Einstein equation holds at a scalar jet
exactly on the zero-gradient, zero-potential, zero-curvature-kernel locus.
The profile condition is equivalently that the positive reciprocal index is
affine on each connected interval.

## Sourced Inputs

The review used v0.129.0, C-GOR-001, C-STG-001, C-LIN-001, the relevant
canonical APIs, both P178 proposal records, every append-only attempt,
hash-pinned SC1 and its direct graph, and the primary and independent exact
oracles. SC1's copied Gordon sign, opposite scalar-potential sign, omitted
`tx` equation, unrestricted division by velocity, and old `5/6` witness were
not imported as premises.

## Independence

The canonical route composes the accepted Gordon, scalar-stress, and linear-
system APIs. The independent route imports none of the new compatibility
module: it reconstructs Christoffels and curvature, builds the canonical
stress directly, eliminates a general nonzero boost, treats rest separately,
and differentiates the reciprocal index afresh.

## Verification Status

The claim earns `symbolic_verified`. The primary verifier passes 35 checks,
the independent derivation 14, the source graph 21, the historical C-GOR-001
verifier 29, and 53 focused tests pass. The integrated promotion boundary
validates 715 memory records and passes all 1,514 repository tests. The
nonzero branch has an explicit
nonvanishing rank-three minor; the rest branch uses the zero `tt` and `xx`
equations plus real-square nonnegativity; the remaining transverse curvature
equations force the kernel to vanish.

## Sensitivity and Counterexamples

Wrong Gordon and potential signs change the result. Active temporal and
transverse derivatives expose the omitted `tx` residual. Dropping `xx` opens
only the branch `U_x^2=-2V`, which the nonnegative cosine potential closes at
vacuum. A nonzero curvature kernel fails after scalar vacuum. Reciprocal-
affine profiles pass while an exponential index fails. The repaired symbolic
subluminal guard rejects luminal, superluminal, floating, and undecidable
inputs while admitting exact rapidity parameterizations.

## Framework Compatibility

The result preserves the accepted metric signature, component order, Gordon
coefficient, scalar-stress sign, and positive-coupling convention. It adds no
fitted constant. The theorem is algebraic and local: the scalar Euler equation
requires a stationary potential value separately, and global boundary data
remain outside the claim. No foundational revision is needed.

## Dependency and Consumer Replay

The accepted dependencies are C-GOR-001, C-STG-001, and C-LIN-001. G2 and G3
retain only their existing qualified mappings. SC1 and SC2 execute natively
with no NumPy integration-name event. SC2 remains pending and unmapped even
though its seven predicates execute, because its prose consumes SC1's old
derivation rather than the accepted theorem.

## Competing Candidate Audit

Seven candidates and structural criteria were frozen before source-body
inspection. The generic classifier duplicated C-LIN-001, accepted composition
alone omitted the new iff locus, and the proposed breather embedding lacked
four-dimensional premises. Candidate D wins through exact component closure,
rest and profile coverage, parameter economy, reusable API value, and mutation
sensitivity—not numerical agreement with SC1.

## Four-Axis Decision

The four independent governance axes all support the narrow theorem.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive theorem depending on C-GOR-001, C-STG-001, and C-LIN-001

## Promotion and Scope Ceiling

Release v0.130.0 adds C-GOR-002, its pure API and tests, the narrow symbolic
domain-guard repair, and qualified SC1 mapping. The claim does not establish a
nonvacuum source, breather embedding, complete Einstein-scalar solution,
material medium, physical gravity, observation, or substrate realization.

## Cross-References

See P178, SC1, C-GOR-001, C-STG-001, C-LIN-001,
`gordon_scalar_compatibility.py`, its focused tests, and the three P178 oracle
routes.
