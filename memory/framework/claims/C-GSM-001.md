---
description: Accepted framework claim C-GSM-001
author: framework-registry
created: '2026-08-10T06:45:00Z'
updated: '2026-08-10T06:45:00Z'
tags:
- substrate-framework
- accepted-claim
- C-GSM-001
category: claims
confidence: established
status: active
---
# C-GSM-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

Let a nonzero finite-dimensional complex inner-product carrier have a nonempty supplied family of exact Hermitian generators T_a, exact real couplings g_a, and an exact declared vacuum column phi_0. Conditional on the scalar covariant kinetic term with D_mu*phi_0=-i*sum_a(g_a*A_mu^a*T_a)*phi_0, write its real gauge-field quadratic part as one half A^T*M2*A. Then M2_ab=g_a*g_b*phi_0_dagger*{T_a,T_b}*phi_0, equivalently twice the real Gram matrix of u_a=g_a*T_a*phi_0. It is real symmetric positive semidefinite and x^T*M2*x=2*norm(sum_a x_a*u_a)^2 for every real coefficient vector x. Thus its kernel is exactly the coupled vacuum stabilizer. When the supplied generators are independent over real coefficients and every coupling is nonzero, its nullity is the stabilizer dimension in that generator span; dependent labels or zero couplings do not support that interpretation. If the real gauge fields instead have a separately declared symmetric positive-definite kinetic metric K, their quadratic mass parameters are the generalized eigenvalues of M2*x=lambda*K*x, not the raw eigenvalues of M2 unless K is identity. Under a real invertible field change A=S*A_new, both forms transform by congruence, M2_new=S^T*M2*S and K_new=S^T*K*S, preserving generalized eigenvalues and nullity. For T_i=sigma_i/2, T_4=I/2, couplings (g,g,g,g_prime), and phi_0=(0,v/sqrt(2)), with exact positive g, g_prime, and v, the canonical M2 has charged diagonal entries g^2*v^2/4 and neutral block v^2/4 times [[g^2,-g*g_prime],[-g*g_prime,g_prime^2]], rank three, a null vector proportional to (g_prime,g), nonzero neutral eigenvalue (g^2+g_prime^2)*v^2/4, and the conditional rho identity one. The congruence B mapped to -B flips the neutral off-diagonal sign while preserving these invariants. These are exact conditional quadratic identities. They do not derive the scalar action or potential, prove phi_0 is a stationary ground state or condensate, supply a gauge kinetic action, establish a spectral pole or Higgs particle, identify photon W or Z fields, select the Standard Model, or realize a substrate mass mechanism.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-NAG-001, C-GAU-001, C-REP-002. Assumptions: The carrier is finite-dimensional and nonzero with its standard positive inner product; all matrix and scalar inputs are exact, and floating inputs are outside the API., Every supplied generator is a same-size Hermitian matrix, every coupling is explicitly real, the vacuum is a matching column, and gauge-field coefficients are real., The scalar covariant kinetic term and one-half real-field quadratic convention are separately declared; the theorem derives their quadratic coefficient rather than the action or vacuum., Kernel equality is for the coupled orbit map. Interpreting its nullity as the stabilizer dimension in the supplied generator span additionally requires an independent real generator basis and nonzero couplings., The generalized quadratic-mass statement requires a separately declared exact symmetric positive-definite kinetic metric in the same real gauge basis; no spectral-pole interpretation is inferred., The SU2 times U1 specialization uses the exact Pauli-half generators, Abelian generator I/2, positive g g_prime and v, lower vacuum (0,v/sqrt(2)), and canonical kinetic metric for its displayed raw eigenvalues and rho identity., No scalar potential, stationary ground state, condensate ontology, gauge kinetic dynamics, particle identity, Standard Model selection, observable, or substrate realization is imported.. Comparators: M1 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; native execution passes all nine predicates without a NumPy compatibility event, while the scalar vacuum and kinetic actions remain declared, raw masses require K, the advertised sign-only guard actually changes magnitude, and physical condensate Higgs photon W Z electroweak Standard Model and substrate readings are corrected qualified or rejected.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.120.0` with provenance `campaigns/P154-m1-anderson-higgs-mass-audit/adjudication.yaml`.

- `campaigns/P154-m1-anderson-higgs-mass-audit/verify.py`
- `campaigns/P154-m1-anderson-higgs-mass-audit/reviews/independent_gauge_scalar_mass_review.py`
- `campaigns/P154-m1-anderson-higgs-mass-audit/reviews/replay_source_graph.py`
- `campaigns/P154-m1-anderson-higgs-mass-audit/attempts/0006/result.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/attempts/0007/result.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/source-reproduction.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/source-audit.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/check-adjudication.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/input-provenance.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/dependency-audit.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/consumer-audit.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/nonduplication-audit.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/candidate-comparison.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/primary-provenance.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/evidence/literature-audit.yaml`
- `campaigns/P154-m1-anderson-higgs-mass-audit/reviews/source_adjudication.md`
- `campaigns/P154-m1-anderson-higgs-mass-audit/reviews/impact_analysis.md`
- `memory/vantasner/decisions/C-GSM-001-review.md`
- `memory/vantasner/decisions/M1-qualified-review.md`
- `src/substrate_framework/gauge_scalar_mass.py`
- `tests/test_gauge_scalar_mass.py`
