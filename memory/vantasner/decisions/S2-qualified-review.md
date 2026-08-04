---
description: Qualified review of S2's hedgehog fluctuation and meson-spectrum source claim
author: vantasner-review
created: '2026-08-09T09:00:00Z'
updated: '2026-08-09T09:00:00Z'
tags: [substrate-framework, source-review, migration-S2, radial-spectrum]
category: decisions
confidence: established
status: archived
---
# S2 Qualified Review

## Decision

S2 is qualified through C-MOD-001, C-MOD-002, C-SCL-001, C-SG-002, and
C-SK-001. Provisional C-MES-001 is not promoted because no distinct
dependency-closed meson theorem remains.

## Corrected Positive Object

The accepted complete radial Hessian contains the mixed correction omitted by
S2 and has exact massless continuum edge zero. Corrected finite-box levels fall
from 0.131132 to 0.061072 to 0.034754 as the wall grows from 12 to 24, with
wall-squared scaling and controlled residuals. This positively identifies the
calculation as a wall-quantized continuum ladder, not a bound breathing mode.

The complete inertia shape functional converges to 6.37234; S2's 5.8853
excludes the core and leading tail. Its 293 MeV check does not use either value
and instead evaluates a moment of inertia fitted to the same target splitting.

## Retained and Rejected Content

The stationary profile, finite-difference EOM evidence, conditional rotor
arithmetic, C-SG-002 energy expression, and C-SK-001 cancellation survive only
under their declared ceilings. S2 derives no collective action,
Finkelstein-Rubinstein state assignment, complete fluctuation channels,
half-line bound state, phase shift, resonance pole or width, vacuum meson mass,
quantization, particle identity, absolute scale, or substrate mechanism.

## Compatibility and Closure

Native S2 aborts on three removed NumPy attribute calls before its first check.
An isolated alias backed by `np.trapezoid` reproduces all ten predicates without
altering the source hash; this is compatibility provenance, not scientific
failure or evidence. Primary, independent, graph, and focused-test routes pass
27, 18, 45, and 90 checks respectively. No canonical code or release changes.

## Cross-References

See P138, its predicate adjudication, source audit, literature audit, impact
analysis, and frozen 20-node dependency/consumer graph.
