---
description: Accepted framework claim C-RGE-004
author: framework-registry
created: '2026-08-03T23:30:00Z'
updated: '2026-08-03T23:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RGE-004
category: claims
confidence: established
status: active
---
# C-RGE-004

## Statement
The accepted statement is reproduced exactly from the claim registry.

For a separately supplied finite family of at least two exact real inverse-coupling coordinates a_i and signed exact real coefficients b_i in the declared affine convention a_i=A+B*b_i, the rows (1,b_i) define an exact two-coordinate linear system. Composing C-LIN-001, the family has a common intersection exactly when coefficient and augmented ranks agree, and it uniquely identifies A and B exactly when the common rank is two. A pair with b_i!=b_j has the unique crossing B_ij=(a_i-a_j)/(b_i-b_j); equal coefficients with equal coordinates are coincident, while equal coefficients with unequal coordinates are parallel and disjoint. Thus a consistent rank-two family makes all distinct-pair crossings agree, whereas unequal pairwise crossings are an exact counterexample to common intersection. Under the declared reference shift a_i'=a_i-delta*b_i, A is invariant and B'=B-delta. Separately, for supplied positive electromagnetic inverse E, strong inverse S, hypercharge weight n, and signed b1,b2,b3 with D=b2+n*b1-(1+n)*b3 nonzero, the exact-matching equations a_i=A+B*b_i, a3=S, and E=a2+n*a1 have the unique inverse reconstruction B=(E-(1+n)*S)/D, A=S-B*b3, weak coordinate w=a2/E, and common-coupling boundary w_boundary=1/(1+n). This is conditional inverse inference from two supplied observations and an exact matching premise, not an ab-initio prediction. For a positive Abelian coordinate rescaling alpha1'=q*alpha1, the paired map a1'=a1/q, b1'=b1/q, and n'=q*n preserves the electromagnetic row but not an unqualified equality between the Abelian and non-Abelian coupling coordinates. Independent additive sector matching offsets can represent arbitrary supplied intercepts and therefore must remain explicit. Applied only to WM3's supplied exact readings E=1279/10, S=500/59, n=5/3, and (b1,b2,b3)=(41/10,-19/6,-7), the reconstruction gives A=1639681/39530, B=186383/39530, w=6296809/30335322, and boundary 3/8. These results derive no beta function, U1 or SU2 coefficient, physical gauge sector, simple-group embedding, normalization, matching boundary, threshold spectrum, observation, weak-angle scheme, reference scale, perturbative domain, Standard Model, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIN-001. Assumptions: Every inverse coupling, signed coefficient, provenance label, affine convention, and reference coordinate is separately supplied; exact APIs reject floating inputs., A physical inverse coupling is positive, but the algebraic intersection diagnostic permits exact real coordinates so inconsistent and nonphysical countermodels remain testable., The electroweak-form specialization assumes positive E, S, and n, nonzero D, exact common matching, and the declared relation E=a2+n*a1., The scale expression mu0*exp(2*pi*B) applies only when B is separately declared to equal log(Lambda/mu0)/(2*pi) with positive mu0., Abelian rescaling is a coordinate transformation; a physical embedding fixing q and any equality to non-Abelian coordinates are separate premises., Independent threshold or matching offsets are not assumed zero, and no perturbative validity or decoupling statement follows from affine algebra alone., The WM3 numerical specialization treats its decimal strings as exact supplied readings and imports no physical interpretation or comparator scheme.. Comparators: WM3's supplied 11561/50000 weak-angle reading was opened only after structural selection froze; it is scheme-unspecified source evidence and not a fit target or accepted observable..

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.74.0` with provenance `campaigns/P083-wm3-one-loop-running-audit/adjudication.yaml`.

- `campaigns/P083-wm3-one-loop-running-audit/verify.py`
- `campaigns/P083-wm3-one-loop-running-audit/attempts/0001/result.yaml`
- `campaigns/P083-wm3-one-loop-running-audit/attempts/0002/result.yaml`
- `campaigns/P083-wm3-one-loop-running-audit/reviews/independent_running_review.py`
- `campaigns/P083-wm3-one-loop-running-audit/evidence/source-reproduction.yaml`
- `campaigns/P083-wm3-one-loop-running-audit/evidence/source-audit.yaml`
- `campaigns/P083-wm3-one-loop-running-audit/evidence/candidate-comparison.yaml`
- `campaigns/P083-wm3-one-loop-running-audit/evidence/primary-provenance.yaml`
- `campaigns/P083-wm3-one-loop-running-audit/evidence/literature-audit.yaml`
- `campaigns/P083-wm3-one-loop-running-audit/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RGE-004-review.md`
- `tests/test_renormalization.py`
