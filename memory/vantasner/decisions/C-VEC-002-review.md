---
description: Independent review of U2 invariant metrics and vector-current sextic matching
author: vantasner-review
created: '2026-08-06T10:22:22Z'
updated: '2026-08-06T10:32:25Z'
tags:
- substrate-framework
- claim-review
- C-VEC-002
category: decisions
confidence: established
status: archived
---
# Review of C-VEC-002

## Decision

C-VEC-002 is accepted at symbolic verification in v0.156.0. It classifies the
complete positive adjoint-invariant U(2) metric family and gives a conditional
algebraic vector-current match in both source and accepted BPS conventions. It
is not a physical HLS, omega, baryon, KSRF, or parameter-value theorem.

## Evidence

The primary route solves the full invariant-form equations, reconstructs the
single-plus-double-trace family, derives the stationary vector and both lambda
conventions, exposes the nonzero kinetic-inverse residual, and tests exact
parameter families. The fresh independent route repeats those results without
importing the canonical claim APIs. The positive invariant metric
`diag(5,2,2,2)` breaks the source's forced singlet-triplet degeneracy, and
mass, coupling, current, derivative, metric, KSRF-parameter, and pi-squared
mutations are all load bearing.

## Framework Fit

Dependency closes through C-EFT-001, C-BPS-001, and C-CHI-001. C-VEC-001,
C-WZW-002, and C-TOP-002 retain their explicit ceilings. No accepted object
supplies a physical omega, rho, baryon current, `N_c`, universality, KSRF,
decay scale, medium response, or substrate map.

## Done Gate

Registry, release, implementation, tests, MK2 disposition, source graph,
generated state, and durable memory must agree at the integrated v0.156.0
promotion boundary. They do: the workflow validates 198 accepted claims, nine
pending and zero partial source units, and 877 memory records; all 1,901 tests
pass in 189.70 seconds and the complete gate exits zero in 204.35 seconds at
218,884 KiB peak RSS. The accepted claim carries no unresolved scientific
debt.
