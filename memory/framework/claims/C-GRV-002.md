---
description: Accepted framework claim C-GRV-002
author: framework-registry
created: '2026-08-18T15:48:27+00:00'
updated: '2026-08-18T15:48:27+00:00'
tags:
- substrate-framework
- accepted-claim
- C-GRV-002
category: claims
confidence: established
status: active
---
# C-GRV-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Under C-IGR-004's derived usable renormalization condition 1/G_total=B+Delta with Delta=N*(1-6*xi)*Lambda^2*J(z)/(12*pi) and 0<J(z)<=1 on the usable set, the exact necessary-and-sufficient conditions for the attractive Newtonian sign 1/G_total>0 on the full declared parameter domain (positive integer N, exact xi with decidable relation to 1/6, nonnegative exact m2, positive cutoff Lambda, real baseline B, usable scheme) are: for xi<1/6, Delta>0 and the total is attractive iff B>-Delta, hence attractive for every m2>=0 iff B>=0 (the large-mass worst case J->0 fixes the uniform threshold at zero) while a negative B turns repulsive above the unique critical mass with J(z_c)=-12*pi*B/(N*(1-6*xi)*Lambda^2); for xi=1/6, Delta=0 identically (conformal point) and the total is attractive iff B>0, so the purely-induced reading B=0 lands exactly on the marginal locus 1/G_total=0 (neither attractive nor repulsive); for xi>1/6, Delta<0 and the total is attractive iff B>N*(6*xi-1)*Lambda^2*J(z)/(12*pi)>0, so only a positive baseline can produce an attractive total. The additive baseline B is a declared premise per C-GRV-001; the purely-induced reading B=0 is itself a declared premise whose exact verdict is attractive iff xi<1/6, independent of N, m2, Lambda, and usable scheme, with G_total=12*pi/(N*(1-6*xi)*J(z)*Lambda^2) for xi<1/6. The total Newton constant is the reciprocal G_total=1/(B+Delta), which preserves sign (a repulsive total returns a negative G_total, not an error) and returns no Newton constant at the marginal locus; its purely-induced value is scheme-bracketed with G_sharp/G_smooth=R(z) exactly. No unique numeric G, no observed gravity comparator, no sourced geometry, and no radiative prediction follow; comparator blinding holds.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GRV-001, C-IGR-001, C-IGR-002, C-IGR-004. Assumptions: Every C-IGR-004 assumption remains in force, including the derived usable set, the local-coefficient ceiling, and the predeclared control domain., The additive baseline B is a declared premise per C-GRV-001; the purely-induced reading B=0 is itself a declared premise, not a derived value., The total sign is exact and necessary-and-sufficient because 0<J(z)<=1 on the usable set makes sign(Delta)=sign(1-6*xi); the reciprocal Newton constant preserves this sign and is undefined only at the marginal locus., No accepted claim supplies a unique numeric normalization, a sourced field-equation solution, or an empirical gravity comparator.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.162.0` with provenance `campaigns/P231-total-coupling-rung/adjudication.yaml`.

- `campaigns/P231-total-coupling-rung/verify.py`
- `campaigns/P231-total-coupling-rung/reviews/independent_total_coupling_review.py`
- `campaigns/P231-total-coupling-rung/reviews/C-GRV-002-claim-review.md`
- `campaigns/P231-total-coupling-rung/evidence/formula-freeze.yaml`
- `campaigns/P231-total-coupling-rung/evidence/candidate-comparison.yaml`
- `campaigns/P231-total-coupling-rung/evidence/consumer-audit.yaml`
- `campaigns/P231-total-coupling-rung/attempts/0004/manifest.yaml`
- `src/substrate_framework/total_gravitational_coupling.py`
- `tests/test_total_gravitational_coupling.py`
- `memory/vantasner/decisions/C-GRV-002-review.md`
