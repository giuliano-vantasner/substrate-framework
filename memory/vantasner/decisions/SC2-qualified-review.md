---
description: Qualify SC2 through an exact averaged Einstein-scalar reduction and one finite-wall branch
author: vantasner-review
created: '2026-08-11T07:12:00Z'
updated: '2026-08-11T07:12:00Z'
tags: [substrate-framework, source-review, migration-SC2, einstein-scalar]
category: decisions
confidence: established
status: archived
---
# SC2 Qualified Review

## Source Unit Under Review

SC2 executes seven predicates for a static areal metric sourced by a
phase-averaged single-harmonic canonical sine-Gordon scalar and calls the
result a closed Gordon or Horndeski PDE solve.

## Surviving Content

The averaged stress and E1, E2, and E3 structures survive after adding the
physical scale ledger and exact scope. C-STG-002 owns that exact reduction,
and C-PDE-013 owns one corrected finite-wall amplitude-three branch with full
numeric diagnostics.

## Corrected Scope

SC2.3 is induced conservation, not an independent full-system oracle. The
pointwise scalar and stress retain nonzero discarded harmonics. The source
contains no nonminimal Horndeski action, its wall is not infinity, and its
sampled family proves no global monotonicity, uniqueness, physical scale,
Gordon closure, or substrate mechanism.

## Verification and Compatibility

Primary, independent, and graph routes pass 34, 9, and 29 checks. Forty-five
focused tests pass before the integrated boundary. Mutable P179 quadrature
uses `numpy.trapezoid`; immutable QB3 and TX1 legacy spellings produce no
native stop and no scientific candidate failure.

## Four-Axis Decision

SC2 receives a qualified source disposition through individual accepted
mappings.

- Verification: symbolic evidence for C-STG-002 and numeric evidence for C-PDE-013.
- Review: audited predicate by predicate.
- Compatibility: corrected through accepted canonical action, projection, averaging, and wall semantics.
- Epistemic: qualified source evidence, not blanket source-prose promotion.
- Release: v0.131.0 adds C-STG-002 and qualified C-PDE-013.

## Closure

Qualify SC2 through C-STG-001, C-PDE-005, C-PDE-009, C-PDE-012,
C-STG-002, and C-PDE-013. Its full-PDE, independent-angular-equation,
Horndeski, exact-breather, physical-gravity, and substrate readings remain
unaccepted. TX1 stays pending and inherits no authority.
