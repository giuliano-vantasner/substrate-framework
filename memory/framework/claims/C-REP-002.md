---
description: Accepted framework claim C-REP-002
author: framework-registry
created: '2026-08-09T23:15:00Z'
updated: '2026-08-09T23:15:00Z'
tags:
- substrate-framework
- accepted-claim
- C-REP-002
category: claims
confidence: established
status: active
---
# C-REP-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let H_I=C^2 have its standard inner product and Hermitian generators T_a=sigma_a/2. Let H_C be a nonzero finite-dimensional complex inner-product space and let P be a Hermitian idempotent on H_C, with P_R=I-P. Then G_a^L=T_a tensor P and G_a^R=T_a tensor P_R are Hermitian and each obeys [G_a,G_b]=i*epsilon_abc*G_c; G^L acts as the fundamental doublet on H_I tensor image(P) and vanishes on H_I tensor kernel(P), with the roles exchanged for G^R. The vector and axial combinations are G^V=G^L+G^R=T_a tensor I and G^A=G^L-G^R. If a declared unitary parity operator exchanges P and P_R while leaving H_I untouched, it exchanges G^L and G^R, leaves G^V even, and makes G^A odd; G^L alone is not a parity-odd eigenoperator. On H_I itself the full commutant of all T_a consists only of scalar matrices, so no nontrivial rank-one projector on that same irreducible carrier can be an independent chirality projector. In particular T_a*diag(1,0) is non-Hermitian for a=1,2 and fails the su2 algebra. Any Hermitian Abelian generator Y commuting with every T_a is y*I, so Q=T_3+c*Y has eigenvalues c*y+1/2 and c*y-1/2 with separation one. Assigned labels plus and minus one therefore cannot both be eigenvalues of one such Q; the rescaled declaration q_top/2=T3 with y=0 is algebraically compatible but is not selected by the representation. These exact finite-dimensional identities establish no physical state identification, topological transition, Lorentz chirality, fermion parity, gauge connection, interaction, anomaly statement, weak sector, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-SPN-002. Assumptions: H_I uses the exact standard positive-definite inner product and fixed Pauli-half normalization; floating inputs are outside the exact API., H_C is finite-dimensional and nonzero, and P is an exact Hermitian idempotent. It is a separately declared carrier rather than the isospin C2., The optional parity statement requires a separately declared exact unitary on H_C that exchanges P and I-P while acting trivially on H_I., The Abelian generator is Hermitian and commutes with the full irreducible SU2 action; its eigenvalue y and coefficient c are supplied exact real normalization data., Labels compared with the spectrum are supplied coordinate values. Representation algebra does not select a topological or electric charge normalization., No matter field, Lorentz transformation, connection, action, current, anomaly calculation, interaction, boundary evolution, or physical state identification is imported.. Comparators: W2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all nine predicates without a NumPy compatibility event, while physical kink and antikink state identity, event-charge matching, forced T3 calibration, common hypercharge, same-carrier chirality, left SU2 representation, parity-odd charge selection, fermion parity, gauge interaction, and weak-sector readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.114.0` with provenance `campaigns/P147-w2-su2-doublet-audit/adjudication.yaml`.

- `campaigns/P147-w2-su2-doublet-audit/verify.py`
- `campaigns/P147-w2-su2-doublet-audit/reviews/independent_su2_factor_review.py`
- `campaigns/P147-w2-su2-doublet-audit/reviews/replay_source_graph.py`
- `campaigns/P147-w2-su2-doublet-audit/attempts/0004/result.yaml`
- `campaigns/P147-w2-su2-doublet-audit/attempts/0005/result.yaml`
- `campaigns/P147-w2-su2-doublet-audit/attempts/0006/result.yaml`
- `campaigns/P147-w2-su2-doublet-audit/attempts/0007/result.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/source-reproduction.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/source-audit.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/check-adjudication.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/input-provenance.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/dependency-audit.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/consumer-audit.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/candidate-comparison.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/primary-provenance.yaml`
- `campaigns/P147-w2-su2-doublet-audit/evidence/literature-audit.yaml`
- `campaigns/P147-w2-su2-doublet-audit/reviews/source_adjudication.md`
- `campaigns/P147-w2-su2-doublet-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-REP-002-review.md`
- `memory/vantasner/decisions/W2-qualified-review.md`
- `src/substrate_framework/su2_doublets.py`
- `tests/test_su2_doublets.py`
