---
description: Accepted framework claim C-GTR-001
author: framework-registry
created: '2026-08-02T22:00:00Z'
updated: '2026-08-02T22:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-GTR-001
category: claims
confidence: established
status: active
---
# C-GTR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-WID-001's distinction between zero-transfer and pion-pole couplings, let m_pi^2 and g0 be positive and declare the regular expansion G_piNN(-m_pi^2)=g0-s*m_pi^2+R*m_pi^4 together with the separate zero-transfer relation M*g_A=F*g0. The discrepancy Delta=1-M*g_A/(F*G_piNN(-m_pi^2)) then equals m_pi^2*(-s+R*m_pi^2)/(g0-s*m_pi^2+R*m_pi^4), has leading coefficient -s/g0, and tends to zero in the chiral limit. A square-root coupling counterexample proves that current conservation without the regularity premise does not force mass-squared scaling. Separately, the supplied monomial equation g_piNN*F=g_A*M has exponent row (1,1,-1,-1), rank one, and a three-dimensional nullspace; exact common-scale, inverse-decay/coupling, and inverse-mass/axial rescalings preserve it. Solving this equation for g_A or g_piNN is therefore invertible bookkeeping, not prediction. This exact conditional theorem derives no discrepancy coefficient, physical parameter, EFT, QCD relation, state dictionary, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-WID-001. Assumptions: The zero-transfer relation is separately imposed, the coupling expansion is regular in m_pi^2 with finite supplied coefficients, and its denominator is nonzero in the evaluated neighborhood., The discrepancy definition uses the stated zero-transfer and pion-pole evaluation points; a different sign, coupling definition, or normalization requires a new derivation., The monomial inputs and rescaling parameter are positive and otherwise independent; the nullspace families demonstrate nonidentifiability rather than physical symmetries., No phenomenological value or pending PG4, S1, or S2 premise enters the relation, expansion, coefficient, or rank calculation.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.57.0` with provenance `campaigns/P063-pg4-goldberger-treiman/adjudication.yaml`.

- `campaigns/P063-pg4-goldberger-treiman/verify.py`
- `campaigns/P063-pg4-goldberger-treiman/attempts/0001/result.yaml`
- `campaigns/P063-pg4-goldberger-treiman/attempts/0005/result.yaml`
- `campaigns/P063-pg4-goldberger-treiman/reviews/independent_axial_review.py`
- `campaigns/P063-pg4-goldberger-treiman/evidence/primary-provenance.yaml`
- `campaigns/P063-pg4-goldberger-treiman/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-GTR-001-review.md`
- `tests/test_axial_ward.py`
