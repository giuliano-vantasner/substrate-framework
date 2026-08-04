---
description: Qualified review of W7 SU2L gauging and charged-current bridge
author: vantasner-review
created: '2026-08-10T03:55:00Z'
updated: '2026-08-10T03:55:00Z'
tags: [substrate-framework, source-review, migration-W7, nonabelian-gauge]
category: decisions
confidence: established
status: archived
---
# W7 Qualified Review

## Decision

W7 is qualified through C-NAG-001 and accepted representation, Abelian-gauge,
Maxwell, and scattering ceilings. Its conditional unprojected curvature and
charged-basis identities survive. No same-carrier SU2L gauging, physical
charged current, Yang-Mills dynamics, coupling match, mass, anomaly control,
weak boson, detector, or substrate mechanism is promoted.

## Corrected Positive Object

For `D=partial-i*g*W`, product-rule covariance requires
`W'=U*W*U_dagger-(i/g)*(partial U)*U_dagger`. It gives exact derivative and
curvature covariance, `[D_mu,D_nu]=-i*g*F_mu_nu`, and invariant trace square.
On C-REP-002's carrier, `T_a tensor P` closes and annihilates the complementary
block.

## Retained and Rejected Content

W7's plus-sign finite law breaks its convention, while CHECK1 evaluates only
the homogeneous rotation. `T_a*P_L` on the same carrier is non-Hermitian and
does not close. The source's assigned charges differ by two, its unit event is
inserted, and ladder elements do not construct a matter current. One component
square is not a varied action. `g^2=k*Z` is assigned, and left maps to right
under parity rather than being odd.

## Compatibility and Closure

Native W7 passes all eleven checks with no integration compatibility event.
Primary, independent, focused, and graph routes pass 31, 16, 19, and 61
checks; the graph pins 168 predicates and nineteen assertions. Mutable P151
and canonical code contain no legacy integration access; inherited G1, W1,
and W3 shapes remain alias-only version evidence through `np.trapezoid`.
GitNexus rates the additive API LOW risk with no callers, affected modules, or
affected flow. Pending consumers gain no physical authority.

## Cross-References

See P151, C-NAG-001, C-REP-002, C-SPN-002, C-GAU-001, C-MAX-001,
C-SCT-001, the source and predicate audits, independent derivation, and frozen
graph.
