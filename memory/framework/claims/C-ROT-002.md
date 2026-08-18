---
description: Accepted framework claim C-ROT-002
author: framework-registry
created: '2026-08-18T22:40:00+02:00'
updated: '2026-08-18T22:40:00+02:00'
tags:
- substrate-framework
- accepted-claim
- C-ROT-002
category: claims
confidence: established
status: active
---
# C-ROT-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Declare the quantum symmetric-top rotational band M(J)=Mcl+J*(J+1)/(2*Lambda) and the classical rotor band Mcl_prime(J)=Mcl+J^2/(2*Lambda) for real classical mass Mcl and nonzero moment of inertia Lambda. Then the J=3/2 member lies strictly above the J=1/2 member for positive Lambda, with exact splitting M(3/2)-M(1/2)=3/(2*Lambda) independent of Mcl; the excitation energies stand in exact ratio M(3/2)-Mcl = 5*(M(1/2)-Mcl) for every nonzero Lambda, while the classical rotor gives ratio 9 and a different splitting, so the quantum band splitting is not the classical one. Adding an arbitrary one-loop vacuum energy E1 to the mass, Mtot(J)=Mcl+E1+J*(J+1)/(2*Lambda), leaves the splitting exactly 3/(2*Lambda) for every E1 - it is a function of the inertia alone, with zero derivative in E1 and identical splittings for distinct vacuum energies - while every individual level strictly increases with E1. In the corpus inertia frame Lambda=L*(1+lambda1)/(3*e^4*m_e) the splitting equals (9/2)*e^4*m_e/(L*(1+lambda1)) identically and is strictly decreasing in the inertia correction lambda1>-1, with distinct corrections giving distinct splittings; the two one-loop questions (level shift by E1, splitting shift by lambda1) are independent. This is a conditional band-structure theorem on the declared spectra. It does not derive the moment of inertia from a field theory, quantize a rotor, identify Delta or nucleon states, fix Mcl, E1, Lambda, or any coupling, or compare to observed splittings.

## Status Axes
The four governance axes remain independent.

Verification is `formal_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The band formulas, the J=1/2 and J=3/2 assignments, and the corpus inertia frame are declared inputs; the claim machine-checks the exact gap, ratio, vacuum-independence, and monotonicity identities of the declared functions.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.163.0` with provenance `campaigns/P233-lean-discrete-facts/adjudication.yaml`.

- `formal/SubstrateFramework/Ingested/Phase47BM_RigidTopSpectrum.lean`
- `formal/SubstrateFramework/Ingested/Phase48CE_OperatorAndGap.lean`
- `campaigns/P233-lean-discrete-facts/attempts/0001/result.yaml`
- `campaigns/P232-lean-corpus-census/census.yaml`
