---
description: Terminal duplicate-evidence review of MR2 BPS normalization correction
author: vantasner-review
created: '2026-08-06T12:31:00Z'
updated: '2026-08-06T12:31:00Z'
tags:
- substrate-framework
- source-disposition
- MR2
category: decisions
confidence: established
status: archived
---
# MR2 Duplicate-Evidence Review

## Decision

MR2 is duplicate evidence for C-BPS-001, C-VEC-002, and C-GSK-001. Its
pi-squared correction is exact and useful provenance, but it does not add a
claim, API, or release.

## Exact ceiling

The normalized hedgehog density is C-BPS-001's degree-one specialization. For
one common normalized current, positive-root elimination gives
`lambda_A=pi^2*lambda_BPS`, already owned by C-VEC-002 and C-BPS-001. The two
reduced `c6` coordinates are already C-GSK-001. MR2's reduced square completion
eliminates to the same `2*lambda_A*mu*W` coefficient and is dependent regression
evidence rather than an independent oracle.

## Rejected extensions

The corrected expression retains supplied `N_c`, pion mass, and degree. Its
99.417 MeV value also assumes unaccepted coupling maps and equality attainment,
so it is not a zero-parameter physical baryon mass or a ten-percent sector
contribution. The selected-token AST guard is not complete comparator or
dependency provenance, and no physical compacton-radius correction follows.

## Verification and compatibility

Twenty-five primary, eighteen fresh independent, and ten graph checks pass,
along with 64 focused tests. Current rescaling, normalization, missing
pi-squared conversion, wrong-coordinate, and nonattainment mutations all change
the relevant verdict. MR2 has no NumPy or SciPy integration surface. Pending
MR3, MR5, and MR6 use current SciPy `trapezoid`; immutable legacy aliases remain
compatibility provenance only.
