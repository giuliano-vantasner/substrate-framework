---
description: Independent review of exact Gordon effective-metric claim C-GOR-001
author: vantasner-review
created: '2026-08-09T15:25:00Z'
updated: '2026-08-09T15:25:00Z'
tags: [substrate-framework, claim-review, gordon-metric, analog-geometry]
category: decisions
confidence: established
status: archived
---
# Review of C-GOR-001

## Claim Under Review

C-GOR-001 gives the signature-consistent mostly-plus Gordon effective metric,
its inverse, determinants, rest null speed, and the exact Einstein tensor and
Bianchi identity for a uniform z flow with transverse refractive index. It
establishes effective geometry only, not an Einstein source, material action,
physical gravity, observation, or substrate mechanism.

## Sourced Inputs

The review reads v0.108.0, the frozen P142 contract, hash-pinned G2 and dossier,
every attempt and evidence record, the canonical module and focused tests, the
fresh independent tensor reconstruction, the primary Gordon convention, and
the frozen source graph. The claim has no accepted dependency; signature,
normalized timelike four-velocity, positive index, Gordon rank-one relation,
and standard differential geometry are visible premises.

## Independence

The canonical route returns exact SymPy data from `gordon_metric.py`. The
independent reviewer does not import that module. It constructs the metric and
inverse afresh, derives Christoffels, Ricci, scalar and Einstein tensors by
direct loops, computes the mixed contracted divergence, evaluates the witness,
and independently constructs the copied-sign signature counterexample.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary source-aware verifier
passes 29 checks, the independent route passes 16, and 15 focused package tests
pass. The source graph passes 74 checks over 31 nodes and 325 predicates. All
positive obligations use exact integers, rationals, functions, and declared
real or positive symbols; no numerical quadrature or fitted parameter enters.

## Sensitivity and Counterexamples

Changing `1-n^2` to `n^2-1`, `1+n^2`, or zero breaks the exact determinant.
The copied source sign creates determinant `n^2-2`; at `n=2` its inverse metric
is positive definite. The corrected witness is `G_tt=1/6`, and mutations to
`5/6`, `-1/6`, or zero fail. Constant index gives a zero tensor. Correct static
Gordon differs from the fixed optical family at first weak-index order. A
z-independent one-plus-one scalar has `T_tz=0`, while the nonflat half-boost
geometry has nonzero `G_tz`, rejecting every scalar coupling match.

## Framework Compatibility

The result is a pure additive mathematical API and does not modify accepted
optical, sine-Gordon, stress, numeric, or unit conventions. Its explicit analog
scope prevents nonzero curvature from silently becoming Einstein dynamics.
GitNexus reports LOW risk, one new internal caller for the base constructor,
zero preexisting callers for the profile tensor, zero affected processes, and
no preexisting exact Gordon surface.

## Dependency and Consumer Replay

C-GOR-001 has no accepted dependency. The 31-node frozen graph contains G2,
B1, C1, T2C, and all 28 direct reverse consumers; it inventories 325 predicates
and passes 74 checks. Fourteen qualified consumers keep independent closures,
twelve pending consumers gain no authority, and two remain duplicate evidence.
Eight immutable compatibility shapes are alias-only and backed by
`np.trapezoid`; G2 and mutable P142 code have no compatibility event.

## Competing Candidate Audit

Literal G2 is rejected despite its six-check pass because its rank-one sign is
wrong for its declared signature. Exact kinematics and fresh curvature are
selected for complete convention, domain, parameter economy, exact limits, and
reusable API value. Source compatibility supplies a decisive rejection guard,
and constant-index, weak-index, and wrong-sign alternatives delimit the claim.
The missing material and Einstein dynamics are not replaced with a fitted
coupling or a weaker headline.

## Four-Axis Decision

The exact conditional effective-geometry surface earns acceptance while the
claimed physical Einstein-source interpretation is rejected.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new exact conditional Gordon effective-geometry theorem

## Promotion Transaction

Promotion adds the pure module and exports, focused tests, C-GOR-001, release
v0.109.0, generated records, and the qualified G2 disposition. Generated docs,
accepted memory, and the source queue are rebuilt from canonical inputs.

## Continuation if Not Accepted

This clause is inactive for the exact geometry theorem. It remains active for
the rejected physical objective: a future proposal must declare a medium and
matter action, derive its conserved stress, solve every Einstein component with
boundary data, and fix the coupling and physical dictionary independently.

## Done Gate

Convention, normalization, inverse, determinants, null cone, curvature,
Bianchi identity, limits, mutations, countermodels, source incompatibility,
independence, implementation, dependencies, consumers, compatibility,
nonduplication, source qualification, release, and generated state close with
an empty debt ledger.

## Cross-References

See P142, G2, C-OG-001, C-CC-001, C-OG-004, `gordon_metric.py`,
`test_gordon_metric.py`, the source adjudication, literature audit, impact
analysis, and frozen source graph.
