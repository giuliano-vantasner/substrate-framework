---
description: Accepted framework claim C-NAG-001
author: framework-registry
created: '2026-08-10T03:55:00Z'
updated: '2026-08-10T03:55:00Z'
tags:
- substrate-framework
- accepted-claim
- C-NAG-001
category: claims
confidence: established
status: active
---
# C-NAG-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let H_I=C^2 carry the exact Pauli-half generators T_a, let H_C be a nonzero finite-dimensional carrier, and let P be an exact Hermitian projector with P_R=I-P. On H_I tensor H_C define G_a=T_a tensor P. For a smooth local U_I(x) in SU2 define U=U_I tensor P+I tensor P_R. Let g be exact positive, W_mu=W_mu^a G_a, and D_mu=partial_mu-i*g*W_mu. The finite transformation W_mu'=U*W_mu*U_dagger-(i/g)*(partial_mu U)*U_dagger gives D_mu'(U*psi)=U*D_mu psi. The curvature F_mu_nu=partial_mu W_nu-partial_nu W_mu-i*g*[W_mu,W_nu] obeys [D_mu,D_nu]psi=-i*g*F_mu_nu*psi and transforms as F_mu_nu'=U*F_mu_nu*U_dagger. The connection annihilates the P_R sector. With a separately declared invariant metric and cyclic trace, the quadratic trace density is gauge invariant and contains the noncommutative cubic and quartic algebra, but this does not derive an action coefficient or equation of motion. A declared parity exchange maps the left construction to a distinct right construction rather than making the left connection parity odd. These identities derive no physical matter field, charged current, charge-event equality, anomaly cancellation, Yang-Mills induction, weak boson, mass, coupling match, detector, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-REP-002. Assumptions: All matrices, fields, coordinates, and couplings are exact; floating inputs are outside the exact API, and g is explicitly positive., The connection is Hermitian in a finite carrier, coordinate derivatives commute, and U_I is a smooth exact SU2-valued matrix., H_C is finite-dimensional and nonzero, and P is an exact Hermitian idempotent supplied independently of the Pauli-half isospin carrier., The finite transformation convention is paired specifically with D=partial-i*g*W; changing the derivative convention changes its inhomogeneous sign., The quadratic-density statement additionally assumes a separately declared invariant metric and cyclic trace and does not supply an action normalization., The parity statement requires a separately declared exact unitary exchanging P and I-P while leaving H_I unchanged., No physical matter content, current, source equation, anomaly cancellation, mass mechanism, coupling match, gauge fixing, detector, or substrate map is imported.. Comparators: W7 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all eleven predicates without a NumPy compatibility event, while its finite connection sign, same-carrier projected generators, charge-event equality, action and dynamics, coupling match, parity reading, charged-current, weak-boson, mass, anomaly, detector, and substrate claims are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.117.0` with provenance `campaigns/P151-w7-su2l-gauging-audit/adjudication.yaml`.

- `campaigns/P151-w7-su2l-gauging-audit/verify.py`
- `campaigns/P151-w7-su2l-gauging-audit/reviews/independent_nonabelian_review.py`
- `campaigns/P151-w7-su2l-gauging-audit/reviews/replay_source_graph.py`
- `campaigns/P151-w7-su2l-gauging-audit/attempts/0004/result.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/attempts/0005/result.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/attempts/0006/result.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/attempts/0007/result.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/attempts/0008/result.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/source-reproduction.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/source-audit.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/check-adjudication.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/input-provenance.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/dependency-audit.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/consumer-audit.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/candidate-comparison.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/primary-provenance.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/evidence/literature-audit.yaml`
- `campaigns/P151-w7-su2l-gauging-audit/reviews/source_adjudication.md`
- `campaigns/P151-w7-su2l-gauging-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-NAG-001-review.md`
- `memory/vantasner/decisions/W7-qualified-review.md`
- `src/substrate_framework/nonabelian_gauge.py`
- `tests/test_nonabelian_gauge.py`
