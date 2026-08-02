---
description: Independent review of C-WZW-002 SU3 pi5 period and sphere level
author: vantasner-review
created: '2026-08-02T16:00:00Z'
updated: '2026-08-02T16:00:00Z'
tags:
- substrate-framework
- claim-review
- su3-period
category: decisions
confidence: established
status: active
---
# C-WZW-002 Claim Review

## Claim Under Review

The claim adds an explicit primitive `S5->SU3` map, an independently certified
degree witness, the exact period of C-WZW-001's real trace-five form, and the
conditional coefficient lattice for two five-ball fillings of an `S4`
boundary. It excludes general five-manifold and physical identifications.

## Authority and Independence

The review uses v0.50.0, C-WZW-001, C-LIE-001, the frozen P057 contract, the
hash-pinned WZ2 source, and primary Puttmann-Rigas and Bott topology sources.
The explicit generator formula and degree criterion come from
Puttmann-Rigas, but P057 independently proves SU(3) membership and calculates
both oriented regular-value Jacobians. The trace period is derived from the
accepted form after the generator class is fixed; Hu-Hu's matching period is a
post-gate comparator, not an input.

The numerical reviewer imports no canonical WZW map or period helper. It
reimplements the primary formula, uses finite differences instead of symbolic
differentials, and integrates all five coordinates by Gauss-Legendre cubature.

## Verification and Sensitivity

Exact polynomial identities give determinant one and unitarity on the sphere.
The two preimage determinants `8,8` give column degree `+2`, which the audited
generator theorem converts to primitive class `+1` without inspecting a WZW
integral. Equivariance reduces the period to one exact tangent calculation:
raw density `-480*i`, real density `-480`, sphere volume `pi^3`, and real period
`-480*pi^3`.

Central-difference errors converge quadratically, and independent cubature
converges to the exact period with final relative error below `6e-4`. Reversing
orientation flips the sign. Rescaling a tangent, removing `-i`, halving the
period, halving the level, and using irrational or half-integer levels all
break the relevant verdict.

## Source Qualification

WZ2's clean tally is not an oracle. Its projector map has determinant
`exp(iF)`, its suspension of `CP2` is not `S5`, its generator label is circular,
its doubling check multiplies a stored integral by `nwind`, and its coarse
grid uses `round` without finite-difference refinement or an independent
method. The surviving phase mechanism is promoted only through P057's exact
replacement.

## Four-Axis Decision

- Verification: `symbolic_verified`, with independent converged numeric evidence
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Dependency: `C-WZW-001`
- Relationship: no challenge or supersession

## Scope Ceiling

The theorem applies to sphere ambiguities produced by two five-ball fillings.
It does not assert the primitive homology period on arbitrary closed
five-manifolds or silently add spin/bordism hypotheses. The integer label is
not `N_c`, a baryon number, an anomaly coefficient, or a representation rule.
No physical WZW action or substrate mechanism follows.

## Done Gate

Acceptance requires the exact and independent verifiers, focused tests,
source qualification, impact replay, release and generated synchronization,
one final repository validation, full pytest, `git diff --check`, and an empty
P057 debt ledger.
