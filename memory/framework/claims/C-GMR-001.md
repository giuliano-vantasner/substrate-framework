---
description: Accepted framework claim C-GMR-001
author: framework-registry
created: '2026-08-02T20:00:00Z'
updated: '2026-08-02T20:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-GMR-001
category: claims
confidence: established
status: active
---
# C-GMR-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on positive quark-mass sum m_q, positive decay scale F, positive convention factor c, negative condensate Sigma, and the separately declared relation M^2*F^2=-c*m_q*Sigma, exact solution gives M^2=-c*m_q*Sigma/F^2>0. Holding the other inputs fixed, its logarithmic sensitivities with respect to m_q, Sigma, F, and c are respectively 1, 1, -2, and 1, and M^2 tends to zero as m_q tends to zero. If m_q, Sigma, F, and c have mass dimensions 1, 3, 1, and 0, both sides have mass dimension four. For every positive rho, replacing F by rho*F and Sigma by rho^2*Sigma leaves M^2 unchanged, so the relation alone does not determine its inputs or a numerical mass. This exact conditional parameter ledger does not derive GMOR, a chiral current or vacuum, a condensate convention or value, a decay constant, quark masses, a physical pion identity, QCD dynamics, or a substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The displayed GMOR-form relation is an approved conditional premise for this algebraic claim rather than a framework derivation., The quark-mass sum, decay scale, and convention factor are positive, the condensate is negative, and the mass-dimension assignments are exactly those stated., Logarithmic sensitivities vary one nonzero input at a time while holding the others fixed; they do not describe an RG flow or correlated physical family., The positive-rho rescaling is an identifiability counterexample and supplies no physical transformation law for a condensate or decay constant.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.55.0` with provenance `campaigns/P061-pg2-explicit-breaking/adjudication.yaml`.

- `campaigns/P061-pg2-explicit-breaking/verify.py`
- `campaigns/P061-pg2-explicit-breaking/attempts/0002/result.yaml`
- `campaigns/P061-pg2-explicit-breaking/attempts/0003/result.yaml`
- `campaigns/P061-pg2-explicit-breaking/reviews/independent_breaking_review.py`
- `campaigns/P061-pg2-explicit-breaking/evidence/primary-provenance.yaml`
- `campaigns/P061-pg2-explicit-breaking/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-GMR-001-review.md`
- `tests/test_explicit_breaking.py`
