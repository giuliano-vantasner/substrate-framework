---
description: Accepted framework claim C-OVL-001
author: framework-registry
created: '2026-08-03T06:00:00Z'
updated: '2026-08-03T06:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-OVL-001
category: claims
confidence: established
status: active
---
# C-OVL-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

For any whole-line L2 mode eta normalized by integral_R |eta|^2 dx=1 and any supplied bounded real multiplication profile Phi with essential range Phi_min<=Phi<=Phi_max, its expectation y=integral_R |eta|^2*Phi dx obeys Phi_min<=y<=Phi_max. For positive p,r,kappa and real A, if eta is proportional to sech(kappa*x)^p and Phi=A*sech(kappa*x)^r under Cartesian dx, then normalization gives the exact matched-width overlap y=A*Gamma(p+r/2)*Gamma(p+1/2) /(Gamma(p)*Gamma(p+r/2+1/2)); the common kappa cancels, but A does not. The p=2,r=1 value is 9*pi*A/32. For C-QBL-003's actual unnormalized even sech^2 and odd sech*tanh modes against A*sech at the same width, the normalized squared-density expectations are respectively 9*pi*A/32 and 3*pi*A/16, their ratio for common A is 2/3, and the weighted even-odd cross expectation vanishes by parity. After L2 normalization y has the mass dimension of Phi. A separately declared product m=y*v has the sum of the supplied profile and scale dimensions; a common v cancels from mass ratios, while independent amplitudes remain, and y->rho*y with v->v/rho leaves m invariant. These exact conditional expectation and parameter results derive no fermion, Yukawa interaction, physical condensate or VEV, generation assignment, hierarchy, mixing, absolute mass, radial-measure formula, Standard-Model map, or substrate mechanism. C-QBL-003's negative and zero Hessian eigenvalues remain non-mass objects but do not uniquely select this overlap functional.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-QBL-003. Assumptions: General expectation bounds require a normalized complex or real L2 density and the declared almost-everywhere essential bounds of a real multiplier profile., The gamma ratio uses Cartesian whole-line dx, positive mode and multiplier powers, one shared positive inverse width, and a separately supplied real amplitude., The two concrete mode formulas use exactly C-QBL-003's conditional scalar-Hessian shapes and the separately declared even A*sech multiplier; they do not assign particle or flavor semantics., Every dimension, amplitude, external scale, and comparison convention is supplied explicitly; positivity follows only when the multiplier amplitude and external scale have the required signs., Mismatched widths, radial measures, hierarchy, mixing, and physical interaction or mass interpretations require separate claims.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.64.0` with provenance `campaigns/P070-mh1-normalized-overlap/adjudication.yaml`.

- `campaigns/P070-mh1-normalized-overlap/verify.py`
- `campaigns/P070-mh1-normalized-overlap/attempts/0001/result.yaml`
- `campaigns/P070-mh1-normalized-overlap/attempts/0002/result.yaml`
- `campaigns/P070-mh1-normalized-overlap/attempts/0003/result.yaml`
- `campaigns/P070-mh1-normalized-overlap/attempts/0004/result.yaml`
- `campaigns/P070-mh1-normalized-overlap/attempts/0005/result.yaml`
- `campaigns/P070-mh1-normalized-overlap/attempts/0006/result.yaml`
- `campaigns/P070-mh1-normalized-overlap/attempts/0007/result.yaml`
- `campaigns/P070-mh1-normalized-overlap/attempts/0008/result.yaml`
- `campaigns/P070-mh1-normalized-overlap/reviews/independent_overlap_review.py`
- `campaigns/P070-mh1-normalized-overlap/evidence/primary-provenance.yaml`
- `campaigns/P070-mh1-normalized-overlap/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-OVL-001-review.md`
- `tests/test_normalized_overlaps.py`
