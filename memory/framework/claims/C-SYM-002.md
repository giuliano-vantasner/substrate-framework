---
description: Accepted framework claim C-SYM-002
author: framework-registry
created: '2026-08-03T13:30:00Z'
updated: '2026-08-03T13:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-SYM-002
category: claims
confidence: established
status: active
---
# C-SYM-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

For explicitly positive real coordinates x and coefficients A, the map D_A(x)=A/x is an involution, every orbit has product x*D_A(x)=A, and its unique positive fixed coordinate is sqrt(A). Any supplied positive target t can be made fixed by the inverse construction A=t^2, so neither A nor t is selected by fixed-point algebra. If positive coupling coordinates beta and beta_tilde with separately supplied product P=beta*beta_tilde are exchanged and x=beta^2, the induced squared- coordinate map has A=P^2 and fixed x=P; in particular P=4*pi gives the conditional map x->16*pi^2/x and fixed coordinate 4*pi. Under a positive coordinate reparameterization x'=rho*x, conjugating the same reciprocal relation requires A'=rho^2*A, sends the numeric fixed coordinate to rho*sqrt(A), and preserves the dual-orbit structure. Generic positive x belongs to a valid off-fixed pair and is not thereby required to satisfy x=D_A(x). These exact facts establish no physical action or observable duality, no accepted coupling normalization or dual-product premise, no restriction to or mechanism selecting a self-dual subfamily, and no coupling value, beta coefficient, scale, particle interpretation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Every map coordinate, coefficient, target, dual product, and coordinate-rescaling factor used in the corresponding statement is explicitly positive and real; omitting positivity changes the fixed-point domain., The optional squared-coupling specialization assumes two separately supplied positive normalized couplings, their product P, and an exchange of those coupling coordinates; it does not derive or physically authorize that exchange., Coordinate reparameterization means conjugating one declared map by x'=rho*x; it is a convention change and not a physical RG flow or rescaling of a measured system., The arbitrary-target formula A=t^2 is an inverse construction with t as input, not a prediction or selection rule., Calling the algebra a physical duality or requiring fixed-point occupancy needs a separately accepted action or observable equivalence, domains, normalization, and selection premise.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.70.0` with provenance `campaigns/P077-as6-self-dual-coupling-audit/adjudication.yaml`.

- `campaigns/P077-as6-self-dual-coupling-audit/verify.py`
- `campaigns/P077-as6-self-dual-coupling-audit/attempts/0001/result.yaml`
- `campaigns/P077-as6-self-dual-coupling-audit/attempts/0002/result.yaml`
- `campaigns/P077-as6-self-dual-coupling-audit/attempts/0003/result.yaml`
- `campaigns/P077-as6-self-dual-coupling-audit/attempts/0004/result.yaml`
- `campaigns/P077-as6-self-dual-coupling-audit/reviews/independent_coupling_duality_review.py`
- `campaigns/P077-as6-self-dual-coupling-audit/evidence/source-reproduction.yaml`
- `campaigns/P077-as6-self-dual-coupling-audit/evidence/source-audit.yaml`
- `campaigns/P077-as6-self-dual-coupling-audit/evidence/candidate-comparison.yaml`
- `campaigns/P077-as6-self-dual-coupling-audit/evidence/primary-provenance.yaml`
- `campaigns/P077-as6-self-dual-coupling-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-SYM-002-review.md`
- `tests/test_coupling_duality.py`
