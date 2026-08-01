---
description: Independent review of C-OG-001
author: vantasner-review
created: '2026-08-01T11:27:57Z'
updated: '2026-08-01T11:27:57Z'
tags:
- substrate-framework
- claim-review
- optical-geometry
- dilaton
category: decisions
confidence: working
status: archived
---
# Review of C-OG-001

## Claim Under Review
For every positive twice-differentiable static index `n(x)` and `c0>0`, the declared 1+1 metric `g=diag(-1/n,n/c0^2)` has Ricci scalar `R=c0^2(n n_xx-2 n_x^2)/n^3`. Its scalar wave operator satisfies `Box_g log(n)=R`. Among twice-differentiable compositions `f(n)` satisfying that identity for every profile, the complete solution is `f(n)=log(n)+C`.

## Sourced Inputs
The review read base release `v0.3.0`, P004's manifest and frozen criteria, attempt `0001`, canonical optical APIs and tests, and hash-pinned source unit T1B. The optical metric is a declared conditional model premise. The accepted sine-Gordon claims are invariants but not dependencies.

## Independence
The proposal route uses the constant determinant and independent profile-jet coefficient matching. The review route does not import the optical geometry module: it constructs every Christoffel symbol, Ricci component, scalar trace, Hessian, and scalar wave operator from the metric definition. Both routes agree for arbitrary symbolic `n(x)`.

## Verification Status
Exact SymPy identities establish the metric determinant, curvature, wave operator, and arbitrary-profile equality. Matching independent local values of `n_xx` and `n_x^2` forces `f'=1/n` and `f''=-1/n^2`; integration gives `log(n)+C`. This earns `symbolic_verified`, conditional on the explicitly declared metric.

## Sensitivity and Counterexamples
The exact predicate rejects logarithm scales 2 and -1 and a linear-in-index contamination. An arbitrary additive constant is required to pass and is separately verified as an actual symmetry, not treated as an insensitive-verifier defect. The independent route reproduces T1B's concrete `f(n)=n` failure. A 3+1 radial metric gives a nonzero residual, preventing dimensional overextension.

## Framework Compatibility
The claim is a compatible extension: it adds a conditional optical-geometry root without altering the accepted sine-Gordon sector. Positivity, differentiability, dimension, signature, and signal-speed convention are explicit. It neither asserts a matter source nor promotes an effective Newton constant.

## Dependency and Consumer Replay
Direct consumers are `src/substrate_framework/optical_geometry.py`, its package exports, and `tests/test_optical_geometry.py`; C-OG-002 depends on it. Future optical-gravity candidates must import these definitions. T1B remains partially migrated because its sourced Poisson and 3+1 narrative are not established here.

## Competing Candidate Audit
Candidates A, B, and C were frozen before implementation. A was selected for the general uniqueness result, B provides independent tensor construction, and C remains a sensitive counterexample. No comparator value influenced selection.

## Four-Axis Decision
The exact arbitrary-profile proof supports a conditional framework extension with no conflict.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: additive, with no challenge or supersession

## Promotion Transaction
Promotion freezes P004, adds importable optical APIs/tests and C-OG-001, creates release `v0.4.0`, regenerates docs/memory, marks T1B partial with its exact remainder, regenerates the migration queue, and replays all affected paths.

## Continuation if Not Accepted
Any replay failure withdraws acceptance and activates Candidate B as the primary derivation. A single concrete profile cannot replace the general quantifier.

## Done Gate
The claim gate is satisfied subject to promotion replay: the positive object and uniqueness class exist, the declared premise and quantifiers are explicit, independent tensor machinery agrees, mutations are sensitive, and no claim debt remains.

## Cross-References
See `campaigns/P004-optical-dilaton`, source unit T1B in `migration/source-claims.yaml`, `governance/claims.yaml`, and the parent migration effort.
