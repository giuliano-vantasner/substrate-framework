---
description: Qualify WM7 through accepted supplied-table, representation, trace-coordinate, and affine-kinetic ceilings
author: vantasner-review
created: '2026-08-05T21:35:00Z'
updated: '2026-08-05T21:35:00Z'
tags:
- substrate-framework
- source-review
- migration-WM7
- gauge-beta
- induction-traces
category: decisions
confidence: established
status: archived
---
# WM7 Qualified Review

## Exact surviving content

For the accepted supplied three-generation table and `N_H` complex scalar
doublets, the matter contribution vector is exactly
`(4+N_H/10,4+N_H/6,4)`. It is concurrent iff `N_H=0`; `N_H=1` gives
`(41/10,25/6,4)`, integer ratio `123:125:120`, and spread `25/24`.

The two-column weight design has rank two and one consistency relation. It
recovers `c_F=2/3` and `c_S=1/3`, but the target coefficients were constructed
with those same imported weights. This is inverse reconstruction, not an
independent loop derivation.

## Boundary and interpretation ceiling

The advertised coupling ratio additionally imposes zero affine boundaries and
one common coefficient. Nonzero boundaries or independent coefficients break
it. The `25/66` coordinate further requires a common inverse-trace law and the
chosen Abelian normalization. It is not a physical weak-angle boundary.

C-REP-003 supplies the finite scalar and fermion rows, while C-MIX-002 counts a
generic phase slot; neither derives a physical scalar or generation count. A
negative gauge beta contribution does not force a negative total affine kinetic
coordinate. No determinant, regulator, counterterm, common action, matching,
physical field completeness, observed running, or substrate mechanism survives.

## Verification and compatibility

WM7 reproduces ten checks. The mutation-sensitive primary and fresh raw-SymPy
routes pass 38 and 21 checks. The 26-node terminal graph passes 67 checks over
228 static predicates and 31 assertions while excluding pending WM8 and all
reverse consumers as authority.

WM7 and mutable P204 have no quadrature surface. Immutable S2, W1, and W3
retain legacy-name syntax; those are alias-only compatibility events and cause
zero scientific failures.

## Four-axis decision

- Verification: exact symbolic evidence for supplied contributions, rank,
  scalar-count concurrence, conditional ratios, and mutations.
- Review: audited predicate by predicate and qualified.
- Compatibility: accepted composition of C-MIX-002, C-REP-001, C-REP-003,
  C-ANO-001, C-RGE-005, and C-VAC-003.
- Epistemic: qualified source evidence, not a new claim.
- Release: v0.150.0 unchanged.

## Closure

C-RGE-007 remains reserved and unpromoted. No canonical API, test, accepted
registry entry, or release claim set changes. WM7's disposition, generated
queue, campaign, and durable memory form the complete governed delta.
