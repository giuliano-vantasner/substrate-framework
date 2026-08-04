---
description: Qualified review of QCD2 SU3 dimensional-lift bridge
author: vantasner-review
created: '2026-08-10T17:55:00Z'
updated: '2026-08-10T18:00:00Z'
tags: [substrate-framework, source-review, migration-QCD2, dimensional-lift]
category: decisions
confidence: established
status: archived
---
# QCD2 Qualified Review

## Decision

QCD2 is qualified through C-LIE-003, C-NVP-002, C-KRN-001, and C-KRN-002 with
no new claim, API, or release. Its exact SU3 trace and fixed-input Riesz
arithmetic survives; its claimed Yang--Mills and 3+1-dimensional lift does not.

## Corrected Positive Object

For independently supplied inputs, the standard fundamental SU3 trace metric
can be tensored with the accepted scalar Riesz Green function and differentiated
radially. This is exact accepted composition. It does not transport the
two-dimensional loop theorem, select the dimension or exponent, or construct a
gauge action or spacetime propagator.

## Retained and Rejected Content

QCD2 multiplies an already inverted scalar kernel by the trace metric. A
trace-weighted quadratic operator instead inverts with the reciprocal metric,
giving a factor-of-four counterexample in the fundamental normalization. The
source has no action, dimension map, time operator, signature, gauge fixing,
source, boundary prescription, kinetic normalization, or dimension selection.
Its force, Abelian-limit, FFT, physical-color, and substrate readings are not
promoted.

## Compatibility and Closure

Native QCD2 stops at an eager legacy NumPy fallback. An isolated alias backed by
`np.trapezoid` passes all ten predicates; this is version-only provenance, not
scientific failure or support. Primary, independent, focused accepted-API, and
frozen-graph routes pass 33, 21, 53, and 25 checks or tests, with the graph
replaying 135 immutable predicates across thirteen units. No accepted consumer
or release changes.

## Cross-References

See P161, C-LIE-003, C-NVP-002, C-KRN-001, C-KRN-002, the predicate and source
audits, independent inversion review, semantic graph, impact analysis, and
v0.124.0.

