---
description: Qualify TX1 through exact conditional factorization and one corrected numeric branch
author: vantasner-review
created: '2026-08-11T07:43:00Z'
updated: '2026-08-11T07:43:00Z'
tags: [substrate-framework, source-review, migration-TX1, rational-map]
category: decisions
confidence: established
status: archived
---
# TX1 Qualified Review

## Source Unit Under Review

TX1 executes nine predicates for the intrinsic rank-two energy moment of
declared B1, B2, and B4 rational-map configurations and promotes the B2 result
as a unique physical carrier.

## Surviving Content

The displayed conditional local density, exact B1 null, exact B2 axial form
and sign, and one corrected B2 stationary-branch magnitude survive through
C-RMOM-001 and C-RMOM-002. The accepted tail exponent remains C-RPROF-001.

## Corrected Scope

TX1 computes normalized I_STF but calls it Q, has an R-squared monopole-tail
error, couples wall and mesh changes, and lacks an independent solver. B4 is a
numeric null only. No exact cubic or minimal-map theorem, unique physical
carrier, full field, conserved stress, absolute scale, physical state,
rotation, gravity, waveform, or radiation is accepted.

## Verification and Compatibility

Primary, independent, and focused routes pass 21, 9, and 54 checks or tests.
The exact sign is comparator-free and corrected numerical methods agree within
`2.865e-7` relative. TX1 runs natively through `numpy.trapezoid`; its isolated
legacy spelling creates no version failure or scientific rejection.

## Four-Axis Decision

TX1 receives a qualified source disposition through individual accepted
mappings.

- Verification: symbolic evidence for C-RMOM-001 and numeric evidence for C-RMOM-002.
- Review: audited predicate by predicate.
- Compatibility: corrected through accepted rational-map, radial-profile, and STF conventions.
- Epistemic: qualified source evidence, not blanket source-prose promotion.
- Release: v0.132.0 adds C-RMOM-001 and qualified C-RMOM-002.

## Closure

Qualify TX1 through C-RMAP-001, C-RPROF-001/002, C-MOM-001/003, and
C-RMOM-001/002. Every stronger physical or unique-carrier reading remains
unaccepted. TX2 and TX3 stay pending and inherit no blanket authority.
