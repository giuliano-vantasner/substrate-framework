---
description: Accepted framework claim C-NVP-002
author: framework-registry
created: '2026-08-10T17:07:00Z'
updated: '2026-08-10T17:07:00Z'
tags:
- substrate-framework
- accepted-claim
- C-NVP-002
category: claims
confidence: established
status: active
---
# C-NVP-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let Q>0, m>0, and g>0 be exact, let N_s be a positive integer, and let T_a for a=1,...,n be a nonempty same-size family of finite exact Hermitian matrices. Supply exact explicitly real fully antisymmetric f_abc such that [T_a,T_b]=i*sum_c f_abc*T_c and require tr_R(T_a*T_b)=T(R)*delta_ab for exact T(R)>0. Separately declare N_s identical massive complex-scalar multiplets in representation R on flat two-dimensional Euclidean space, with D_mu=partial_mu-i*g*W_mu^a*T_a, operator -D^2+m^2, the complex-scalar one-loop determinant, and a translation- and background-gauge-preserving regulator. In the quadratic convention of C-VAC-001, with z=sqrt(Q)/sqrt(Q+4*m^2), the nonzero-momentum color projector coefficient is Pi_hat^ab(Q)=tr_R(T_a*T_b)*N_s*g^2/pi*(atanh(z)/z-1), and the transverse form factor is Pi_hat^ab/Q. Before transverse decomposition, contraction of the scalar bubble and seagull gives respectively +2*N_s*g^2*tr_R(T_a*T_b) and -2*N_s*g^2*tr_R(T_a*T_b) times the common tadpole and q_nu, so their sum vanishes. The projector coefficient vanishes as Q tends to zero and as m tends to infinity, while at fixed Q>0 it diverges as m tends to zero. Its leading local Euclidean density is N_s*g^2*T(R)/(48*pi*m^2)*sum_a F_mu_nu^a*F_mu_nu^a, equivalently N_s*g^2/(48*pi*m^2)*tr_R(F_mu_nu*F_mu_nu), with the full non-Abelian curvature fixed by the C-NAG-001 convention. The independent proper-time factors (4*pi)^(-1), 1/12, and integral_0^infinity exp(-m^2*s) ds=1/m^2 give the same trace-density coefficient. This loop term is additive to separately declared bare and counterterm coefficients. It supplies no unique total coupling, physical quark or gluon, QCD sector, massless pole, preferred dimension, dimensional lift, observation, or substrate gauge mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-NAG-001, C-VAC-001. Assumptions: Flat two-dimensional Euclidean space, positive exact Q m and g, positive integer N_s, and the stated quadratic effective-action convention are declared together., The generators are finite same-size exact Hermitian matrices; the supplied exact real fully antisymmetric structure constants use orthogonal generator coordinates, close every commutator, and pair with one positive isotropic trace metric., The quantum fields are N_s identical massive complex scalars in that representation, with no real-scalar half factor and no silent identification with an accepted classical or substrate field., The regulator and subtraction preserve background gauge invariance and translation shifts, and the bubble and seagull belong to the same minimally coupled scalar action., The leading local curvature statement is a low-momentum inverse-mass expansion for m>0 and does not claim that higher-derivative or higher-curvature terms vanish., Component-density and trace-density coefficients remain separately typed by tr_R(T_a*T_b)=T(R)*delta_ab., Bare and counterterm coefficients, field normalization, matching scale, state, physical matter representation, dimension lift, observation, and substrate dictionary are not imported.. Comparators: QCD1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all eleven predicates without a NumPy compatibility event, while it declares no quantum determinant regulator bubble seagull or counterterm, imposes transversality, uses a fermion-shaped numerator for a scalar reading, produces a nonlocal curvature kernel, omits full background completion, changes normalization in its Abelian guard, and does not derive a unique coupling physical QCD sector dimensional lift or substrate mechanism.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.124.0` with provenance `campaigns/P160-qcd1-su3-kinetic-induction-audit/adjudication.yaml`.

- `campaigns/P160-qcd1-su3-kinetic-induction-audit/verify.py`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/reviews/independent_su3_scalar_review.py`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/reviews/replay_source_graph.py`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/attempts/0009/result.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/attempts/0011/result.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/attempts/0014/result.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/source-reproduction.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/source-audit.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/check-adjudication.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/input-provenance.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/dependency-audit.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/consumer-audit.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/source-graph-inventory.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/candidate-comparison.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/primary-provenance.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/compatibility-audit.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/evidence/literature-audit.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/reviews/source_adjudication.md`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/reviews/impact_analysis.md`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/attempts/0015/result.yaml`
- `campaigns/P160-qcd1-su3-kinetic-induction-audit/attempts/0016/result.yaml`
- `memory/vantasner/decisions/C-NVP-002-review.md`
- `memory/vantasner/decisions/QCD1-qualified-review.md`
- `src/substrate_framework/nonabelian_vacuum_polarization.py`
- `tests/test_nonabelian_vacuum_polarization.py`
