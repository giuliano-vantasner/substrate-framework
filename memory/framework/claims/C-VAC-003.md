---
description: Accepted framework claim C-VAC-003
author: framework-registry
created: '2026-08-11T12:54:00Z'
updated: '2026-08-11T12:54:00Z'
tags:
- substrate-framework
- accepted-claim
- C-VAC-003
category: claims
confidence: established
status: active
---
# C-VAC-003

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-GAU-001's connection convention, C-DIM-009's mass- dimension and normalization bookkeeping, C-VAC-002's independently declared charged-Dirac D4 comparator, and C-MAX-001's exact no-kinetic variational ceiling, independently declare one or more free complex charged scalars, the scalar determinant Tr log(-D^2+M2) at one loop, the tensor convention Pi_mn=(q^2*g_mn-q_m*q_n)*Pi2(q^2), and one common shift-invariant gauge-preserving regulator for the oriented scalar bubble and seagull. With D_p=p^2+M2 and D_pq=(p+q)^2+M2, q*(2p+q)=D_pq-D_p. After the declared common momentum translation, the bubble Ward contraction is +2*q_nu times the tadpole integral and the seagull is its negative, deriving transversality rather than imposing a transverse ansatz. For positive spacelike Q=-q^2, nonnegative M2, positive charge magnitude e with [e^2]=4-d, positive integration dimension d away from unevaluated Gamma poles, and positive integer species count N, define Delta=M2+x*(1-x)*Q. The exact source-convention scalar form factor is Pi2(-Q)=-N*e^2*Gamma(2-d/2)/(4*pi)^(d/2) times the integral from zero to one of (1-2*x)^2*Delta^(d/2-2) dx, and is dimensionless. Separately set d=4-2*epsilon, multiply by mu2^epsilon, require M2>0, and take zero momentum. The bare form factor is -N*e^2*Gamma(epsilon)*(4*pi*mu2/M2)^epsilon/(48*pi^2), with Laurent residue -N*e^2/(48*pi^2). Adding the displayed MS-bar pole counterterm and arbitrary finite local c_fin gives Pi2_MSbar(0)=N*e^2*log(M2/mu2)/(48*pi^2)+c_fin. Its log(M2), log(m), and log(mu) slopes are respectively N*e^2/(48*pi^2), N*e^2/(24*pi^2), and -N*e^2/(24*pi^2); in the same convention the C-VAC-002 Dirac slopes are exactly four times these one-species scalar slopes. For the connection field B=e*A and kinetic action -Z_B*F(B)^2/4, separately supplied nonnegative exact complex-scalar and Dirac invariant weights W_s and W_f compose as b=W_s/3+4*W_f/3, with mu*dZ_B/dmu=-b/(8*pi^2). For positive mu and mu_ref and an independent real reference value Z_ref, the complete exact family is Z_B(mu)=Z_ref+b*log(mu_ref/mu)/(8*pi^2). Under mu_ref'=kappa*mu_ref, the same function has Z_ref'=Z_ref-b*log(kappa)/(8*pi^2). The separately declared zero-matching specialization Z_ref=0 has positive Z_B exactly when b>0 and mu_ref>mu; general positivity depends on Z_ref. Neither an absent kinetic operator in a no-matter theory nor C-MAX-001's current constraint fixes Z_ref in a theory after charged matter is introduced. This theorem does not fix Z_ref, a bare coefficient, finite matching condition, reference scale, physical charged spectrum, multiplicity, representation, gauge group, total coupling, preferred dimension, observation, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-GAU-001, C-DIM-009, C-VAC-002, C-MAX-001. Assumptions: The free complex charged scalars, scalar determinant sign, loop order, masses, charges, tensor sign, quadratic-action convention, and regulator are declared rather than derived from accepted substrate matter., The bubble and seagull use one regulator preserving their common loop-momentum translation, or any restoring counterterm is separately governed. The parameter weight alone does not establish this premise., The physical-dimension family uses [e^2]=4-d. Dimensional continuation near four supplies mu2^epsilon, and the zero-momentum D4 endpoint requires positive M2., MS-bar specifies the displayed pole subtraction but does not fix c_fin, a bare kinetic term, finite threshold matching, reference value, or total coupling., B=e*A, the generator basis, matter weights, and kinetic-action convention are fixed together. Changing a generator normalization without its paired coupling and invariant-weight transformations defines a different comparison., W_s and W_f are supplied exact invariant sums; no representation, group, multiplicity, charge spectrum, or physical excitation is inferred from their coefficients., Z_ref includes the independently supplied renormalized local and finite matching coordinates. Z_ref=0 is a separate compositeness or matching premise, not a consequence of the flow or of removing a kinetic term in another theory., No accepted claim identifies the conditional scalar or Dirac fields, scales, boundary values, group data, or total coefficient with observations or a substrate realization.. Comparators: GK3D2 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its scalar-to-Dirac factor four, conditional matter weights, affine flow, and explicit zero-matching specialization survive, while its incomplete scalar derivation, rung25 boundary inference, erased additive constant, general positivity, unique logarithm, physical coupling, and substrate readings are corrected, qualified, or rejected, C-VAC-001 remains the distinct massive complex-scalar Euclidean D2 bubble-plus-seagull theorem, C-RGE-005 imports the same generic complex-scalar and Weyl loop weights but does not derive the scalar loop or select matching data, arXiv:hep-ph/9806451 and arXiv:1611.00446v2 independently corroborate the scalar bubble-seagull structure and one-complex-scalar beta coefficient in their declared conventions.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.138.0` with provenance `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/adjudication.yaml`.

- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/verify.py`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/reviews/independent_scalar_kinetic_review.py`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/reviews/replay_source_graph.py`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/reviews/C-VAC-003-claim-review.md`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/reviews/source_adjudication.md`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/reviews/impact_analysis.md`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/attempts/0004/result.yaml`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/attempts/0007/result.yaml`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/attempts/0009/result.yaml`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/evidence/formula-freeze.yaml`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/evidence/literature-audit.yaml`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/evidence/input-provenance.yaml`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/evidence/dependency-audit.yaml`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/evidence/consumer-audit.yaml`
- `campaigns/P186-gk3d2-induced-kinetic-normalization-audit/evidence/primary-provenance.yaml`
- `memory/vantasner/decisions/C-VAC-003-review.md`
- `memory/vantasner/decisions/GK3D2-qualified-review.md`
- `src/substrate_framework/vacuum_polarization.py`
- `tests/test_scalar_qed4_kinetic.py`
