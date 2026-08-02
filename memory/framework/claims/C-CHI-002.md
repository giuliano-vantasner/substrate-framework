---
description: Accepted framework claim C-CHI-002
author: framework-registry
created: '2026-08-02T20:00:00Z'
updated: '2026-08-02T20:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-CHI-002
category: claims
confidence: established
status: active
---
# C-CHI-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-CHI-001's Pauli convention, let U=exp(i*q*tau3*pi/F) with positive F and q, and declare the Lagrangian terms Z*Tr(partial U*partial U^dagger)+C*Tr(U-I_2), with positive Z and real C. Then Tr(U-I_2)=2*cos(q*pi/F)-2. Taking the potential as -C*Tr(U-I_2), the scalar kinetic coefficient is 4*Z*q^2/F^2, the origin potential curvature is 2*C*q^2/F^2, and the generalized quadratic mass squared is C/(2*Z), independent of q and F. In the separately declared Skyrme coefficient pair Z=F^2/16 and C=m^2*F^2/8, this generalized mass is m^2: q=1 gives kinetic coefficient 1/4 and curvature m^2/4, while q=2 gives coefficient one and curvature m^2. By contrast, pairing the q=1 kinetic coefficient 1/4 with V=m^2*F^2*(1-cos(pi/F)) gives generalized mass squared 4*m^2, and matching that V to -C*Tr(U-I_2) requires C=m^2*F^2/2, four times the declared Skyrme trace coefficient. These are convention-covariant coordinate identities. They establish no chiral action from the framework, physical pion or decay constant, derived coefficient, GMOR relation, numerical mass, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-BRK-001, C-CHI-001. Assumptions: Pauli matrices are Hermitian with Tr(tau_a*tau_b)=2*delta_ab; the group coordinate, identity matrix, and signs of Lagrangian versus potential are exactly those displayed., F, q, and Z are positive; C is a separately declared real trace coefficient; and every comparison keeps kinetic and potential terms in the same scalar coordinate., The Skyrme coefficient pair is a conditional imported model convention, not a coefficient derived from C-SG-001 or substrate dynamics., Coordinate-multiplier cancellation concerns the generalized quadratic ratio only and does not identify globally rescaled fields or actions without the displayed conversion.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.55.0` with provenance `campaigns/P061-pg2-explicit-breaking/adjudication.yaml`.

- `campaigns/P061-pg2-explicit-breaking/verify.py`
- `campaigns/P061-pg2-explicit-breaking/attempts/0002/result.yaml`
- `campaigns/P061-pg2-explicit-breaking/attempts/0003/result.yaml`
- `campaigns/P061-pg2-explicit-breaking/reviews/independent_breaking_review.py`
- `campaigns/P061-pg2-explicit-breaking/evidence/primary-provenance.yaml`
- `campaigns/P061-pg2-explicit-breaking/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-CHI-002-review.md`
- `tests/test_explicit_breaking.py`
- `tests/test_symmetry_breaking.py`
