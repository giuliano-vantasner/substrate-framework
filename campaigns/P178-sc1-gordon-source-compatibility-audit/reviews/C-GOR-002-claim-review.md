---
description: Independent review of exact Gordon canonical-scalar compatibility claim C-GOR-002
author: vantasner-review
created: '2026-08-11T06:47:00Z'
updated: '2026-08-11T06:47:00Z'
tags:
- substrate-framework
- claim-review
- gordon-metric
- canonical-scalar
category: decisions
confidence: established
status: archived
---
# Review of C-GOR-002

## Claim Under Review

C-GOR-002 is an exact necessary-and-sufficient local compatibility theorem.
Let `n(x)>0` be twice differentiable on a connected interval, let the accepted
mostly-plus C-GOR-001 metric have a uniform subluminal z velocity, and let a
real canonical C-STG-001 scalar depend only on `t,x`, with real potential value
`V` and positive coupling `kappa`. Then `G_ab=kappa*T_ab` in every covariant
component exactly when `U_t=U_x=V=K=0`, where
`K=(n*n_xx-2*n_x^2)/n^2`. The kernel condition is equivalent to
`(1/n)_xx=0`, so the positive reciprocal index is affine on the interval. The
claim is a local algebraic and profile classifier, not a breather, material,
or physical-gravity solution.

## Sourced Inputs

The review reads v0.129.0, the freeze commit `c9a472c`, both P178 proposal
states, every append-only attempt, hash-pinned SC1, C-GOR-001, C-STG-001,
C-LIN-001, the canonical modules, 53 focused tests, the primary and independent
verifiers, the four-node source replay, and every source, dependency,
consumer, compatibility, nonduplication, candidate, impact, and provenance
record. SC1's old metric, wrong stress sign, omitted `tx`, rest omission,
Guard A, `5/6`, SC2 authority, and physical prose remain outside the delta.

## Independence

The canonical route composes `gordon_metric.py`, `einstein_scalar.py`, and
`linear_systems.py`. The independent reviewer imports none of the proposed
compatibility code. It reconstructs Christoffels, Ricci and Einstein tensors,
forms the canonical stress directly, derives a fresh general-velocity
coefficient matrix and minors, closes the rest branch separately, and
differentiates the reciprocal index afresh.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary route passes 35 exact
checks, the independent route passes 14, the four-node source graph passes 21,
the historical C-GOR-001 verifier passes 29, and 53 focused tests pass. The
nonzero-boost proof has an explicit nonzero rank-three minor; the rest proof
uses the exact zero `tt` and `xx` equations plus nonnegative real squares; the
fresh rest curvature shows the remaining `yy,zz` equations force `K=0`.
There are no unevaluated symbolic objects, float inputs, numerical tolerances,
or empirical comparators in the claim.

## Sensitivity and Counterexamples

Wrong Gordon coefficient signs recreate the spurious pole and rejected `5/6`.
The wrong potential sign changes every zero-gradient stress component. An
active temporal and transverse derivative makes the omitted `tx` residual
nonzero. Dropping `xx` changes the canonical algebraic family to
`U_x^2=-2V`, disproving SC1 Guard A for a nonnegative cosine potential.
Positive rest-square mutations fail, a nonzero curvature kernel fails after
the scalar vacuum, and an unsimplified symbolic margin used to reject a valid
subluminal parametrization. Reciprocal-affine profiles pass, while `n=e^x`
has `K=-1` and fails.

## Framework Compatibility

The theorem preserves the accepted mostly-plus signature, coordinate order,
Gordon convention, canonical stress sign, coupling positivity, and analog-
geometry ceiling. It adds no fitted constant or free parameter. The one guard
repair simplifies the already-required positive subluminal margin; it does not
admit float, luminal, superluminal, complex, or undecidable speeds. The claim
requires no foundational revision.

## Dependency and Consumer Replay

Accepted dependencies are C-GOR-001, C-STG-001, and C-LIN-001. G2 and G3
remain individually qualified through their accepted mappings. SC1 and SC2
execute natively without any trapezoid-name compatibility event. SC2 is the
only direct source reverse consumer; its seven checks pass, but it remains
pending without accepted mappings because its prose imports SC1's noncanonical
derivation. Focused package tests and the P142 verifier pass, and the debt
ledger is empty.

## Competing Candidate Audit

Seven candidates were frozen after acknowledging queue exposure. Literal SC1
was retained as evidence only; accepted composition alone lacked the new
if-and-only-if locus; the generic tensor classifier duplicated C-LIN-001; the
one-plus-one embedding lacked transverse and dimensional premises; and no
backward-defined effective matter source was admitted. Candidate D wins on
accepted-object fidelity, exact component closure, rest and profile coverage,
zero new parameters, reusable API value, and mutation sensitivity—not on
agreement with SC1's advertised conclusion.

## Four-Axis Decision

The exact compatibility locus earns acceptance as a new compatible extension.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new theorem depending on C-GOR-001, C-STG-001, and C-LIN-001

## Promotion Transaction

Promotion adds the pure compatibility module and tests, the narrow Gordon
domain-guard repair, C-GOR-002, release v0.130.0, generated records, durable
claim and source decisions, and a qualified SC1 disposition mapped to
C-GOR-001, C-STG-001, and C-GOR-002. The queue must be regenerated from
`migration/dispositions.yaml`; SC2 remains pending. Targeted scientific routes,
one integrated `scripts/validate.sh`, and `git diff --check` are required.

## Continuation if Not Accepted

This clause is inactive for C-GOR-002. It remains active for SC2 and for any
physical Gordon or scalar-tensor realization: each needs its own frozen
campaign, action, conserved source, componentwise equations, boundary data,
solver evidence, scale, and consumer replay.

## Done Gate

The exact positive locus, accepted dependency closure, source adjudication,
independent derivation, mutations, known limits, importable implementation,
tests, consumer replay, compatibility classification, claim review, and empty
debt ledger pass. Governance materialization now agrees across claim, release,
SC1 disposition, regenerated queue, generated docs, and durable memory; the
integrated promotion gate validates 715 memory records and passes all 1,514
repository tests.

## Cross-References

See P178, SC1, C-GOR-001, C-STG-001, C-LIN-001, the primary verifier,
independent review, source graph, source adjudication, compatibility module,
focused tests, and the framework-migration effort.
