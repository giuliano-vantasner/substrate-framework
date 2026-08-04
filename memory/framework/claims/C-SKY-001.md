---
description: Accepted framework claim C-SKY-001
author: framework-registry
created: '2026-08-09T07:20:00Z'
updated: '2026-08-09T07:20:00Z'
tags:
- substrate-framework
- accepted-claim
- C-SKY-001
category: claims
confidence: established
status: active
---
# C-SKY-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Declare a static three-component real linear field phi_a on R^3 with source-coupled energy E[phi;J]=K/2*integral[(grad phi_a)^2+m^2*phi_a^2] d^3x-integral J_a*phi_a d^3x, where K>0 and m>=0, so that K*(-Delta+m^2)*phi_a=J_a. Put equal triplet point-dipole sources of magnitude P>=0 at distinct X_A and X_B, with J_A^a=-P*A_ai*partial_i delta(x-X_A) and J_B^a=-P*B_ai*partial_i delta(x-X_B), A and B proper rotations. Let R=|X_B-X_A|>0, u=(X_B-X_A)/R, D=A^T*B in SO(3), and G_m(R)=exp(-mR)/(4*pi*R). After subtracting the two divergent isolated point-dipole self energies, the finite on-shell cross energy is exactly E_int=P^2/K*[(G_m'/R)*Tr(D)+(G_m''-G_m'/R)*u^T*D*u]. Write a=G_m'/R=-exp(-mR)*(1+mR)/(4*pi*R^3) and c=G_m''=exp(-mR)*(m^2*R^2+2*mR+2)/(4*pi*R^3). Over the full proper relative-orientation space, the global minimum is -P^2*c/K, attained by every pi rotation about an axis perpendicular to u; the global maximum is P^2*(c-2a)/K, attained by the pi rotation about u; and the identity orientation has energy P^2*m^2*G_m/K. At fixed most-attractive orientation the radial force is -P^2*exp(-mR)*(m^3*R^3+3*m^2*R^2+6*mR+6)/(4*pi*K*R^4), strictly inward for P>0. For m>0 the interaction and force decay faster than every power; as m tends to zero from above the minimum energy tends to -P^2/(2*pi*K*R^3) and the force to -3*P^2/(2*pi*K*R^4). This is an exact conditional source-coupled long-range point-dipole theorem. It does not derive the declared field or sources from a nonlinear Skyrme action, construct B=1 or two-center Skyrmion solutions, prove a product ansatz or short-range core, quantize a nucleon, or establish a nucleon-nucleon potential, binding, material, scale, observation, or substrate mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: none. Assumptions: The displayed three-component static linear field energy, positive stiffness, nonnegative mass, source coupling sign, and distributional point-dipole sources are declared model data rather than consequences of an accepted nonlinear field theory., The two source centers are distinct, R is positive, u is unit normalized, A and B are proper rotations, D=A^T*B lies in SO(3), and both triplets have the same nonnegative magnitude P and displayed source convention., Point-dipole isolated self energies diverge. The claim concerns only the finite cross term after the two isolated self energies are subtracted in the displayed on-shell source-coupled energy convention., The radial force differentiates the cross energy with D fixed. Orientation relaxation as R changes, collective kinetic terms, radiation, retardation, deformation, overlap, and nonlinear core dynamics define different problems., Exponential finite range requires m>0. The m=0 formula is a separate inverse-cube massless limit. When P=0 all energies and forces vanish and the named extremizing orientations are nonunique., The SO(3) extrema concern the complete declared classical relative-orientation variable. They are not spin or isospin expectation values and do not perform semiclassical or quantum nucleon projection., No accepted claim maps K, P, m, A, B, the triplet field, or the source centers to physical pions, Skyrmions, baryons, nucleons, a nuclear potential, a material, measured units, or a substrate sector.. Comparators: S1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its one-coordinate and supplied-profile algebra survives conditionally, while its numeric force equation, assigned orientation literals, ANW attribution, two-Skyrmion/nucleon reading, and physical conclusions are corrected qualified or rejected, Foster-Krusch 2015 and Harland-Halcrow arXiv:2101.02633v3 are primary scope cross-checks for a long-range dipole approximation only; no literature coefficient or empirical nuclear comparator enters the derivation or selection.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.105.0` with provenance `campaigns/P137-s1-two-skyrmion-force-audit/adjudication.yaml`.

- `campaigns/P137-s1-two-skyrmion-force-audit/verify.py`
- `campaigns/P137-s1-two-skyrmion-force-audit/reviews/independent_massive_dipole_review.py`
- `campaigns/P137-s1-two-skyrmion-force-audit/reviews/replay_source_graph.py`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0002/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0003/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0004/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0005/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0006/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0007/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0008/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0009/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0010/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/attempts/0011/result.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/source-reproduction.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/source-audit.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/check-adjudication.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/input-provenance.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/dependency-audit.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/consumer-audit.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/candidate-comparison.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/primary-provenance.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/evidence/literature-audit.yaml`
- `campaigns/P137-s1-two-skyrmion-force-audit/reviews/source_adjudication.md`
- `campaigns/P137-s1-two-skyrmion-force-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-SKY-001-review.md`
- `memory/vantasner/decisions/S1-qualified-review.md`
- `src/substrate_framework/massive_dipoles.py`
- `tests/test_massive_dipoles.py`
