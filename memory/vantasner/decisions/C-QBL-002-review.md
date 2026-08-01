---
description: Independent review of C-QBL-002
author: vantasner-review
created: '2026-08-01T16:49:00Z'
updated: '2026-08-01T16:49:00Z'
tags:
- substrate-framework
- claim-review
- exact-sine-qball
- implicit-profile
category: decisions
confidence: working
status: archived
---
# Review of C-QBL-002

## Claim Under Review

Conditional on the declared exact-sine stationary equation and `C-U1-001`,
the claim gives one unique positive first peak, the exact inverse homoclinic and
charge quadratures, and the controlled scaled limit to `C-QBL-001` without an
object or stability interpretation.

## Sourced Inputs

The review read `v0.27.0`, `C-U1-001`, `C-QBL-001`, P032, both derivation
routes, package APIs/tests, hash-pinned FG1, its five-check original failure,
compatibility-only completion, and the check-family adjudication.

## Independence

The main route uses canonical exact functions, bracketed roots, an
endpoint-regularized charge map, and direct comparison with FG1's long IVP.
The independent route derives the mechanical energy, squared-sinc
monotonicity, inverse branch, charge factor, and scaled limit without importing
the new module.

## Verification Status

Exact differentiation, limits, monotonicity witnesses, implicit
differentiation, power series, and scaling support `symbolic_verified` for the
claim. Root and quadrature evaluations validate the reusable implementation;
they do not upgrade any stability statement. FG1's source IVP is rejected as a
global charge oracle.

## Sensitivity and Counterexamples

Changing the sine normalization, cosine first-integral coefficient, or
frequency sign breaks closure. Selecting a later root crosses an interval with
negative orbit square. EM1's width misses by one-half and its unit profile
fails the exact equation. Three shrinking frequencies approach the quartic
peak and charge limits, while a finite-frequency identity is not asserted.

## Framework Compatibility

The claim is a compatible conditional extension of `C-U1-001` and
`C-QBL-001`. The exact-sine ODE and potential relation remain explicit model
premises. Current normalization, dimensionless 1+1 conventions, branch, and
frequency domain agree; the accepted real sine-Gordon field is not
complexified or identified with this profile.

## Dependency and Consumer Replay

Accepted dependencies are `C-U1-001` and `C-QBL-001`. Direct consumers are
`exact_sine_qball.py`, exports/tests, FG1's disposition, and future exact-
potential fluctuation audits. The source's long-domain IVP and VK labels are
not consumers of the accepted claim. Focused replay passes with no debt.

## Competing Candidate Audit

Candidate A was selected because global implicit existence and charge close
exactly even though the source's numeric path fails. Candidate B would discard
that valid structure. Candidate C conflicts with direct residuals and confuses
a controlled limit with finite-amplitude identity.

## Four-Axis Decision

The axes describe the conditional implicit family only.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: compatible_extension
- Epistemic: active
- Relationship: exact-potential extension and controlled limit of C-QBL-001

## Promotion Transaction

Promotion adds pure exact-sine APIs, guarded numeric quadrature/tests,
immutable P032, qualified FG1 disposition, `v0.28.0`, generated records, and
parent synchronization.

## Continuation if Not Accepted

If root or quadrature closure had failed, Candidate B would retain only the
local series. Stability requires a separate proposal with a second variation,
operator domain, theorem hypotheses, and mutation-sensitive spectral oracle.

## Done Gate

Equation provenance, root, branch, profile, charge, asymptotic limit, source
failure, separatrix guard, object boundary, consumers, disposition, and debt
closure are complete.

## Cross-References

See P032, FG1, `exact_sine_qball.py`, `C-U1-001`, `C-QBL-001`, and the parent
migration effort.
