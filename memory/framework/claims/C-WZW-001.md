---
description: Accepted framework claim C-WZW-001
author: framework-registry
created: '2026-08-02T15:00:00Z'
updated: '2026-08-02T15:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-WZW-001
category: claims
confidence: established
status: active
---
# C-WZW-001

## Statement
The accepted statement is reproduced exactly from the claim registry.

In the explicit fundamental SU(3) convention of C-LIE-001, let E_a=i*T_a, so E_a is anti-Hermitian and [E_a,E_b]=-f_abc*E_c, and define the real left-invariant five-cochain Omega_5=-i*Alt Tr(theta^5), where theta=g^{-1}dg and Alt is the unnormalized signed permutation sum with no hidden 1/5! factor. The exact Chevalley-Eilenberg differentials built from those structure constants obey d_5*d_4=0, have rank(d_4)=35 and rank(d_5)=20, and hence have a 36-dimensional degree-five cocycle kernel and one-dimensional invariant fifth cohomology. Omega_5 has nine nonzero basis components, squared coefficient norm 75/4, obeys d_5*Omega_5=0, and is not in image(d_4): appending it raises the image rank from 35 to 36, while independently Omega_5^T*d_4=0 and Omega_5^T*Omega_5=75/4. Because SU(3) is compact and Omega_5 is left invariant, a hypothetical global primitive could be averaged with normalized Haar measure to an invariant primitive; the exact non-image result therefore makes Omega_5 globally non-exact without assigning any period normalization. The density is a local, metric-free polynomial in a smooth group-valued map and its first derivatives. For an ungauged variation delta U=U*v, delta Tr(theta^5)=d(5*Tr(v*theta^4)); this is an exact boundary identity. If two compatible oriented fillings have integrals I_B and I_Bprime, their glued closed-cycle period is I_B-I_Bprime and the extension phase ratio for coefficient c is exp(i*c*(I_B-I_Bprime)); filling independence follows only under the additional premise that c times every allowed period lies in 2*pi*Z. The theorem fixes no generator period, integer level, WZW coefficient, N_c, baryon current or charge, gauge connection, Chern-Simons descent, anomaly inflow, representation selection, physical bulk or boundary dynamics, absolute scale, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIE-001. Assumptions: The generator, trace, and structure-constant conventions are exactly those of C-LIE-001, and theta is expanded in the anti-Hermitian basis E_a=i*T_a., Alt denotes the full unnormalized alternating sum, Omega_5 includes the displayed minus-i reality factor, and orientation reversal changes every five-dimensional integral's sign., Standard exterior-calculus sign rules, the Maurer-Cartan identity, Stokes' theorem, compactness of the matrix group SU(3), and normalized Haar averaging are approved mathematical imports., The global non-exactness implication uses only that averaging commutes with d and fixes a left-invariant form; it supplies no period lattice or integral generator., The filling comparison assumes smooth compatible extensions and oriented gluing; its phase statement is conditional on a separately declared coefficient and period lattice., The boundary identity varies an ungauged group-valued map and is not a gauge-anomaly, baryon-current, or physical-inflow theorem.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.50.0` with provenance `campaigns/P056-wz1-wzw-five-form-inflow/adjudication.yaml`.

- `campaigns/P056-wz1-wzw-five-form-inflow/verify.py`
- `campaigns/P056-wz1-wzw-five-form-inflow/attempts/0002/result.yaml`
- `campaigns/P056-wz1-wzw-five-form-inflow/attempts/0003/result.yaml`
- `campaigns/P056-wz1-wzw-five-form-inflow/reviews/independent_cohomology_review.py`
- `campaigns/P056-wz1-wzw-five-form-inflow/reviews/source_adjudication.md`
- `memory/vantasner/decisions/C-WZW-001-review.md`
- `tests/test_wzw.py`
