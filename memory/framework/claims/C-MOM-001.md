---
description: Accepted framework claim C-MOM-001
author: framework-registry
created: '2026-08-01T17:44:29Z'
updated: '2026-08-01T17:44:29Z'
tags:
- substrate-framework
- accepted-claim
- C-MOM-001
category: claims
confidence: established
status: active
---
# C-MOM-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let T^{mu nu} be a smooth symmetric tensor in inertial flat 3+1 coordinates satisfying partial_mu T^{mu nu}=0. Assume localization strong enough that the surface terms for total charges and the coordinate- weighted first and second moments vanish. Define M=integral T^{00} d^3x, P^i=integral T^{0i} d^3x, D^i=integral x^i T^{00} d^3x, and I^{ij}=integral x^i x^j T^{00} d^3x. Then dot M=0, dot P^i=0, dot D^i=P^i, ddot D^i=0, and ddot I^{ij}=2*integral T^{ij} d^3x. Thus the dipole is generally affine in time rather than constant. For normalized STF I_STF=I-delta*Tr(I)/3, ddot I_STF^{ij}=2*integral [T^{ij}-delta^{ij} T^{kk}/3] d^3x. The alternative source convention Q=3*I-delta*Tr(I) is exactly 3*I_STF and has three times this acceleration. Constant translation of the spatial origin leaves ddot I unchanged because ddot M and ddot D vanish. Nonzero boundary flux invalidates the conserved integrated charges, and without T^{i0}=T^{0i}, dot D^i need not equal P^i. These identities establish no gravitational field equation, retarded solution, TT coupling, radiating multipole order, nonzero quadrupole radiation, waveform, power, gravitational coupling, 1+1 contrast, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `native`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: Spatial coordinates are inertial Cartesian coordinates and partial_t T^{0 nu}+partial_j T^{j nu}=0 fixes the sign convention., Tensor symmetry identifies the energy-flux components T^{i0} with the momentum-density components T^{0i}., Localization removes ordinary and coordinate-weighted surface terms through second moment order., The theorem concerns exact source moments and does not assume that any moment couples to or radiates a field., Point-mass helper APIs compute declared kinematic moments and do not by themselves provide a locally conserved binding stress.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.32.0` with provenance `campaigns/P036-gw1-conserved-stress-moments/adjudication.yaml`.

- `campaigns/P036-gw1-conserved-stress-moments/verify.py`
- `campaigns/P036-gw1-conserved-stress-moments/attempts/0001/result.yaml`
- `campaigns/P036-gw1-conserved-stress-moments/reviews/independent_weak_moment_review.py`
- `campaigns/P036-gw1-conserved-stress-moments/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-MOM-001-review.md`
- `tests/test_conserved_moments.py`
