---
description: Accepted framework claim C-BER-001
author: framework-registry
created: '2026-08-10T04:55:00Z'
updated: '2026-08-10T04:55:00Z'
tags:
- substrate-framework
- accepted-claim
- C-BER-001
category: claims
confidence: established
status: active
---
# C-BER-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let k be an integer and phi range from zero to two pi. In a complex carrier of dimension at least two, define the normalized real lift n_k(phi)=(cos(k*phi/2),sin(k*phi/2),0,...). Its rank-one projector is periodic and n_k(2*pi)=(-1)^k*n_k(0). More generally, let psi be an exact normalized section of this closed rank-one projector path with psi(2*pi)=tau*psi(0), where |tau|=1. With convention A=i*psi_dagger*d_phi psi, the closed-ray Berry holonomy is H=tau*exp(i*integral_0^{2*pi} A*dphi). Under a smooth exact phase change psi'=exp(i*chi)*psi, A'=A-d_phi chi and tau'=exp(i*(chi(2*pi)-chi(0)))*tau, so H is invariant. The real lift has A=0 and tau=(-1)^k. Its periodic complex gauge exp(-i*k*phi/2)*n_k has A=k/2 and tau=1. Both give H=(-1)^k. In contrast, exp(-i*k*phi/2) times a fixed ray has a constant projector and H=1 even though its bare integral phase is (-1)^k. Thus the local one-form is not a unique invariant, and these identities derive no physical vector potential, curvature or core source, defect dynamics, electromagnetic field, fermion, material realization, coupling, or observation.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-TOP-001. Assumptions: All vectors, coordinates, phases, endpoints, and integrals are exact; floating and unevaluated-integral inputs are outside the exact API., The section is a finite-dimensional complex column of dimension at least two, exactly normalized at every path point, and its rank-one projector closes between the stated endpoints., The endpoint section differs from its start by one exact unit-modulus scalar tau, and the Berry convention is specifically A=i*psi_dagger*d_phi psi., The explicit projective family uses an integer winding and an explicitly real coordinate on zero to two pi., The named parity character imports only C-TOP-001; equal values from other characters, Wilson loops, representations, or physical sectors do not identify objects., No physical carrier, order parameter, material phase, defect existence, core regularization, curvature, action, dynamics, coupling, electromagnetic dictionary, state, or observation is inferred.. Comparators: B1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its unchanged source passes all eight predicates under an explicit np.trapz alias backed by np.trapezoid, while native failure is version-only and its fixed-ray projector, omitted endpoint transition, one-object collapse, complete-guard claim, and physical emergent-vector-potential reading are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.118.0` with provenance `campaigns/P152-b1-berry-connection-audit/adjudication.yaml`.

- `campaigns/P152-b1-berry-connection-audit/verify.py`
- `campaigns/P152-b1-berry-connection-audit/reviews/independent_berry_review.py`
- `campaigns/P152-b1-berry-connection-audit/reviews/replay_source_graph.py`
- `campaigns/P152-b1-berry-connection-audit/attempts/0004/result.yaml`
- `campaigns/P152-b1-berry-connection-audit/attempts/0006/result.yaml`
- `campaigns/P152-b1-berry-connection-audit/attempts/0007/result.yaml`
- `campaigns/P152-b1-berry-connection-audit/attempts/0008/result.yaml`
- `campaigns/P152-b1-berry-connection-audit/attempts/0009/result.yaml`
- `campaigns/P152-b1-berry-connection-audit/attempts/0010/result.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/source-reproduction.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/source-audit.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/check-adjudication.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/input-provenance.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/dependency-audit.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/consumer-audit.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/candidate-comparison.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/primary-provenance.yaml`
- `campaigns/P152-b1-berry-connection-audit/evidence/literature-audit.yaml`
- `campaigns/P152-b1-berry-connection-audit/reviews/source_adjudication.md`
- `campaigns/P152-b1-berry-connection-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-BER-001-review.md`
- `memory/vantasner/decisions/B1-qualified-review.md`
- `src/substrate_framework/berry_holonomy.py`
- `tests/test_berry_holonomy.py`
