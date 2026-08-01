---
description: Independent review of C-OG-002
author: vantasner-review
created: '2026-08-01T11:27:57Z'
updated: '2026-08-01T11:27:57Z'
tags:
- substrate-framework
- claim-review
- optical-geometry
- weak-field
category: decisions
confidence: working
status: archived
---
# Review of C-OG-002

## Claim Under Review
Conditional on `C-OG-001` and the explicitly imported TF relation `n=(1+2 Phi/c0^2)^-1`, the dilaton is exactly `log(n)=-log(1+2 Phi/c0^2)` with weak-field coefficient `-2 Phi/c0^2`. The declared metric's slow coordinate-geodesic acceleration is exactly `-(1+2 Phi/c0^2) Phi_x` and, under `Phi=lambda U`, satisfies `a/lambda -> -U_x` as `lambda->0+`.

## Sourced Inputs
The review read C-OG-001's derivation and review inputs, P004 attempt `0001`, the canonical conditional index and geodesic APIs, tests, and source unit T1B. The TF relation is an assumption of this claim and is neither fitted nor promoted as a derived constitutive law.

## Independence
The proposal route differentiates the canonical TF map and uses the metric-specific API. The independent route reconstructs the connection directly from the substituted metric and evaluates `-Gamma^x_tt` without importing any proposed optical API.

## Verification Status
Exact substitution proves the nonlinear dilaton and acceleration expressions; exact one-parameter limits establish both leading weak-field coefficients. The independent Christoffel derivation agrees. The conditional mathematical statement earns `symbolic_verified`; this does not grant verification to the imported TF constitutive premise.

## Sensitivity and Counterexamples
The joint predicate accepts the coefficient pair `(2,2)` and rejects an index coefficient of 1, a sign-flipped coefficient -2, and a factor-one geodesic denominator. Thus both the potential normalization and the drift factor are load-bearing. The result reports the exact nonlinear acceleration before its weak limit, preventing a leading-order identity from being narrated as exact Newtonian motion.

## Framework Compatibility
The claim is a compatible conditional extension. `Phi/c0^2` is explicitly dimensionless, the positive-index domain is enforced for numeric calls, and no gravity-source equation or absolute coupling is introduced. It naturally composes with C-OG-001 and leaves all sine-Gordon invariants unchanged.

## Dependency and Consumer Replay
The direct dependency is C-OG-001 plus the named TF import. Consumers are the potential/index and geodesic APIs and tests. The claimed Poisson coefficient in T1B is deliberately not a consumer because its sourced equation is absent; it remains in the source-unit remainder.

## Competing Candidate Audit
Candidate A fixed the geometry and uniqueness before the conditional relation was evaluated. Candidate B independently reconstructed the drift. Candidate C's series route was used only after the structural metric choice was frozen. No empirical comparator exists.

## Four-Axis Decision
The exact conditional map is accepted without upgrading its declared constitutive input.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive, with no challenge or supersession

## Promotion Transaction
Promotion freezes P004, adds C-OG-002 and its pure APIs/tests, creates release `v0.4.0`, regenerates canonical records, and records T1B as partially migrated rather than claiming its sourced-Poisson conclusion.

## Continuation if Not Accepted
Any failure activates a direct coordinate-geodesic expansion and leaves T1B pending. The imported TF relation cannot be adjusted to rescue a normalization mismatch.

## Done Gate
The claim gate is satisfied subject to promotion replay: exact and weak conditional objects exist, the import is explicit, the independent connection agrees, mutations reject wrong coefficients, and no claim debt remains.

## Cross-References
See C-OG-001, `campaigns/P004-optical-dilaton`, source unit T1B in `migration/source-claims.yaml`, and the parent migration effort.
