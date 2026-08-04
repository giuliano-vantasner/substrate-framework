---
description: Accepted framework claim C-VAC-001
author: framework-registry
created: '2026-08-09T04:40:00Z'
updated: '2026-08-09T04:40:00Z'
tags:
- substrate-framework
- accepted-claim
- C-VAC-001
category: claims
confidence: established
status: active
---
# C-VAC-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-GAU-001's local-U1 connection convention, independently declare N positive-integer identical complex scalars in Euclidean two dimensions with mass m>0, charge magnitude e>0, covariant derivative D_mu=partial_mu-i*e*A_mu, quadratic operator -D^2+m^2, one-loop contribution Gamma_loop=Tr log(-D^2+m^2), a translation- and gauge-preserving regulator, and the quadratic convention Gamma_loop^(2)=A_mu*Pi_mu_nu*A_nu/2. Including both the scalar bubble and seagull, their contracted tadpole coefficients are respectively +2*N*e^2 and -2*N*e^2, so the Ward identity follows from their exact cancellation under the regulator's momentum-shift identity rather than from imposing a transverse ansatz. For Euclidean Q=q^2>0, define P_mu_nu=delta_mu_nu-q_mu*q_nu/Q and z=sqrt(Q)/sqrt(Q+4*m^2). Then Pi_mu_nu=P_mu_nu*Pi_hat(Q) =(Q*delta_mu_nu-q_mu*q_nu)*Pi_scalar(Q), where Pi_hat(Q)=N*e^2/pi*(atanh(z)/z-1) and Pi_scalar(Q)=Pi_hat(Q)/Q. Equivalently, Pi_hat=N*e^2*Q/(4*pi) times the integral from zero to one of (1-2*x)^2/[m^2+Q*x*(1-x)] dx. The low-momentum expansion is Pi_hat=N*e^2*Q/(12*pi*m^2)-N*e^2*Q^2/(120*pi*m^4)+O(Q^3), so this loop's leading local Euclidean effective-Lagrangian coefficients are N*e^2/(48*pi*m^2) for F_mu_nu*F_mu_nu and N*e^2/(24*pi*m^2) for F_01^2. At fixed Q>0 the m->0+ scalar limit diverges to positive infinity, whereas the fixed-Q heavy-mass limit and the e->0 loop contribution vanish. The finite e^2/pi massless limit of the fermion-shaped x*(1-x) integrand is not this scalar theorem. The result imports the quantum field, statistics, determinant, mass, charge, multiplicity, regulator, and loop prescription. It neither quantizes C-U1-001's classical field nor identifies physical electric charge, and it supplies no bare Maxwell coefficient, counterterm choice, gauge-field measure, analytic continuation, gauge fixing, propagator pole, propagating photon, preferred dimension, dimensional lift, observation, or substrate gauge-sector mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GAU-001. Assumptions: The Euclidean quantum complex scalar, positive mass and charge magnitude, positive integer species multiplicity, functional determinant, loop order, and quadratic-action convention are separately declared rather than derived from the accepted classical field., The loop prescription preserves gauge invariance and momentum shifts, or includes explicitly governed restoring counterterms; the bubble and seagull use the displayed common convention., Q is strictly positive for the projector representation. The zero-momentum result is a one-sided analytic limit, not evaluation of the undefined projector at q=0., The local coefficients describe the loop contribution in the low-momentum expansion. A separately supplied bare coefficient and allowed local counterterms remain additive and field-normalization dependent., The fixed-Q massless limit is infrared singular. It cannot be interchanged silently with the Q-to-zero limit or replaced by the fermionic Schwinger coefficient., A pole or physical spectrum requires a complete bare-plus-loop kernel, analytic continuation, sign and gauge conventions, gauge-field measure, and degree-of-freedom analysis that are outside this claim., No accepted claim identifies this quantum field, e, N, or m with a substrate excitation, electric charge, observed matter, or a preferred physical dimension.. Comparators: EM5 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its projector identities and narrow massive zero-Q limit survive, while its scalar/fermion statistics mix, imposed Ward check, local-Maxwell identification, induced coupling, pole, photon, dispersion, neutral closure, charge map, and substrate mechanism are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.103.0` with provenance `campaigns/P135-em5-induced-gauge-audit/adjudication.yaml`.

- `campaigns/P135-em5-induced-gauge-audit/verify.py`
- `campaigns/P135-em5-induced-gauge-audit/reviews/independent_scalar_qed2_review.py`
- `campaigns/P135-em5-induced-gauge-audit/reviews/replay_source_graph.py`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0001/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0002/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0003/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0004/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0005/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0006/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0007/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0008/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0009/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/attempts/0010/result.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/source-reproduction.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/source-audit.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/check-adjudication.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/input-provenance.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/dependency-audit.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/consumer-audit.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/candidate-comparison.yaml`
- `campaigns/P135-em5-induced-gauge-audit/evidence/primary-provenance.yaml`
- `campaigns/P135-em5-induced-gauge-audit/reviews/source_adjudication.md`
- `campaigns/P135-em5-induced-gauge-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-VAC-001-review.md`
- `memory/vantasner/decisions/EM5-qualified-review.md`
- `src/substrate_framework/vacuum_polarization.py`
- `tests/test_vacuum_polarization.py`
