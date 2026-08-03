---
description: Accepted framework claim C-RPROF-001
author: framework-registry
created: '2026-08-07T15:30:00Z'
updated: '2026-08-07T15:30:00Z'
tags:
- substrate-framework
- accepted-claim
- C-RPROF-001
category: claims
confidence: established
status: active
---
# C-RPROF-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-RMAP-001's declared positive integer degree B and positive angular coefficient I, and on the separately declared dimensionless radial functional E=4*pi*integral_0^infinity [r^2*f'^2 +2*B*sin(f)^2*(1+f'^2)+I*sin(f)^4/r^2] dr, exact one-dimensional variation gives (r^2+2*B*sin(f)^2)*f''+2*r*f' +B*sin(2*f)*(f'^2-1)-I*sin(2*f)*sin(f)^2/r^2=0. The density separates as E=E2+E4 with E2=4*pi*integral [r^2*f'^2+2*B*sin(f)^2]dr and E4=4*pi*integral [2*B*sin(f)^2*f'^2+I*sin(f)^4/r^2]dr. Under the scale family f_s(r)=f(exp(s)*r), convergence and endpoint data that remove boundary terms give E(s)=exp(-s)*E2+exp(s)*E4; a stationary member therefore obeys E2=E4 and has positive curvature E2+E4 in this scale direction. Linearized regular-origin and decaying massless-tail powers are sigma=(sqrt(1+8*B)-1)/2 and p=(sqrt(1+8*B)+1)/2, satisfying sigma*(sigma+1)=2*B and p*(p-1)=2*B, with asymptotic residuals r*f'+sigma*(pi-f)=0 and r*f'+p*f=0. At B=1,I=1 the density and equation reduce exactly to C-MOD-001. These are conditional exact reduced-model identities. They do not derive a physical Skyrme action or rational-map ansatz, prove half-line existence or uniqueness, establish local or global minimization, solve a full three-dimensional field, identify degree with a baryon or nucleus, or supply a mass, binding energy, reaction, yield, material, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-RMAP-001, C-MOD-001. Assumptions: C-RMAP-001's sphere normalization and conditional definitions hold, while the displayed radial functional and its dimensionless normalization remain explicit declared premises rather than consequences of an accepted physical action., B is a positive integer, I is positive, r is positive, and the profile is differentiable and convergent enough for the displayed variation, integrations by parts, and scale substitution., The endpoint powers follow the linearized or dominant-balance equations. At B=1 nonlinear terms also enter the leading origin coefficient equation but do not change sigma=1., The Robin expressions encode leading asymptotic behavior at finite numerical cutoffs; they are not exact finite-radius vacuum values., E2=E4 establishes stationarity only along the displayed scale family. Positive scale curvature alone proves neither a local minimum in the full radial function space nor any full-field stability., C-MOD-001 is an exact B=1 compatibility surface only. Neither it nor this claim establishes a physical soliton, particle, or state map.. Comparators: E2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its functional and numeric comparators were exposed before P105, so selection rests on exact derivation, accepted inputs, endpoint structure, independent methods, mutations, and frozen ceilings rather than decimal closeness.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.89.0` with provenance `campaigns/P105-e2-rational-map-radial-profiles/adjudication.yaml`.

- `campaigns/P105-e2-rational-map-radial-profiles/verify.py`
- `campaigns/P105-e2-rational-map-radial-profiles/reviews/independent_radial_review.py`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/source-reproduction.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/source-audit.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/check-adjudication.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/dependency-audit.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/consumer-audit.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/candidate-comparison.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/evidence/primary-provenance.yaml`
- `campaigns/P105-e2-rational-map-radial-profiles/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-RPROF-001-review.md`
- `tests/test_rational_map_radial.py`
