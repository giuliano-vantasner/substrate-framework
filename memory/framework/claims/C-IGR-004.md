---
description: Accepted framework claim C-IGR-004
author: framework-registry
created: '2026-08-18T15:48:27+00:00'
updated: '2026-08-18T15:48:27+00:00'
tags:
- substrate-framework
- accepted-claim
- C-IGR-004
category: claims
confidence: established
status: active
---
# C-IGR-004

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-GRV-001's independent additive inverse-coupling baseline and the accepted constant-mass one-loop coefficient families C-IGR-001..003, the derived usable total gravitational coupling is the governed renormalization condition 1/G_total=B+N*(1-6*xi)*Lambda^2*J(z)/(12*pi) with z=m2/Lambda^2 and J(z)=I2/Lambda^2 the curvature-class scale factor of the accepted family; the induced shift is taken unchanged from C-IGR-001..003 as Delta(1/G)=N*(1-6*xi)*I2/(12*pi), and B is a declared premise. Three exact substrate-internal selection legs output the usable scheme set rather than choosing it: (L1) strict spectral positivity 0<J(z)<=J(0)=1 because J is the tail integral of a strictly positive integrand (positive operator spectrum); (L2) strict monotone large-mass decoupling dJ/dz=-(tau^-1 class)<0, the tau^-1 class itself a positive-integrand integral (E1(z) sharp with exact squeeze 0<E1(z)<=exp(-z)/z, 2*K0(2*sqrt(z)) smooth); and (L3) cutoff-ontology closure, the scheme scale carrying C-GRV-001's E_cut=hbar*c/a. Sharp and smooth proper-time families pass all three; the power-subtracted family J=z*(log z+EulerGamma-1) fails L1 and L2 (sign change at the exact root z*=exp(1-EulerGamma), derivative sign change at exp(-EulerGamma)) and fails L3 (a subtraction scale mu carries no cutoff identification), so the usable set is exactly {sharp, smooth} and the power-subtracted family is retained only as the exact scale-dependence ledger. The residual scheme dependence is the exact spread ratio R(z)=J_smooth/J_sharp (=1 only at z=0, =2*e*K1(2)/(1-e*E1(1))=1.88377257808... at z=1, unbounded as z->inf); the tau^-1 higher-curvature control class is exactly -dJ/dz per scheme and bounded on the predeclared domain z>=z_min>0, the tau^-3 vacuum class is exhibited from the accepted family, and the nonlocal remainder is bounded by Lambda^-2*||R_E|| in the predeclared small-curvature domain. This is a conditional composition of accepted families, not a selected physical regulator, a unique numeric normalization, a full or nonlocal determinant, a total sign, a sourced geometry, or an empirical prediction; no observed G or Planck-scale comparator enters selection, formulas, tolerances, or tests.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GRV-001, C-IGR-001, C-IGR-002, C-IGR-003. Assumptions: Every operator, mass, determinant, local-coefficient, matching, constant-mass, and additive-baseline assumption of C-IGR-001..003 remains in force., The usable scheme set and its finite parts are outputs of the exact selection legs L1/L2/L3, not a regulator choice; no undeclared premise distinguishes sharp from smooth., The additive baseline B stays a declared premise per C-GRV-001; dimensions do not set B=0., The tau^-1 higher-curvature class is logarithmically divergent at m2=0, so the control ledger predeclares z=m2/Lambda^2>=z_min>0; the nonlocal remainder is bounded, not derived, in the declared small-curvature domain., The spread R(z) is unbounded, so no unique numeric normalization follows; the scheme bracket is the exact quoted downstream ceiling.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.162.0` with provenance `campaigns/P231-total-coupling-rung/adjudication.yaml`.

- `campaigns/P231-total-coupling-rung/verify.py`
- `campaigns/P231-total-coupling-rung/reviews/independent_total_coupling_review.py`
- `campaigns/P231-total-coupling-rung/reviews/C-IGR-004-claim-review.md`
- `campaigns/P231-total-coupling-rung/evidence/formula-freeze.yaml`
- `campaigns/P231-total-coupling-rung/evidence/candidate-comparison.yaml`
- `campaigns/P231-total-coupling-rung/evidence/dependency-audit.yaml`
- `campaigns/P231-total-coupling-rung/evidence/nonduplication-audit.yaml`
- `campaigns/P231-total-coupling-rung/attempts/0004/manifest.yaml`
- `src/substrate_framework/total_gravitational_coupling.py`
- `tests/test_total_gravitational_coupling.py`
- `memory/vantasner/decisions/C-IGR-004-review.md`
