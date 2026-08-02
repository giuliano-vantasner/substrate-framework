---
description: Independent review of C-PRB-001 exponential fixation and intensity normalization covariance
author: vantasner-review
created: '2026-08-03T16:45:00Z'
updated: '2026-08-03T16:45:00Z'
tags:
- substrate-framework
- claim-review
- fixation-probability
category: decisions
confidence: established
status: archived
---
# C-PRB-001 Claim Review

## Claim Under Review

C-PRB-001 states the exact continuous exponential-fixation family, its
conditional absorbing-boundary derivation, probability and bias properties,
implicit target preimages, and two-intensity normalization covariance. It
explicitly excludes a quantum or physical stochastic interpretation.

## Sourced Inputs

The review reads release `v0.71.0`, C-U1-002, C-OVL-001, C-DIM-008,
C-IDN-002, their canonical modules and reviews, P079's frozen contract,
attempts 0001 through 0003, the hash-pinned AS8 reproduction and source audit,
candidate comparison, impact map, new canonical module, focused tests, and
both verifier routes. AS8, pending S3, and every physical factor advertised in
the source remain noncanonical evidence rather than claim premises.

## Independence

The independent route imports no `fixation_probability`, `thermal`,
`normalized_overlaps`, `u1_charge`, or scale API. It rebuilds the neutral
limit, BVP solution, determinant, derivatives, strict-convexity factor,
symmetry, series, sign and endpoint limits, intensity parameterization, fixed-
coefficient scaling, compensating transformation, and unit normalization from
fresh SymPy expressions, then audits the immutable source AST separately.

## Verification Status

The maximum verdict is `symbolic_verified`. The primary route passes 35 exact
checks, the independent route passes 27 exact checks, and 82 affected
canonical tests pass. Attempts 0002 and 0003 preserve source-audit-only AST
predicate failures; all preceding scientific checks had passed, and the final
route inspects the exact load-line tuple. No simulation, fit, unresolved
integral, numerical quadrature, deprecated `np.trapz`, or replacement NumPy
alias is used.

## Sensitivity and Counterexamples

Changing the declared generator coefficient from `S` to `2*S` gives a nonzero
residual. Flipping `S` moves an interior probability to the opposite side of
its neutral value. The source's two amplitude examples have different raw
norms but identical unit-normalized intensities. Holding `kappa` fixed makes
`S` scale quadratically, while `kappa->kappa/lambda^2` or the corresponding
unit-normalized coefficient preserves it. These mutations separate the exact
family from the advertised absolute-scale interpretation.

## Framework Compatibility and Nonduplication

The claim is a compatible exact extension with no claim dependency. C-TH-001
contains a different normalized thermal occupation, while C-U1-002 and
C-OVL-001 address amplitude bookkeeping in different profile systems.
C-PRB-001's reusable contribution is the continuous exponential fixation BVP,
strict selection monotonicity, complement/bias structure, implicit target
preimage, and the coupled raw/normalized intensity transformation. Existing
claims serve only as interpretation ceilings and no invariant changes.

## Dependency and Consumer Replay

The theorem uses exact real calculus and separately declared domains, so its
claim dependency list is empty. C-U1-002, C-OVL-001, C-DIM-008, and C-IDN-002
cap AS8's source-specific quantum and scale readings. New consumers are package
code and exports, focused tests, P079 verification, governance records,
generated claim/release memory, and the AS8 disposition. GitNexus reports LOW
impact and no affected execution flow; direct search covers the additive
unindexed module.

## Competing Candidate Audit

Candidates B-E survive as the continuous family, conditional BVP, intensity
coordinates, and inverse-target ceiling. Candidates F and G survive as
provenance and normalization ceilings. Candidate A remains source regression
evidence only. Source examples opened after the contract freeze selected no
generator coefficient, physical normalization, parameter, or verdict.

## Four-Axis Decision

The exact evidence supports acceptance.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Dependencies: none

## Promotion Transaction

Promotion adds C-PRB-001 to `v0.72.0`, qualifies AS8 through the editable
disposition source, regenerates the queue, and synchronizes code, tests,
immutable campaign evidence, registry, release manifests, generated docs, and
accepted memory. One integrated workflow gate includes the complete pytest
suite; record-only synchronization receives targeted validation rather than a
duplicate full-suite ceremony.

## Done Gate

Claim-level debt closes only after registry, release, queue, docs, memory,
campaign, affected consumers, and integrated validation agree. The parent
migration remains active because later source units remain pending.

## Cross-References

See P079, AS8, C-U1-002, C-OVL-001, C-DIM-008, C-IDN-002,
`fixation_probability.py`, `test_fixation_probability.py`, base release
`v0.71.0`, and the parent migration effort.
