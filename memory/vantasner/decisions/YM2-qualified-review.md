---
description: Qualified review of YM2 Yang-Mills dimensional-lift bridge
author: vantasner-review
created: '2026-08-10T15:25:00Z'
updated: '2026-08-10T15:30:00Z'
tags: [substrate-framework, source-review, migration-YM2, dimensional-lift]
category: decisions
confidence: established
status: archived
---
# YM2 Qualified Review

## Decision

YM2 is qualified through C-NVP-001, C-KRN-001, and C-KRN-002 with no new claim,
API, or release. Its exact trace and fixed-input Riesz arithmetic survives; its
claimed Yang--Mills and 3+1-dimensional lift does not.

## Corrected Positive Object

For independently supplied inputs, the fundamental SU2 trace metric can be
tensored with the accepted scalar Riesz Green function and differentiated
radially. This is exact accepted composition. It does not transport the
two-dimensional loop theorem, select the dimension or exponent, or construct
a gauge action or spacetime propagator.

## Retained and Rejected Content

YM2 multiplies an already inverted scalar kernel by the trace metric. A
trace-weighted quadratic operator instead inverts with the reciprocal metric,
giving a factor-of-four counterexample in the fundamental normalization. The
source has no action, time operator, signature, gauge fixing, source, boundary
prescription, kinetic normalization, dimension selection, or nonlinear
covariant completion. Its force, Abelian-limit, FFT, weak-sector, and substrate
readings are therefore not promoted.

## Compatibility and Closure

Native YM2 stops at an eager legacy NumPy fallback. An isolated alias backed by
`np.trapezoid` passes all ten predicates; this is version-only provenance, not
scientific failure or support. Primary, independent, focused accepted-API, and
frozen-graph routes pass 31, 20, 37, and 27 checks or tests, with the graph
replaying 165 immutable predicates across sixteen units. No accepted consumer
or release changes.

## Cross-References

See P159, C-NVP-001, C-KRN-001, C-KRN-002, the predicate and source audits,
independent inversion review, semantic graph, impact analysis, and v0.123.0.
