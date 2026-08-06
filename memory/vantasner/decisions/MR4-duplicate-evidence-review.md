---
description: Terminal duplicate-evidence review of MR4 rho-saturation coupling
author: vantasner-review
created: '2026-08-06T13:28:00Z'
updated: '2026-08-06T13:28:00Z'
tags:
- substrate-framework
- source-disposition
- MR4
category: decisions
confidence: established
status: archived
---
# MR4 Duplicate-Evidence Review

## Decision

MR4 is duplicate evidence for C-VEC-001 and C-SK-001. Its leading HLS
normalization is exact and useful regression evidence, but it adds no claim,
API, or release.

## Exact ceiling

The explicit SU(2) one-form and Maurer-Cartan calculations reproduce
C-VEC-001's half-connection curvature, one-sixteenth trace factor, and leading
`e=g` normalization. Combining its conditional vector mass coordinate with
C-SK-001's common unit gives `e^2=m_V/(sqrt(a)U)`. This is a direct algebraic
composition of accepted owners, not a new theorem.

## Rejected extensions

The specialization retains supplied `a=2`, rho mass, electron mass, and the
physical field identification. The two convention readings are parameter
choices rather than an extremal bound. The source uses the leading algebraic
heavy-vector equation and therefore proves no full-vector or all-orders
statement. Its selected-token guard also omits load-bearing inputs and data
flow.

## Verification and compatibility

Thirty primary, nineteen fresh independent, and eight graph checks pass,
along with 34 focused tests. Mutating the KSRF coefficient, one-sixteenth trace
factor, or common-unit coefficient changes the relevant verdict. MR4 has no
NumPy or SciPy integration surface. Pending MR5 and MR6 use current SciPy
`trapezoid`; no version-only compatibility event is a scientific failure.
