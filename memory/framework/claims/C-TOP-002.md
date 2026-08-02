---
description: Accepted framework claim C-TOP-002
author: framework-registry
created: '2026-08-02T17:00:00Z'
updated: '2026-08-02T17:00:00Z'
tags:
- substrate-framework
- accepted-claim
- C-TOP-002
category: claims
confidence: established
status: active
---
# C-TOP-002

## Statement
The accepted statement is reproduced exactly from the claim registry.

In C-LIE-001's fundamental trace convention, let theta=U^dagger*dU for a smooth SU(3)-valued map. The exact invariant Chevalley-Eilenberg differentials have rank(d_2)=20 and rank(d_3)=35, so the degree-three cocycle kernel has dimension 21 and H^3 has dimension one. The real cochain Alt Tr(theta^3) has nine nonzero components, squared coefficient norm 9, is closed, and is not in image(d_2), since adjoining it raises the image rank from 20 to 21. On the unit quaternion sphere oriented as the boundary of (a0,a1,a2,a3), the upper-SU(2)-block map q(a)=a0*I+i*(a1*sigma1+a2*sigma2+a3*sigma3) embedded in SU(3) has a first-column real coordinate map of determinant and degree +1, hence is a pi_3(SU(3)) generator under the audited stable inclusion criterion. Its exact oriented tangent density is Alt Tr(theta^3)=12 and its raw period is 24*pi^2. Therefore omega_3=-Alt Tr(theta^3)/(24*pi^2) has period -1 on that positive generator. With epsilon^(0123)=+1, the corresponding coordinate current J^mu=-(1/(24*pi^2))*epsilon^(mu nu rho sigma)*Tr(L_nu L_rho L_sigma), L_mu=U^dagger*partial_mu U, is identically conserved for every smooth U: the full graded derivative reduces by Maurer-Cartan flatness to the alternating trace of four one-forms, which vanishes by graded cyclicity. For the static upper-block hedgehog U=cos(F(r))*I+i*sin(F(r))*rhat.sigma, its local density for r>0 is -sin(F)^2*F'/(2*pi^2*r^2), its angularly integrated radial density is -2*sin(F)^2*F'/pi, and its charge is [F-sin(F)*cos(F)]_(outer)^(inner)/pi. Smooth constant endpoint data F(0)=n*pi and F(infinity)=0 therefore give charge n, while reversing orientation reverses the charge. This is a mathematical winding-current theorem. It is not by itself a Noether current, gauged-WZW-response current, physical baryon current, anomaly, identification with N_c, representation selection, absolute-scale statement, or substrate realization.

## Status Axes
The four governance axes remain independent.

Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`.

## Dependency and Import Closure
The registry records the accepted closure and declared non-claim inputs.

Dependencies: C-LIE-001. Assumptions: The fundamental generators, matrix trace, and anti-Hermitian left-current convention are exactly those of C-LIE-001., Alt is the full unnormalized alternating sum, epsilon^(0123)=+1, and spatial orientation is induced by the ordered coordinates (x,y,z); reversing orientation reverses current and charge but not conservation., Puttmann-Rigas Lemma 1.1, Bott stability, the standard SU(2)->SU(3)->S^5 fibration exact sequence, pi_3(SU(2))=Z, sphere volumes, smooth pullback, and Stokes are approved mathematical imports with the displayed generator algebra and degree independently reproduced here., A compactified-space integer statement assumes U approaches one constant at spatial infinity; the hedgehog statement additionally assumes sufficient smoothness and regularity at the origin and infinity for the displayed boundary reduction., The minus normalization is a declared orientation convention derived from the positive generator period and selected so F(0)=pi to F(infinity)=0 has charge +1; the positive quaternion generator consequently has normalized period -1., No accepted action couples this current to an external U(1), derives it from WZW descent, or maps its integer to a physical baryon or microscopic color count.. Comparators: none.

## Provenance and Evidence
The accepted release and immutable campaign evidence are the authoritative pointers.

Accepted in `v0.52.0` with provenance `campaigns/P058-wz3-su3-winding-current/adjudication.yaml`.

- `campaigns/P058-wz3-su3-winding-current/verify.py`
- `campaigns/P058-wz3-su3-winding-current/attempts/0002/result.yaml`
- `campaigns/P058-wz3-su3-winding-current/attempts/0003/result.yaml`
- `campaigns/P058-wz3-su3-winding-current/reviews/independent_winding_review.py`
- `campaigns/P058-wz3-su3-winding-current/reviews/source_adjudication.md`
- `campaigns/P058-wz3-su3-winding-current/evidence/topology-anomaly-provenance.yaml`
- `memory/vantasner/decisions/C-TOP-002-review.md`
- `tests/test_wzw.py`
