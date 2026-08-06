---
description: Terminal qualified review of MK4 compacton perturbation
author: vantasner-review
created: '2026-08-06T11:12:00Z'
updated: '2026-08-06T11:12:00Z'
tags:
- substrate-framework
- source-disposition
- MK4
category: decisions
confidence: established
status: archived
---
# MK4 Qualified Review

## Decision

MK4 is qualified through C-BPS-001, C-BPS-002, C-BPS-003, and P107's existing
obstruction evidence. Its conditional compacton and termwise edge behavior
survive, but no new claim, API, or release is created.

## Exact Survivors and Corrections

For the declared reduced radial equation with `V=1-cos(F)`, the compacton is
`F=2 acos(r/R)` inside its support and zero outside, with
`R^3=2 sqrt(2) lambda B/mu`. The L2 edge density uses the first radial
derivative, not the queue excerpt's double-prime transcription, and has a
simple pole with coefficient two. Its cutoff integral grows as
`2R log(1/delta)`, whereas the separately audited L4 edge factors remain
finite.

## Rejected Extensions

The reduced density does not prove arbitrary-degree equality existence;
accepted claims select neither the potential nor physical couplings; bound
linearity gives energy cancellation only under attainment; finite L4 terms do
not cancel positive divergent L2 energy; and no cutoff or smoothing produces
a regulator-independent first-order coefficient. The failed perturbative
expectation therefore does not solve a boundary layer or full generalized
model. P107 already owns all exact survivors.

## Evidence and Terminal State

Nineteen primary, eight fresh independent, nine graph checks, and 22 focused
tests pass. The eleven-node graph pins 70 predicates and 13 assertions. MK4
uses current SciPy `trapezoid`; inherited E2 has only a safe current-first
fallback, so no version event becomes a scientific failure. MK5, MK6, MR2,
and MR6 remain pending without backward authority. Accepted claims, package
APIs, tests, and v0.156.0 are unchanged, so the closeout reuses P215's clean
1,901-test accepted-release boundary.

