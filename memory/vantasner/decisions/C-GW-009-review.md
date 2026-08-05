---
description: Independent review and acceptance decision for C-GW-009
author: vantasner
created: '2026-08-11T08:16:00Z'
updated: '2026-08-11T08:16:00Z'
tags:
- substrate-framework
- claim-review
- C-GW-009
category: decisions
confidence: established
status: active
---
# C-GW-009 Claim Review

## Claim Under Review

C-GW-009 gives exact kinematics and conditional TT algebra for a rigidly
rotated axisymmetric STF tensor. It preserves the full tensor's repeated
eigenvalue while deriving the aligned null, perpendicular twice-frequency
path, derivative norms and principal values, generic-tilt mixed harmonics,
and convention-safe conditional readout and power.

## Sourced Inputs

The review reads v0.132.0, C-MOM-001, C-GW-001/002/008, C-RMOM-001/002,
frozen P181, hash-pinned TX2, its complete source and check audit, the pure
module and tests, failed attempts 0003/0004/0006/0007/0009, both exact
derivations, and all dependency, consumer, candidate, compatibility, and
nonduplication evidence directly.

## Independence

The independent route imports no proposed rotation helper. It uses a matrix
exponential, a dyadic axisymmetric tensor, nested generator commutators, and a
direct transverse-plane projector. It independently reproduces every
load-bearing polynomial, norm, harmonic, readout, and power factor in ten
checks.

## Verification Status

The maximum verdict is `symbolic_verified`. The 24-check primary verifier and
10-check independent route resolve every derivative and determinant to exact
expressions with no unevaluated object. Eighty-nine focused tests and the
ten-check source graph are regression and consumer evidence, not substitutes
for the exact oracle.

## Sensitivity and Counterexamples

Setting `q=0` or `Omega=0` destroys the nonzero derivative. Using the triple
tensor with the normalized coefficient creates the expected factor-nine
power error. Replacing the axisymmetric body with `diag(q,0,-q)` removes the
repeated eigenvalue. A generic tilt exposes the fundamental that the
perpendicular special case lacks. These mutations fail the relevant verdicts.

## Framework Compatibility

The theorem is a compatible extension. It preserves all STF, TT, scale, axis,
trace, determinant, eigenvalue, unit, and zero-limit conventions. `Omega` is
explicitly declared rather than fitted or selected. The waveform and power
remain conditional on C-GW-001; no source dynamics or gravity is inferred.

## Dependency and Consumer Replay

Dependencies close through C-MOM-001 and C-GW-001/002/008. C-RMOM-001/002
enter only the TX2 application. The primary, independent, graph, and 89-test
routes pass. TX3 remains pending and inherits no blanket claim about observer
frames, rank, Omega independence, gravity, or physical radiation. No legacy
NumPy integration access exists in TX2, TX3, or the new module.

## Competing Candidate Audit

Six candidates and structural criteria were frozen before the body audit.
Invariant eigenstructure and exact conditional composition defeat the
coordinate-diagonal classification without any numerical comparator. A full
rotating-field construction remains a separate, more assumption-heavy
candidate requiring new dynamics.

## Four-Axis Decision

The four axes are independently closed for the exact scoped theorem.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: new claim with no supersedes edge

## Promotion Transaction

Promotion adds the pure rotation module and tests, C-GW-009, the P181 campaign,
v0.133.0, a qualified TX2 disposition, generated queue and docs, accepted
memory, and validated consumer closure. Every evidence path is materialized
before registry insertion.

## Continuation if Not Accepted

This section is inapplicable to the accepted exact theorem. Any claim of a
dynamically solved rotating field, selected angular speed, stability, or
physical gravity remains a separate future candidate rather than hidden debt.

## Done Gate

Accept only with the complete promotion transaction, clean integrated gate,
and empty P181 debt ledger. The scientific evidence for the scoped claim is
complete; governed synchronization remains the transaction boundary.

## Cross-References

See P181, TX2, C-MOM-001, C-GW-001/002/008, C-RMOM-001/002, the primary and
independent verifiers, source adjudication, v0.133.0, and the framework
migration effort.
