---
description: Accepted review of exact central-radial spectral classification claim C-PDE-012
author: vantasner-review
created: '2026-08-11T06:02:00Z'
updated: '2026-08-11T06:02:00Z'
tags: [substrate-framework, claim-review, C-PDE-012, radial-spectrum]
category: decisions
confidence: established
status: archived
---
# C-PDE-012 Claim Review

## Claim Under Review

C-PDE-012 is an exact conditional theorem for real three-dimensional central
radial equations. It transports the operator, regular-origin power, and radial
norm under `chi=r*g`; calibrates the constant-vacuum Dirichlet ball with
spherical Bessel zeros; exposes the conditional threshold quadratic form; and
types a forced-zero endpoint test as non-discriminating.

## Sourced Inputs

The review read v0.128.0, C-PDE-003/004/005/006/009, the relevant package APIs,
P054's accepted-background numeric audit, both P177 proposal records,
hash-pinned BX1, all attempts, the dependency and reverse-consumer graph, and
the primary and independent oracles. BX1's hard-coded Bessel zero, sampled
global positivity, fixed-guess branch interpretation, and physical result
prose are not imported as authority.

## Independence

The canonical route uses the new pure module and the existing generic FEM for
one soluble control. The independent route imports neither BX1, the primary
verifier, nor the new module; it differentiates the transform directly, uses
the closed-form spherical `j2`, brackets its root independently, assembles a
fresh tridiagonal operator, evaluates exact trial-function forms, and checks
endpoint inequalities with rational numbers.

## Verification Status

The exact identities earn `symbolic_verified`. The primary route passes 39
checks, the independent route 22, and 103 focused package and accepted-
dependency tests pass. P054's unchanged finite-wall values remain numeric
evidence and are hash-reused instead of promoted to an exact premise.

## Sensitivity and Counterexamples

Using `chi/r^2`, centrifugal coefficients five or seven, or wall-gap powers
one or three breaks the relevant identity. A negative excess potential defeats
the threshold premise and gives a negative exact trial form. A nondecayed
unforced endpoint fails the same arithmetic tolerance that a forced zero
passes. Failed float-before-symbolic, decimal, wall-offset, registry-wording,
and resolution oracles are preserved and repaired without lowering the claim.

## Framework Compatibility

The theorem is native to C-PDE-003's three-dimensional l-mode equation and
C-PDE-005's unit far threshold, while C-PDE-009 supplies the averaged-versus-
Floquet ceiling. It changes no existing API and adds no eigensolver. C-MOD-001
and C-MOD-002 are nonduplication neighbors only, not sine-Gordon premises.

## Dependency and Consumer Replay

Direct dependencies are C-PDE-003, C-PDE-005, and C-PDE-009, transitively
C-PDE-001 and C-SG-001. The ten-node source graph passes 24 checks over 72
runtime predicates and 15 assertions. Immutable P3D2, QB3, QB4, and TX1 use
isolated aliases backed by `numpy.trapezoid`; no version event becomes a
scientific failure. SC2 and TX1 through TX3 remain pending.

## Competing Candidate Audit

Eight candidates and structural criteria were frozen before source-body
inspection. A second finite-box solver is rejected because `radial_modes.py`
already supplies one and P054 owns the scoped numeric scan. A full Floquet
problem remains distinct and unresolved. The exact theorem wins by domain
closure, soluble limits, mutation sensitivity, novelty, and assumption economy
rather than numerical closeness to BX1.

## Four-Axis Decision

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: additive theorem depending on C-PDE-003/005/009

## Promotion Transaction

Promotion adds the pure module and tests, C-PDE-012, P177 evidence, release
v0.129.0, qualified BX1 disposition, regenerated documentation and accepted
memory, and the regenerated source queue. No existing accepted claim changes.

## Scope Ceiling

The exact conditional form bound does not prove BX1's sampled premise. The
vacuum wall theorem establishes no localized half-line mode, while the
endpoint counterexample establishes only non-discrimination after a forced
zero. No averaged or Floquet mode, nonlinear deformation, all-channel
nonexistence, gravity, radiation, absolute scale, particle identity, or
substrate mechanism is accepted.

## Cross-References

See P177, BX1, C-PDE-003/004/005/006/009, P054,
`radial_spectral_classification.py`, and its focused tests.
