---
description: Independent review of C-GLS-001 exact declared-covariance residual ledger
author: vantasner-review
created: '2026-08-03T00:36:00Z'
updated: '2026-08-03T00:36:00Z'
tags:
- substrate-framework
- claim-review
- generalized-least-squares
category: decisions
confidence: established
status: archived
---
# C-GLS-001 Claim Review

## Claim Under Review

C-GLS-001 states the unique exact generalized least-squares estimator for a
full-column-rank design and separately declared symmetric positive-definite
covariance, together with its fitted vector, residual projector, normal
residual, quadratic residual, and residual degrees of freedom. It assigns no
sampling distribution, significance, model adequacy, physical independence,
or absolute scale.

## Sourced Inputs

The review reads C-LIN-001, P065's frozen uncertainty candidate, attempts 0003
through 0005, the primary-provenance inventory, canonical API and focused tests,
and both exact verifier routes. OD and AS4 provide neither a covariance nor
actual observation column and therefore do not instantiate this theorem.

## Independence

The independent review imports no GLS implementation. It differentiates the
exact quadratic form directly, proves positive curvature, derives the normal
orthogonality and residual degrees, inverts a symbolic two-row correlated
covariance, and identifies its singular boundary from the determinant.

## Verification Status

The verdict is `symbolic_verified`. All displayed matrices and results are
exact SymPy objects. The API refuses floating, nonsymmetric, singular,
indefinite, dimension-mismatched, and missing-provenance covariance inputs and
refuses rank-deficient designs because no generalized inverse or prior is part
of the claim.

## Sensitivity and Counterexamples

For two equal-coefficient rows with observations one and three and identity
covariance, the exact estimator is two, residual is `(-1,1)`, chi-square is
two, and one residual degree remains. Setting correlation to one-half leaves
the estimator and coefficient rank unchanged but raises the anti-common-mode
quadratic residual to four. At correlation one the covariance is singular and
the theorem refuses it. Rescaling the diagonal covariance changes chi-square,
so the verdict is sensitive to its load-bearing error model.

## Framework Compatibility

The theorem is a compatible mathematical extension depending on C-LIN-001's
exact rank semantics. Row and covariance provenance are mandatory. Shared
inputs belong in the covariance; distinct labels or narrative routes are not
independence evidence. The result cannot promote OD or AS4 without accepted
physical rows, observations, coefficients, and a governed stochastic model.

## Dependency and Consumer Replay

The accepted dependency is C-LIN-001. Consumers are the new pure module,
focused tests, P065 exact reviews, governance and generated records, and future
uncertain scale audits. Post-change graph detection reports only new internal
scale-module flows, and the full promotion workflow passes all 501 repository
tests before commit.

## Competing Candidate Audit

Candidate D is selected because it exposes the covariance, estimator, residual,
and degrees of freedom without converting agreement into a derivation or
assigning an undeclared distribution. Candidate A has no uncertainty model and
cannot support this claim. The AS4 row count did not select the GLS form.

## Four-Axis Decision

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new exact conditional GLS ledger depending on C-LIN-001

## Promotion Transaction

Promotion adds C-GLS-001 to `v0.59.0` within P065's atomic synchronization.
The primary and independent exact routes, focused tests, graph audit, full
workflow gate, and diff checks must pass.

## Continuation if Not Accepted

This clause is inactive after the promotion gate. Rank-deficient, stochastic,
Bayesian, nonlinear, or empirical applications require separately reviewed
claims and explicit priors, distributions, solvers, and validation.

## Done Gate

The claim-level debt is empty only after synchronized promotion. Corpus-level
work remains active while later migration units are pending.

## Cross-References

See P065, C-IDN-001, C-LIN-001, `scale_constraints.py`,
`test_scale_constraints.py`, release `v0.59.0`, and the parent migration effort.
