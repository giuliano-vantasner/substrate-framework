---
description: Accepted framework claim C-DIM-008
author: framework-registry
created: '2026-08-03T11:30:00Z'
updated: '2026-08-03T11:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-DIM-008
category: claims
confidence: established
status: active
---
# C-DIM-008

## Statement
The accepted statement is reproduced exactly from the claim registry.

In M,L,T base-dimension order, the declared primitive columns c=(0,1,-1) and hbar=(1,2,-1) form the matrix [[0,1],[1,2],[-1,-1]], whose coefficient rank is two; adjoining the pure-length target (0,1,0) raises augmented rank to three, so no monomial in c, hbar, and dimensionless numbers has length dimension. Appending that target itself as a primitive a gives the full-rank matrix [[0,1,0],[1,2,1],[-1,-1,0]] and the unique target powers (0,0,1), which supplies rather than derives the length primitive and leaves its value unconstrained. Conditional on C-RGE-001's positive formal relation Lambda=mu0*exp(-X), X=8*pi^2/(b0*g^2), and a separately supplied positive inverse-energy conversion K, the length ell=K/Lambda retains mu0, K, g^2, and b0. At fixed g^2, b0, and K, the finite reference change mu0->rho*mu0 gives Lambda->rho*Lambda and ell->ell/rho while Lambda/mu0 remains exp(-X). Any supplied positive target Lambda_t or ell_t can be reproduced by choosing mu0=Lambda_t*exp(X) or mu0=K*exp(X)/ell_t respectively, so these are inverse constructions with the target as input, not absolute predictions. Separately, for a fixed positive dimensionful quantity Q=N*u, rescaling the unit standard to rho*u changes its numeric coordinate to N/rho while reconstructing the same Q; unit-coordinate covariance neither creates Q nor selects its magnitude. AS5's target-span subclaim survives, but its displayed scale contains mu0, its no-import predicate does not test mu0, and its exp(-X) label for a/xi reverses the inverse-energy orientation inherited from AS1. This ledger derives no physical beta function, coupling, reference scale, conversion, QCD, confinement, lattice, soliton, chemistry, gravity, empirical scale, or preferred unit system.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-DIM-002, C-RGE-001, C-RGE-003, C-IDN-001. Assumptions: Base-dimension rows are exactly M,L,T; primitive columns and target vectors use the declared order, and added primitives can change target membership and uniqueness., The one-loop beta function, positive reference energy, coupling squared, beta coefficient, conversion, and formal-domain qualifications remain supplied under C-RGE-001 and C-RGE-003., Reference rescaling holds the dimensionless flow inputs and conversion fixed; it is a family of admissible boundary data, not RG evolution along a running coupling., Arbitrary-target formulas are inverse constructions and require the target as an input; they do not select the target or reference physically., Unit-coordinate covariance holds one dimensionful quantity fixed while changing a positive compatible unit standard; a physical rescaling is a different operation., No accepted AS4 or later source supplies an empirical row, absolute boundary, beta coefficient, coupling value, or physical scale identification.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.69.0` with provenance `campaigns/P076-as5-scale-provenance-audit/adjudication.yaml`.

- `campaigns/P076-as5-scale-provenance-audit/verify.py`
- `campaigns/P076-as5-scale-provenance-audit/attempts/0001/result.yaml`
- `campaigns/P076-as5-scale-provenance-audit/attempts/0002/result.yaml`
- `campaigns/P076-as5-scale-provenance-audit/attempts/0003/result.yaml`
- `campaigns/P076-as5-scale-provenance-audit/reviews/independent_scale_provenance_review.py`
- `campaigns/P076-as5-scale-provenance-audit/evidence/source-reproduction.yaml`
- `campaigns/P076-as5-scale-provenance-audit/evidence/source-audit.yaml`
- `campaigns/P076-as5-scale-provenance-audit/evidence/candidate-comparison.yaml`
- `campaigns/P076-as5-scale-provenance-audit/evidence/primary-provenance.yaml`
- `campaigns/P076-as5-scale-provenance-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-DIM-008-review.md`
- `tests/test_scale_provenance.py`
