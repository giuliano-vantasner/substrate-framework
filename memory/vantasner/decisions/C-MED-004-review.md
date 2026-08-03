---
description: Independent review of C-MED-004 mixed-coordinate sine-Gordon ledger
author: vantasner-review
created: '2026-08-03T10:40:00Z'
updated: '2026-08-03T10:40:00Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- dimensional-analysis
category: decisions
confidence: established
status: archived
---
# Review of C-MED-004

## Claim Under Review

The claim conditionally treats `theta_z_tau=g*sin(theta)` with physical length
`z`, physical time `tau`, dimensionless `theta`, and exact positive
`g` of dimension inverse length-time. It derives the linear characteristic,
normalization family, explicit hyperbolic coordinate map, and the absence of a
unique laboratory frequency scale, while excluding a Maxwell-Bloch
derivation, optical material, gas gap, or self-induced-transparency claim.

## Sourced Inputs

The review reads release `v0.82.0`, C-SG-001, C-DIM-002, C-MED-003, and
C-SG-018, the P097 contract and attempts, MC3 reproduction and all twenty-nine
predicate decisions, the imported rung165/rung176/ME3 audit, the primary
McCall-Hahn records, and every named consumer. The optical regime, absorption
formula, H2/D2 window, 0.05-bar value, and laboratory gap remain outside the
claim.

## Independence

The independent review imports no mixed-coordinate or lattice canonical API.
It differentiates a fresh plane wave, constructs the coefficient dimensions
from base vectors, derives the reciprocal scale null direction, applies the
chain rule to a fresh nonlinear trial field, inverts the coordinate map, and
checks the static kink by exact trigonometric expansion.

## Verification Status

The maximum verdict is `symbolic_verified`. Exact differentiation,
dimensions, rank and nullspace, coordinate algebra, limits, and trigonometric
identities close the claim. The McCall-Hahn records define a literature scope
ceiling only; no textual citation or source PASS count is treated as a proof
of the promoted equations or their interpretation.

## Sensitivity and Counterexamples

Mixed-derivative sign, coefficient factor, Klein-Gordon, and squared-frequency
mutations fail. At fixed `g`, doubling the arbitrary length scale doubles the
inferred inverse-time scale, so `g` cannot be a unique laboratory gap. The
dimension vectors separately reject identifying inverse-length absorption
with either `g` or angular-frequency squared. A supplied inverse-time factor
can complete the dimensions but does not derive its value.

## Framework Compatibility

The claim is a compatible extension of C-SG-001 and C-DIM-002. The explicit
map reaches the accepted normalized hyperbolic sine-Gordon sign convention,
but mixed physical coordinates remain distinct from C-MED-003's laboratory
space-time equation and C-SG-018's Klein-Gordon spectrum. No coordinate name
or citation silently transfers a laboratory dispersion between them.

## Dependency and Consumer Replay

The dependencies are C-SG-001 and C-DIM-002. Direct consumers are the new
mixed-coordinate module, package exports, focused tests, and both P097
verifiers. Adjacent continuum and normalized tests replay. MC4, MD1, and the
engineering consumers add material, simulation, frequency, population,
radiation, or design premises and remain outside the accepted closure.

## Competing Candidate Audit

Candidates F-H were preregistered alongside the lattice alternatives before
source execution or primary-literature inspection. The direct mixed
characteristic and explicit coordinate map are selected because they close
dimensions and signs with the fewest premises. The alpha-to-gap route is
rejected structurally, not because of a failed numerical comparator.

## Four-Axis Decision

The exact conditional mixed-coordinate theorem is accepted with a strict
laboratory-frequency and optical-interpretation ceiling.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: depends on C-SG-001 and C-DIM-002 and challenges or supersedes no accepted claim

## Promotion Transaction

Promotion adds C-MED-004, the pure mixed-coordinate module and tests,
immutable P097 evidence, qualified MC3 disposition, release `v0.83.0`, and
generated docs and memory. The governance validator checks accepted registry
membership and release closure before the transaction is committed.

## Continuation if Not Accepted

This section is not invoked because the exact conditional theorem is
accepted. A self-induced-transparency or gas-frequency claim requires a
separate proposal deriving the Maxwell-Bloch reduction, physical retarded-time
normalization, coefficient imports, material regime, and laboratory
observable.

## Done Gate

The positive theorem, dependency closure, independent chain-rule derivation,
mutations, scale counterfamily, exact limits, importable API/tests, literature
ceiling, and consumer map close with an empty claim ledger. The wider corpus
migration remains active.

## Cross-References

See P097, MC3, C-SG-001, C-DIM-002, C-MED-003, C-SG-018, the mixed
sine-Gordon module, C-LAT-002, and the framework-migration effort.
