---
description: Accepted framework claim C-BND-001
author: framework-registry
created: '2026-08-09T21:15:00Z'
updated: '2026-08-09T21:15:00Z'
tags:
- substrate-framework
- accepted-claim
- C-BND-001
category: claims
confidence: established
status: active
---
# C-BND-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let phi be a sufficiently smooth real scalar, let u=phi_t(t,b) and v=phi_x(t,b), and let a, beta, and the scalar source J be exact real declared boundary data. Define R_(a,beta,J)=a*u+beta*v-J. Under scalar spatial parity phi_P(t,x)=phi(t,-x) and source pullback J_P(t,x)=J(t,-x), exact chain rule gives R_(a,beta,J_P)[phi_P](t,b)=R_(a,-beta,J)[phi](t,-b). Thus beta and minus beta form a parity-covariant parameter family. At a parity center, a fixed residual is internally invariant for arbitrary traces iff beta=0. The mixed residual is not a parity-odd eigenobject: its a*u-J part is even and beta*v part is odd; it is purely odd only when the even part is absent. Under the simultaneous parity map from a right half-line to a left half-line, the outward-normal derivative and its coefficient are unchanged. Finally one residual equation does not determine both u and v; for beta=0 it leaves v arbitrary, and for beta nonzero it admits the family v=(J-a*u)/beta. It therefore derives neither boundary sign correlation nor topological charge transfer or selection without additional dynamics and vacuum-boundary data. This exact conditional theorem supplies no boundary action, field evolution, charge map, fermion parity, chiral matter, weak interaction, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SG-013. Assumptions: Inputs are exact and real; floating values are outside the exact API., Phi and the scalar source are sufficiently regular for the displayed traces, reflection, and chain rule., Phi and J transform as scalars with no intrinsic parity sign; a pseudoscalar source requires a different declared theorem., Fixed-coordinate parity reflects b and flips phi_x, while the outward-normal statement transforms the half-line domain and its normal together., Internal invariance is tested at a parity center for arbitrary independent traces; restricting to a selected solution can produce state symmetry without operator invariance., The beta branch is declared zero or nonzero before solving the trace family, and one residual supplies only one scalar constraint., No boundary action, initial or boundary evolution data, vacuum endpoints, charge map, fermionic state, or weak-sector dynamics are imported.. Comparators: W1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; alias-only np.trapz-to-np.trapezoid replay passes all eight source checks, while intrinsic parity breaking, hard-coded charge selection, inserted vector and chiral witnesses, correlation-as-Delta-Q, fermion parity, weak interaction, boundary action, and nonlinear chiral-split readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.113.0` with provenance `campaigns/P146-w1-parity-boundary-audit/adjudication.yaml`.

- `campaigns/P146-w1-parity-boundary-audit/verify.py`
- `campaigns/P146-w1-parity-boundary-audit/reviews/independent_boundary_parity_review.py`
- `campaigns/P146-w1-parity-boundary-audit/reviews/replay_source_graph.py`
- `campaigns/P146-w1-parity-boundary-audit/attempts/0004/result.yaml`
- `campaigns/P146-w1-parity-boundary-audit/attempts/0005/result.yaml`
- `campaigns/P146-w1-parity-boundary-audit/attempts/0006/result.yaml`
- `campaigns/P146-w1-parity-boundary-audit/attempts/0007/result.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/source-reproduction.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/source-audit.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/check-adjudication.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/input-provenance.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/dependency-audit.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/consumer-audit.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/candidate-comparison.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/primary-provenance.yaml`
- `campaigns/P146-w1-parity-boundary-audit/evidence/literature-audit.yaml`
- `campaigns/P146-w1-parity-boundary-audit/reviews/source_adjudication.md`
- `campaigns/P146-w1-parity-boundary-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-BND-001-review.md`
- `memory/vantasner/decisions/W1-qualified-review.md`
- `src/substrate_framework/boundary_correlations.py`
- `tests/test_boundary_correlations.py`
