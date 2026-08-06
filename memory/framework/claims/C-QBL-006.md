---
description: Accepted framework claim C-QBL-006
author: framework-registry
created: '2026-08-06T07:46:24Z'
updated: '2026-08-06T07:46:24Z'
tags:
- substrate-framework
- accepted-claim
- C-QBL-006
category: claims
confidence: established
status: active
---
# C-QBL-006

## Statement
The accepted statement is reproduced exactly from the claim registry.

Conditional on C-QBL-001's equal positive profiles f_1=A*sech(kappa*(x+d/2)) and f_2=A*sech(kappa*(x-d/2)) with A,kappa,d>0, separately declare the complex trial superposition Phi=f_1+exp(i*delta)*f_2 and the whole-line functional E[Phi]=integral dx*[|Phi_x|^2+kappa^2*|Phi|^2-|Phi|^4/24]. With s=kappa*d and c=cos(delta), define J31(s)=2*(sinh(s)*cosh(s)-s)/sinh(s)^3 and J22(s)=4*(s*cosh(s)-sinh(s))/sinh(s)^3. Exact expansion, isolated-profile subtraction, and the profile equation give I31=A^4*J31/kappa, I22=A^4*J22/kappa, and E_int=E[Phi]-E[f_1]-E[f_2]=-c*I31/6-(1+2*c^2)*I22/12. Thus the finite interaction contains phase-independent, linear-cosine, and cosine-squared terms and is not a pure cosine. At c=0 it is exactly -I22/12. The exact tail limits are J31~4*exp(-s) and J22~16*(s-1)*exp(-2*s), so for fixed nonzero c the leading interaction is -2*A^4*c*exp(-s)/(3*kappa), whereas the perpendicular case has the doubled exponential rate and linear prefactor. This is the energy of a two-profile trial superposition. It establishes no common nonlinear two-soliton or multi-profile solution, merger or persistence dynamics, equilibrium separation, spectral orbital or nonlinear stability, selected object count, physical condensate, generation, Standard-Model map, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-QBL-001, C-QBL-003. Assumptions: The complex functional is separately declared and is twice C-QBL-003's real scalar energy on a real field; no accepted claim promotes it to a physical condensate action., Both fixed trial profiles have the same positive amplitude inverse width and separation coordinate and individually obey C-QBL-001's quartic profile equation., The phase is spatially constant and c is exactly cos(delta). Changing the profile, nonlinear potential, phase field, width, amplitude, or number of profiles changes the interaction., Interaction energy means subtraction of two isolated profile energies. Its separation derivative is only a declared collective-coordinate generalized force and not field dynamics., Tail statements take s to positive infinity at fixed nonzero c; c=0 is a different leading-order branch.. Comparators: GC4 at substrate@6d1f4e02f87a0bd1dc326cb68af01872d1e88c64; its grid values are reproduced exactly while its finite pure-cosine and stability readings are corrected, Omitting the phase-independent and cosine-squared terms fails the exact perpendicular interaction and the source values, Separation mutations expose opposite generalized-force signs for anti-phase and Z3 pair choices outside the sampled tail regime.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.153.0` with provenance `campaigns/P211-gc4-phase-packing-stability-audit/adjudication.yaml`.

- `campaigns/P211-gc4-phase-packing-stability-audit/verify.py`
- `campaigns/P211-gc4-phase-packing-stability-audit/reviews/independent_phase_interaction_review.py`
- `campaigns/P211-gc4-phase-packing-stability-audit/reviews/C-QBL-006-claim-review.md`
- `campaigns/P211-gc4-phase-packing-stability-audit/reviews/source_adjudication.md`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/formula-freeze.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/dependency-audit.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/primary-provenance.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/independent-provenance.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/compatibility-audit.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/evidence/impact-analysis.yaml`
- `campaigns/P211-gc4-phase-packing-stability-audit/attempts/0004/result.yaml`
- `src/substrate_framework/phase_interactions.py`
- `tests/test_phase_interactions.py`
