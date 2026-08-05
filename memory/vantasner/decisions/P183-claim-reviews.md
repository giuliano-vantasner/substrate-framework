---
description: Independent review and acceptance decisions for C-FLO-001 C-ROT-001 and C-RMAP-003
author: vantasner
created: '2026-08-11T10:26:00Z'
updated: '2026-08-11T10:26:00Z'
tags:
- substrate-framework
- claim-review
- P183
category: decisions
confidence: established
status: active
---
# P183 Claim Reviews

## Claims Under Review

C-FLO-001 gives the exact finite co-rotating change of variables, periodic
monodromy, and complete finite-matrix power-boundedness criterion. C-ROT-001
classifies the exact free oblate symmetric top: a fixed transverse equilibrium
is unstable while the whole transverse equilibrium circle is stable as a set
in body angular-velocity space. C-RMAP-003 gives the exact stationary degree-
two rational-map angular Hessian, five-dimensional symmetry kernel, and
positive complement in one declared coefficient chart.

## Independence and Sensitivity

The rotating review imports no new P183 stability API and independently
derives frame transformation, Jordan counterexamples, Euler linearization,
invariants, exact nonlinear trajectory, fixed-point drift, set distance, and
density-inertia convention. The shape review rebuilds the integrand and chart,
then exactly integrates all ten gradients and 55 Hessian entries without
importing the canonical matrix. Jordan, positive-exponent, inertia-sign,
normalization, negative-curvature, nonstationary, and missing-symmetry
mutations break their intended verdicts.

## Four-Axis Decisions

All three claims are `symbolic_verified`, `accepted`,
`compatible_extension`, and `active`. None uses a supersession edge. Their
scope ceilings are claim content: finite matrices are not field operators, the
free top is not a Skyrme collective model, and the rational-map chart is not a
full-field kinetic or dynamical stability problem.

## Source Decision

TX4's unconditional rotating-B2 stability headline is unsupported. Its
nonzero nilpotent rotor generator directly refutes the inference from unit
multipliers to bounded linear powers. Its literal energy comparison proves no
fission theorem, and TX5 cannot validate it retroactively. Qualify TX4 only
through the three corrected claims and already accepted static dependencies.

## Cross-References

See P183, the three claim-level reviews, exact and independent verifiers,
source adjudication, v0.135.0, and the framework-migration effort.
